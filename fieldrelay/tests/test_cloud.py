import copy

from fastapi.testclient import TestClient

from fieldrelay.cloud import create_app
from fieldrelay.security import canonical_json, digest, sign_body
from fieldrelay.store import EventStore

SECRET = "test-secret-89b4"


def submit(client, events, secret=SECRET, body=None, signature=None):
    body = body if body is not None else canonical_json({"events": events})
    signature = signature if signature is not None else sign_body(secret, body)
    return client.post(
        "/v1/events/batch",
        content=body,
        headers={"Content-Type": "application/json", "X-FieldRelay-Signature": signature},
    )


def test_accepts_event_and_replay_is_idempotent(tmp_path):
    app = create_app(tmp_path / "cloud.db", SECRET)
    client = TestClient(app)
    event = EventStore(tmp_path / "edge.db").add_event("SITE-01", "supply_update", {"item": "water", "quantity": 9})
    first = submit(client, [event])
    second = submit(client, [event])
    assert first.status_code == 200
    assert first.json()["accepted"] == [event["event_id"]]
    assert second.status_code == 200
    assert second.json()["duplicates"] == [event["event_id"]]
    assert client.get("/v1/stats").json()["stored_events"] == 1


def test_rejects_invalid_batch_signature(tmp_path):
    client = TestClient(create_app(tmp_path / "cloud.db", SECRET))
    event = EventStore(tmp_path / "edge.db").add_event("SITE-01", "site_note", {"note": "Road open"})
    body = canonical_json({"events": [event]})
    response = submit(client, [event], body=body, signature="0" * 64)
    assert response.status_code == 401


def test_rejects_payload_modified_after_event_was_created(tmp_path):
    client = TestClient(create_app(tmp_path / "cloud.db", SECRET))
    event = EventStore(tmp_path / "edge.db").add_event("SITE-01", "site_note", {"note": "Road open"})
    altered = copy.deepcopy(event)
    altered["payload"]["note"] = "Road closed"
    response = submit(client, [altered])
    assert response.status_code == 422
    assert client.get("/v1/stats").json()["stored_events"] == 0


def test_rejects_event_id_collision_without_overwriting_record(tmp_path):
    client = TestClient(create_app(tmp_path / "cloud.db", SECRET))
    store = EventStore(tmp_path / "edge.db")
    event = store.add_event("SITE-01", "site_note", {"note": "Road open"})
    assert submit(client, [event]).status_code == 200
    altered = copy.deepcopy(event)
    altered["payload"]["note"] = "Road closed"
    core = {key: altered[key] for key in ("event_id", "site_code", "event_type", "created_at", "payload")}
    altered["event_sha256"] = digest(core)
    response = submit(client, [altered])
    assert response.status_code == 409
    stored = client.get("/v1/events").json()
    assert len(stored) == 1
    assert stored[0]["payload"]["note"] == "Road open"
