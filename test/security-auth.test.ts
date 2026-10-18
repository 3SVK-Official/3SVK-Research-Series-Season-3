import assert from "node:assert/strict";
import { after, describe, it } from "node:test";
import type { AddressInfo } from "node:net";
import type { AuthenticationService, AuthenticatedPrincipal } from "../src/security/oidc-auth.js";
import {
  canImportEvents,
  canReviewIncidents,
  readOidcSettings
} from "../src/security/oidc-auth.js";
import { createAppServer } from "../src/server.js";

describe("OIDC configuration and workspace authorization", () => {
  it("requires explicit issuer, client credentials, base URL, and membership configuration", () => {
    assert.throws(
      () => readOidcSettings({}),
      /OIDC mode requires OIDC_ISSUER_URL/
    );
    assert.throws(
      () => readOidcSettings({
        OIDC_ISSUER_URL: "https://identity.example",
        OIDC_CLIENT_ID: "sentinel",
        OIDC_CLIENT_SECRET: "test-secret",
        APP_BASE_URL: "https://sentinel.example/"
      }),
      /OIDC_MEMBERSHIPS_JSON/
    );
  });

  it("requires loopback HTTP for local development and HTTPS for production", () => {
    const base = {
      OIDC_ISSUER_URL: "http://127.0.0.1:8080/realms/test",
      OIDC_CLIENT_ID: "sentinel",
      OIDC_CLIENT_SECRET: "test-secret",
      APP_BASE_URL: "http://127.0.0.1:4173/",
      OIDC_MEMBERSHIPS_JSON: JSON.stringify({
        "subject-1": { tenantId: "tenant-a", role: "admin" }
      })
    };
    assert.equal(readOidcSettings(base).memberships.size, 1);
    assert.throws(
      () => readOidcSettings({
        ...base,
        NODE_ENV: "production"
      }),
      /must use HTTPS in production/
    );
    assert.throws(
      () => readOidcSettings({
        ...base,
        OIDC_ISSUER_URL: "http://identity.example"
      }),
      /must use HTTPS except for loopback/
    );
    assert.throws(
      () => readOidcSettings({
        ...base,
        OIDC_TOKEN_AUTH_METHOD: "unsupported"
      }),
      /token authentication method are invalid/
    );
  });

  it("enforces least-privilege role capabilities", () => {
    assert.equal(canReviewIncidents("viewer"), false);
    assert.equal(canReviewIncidents("analyst"), true);
    assert.equal(canImportEvents("analyst"), false);
    assert.equal(canImportEvents("admin"), true);
  });
});

describe("OIDC tenant-scoped local API", () => {
  let server: ReturnType<typeof createAppServer>;
  let baseUrl: string;
  const principals = new Map<string, AuthenticatedPrincipal>([
    ["admin-session", {
      subject: "admin-sub",
      tenantId: "tenant-a",
      role: "admin"
    }],
    ["viewer-session", {
      subject: "viewer-sub",
      tenantId: "tenant-b",
      role: "viewer"
    }]
  ]);
  let expectedOrigin = "";

  const authenticator: AuthenticationService = {
    async beginLogin() {
      return {
        flowId: "test-flow",
        authorizationUrl: new URL("https://identity.example/authorize")
      };
    },
    async completeLogin() {
      return undefined;
    },
    getPrincipal(sessionId) {
      const principal = sessionId ? principals.get(sessionId) : undefined;
      return principal ? structuredClone(principal) : undefined;
    },
    revokeSession(sessionId) {
      if (sessionId) principals.delete(sessionId);
    },
    usesSecureCookies() {
      return true;
    },
    acceptsOrigin(origin) {
      return origin === expectedOrigin;
    },
    callbackUrl(search) {
      return new URL(`https://sentinel.example/auth/callback${search}`);
    }
  };

  after(async () => {
    if (server?.listening) {
      await new Promise<void>((resolve, reject) => {
        server.close((error) => error ? reject(error) : resolve());
      });
    }
  });

  it("requires a session and isolates imported events and workflow by tenant", async () => {
    server = createAppServer(undefined, { authMode: "oidc", authenticator });
    await new Promise<void>((resolve, reject) => {
      server.once("error", reject);
      server.listen(0, "127.0.0.1", resolve);
    });
    const address = server.address() as AddressInfo;
    baseUrl = `http://127.0.0.1:${address.port}`;
    expectedOrigin = baseUrl;

    const unauthenticated = await fetch(`${baseUrl}/api/v1/events`);
    assert.equal(unauthenticated.status, 401);
    const landing = await fetch(baseUrl, { redirect: "manual" });
    assert.equal(landing.status, 302);
    assert.equal(landing.headers.get("location"), "/auth/login");
    const loginStart = await fetch(`${baseUrl}/auth/login`, { redirect: "manual" });
    assert.equal(loginStart.status, 302);
    assert.match(loginStart.headers.get("set-cookie") ?? "", /HttpOnly; SameSite=Lax; Secure/);

    const adminCaseUpdate = await fetch(
      `${baseUrl}/api/v1/incidents/${encodeURIComponent("auth-sequence:demo-002")}`,
      {
        method: "PATCH",
        headers: {
          "content-type": "application/json",
          cookie: "sentinel_session=admin-session",
          origin: baseUrl
        },
        body: JSON.stringify({ status: "investigating" })
      }
    );
    assert.equal(adminCaseUpdate.status, 200);

    const tenantBIncidentsResponse = await fetch(`${baseUrl}/api/v1/incidents`, {
      headers: { cookie: "sentinel_session=viewer-session" }
    });
    const tenantBIncidents = await tenantBIncidentsResponse.json() as {
      incidents: Array<{ id: string; status: string }>;
    };
    assert.equal(
      tenantBIncidents.incidents.find((incident) => incident.id === "auth-sequence:demo-002")?.status,
      "new"
    );

    const imported = await fetch(`${baseUrl}/api/v1/events/import`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: "sentinel_session=admin-session",
        origin: baseUrl
      },
      body: JSON.stringify({
        events: [{
          id: "tenant-a-event",
          source: "test",
          observedAt: "2026-10-18T00:00:00.000Z",
          eventType: "test.alert",
          severity: "low",
          summary: "Synthetic tenant A event.",
          entities: []
        }]
      })
    });
    assert.equal(imported.status, 200);

    const tenantAEvents = await fetch(`${baseUrl}/api/v1/events`, {
      headers: { cookie: "sentinel_session=admin-session" }
    });
    const tenantA = await tenantAEvents.json() as {
      mode: string;
      events: Array<{ id: string }>;
    };
    assert.equal(tenantA.mode, "uploaded");
    assert.deepEqual(tenantA.events.map((event) => event.id), ["tenant-a-event"]);

    const tenantBEvents = await fetch(`${baseUrl}/api/v1/events`, {
      headers: { cookie: "sentinel_session=viewer-session" }
    });
    const tenantB = await tenantBEvents.json() as {
      mode: string;
      events: Array<{ id: string }>;
    };
    assert.equal(tenantB.mode, "demo");
    assert.equal(tenantB.events.some((event) => event.id === "tenant-a-event"), false);

    const deniedImport = await fetch(`${baseUrl}/api/v1/events/import`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: "sentinel_session=viewer-session",
        origin: baseUrl
      },
      body: JSON.stringify({ events: [] })
    });
    assert.equal(deniedImport.status, 403);

    const deniedCaseUpdate = await fetch(
      `${baseUrl}/api/v1/incidents/${encodeURIComponent("auth-sequence:demo-002")}`,
      {
        method: "PATCH",
        headers: {
          "content-type": "application/json",
          cookie: "sentinel_session=viewer-session",
          origin: baseUrl
        },
        body: JSON.stringify({ status: "investigating" })
      }
    );
    assert.equal(deniedCaseUpdate.status, 403);

    const deniedCrossOrigin = await fetch(`${baseUrl}/api/v1/events/reset-demo`, {
      method: "POST",
      headers: {
        cookie: "sentinel_session=admin-session",
        origin: "https://attacker.example"
      }
    });
    assert.equal(deniedCrossOrigin.status, 403);

    const logout = await fetch(`${baseUrl}/auth/logout`, {
      method: "POST",
      headers: {
        cookie: "sentinel_session=admin-session",
        origin: baseUrl
      },
      redirect: "manual"
    });
    assert.equal(logout.status, 303);
    assert.match(logout.headers.get("set-cookie") ?? "", /sentinel_session=;.*Max-Age=0/);
    const afterLogout = await fetch(`${baseUrl}/api/v1/events`, {
      headers: { cookie: "sentinel_session=admin-session" }
    });
    assert.equal(afterLogout.status, 401);
  });
});
