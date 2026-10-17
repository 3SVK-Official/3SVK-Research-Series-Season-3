# FieldRelay

**Offline-first records for field operations**

FieldRelay lets a field team capture supply, service, and site observations when a network connection is unreliable, then synchronize them with a cloud endpoint when the connection returns. Each record is written to a durable local outbox first. The cloud service validates signed batches, verifies per-record hashes, and accepts replays without creating duplicate records.

## What is included

- Browser-based field console
- Persistent local SQLite outbox
- Batch synchronization with bounded exponential retry and a dead-letter state
- HMAC-SHA256 request authentication and per-event SHA-256 integrity checks
- Idempotent cloud ingestion with collision detection
- Docker Compose deployment with separate edge and cloud data volumes
- Unit tests and a reproducible local ingestion benchmark
- Research paper and system architecture

## Run with Docker Compose

Requirements: Docker Engine and Docker Compose.

1. Copy `.env.example` to `.env` and replace the secret with a random value.
2. Start the services:

   ```bash
   docker compose up --build
   ```

3. Open `http://localhost:8500` for the field console. The cloud API is available at `http://localhost:8000/health`.
4. Add several sample operational records. Choose **Simulate offline** and add more records; the queue should grow without marking those records as synced. Restore the connection and choose **Sync now**.
5. Open `http://localhost:8000/v1/stats` to see the cloud record count. Sync an already acknowledged record only once; replay checks are covered by the tests.

Do not put real personal, medical, or other sensitive data into the demonstration.

## Run locally without Docker

Use Python 3.11 or newer.

```bash
python -m venv .venv
```

Activate the virtual environment, install dependencies, and set a shared key in the same shell environment used by both services:

```bash
python -m pip install -r requirements.txt
```

Generate a key and export it. In Bash:

```bash
export FIELDRELAY_SHARED_SECRET="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export PYTHONPATH=src
uvicorn fieldrelay.cloud:app --host 127.0.0.1 --port 8000
```

In a second terminal, activate the same environment, set the same `FIELDRELAY_SHARED_SECRET`, set `PYTHONPATH=src`, and run:

```bash
uvicorn fieldrelay.edge:app --host 127.0.0.1 --port 8500
```

Open `http://127.0.0.1:8500`.

## Tests and benchmark

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/benchmark.py
```

The benchmark writes `results/benchmark.json`. It runs against an in-process test client and synthetic records; it is not a cloud load test. Keep results from your own run with the report rather than interpreting them as a production SLA.

## Design decisions

A local durable outbox separates record capture from network availability. Bounded batches reduce request overhead. Idempotent ingestion is necessary because a client may lose an acknowledgement after the server has already committed a batch. Each record is addressed by a stable event ID, and an ID reused with different content is rejected rather than silently overwritten. The request body is authenticated with HMAC-SHA256; per-event hashes provide an additional integrity check.

## Deployment boundary

The demo uses SQLite for both the edge outbox and cloud store. A production installation should use managed storage and backups, HTTPS, secret management and rotation, authorization per field team, request rate limits, retention rules, queue-depth alerts, and a managed queue or database if concurrent write volume grows.

## Project files

- `research-paper.md` — problem statement, implementation, evaluation, limits, and references
- `framework-record.md` — research-challenge technical record
- `docs/architecture.md` — components, data flow, and deployment notes
- `src/fieldrelay/` — edge service, cloud service, persistence, and request signing
- `tests/` — automated correctness tests
- `scripts/benchmark.py` — local synthetic benchmark
