import assert from "node:assert/strict";
import { after, before, describe, it } from "node:test";
import type { AddressInfo } from "node:net";
import { findAuthenticationSequenceCandidates } from "../src/analysis/authentication-sequence.js";
import { InMemoryIncidentWorkflow } from "../src/analysis/incident-workflow.js";
import { createDemoConnector } from "../src/connectors/demo-connector.js";
import type { SecurityEvent } from "../src/domain/security-event.js";
import { MAX_IMPORT_BYTES } from "../src/ingestion/validate-event-import.js";
import { createAppServer } from "../src/server.js";

function authenticationEvent(
  id: string,
  eventType: string,
  observedAt: string
): SecurityEvent {
  return {
    id,
    source: "test",
    observedAt,
    eventType,
    severity: "medium",
    summary: id,
    entities: [{ kind: "user", value: "test@example.test" }]
  };
}

describe("authentication sequence analysis", () => {
  it("matches an account's events within the ten-minute boundary", () => {
    const candidates = findAuthenticationSequenceCandidates([
      authenticationEvent("success", "authentication.success", "2026-10-17T09:10:00.000Z"),
      authenticationEvent("failure", "authentication.failure", "2026-10-17T09:00:00.000Z")
    ]);

    assert.equal(candidates.length, 1);
    assert.deepEqual(
      candidates[0].evidence.map((event) => event.eventId),
      ["failure", "success"]
    );
  });

  it("does not match events outside the ten-minute window", () => {
    const candidates = findAuthenticationSequenceCandidates([
      authenticationEvent("failure", "authentication.failure", "2026-10-17T09:00:00.000Z"),
      authenticationEvent("success", "authentication.success", "2026-10-17T09:10:00.001Z")
    ]);

    assert.equal(candidates.some(
      (candidate) => candidate.rule === "authentication-failures-followed-by-success"
    ), false);
    assert.equal(candidates.length, 2);
  });
});

describe("incident workflow", () => {
  it("tracks allowed status transitions and returns detached history", () => {
    const workflow = new InMemoryIncidentWorkflow();
    const initial = workflow.get("incident-1", "2026-10-18T00:00:00.000Z");
    assert.equal(initial.status, "new");

    const investigating = workflow.transition(
      "incident-1",
      "investigating",
      "2026-10-18T00:05:00.000Z"
    );
    assert.equal(investigating?.status, "investigating");
    assert.deepEqual(investigating?.history, [{
      from: "new",
      to: "investigating",
      changedAt: "2026-10-18T00:05:00.000Z"
    }]);

    const resolved = workflow.transition(
      "incident-1",
      "resolved",
      "2026-10-18T00:10:00.000Z"
    );
    assert.equal(resolved?.status, "resolved");
    assert.equal(resolved?.history.length, 2);
    assert.equal(workflow.transition("incident-1", "new"), undefined);

    investigating!.history.length = 0;
    assert.equal(workflow.get("incident-1").history.length, 2);
  });
});

describe("local incident-response API", () => {
  let server: ReturnType<typeof createAppServer>;
  let baseUrl: string;

  before(async () => {
    server = createAppServer();
    await new Promise<void>((resolve, reject) => {
      server.once("error", reject);
      server.listen(0, "127.0.0.1", resolve);
    });

    const address = server.address() as AddressInfo;
    baseUrl = `http://127.0.0.1:${address.port}`;
  });

  after(async () => {
    await new Promise<void>((resolve, reject) => {
      server.close((error) => error ? reject(error) : resolve());
    });
  });

  it("serves the local review dashboard with a restrictive content policy", async () => {
    const response = await fetch(`${baseUrl}/`);
    const html = await response.text();

    assert.equal(response.status, 200);
    assert.match(response.headers.get("content-type") ?? "", /text\/html/);
    assert.match(
      response.headers.get("content-security-policy") ?? "",
      /script-src 'self'/
    );
    assert.match(html, /Incident queue/);
  });

  it("serves the dashboard assets without allowing arbitrary file paths", async () => {
    const scriptResponse = await fetch(`${baseUrl}/app.js`);
    assert.equal(scriptResponse.status, 200);
    assert.match(scriptResponse.headers.get("content-type") ?? "", /javascript/);

    const traversalResponse = await fetch(`${baseUrl}/..%2fpackage.json`);
    assert.equal(traversalResponse.status, 404);
  });

  it("serves the normalized event import template", async () => {
    const response = await fetch(`${baseUrl}/event-import-template.json`);
    const body = await response.json() as { events: Array<{ id: string }> };

    assert.equal(response.status, 200);
    assert.equal(body.events.length, 2);
    assert.equal(response.headers.get("content-type"), "application/json; charset=utf-8");
  });

  it("serves the Wazuh JSON-lines example", async () => {
    const response = await fetch(`${baseUrl}/wazuh-alerts-example.jsonl`);
    const body = await response.text();

    assert.equal(response.status, 200);
    assert.match(response.headers.get("content-type") ?? "", /application\/x-ndjson/);
    assert.equal(body.trim().split(/\r?\n/).length, 2);
  });

  it("serves only normalized demo security events", async () => {
    const response = await fetch(`${baseUrl}/api/v1/events`);
    const body = await response.json() as { events: Array<Record<string, unknown>> };

    assert.equal(response.status, 200);
    assert.equal(body.events.length, 3);
    assert.equal(body.events[0].source, "demo");
    assert.equal("rawData" in body.events[0], false);
    assert.equal(response.headers.get("cache-control"), "no-store");
  });

  it("exposes a minimal health endpoint", async () => {
    const response = await fetch(`${baseUrl}/healthz`);
    assert.equal(response.status, 200);
    assert.deepEqual(await response.json(), { status: "ok" });
  });

  it("serves a public demo as read-only and rejects every mutation method", async () => {
    const publicDemo = createAppServer(createDemoConnector(), { readOnlyDemo: true });
    await new Promise<void>((resolve, reject) => {
      publicDemo.once("error", reject);
      publicDemo.listen(0, "127.0.0.1", resolve);
    });
    const address = publicDemo.address() as AddressInfo;
    const publicUrl = `http://127.0.0.1:${address.port}`;

    try {
      const identityResponse = await fetch(`${publicUrl}/api/v1/me`);
      const identity = await identityResponse.json() as {
        role: string;
        readOnly: boolean;
      };
      assert.equal(identity.role, "viewer");
      assert.equal(identity.readOnly, true);

      const pathsAndMethods = [
        ["/api/v1/events/import", "POST"],
        ["/api/v1/events/import/wazuh", "POST"],
        ["/api/v1/events/reset-demo", "POST"],
        ["/api/v1/incidents/auth-sequence%3Ademo-002", "PATCH"]
      ] as const;
      for (const [path, method] of pathsAndMethods) {
        const response = await fetch(`${publicUrl}${path}`, {
          method,
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ status: "resolved", events: [] })
        });
        assert.equal(response.status, 405, `${method} ${path}`);
        assert.equal(response.headers.get("allow"), "GET");
        assert.deepEqual(await response.json(), {
          error: "This public demo is read-only."
        });
      }

      const eventsResponse = await fetch(`${publicUrl}/api/v1/events`);
      const events = await eventsResponse.json() as {
        mode: string;
        events: Array<{ source: string }>;
      };
      assert.equal(events.mode, "demo");
      assert.equal(events.events.length, 3);
      assert.equal(events.events[0].source, "demo");
    } finally {
      await new Promise<void>((resolve, reject) => {
        publicDemo.close((error) => error ? reject(error) : resolve());
      });
    }
  });

  it("does not allow read-only public demo mode with a live connector", () => {
    assert.throws(
      () => createAppServer({
        name: "live-test",
        mode: "live",
        async fetchEvents() {
          return [];
        }
      }, { readOnlyDemo: true }),
      /requires local authentication and the demo connector/
    );
  });

  it("allows same-origin public demo imports but blocks resets and case updates", async () => {
    const publicDemo = createAppServer(createDemoConnector(), {
      readOnlyDemo: true,
      publicDemoImports: true
    });
    await new Promise<void>((resolve, reject) => {
      publicDemo.once("error", reject);
      publicDemo.listen(0, "127.0.0.1", resolve);
    });
    const address = publicDemo.address() as AddressInfo;
    const publicUrl = `http://127.0.0.1:${address.port}`;

    try {
      const identityResponse = await fetch(`${publicUrl}/api/v1/me`);
      const identity = await identityResponse.json() as {
        role: string;
        canImportEvents: boolean;
        readOnly: boolean;
      };
      assert.equal(identity.role, "viewer");
      assert.equal(identity.canImportEvents, true);
      assert.equal(identity.readOnly, true);

      const maliciousOrigin = await fetch(`${publicUrl}/api/v1/events/import`, {
        method: "POST",
        headers: {
          "content-type": "application/json",
          origin: "https://attacker.example"
        },
        body: JSON.stringify({ events: [] })
      });
      assert.equal(maliciousOrigin.status, 403);

      const importedEvent = {
        id: "public-demo-import",
        source: "public-demo",
        observedAt: "2026-10-18T10:00:00.000Z",
        eventType: "test.alert",
        severity: "medium",
        summary: "Synthetic event uploaded to the public demo.",
        entities: []
      };
      const importResponse = await fetch(`${publicUrl}/api/v1/events/import`, {
        method: "POST",
        headers: {
          "content-type": "application/json",
          origin: publicUrl
        },
        body: JSON.stringify({ events: [importedEvent] })
      });
      assert.equal(importResponse.status, 200);
      assert.deepEqual(await importResponse.json(), {
        imported: 1,
        mode: "uploaded",
        format: "normalized-json"
      });

      const eventsResponse = await fetch(`${publicUrl}/api/v1/events`);
      const events = await eventsResponse.json() as {
        mode: string;
        events: Array<{ id: string }>;
      };
      assert.equal(events.mode, "uploaded");
      assert.deepEqual(events.events.map((event) => event.id), ["public-demo-import"]);

      for (const [path, method] of [
        ["/api/v1/events/reset-demo", "POST"],
        ["/api/v1/incidents/auth-sequence%3Ademo-002", "PATCH"]
      ] as const) {
        const response = await fetch(`${publicUrl}${path}`, {
          method,
          headers: {
            "content-type": "application/json",
            origin: publicUrl
          },
          body: JSON.stringify({ status: "resolved" })
        });
        assert.equal(response.status, 405, `${method} ${path}`);
      }
    } finally {
      await new Promise<void>((resolve, reject) => {
        publicDemo.close((error) => error ? reject(error) : resolve());
      });
    }
  });

  it("reports live connector mode and query limits without claiming in-memory persistence", async () => {
    const liveServer = createAppServer({
      name: "wazuh-indexer",
      mode: "live",
      limits: { maxEvents: 500, lookbackHours: 12 },
      async fetchEvents() {
        return [authenticationEvent(
          "live-alert",
          "wazuh.rule.9001",
          "2026-10-18T01:00:00.000Z"
        )];
      }
    });
    await new Promise<void>((resolve, reject) => {
      liveServer.once("error", reject);
      liveServer.listen(0, "127.0.0.1", resolve);
    });
    const address = liveServer.address() as AddressInfo;

    try {
      const response = await fetch(`http://127.0.0.1:${address.port}/api/v1/events`);
      const body = await response.json() as {
        mode: string;
        persistence: string;
        source: string;
        limits: { maxEvents: number; lookbackHours: number };
      };
      assert.equal(body.mode, "live");
      assert.equal(body.persistence, "source");
      assert.equal(body.source, "wazuh-indexer");
      assert.deepEqual(body.limits, { maxEvents: 500, lookbackHours: 12 });
    } finally {
      await new Promise<void>((resolve, reject) => {
        liveServer.close((error) => error ? reject(error) : resolve());
      });
    }
  });

  it("returns a review candidate with linked evidence for the demo sequence", async () => {
    const response = await fetch(`${baseUrl}/api/v1/incidents`);
    const body = await response.json() as {
      incidents: Array<{
        title: string;
        evidence: Array<{ eventId: string }>;
        requiresHumanReview: boolean;
      }>;
    };

    assert.equal(response.status, 200);
    assert.equal(body.incidents.length, 2);
    assert.equal(body.incidents[0].title, "Security alert requires review");
    assert.deepEqual(
      body.incidents[1].evidence.map((item) => item.eventId),
      ["demo-001", "demo-002"]
    );
    assert.equal(body.incidents[1].requiresHumanReview, true);
  });

  it("supports incident lifecycle updates with an in-memory status history", async () => {
    const listResponse = await fetch(`${baseUrl}/api/v1/incidents`);
    const listed = await listResponse.json() as {
      incidents: Array<{ id: string; status: string }>;
    };
    const incident = listed.incidents.find((item) => item.id === "auth-sequence:demo-002");
    assert.ok(incident);
    assert.equal(incident.status, "new");

    const update = async (status: string) => fetch(
      `${baseUrl}/api/v1/incidents/${encodeURIComponent(incident.id)}`,
      {
        method: "PATCH",
        headers: {
          "content-type": "application/json",
          origin: baseUrl
        },
        body: JSON.stringify({ status })
      }
    );

    const investigatingResponse = await update("investigating");
    assert.equal(investigatingResponse.status, 200);
    const investigating = await investigatingResponse.json() as {
      incident: { status: string; history: Array<{ from: string; to: string; changedAt: string }> };
    };
    assert.equal(investigating.incident.status, "investigating");
    assert.equal(investigating.incident.history[0].from, "new");
    assert.equal(investigating.incident.history[0].to, "investigating");
    assert.ok(Number.isFinite(Date.parse(investigating.incident.history[0].changedAt)));

    const resolvedResponse = await update("resolved");
    assert.equal(resolvedResponse.status, 200);
    const invalidTransition = await update("new");
    assert.equal(invalidTransition.status, 409);

    const refreshed = await fetch(`${baseUrl}/api/v1/incidents`);
    const current = await refreshed.json() as {
      incidents: Array<{ id: string; status: string; history: unknown[] }>;
    };
    const currentIncident = current.incidents.find((item) => item.id === incident.id);
    assert.equal(currentIncident?.status, "resolved");
    assert.equal(currentIncident?.history.length, 2);

    const invalidOrigin = await fetch(
      `${baseUrl}/api/v1/incidents/${encodeURIComponent(incident.id)}`,
      {
        method: "PATCH",
        headers: {
          "content-type": "application/json",
          origin: "https://attacker.example"
        },
        body: JSON.stringify({ status: "investigating" })
      }
    );
    assert.equal(invalidOrigin.status, 403);

    const malformed = await fetch(`${baseUrl}/api/v1/incidents/not-a-real-incident`, {
      method: "PATCH",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ status: "investigating" })
    });
    assert.equal(malformed.status, 404);

    await fetch(`${baseUrl}/api/v1/events/reset-demo`, { method: "POST" });
  });

  it("returns standalone candidates for critical alerts and account creation events", async () => {
    const connector = createAppServer({
      name: "candidate-test",
      async fetchEvents() {
        return [
          {
            id: "critical-alert",
            source: "wazuh",
            observedAt: "2026-10-18T01:10:05.123Z",
            eventType: "file.discovery",
            severity: "critical",
            summary: "Access to hidden file or directory found.",
            entities: [
              { kind: "host", value: "prod-app-server-02" },
              { kind: "user", value: "www-data" }
            ]
          },
          {
            id: "new-account",
            source: "wazuh",
            observedAt: "2026-10-18T01:12:44.456Z",
            eventType: "account.creation",
            severity: "medium",
            summary: "New user added to the system.",
            entities: [
              { kind: "host", value: "corporate-dc-01" },
              { kind: "user", value: "backdoor_admin" }
            ]
          }
        ];
      }
    });
    await new Promise<void>((resolve) => connector.listen(0, "127.0.0.1", resolve));
    const address = connector.address() as AddressInfo;

    try {
      const response = await fetch(`http://127.0.0.1:${address.port}/api/v1/incidents`);
      const body = await response.json() as {
        incidents: Array<{ title: string; priority: string; evidence: Array<{ eventId: string }> }>;
      };

      assert.equal(body.incidents.length, 2);
      assert.deepEqual(body.incidents.map((item) => item.title), [
        "New account created",
        "Sensitive file or directory discovery"
      ]);
      assert.deepEqual(body.incidents.map((item) => item.priority), ["medium", "critical"]);
    } finally {
      await new Promise<void>((resolve, reject) => {
        connector.close((error) => error ? reject(error) : resolve());
      });
    }
  });

  it("does not accept write requests", async () => {
    const response = await fetch(`${baseUrl}/api/v1/events`, { method: "POST" });
    assert.equal(response.status, 405);
    assert.equal(response.headers.get("allow"), "GET");
  });

  it("rejects cross-origin mutation requests before reading or changing imported data", async () => {
    const response = await fetch(`${baseUrl}/api/v1/events/import`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        origin: "https://attacker.example"
      },
      body: JSON.stringify({ events: [] })
    });

    assert.equal(response.status, 403);
    assert.deepEqual(await response.json(), {
      error: "Cross-origin requests are not allowed."
    });

    const eventsResponse = await fetch(`${baseUrl}/api/v1/events`);
    const events = await eventsResponse.json() as { mode: string; events: unknown[] };
    assert.equal(events.mode, "demo");
    assert.equal(events.events.length, 3);
  });

  it("imports validated events in memory, preserves prior data on failure, and resets to the demo", async () => {
    const event = {
      id: "import-failure",
      source: "test-import",
      observedAt: "2026-10-17T09:00:00.000Z",
      eventType: "authentication.failure",
      severity: "medium",
      summary: "Test failed sign-in.",
      entities: [{ kind: "user", value: "import@example.test" }]
    };
    const successfulEvent = {
      ...event,
      id: "import-success",
      observedAt: "2026-10-17T09:05:00.000Z",
      eventType: "authentication.success",
      severity: "high",
      summary: "Test successful sign-in."
    };

    const importResponse = await fetch(`${baseUrl}/api/v1/events/import`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        origin: baseUrl
      },
      body: JSON.stringify({ events: [event, successfulEvent] })
    });
    assert.equal(importResponse.status, 200);
    assert.deepEqual(await importResponse.json(), {
      imported: 2,
      mode: "uploaded",
      format: "normalized-json"
    });

    const eventsResponse = await fetch(`${baseUrl}/api/v1/events`);
    const imported = await eventsResponse.json() as {
      events: Array<{ id: string }>;
      mode: string;
      persistence: string;
    };
    assert.equal(imported.mode, "uploaded");
    assert.equal(imported.persistence, "memory-only");
    assert.deepEqual(imported.events.map((item) => item.id), ["import-failure", "import-success"]);

    const incidentResponse = await fetch(`${baseUrl}/api/v1/incidents`);
    const incidents = await incidentResponse.json() as {
      incidents: Array<{ evidence: Array<{ eventId: string }> }>;
    };
    assert.deepEqual(
      incidents.incidents[0].evidence.map((item) => item.eventId),
      ["import-failure", "import-success"]
    );

    const invalidResponse = await fetch(`${baseUrl}/api/v1/events/import`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ events: [{ ...event, rawLog: "should be rejected" }] })
    });
    assert.equal(invalidResponse.status, 400);

    const retainedResponse = await fetch(`${baseUrl}/api/v1/events`);
    const retained = await retainedResponse.json() as { events: Array<{ id: string }> };
    assert.deepEqual(retained.events.map((item) => item.id), ["import-failure", "import-success"]);

    const resetResponse = await fetch(`${baseUrl}/api/v1/events/reset-demo`, { method: "POST" });
    assert.equal(resetResponse.status, 200);
    const restoredResponse = await fetch(`${baseUrl}/api/v1/events`);
    const restored = await restoredResponse.json() as {
      events: Array<{ source: string }>;
      mode: string;
    };
    assert.equal(restored.mode, "demo");
    assert.equal(restored.events.length, 3);
    assert.equal(restored.events[0].source, "demo");
  });

  it("imports Wazuh JSON-lines alerts into normalized events without retaining raw logs", async () => {
    const wazuhAlert = {
      id: "wazuh-test-1",
      timestamp: "2026-10-17T09:14:00.000+0000",
      rule: {
        level: 5,
        description: "Synthetic failed login",
        id: "5503",
        groups: ["authentication_failed"],
        mitre: {
          id: ["T1110"],
          tactic: ["Credential Access"],
          technique: ["Brute Force"]
        }
      },
      agent: { id: "001", name: "test-host" },
      data: { srcuser: "test@example.test", srcip: "192.0.2.14" },
      full_log: "Sensitive raw log must not be returned."
    };
    const successfulAlert = {
      ...wazuhAlert,
      id: "wazuh-test-2",
      timestamp: "2026-10-17T09:15:00.000+0000",
      rule: {
        level: 10,
        description: "Synthetic successful login",
        id: "5715",
        groups: ["authentication_success"]
      }
    };
    const response = await fetch(`${baseUrl}/api/v1/events/import/wazuh`, {
      method: "POST",
      headers: { "content-type": "application/x-ndjson" },
      body: `${JSON.stringify(wazuhAlert)}\n${JSON.stringify(successfulAlert)}\n`
    });

    assert.equal(response.status, 200);
    assert.deepEqual(await response.json(), {
      imported: 2,
      mode: "uploaded",
      format: "wazuh-json-lines"
    });

    const eventsResponse = await fetch(`${baseUrl}/api/v1/events`);
    const events = await eventsResponse.json() as {
      events: Array<{
        eventType: string;
        source: string;
        wazuh?: {
          ruleId: string;
          groups: string[];
          mitre: { ids: string[] };
        };
      }>;
      format: string;
    };
    assert.equal(events.format, "wazuh-json-lines");
    assert.equal(events.events[0].eventType, "authentication.failure");
    assert.equal(events.events[0].source, "wazuh");
    assert.deepEqual(events.events[0].wazuh, {
      ruleId: "5503",
      level: 5,
      groups: ["authentication_failed"],
      mitre: {
        ids: ["T1110"],
        tactics: ["Credential Access"],
        techniques: ["Brute Force"]
      },
      agentId: "001",
      agentName: "test-host"
    });
    assert.equal(JSON.stringify(events).includes("Sensitive raw log"), false);

    const incidentsResponse = await fetch(`${baseUrl}/api/v1/incidents`);
    const incidents = await incidentsResponse.json() as {
      incidents: Array<{
        evidence: Array<{ eventId: string }>;
        wazuhAlerts?: Array<{ context: { ruleId: string; mitre: { ids: string[] } } }>;
      }>;
    };
    assert.deepEqual(
      incidents.incidents[0].evidence.map((item) => item.eventId),
      ["wazuh-test-1", "wazuh-test-2"]
    );
    assert.deepEqual(
      incidents.incidents[0].wazuhAlerts?.map((alert) => alert.context.mitre.ids),
      [["T1110"], []]
    );

    await fetch(`${baseUrl}/api/v1/events/reset-demo`, { method: "POST" });
  });

  it("imports single-alert and events-wrapped Wazuh JSON files through either import action", async () => {
    const alert = {
      id: "wazuh-json-alert",
      timestamp: "2026-10-18T00:54:21.104+0000",
      rule: {
        level: 10,
        description: "sshd: SSH insecure connection attempt - brute force attack.",
        id: "5712",
        groups: ["syslog", "sshd", "authentication_failures"]
      },
      agent: { id: "004", name: "prod-web-server-01", ip: "192.168.10.45" },
      data: {
        srcip: "203.0.113.89",
        srcport: "49231",
        dstuser: "root",
        system_name: "ubuntu-server"
      },
      full_log: "Raw log fields must not be retained."
    };

    const importCases = [
      { path: "/api/v1/events/import/wazuh", document: alert },
      { path: "/api/v1/events/import/wazuh", document: { events: [alert] } },
      { path: "/api/v1/events/import", document: alert }
    ];

    for (const { path, document } of importCases) {
      const response = await fetch(`${baseUrl}${path}`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(document)
      });
      assert.equal(response.status, 200);

      const eventsResponse = await fetch(`${baseUrl}/api/v1/events`);
      const events = await eventsResponse.json() as {
        events: Array<Record<string, unknown>>;
        format: string;
      };
      assert.equal(events.events.length, 1);
      assert.equal(events.events[0].eventType, "authentication.failure");
      assert.equal(events.events[0].severity, "high");
      assert.equal(events.format, "wazuh-json");
      assert.equal(JSON.stringify(events).includes("Raw log fields"), false);

      await fetch(`${baseUrl}/api/v1/events/reset-demo`, { method: "POST" });
    }
  });

  it("rejects invalid Wazuh JSON-lines without replacing the current event set", async () => {
    const response = await fetch(`${baseUrl}/api/v1/events/import/wazuh`, {
      method: "POST",
      headers: { "content-type": "application/x-ndjson" },
      body: '{"id":"incomplete"}'
    });
    assert.equal(response.status, 400);

    const eventsResponse = await fetch(`${baseUrl}/api/v1/events`);
    const events = await eventsResponse.json() as { mode: string };
    assert.equal(events.mode, "demo");
  });

  it("returns an actionable hint when normalized event JSON is sent to the Wazuh importer", async () => {
    const response = await fetch(`${baseUrl}/api/v1/events/import/wazuh`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        events: [{
          id: "normalized-test",
          source: "test",
          observedAt: "2026-10-17T09:14:00.000Z",
          eventType: "authentication.failure",
          severity: "medium",
          summary: "Normalized test event.",
          entities: []
        }]
      })
    });

    assert.equal(response.status, 400);
    assert.deepEqual(await response.json(), {
      error: "This file is already in normalized event format. Use Import JSON instead of Import Wazuh."
    });
  });

  it("allows only POST on import and reset endpoints", async () => {
    const response = await fetch(`${baseUrl}/api/v1/events/import/wazuh`);
    assert.equal(response.status, 405);
    assert.equal(response.headers.get("allow"), "POST");
  });

  it("requires JSON and rejects malformed imports without replacing the demo", async () => {
    const wrongType = await fetch(`${baseUrl}/api/v1/events/import`, {
      method: "POST",
      headers: { "content-type": "text/plain" },
      body: "{}"
    });
    assert.equal(wrongType.status, 415);

    const malformed = await fetch(`${baseUrl}/api/v1/events/import`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: "{"
    });
    assert.equal(malformed.status, 400);

    const eventsResponse = await fetch(`${baseUrl}/api/v1/events`);
    const result = await eventsResponse.json() as { mode: string };
    assert.equal(result.mode, "demo");
  });

  it("rejects event import bodies above the byte limit", async () => {
    const oversized = " ".repeat(MAX_IMPORT_BYTES + 1);
    const response = await fetch(`${baseUrl}/api/v1/events/import`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: oversized
    });

    assert.equal(response.status, 413);
    assert.deepEqual(await response.json(), {
      error: "Import exceeds the 1 MiB size limit."
    });
  });

  it("returns a generic service error when a connector fails", async () => {
    const failingServer = createAppServer({
      name: "failing-test",
      async fetchEvents() {
        throw new Error("sensitive connector detail");
      }
    });
    await new Promise<void>((resolve) => failingServer.listen(0, "127.0.0.1", resolve));
    const address = failingServer.address() as AddressInfo;

    try {
      const response = await fetch(`http://127.0.0.1:${address.port}/api/v1/events`);
      assert.equal(response.status, 503);
      assert.deepEqual(await response.json(), {
        error: "Alert source is temporarily unavailable"
      });
    } finally {
      await new Promise<void>((resolve, reject) => {
        failingServer.close((error) => error ? reject(error) : resolve());
      });
    }
  });

  it("rejects invalid event timestamps instead of silently skipping them", async () => {
    const connector = createDemoConnector();
    const events = await connector.fetchEvents();
    events[0].observedAt = "not-a-timestamp";

    assert.throws(
      () => findAuthenticationSequenceCandidates(events),
      /Invalid observedAt timestamp on event: demo-001/
    );
  });
});
