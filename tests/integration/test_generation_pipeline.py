import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

pytestmark = pytest.mark.asyncio


async def test_generation_pipeline_e2e():
    """
    End-to-end test for the generation pipeline.
    - Ingest a document.
    - Retrieve it via query.
    - Generate an answer based on the retrieved document/context.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Ingest a document
        ingest_payload = {
            "doc_id": "doc_1",
            "text": "Most suitable programming language for RAG is Python.",
        }
        resp_ingest = await client.post("/api/v1/ingestion/ingest", json=ingest_payload)
        assert resp_ingest.status_code == 200
        assert resp_ingest.json()["status"] == "accepted"

        # Retrieve the documents
        query_payload = {
            "query": "What is the most suitable programming language for RAG?"
        }
        resp_retrieval = await client.post(
            "/api/v1/retrieval/query", json=query_payload
        )

        assert resp_retrieval.status_code == 200
        retrieved_data = resp_retrieval.json()
        assert len(retrieved_data["results"]) > 0, "retrieval returned empty results"
        assert retrieved_data["results"][0]["doc_id"] == "doc_1"

        # Generate answer
        generation_payload = {
            "query": "What is the most suitable programming language for RAG?",
            "context_size": 3,
        }

        resp_generation = await client.post(
            "/api/v1/generation/generate", json=generation_payload
        )
        assert resp_generation.status_code == 200
        generation_data = resp_generation.json()

        # validate coherence between retrieved context and generated answer
        assert generation_data["query"] == generation_payload["query"]
        assert "Mock answer" in generation_data["answer"]["text"]
        assert len(generation_data["answer"]["used_contexts"]) > 0, (
            "No contexts used in generation"
        )
