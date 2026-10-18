<<<<<<< HEAD
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
hackathon demo. In Render, create a **New Blueprint Instance** from
this GitHub repository and deploy the `incident-response-demo` web service.
The Blueprint binds to Render's public interface with the synthetic demo
connector; it does not include Wazuh credentials or real alert data. Render
builds with `npm ci && npm run build`, starts with `npm start`, and uses
`/healthz` for its health check.

The public demo allows same-origin JSON/Wazuh file imports so visitors can try
the workflow. Uploads replace the shared in-memory event set for all visitors
and disappear when the service restarts. Any visitor can replace the displayed
data, so import synthetic or sanitized test alerts only. Reset and case-status
mutations remain disabled. Use a private, authenticated deployment for real
systems or customer logs.

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
`ALERT_SOURCE=demo`, `READ_ONLY_DEMO=true`, and `PUBLIC_DEMO_IMPORTS=true`.
Only same-origin event imports are enabled; reset and case-status changes are
blocked. Uploaded events are shared among visitors and held in memory only.
No Wazuh endpoint or credential is part of this deployment configuration.

To deploy, import this repository into Render as a Blueprint and apply the
`incident-response-demo` service. Render builds with `npm ci && npm run build`,
starts with `npm start`, and checks `/healthz`. After deployment, use the
service URL supplied by Render. The prototype uses in-memory state and does
not provide a production availability or data-retention guarantee.
=======
3SVK-Research-Series-Season-3 Official research archive, documentation, and proceedings for the National Research & Innovation Challenge Season 3 by 3SVK.

🔒 Intellectual Property, Copyright & Legal Notice © 2026 3SVK Official. All rights reserved.

The research tracks, problem statements, documentation, frameworks, and structural designs published in this repository are the exclusive intellectual property of 3SVK, protected under the Indian Copyright Act, 1957, and international copyright treaties.

Permitted Use: Registered participants may use the provided templates and resources strictly for the purpose of competing in the National Research & Innovation Challenge Season 3. Legal Prohibition: In accordance with the Copyright Act of India, any unauthorized reproduction, redistribution, adaptation, commercial exploitation, or plagiarism of these works without explicit written consent from 3SVK constitutes an infringement under Section 51 and is punishable under Section 63 and other applicable provisions of Indian law.

📚 Official Citation If you use, reference, or build upon this research series, please cite it via our permanent Zenodo DOI:

3SVK Official. (2026). 3SVK Research Series Season 3: Official Archive & Proceedings. Zenodo. https://doi.org/10.5281/zenodo.22008262

Adaptive Edge-AI Framework for Real-Time Anomaly Detection A resource-aware adaptive framework for real-time anomaly detection at the edge, dynamically balancing detection accuracy with computational constraints.

Research Objective This project investigates whether an adaptive, resource-aware edge-AI framework can detect anomalies in real time while reducing inference latency, network/data-transfer overhead, and computational resource consumption compared with a conventional centralized detection architecture without materially degrading detection performance.

Problem Addressed Traditional centralized anomaly detection systems incur high latency and network overhead, while static edge-based approaches lack flexibility to adapt to varying resource conditions. Existing edge-based systems typically employ fixed model complexity, leading to either over-provisioning (complex models exceeding available resources) or under-provisioning (simple models failing to detect subtle anomalies).

Implemented Approach The framework implements a utility-based adaptive controller that:

Dynamically selects between three detection models of varying complexity based on real-time CPU, memory, and network conditions Optimizes transmission decisions to balance local processing with cloud offloading when beneficial Employs a mathematically defined utility function that explicitly considers CPU, memory, latency, detection confidence, transmission costs, and model complexity Uses validation-based threshold calibration to prevent test-set leakage Adaptive Controller The adaptive controller maintains a state vector:

s = (cpu_util, mem_util, net_latency, bandwidth, data_difficulty, anomaly_confidence) At each decision point, the controller selects a model mode m ∈ {LIGHT, STANDARD, HEAVY} and transmission decision t ∈ {LOCAL_ONLY, TRANSMIT} by maximizing:

U(m, t) = w_cpu * (1 - cpu_cost(m)) + w_mem * (1 - mem_cost(m)) + w_lat * (1 - latency_cost(m, t)) + w_conf * confidence(m) - w_trans * trans_cost(t) - w_comp * complexity_cost(m) Subject to feasibility constraints:

cpu_util + cpu_overhead(m) ≤ cpu_threshold mem_util + mem_overhead(m) ≤ mem_threshold if t = TRANSMIT: net_latency ≤ latency_max Dataset The framework uses synthetic time-series data with:

5,000 samples 5% anomaly rate Train/Val/Test split: 70/15/15 Window size: 60 samples Normal samples: sinusoidal pattern with Gaussian noise Anomaly patterns: spikes, dips, sustained shifts, amplitude changes Detection Models Three models of increasing complexity are implemented:

LIGHT: Statistical Z-score based anomaly detector (fast, low memory) STANDARD: Autoencoder with reconstruction error (balanced) HEAVY: LSTM Autoencoder for temporal patterns (high accuracy, high computational cost) Leakage Prevention To prevent test-set leakage, all three systems (Centralized, Static Edge, Adaptive Edge) use validation-based threshold calibration with F1 optimization on the validation set before evaluating on the test set.

Validation-Based Threshold Calibration The ThresholdCalibrator class implements multiple calibration methods:

f1_optimize: Maximize F1 score on validation data (used in experiments) percentile: Use fixed percentile (e.g., 95th) precision_constrained: Maximize recall subject to precision constraint recall_constrained: Maximize precision subject to recall constraint This ensures fair comparison between systems and prevents overfitting to the test set.

Project Structure 3svk/ ├── configs/ # Configuration files │ └── default_config.yaml ├── diagrams/ # Architecture diagrams │ └── architecture.md ├── experiments/ # Experiment scripts │ ├── baseline_centralized/ │ ├── baseline_static_edge/ │ ├── proposed/ │ ├── ablation/ │ ├── verify_results.py │ └── generate_figures.py ├── figures/ # Generated figures and tables ├── references/ # Literature review and research gap │ ├── literature_review.md │ └── research_gap.md ├── results/ # Experiment results (JSON) ├── src/ # Source code │ ├── adaptive/ # Adaptive controller │ ├── cloud/ # Cloud coordinator │ ├── data/ # Data loading and streaming │ ├── edge/ # Edge processor │ ├── evaluation/ # Metrics and monitoring │ ├── models/ # Detection models │ └── preprocessing/ # Data preprocessing ├── tests/ # Unit tests ├── requirements.txt # Python dependencies ├── research-paper.md # Complete research paper └── README.md # This file Installation Prerequisites Python 3.14.6 pip Setup Clone the repository: git clone cd 3svk Install dependencies: python -m pip install -r requirements.txt Usage Running Experiments Run All Experiments python experiments/verify_results.py This will:

Run baseline centralized experiment Run baseline static edge experiment Run proposed adaptive edge experiment Save results to results/ directory Run Individual Experiments

Baseline A: Centralized Detection
python experiments/baseline_centralized/run.py

Baseline B: Static Edge Detection
python experiments/baseline_static_edge/run.py

Proposed: Adaptive Edge Framework
python experiments/proposed/run.py

Ablation Study
python experiments/ablation/run.py Generate Figures and Tables python experiments/generate_figures.py This will generate:

Benchmark comparison table Performance comparison plots Summary report Running Tests

Run all tests
python -m pytest tests/ -v

Run specific test file
python -m pytest tests/test_data.py -v python -m pytest tests/test_preprocessing.py -v python -m pytest tests/test_adaptive.py -v Configuration Edit configs/default_config.yaml to customize:

Data: Dataset parameters, window size, anomaly ratio Preprocessing: Normalization method, feature engineering Models: Model architectures and hyperparameters Controller: Utility function weights and thresholds Evaluation: Metrics to compute Experiments: Random seed, sample sizes Architecture Components Data Ingestion (src/data/)

DataLoader: Loads and splits datasets DataStream: Simulates streaming data with buffering Preprocessing (src/preprocessing/)

Preprocessor: Normalization and window creation FeatureEngineer: Rolling statistics and difference features Detection Models (src/models/)

IsolationForestModel: Lightweight statistical detector AutoencoderModel: Standard autoencoder LSTMAutoencoderModel: Heavy LSTM autoencoder Adaptive Controller (src/adaptive/)

AdaptiveController: Resource-aware decision making with utility function Processing (src/edge/, src/cloud/)

EdgeProcessor: Local processing with adaptive model selection CloudCoordinator: Centralized processing simulation Evaluation (src/evaluation/)

MetricsCalculator: Detection and system metrics SystemMonitor: CPU, memory, and network monitoring Three Implemented Systems

Centralized Detection (Baseline A) All data transmitted to cloud for processing Uses HEAVY model (LSTM Autoencoder) in cloud No local processing No adaptation
Static Edge Detection (Baseline B) All data processed locally Fixed STANDARD model (Autoencoder) No adaptation Transmits only anomaly events (30,720 bytes)
Adaptive Edge Framework (Proposed) Dynamic local/transmission decision Adaptive model selection (LIGHT/STANDARD/HEAVY) Resource-aware processing with utility function Transmits only anomaly events (30,720 bytes) Under current resource constraints, controller primarily selects STANDARD mode Experimental Methodology Detection Metrics Accuracy, Precision, Recall, F1-Score ROC-AUC, PR-AUC False Positive Rate, False Negative Rate Latency Measurement Centralized: Includes network transmission (uplink + downlink + inference) Edge systems: Measure local inference only Reported metrics: mean, std, min, max, p50, p95, p99 CPU Measurement Mean CPU utilization percentage Standard deviation Min/max values Memory Measurement Mean memory utilization percentage Standard deviation Min/max values Communication Measurement Total data transmitted in bytes Edge systems transmit only anomaly events Centralized transmits all data Current Verified Results Results from results/final_results.json (validated on 2026-09-09):
Detection Performance Method Accuracy Precision Recall F1-Score ROC-AUC PR-AUC Centralized 0.2142 0.0797 1.0000 0.1476 0.6190 0.0814 Static Edge 0.8683 0.1562 0.2128 0.1802 0.6128 0.1123 Adaptive Edge (Ours) 0.8683 0.1562 0.2128 0.1802 0.6128 0.1123 Note: All methods use validation-based threshold calibration (F1 optimization) to prevent test-set leakage. Edge methods achieve better F1 due to improved precision. The adaptive controller makes resource-aware decisions but primarily selects the STANDARD model under current resource constraints.

System Performance Method Latency (ms) CPU (%) Memory (%) Data (bytes) Centralized 101.13 59.66 77.88 331,680 Static Edge 0.39 37.90 77.30 30,720 Adaptive Edge (Ours) 0.50 47.61 79.90 30,720 Note: Centralized latency includes network transmission (uplink + downlink + inference). Edge systems measure local inference only. Edge systems transmit only anomaly events (30,720 bytes), while centralized transmits all data (331,680 bytes).

Key Improvements Latency: 99.61% reduction vs Centralized (Static Edge), 99.51% reduction vs Centralized (Adaptive Edge) Note: Latency reduction is due to network elimination (architectural advantage), not algorithmic improvement Data Transmission: 90.74% reduction vs Centralized (both Edge methods) Note: Data reduction due to local processing (architectural advantage) Detection Performance: Edge methods achieve 22.0% higher F1 vs Centralized (0.1802 vs 0.1476) Documentation Research Paper: research-paper.md - Complete research paper with methodology, results, and discussion Architecture: diagrams/architecture.md - Detailed system architecture Literature Review: references/literature_review.md - Related work and background Research Gap: references/research_gap.md - Problem statement and contribution Reproducibility All experiments use fixed random seeds (configured in default_config.yaml) to ensure reproducibility. Results are saved as JSON files in the results/ directory.

Python 3.14.6 Compatibility This project is tested and verified to work with Python 3.14.6. All dependencies are compatible with Python 3.14.6.

Limitations Synthetic Data: Evaluation on synthetic data may not reflect real-world performance Controller Tuning: Utility function weights require domain-specific calibration for optimal model switching Single Run: Results from single run; multiple runs with statistical reporting recommended for production Detection Performance: All methods have low F1 scores (<0.2), indicating challenging detection task or need for model improvement Adaptive Behavior: Under current resource constraints, the adaptive controller primarily selects the STANDARD mode, resulting in behavior similar to static edge processing License This project is submitted for the 3SVK Challenge.

Contact For questions or issues, please refer to the research paper or contact the authors.
>>>>>>> f313c139f210db05c8a8aa0db12c625271890e31
