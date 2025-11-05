from app.core.interfaces import BaseEmbeddingRepository
from app.core.repositories import global_vector_repo


async def get_embedding_repo() -> BaseEmbeddingRepository:
    """
    Shared vector repository dependency for ingestion.
    """
    return global_vector_repo
