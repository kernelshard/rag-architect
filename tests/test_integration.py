import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_ingestion_and_retrieval_flow():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Ingest a document
        ingest_payload = {"doc_id": "doc_1", "text": "Hello world"}
        resp_ingest = await client.post("/api/v1/ingestion/ingest", json=ingest_payload)
        assert resp_ingest.status_code == 200
        assert resp_ingest.json()["status"] == "accepted"

        # Retrieve the document
        query_payload = {"query": "hello"}
        resp_retrieve = await client.post("/api/v1/retrieval/query", json=query_payload)

        assert resp_retrieve.status_code == 200
        data = resp_retrieve.json()
        assert data["results"], "retrieval returned empty results"
        assert data["results"][0]["score"] > 0 <= 1


@pytest.mark.asyncio
async def test_metrics_endpoint_increments():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Hit the ping endpoint to generate some metrics
        await client.get("/api/v1/ping")

        resp = await client.get("/metrics")
        assert resp.status_code == 200

        metrics_text = resp.text
        assert "app_requests_total" in metrics_text
        assert 'method="GET"' in metrics_text
        assert 'endpoint="/api/v1/ping"' in metrics_text
