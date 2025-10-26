from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ping_health_check():
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "ok"
    assert "uptime_seconds" in body
