# SentinelOps — Incident Response Prototype

SentinelOps is a defensive security-event analysis prototype. It provides a
synthetic-data demo, local JSON/Wazuh file imports, and an optional read-only
Wazuh Indexer connector. It presents rule-based review candidates for human
assessment and does not perform automated response actions.

## Requirements

- Node.js 24 or newer
- npm

## Run locally

```powershell
npm install
npm test
npm run build
npm start
```

Open `http://127.0.0.1:4173/api/v1/events` to inspect the sample normalized
events. Open `http://127.0.0.1:4173/` for the local analyst review dashboard,
or `http://127.0.0.1:4173/api/v1/incidents` for its JSON data. The review queue
correlates failed sign-ins followed by a successful sign-in for the same
account within ten minutes. It also creates review candidates for high/critical
alerts and currently recognized Wazuh account-creation, file-discovery,
malware, vulnerability, privilege-escalation, web-attack, network-scan, and
file-integrity alerts. Other imported events receive a generic triage candidate
so they are not silently omitted. Candidates are analyst work items, not
confirmed incidents or proof of malicious activity; event-family classification
is heuristic and limited to the available alert fields. The standard local
development mode binds to `127.0.0.1`; do not expose that mode to the internet.

## Deploy a public Render demo

This repository includes a Render Blueprint in `render.yaml` for a public,
read-only hackathon demo. In Render, create a **New Blueprint Instance** from
this GitHub repository and deploy the `incident-response-demo` web service.
The Blueprint binds to Render's public interface with the synthetic demo
connector; it does not include Wazuh credentials or real alert data. Render
builds with `npm ci && npm run build`, starts with `npm start`, and uses
`/healthz` for its health check.

Public demo mode rejects every non-GET request at the server, including import,
reset, and incident workflow mutations. It also hides the import controls and
disables review status changes in the dashboard. This mode is intended only
for showing synthetic data. Do not change it to use live data or real customer
logs; use a private, authenticated deployment for those.

## Import test events

The dashboard's **Import JSON** action accepts normalized JSON in the format
shown by **Download normalized JSON format**, and automatically recognizes
Wazuh JSON files that contain one alert, an array of alerts, or an `events`
array. **Import Wazuh** accepts the same Wazuh documents plus JSON-lines
exports (`.json`, `.jsonl`, or `.ndjson`). Both paths are limited to 1 MiB and
500 events. The server validates the complete document before replacing the
current in-memory event set; unsupported fields (including raw log payloads),
duplicate IDs, invalid timestamps, and invalid event types are rejected.
**Restore sample** returns to the built-in synthetic events.

The Wazuh adapter maps alert IDs, timestamps, rule levels, descriptions,
groups, MITRE ATT&CK identifiers/tactics/techniques, agent details, decoder
names, locations, and selected decoded entities into the shared event model.
The review result shows this source context so an analyst can trace a
classification to its alert. It deliberately does not retain `full_log`,
command text, or arbitrary alert fields. Unknown alert families remain visible
as review candidates, but they are not automatically understood or detected as
specific attack types. Download the bundled synthetic example to try the
mapping. This file importer is not a live Wazuh API connector and does not use
Wazuh credentials. See the [Wazuh alert management documentation](https://documentation.wazuh.com/current/user-manual/manager/alert-management.html),
[Wazuh rules documentation](https://documentation.wazuh.com/current/user-manual/ruleset/rules/index.html),
and [MITRE ATT&CK integration documentation](https://documentation.wazuh.com/current/user-manual/ruleset/mitre.html).

## Local incident workflow

Review candidates can be moved through New, Investigating, and Resolved states.
The API rejects invalid transitions, exposes the status-change timestamps, and
requires a same-origin browser request for updates in local mode. Workflow
state is held only in process memory and resets on restart, successful event
import, or restore-sample. Changes are not attributed to a verified user and
do not form a durable audit trail; this workflow is for prototyping only.

## Connect to a Wazuh Indexer

To read recent alerts from an authorized Wazuh Indexer, configure
`ALERT_SOURCE=wazuh-indexer`, `WAZUH_INDEXER_URL`,
`WAZUH_INDEXER_USERNAME`, and `WAZUH_INDEXER_PASSWORD` before starting the
server. The URL must use HTTPS; HTTP is accepted only for loopback development.
The connector uses the indexer's standard read-only search endpoint with the
configured user's Basic authentication, queries `wazuh-alerts-*` by default,
and retrieves at most the latest 500 alerts from the last 24 hours by default.
Override the alert index with `WAZUH_INDEXER_INDEX` and the lookback window
with `WAZUH_INDEXER_LOOKBACK_HOURS` (1–168). Credentials should be stored in
the local environment or a secret manager, never committed to source control.
Use a least-privilege indexer account restricted to reading the alert indices;
do not disable TLS certificate verification.

The dashboard refreshes live data every 30 seconds while visible and also has
a manual refresh button. This is polling, not a streaming connector. A Wazuh
manager API URL alone is not an alert feed: this connector reads indexed alert
documents from the Wazuh Indexer. Its results are limited to the index range,
lookback window, permissions, and 500-alert batch limit configured above.
Wazuh remains responsible for its installed/configured rules and decoders; this
application analyzes and presents the alerts Wazuh has already generated.
Configure and validate data collection and alert generation in Wazuh itself.
See the [Wazuh Indexer documentation](https://documentation.wazuh.com/current/user-manual/wazuh-indexer/index.html),
[Wazuh API authentication documentation](https://documentation.wazuh.com/current/user-manual/api/getting-started.html),
and [Wazuh alert management documentation](https://documentation.wazuh.com/current/user-manual/manager/alert-management.html).

Imported events exist only in this server process's memory. They are not
persisted to disk, but can be read by clients able to access this local
development server. Restarting the process discards them. Do not import
production, personal, or otherwise sensitive logs.

## OIDC sign-in and workspace roles

Set `AUTH_MODE=oidc` to enable the standard OpenID Connect authorization-code
flow. Configure `OIDC_ISSUER_URL`, `OIDC_CLIENT_ID`,
`OIDC_CLIENT_SECRET`, `APP_BASE_URL`, and `OIDC_MEMBERSHIPS_JSON`. Optionally
set `OIDC_TOKEN_AUTH_METHOD` to `client_secret_basic` (default) or
`client_secret_post` if required by the identity provider. The
membership JSON maps exact identity-provider `sub` claim values to a
`tenantId` and a role (`viewer`, `analyst`, or `admin`). Unmapped identities
are denied; the app does not auto-provision users. The issuer must support
OIDC discovery, authorization code, PKCE S256, and standard ID tokens. One
issuer is configured per app instance; provider-specific features and
multi-issuer login are not included.

The browser flow uses the maintained `openid-client` library with state, nonce,
and PKCE verification. Sessions are opaque, HttpOnly, SameSite=Lax cookies
with an eight-hour lifetime; cookies are marked Secure when `APP_BASE_URL` is
HTTPS. Viewers can read their workspace, analysts can update review status,
and admins can import/reset events. Requests are partitioned by the configured
tenant identifier within the running process.

This is an initial integration, not production-ready identity infrastructure:
sessions, workspace membership, imported events, and workflow history are
process-memory only. Membership changes require configuration updates and a
restart. There is no database-backed session revocation, MFA enforcement,
tenant administration, durable audit, or multi-replica session sharing.
Production `APP_BASE_URL` and issuer URLs must use HTTPS. Set `HOST` to a
non-loopback interface only with `AUTH_MODE=oidc` and behind a properly
configured HTTPS reverse proxy. Do not use real customer data until durable
storage, deployment controls, and an authorized pilot have been implemented
and reviewed.

## Product boundary

This is still a prototype. The Render configuration is a public, read-only
synthetic-data demo. Standard local mode is unauthenticated and loopback-only.
OIDC mode provides single-process, configuration-mapped workspaces, but there
is no durable storage, central membership administration, durable audit trail,
or production deployment configuration. The optional Wazuh Indexer connector
reads already-generated alert documents; it does not collect endpoint logs or
replace Wazuh rules and decoders. It polls a bounded recent-alert window and
has not been validated against every Wazuh deployment. Do not expose standard
local mode to a network. OIDC mode is not ready for operational security
decisions. Local mutation endpoints reject browser requests with a non-loopback
or mismatched `Origin`; OIDC mode requires the exact configured application
origin. These are CSRF safeguards, not authorization; originless local
requests remain available to local clients. The case workflow does not make
candidate findings accurate or complete; all remain unverified analyst-review
signals.
Production work will require a threat model, an authorized pilot environment,
secret-management design, access control, tenant isolation, retention controls,
auditing, connector-specific least-privilege permissions, and a security review
before deployment. The product's response lifecycle should be designed against
[NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) and the
[NIST Cybersecurity Framework](https://www.nist.gov/cyberframework); technical
web controls should be verified against
[OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
and the [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/).
Detection coverage should map to a versioned source such as
[MITRE ATT&CK](https://attack.mitre.org/) without treating a mapping as proof
that an incident occurred.

## Render deployment details

The `render.yaml` Blueprint configures the public service named
`incident-response-demo` with `HOST=0.0.0.0`, `AUTH_MODE=local`,
`ALERT_SOURCE=demo`, and `READ_ONLY_DEMO=true`. The server rejects every
non-GET request in this mode and only serves synthetic events. No Wazuh
endpoint, credential, uploaded event data, or customer log is part of this
deployment configuration.

To deploy, import this repository into Render as a Blueprint and apply the
`incident-response-demo` service. Render builds with `npm ci && npm run build`,
starts with `npm start`, and checks `/healthz`. After deployment, use the
service URL supplied by Render. The prototype uses in-memory state and does
not provide a production availability or data-retention guarantee.
