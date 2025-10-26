from fastapi.testclient import TestClient

from app.main import app


def test_metrics_exposure():
    client = TestClient(app)
    response = client.get("/metrics")
    assert response.status_code == 200

    # Prometheus metrics endpoint returns text format
    content = response.text

    assert "app_requests_total " in content
    assert (
        "HELP" in content
    )  # Prometheus help text e.g. "HELP app_requests_total Total number of requests"
    assert "TYPE" in content  # Prometheus type text e.g counter, gauge
