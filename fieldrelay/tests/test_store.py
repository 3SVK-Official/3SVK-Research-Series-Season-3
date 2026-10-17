import json

from fieldrelay.store import EventStore


def test_event_is_persisted_and_retrievable(tmp_path):
    path = tmp_path / "edge.db"
    store = EventStore(path)
    event = store.add_event("SITE-01", "supply_update", {"item": "water", "quantity": 12})
    reopened = EventStore(path)
    batch = reopened.ready_batch()
    assert len(batch) == 1
    assert batch[0]["event_id"] == event["event_id"]
    assert reopened.counts() == {"pending": 1, "synced": 0, "dead": 0, "total": 1}
    assert json.loads(json.dumps(batch[0]))["event_sha256"] == event["event_sha256"]


def test_retry_schedule_and_dead_letter(tmp_path):
    store = EventStore(tmp_path / "edge.db", max_attempts=2, base_delay_seconds=2, max_delay_seconds=10)
    event = store.add_event("SITE-02", "service_status", {"item": "power", "status": "Low"})
    store.mark_failed([event["event_id"]], "temporary outage", now=100)
    assert store.ready_batch(now=101) == []
    assert len(store.ready_batch(now=102)) == 1
    store.mark_failed([event["event_id"]], "still unavailable", now=102)
    assert store.counts() == {"pending": 0, "synced": 0, "dead": 1, "total": 1}
    assert store.list_events()[0]["last_error"] == "still unavailable"


def test_acknowledged_records_are_not_requeued(tmp_path):
    store = EventStore(tmp_path / "edge.db")
    event = store.add_event("SITE-03", "site_note", {"note": "Road access restored"})
    store.mark_synced([event["event_id"]])
    assert store.ready_batch() == []
    assert store.counts()["synced"] == 1
