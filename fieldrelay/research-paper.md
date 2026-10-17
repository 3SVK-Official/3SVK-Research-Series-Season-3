# FieldRelay: Durable Offline-to-Cloud Synchronization for Intermittently Connected Field Operations

**Author:** Zeeshan Ali Sheikh
**Challenge:** National Research & Innovation Challenge Season 3 — Cloud Innovation

## Abstract

Field teams may need to collect operational records in locations where connectivity is slow, unstable, or temporarily unavailable. A form that writes directly to a remote service couples data capture to network availability and can invite duplicate submissions when acknowledgements are delayed. FieldRelay is an offline-first synchronization prototype that stores each field record in a durable local outbox before transmission. When connectivity is available, the edge service sends bounded JSON batches to a cloud ingest API. The service authenticates each request with HMAC-SHA256, validates per-event content hashes, and uses event IDs to make repeated submissions idempotent. Bounded exponential retries and a dead-letter state provide a defined path for transient and persistent failures. The code includes separate edge and cloud services, a browser console, automated tests, and a local synthetic benchmark. The evaluation is designed to verify data handling and replay behavior; it does not claim production cloud throughput or field-trial outcomes.

**Keywords:** cloud engineering, offline-first systems, synchronization, idempotency, durable queue, data integrity, field operations

## 1. Problem Statement

A field operator may need to record supplies, service availability, or a site observation while the device has little or no connectivity. In a direct-to-cloud design, capture depends on a successful request to the central service. A timeout creates ambiguity: the server may not have received the record, or it may have committed the record while the response was lost. Retrying without an idempotency mechanism can create duplicates, while discarding the local submission can lose operational information.

FieldRelay addresses the interval between local capture and confirmed cloud acceptance. The objective is to preserve records across a disconnected period and make a later synchronization attempt safe to repeat. The project is intended for non-sensitive operational metadata, not personal or clinical records.

## 2. Design Goals

1. Save a record locally before any network request is made.
2. Keep record capture available while the simulated uplink is unavailable.
3. Support replay without inserting the same event twice.
4. Detect payload modification and reject reuse of an event ID with different content.
5. Bound batch size and retry behavior so repeated failures do not produce an unlimited request loop.
6. Make the behavior easy to verify using tests and a small local deployment.

## 3. System Architecture

FieldRelay contains two services. The edge service exposes the operator console and owns the local SQLite outbox. The cloud service exposes an ingest API and maintains a separate SQLite event store. Docker Compose runs the services in separate containers with separate persistent volumes.

The edge service assigns each record a UUID and UTC timestamp, then calculates a SHA-256 digest over its event content. The synchronization worker selects up to 50 ready records and sends a deterministic JSON body. An HMAC-SHA256 signature is calculated over the exact transmitted body. The cloud service checks the signature before parsing the request, validates the event schema and content digests, and checks for event ID collisions before committing any new event in the batch.

The response identifies newly accepted and already-seen event IDs. The edge service changes an event's state to `synced` only when all IDs in the request are accounted for by the acknowledgement. Failed requests remain in the outbox, receive an exponential retry schedule capped at 300 seconds, and move to `dead` after five failed attempts. A dead-letter record remains inspectable rather than being silently discarded.

## 4. Implementation

The edge and cloud services are written in Python using FastAPI. SQLite provides a lightweight persistent store for the prototype, with write-ahead logging enabled. The operator interface is served by the edge service and uses standard browser JavaScript. Requests are authenticated with a shared HMAC key provided through an environment variable; the repository contains an example environment file, not a production credential.

An event envelope contains `event_id`, `site_code`, `event_type`, `created_at`, `payload`, and `event_sha256`. The request signature protects the transmitted batch against undetected changes by an intermediary that does not possess the key. The event digest gives the service an additional way to detect a changed event body. Neither mechanism encrypts data at rest; deployment requires HTTPS and appropriate storage protection.

Idempotency is enforced by a unique key on `event_id` in the cloud store. An exact replay produces a duplicate acknowledgement. If a previously used ID arrives with a different event digest, the service rejects the batch with a conflict response and preserves the original record. These rules address the common uncertainty that follows a successful database commit and a lost network acknowledgement.

## 5. Evaluation Method

The automated tests exercise local persistence, retry scheduling, transition to dead-letter state, acknowledgement handling, valid signed ingestion, duplicate replay, invalid signatures, modified payloads, and event ID collisions. The benchmark script generates 1,000 synthetic operational events, submits them in batches of 50, then replays the same batches. It records runtime information, elapsed time, throughput across both passes, the number of new records, and the number of duplicate acknowledgements in `results/benchmark.json`.

This test-client benchmark runs in-process without a cloud host or external network. It evaluates the service's functional ingestion path and replay behavior; it is not a substitute for measuring latency, throughput, durability, or failure recovery on a deployed cloud platform. Results should be generated again on the machine used for the submission.

## 6. Results and Interpretation

The benchmark output is stored in `results/benchmark.json`. In the recorded run, 1,000 unique events were accepted in 20 batches and the same 20 batches were replayed. The service acknowledged all 1,000 replayed IDs as duplicates, and the cloud store still contained 1,000 unique events. The two passes took 0.1195 seconds in the recorded local run, or 16,738.05 combined record operations per second. Eight automated tests passed. These figures describe the recorded local test-client run only; the measured elapsed time and operations rate will vary by machine and runtime.

The tests additionally check that an invalid batch signature is refused, event content that no longer matches its digest is rejected, and conflicting content cannot overwrite a previously accepted event. These tests provide evidence for the implemented protocol behavior, not evidence of production reliability under arbitrary load or regional failure.

| Check | Recorded result | Scope |
|---|---:|---|
| Unique synthetic events accepted | 1,000 of 1,000 | Local in-process test client |
| Replayed events acknowledged as duplicates | 1,000 of 1,000 | Second pass over the same IDs |
| Unique cloud rows after replay | 1,000 | No duplicate rows added |
| Total time for acceptance and replay passes | 0.1195 seconds | Python 3.13.5, local test client |
| Combined record operations per second | 16,738.05 | Derived from 2,000 operations / elapsed time |
| Automated tests | 8 passed | Local test run |

## 7. Discussion

The main design decision is to separate the act of recording an observation from the act of delivering it. The edge outbox is the durable boundary for capture, while the cloud service is responsible for validation and idempotent persistence. Bounded batching reduces per-request overhead, and explicit acknowledgement handling prevents the client from marking unconfirmed records as synchronized.

The approach follows established queue-based load-leveling guidance: buffer work when the downstream service is temporarily unavailable, retry transient failures, and make consumers tolerate repeated delivery. The project combines these ideas in a small implementation that can run without a paid cloud account and can later replace SQLite with a managed database or durable queue.

## 8. Limitations and Future Work

The prototype currently uses one shared secret, a single cloud database, manual synchronization, and one edge queue. It has no user-level access policy, key rotation, per-tenant rate limits, automated background scheduler, or multi-region disaster recovery. The browser can continue capture only while the edge service itself is reachable; the simulated offline mode represents an unavailable uplink to the cloud, not a disconnected browser-to-edge link. The benchmark uses synthetic data and an in-process test client rather than an actual WAN or cloud deployment.

Next steps are to test on a low-bandwidth link, add authenticated field-team identities, rotate keys through a secret manager, add operational metrics and queue-depth alerts, and compare the SQLite implementation with a managed queue and relational database. A field trial should also measure duplicate rate, recovery time after reconnection, queue growth, and behavior under storage pressure.

## 9. Conclusion

FieldRelay demonstrates a practical design for field data capture that remains available through an uplink interruption. Its persistent outbox, signed batch protocol, content validation, idempotent cloud ingestion, and bounded retry state are implemented and covered by automated tests. The supplied benchmark checks unique storage and duplicate replay on synthetic records. Deployment-scale claims remain open until the prototype is evaluated against a real cloud service and intermittent network conditions.

## References

1. Microsoft, “Queue-Based Load Leveling Pattern,” Azure Architecture Center. https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling
2. Microsoft, “Messaging options,” Azure Architecture Center. https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/messaging
3. A. Rundgren, B. Jordan, and S. Erdtman, “JSON Canonicalization Scheme (JCS),” RFC 8785, June 2020. https://www.rfc-editor.org/rfc/rfc8785

## Reproducibility

Install the dependencies in `requirements.txt`, run `PYTHONPATH=src python -m pytest -q`, and execute `PYTHONPATH=src python scripts/benchmark.py`. The benchmark writes the run-specific result file to `results/benchmark.json`. For a browser demonstration, follow the local setup or Docker Compose instructions in `README.md`.
