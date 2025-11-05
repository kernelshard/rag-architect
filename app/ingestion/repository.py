from typing import Any

from app.core.interfaces import BaseEmbeddingRepository


class InMemoryEmbeddingRepo(BaseEmbeddingRepository):
    def __init__(self) -> None:
        self.store: dict[str, dict] = {}

    async def store_embedding(
        self, doc_id: str, vector: list[float], metadata: dict[str, Any]
    ) -> None:
        self.store[doc_id] = {"vector": vector, "metadata": metadata}
