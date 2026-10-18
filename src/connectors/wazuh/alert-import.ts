import type {
  SecurityEntity,
  SecurityEvent,
  SecuritySeverity,
  WazuhAlertContext
} from "../../domain/security-event.js";
import {
  EventImportValidationError,
  MAX_IMPORT_EVENTS,
  validateEventImport
} from "../../ingestion/validate-event-import.js";

export class WazuhImportError extends Error {}

interface WazuhRule {
  id: string;
  level: number;
  description?: string;
  groups?: string[];
  mitre?: {
    id?: string[];
    tactic?: string[];
    technique?: string[];
  };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isNormalizedEventDocument(value: unknown): boolean {
  try {
    validateEventImport(value);
    return true;
  } catch (error) {
    if (error instanceof EventImportValidationError) {
      return false;
    }
    throw error;
  }
}

function requiredString(value: unknown, field: string, maxLength = 512): string {
  if (
    typeof value !== "string" ||
    value.trim().length === 0 ||
    value.length > maxLength
  ) {
    throw new WazuhImportError(`${field} must be a non-empty string of at most ${maxLength} characters.`);
  }
  return value;
}

function normalizeWazuhTimestamp(timestamp: string): string {
  const normalized = timestamp.replace(/([+-]\d{2})(\d{2})$/, "$1:$2");
  if (!Number.isFinite(Date.parse(normalized))) {
    throw new WazuhImportError("timestamp must be a valid Wazuh timestamp.");
  }
  return normalized;
}

function severityForLevel(level: number): SecuritySeverity {
  if (level >= 12) return "critical";
  if (level >= 8) return "high";
  if (level >= 4) return "medium";
  return "low";
}

function optionalEntity(
  entities: SecurityEntity[],
  kind: SecurityEntity["kind"],
  value: unknown
): void {
  if (typeof value === "string" && value.trim().length > 0) {
    entities.push({ kind, value: value.slice(0, 512) });
  }
}

function optionalString(value: unknown, field: string, maxLength = 512): string | undefined {
  if (value === undefined || value === null || value === "") return undefined;
  return requiredString(value, field, maxLength);
}

function optionalStringList(value: unknown, field: string): string[] {
  if (value === undefined) return [];
  if (
    !Array.isArray(value) ||
    value.length > 100 ||
    value.some((item) => typeof item !== "string" || item.trim().length === 0 || item.length > 256)
  ) {
    throw new WazuhImportError(`${field} must be an array of at most 100 non-empty strings.`);
  }
  return [...value];
}

function classifyEventType(rule: WazuhRule): string {
  const groups = (rule.groups ?? []).map((group) => group.toLowerCase());
  const description = rule.description ?? "";
  if (groups.some((group) => /authentication.*(failed|failures?)|auth.*(failed|failures?)/.test(group))) {
    return "authentication.failure";
  }
  if (groups.some((group) => /authentication.*success|auth.*success/.test(group))) {
    return "authentication.success";
  }
  if (
    groups.some((group) => /adduser|useradd|account.?creation|account.?created|user.?created/.test(group)) ||
    /new user added|user account created/i.test(rule.description ?? "")
  ) {
    return "account.creation";
  }
  if (
    groups.some((group) => /file.?discovery|directory.?discovery/.test(group)) ||
    /hidden file|directory discovery/i.test(description)
  ) {
    return "file.discovery";
  }
  if (
    groups.some((group) => /malware|virus|trojan|rootkit/.test(group)) ||
    /\b(malware|virus|trojan|rootkit)\b/i.test(description)
  ) {
    return "malware.detected";
  }
  if (
    groups.some((group) => /vulnerability|cve/.test(group)) ||
    /\bvulnerability (detected|found)|\bCVE-\d{4}-\d+/i.test(description)
  ) {
    return "vulnerability.detected";
  }
  if (
    groups.some((group) => /privilege.?escalation|sudoers/.test(group)) ||
    /privilege escalation|elevated privileges|sudoers file/i.test(description)
  ) {
    return "privilege.escalation";
  }
  if (
    groups.some((group) => /web.?attack|web.?exploit|sql.?injection/.test(group)) ||
    /web attack|sql injection|cross.?site scripting|command injection|directory traversal/i.test(description)
  ) {
    return "web.attack";
  }
  if (
    groups.some((group) => /network.?scan|port.?scan/.test(group)) ||
    /network scan|port scan/i.test(description)
  ) {
    return "network.scan";
  }
  if (
    groups.some((group) => /syscheck|file.?integrity/.test(group)) ||
    /file integrity|checksum.*changed|file.*modified/i.test(description)
  ) {
    return "file.integrity.change";
  }
  return `wazuh.rule.${rule.id}`;
}

export function normalizeWazuhAlert(value: unknown): SecurityEvent {
  if (!isRecord(value) || !isRecord(value.rule)) {
    throw new WazuhImportError("Each Wazuh alert must contain an alert object and rule object.");
  }

  const id = requiredString(value.id, "id", 128);
  const timestamp = normalizeWazuhTimestamp(requiredString(value.timestamp, "timestamp", 40));
  const ruleId = requiredString(value.rule.id, "rule.id", 32);
  if (
    typeof value.rule.level !== "number" ||
    !Number.isInteger(value.rule.level) ||
    value.rule.level < 0 ||
    value.rule.level > 15
  ) {
    throw new WazuhImportError("rule.level must be an integer from 0 to 15.");
  }

  const description = typeof value.rule.description === "string"
    ? value.rule.description.trim().slice(0, 1000)
    : "";
  if (
    value.rule.groups !== undefined &&
    (!Array.isArray(value.rule.groups) ||
      value.rule.groups.length > 100 ||
      value.rule.groups.some((group) => typeof group !== "string"))
  ) {
    throw new WazuhImportError("rule.groups must be an array of at most 100 strings.");
  }
  if (value.rule.mitre !== undefined && !isRecord(value.rule.mitre)) {
    throw new WazuhImportError("rule.mitre must be an object.");
  }
  const mitre = isRecord(value.rule.mitre) ? value.rule.mitre : {};

  const rule: WazuhRule = {
    id: ruleId,
    level: value.rule.level,
    description,
    groups: value.rule.groups as string[] | undefined,
    mitre: {
      id: optionalStringList(mitre.id, "rule.mitre.id"),
      tactic: optionalStringList(mitre.tactic, "rule.mitre.tactic"),
      technique: optionalStringList(mitre.technique, "rule.mitre.technique")
    }
  };

  const data = isRecord(value.data) ? value.data : {};
  const agent = isRecord(value.agent) ? value.agent : {};
  const decoder = isRecord(value.decoder) ? value.decoder : {};
  const entities: SecurityEntity[] = [];
  optionalEntity(entities, "host", agent.name);
  optionalEntity(entities, "ip", agent.ip);
  optionalEntity(entities, "user", data.srcuser);
  optionalEntity(entities, "user", data.dstuser);
  optionalEntity(entities, "user", data.user);
  optionalEntity(entities, "ip", data.srcip);
  optionalEntity(entities, "ip", data.dstip);
  optionalEntity(entities, "ip", data.ip);
  optionalEntity(entities, "file", data.path);
  optionalEntity(entities, "file", data.filename);
  const agentId = optionalString(agent.id, "agent.id", 128);
  const agentName = optionalString(agent.name, "agent.name");
  const location = optionalString(value.location, "location");
  const decoderName = optionalString(decoder.name, "decoder.name");

  const normalizedEvent: SecurityEvent = {
    id,
    source: "wazuh",
    observedAt: timestamp,
    eventType: classifyEventType(rule),
    severity: severityForLevel(rule.level),
    summary: description || `Wazuh rule ${rule.id} triggered at level ${rule.level}.`,
    entities,
    wazuh: {
      ruleId: rule.id,
      level: rule.level,
      groups: rule.groups ?? [],
      mitre: {
        ids: rule.mitre?.id ?? [],
        tactics: rule.mitre?.tactic ?? [],
        techniques: rule.mitre?.technique ?? []
      },
      ...(agentId ? { agentId } : {}),
      ...(agentName ? { agentName } : {}),
      ...(location ? { location } : {}),
      ...(decoderName ? { decoderName } : {})
    } satisfies WazuhAlertContext
  };

  try {
    return validateEventImport({ events: [normalizedEvent] })[0];
  } catch (error) {
    if (error instanceof EventImportValidationError && error.message.includes("observedAt")) {
      throw new WazuhImportError("timestamp must be a valid Wazuh timestamp.");
    }
    throw error;
  }
}

export function normalizeWazuhJsonLines(input: string): SecurityEvent[] {
  const lines = input.split(/\r?\n/);
  const alerts: unknown[] = [];

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index].trim();
    if (!line) continue;

    if (alerts.length >= MAX_IMPORT_EVENTS) {
      throw new WazuhImportError(`Wazuh import may contain at most ${MAX_IMPORT_EVENTS} alerts.`);
    }

    let alert: unknown;
    try {
      alert = JSON.parse(line) as unknown;
    } catch {
      throw new WazuhImportError(`Line ${index + 1} is not valid JSON.`);
    }

    try {
      alerts.push(normalizeWazuhAlert(alert));
    } catch (error) {
      const message = error instanceof Error ? error.message : "Invalid alert.";
      throw new WazuhImportError(`Line ${index + 1}: ${message}`);
    }
  }

  if (alerts.length === 0) {
    throw new WazuhImportError("Wazuh import must contain at least one alert.");
  }

  try {
    return validateEventImport({ events: alerts });
  } catch (error) {
    if (error instanceof Error) {
      throw new WazuhImportError(error.message);
    }
    throw error;
  }
}

function normalizeWazuhAlerts(alerts: unknown[]): SecurityEvent[] {
  if (alerts.length === 0) {
    throw new WazuhImportError("Wazuh import must contain at least one alert.");
  }
  if (alerts.length > MAX_IMPORT_EVENTS) {
    throw new WazuhImportError(`Wazuh import may contain at most ${MAX_IMPORT_EVENTS} alerts.`);
  }

  const normalized = alerts.map((alert, index) => {
    try {
      return normalizeWazuhAlert(alert);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Invalid alert.";
      throw new WazuhImportError(`Alert ${index + 1}: ${message}`);
    }
  });

  try {
    return validateEventImport({ events: normalized });
  } catch (error) {
    if (error instanceof Error) {
      throw new WazuhImportError(error.message);
    }
    throw error;
  }
}

export function normalizeWazuhJsonDocument(value: unknown): SecurityEvent[] {
  if (Array.isArray(value)) {
    return normalizeWazuhAlerts(value);
  }

  if (!isRecord(value)) {
    throw new WazuhImportError(
      "Wazuh JSON must be one alert object, an array of alerts, or an object with an events array."
    );
  }

  if ("events" in value) {
    if (!Array.isArray(value.events)) {
      throw new WazuhImportError("The Wazuh JSON events property must be an array.");
    }
    if (value.events.length > 0 && isRecord(value.events[0]) && !("rule" in value.events[0])) {
      if (isNormalizedEventDocument(value)) {
        throw new WazuhImportError(
          "This file is already in normalized event format. Use Import JSON instead of Import Wazuh."
        );
      }
    }
    return normalizeWazuhAlerts(value.events);
  }

  if (!("rule" in value)) {
    throw new WazuhImportError(
      "This file is not a Wazuh alert. Wazuh alerts need timestamp, id, and rule fields; use Import JSON for normalized event files."
    );
  }

  return normalizeWazuhAlerts([value]);
}

export function isWazuhJsonDocument(value: unknown): boolean {
  if (Array.isArray(value)) {
    return value.length > 0 && isRecord(value[0]) && "rule" in value[0];
  }
  if (!isRecord(value)) {
    return false;
  }
  if ("rule" in value) {
    return true;
  }
  return (
    Array.isArray(value.events) &&
    value.events.length > 0 &&
    isRecord(value.events[0]) &&
    "rule" in value.events[0]
  );
}

export function normalizeWazuhJson(input: string): SecurityEvent[] {
  let value: unknown;
  try {
    value = JSON.parse(input) as unknown;
  } catch {
    throw new WazuhImportError("Wazuh JSON file must contain valid JSON.");
  }
  return normalizeWazuhJsonDocument(value);
}
