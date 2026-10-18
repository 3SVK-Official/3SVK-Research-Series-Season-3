import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  normalizeWazuhAlert,
  normalizeWazuhJson,
  normalizeWazuhJsonDocument,
  normalizeWazuhJsonLines
} from "../src/connectors/wazuh/alert-import.js";
import { findAuthenticationSequenceCandidates } from "../src/analysis/authentication-sequence.js";

const failedLogin = {
  id: "1718000000.1001",
  timestamp: "2026-10-17T09:14:00.000+0000",
  rule: {
    level: 5,
    description: "Multiple authentication failures for one account",
    id: "5503",
    groups: ["authentication_failed"]
  },
  agent: { id: "001", name: "lab-workstation-07" },
  data: {
    srcuser: "analyst@example.test",
    srcip: "192.0.2.24",
    filename: "/tmp/example"
  },
  full_log: "Must not be copied into normalized event data."
};

describe("Wazuh JSON alert normalization", () => {
  it("maps known fields into the shared event model and excludes raw alert fields", () => {
    const event = normalizeWazuhAlert(failedLogin);

    assert.deepEqual(event, {
      id: "1718000000.1001",
      source: "wazuh",
      observedAt: "2026-10-17T09:14:00.000+00:00",
      eventType: "authentication.failure",
      severity: "medium",
      summary: "Multiple authentication failures for one account",
      entities: [
        { kind: "host", value: "lab-workstation-07" },
        { kind: "user", value: "analyst@example.test" },
        { kind: "ip", value: "192.0.2.24" },
        { kind: "file", value: "/tmp/example" }
      ],
      wazuh: {
        ruleId: "5503",
        level: 5,
        groups: ["authentication_failed"],
        mitre: { ids: [], tactics: [], techniques: [] },
        agentId: "001",
        agentName: "lab-workstation-07"
      }
    });
    assert.equal(JSON.stringify(event).includes("full_log"), false);
  });

  it("normalizes JSON-lines exports and maps Wazuh rule levels", () => {
    const secondAlert = {
      ...failedLogin,
      id: "1718000060.1002",
      timestamp: "2026-10-17T09:15:00.000+0000",
      rule: {
        level: 12,
        description: "Synthetic critical alert",
        id: "9001",
        groups: ["malware"]
      }
    };
    const events = normalizeWazuhJsonLines(
      `${JSON.stringify(failedLogin)}\n${JSON.stringify(secondAlert)}\n`
    );

    assert.equal(events.length, 2);
    assert.equal(events[0].eventType, "authentication.failure");
    assert.equal(events[0].severity, "medium");
    assert.equal(events[1].eventType, "malware.detected");
    assert.equal(events[1].severity, "critical");
  });

  it("preserves allowlisted Wazuh rule, ATT&CK, decoder, agent, and location context", () => {
    const event = normalizeWazuhAlert({
      ...failedLogin,
      rule: {
        ...failedLogin.rule,
        mitre: {
          id: ["T1110", "T1078"],
          tactic: ["Credential Access"],
          technique: ["Brute Force", "Valid Accounts"]
        }
      },
      agent: { id: "001", name: "lab-workstation-07", ip: "192.0.2.40" },
      decoder: { name: "sshd" },
      location: "/var/log/auth.log",
      full_log: "Must remain excluded."
    });

    assert.deepEqual(event.wazuh, {
      ruleId: "5503",
      level: 5,
      groups: ["authentication_failed"],
      mitre: {
        ids: ["T1110", "T1078"],
        tactics: ["Credential Access"],
        techniques: ["Brute Force", "Valid Accounts"]
      },
      agentId: "001",
      agentName: "lab-workstation-07",
      location: "/var/log/auth.log",
      decoderName: "sshd"
    });
    assert.deepEqual(event.entities.find((entity) => entity.kind === "ip"), {
      kind: "ip",
      value: "192.0.2.40"
    });
    assert.equal(JSON.stringify(event).includes("Must remain excluded"), false);
  });

  it("classifies additional Wazuh alert families", () => {
    const cases = [
      { groups: ["malware"], description: "Malware detected", expected: "malware.detected" },
      { groups: ["vulnerability-detector"], description: "CVE-2026-12345 found", expected: "vulnerability.detected" },
      { groups: ["privilege_escalation"], description: "Unexpected sudoers file change", expected: "privilege.escalation" },
      { groups: ["web_attack"], description: "Suspicious request", expected: "web.attack" },
      { groups: ["network_scan"], description: "Multiple ports probed", expected: "network.scan" },
      { groups: ["syscheck"], description: "File checksum changed", expected: "file.integrity.change" }
    ];

    for (const [index, item] of cases.entries()) {
      const event = normalizeWazuhAlert({
        ...failedLogin,
        id: `family-${index}`,
        rule: {
          level: 7,
          id: `${9000 + index}`,
          description: item.description,
          groups: item.groups
        }
      });
      assert.equal(event.eventType, item.expected, item.description);
    }
  });

  it("creates a human-review triage candidate for an otherwise unclassified low-severity alert", () => {
    const event = normalizeWazuhAlert({
      ...failedLogin,
      id: "unclassified-low",
      rule: {
        level: 2,
        id: "100",
        description: "A Wazuh alert outside the currently mapped families.",
        groups: ["syslog"]
      }
    });

    const [candidate] = findAuthenticationSequenceCandidates([event]);
    assert.equal(candidate.title, "Security alert requires review");
    assert.equal(candidate.priority, "review");
    assert.match(candidate.explanation, /not a confirmed incident/);
    assert.deepEqual(candidate.evidence.map((item) => item.eventId), ["unclassified-low"]);
  });

  it("returns source rule and MITRE context with the analyst review candidate", () => {
    const event = normalizeWazuhAlert({
      ...failedLogin,
      rule: {
        ...failedLogin.rule,
        mitre: { id: ["T1110"], tactic: ["Credential Access"], technique: ["Brute Force"] }
      }
    });

    const [candidate] = findAuthenticationSequenceCandidates([event]);
    assert.deepEqual(candidate.wazuhAlerts, [{
      eventId: event.id,
      context: event.wazuh
    }]);
  });

  it("accepts a single Wazuh alert object, an alert array, and an events wrapper", () => {
    const wrapped = { events: [failedLogin] };

    assert.equal(normalizeWazuhJson(JSON.stringify(failedLogin)).length, 1);
    assert.equal(normalizeWazuhJson(JSON.stringify([failedLogin])).length, 1);
    assert.equal(normalizeWazuhJson(JSON.stringify(wrapped)).length, 1);
    assert.equal(normalizeWazuhJsonDocument(wrapped)[0].source, "wazuh");
  });

  it("directs normalized event documents to the normalized JSON import action", () => {
    const normalizedDocument = {
      events: [{
        id: "normalized-1",
        source: "test",
        observedAt: "2026-10-17T09:14:00.000Z",
        eventType: "authentication.failure",
        severity: "medium",
        summary: "A normalized test event.",
        entities: []
      }]
    };

    assert.throws(
      () => normalizeWazuhJsonDocument(normalizedDocument),
      /already in normalized event format\. Use Import JSON instead of Import Wazuh/
    );
  });

  it("creates review candidates for high-severity alerts and account creation in the provided shape", () => {
    const document = {
      events: [
        {
          timestamp: "2026-10-18T01:10:05.123+0000",
          severity: "high",
          risk_score: 85,
          risk_level: 12,
          rule: {
            level: 12,
            description: "Access to hidden file / directory found.",
            id: "554",
            groups: ["syslog", "ossec", "pci_dss_10.6.1"]
          },
          agent: { id: "002", name: "prod-app-server-02", ip: "192.168.10.52" },
          id: "1697677805.9876543",
          data: { command: "cat /var/www/html/.env", srcuser: "www-data", system_name: "ubuntu" },
          location: "/var/log/audit/audit.log"
        },
        {
          timestamp: "2026-10-18T01:12:44.456+0000",
          severity: "medium",
          risk_score: 50,
          risk_level: 7,
          rule: {
            level: 7,
            description: "New user added to the system.",
            id: "5901",
            groups: ["syslog", "ossec", "adduser"]
          },
          agent: { id: "005", name: "corporate-dc-01", ip: "192.168.20.10" },
          id: "1697677964.1234567",
          data: { dstuser: "backdoor_admin", user: "root", system_name: "win-dc-01" },
          location: "/var/log/secure"
        }
      ]
    };

    const events = normalizeWazuhJson(JSON.stringify(document));
    const candidates = findAuthenticationSequenceCandidates(events);

    assert.equal(candidates.length, 2);
    assert.deepEqual(
      candidates.map((candidate) => candidate.title),
      ["New account created", "Sensitive file or directory discovery"]
    );
    assert.deepEqual(
      candidates.map((candidate) => candidate.priority),
      ["medium", "critical"]
    );
    assert.deepEqual(
      candidates.map((candidate) => candidate.evidence[0].eventId),
      ["1697677964.1234567", "1697677805.9876543"]
    );
    assert.equal(candidates[1].subjectLabel, "Account");
    assert.equal(JSON.stringify(candidates).includes("cat /var/www/html/.env"), false);
  });

  it("rejects malformed lines and invalid Wazuh fields with line numbers", () => {
    assert.throws(
      () => normalizeWazuhJsonLines(`${JSON.stringify(failedLogin)}\n{bad json}`),
      /Line 2 is not valid JSON/
    );
    assert.throws(
      () => normalizeWazuhJsonLines(JSON.stringify({
        ...failedLogin,
        rule: { ...failedLogin.rule, level: 16 }
      })),
      /Line 1: rule.level must be an integer from 0 to 15/
    );
    assert.throws(
      () => normalizeWazuhJsonLines(JSON.stringify({
        ...failedLogin,
        rule: { ...failedLogin.rule, groups: ["valid", 4] }
      })),
      /rule.groups must be an array/
    );
  });

  it("rejects duplicate IDs and invalid calendar dates", () => {
    assert.throws(
      () => normalizeWazuhJsonLines(`${JSON.stringify(failedLogin)}\n${JSON.stringify(failedLogin)}`),
      /Event IDs must be unique/
    );
    assert.throws(
      () => normalizeWazuhAlert({
        ...failedLogin,
        timestamp: "2026-02-30T09:14:00.000+0000"
      }),
      /valid Wazuh timestamp/
    );
  });
});
