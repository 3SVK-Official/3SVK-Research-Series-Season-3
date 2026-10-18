export type SecuritySeverity = "low" | "medium" | "high" | "critical";

export interface SecurityEntity {
  kind: "user" | "ip" | "host" | "file";
  value: string;
}

export interface WazuhAlertContext {
  ruleId: string;
  level: number;
  groups: string[];
  mitre: {
    ids: string[];
    tactics: string[];
    techniques: string[];
  };
  agentId?: string;
  agentName?: string;
  location?: string;
  decoderName?: string;
}

export interface SecurityEvent {
  id: string;
  source: string;
  observedAt: string;
  eventType: string;
  severity: SecuritySeverity;
  summary: string;
  entities: SecurityEntity[];
  wazuh?: WazuhAlertContext;
}
