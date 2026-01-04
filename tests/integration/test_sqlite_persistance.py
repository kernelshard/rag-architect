from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app
from app.ingestion import deps as ingestion_deps
from app.retrieval import deps as retrieval_deps
from app.retrieval.repo_sqlite import SQLiteVectorRepo

pytestmark = pytest.mark.asyncio


async def test_sqlite_persists_accross_restart(tmp_path):
    db = tmp_path / "vector_store.sqlite"
    repo = SQLiteVectorRepo(db_path=str(db))

    async def override_repo():
        yield repo

    app.dependency_overrides[ingestion_deps.get_embedding_repo] = override_repo
    app.dependency_overrides[retrieval_deps.get_vector_repo] = override_repo

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            await client.post(
                "/api/v1/ingestion/ingest",
                json={"doc_id": "d1", "text": "hello world"},
            )

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.post(
                "/api/v1/retrieval/query",
                json={"query": "hello"},
            )
            assert resp.status_code == 200
            assert resp.json()["results"][0]["doc_id"] == "d1"
    finally:
        app.dependency_overrides.clear()
