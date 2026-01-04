from typing import AsyncIterator

from app.core.config import settings
from app.core.interfaces import BaseVectorSearchRepository
from app.core.logging import get_logger
from app.core.repositories import global_vector_repo
from app.retrieval.repo_sqlite import SQLiteVectorRepo

logger = get_logger(__name__)

_sqlite_vector_repo: SQLiteVectorRepo | None = None


async def get_vector_repo() -> AsyncIterator[BaseVectorSearchRepository]:
    """
    Dependency injector for vector search repository based on configuration.
    Yields the appropriate repository instance based on the VECTOR_STORE setting.
    """
    # yield global_vector_repo
    global _sqlite_vector_repo

    if settings.VECTOR_STORE == "sqlite":
        if _sqlite_vector_repo is None:
            logger.info("Using SQLiteVectorRepo for vector storage")
            _sqlite_vector_repo = SQLiteVectorRepo(db_path=settings.VECTOR_STORE_PATH)
        yield _sqlite_vector_repo
    else:
        logger.info(
            f"Using InMemoryVectorRepo for vector storage (store has {len(global_vector_repo._store)} items)"
        )
        # Fallback to in-memory repo
        yield global_vector_repo
