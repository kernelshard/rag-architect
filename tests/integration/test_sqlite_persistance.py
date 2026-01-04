from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app

pytestmark = pytest.mark.asyncio


async def test_sqlite_persists_accross_restart(tmp_path, monkeypatch):
    from app.retrieval import deps

    deps._sqlite_vector_repo = None  # ← critical

    db = tmp_path / "vector_store.sqlite"
    monkeypatch.setenv("VECTOR_STORE", "sqlite")
    monkeypatch.setenv("VECTOR_STORE_PATH", str(db))

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Ingest a document
        await client.post(
            "/api/v1/ingestion/ingest",
            json={"doc_id": "d1", "text": "hello world"},
        )

    # new client simulates restart of app
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Retrieve the document
        resp = await client.post(
            "/api/v1/retrieval/query",
            json={"query": "hello"},
        )
        assert resp.status_code == 200
        assert resp.json()["results"][0]["doc_id"] == "d1"
