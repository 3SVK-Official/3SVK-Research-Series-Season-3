import json
import sqlite3
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from fieldrelay.security import digest


class EventStore:
    def __init__(self, path, max_attempts=5, base_delay_seconds=2, max_delay_seconds=300):
        self.path = str(path)
        self.max_attempts = max_attempts
        self.base_delay_seconds = base_delay_seconds
        self.max_delay_seconds = max_delay_seconds
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute(
                """CREATE TABLE IF NOT EXISTS outbox (
                    event_id TEXT PRIMARY KEY,
                    event_json TEXT NOT NULL,
                    event_sha256 TEXT NOT NULL,
                    state TEXT NOT NULL DEFAULT 'pending',
                    attempts INTEGER NOT NULL DEFAULT 0,
                    next_attempt_at REAL NOT NULL DEFAULT 0,
                    last_error TEXT,
                    created_at TEXT NOT NULL,
                    synced_at TEXT
                )"""
            )

    @contextmanager
    def connection(self):
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def add_event(self, site_code, event_type, payload):
        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        core = {
            "event_id": str(uuid.uuid4()),
            "site_code": site_code.strip(),
            "event_type": event_type,
            "created_at": created_at,
            "payload": payload,
        }
        event = {**core, "event_sha256": digest(core)}
        with self.connection() as connection:
            connection.execute(
                "INSERT INTO outbox(event_id,event_json,event_sha256,state,attempts,next_attempt_at,created_at) VALUES(?,?,?,'pending',0,0,?)",
                (event["event_id"], json.dumps(event, ensure_ascii=False, sort_keys=True), event["event_sha256"], created_at),
            )
        return event

    def ready_batch(self, limit=50, now=None):
        now = time.time() if now is None else now
        with self.connection() as connection:
            rows = connection.execute(
                "SELECT event_json FROM outbox WHERE state='pending' AND next_attempt_at<=? ORDER BY created_at,event_id LIMIT ?",
                (now, limit),
            ).fetchall()
        return [json.loads(row["event_json"]) for row in rows]

    def mark_synced(self, event_ids, synced_at=None):
        if not event_ids:
            return
        synced_at = synced_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
        marks = ",".join("?" for _ in event_ids)
        with self.connection() as connection:
            connection.execute(
                f"UPDATE outbox SET state='synced', synced_at=?, last_error=NULL WHERE event_id IN ({marks})",
                [synced_at, *event_ids],
            )

    def mark_failed(self, event_ids, error, now=None):
        if not event_ids:
            return
        now = time.time() if now is None else now
        with self.connection() as connection:
            for event_id in event_ids:
                row = connection.execute("SELECT attempts FROM outbox WHERE event_id=?", (event_id,)).fetchone()
                if row is None:
                    continue
                attempts = row["attempts"] + 1
                delay = min(self.base_delay_seconds * (2 ** (attempts - 1)), self.max_delay_seconds)
                state = "dead" if attempts >= self.max_attempts else "pending"
                next_attempt_at = now + delay if state == "pending" else now
                connection.execute(
                    "UPDATE outbox SET attempts=?,state=?,next_attempt_at=?,last_error=? WHERE event_id=?",
                    (attempts, state, next_attempt_at, str(error)[:500], event_id),
                )

    def counts(self):
        result = {"pending": 0, "synced": 0, "dead": 0, "total": 0}
        with self.connection() as connection:
            rows = connection.execute("SELECT state,COUNT(*) AS n FROM outbox GROUP BY state").fetchall()
        for row in rows:
            result[row["state"]] = row["n"]
            result["total"] += row["n"]
        return result

    def list_events(self, limit=100):
        with self.connection() as connection:
            rows = connection.execute(
                "SELECT event_id,event_json,state,attempts,last_error,created_at,synced_at FROM outbox ORDER BY created_at DESC,event_id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [
            {
                "event_id": row["event_id"],
                "site_code": json.loads(row["event_json"])["site_code"],
                "event_type": json.loads(row["event_json"])["event_type"],
                "created_at": row["created_at"],
                "state": row["state"],
                "attempts": row["attempts"],
                "last_error": row["last_error"],
                "synced_at": row["synced_at"],
            }
            for row in rows
        ]
