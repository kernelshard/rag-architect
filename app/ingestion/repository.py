from typing import Any

from app.core.interfaces import BaseEmbeddingRepository


class InMemoryEmbeddingRepo(BaseEmbeddingRepository):
    def __init__(self) -> None:
        self.store: dict[str, dict] = {}

    async def store_embedding(
        self, doc_id: str, vectors: list[float], metadata: dict[str, Any]
    ) -> None:
        self.store[doc_id] = {"vectors": vectors, "metadata": metadata}
