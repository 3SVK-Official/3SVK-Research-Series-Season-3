import type { SecurityEvent } from "../domain/security-event.js";

export interface AlertConnector {
  readonly name: string;
  readonly mode?: "demo" | "live";
  readonly limits?: {
    maxEvents?: number;
    lookbackHours?: number;
  };
  fetchEvents(): Promise<SecurityEvent[]>;
}
