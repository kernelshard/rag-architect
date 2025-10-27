import pytest

from app.core.constants import IngestionStatus
from app.ingestion.models import IngestRequest
from app.ingestion.repository import InMemoryEmbeddingRepo
from app.ingestion.service import ingest_document


@pytest.mark.asyncio
async def test_ingest_document_saves_to_repo():
    # deps
    repo = InMemoryEmbeddingRepo()
    req = IngestRequest(doc_id="doc-01", text="Hello, Welcome to the RAG world?")

    # ops
    resp = await ingest_document(req, repo)

    # assert
    assert resp.status == IngestionStatus.Accepted
    assert resp.doc_id == "doc-01"
    assert "doc-01" in repo.store
    saved = repo.store["doc-01"]
    assert isinstance(saved["vectors"], list)
    assert "metadata" in saved
