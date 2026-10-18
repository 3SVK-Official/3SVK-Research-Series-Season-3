import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  EventImportValidationError,
  MAX_IMPORT_EVENTS,
  validateEventImport
} from "../src/ingestion/validate-event-import.js";

const validEvent = {
  id: "auth-failure",
  source: "test-source",
  observedAt: "2026-10-17T09:14:00.000Z",
  eventType: "authentication.failure",
  severity: "medium",
  summary: "A test sign-in failed.",
  entities: [{ kind: "user", value: "analyst@example.test" }]
};

describe("normalized event import validation", () => {
  it("accepts normalized events and returns a detached copy", () => {
    const input = { events: [validEvent] };
    const validated = validateEventImport(input);
    validated[0].entities[0].value = "changed";

    assert.equal(validated[0].source, "test-source");
    assert.equal(input.events[0].entities[0].value, "analyst@example.test");
  });

  it("rejects extra event fields so raw payloads are not retained", () => {
    assert.throws(
      () => validateEventImport({ events: [{ ...validEvent, rawLog: "sensitive" }] }),
      EventImportValidationError
    );
  });

  it("accepts bounded Wazuh detection context without allowing arbitrary payload fields", () => {
    const result = validateEventImport({
      events: [{
        ...validEvent,
        wazuh: {
          ruleId: "5503",
          level: 5,
          groups: ["authentication_failed"],
          mitre: { ids: ["T1110"], tactics: [], techniques: [] },
          agentName: "test-host"
        }
      }]
    });
    assert.equal(result[0].wazuh?.ruleId, "5503");
    assert.throws(
      () => validateEventImport({
        events: [{
          ...validEvent,
          wazuh: {
            ruleId: "5503",
            level: 5,
            groups: [],
            mitre: { ids: [], tactics: [], techniques: [] },
            raw: "unbounded fields are rejected"
          }
        }]
      }),
      /unsupported or missing fields/
    );
  });

  it("rejects duplicate event IDs", () => {
    assert.throws(
      () => validateEventImport({ events: [validEvent, validEvent] }),
      /Event IDs must be unique/
    );
  });

  it("rejects invalid event timestamps and event type identifiers", () => {
    assert.throws(
      () => validateEventImport({
        events: [{ ...validEvent, observedAt: "2026-10-17T09:14:00" }]
      }),
      /ISO 8601 timestamp with a timezone/
    );
    assert.throws(
      () => validateEventImport({
        events: [{ ...validEvent, observedAt: "2026-02-30T09:14:00.000Z" }]
      }),
      /ISO 8601 timestamp with a timezone/
    );
    assert.throws(
      () => validateEventImport({
        events: [{ ...validEvent, eventType: "authentication.failure\nextra" }]
      }),
      /eventType must be a valid string/
    );
  });

  it("enforces the event-count limit", () => {
    assert.throws(
      () => validateEventImport({ events: Array.from({ length: MAX_IMPORT_EVENTS + 1 }, () => validEvent) }),
      /at most 500 entries/
    );
  });
});
