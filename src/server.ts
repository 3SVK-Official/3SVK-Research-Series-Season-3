import { createServer, type Server } from "node:http";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { findAuthenticationSequenceCandidates } from "./analysis/authentication-sequence.js";
import { InMemoryIncidentWorkflow, isIncidentStatus } from "./analysis/incident-workflow.js";
import { createDemoConnector } from "./connectors/demo-connector.js";
import type { AlertConnector } from "./connectors/alert-connector.js";
import {
  createWazuhIndexerConnector,
  readWazuhIndexerSettings
} from "./connectors/wazuh/indexer-connector.js";
import {
  canImportEvents,
  canReviewIncidents,
  type AuthenticationService,
  OidcAuthenticator,
  type AuthenticatedPrincipal
} from "./security/oidc-auth.js";
import {
  isWazuhJsonDocument,
  normalizeWazuhJson,
  normalizeWazuhJsonLines,
  WazuhImportError
} from "./connectors/wazuh/alert-import.js";
import type { SecurityEvent } from "./domain/security-event.js";
import {
  EventImportValidationError,
  MAX_IMPORT_BYTES,
  validateEventImport
} from "./ingestion/validate-event-import.js";

const staticAssets = new Map([
  ["/", {
    body: readFileSync(new URL("../public/index.html", import.meta.url)),
    contentType: "text/html; charset=utf-8"
  }],
  ["/app.css", {
    body: readFileSync(new URL("../public/app.css", import.meta.url)),
    contentType: "text/css; charset=utf-8"
  }],
  ["/app.js", {
    body: readFileSync(new URL("../public/app.js", import.meta.url)),
    contentType: "text/javascript; charset=utf-8"
  }],
  ["/event-import-template.json", {
    body: readFileSync(new URL("../public/event-import-template.json", import.meta.url)),
    contentType: "application/json; charset=utf-8"
  }],
  ["/wazuh-alerts-example.jsonl", {
    body: readFileSync(new URL("../public/wazuh-alerts-example.jsonl", import.meta.url)),
    contentType: "application/x-ndjson; charset=utf-8"
  }]
]);

function sendJson(
  response: import("node:http").ServerResponse,
  statusCode: number,
  body: unknown
): void {
  response.writeHead(statusCode, {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
    "x-content-type-options": "nosniff",
    "x-frame-options": "DENY",
    "referrer-policy": "no-referrer"
  });
  response.end(JSON.stringify(body));
}

function sendStaticAsset(
  response: import("node:http").ServerResponse,
  body: Buffer,
  contentType: string
): void {
  response.writeHead(200, {
    "content-type": contentType,
    "cache-control": "no-store",
    "x-content-type-options": "nosniff",
    "x-frame-options": "DENY",
    "referrer-policy": "no-referrer",
    "content-security-policy":
      "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; " +
      "img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
  });
  response.end(body);
}

class ImportRequestError extends Error {
  constructor(
    message: string,
    readonly statusCode: number
  ) {
    super(message);
  }
}

async function readRequestText(
  request: import("node:http").IncomingMessage,
  acceptedContentTypes: string[]
): Promise<string> {
  const contentType = request.headers["content-type"]?.split(";")[0].trim().toLowerCase();
  if (!contentType || !acceptedContentTypes.includes(contentType)) {
    request.resume();
    throw new ImportRequestError(`Content-Type must be ${acceptedContentTypes.join(" or ")}.`, 415);
  }

  const declaredLength = request.headers["content-length"];
  if (declaredLength && Number(declaredLength) > MAX_IMPORT_BYTES) {
    request.resume();
    throw new ImportRequestError("Import exceeds the 1 MiB size limit.", 413);
  }

  const chunks: Buffer[] = [];
  let totalBytes = 0;
  let tooLarge = false;
  for await (const chunk of request) {
    const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    totalBytes += buffer.length;
    if (totalBytes > MAX_IMPORT_BYTES) {
      tooLarge = true;
      chunks.length = 0;
    } else if (!tooLarge) {
      chunks.push(buffer);
    }
  }

  if (tooLarge) {
    throw new ImportRequestError("Import exceeds the 1 MiB size limit.", 413);
  }

  try {
    return new TextDecoder("utf-8", { fatal: true }).decode(Buffer.concat(chunks, totalBytes));
  } catch {
    throw new ImportRequestError("Request body must be valid UTF-8 text.", 400);
  }
}

async function readJsonImportBody(request: import("node:http").IncomingMessage): Promise<unknown> {
  const text = await readRequestText(request, ["application/json"]);
  try {
    return JSON.parse(text) as unknown;
  } catch {
    throw new ImportRequestError("Request body must be valid UTF-8 JSON.", 400);
  }
}

function hasAllowedMutationOrigin(request: import("node:http").IncomingMessage): boolean {
  const origin = request.headers.origin;
  if (origin === undefined) {
    return true;
  }

  try {
    const originUrl = new URL(origin);
    const requestUrl = new URL(
      request.url ?? "/",
      `http://${request.headers.host ?? "localhost"}`
    );
    const loopbackHosts = new Set(["127.0.0.1", "localhost", "[::1]"]);
    return (
      originUrl.origin === requestUrl.origin &&
      originUrl.protocol === "http:" &&
      loopbackHosts.has(originUrl.hostname.toLowerCase())
    );
  } catch {
    return false;
  }
}

function cookieValue(
  request: import("node:http").IncomingMessage,
  name: string
): string | undefined {
  const cookieHeader = request.headers.cookie;
  if (!cookieHeader) return undefined;
  for (const pair of cookieHeader.split(";")) {
    const separator = pair.indexOf("=");
    if (separator < 0 || pair.slice(0, separator).trim() !== name) continue;
    try {
      return decodeURIComponent(pair.slice(separator + 1).trim());
    } catch {
      return undefined;
    }
  }
  return undefined;
}

function cookieHeader(
  name: string,
  value: string,
  options: { secure: boolean; maxAge: number }
): string {
  return `${name}=${encodeURIComponent(value)}; Path=/; Max-Age=${options.maxAge}; HttpOnly; SameSite=Lax${options.secure ? "; Secure" : ""}`;
}

export interface AppServerOptions {
  authMode?: "local" | "oidc";
  authenticator?: AuthenticationService;
  readOnlyDemo?: boolean;
}

export function createAppServer(
  connector: AlertConnector = createDemoConnector(),
  options: AppServerOptions = {}
): Server {
  const authMode = options.authMode ?? "local";
  const readOnlyDemo = options.readOnlyDemo ?? false;
  if (authMode !== "local" && authMode !== "oidc") {
    throw new Error("AUTH_MODE must be local or oidc.");
  }
  if (readOnlyDemo && (authMode !== "local" || connector.mode !== "demo")) {
    throw new Error("Read-only public demo mode requires local authentication and the demo connector.");
  }
  if (authMode === "oidc" && !options.authenticator) {
    throw new Error("OIDC mode requires a configured OIDC authenticator.");
  }
  const authenticator = options.authenticator;
  const importedEvents = new Map<string, SecurityEvent[]>();
  const importedFormats = new Map<string, "normalized-json" | "wazuh-json" | "wazuh-json-lines">();
  const workflows = new Map<string, InMemoryIncidentWorkflow>();
  const workflowFor = (tenantId: string): InMemoryIncidentWorkflow => {
    let workflow = workflows.get(tenantId);
    if (!workflow) {
      workflow = new InMemoryIncidentWorkflow();
      workflows.set(tenantId, workflow);
    }
    return workflow;
  };
  const server = createServer(async (request, response) => {
    const pathname = new URL(request.url ?? "/", "http://localhost").pathname;
    const staticAsset = staticAssets.get(pathname);
    const isEventImport = pathname === "/api/v1/events/import";
    const isWazuhImport = pathname === "/api/v1/events/import/wazuh";
    const isDemoReset = pathname === "/api/v1/events/reset-demo";
    const isLogin = pathname === "/auth/login";
    const isCallback = pathname === "/auth/callback";
    const isLogout = pathname === "/auth/logout";
    const isCurrentPrincipal = pathname === "/api/v1/me";
    const incidentIdMatch = /^\/api\/v1\/incidents\/([^/]+)$/.exec(pathname);
    const isIncidentUpdate = incidentIdMatch !== null;

    if (
      !staticAsset &&
      pathname !== "/healthz" &&
      pathname !== "/api/v1/events" &&
      pathname !== "/api/v1/incidents" &&
      !isLogin &&
      !isCallback &&
      !isLogout &&
      !isCurrentPrincipal &&
      !isIncidentUpdate &&
      !isEventImport &&
      !isWazuhImport &&
      !isDemoReset
    ) {
      sendJson(response, 404, { error: "Not found" });
      return;
    }

    if (readOnlyDemo && request.method !== "GET") {
      response.setHeader("allow", "GET");
      sendJson(response, 405, { error: "This public demo is read-only." });
      return;
    }

    if ((isLogin || isCallback) && request.method !== "GET") {
      response.setHeader("allow", "GET");
      sendJson(response, 405, { error: "Method not allowed" });
      return;
    }
    if (isLogout && request.method !== "POST") {
      response.setHeader("allow", "POST");
      sendJson(response, 405, { error: "Method not allowed" });
      return;
    }

    if (isLogin) {
      if (authMode !== "oidc" || !authenticator) {
        sendJson(response, 404, { error: "Not found" });
        return;
      }
      try {
        const flow = await authenticator.beginLogin();
        response.writeHead(302, {
          location: flow.authorizationUrl.href,
          "cache-control": "no-store",
          "set-cookie": cookieHeader("oidc_flow", flow.flowId, {
            secure: authenticator.usesSecureCookies(),
            maxAge: 600
          })
        });
        response.end();
      } catch (error) {
        console.error(`OIDC login initialization failed: ${error instanceof Error ? error.name : "UnknownError"}`);
        sendJson(response, 503, { error: "Sign-in is temporarily unavailable." });
      }
      return;
    }

    if (isCallback) {
      if (authMode !== "oidc" || !authenticator) {
        sendJson(response, 404, { error: "Not found" });
        return;
      }
      try {
        const callbackUrl = authenticator.callbackUrl(
          new URL(request.url ?? "/", "http://localhost").search
        );
        const login = await authenticator.completeLogin(
          callbackUrl,
          cookieValue(request, "oidc_flow")
        );
        if (!login) {
          response.setHeader("set-cookie", cookieHeader("oidc_flow", "", {
            secure: authenticator.usesSecureCookies(),
            maxAge: 0
          }));
          sendJson(response, 403, { error: "This identity is not assigned to a workspace." });
          return;
        }
        response.writeHead(302, {
          location: "/",
          "cache-control": "no-store",
          "set-cookie": [
            cookieHeader("sentinel_session", login.sessionId, {
              secure: authenticator.usesSecureCookies(),
              maxAge: 8 * 60 * 60
            }),
            cookieHeader("oidc_flow", "", {
              secure: authenticator.usesSecureCookies(),
              maxAge: 0
            })
          ]
        });
        response.end();
      } catch (error) {
        console.error(`OIDC callback failed: ${error instanceof Error ? error.name : "UnknownError"}`);
        response.setHeader("set-cookie", cookieHeader("oidc_flow", "", {
          secure: authenticator.usesSecureCookies(),
          maxAge: 0
        }));
        sendJson(response, 401, { error: "Sign-in could not be completed." });
      }
      return;
    }

    if (isLogout) {
      if (authMode !== "oidc" || !authenticator) {
        sendJson(response, 404, { error: "Not found" });
        return;
      }
      if (!authenticator.acceptsOrigin(request.headers.origin)) {
        sendJson(response, 403, { error: "Cross-origin requests are not allowed." });
        return;
      }
      authenticator.revokeSession(cookieValue(request, "sentinel_session"));
      response.writeHead(303, {
        location: "/auth/login",
        "cache-control": "no-store",
        "set-cookie": cookieHeader("sentinel_session", "", {
          secure: authenticator.usesSecureCookies(),
          maxAge: 0
        })
      });
      response.end();
      return;
    }

    if (pathname === "/healthz" && request.method === "GET") {
      sendJson(response, 200, { status: "ok" });
      return;
    }

    const principal: AuthenticatedPrincipal | undefined = authMode === "oidc"
      ? authenticator?.getPrincipal(cookieValue(request, "sentinel_session"))
      : {
          subject: "local-analyst",
          tenantId: "local",
          role: readOnlyDemo ? "viewer" : "admin"
        };

    if (isCurrentPrincipal) {
      if (!principal) {
        sendJson(response, 401, { error: "Authentication required." });
      } else {
        sendJson(response, 200, {
          subject: principal.subject,
          tenantId: principal.tenantId,
          role: principal.role,
          email: principal.email,
          displayName: principal.displayName,
          mode: authMode,
          readOnly: readOnlyDemo
        });
      }
      return;
    }

    if (authMode === "oidc" && !principal) {
      if (pathname === "/") {
        response.writeHead(302, { location: "/auth/login", "cache-control": "no-store" });
        response.end();
      } else {
        sendJson(response, 401, { error: "Authentication required." });
      }
      return;
    }
    if (!principal) {
      sendJson(response, 401, { error: "Authentication required." });
      return;
    }

    const tenantId = principal.tenantId;
    const tenantWorkflow = workflowFor(tenantId);

    if (
      (isEventImport || isWazuhImport || isDemoReset) &&
      request.method !== "POST"
    ) {
      response.setHeader("allow", "POST");
      sendJson(response, 405, { error: "Method not allowed" });
      return;
    }

    if (
      ((isEventImport || isWazuhImport || isDemoReset) && request.method === "POST" ||
        isIncidentUpdate && request.method === "PATCH") &&
      !(authMode === "oidc"
        ? authenticator?.acceptsOrigin(request.headers.origin)
        : hasAllowedMutationOrigin(request))
    ) {
      sendJson(response, 403, { error: "Cross-origin requests are not allowed." });
      return;
    }

    if (isIncidentUpdate && request.method !== "PATCH") {
      response.setHeader("allow", "PATCH");
      sendJson(response, 405, { error: "Method not allowed" });
      return;
    }

    if ((isEventImport || isWazuhImport || isDemoReset) && !canImportEvents(principal.role)) {
      sendJson(response, 403, { error: "Administrator role required." });
      return;
    }
    if (isIncidentUpdate && !canReviewIncidents(principal.role)) {
      sendJson(response, 403, { error: "Analyst role required." });
      return;
    }

    if (isEventImport && request.method === "POST") {
      try {
        const payload = await readJsonImportBody(request);
        const isWazuh = isWazuhJsonDocument(payload);
        const events = isWazuh
          ? normalizeWazuhJson(JSON.stringify(payload))
          : validateEventImport(payload);
        const format = isWazuh ? "wazuh-json" : "normalized-json";
        importedEvents.set(tenantId, events);
        importedFormats.set(tenantId, format);
        tenantWorkflow.clear();
        sendJson(response, 200, {
          imported: events.length,
          mode: "uploaded",
          format
        });
      } catch (error) {
        if (error instanceof ImportRequestError) {
          sendJson(response, error.statusCode, { error: error.message });
          return;
        }
        if (error instanceof EventImportValidationError) {
          sendJson(response, 400, { error: error.message });
          return;
        }
        if (error instanceof WazuhImportError) {
          sendJson(response, 400, { error: error.message });
          return;
        }
        console.error(`Event import failed: ${error instanceof Error ? error.name : "UnknownError"}`);
        sendJson(response, 500, { error: "Unable to import events." });
      }
      return;
    }

    if (isWazuhImport && request.method === "POST") {
      try {
        const body = await readRequestText(request, [
          "application/json",
          "application/x-ndjson",
          "application/ndjson"
        ]);
        const contentType = request.headers["content-type"]?.split(";")[0].trim().toLowerCase();
        const events = contentType === "application/json"
          ? normalizeWazuhJson(body)
          : normalizeWazuhJsonLines(body);
        const format = contentType === "application/json"
          ? "wazuh-json"
          : "wazuh-json-lines";
        importedEvents.set(tenantId, events);
        importedFormats.set(tenantId, format);
        tenantWorkflow.clear();
        sendJson(response, 200, {
          imported: events.length,
          mode: "uploaded",
          format
        });
      } catch (error) {
        if (error instanceof ImportRequestError) {
          sendJson(response, error.statusCode, { error: error.message });
          return;
        }
        if (error instanceof WazuhImportError) {
          sendJson(response, 400, { error: error.message });
          return;
        }
        console.error(`Wazuh import failed: ${error instanceof Error ? error.name : "UnknownError"}`);
        sendJson(response, 500, { error: "Unable to import Wazuh alerts." });
      }
      return;
    }

    if (isDemoReset && request.method === "POST") {
      importedEvents.delete(tenantId);
      importedFormats.delete(tenantId);
      tenantWorkflow.clear();
      sendJson(response, 200, { mode: "demo" });
      return;
    }

    if (isIncidentUpdate && request.method === "PATCH") {
      try {
        const payload = await readJsonImportBody(request);
        if (
          typeof payload !== "object" ||
          payload === null ||
          Array.isArray(payload) ||
          Object.keys(payload).length !== 1 ||
          !("status" in payload) ||
          !isIncidentStatus(payload.status)
        ) {
          sendJson(response, 400, { error: "Body must contain one valid incident status." });
          return;
        }

        const events = importedEvents.get(tenantId) ?? await connector.fetchEvents();
        const incidents = findAuthenticationSequenceCandidates(events);
        let incidentId: string;
        try {
          incidentId = decodeURIComponent(incidentIdMatch[1]);
        } catch {
          sendJson(response, 400, { error: "Incident identifier is malformed." });
          return;
        }
        const candidate = incidents.find((incident) => incident.id === incidentId);
        if (!candidate) {
          sendJson(response, 404, { error: "Incident not found." });
          return;
        }

        const state = tenantWorkflow.transition(incidentId, payload.status);
        if (!state) {
          sendJson(response, 409, { error: "Incident status transition is not allowed." });
          return;
        }
        sendJson(response, 200, { incident: { ...candidate, ...state } });
      } catch (error) {
        if (error instanceof ImportRequestError) {
          sendJson(response, error.statusCode, { error: error.message });
          return;
        }
        console.error(`Incident update failed: ${error instanceof Error ? error.name : "UnknownError"}`);
        sendJson(response, 503, { error: "Unable to update incident status." });
      }
      return;
    }

    if (request.method !== "GET") {
      response.setHeader(
        "allow",
        isEventImport || isWazuhImport || isDemoReset ? "GET, POST" : "GET"
      );
      sendJson(response, 405, { error: "Method not allowed" });
      return;
    }

    if (staticAsset) {
      sendStaticAsset(response, staticAsset.body, staticAsset.contentType);
      return;
    }

    if (pathname === "/healthz") {
      sendJson(response, 200, { status: "ok" });
      return;
    }

    try {
      const events = importedEvents.get(tenantId) ?? await connector.fetchEvents();
      if (pathname === "/api/v1/events") {
        sendJson(response, 200, {
          events,
          mode: importedEvents.has(tenantId) ? "uploaded" : connector.mode ?? "demo",
          persistence: importedEvents.has(tenantId) || connector.mode !== "live"
            ? "memory-only"
            : "source",
          source: connector.name,
          limits: connector.limits,
          format: importedFormats.get(tenantId)
        });
        return;
      }

      const incidents = findAuthenticationSequenceCandidates(events).map((incident) => ({
        ...incident,
        ...tenantWorkflow.get(incident.id)
      }));
      sendJson(response, 200, { incidents });
    } catch (error) {
      const errorName = error instanceof Error ? error.name : "UnknownError";
      console.error(`Alert connector "${connector.name}" failed: ${errorName}`);
      sendJson(response, 503, { error: "Alert source is temporarily unavailable" });
    }
  });
  server.requestTimeout = 30_000;
  return server;
}

const port = Number(process.env.PORT ?? "4173");
if (!Number.isInteger(port) || port < 1024 || port > 65535) {
  throw new Error("PORT must be an integer between 1024 and 65535.");
}

function isLoopbackAddress(host: string): boolean {
  return ["127.0.0.1", "localhost", "::1", "[::1]"].includes(host.toLowerCase());
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  void (async () => {
    const configuredAuthMode = process.env.AUTH_MODE;
    if (configuredAuthMode && configuredAuthMode !== "local" && configuredAuthMode !== "oidc") {
      throw new Error("AUTH_MODE must be local or oidc.");
    }
    const authMode: "local" | "oidc" = configuredAuthMode === "oidc" ? "oidc" : "local";
    const alertSource = process.env.ALERT_SOURCE ?? "demo";
    if (alertSource !== "demo" && alertSource !== "wazuh-indexer") {
      throw new Error("ALERT_SOURCE must be demo or wazuh-indexer.");
    }
    const rawReadOnlyDemo = process.env.READ_ONLY_DEMO ?? "false";
    if (rawReadOnlyDemo !== "true" && rawReadOnlyDemo !== "false") {
      throw new Error("READ_ONLY_DEMO must be true or false.");
    }
    const readOnlyDemo = rawReadOnlyDemo === "true";
    if (readOnlyDemo && (authMode !== "local" || alertSource !== "demo")) {
      throw new Error("READ_ONLY_DEMO requires AUTH_MODE=local and ALERT_SOURCE=demo.");
    }
    const host = process.env.HOST ?? "127.0.0.1";
    if (
      authMode === "local" &&
      !isLoopbackAddress(host) &&
      !readOnlyDemo
    ) {
      throw new Error("Local demo mode may bind only to a loopback address unless READ_ONLY_DEMO=true.");
    }
    const authenticator = authMode === "oidc"
      ? await OidcAuthenticator.create()
      : undefined;
    const connector = alertSource === "wazuh-indexer"
      ? createWazuhIndexerConnector(readWazuhIndexerSettings())
      : createDemoConnector();
    const server = createAppServer(connector, { authMode, authenticator, readOnlyDemo });
    server.listen(port, host, () => {
      console.log(
        `Application listening on ${readOnlyDemo ? "public read-only demo" : authMode === "oidc" ? "OIDC-protected" : "local"} interface ${host}:${port}`
      );
    });
  })().catch((error: unknown) => {
    console.error(
      `Application startup failed: ${error instanceof Error ? error.message : "Unknown error"}`
    );
    process.exitCode = 1;
  });
}
