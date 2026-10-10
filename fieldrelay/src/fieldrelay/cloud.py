import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from fieldrelay.security import digest, verify_signature


class EventRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: str = Field(min_length=36, max_length=36)
    site_code: str = Field(min_length=2, max_length=24, pattern=r"^[A-Za-z0-9_-]+$")
    event_type: str = Field(min_length=2, max_length=40)
    created_at: str = Field(min_length=10, max_length=40)
    payload: dict[str, Any]
    event_sha256: str = Field(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$")

    def core(self):
        return {
            "event_id": self.event_id,
            "site_code": self.site_code,
            "event_type": self.event_type,
            "created_at": self.created_at,
            "payload": self.payload,
        }


class BatchRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    events: list[EventRecord] = Field(min_length=1, max_length=100)


def create_app(db_path=None, secret=None):
    app = FastAPI(title="FieldRelay Cloud Ingest", version="1.0.0")
    app.state.db_path = str(db_path or os.getenv("FIELDRELAY_CLOUD_DB", "data/cloud.db"))
    app.state.secret = secret if secret is not None else os.getenv("FIELDRELAY_SHARED_SECRET", "")
    Path(app.state.db_path).parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connection():
        connection = sqlite3.connect(app.state.db_path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    with connection() as db:
        db.execute("PRAGMA journal_mode=WAL")
        db.execute(
            """CREATE TABLE IF NOT EXISTS received_events (
                event_id TEXT PRIMARY KEY,
                site_code TEXT NOT NULL,
                event_type TEXT NOT NULL,
                created_at TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                event_sha256 TEXT NOT NULL,
                received_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )

    @app.get("/health")
    def health():
        return {"ok": True, "service": "fieldrelay-cloud", "auth_configured": bool(app.state.secret)}

    @app.get("/v1/stats")
    def stats():
        with connection() as db:
            count = db.execute("SELECT COUNT(*) FROM received_events").fetchone()[0]
            sites = db.execute("SELECT COUNT(DISTINCT site_code) FROM received_events").fetchone()[0]
        return {"stored_events": count, "sites": sites}

    @app.get("/v1/events")
    def events(limit: int = 50):
        if limit < 1 or limit > 200:
            raise HTTPException(status_code=422, detail="limit must be between 1 and 200")
        with connection() as db:
            rows = db.execute(
                "SELECT event_id,site_code,event_type,created_at,payload_json,event_sha256,received_at FROM received_events ORDER BY received_at DESC,event_id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [
            {
                "event_id": row["event_id"],
                "site_code": row["site_code"],
                "event_type": row["event_type"],
                "created_at": row["created_at"],
                "payload": json.loads(row["payload_json"]),
                "event_sha256": row["event_sha256"],
                "received_at": row["received_at"],
            }
            for row in rows
        ]

    @app.post("/v1/events/batch")
    async def ingest(request: Request):
        body = await request.body()
        signature = request.headers.get("X-FieldRelay-Signature", "")
        if not app.state.secret:
            raise HTTPException(status_code=503, detail="Shared secret is not configured")
        if not verify_signature(app.state.secret, body, signature):
            raise HTTPException(status_code=401, detail="Invalid batch signature")
        try:
            batch = BatchRecord.model_validate_json(body)
        except ValidationError as exc:
            raise HTTPException(status_code=422, detail=exc.errors(include_input=False)) from exc
        events = [event.model_dump() for event in batch.events]
        for event in batch.events:
            if digest(event.core()) != event.event_sha256:
                raise HTTPException(status_code=422, detail=f"Integrity check failed for event {event.event_id}")
        ids = [event.event_id for event in batch.events]
        if len(ids) != len(set(ids)):
            raise HTTPException(status_code=422, detail="A batch cannot contain duplicate event IDs")
        accepted = []
        duplicates = []
        with connection() as db:
            for event in events:
                existing = db.execute(
                    "SELECT event_sha256 FROM received_events WHERE event_id=?", (event["event_id"],)
                ).fetchone()
                if existing and existing["event_sha256"] != event["event_sha256"]:
                    raise HTTPException(status_code=409, detail=f"Event ID collision: {event['event_id']}")
            for event in events:
                existing = db.execute(
                    "SELECT event_sha256 FROM received_events WHERE event_id=?", (event["event_id"],)
                ).fetchone()
                if existing:
                    duplicates.append(event["event_id"])
                else:
                    db.execute(
                        "INSERT INTO received_events(event_id,site_code,event_type,created_at,payload_json,event_sha256) VALUES(?,?,?,?,?,?)",
                        (
                            event["event_id"], event["site_code"], event["event_type"], event["created_at"],
                            json.dumps(event["payload"], ensure_ascii=False, sort_keys=True), event["event_sha256"],
                        ),
                    )
                    accepted.append(event["event_id"])
        return {"accepted": accepted, "duplicates": duplicates, "stored": len(accepted)}

    return app


app = create_app()
