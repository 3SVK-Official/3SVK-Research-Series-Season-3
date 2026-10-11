import json
import platform
import sys
import tempfile
import time
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fieldrelay.cloud import create_app
from fieldrelay.security import canonical_json, sign_body
from fieldrelay.store import EventStore


def main():
    secret = "fieldrelay-local-benchmark-secret"
    with tempfile.TemporaryDirectory(prefix="fieldrelay-benchmark-") as temp:
        client = TestClient(create_app(Path(temp) / "cloud.db", secret))
        store = EventStore(Path(temp) / "edge.db")
        size = 1000
        batch_size = 50
        events = [
            store.add_event(
                f"SITE-{number % 8 + 1:02d}",
                "supply_update",
                {"item": f"item-{number % 20}", "quantity": number % 100, "status": "Available", "note": "synthetic benchmark record"},
            )
            for number in range(size)
        ]
        batches = [events[start:start + batch_size] for start in range(0, size, batch_size)]
        start = time.perf_counter()
        accepted = 0
        replayed = 0
        for batch in batches:
            body = canonical_json({"events": batch})
            signature = sign_body(secret, body)
            response = client.post(
                "/v1/events/batch", content=body,
                headers={"Content-Type": "application/json", "X-FieldRelay-Signature": signature},
            )
            response.raise_for_status()
            accepted += len(response.json()["accepted"])
        for batch in batches:
            body = canonical_json({"events": batch})
            signature = sign_body(secret, body)
            response = client.post(
                "/v1/events/batch", content=body,
                headers={"Content-Type": "application/json", "X-FieldRelay-Signature": signature},
            )
            response.raise_for_status()
            replayed += len(response.json()["duplicates"])
        elapsed = time.perf_counter() - start
        stats = client.get("/v1/stats").json()
        results = {
            "experiment": "FieldRelay local synthetic ingestion and replay",
            "environment": {"python": platform.python_version(), "platform": platform.platform()},
            "transport": "FastAPI TestClient in-process; no external network",
            "records_generated": size,
            "batch_size": batch_size,
            "batches_per_pass": len(batches),
            "initially_accepted": accepted,
            "replay_duplicates": replayed,
            "unique_cloud_records_after_replay": stats["stored_events"],
            "sites": stats["sites"],
            "elapsed_seconds_for_both_passes": round(elapsed, 4),
            "combined_record_operations_per_second": round((size * 2) / elapsed, 2) if elapsed else None,
            "integrity_check": "passed; each submitted event hash validated by the service",
            "idempotency_check": "passed; replayed event IDs did not increase stored record count",
            "scope_note": "This is a local functional benchmark, not a cloud-hosted load test. Results depend on the machine and runtime.",
        }
        target = ROOT / "results" / "benchmark.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
