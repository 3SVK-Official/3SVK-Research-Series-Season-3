import type { AlertConnector } from "./alert-connector.js";
import type { SecurityEvent } from "../domain/security-event.js";

const demoEvents: SecurityEvent[] = [
  {
    id: "demo-001",
    source: "demo",
    observedAt: "2026-10-17T09:14:00.000Z",
    eventType: "authentication.failure",
    severity: "medium",
    summary: "Several failed sign-in attempts were recorded for one account.",
    entities: [
      { kind: "user", value: "alex@example.test" },
      { kind: "ip", value: "192.0.2.24" }
    ]
  },
  {
    id: "demo-002",
    source: "demo",
    observedAt: "2026-10-17T09:15:00.000Z",
    eventType: "authentication.success",
    severity: "high",
    summary: "A sign-in succeeded for the same account shortly after the failures.",
    entities: [
      { kind: "user", value: "alex@example.test" },
      { kind: "ip", value: "192.0.2.24" }
    ]
  },
  {
    id: "demo-003",
    source: "demo",
    observedAt: "2026-10-17T09:17:00.000Z",
    eventType: "endpoint.alert",
    severity: "low",
    summary: "A workstation generated a routine endpoint alert for review.",
    entities: [{ kind: "host", value: "workstation-07" }]
  }
];

export function createDemoConnector(): AlertConnector {
  return {
    name: "demo",
    mode: "demo",
    async fetchEvents() {
      return demoEvents.map((event) => ({
        ...event,
        entities: event.entities.map((entity) => ({ ...entity }))
      }));
    }
  };
}
