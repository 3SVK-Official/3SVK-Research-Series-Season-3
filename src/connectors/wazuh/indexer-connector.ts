import type { AlertConnector } from "../alert-connector.js";
import type { SecurityEvent } from "../../domain/security-event.js";
import { MAX_IMPORT_EVENTS } from "../../ingestion/validate-event-import.js";
import { normalizeWazuhAlert } from "./alert-import.js";

const MAX_RESPONSE_BYTES = 10 * 1024 * 1024;
const MAX_LOOKBACK_HOURS = 168;
const indexPattern = /^[a-z0-9][a-z0-9*_.-]{0,127}$/;

export interface WazuhIndexerSettings {
  url: URL;
  username: string;
  password: string;
  index: string;
  lookbackHours: number;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isLoopback(hostname: string): boolean {
  return ["localhost", "127.0.0.1", "[::1]"].includes(hostname.toLowerCase());
}

export function readWazuhIndexerSettings(
  environment: NodeJS.ProcessEnv = process.env
): WazuhIndexerSettings {
  const rawUrl = environment.WAZUH_INDEXER_URL;
  const username = environment.WAZUH_INDEXER_USERNAME;
  const password = environment.WAZUH_INDEXER_PASSWORD;
  const index = environment.WAZUH_INDEXER_INDEX ?? "wazuh-alerts-*";
  const lookbackHours = Number(environment.WAZUH_INDEXER_LOOKBACK_HOURS ?? "24");
  if (!rawUrl || !username || !password) {
    throw new Error(
      "Wazuh Indexer mode requires WAZUH_INDEXER_URL, WAZUH_INDEXER_USERNAME, and WAZUH_INDEXER_PASSWORD."
    );
  }

  let url: URL;
  try {
    url = new URL(rawUrl);
  } catch {
    throw new Error("WAZUH_INDEXER_URL must be a valid absolute URL.");
  }
  if (
    (url.protocol !== "https:" && !(url.protocol === "http:" && isLoopback(url.hostname))) ||
    url.username !== "" ||
    url.password !== "" ||
    url.pathname !== "/" ||
    url.search !== "" ||
    url.hash !== ""
  ) {
    throw new Error("WAZUH_INDEXER_URL must use HTTPS and contain only the indexer origin (HTTP is allowed on loopback).");
  }
  if (!username.trim() || !password.trim()) {
    throw new Error("Wazuh Indexer username and password must not be empty.");
  }
  if (!indexPattern.test(index) || index.includes("..")) {
    throw new Error("WAZUH_INDEXER_INDEX must be a valid index name or wildcard pattern.");
  }
  if (
    !Number.isInteger(lookbackHours) ||
    lookbackHours < 1 ||
    lookbackHours > MAX_LOOKBACK_HOURS
  ) {
    throw new Error(`WAZUH_INDEXER_LOOKBACK_HOURS must be an integer from 1 to ${MAX_LOOKBACK_HOURS}.`);
  }

  return { url, username, password, index, lookbackHours };
}

async function readBoundedResponse(response: Response): Promise<string> {
  const declaredLength = response.headers.get("content-length");
  if (declaredLength && Number(declaredLength) > MAX_RESPONSE_BYTES) {
    await response.body?.cancel();
    throw new Error("Wazuh Indexer response exceeds the 10 MiB limit.");
  }

  if (!response.body) return "";
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let length = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    length += value.length;
    if (length > MAX_RESPONSE_BYTES) {
      await reader.cancel();
      throw new Error("Wazuh Indexer response exceeds the 10 MiB limit.");
    }
    chunks.push(value);
  }
  const bytes = new Uint8Array(length);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.length;
  }
  return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
}

export function createWazuhIndexerConnector(
  settings: WazuhIndexerSettings,
  fetcher: typeof fetch = fetch
): AlertConnector {
  let cachedEvents: SecurityEvent[] | undefined;
  let cachedAt = 0;
  let pendingFetch: Promise<SecurityEvent[]> | undefined;

  async function queryIndexer(): Promise<SecurityEvent[]> {
    const endpoint = new URL(`${encodeURIComponent(settings.index)}/_search`, settings.url);
    const authorization = Buffer.from(
      `${settings.username}:${settings.password}`,
      "utf8"
    ).toString("base64");

    const response = await fetcher(endpoint, {
      method: "POST",
      redirect: "error",
      signal: AbortSignal.timeout(15_000),
      headers: {
        authorization: `Basic ${authorization}`,
        "content-type": "application/json",
        accept: "application/json"
      },
      body: JSON.stringify({
        size: MAX_IMPORT_EVENTS,
        track_total_hits: true,
        sort: [{ timestamp: { order: "desc" } }, { _id: { order: "desc" } }],
        query: {
          range: {
            timestamp: {
              gte: `now-${settings.lookbackHours}h`,
              lte: "now"
            }
          }
        }
      })
    });

    if (!response.ok) {
      await response.body?.cancel();
      throw new Error(`Wazuh Indexer returned HTTP ${response.status}.`);
    }

    const responseText = await readBoundedResponse(response);
    let payload: unknown;
    try {
      payload = JSON.parse(responseText) as unknown;
    } catch {
      throw new Error("Wazuh Indexer returned invalid JSON.");
    }
    if (
      !isRecord(payload) ||
      !isRecord(payload.hits) ||
      !Array.isArray(payload.hits.hits)
    ) {
      throw new Error("Wazuh Indexer returned an unexpected search response.");
    }

    const events = payload.hits.hits.map((hit, index) => {
      if (!isRecord(hit) || !isRecord(hit._source)) {
        throw new Error(`Wazuh Indexer result ${index + 1} is missing alert data.`);
      }
      const source = hit._source;
      return normalizeWazuhAlert({
        ...source,
        id: source.id ?? hit._id
      });
    });
    const ids = new Set<string>();
    for (const event of events) {
      if (ids.has(event.id)) {
        throw new Error(`Wazuh Indexer returned duplicate alert ID: ${event.id}`);
      }
      ids.add(event.id);
    }
    return events;
  }

  return {
    name: "wazuh-indexer",
    mode: "live",
    limits: {
      maxEvents: MAX_IMPORT_EVENTS,
      lookbackHours: settings.lookbackHours
    },
    async fetchEvents(): Promise<SecurityEvent[]> {
      if (cachedEvents && Date.now() - cachedAt < 10_000) {
        return structuredClone(cachedEvents);
      }
      if (!pendingFetch) {
        pendingFetch = queryIndexer();
      }
      try {
        const events = await pendingFetch;
        cachedEvents = structuredClone(events);
        cachedAt = Date.now();
        return structuredClone(events);
      } finally {
        pendingFetch = undefined;
      }
    }
  };
}
