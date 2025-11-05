import asyncio
from typing import Any
from app.core.constants import DefaultTopK
from app.core.interfaces import (
    BaseVectorSearchRepository,
    SearchResult,
    BaseEmbeddingRepository,
)
from app.core.logging import get_logger


logger = get_logger(__name__)


class InMemoryVectorRepo(BaseVectorSearchRepository, BaseEmbeddingRepository):
    """
    In-memory mock of a vector search repository for testing purposes.

    Each entry is stored as:
    {
        "id": str,
        "vector": list[float],
        "metadata": dict[str, Any]
    }

    Retrieval is done via cosine similarity.
    """

    def __init__(self) -> None:
        self._store: list[dict[str, Any]] = []

    async def store_embedding(
        self, doc_id: str, vector: list[float], metadata: dict[str, Any] | None = None
    ) -> None:
        """Store an embedding to memory (used by ingestion for test chaining)."""
        metadata = metadata or {}
        entry = {"id": doc_id, "vector": vector, "metadata": metadata}
        self._store.append(entry)
        logger.info(f"Store repo id={id(self)} total_after_store={len(self._store)}")

        logger.debug(f"Stored embedding for: id={doc_id} dim={len(vector)}")

    async def query(
        self,
        query_vector: list[float],
        top_k: int = DefaultTopK,
        filters: dict[str, Any] | None = None,
        include_metadata: bool = True,
    ) -> list[SearchResult]:
        """Returns tpp_k nearest neighbors based on cosine similarity."""
        await asyncio.sleep(0)  # Simulate async operation

        # Step 1 - Optional metadata filtering
        candidates: list[dict[str, Any]] = []
        for v in self._store:
            # exclude non-matching metadata
            if filters:
                filter_matched = _matches_filter(v["metadata"], filters)
                if not filter_matched:
                    continue
            candidates.append(v)

        if not candidates:
            logger.info("No candidates found for query.")

        # Step 2 - Compute cosine similarity scores
        scored_candidates: list[SearchResult] = []
        for c in candidates:
            similarity_score = _cosine_similarity(query_vector, c["vector"])
            result = SearchResult(
                id=c["id"],
                score=similarity_score,
                metadata=c["metadata"] if include_metadata else None,
            )
            scored_candidates.append(result)

        # Step 3 - Sort by score and return top_k
        scored_candidates.sort(key=lambda x: x.score, reverse=True)
        results = scored_candidates[:top_k]
        logger.debug(f"Query returned {len(results)} hits for top_k={top_k}")
        return results


def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two equal-length vectors.
    returns a value between 0.0 and 1.0
    """
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _matches_filter(metadata: dict[str, Any], filters: dict[str, Any]) -> bool:
    """
    Simple key-value match filter using for metadata narrowing.
    """
    for key, value in filters.items():
        if key not in metadata or metadata[key] != value:
            return False
    return True
