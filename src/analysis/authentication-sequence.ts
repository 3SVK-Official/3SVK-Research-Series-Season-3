import type { SecurityEvent, WazuhAlertContext } from "../domain/security-event.js";

const CORRELATION_WINDOW_MS = 10 * 60 * 1000;

export interface IncidentCandidate {
  id: string;
  rule:
    | "authentication-failures-followed-by-success"
    | "high-severity-alert"
    | "account-creation"
    | "file-discovery"
    | "malware-detected"
    | "vulnerability-detected"
    | "privilege-escalation"
    | "web-attack"
    | "network-scan"
    | "file-integrity-change"
    | "alert-review";
  title: string;
  priority: "review" | "medium" | "high" | "critical";
  affectedUser: string;
  subjectLabel: "Account" | "System" | "Event";
  explanation: string;
  startedAt: string;
  detectedAt: string;
  evidence: Array<{
    eventId: string;
    observedAt: string;
    summary: string;
  }>;
  wazuhAlerts?: Array<{
    eventId: string;
    context: WazuhAlertContext;
  }>;
  recommendedChecks: string[];
  requiresHumanReview: true;
}

function userValue(event: SecurityEvent): string | undefined {
  const value = event.entities.find((entity) => entity.kind === "user")?.value.trim();
  return value ? value.toLocaleLowerCase("en-US") : undefined;
}

function candidatePriority(event: SecurityEvent): "review" | "medium" | "high" | "critical" {
  if (event.severity === "critical") return "critical";
  if (event.severity === "high") return "high";
  if (event.severity === "medium") return "medium";
  return "review";
}

function entitySubject(event: SecurityEvent): { label: "Account" | "System" | "Event"; value: string } {
  const user = event.entities.find((entity) => entity.kind === "user")?.value.trim();
  if (user) return { label: "Account", value: user };

  const host = event.entities.find((entity) => entity.kind === "host")?.value.trim();
  if (host) return { label: "System", value: host };

  return { label: "Event", value: event.source };
}

function wazuhAlertContext(events: SecurityEvent[]): IncidentCandidate["wazuhAlerts"] {
  const alerts = events.flatMap((event) => event.wazuh
    ? [{ eventId: event.id, context: event.wazuh }]
    : []);
  return alerts.length > 0 ? alerts : undefined;
}

interface DetectionDefinition {
  rule: IncidentCandidate["rule"];
  title: string;
  explanation: string;
  checks: string[];
}

const DETECTIONS: Partial<Record<string, DetectionDefinition>> = {
  "account.creation": {
    rule: "account-creation",
    title: "New account created",
    explanation: "A monitoring alert reports that a new account was created. Verify the change was authorized and review its assigned privileges.",
    checks: [
      "Confirm who requested the account and whether its creation was approved.",
      "Review the account's privileges, authentication settings, and recent activity."
    ]
  },
  "file.discovery": {
    rule: "file-discovery",
    title: "Sensitive file or directory discovery",
    explanation: "A monitoring alert reports discovery or access involving a file or directory. Verify the activity and inspect the source-system evidence.",
    checks: [
      "Confirm whether the file or directory activity was expected for this system and user.",
      "Review the original alert and nearby process or authentication events in the source system."
    ]
  },
  "malware.detected": {
    rule: "malware-detected",
    title: "Potential malware detected",
    explanation: "A monitoring alert matched a malware-related signal. Validate the detection and affected asset before taking response actions.",
    checks: [
      "Review the detection name, affected file or process, and endpoint telemetry in the source system.",
      "Check for related alerts on the host and confirm the endpoint's containment status."
    ]
  },
  "vulnerability.detected": {
    rule: "vulnerability-detected",
    title: "Vulnerability detected",
    explanation: "A monitoring alert reports a vulnerability on an asset. Confirm exposure and prioritize remediation using the asset's context.",
    checks: [
      "Verify the vulnerability identifier, affected software version, and asset exposure.",
      "Check for an available fix and follow the organization's patch and change process."
    ]
  },
  "privilege.escalation": {
    rule: "privilege-escalation",
    title: "Potential privilege escalation",
    explanation: "A monitoring alert reports possible privilege escalation. Verify whether the activity was authorized and review the initiating account.",
    checks: [
      "Confirm whether the elevated action was approved and expected for this account.",
      "Review nearby authentication, process, and privilege-change events on the host."
    ]
  },
  "web.attack": {
    rule: "web-attack",
    title: "Potential web application attack",
    explanation: "A monitoring alert matched a web-attack pattern. Validate the request and determine whether the application or data was affected.",
    checks: [
      "Review the source request and web-server logs in the monitoring system.",
      "Check application telemetry for successful access, errors, or related requests."
    ]
  },
  "network.scan": {
    rule: "network-scan",
    title: "Network or port scan detected",
    explanation: "A monitoring alert reports scan-like network activity. Confirm whether it came from an authorized scanner or expected assessment.",
    checks: [
      "Identify the source and destination assets and verify whether scanning was authorized.",
      "Review nearby network alerts for follow-on connection or exploitation attempts."
    ]
  },
  "file.integrity.change": {
    rule: "file-integrity-change",
    title: "Monitored file integrity changed",
    explanation: "A monitoring alert reports a change to a monitored file. Confirm the change was expected and trace it to an approved process.",
    checks: [
      "Identify the changed file and compare the change with an approved deployment or maintenance window.",
      "Review the responsible account and nearby process or configuration-change events."
    ]
  }
};

function standaloneCandidate(event: SecurityEvent): IncidentCandidate {
  const detection = DETECTIONS[event.eventType];
  const isHighSeverity = event.severity === "high" || event.severity === "critical";

  const subject = entitySubject(event);
  const rule = detection?.rule ?? (isHighSeverity ? "high-severity-alert" : "alert-review");
  const title = detection?.title ?? (
    isHighSeverity ? "High-severity security alert" : "Security alert requires review"
  );

  return {
    id: `${rule}:${event.id}`,
    rule,
    title,
    priority: candidatePriority(event),
    affectedUser: subject.value,
    subjectLabel: subject.label,
    explanation: detection?.explanation ?? (
      isHighSeverity
        ? "A high-severity monitoring alert needs analyst review. This signal does not by itself confirm malicious activity."
        : "This alert does not match a specific detection rule yet. Review its source details and surrounding events; it is not a confirmed incident."
    ),
    startedAt: event.observedAt,
    detectedAt: event.observedAt,
    evidence: [{
      eventId: event.id,
      observedAt: event.observedAt,
      summary: event.summary
    }],
    ...(wazuhAlertContext([event]) ? { wazuhAlerts: wazuhAlertContext([event]) } : {}),
    recommendedChecks: detection?.checks ?? (
      isHighSeverity
        ? [
            "Review the original alert and its surrounding events in the source monitoring system.",
            "Validate the affected system and account with the responsible owner before responding."
          ]
        : [
            "Review the alert details and related activity in the source monitoring system.",
            "Confirm the affected system and account with the responsible owner before taking action."
          ]
    ),
    requiresHumanReview: true
  };
}

export function findAuthenticationSequenceCandidates(
  events: SecurityEvent[]
): IncidentCandidate[] {
  const eventIds = new Set<string>();
  const orderedEvents = events
    .map((event) => {
      if (eventIds.has(event.id)) {
        throw new Error(`Duplicate security event ID: ${event.id}`);
      }
      eventIds.add(event.id);

      const timestamp = Date.parse(event.observedAt);
      if (!Number.isFinite(timestamp)) {
        throw new Error(`Invalid observedAt timestamp on event: ${event.id}`);
      }

      return { event, timestamp };
    })
    .sort((left, right) => left.timestamp - right.timestamp);

  const failuresByUser = new Map<string, Array<(typeof orderedEvents)[number]>>();
  const candidates: IncidentCandidate[] = [];
  const correlatedEventIds = new Set<string>();

  for (const current of orderedEvents) {
    const account = userValue(current.event);
    if (!account) {
      continue;
    }

    const recentFailures = (failuresByUser.get(account) ?? []).filter(
      (failure) => current.timestamp - failure.timestamp <= CORRELATION_WINDOW_MS
    );

    if (current.event.eventType === "authentication.failure") {
      recentFailures.push(current);
      failuresByUser.set(account, recentFailures);
      continue;
    }

    if (current.event.eventType !== "authentication.success") {
      continue;
    }

    failuresByUser.set(account, recentFailures);

    if (recentFailures.length === 0) {
      continue;
    }

    const evidence = [...recentFailures, current].map(({ event }) => ({
      eventId: event.id,
      observedAt: event.observedAt,
      summary: event.summary
    }));
    for (const item of evidence) {
      correlatedEventIds.add(item.eventId);
    }

    candidates.push({
      id: `auth-sequence:${current.event.id}`,
      rule: "authentication-failures-followed-by-success",
      title: "Failed sign-ins followed by a successful sign-in",
      priority: "review",
      affectedUser: account,
      subjectLabel: "Account",
      explanation:
        "Failed sign-in attempts were followed by a successful sign-in for this account. This pattern can have benign causes and needs verification.",
      startedAt: recentFailures[0].event.observedAt,
      detectedAt: current.event.observedAt,
      evidence,
      ...(wazuhAlertContext([...recentFailures.map(({ event }) => event), current.event])
        ? { wazuhAlerts: wazuhAlertContext([...recentFailures.map(({ event }) => event), current.event]) }
        : {}),
      recommendedChecks: [
        "Confirm with the account owner whether the successful sign-in was expected.",
        "Review the account's MFA and nearby session activity before taking action."
      ],
      requiresHumanReview: true
    });
  }

  for (const { event } of orderedEvents) {
    if (correlatedEventIds.has(event.id)) {
      continue;
    }
    candidates.push(standaloneCandidate(event));
  }

  return candidates.sort(
    (left, right) => Date.parse(right.detectedAt) - Date.parse(left.detectedAt)
  );
}
