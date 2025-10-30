import asyncio

from app.core.interfaces import BaseEmbeddingRepository
from app.core.constants import IngestionStatus
from app.ingestion.models import IngestResponse, IngestRequest

EMBED_DIM = 5  # tiny for tests


async def ingest_document(
    request: IngestRequest, repo: BaseEmbeddingRepository
) -> IngestResponse:
    """
    Orchestrate ingestion of a single document.

    Args:
        request:  validated ingestion request containing text, doc_id etc.
        repo: an implementation of BaseEmbeddingRepository

    Returns:
        IngestResponse summarizing the accepted document
    """
    # Simulate embedding generation
    await asyncio.sleep(0)

    vectors = _mock_embedding(text=request.text)

    # Persist embeddings vua repo
    await repo.store_embedding(
        doc_id=request.doc_id, vectors=vectors, metadata=request.metadata or {}
    )

    return IngestResponse(
        doc_id=request.doc_id,
        status=IngestionStatus.Accepted,
        message="Document accepted for ingestion.",
    )


def _mock_embedding(text: str) -> list[float]:
    """
    Temporary solution for real embedding model call
    """
    base_val = float(sum(ord(c) for c in text) % 100) / 100.0
    return [base_val for _ in range(EMBED_DIM)]
