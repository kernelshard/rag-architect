# tests/retrieval/test_api.py (snippet)
from fastapi.testclient import TestClient
from app.main import app  # your FastAPI app
from app.retrieval.deps import get_vector_repo
from app.retrieval.repository import InMemoryVectorRepo

test_repo = InMemoryVectorRepo()
# populate test_repo with deterministic vectors / metadata if needed

# override dependency to use the test repo
app.dependency_overrides[get_vector_repo] = lambda: test_repo

client = TestClient(app)


def test_query_returns_200_and_expected_schema():
    payload = {"query": "hello world", "top_k": 3}
    resp = client.post("/api/v1/retrieval/query", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["query"] == payload["query"]
    assert isinstance(body["results"], list)
