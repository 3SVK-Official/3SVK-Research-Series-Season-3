# FieldRelay: Technical Framework Record

## 1. Title of the Project

- **Project name:** FieldRelay — Offline-First Cloud Synchronization for Field Operations
- **Framework identifier:** National Research & Innovation Challenge Season 3 — Cloud Innovation

## 2. Applicant Record

- **Primary applicant:** Zeeshan Ali Sheikh
- **Co-applicant / academic mentor:** Add only if applicable and approved by the named person
- **Nationality and permanent address:** Provide directly through the organizer's approved channel if specifically required. Do not publish residential details in a public repository.

## 3. Core Technical Abstract and Architecture

### Problem addressed

Field teams sometimes need to record supply levels, service availability, and site observations when connectivity is intermittent. A direct-to-cloud form can lose a submission or encourage repeated submissions when the response is delayed. FieldRelay separates capture from transmission by writing every record to a durable local outbox before attempting synchronization.

### Core innovation module 1 — Durable edge outbox

The edge service creates a unique event ID, records the event in SQLite, and retains its synchronization state. Ready records are sent in batches of up to 50. Failed batches receive bounded exponential retry scheduling, and repeatedly failing records move to a visible dead-letter state.

### Core innovation module 2 — Integrity-checked idempotent ingest

The sender signs each serialized batch with HMAC-SHA256. Each event also carries a SHA-256 digest of its canonical event content. The cloud API verifies the request signature, validates every record, and checks all existing IDs before writing. A repeated ID with unchanged content is acknowledged as a duplicate; a repeated ID with changed content is rejected.

### Communication and synchronization protocol

- Transport: JSON over HTTP in local development; HTTPS is required for deployment.
- Batch size: up to 50 events per request.
- Authentication: HMAC-SHA256 request signature in `X-FieldRelay-Signature`.
- Acknowledgement: accepted IDs and duplicate IDs are returned separately.
- Retry: bounded exponential delay, capped at 300 seconds; five failed attempts move a record to the dead-letter state.
- Persistence: separate SQLite databases for local outbox and cloud event store.

## 4. Performance and Validation Metrics

Recorded local run (Python 3.13.5, Linux): 1,000 synthetic events accepted in 20 batches; 1,000 replayed IDs acknowledged as duplicates; 1,000 unique cloud rows after replay; 0.1195 seconds for both passes; 16,738.05 combined record operations per second; eight automated tests passed. This was an in-process FastAPI test-client run, not a cloud-hosted load test. Run `PYTHONPATH=src python scripts/benchmark.py` to regenerate `results/benchmark.json` on the submitting machine before final submission.

Correctness tests cover local persistence, retry scheduling, acknowledgement handling, duplicate replay, signature validation, payload modification, and event ID collision handling.

## 5. Scope and Limitations

The present build is a functional prototype. It does not claim multi-region durability, automatic background synchronization, production key rotation, user-level authorization, or field deployment validation. Production use would require HTTPS, secret management, access control, monitoring, data-retention policy, backups, and a managed persistence layer.
