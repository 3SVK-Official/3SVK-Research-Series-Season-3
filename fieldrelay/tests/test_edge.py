import requests
from fastapi.testclient import TestClient

from fieldrelay.cloud import create_app as create_cloud_app
from fieldrelay.edge import create_app as create_edge_app
from fieldrelay.store import EventStore

SECRET = "integration-test-key-44a0"


def test_offline_capture_and_later_sync(monkeypatch, tmp_path):
    cloud_client = TestClient(create_cloud_app(tmp_path / "cloud.db", SECRET))

    class ResponseAdapter:
        def __init__(self, response):
            self.response = response

        def raise_for_status(self):
            if not self.response.is_success:
                raise requests.HTTPError(str(self.response.status_code))

        def json(self):
            return self.response.json()

    def fake_post(url, data, headers, timeout):
        response = cloud_client.post("/v1/events/batch", content=data, headers=headers)
        return ResponseAdapter(response)

    monkeypatch.setattr("fieldrelay.edge.requests.post", fake_post)
    app = create_edge_app(EventStore(tmp_path / "edge.db"), "http://cloud", SECRET)
    client = TestClient(app)
    event_response = client.post(
        "/api/events",
        json={
            "site_code": "SITE-09",
            "event_type": "supply_update",
            "item": "Drinking water",
            "status": "Low",
            "quantity": 4,
            "note": "Restock requested",
        },
    )
    assert event_response.status_code == 200
    event_id = event_response.json()["event_id"]
    assert client.post("/api/link-state", json={"available": False}).json()["available"] is False
    offline_sync = client.post("/api/sync")
    assert offline_sync.status_code == 409
    assert app.state.store.counts()["pending"] == 1
    assert client.post("/api/link-state", json={"available": True}).json()["available"] is True
    sync_response = client.post("/api/sync")
    assert sync_response.status_code == 200
    assert sync_response.json()["synced"] == 1
    assert app.state.store.counts()["synced"] == 1
    assert cloud_client.get("/v1/stats").json()["stored_events"] == 1
    assert cloud_client.get("/v1/events").json()[0]["event_id"] == event_id
