from fastapi.testclient import TestClient

from app.main import app
from app.core.constants import IngestionStatus
from app.ingestion.repository import InMemoryEmbeddingRepo
from app.ingestion.deps import get_embedding_repo

client = TestClient(app)


def test_ingest_document_api():
    """Test the ingestion API endpoint."""
    # Override dependency to use a fresh repo instance for test isolation
    test_repo = InMemoryEmbeddingRepo()
    app.dependency_overrides[get_embedding_repo] = lambda: test_repo

    request_data = {
        "doc_id": "test-doc-01",
        "text": "This is a test document for ingestion.",
        "metadata": {"source": "test"},
    }

    response = client.post("/api/v1/ingestion/ingest", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert data["doc_id"] == "test-doc-01"
    assert data["status"] == IngestionStatus.Accepted
    assert "message" in data

    # Verify the document was stored in the repo
    assert "test-doc-01" in test_repo.store

    # Clean up override
    app.dependency_overrides.pop(get_embedding_repo, None)
