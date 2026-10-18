const incidentCount = document.querySelector("#incident-count");
const eventCount = document.querySelector("#event-count");
const sourceCount = document.querySelector("#source-count");
const navIncidentCount = document.querySelector("#nav-incident-count");
const eventCountLabel = document.querySelector("#event-count-label");
const eventRows = document.querySelector("#event-rows");
const candidateList = document.querySelector("#candidate-list");
const errorBanner = document.querySelector("#load-error");
const refreshButton = document.querySelector("#refresh");
const importButton = document.querySelector("#import-events");
const importWazuhButton = document.querySelector("#import-wazuh");
const resetButton = document.querySelector("#reset-demo");
const logoutButton = document.querySelector("#logout");
const eventFile = document.querySelector("#event-file");
const wazuhFile = document.querySelector("#wazuh-file");
const environmentLabel = document.querySelector("#environment-label");
const dataModeTitle = document.querySelector("#data-mode-title");
const dataModeDescription = document.querySelector("#data-mode-description");
const sourceDescription = document.querySelector("#source-description");
const sourceTotal = document.querySelector("#source-total");
const sourceName = document.querySelector("#source-name");
const sourceDetail = document.querySelector("#source-detail");
const sourceState = document.querySelector("#source-state");
const eventPanelSubtitle = document.querySelector("#event-panel-subtitle");
const workspaceName = document.querySelector("#workspace-name");
const workspaceSubtitle = document.querySelector("#workspace-subtitle");
const profileName = document.querySelector("#profile-name");
const profileRole = document.querySelector("#profile-role");
const workflowFootnote = document.querySelector("#workflow-footnote");

const MAX_FILE_BYTES = 1024 * 1024;
let canReviewCases = true;
let livePollingEnabled = false;
let dashboardLoading = false;

function makeElement(tagName, className, text) {
  const element = document.createElement(tagName);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

function formatShortTimestamp(timestamp) {
  const date = new Date(timestamp);
  if (Number.isNaN(date.valueOf())) return "Unknown time";
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
    timeZone: "UTC"
  }).format(date);
}

function renderCandidateDetails(candidate) {
  const details = makeElement("div", "candidate-expanded");
  details.append(
    makeElement("p", "candidate-explanation", candidate.explanation)
  );

  if (candidate.wazuhAlerts?.length) {
    const alertHeading = makeElement("p", "expanded-label", "WAZUH DETECTION CONTEXT");
    const alertList = makeElement("ul", "check-list");
    for (const { eventId, context } of candidate.wazuhAlerts) {
      const details = [
        `Event ${eventId}: rule ${context.ruleId}, level ${context.level}`,
        context.groups.length ? `Groups: ${context.groups.join(", ")}` : "",
        context.mitre.ids.length ? `MITRE ATT&CK: ${context.mitre.ids.join(", ")}` : "",
        context.mitre.tactics.length ? `Tactics: ${context.mitre.tactics.join(", ")}` : "",
        context.mitre.techniques.length ? `Techniques: ${context.mitre.techniques.join(", ")}` : "",
        context.agentName ? `Agent: ${context.agentName}${context.agentId ? ` (${context.agentId})` : ""}` : "",
        context.decoderName ? `Decoder: ${context.decoderName}` : "",
        context.location ? `Location: ${context.location}` : ""
      ].filter(Boolean);
      alertList.append(makeElement("li", "", details.join(" · ")));
    }
    details.append(alertHeading, alertList);
  }

  const workflow = makeElement("div", "workflow-control");
  const workflowLabel = makeElement("label", "", "CASE STATUS");
  workflowLabel.htmlFor = `status-${candidate.id}`;
  const status = makeElement("select", "incident-status");
  status.id = `status-${candidate.id}`;
  status.setAttribute("aria-label", `Case status for ${candidate.title}`);
  status.disabled = !canReviewCases;
  for (const [value, label] of [
    ["new", "New"],
    ["investigating", "Investigating"],
    ["resolved", "Resolved"]
  ]) {
    const option = makeElement("option", "", label);
    option.value = value;
    option.selected = candidate.status === value;
    status.append(option);
  }
  status.addEventListener("change", () => {
    void updateIncidentStatus(candidate.id, status.value, candidate.status, status);
  });
  workflow.append(workflowLabel, status);
  if (candidate.history.length > 0) {
    const lastChange = candidate.history[candidate.history.length - 1];
    workflow.append(makeElement(
      "span",
      "workflow-updated",
      `Updated ${formatShortTimestamp(lastChange.changedAt)}`
    ));
  }
  details.append(workflow);

  const evidenceHeading = makeElement("p", "expanded-label", "CORRELATED EVIDENCE");
  const evidenceList = makeElement("ol", "evidence-list");
  for (const item of candidate.evidence) {
    const entry = makeElement("li", "evidence-item");
    const evidenceTop = makeElement("div", "evidence-top");
    evidenceTop.append(
      makeElement("span", "evidence-event", item.eventId),
      makeElement("time", "evidence-time", formatShortTimestamp(item.observedAt))
    );
    entry.append(
      evidenceTop,
      makeElement("p", "evidence-summary", item.summary)
    );
    evidenceList.append(entry);
  }
  details.append(evidenceHeading, evidenceList);

  const checksHeading = makeElement("p", "expanded-label", "SUGGESTED ANALYST CHECKS");
  const checks = makeElement("ul", "check-list");
  for (const check of candidate.recommendedChecks) {
    checks.append(makeElement("li", "", check));
  }
  details.append(checksHeading, checks);
  return details;
}

async function updateIncidentStatus(incidentId, status, previousStatus, control) {
  control.disabled = true;
  errorBanner.hidden = true;
  try {
    const response = await fetch(`/api/v1/incidents/${encodeURIComponent(incidentId)}`, {
      method: "PATCH",
      headers: { "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify({ status })
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || "Unable to update case status.");
    }
    await loadDashboard();
  } catch (error) {
    errorBanner.textContent = error instanceof Error
      ? error.message
      : "Unable to update case status.";
    errorBanner.hidden = false;
    control.value = previousStatus;
  } finally {
    control.disabled = false;
  }
}

function renderCandidates(incidents) {
  candidateList.replaceChildren();
  if (incidents.length === 0) {
    const empty = makeElement("div", "queue-empty");
    empty.append(
      makeElement("span", "empty-check", "✓"),
      makeElement("strong", "", "No review candidates"),
      makeElement("p", "", "No matching patterns were found in this sample. This is not a guarantee that a system is secure.")
    );
    candidateList.append(empty);
    return;
  }

  incidents.forEach((candidate, index) => {
    const card = makeElement("article", "candidate-card");
    const button = makeElement("button", "candidate-button");
    button.type = "button";
    button.setAttribute("aria-expanded", String(index === 0));
    button.setAttribute("aria-controls", `candidate-details-${index}`);
    const lead = makeElement("span", "candidate-lead");
    const priority = candidate.priority === "review" ? "REVIEW" : candidate.priority.toUpperCase();
    const priorityClass = candidate.priority === "review" ? "" : ` severity-tag-${candidate.priority}`;
    lead.append(
      makeElement("span", `severity-rail${candidate.priority === "review" ? "" : ` severity-rail-${candidate.priority}`}`),
      makeElement("span", "candidate-main")
    );
    const main = lead.querySelector(".candidate-main");
    main.append(
      makeElement("span", "candidate-title", candidate.title),
      makeElement("span", "candidate-subtitle", `${candidate.subjectLabel} · ${candidate.affectedUser}`)
    );
    const trailing = makeElement("span", "candidate-trailing");
    trailing.append(
      makeElement("span", `review-tag${priorityClass}`, priority),
      makeElement("span", "expand-chevron", "⌄")
    );
    button.append(
      lead,
      trailing
    );
    const detail = renderCandidateDetails(candidate);
    detail.id = `candidate-details-${index}`;
    detail.hidden = index !== 0;

    button.addEventListener("click", () => {
      const expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
      detail.hidden = expanded;
    });
    card.append(button, detail);
    candidateList.append(card);
  });
}

function renderEvents(events) {
  eventRows.replaceChildren();
  if (events.length === 0) {
    const row = makeElement("tr");
    const cell = makeElement("td", "table-loading", "No events in the current sample.");
    cell.colSpan = 5;
    row.append(cell);
    eventRows.append(row);
    return;
  }

  for (const event of events) {
    const row = makeElement("tr");
    const eventCell = makeElement("td");
    eventCell.append(
      makeElement("span", "event-type", event.eventType),
      makeElement("span", "event-source", event.source)
    );
    const summaryCell = makeElement("td", "event-summary-cell", event.summary);
    const entityCell = makeElement("td", "entity-cell");
    if (event.entities.length === 0) {
      entityCell.textContent = "—";
    } else {
      for (const entity of event.entities) {
        entityCell.append(makeElement("span", "entity-chip", `${entity.kind}: ${entity.value}`));
      }
    }
    const severityCell = makeElement("td");
    severityCell.append(makeElement("span", `severity-chip severity-${event.severity}`, event.severity));
    const timeCell = makeElement("td", "time-cell", formatShortTimestamp(event.observedAt));
    row.append(eventCell, summaryCell, entityCell, severityCell, timeCell);
    eventRows.append(row);
  }
}

async function loadDashboard() {
  if (dashboardLoading) return;
  dashboardLoading = true;
  refreshButton.disabled = true;
  errorBanner.hidden = true;
  errorBanner.textContent = "";

  try {
    const [eventsResponse, incidentsResponse, identityResponse] = await Promise.all([
      fetch("/api/v1/events", { headers: { accept: "application/json" } }),
      fetch("/api/v1/incidents", { headers: { accept: "application/json" } }),
      fetch("/api/v1/me", { headers: { accept: "application/json" } })
    ]);

    if ([eventsResponse, incidentsResponse, identityResponse].some((response) => response.status === 401)) {
      window.location.assign("/auth/login");
      return;
    }

    if (!eventsResponse.ok || !incidentsResponse.ok || !identityResponse.ok) {
      throw new Error("The local service could not load security review data.");
    }

    const [eventData, incidentData, identityData] = await Promise.all([
      eventsResponse.json(),
      incidentsResponse.json(),
      identityResponse.json()
    ]);

    if (!Array.isArray(eventData.events) || !Array.isArray(incidentData.incidents)) {
      throw new Error("The local service returned an unexpected data format.");
    }

    const isUploaded = eventData.mode === "uploaded";
    const isLive = eventData.mode === "live";
    const isWazuhJsonLines = eventData.format === "wazuh-json-lines";
    const isWazuh = isWazuhJsonLines || eventData.format === "wazuh-json";
    const sources = new Set(eventData.events.map((event) => event.source));
    canReviewCases = identityData.role === "admin" || identityData.role === "analyst";
    incidentCount.textContent = String(incidentData.incidents.length);
    eventCount.textContent = String(eventData.events.length);
    sourceCount.textContent = String(sources.size);
    navIncidentCount.textContent = String(incidentData.incidents.length);
    eventCountLabel.textContent = String(eventData.events.length);
    environmentLabel.replaceChildren(
      makeElement("span", "status-dot"),
      document.createTextNode(identityData.mode === "oidc"
        ? " AUTHENTICATED WORKSPACE"
        : isLive ? " LIVE WAZUH INDEXER"
        : isWazuh ? " WAZUH ALERT EXPORT" : isUploaded ? " LOCAL IMPORT" : " LOCAL WORKSPACE")
    );
    workspaceName.textContent = identityData.mode === "oidc"
      ? `Workspace ${identityData.tenantId}`
      : "Local workspace";
    workspaceSubtitle.textContent = identityData.mode === "oidc" ? "OIDC authenticated" : "Demo environment";
    profileName.textContent = identityData.mode === "oidc"
      ? identityData.displayName || identityData.email || "Workspace user"
      : "Local analyst";
    profileRole.textContent = identityData.mode === "oidc"
      ? identityData.role
      : "Analyst workspace";
    dataModeTitle.textContent = isLive
      ? "Live Wazuh alerts"
      : isWazuh ? "Wazuh alert export" : isUploaded ? "Imported events" : "Local sample";
    dataModeDescription.textContent = isUploaded
      ? `${isWazuh ? (isWazuhJsonLines ? "Wazuh JSONL" : "Wazuh JSON") : "Normalized JSON"} · memory only`
      : isLive
        ? `Latest indexed alerts · up to ${eventData.limits?.maxEvents ?? 500} alerts from the last ${eventData.limits?.lookbackHours ?? 24} hours`
        : "Demo events · not live telemetry";
    sourceDescription.replaceChildren(
      makeElement("span", "source-indicator"),
      document.createTextNode(isLive
        ? " Live Wazuh Indexer"
        : isWazuh ? " Wazuh export · not live" : isUploaded ? " Local JSON import" : " Demo connector only")
    );
    sourceTotal.textContent = `${sources.size} source${sources.size === 1 ? "" : "s"}`;
    sourceName.textContent = isLive
      ? "Wazuh Indexer"
      : isWazuh
      ? (isWazuhJsonLines ? "Wazuh JSONL export" : "Wazuh JSON export")
      : isUploaded ? "Local JSON import" : "Demo event connector";
    sourceDetail.textContent = isLive
      ? `${eventData.events.length} latest alerts · refreshes every 30 seconds`
      : isUploaded
      ? `${eventData.events.length} normalized events · memory only`
      : "Sample normalized events";
    sourceState.replaceChildren(
      makeElement("span", "source-indicator"),
      document.createTextNode(isLive ? " Connected" : isUploaded ? " Imported" : " Local")
    );
    eventPanelSubtitle.textContent = isUploaded
      ? "Normalized events imported for this local session"
      : isLive
        ? "Recent alerts returned by the configured Wazuh Indexer"
        : "Normalized events from the local demo connector";
    importButton.disabled = identityData.role !== "admin";
    importWazuhButton.disabled = identityData.role !== "admin";
    importButton.hidden = identityData.readOnly === true;
    importWazuhButton.hidden = identityData.readOnly === true;
    resetButton.hidden = !isUploaded || identityData.role !== "admin";
    workflowFootnote.textContent = identityData.readOnly === true
      ? "Public demo · read-only"
      : "Local workflow state · resets on restart";
    logoutButton.hidden = identityData.mode !== "oidc";
    livePollingEnabled = isLive;
    renderCandidates(incidentData.incidents);
    renderEvents(eventData.events);
  } catch (error) {
    errorBanner.textContent = error instanceof Error
      ? error.message
      : "Unable to load local review data.";
    errorBanner.hidden = false;
  } finally {
    dashboardLoading = false;
    refreshButton.disabled = false;
  }
}

async function importSelectedFile(file) {
  errorBanner.hidden = true;
  if (!file) return;
  if (file.size > MAX_FILE_BYTES) {
    errorBanner.textContent = "This file exceeds the 1 MiB import limit.";
    errorBanner.hidden = false;
    return;
  }

  importButton.disabled = true;
  try {
    const response = await fetch("/api/v1/events/import", {
      method: "POST",
      headers: { "content-type": "application/json", accept: "application/json" },
      body: await file.text()
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || "The event file could not be imported.");
    }
    await loadDashboard();
  } catch (error) {
    errorBanner.textContent = error instanceof Error
      ? error.message
      : "Unable to import the selected JSON file.";
    errorBanner.hidden = false;
  } finally {
    importButton.disabled = false;
    eventFile.value = "";
  }
}

async function importWazuhFile(file) {
  errorBanner.hidden = true;
  if (!file) return;
  if (file.size > MAX_FILE_BYTES) {
    errorBanner.textContent = "This file exceeds the 1 MiB import limit.";
    errorBanner.hidden = false;
    return;
  }

  importWazuhButton.disabled = true;
  try {
    const response = await fetch("/api/v1/events/import/wazuh", {
      method: "POST",
      headers: {
        "content-type": file.name.toLowerCase().endsWith(".json")
          ? "application/json"
          : "application/x-ndjson",
        accept: "application/json"
      },
      body: await file.text()
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || "The Wazuh alert file could not be imported.");
    }
    await loadDashboard();
  } catch (error) {
    errorBanner.textContent = error instanceof Error
      ? error.message
      : "Unable to import the selected Wazuh JSONL file.";
    errorBanner.hidden = false;
  } finally {
    importWazuhButton.disabled = false;
    wazuhFile.value = "";
  }
}

async function restoreDemoEvents() {
  resetButton.disabled = true;
  errorBanner.hidden = true;
  try {
    const response = await fetch("/api/v1/events/reset-demo", { method: "POST" });
    if (!response.ok) {
      throw new Error("Unable to restore the local sample.");
    }
    await loadDashboard();
  } catch (error) {
    errorBanner.textContent = error instanceof Error ? error.message : "Unable to restore the local sample.";
    errorBanner.hidden = false;
  } finally {
    resetButton.disabled = false;
  }
}

function signOut() {
  const form = document.createElement("form");
  form.method = "post";
  form.action = "/auth/logout";
  document.body.append(form);
  form.submit();
}

refreshButton.addEventListener("click", loadDashboard);
importButton.addEventListener("click", () => eventFile.click());
importWazuhButton.addEventListener("click", () => wazuhFile.click());
eventFile.addEventListener("change", () => {
  void importSelectedFile(eventFile.files?.[0]);
});
wazuhFile.addEventListener("change", () => {
  void importWazuhFile(wazuhFile.files?.[0]);
});
resetButton.addEventListener("click", restoreDemoEvents);
logoutButton.addEventListener("click", signOut);
loadDashboard();
window.setInterval(() => {
  if (livePollingEnabled && !document.hidden) {
    void loadDashboard();
  }
}, 30_000);
