from app.core.interfaces import BaseEmbeddingRepository
from .repository import InMemoryEmbeddingRepo

_repo = InMemoryEmbeddingRepo()


def get_embedding_repo() -> BaseEmbeddingRepository:
    # TODO: Later we will create/init Qdrant client here
    return _repo
