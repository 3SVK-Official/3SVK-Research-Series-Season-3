import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  createWazuhIndexerConnector,
  readWazuhIndexerSettings
} from "../src/connectors/wazuh/indexer-connector.js";

const settings = {
  url: new URL("https://indexer.example.test/"),
  username: "readonly-user",
  password: "test-password",
  index: "wazuh-alerts-*",
  lookbackHours: 24
};

const indexedAlert = {
  _id: "index-doc-1",
  _source: {
    timestamp: "2026-10-18T09:14:00.000+0000",
    rule: {
      level: 12,
      id: "5503",
      description: "Synthetic alert from the Wazuh Indexer.",
      groups: ["authentication_failed"],
      mitre: {
        id: ["T1110"],
        tactic: ["Credential Access"],
        technique: ["Brute Force"]
      }
    },
    agent: { id: "001", name: "test-host", ip: "192.0.2.14" },
    data: { srcuser: "analyst@example.test" },
    location: "/var/log/auth.log",
    full_log: "This value must not be retained."
  }
};

describe("Wazuh Indexer connector", () => {
  it("requires HTTPS credentials and validates index and time-window configuration", () => {
    assert.throws(
      () => readWazuhIndexerSettings({}),
      /requires WAZUH_INDEXER_URL/
    );

    const environment = {
      WAZUH_INDEXER_URL: "https://indexer.example.test/",
      WAZUH_INDEXER_USERNAME: "readonly-user",
      WAZUH_INDEXER_PASSWORD: "secret"
    };
    assert.deepEqual(readWazuhIndexerSettings(environment), {
      url: new URL("https://indexer.example.test/"),
      username: "readonly-user",
      password: "secret",
      index: "wazuh-alerts-*",
      lookbackHours: 24
    });
    assert.throws(
      () => readWazuhIndexerSettings({
        ...environment,
        WAZUH_INDEXER_URL: "http://indexer.example.test/"
      }),
      /must use HTTPS/
    );
    assert.throws(
      () => readWazuhIndexerSettings({
        ...environment,
        WAZUH_INDEXER_URL: "https://user:secret@indexer.example.test/"
      }),
      /must use HTTPS/
    );
    assert.throws(
      () => readWazuhIndexerSettings({
        ...environment,
        WAZUH_INDEXER_INDEX: "alerts/_search"
      }),
      /valid index name/
    );
    assert.throws(
      () => readWazuhIndexerSettings({
        ...environment,
        WAZUH_INDEXER_LOOKBACK_HOURS: "0"
      }),
      /integer from 1 to 168/
    );
    assert.equal(
      readWazuhIndexerSettings({
        ...environment,
        WAZUH_INDEXER_URL: "http://127.0.0.1:9200/"
      }).url.protocol,
      "http:"
    );
  });

  it("queries recent alerts using read-only search and normalizes alert context", async () => {
    let requestUrl = "";
    let requestInit: RequestInit | undefined;
    const connector = createWazuhIndexerConnector(settings, async (input, init) => {
      requestUrl = String(input);
      requestInit = init;
      return new Response(JSON.stringify({
        hits: { hits: [indexedAlert] }
      }), { status: 200, headers: { "content-type": "application/json" } });
    });

    const events = await connector.fetchEvents();
    assert.equal(connector.mode, "live");
    assert.equal(connector.name, "wazuh-indexer");
    assert.equal(requestUrl, "https://indexer.example.test/wazuh-alerts-*/_search");
    assert.equal(requestInit?.method, "POST");
    assert.equal(requestInit?.redirect, "error");
    assert.equal(
      new Headers(requestInit?.headers).get("authorization"),
      `Basic ${Buffer.from("readonly-user:test-password").toString("base64")}`
    );
    const query = JSON.parse(String(requestInit?.body)) as {
      size: number;
      sort: Array<Record<string, unknown>>;
      query: { range: { timestamp: { gte: string; lte: string } } };
    };
    assert.equal(query.size, 500);
    assert.deepEqual(query.sort, [
      { timestamp: { order: "desc" } },
      { _id: { order: "desc" } }
    ]);
    assert.deepEqual(query.query.range.timestamp, { gte: "now-24h", lte: "now" });
    assert.equal(events.length, 1);
    assert.equal(events[0].id, "index-doc-1");
    assert.equal(events[0].eventType, "authentication.failure");
    assert.equal(events[0].severity, "critical");
    assert.equal(events[0].wazuh?.mitre.ids[0], "T1110");
    assert.equal(JSON.stringify(events).includes("This value must not be retained"), false);
  });

  it("reuses a short-lived detached cache for parallel dashboard reads", async () => {
    let requests = 0;
    const connector = createWazuhIndexerConnector(settings, async () => {
      requests += 1;
      return new Response(JSON.stringify({ hits: { hits: [indexedAlert] } }), {
        status: 200
      });
    });

    const [first, second] = await Promise.all([
      connector.fetchEvents(),
      connector.fetchEvents()
    ]);
    assert.equal(requests, 1);
    first[0].entities.length = 0;
    const third = await connector.fetchEvents();
    assert.equal(requests, 1);
    assert.notEqual(first, second);
    assert.equal(third[0].entities.length > 0, true);
  });

  it("fails explicitly on HTTP errors and malformed indexed alerts", async () => {
    const unauthorized = createWazuhIndexerConnector(settings, async () =>
      new Response("unauthorized", { status: 401 }));
    await assert.rejects(
      () => unauthorized.fetchEvents(),
      /Wazuh Indexer returned HTTP 401/
    );

    const malformed = createWazuhIndexerConnector(settings, async () =>
      new Response(JSON.stringify({ hits: { hits: [{ _id: "missing-source" }] } }), {
        status: 200
      }));
    await assert.rejects(
      () => malformed.fetchEvents(),
      /result 1 is missing alert data/
    );
  });
});
