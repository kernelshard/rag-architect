"""
Retrieval Service

Responsible for:
1. Converting user queries into embedding vectors.
2. Searching the vector store for nearest neighbors.
3. Returning ranked result.

Design principle:
- Framework-agnostic
- Dependency-injected repositories
- Async-first approach
- Logs and observability ready

TODO:
Later versions will apply hybrid retrival concept
and cross encoder reranking - this is base retrieval layer

"""

import asyncio

from app.core.interfaces import BaseVectorSearchRepository
from app.core.logging import get_logger
from app.retrieval.models import RetrievedChunk, RetrievalResponse, RetrievalRequest

logger = get_logger(__name__)


async def retrieve_documents(
    request: RetrievalRequest,
    repo: BaseVectorSearchRepository,
) -> RetrievalResponse:
    """
    Orchestrate retrieval flow:
    1. Embed the query.
    2. Search the vector store for nearest neighbors.
    3. Return ranked chunks

    Args:
        request: validated RetrievalRequest with query text and top_k
        repo: injected repository implementing BaseVectorSearchRepository
        include_metadata: whether to include metadata in results

    Returns:
        RetrievalResponse with top_k ranked result chunks
    """
    # Step 1: Embed the query (mocked async placeholder)
    await asyncio.sleep(0)
    query_vector = _mock_embedding(request.query)

    logger.info(f"Retrieving for query: '{request.query}' | top_k={request.top_k}")

    # Step 2: Query the vector store for nearest embeddings
    search_results = await repo.query(
        query_vector=query_vector,
        top_k=request.top_k,
        filters=request.filters,
        include_metadata=request.include_metadata,
    )

    # Step 3: Process and rank results
    ranked_chunks = []
    for result in search_results:
        chunk = RetrievedChunk(
            doc_id=result.id,
            score=_normalize_score(result.score),
            metadata=result.metadata,
        )
        ranked_chunks.append(chunk)

        logger.info(
            f"Retrieved {len(ranked_chunks)}  results for query = '{request.query}'"
        )

    resp = RetrievalResponse(
        query=request.query,
        results=ranked_chunks,
    )
    return resp


def _mock_embedding(text: str) -> list[float]:
    """
    Placeholder for a real embedding model call
    base_val = float(sum(ord(c) for c in text) % 100) / 100.0

    Note: Don't focus on logic just a deterministic output for testing
    """
    # example:
    # text = "abc"
    # ASCII values: a=97, b=98, c=99
    # total = 97+98+99 = 294
    # 294 % 100 = 94
    # 94 / 100.0 = 0.94
    total = 0
    for c in text:
        total += ord(c)

    mod100 = total % 100
    base_value = mod100 / 100.0
    embedding = [base_value] * 8
    return embedding


def _normalize_score(score: float) -> float:
    """
    Ensure score is between 0.0 and 1.0 for UI
    """
    # Simple and predictable for testing.
    return max(0.0, min(round(score, 3), 1.0))
