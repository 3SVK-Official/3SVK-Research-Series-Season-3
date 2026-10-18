import type {
  SecurityEntity,
  SecurityEvent,
  SecuritySeverity,
  WazuhAlertContext
} from "../domain/security-event.js";

export const MAX_IMPORT_BYTES = 1024 * 1024;
export const MAX_IMPORT_EVENTS = 500;

const severities = new Set<SecuritySeverity>(["low", "medium", "high", "critical"]);
const entityKinds = new Set<SecurityEntity["kind"]>(["user", "ip", "host", "file"]);
const eventKeys = ["id", "source", "observedAt", "eventType", "severity", "summary", "entities"];
const entityKeys = ["kind", "value"];
const wazuhKeys = [
  "ruleId",
  "level",
  "groups",
  "mitre",
  "agentId",
  "agentName",
  "location",
  "decoderName"
];
const mitreKeys = ["ids", "tactics", "techniques"];
const isoTimestamp =
  /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,3})?(Z|([+-])(\d{2}):(\d{2}))$/;

export class EventImportValidationError extends Error {}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function requireExactKeys(
  value: Record<string, unknown>,
  keys: string[],
  path: string
): void {
  const actual = Object.keys(value).sort();
  const expected = [...keys].sort();
  if (
    actual.length !== expected.length ||
    actual.some((key, index) => key !== expected[index])
  ) {
    throw new EventImportValidationError(`${path} must contain exactly: ${keys.join(", ")}.`);
  }
}

function requireString(
  value: unknown,
  path: string,
  maxLength: number,
  pattern?: RegExp
): string {
  if (
    typeof value !== "string" ||
    value.trim().length === 0 ||
    value.length > maxLength ||
    (pattern && !pattern.test(value))
  ) {
    throw new EventImportValidationError(`${path} must be a valid string of at most ${maxLength} characters.`);
  }
  return value;
}

function isValidIsoTimestamp(value: string): boolean {
  const match = isoTimestamp.exec(value);
  if (!match || !Number.isFinite(Date.parse(value))) {
    return false;
  }

  const [year, month, day, hour, minute, second] = match.slice(1, 7).map(Number);
  const calendarDate = new Date(0);
  calendarDate.setUTCFullYear(year, month - 1, day);
  calendarDate.setUTCHours(hour, minute, second, 0);

  if (
    calendarDate.getUTCFullYear() !== year ||
    calendarDate.getUTCMonth() !== month - 1 ||
    calendarDate.getUTCDate() !== day ||
    hour > 23 ||
    minute > 59 ||
    second > 59
  ) {
    return false;
  }

  if (match[8] && (Number(match[9]) > 14 || Number(match[10]) > 59)) {
    return false;
  }

  return !(Number(match[9]) === 14 && Number(match[10]) !== 0);
}

function validateEntity(value: unknown, path: string): SecurityEntity {
  if (!isRecord(value)) {
    throw new EventImportValidationError(`${path} must be an object.`);
  }
  requireExactKeys(value, entityKeys, path);

  if (typeof value.kind !== "string" || !entityKinds.has(value.kind as SecurityEntity["kind"])) {
    throw new EventImportValidationError(`${path}.kind is unsupported.`);
  }

  return {
    kind: value.kind as SecurityEntity["kind"],
    value: requireString(value.value, `${path}.value`, 512)
  };
}

function validateStringList(value: unknown, path: string, maximum: number): string[] {
  if (
    !Array.isArray(value) ||
    value.length > maximum ||
    value.some((item) => typeof item !== "string" || item.trim().length === 0 || item.length > 256)
  ) {
    throw new EventImportValidationError(`${path} must be an array of at most ${maximum} non-empty strings.`);
  }
  return [...value];
}

function validateWazuhContext(value: unknown, path: string): WazuhAlertContext {
  if (!isRecord(value)) {
    throw new EventImportValidationError(`${path} must be an object.`);
  }
  const optionalKeys = ["agentId", "agentName", "location", "decoderName"];
  const requiredKeys = ["ruleId", "level", "groups", "mitre"];
  if (
    Object.keys(value).some((key) => !wazuhKeys.includes(key)) ||
    requiredKeys.some((key) => !(key in value))
  ) {
    throw new EventImportValidationError(`${path} contains unsupported or missing fields.`);
  }

  const ruleId = requireString(value.ruleId, `${path}.ruleId`, 32);
  if (typeof value.level !== "number" || !Number.isInteger(value.level) || value.level < 0 || value.level > 15) {
    throw new EventImportValidationError(`${path}.level must be an integer from 0 to 15.`);
  }
  const groups = validateStringList(value.groups, `${path}.groups`, 100);
  if (!isRecord(value.mitre)) {
    throw new EventImportValidationError(`${path}.mitre must be an object.`);
  }
  requireExactKeys(value.mitre, mitreKeys, `${path}.mitre`);

  const context: WazuhAlertContext = {
    ruleId,
    level: value.level,
    groups,
    mitre: {
      ids: validateStringList(value.mitre.ids, `${path}.mitre.ids`, 100),
      tactics: validateStringList(value.mitre.tactics, `${path}.mitre.tactics`, 100),
      techniques: validateStringList(value.mitre.techniques, `${path}.mitre.techniques`, 100)
    }
  };
  for (const key of optionalKeys) {
    if (key in value) {
      context[key as "agentId" | "agentName" | "location" | "decoderName"] =
        requireString(value[key], `${path}.${key}`, 512);
    }
  }
  return context;
}

function validateEvent(value: unknown, index: number): SecurityEvent {
  const path = `events[${index}]`;
  if (!isRecord(value)) {
    throw new EventImportValidationError(`${path} must be an object.`);
  }
  const actualKeys = Object.keys(value).sort();
  const allowedKeys = [...eventKeys, "wazuh"].sort();
  if (
    eventKeys.some((key) => !(key in value)) ||
    actualKeys.some((key) => !allowedKeys.includes(key))
  ) {
    throw new EventImportValidationError(`${path} must contain exactly: ${eventKeys.join(", ")} and optional wazuh context.`);
  }

  const id = requireString(value.id, `${path}.id`, 128);
  const source = requireString(value.source, `${path}.source`, 80);
  const observedAt = requireString(value.observedAt, `${path}.observedAt`, 40);
  if (!isValidIsoTimestamp(observedAt)) {
    throw new EventImportValidationError(`${path}.observedAt must be an ISO 8601 timestamp with a timezone.`);
  }

  const eventType = requireString(
    value.eventType,
    `${path}.eventType`,
    100,
    /^[a-zA-Z0-9][a-zA-Z0-9._:-]*$/
  );
  if (typeof value.severity !== "string" || !severities.has(value.severity as SecuritySeverity)) {
    throw new EventImportValidationError(`${path}.severity must be low, medium, high, or critical.`);
  }
  const summary = requireString(value.summary, `${path}.summary`, 1000);

  if (!Array.isArray(value.entities) || value.entities.length > 20) {
    throw new EventImportValidationError(`${path}.entities must be an array of at most 20 entities.`);
  }

  const event: SecurityEvent = {
    id,
    source,
    observedAt,
    eventType,
    severity: value.severity as SecuritySeverity,
    summary,
    entities: value.entities.map((entity, entityIndex) =>
      validateEntity(entity, `${path}.entities[${entityIndex}]`)
    )
  };
  if ("wazuh" in value) {
    event.wazuh = validateWazuhContext(value.wazuh, `${path}.wazuh`);
  }
  return event;
}

export function validateEventImport(value: unknown): SecurityEvent[] {
  if (!isRecord(value) || Object.keys(value).length !== 1 || !("events" in value)) {
    throw new EventImportValidationError("The JSON document must contain only an events array.");
  }
  if (!Array.isArray(value.events) || value.events.length > MAX_IMPORT_EVENTS) {
    throw new EventImportValidationError(`events must be an array containing at most ${MAX_IMPORT_EVENTS} entries.`);
  }

  const events = value.events.map(validateEvent);
  const ids = new Set<string>();
  for (const event of events) {
    if (ids.has(event.id)) {
      throw new EventImportValidationError("Event IDs must be unique within an import.");
    }
    ids.add(event.id);
  }

  return events;
}
