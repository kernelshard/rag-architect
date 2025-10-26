from abc import ABC, abstractmethod
from typing import Any, TypedDict


class SearchResult(TypedDict, total=False):
    """Represents a single search hit result from vector store."""

    id: str
    score: float
    text: str
    metadata: dict[str, Any]


class BaseEmbeddingRepository(ABC):
    """Defines the storage contract for document embeddings."""

    @abstractmethod
    async def store_embedding(
        self,
        doc_id: str,
        vectors: list[float],
        metadata: dict[str, Any],
    ) -> None:
        """Persist an embedding vector and associated metadata.

        Args:
            doc_id: The unique id of the document.
            vectors: The embedding values, as a list of floats.
            metadata: The extra infos embedding(e.g. source, title, timestamp etc.).
        """
        ...


class BaseVectorSearchRepository(ABC):
    """
    Defines the retrieval contract for document vector search.
    """

    @abstractmethod
    async def query(
        self,
        query_vector: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
        include_metadata: bool = True,
    ) -> list[SearchResult]:
        """
        Search the vector store for most similar documents.

        Args:
            query_vector: The embedding vector
            top_k: The number of most similar documents to return.
            filters: Optional filters to apply to the query. (e.g. -
            include_metadata: Whether to include metadata in the query.
        """
        ...
