from typing import AsyncIterator

from app.core.interfaces import BaseVectorSearchRepository
from app.core.logging import get_logger
from app.core.repositories import global_vector_repo

logger = get_logger(__name__)


async def get_vector_repo() -> AsyncIterator[BaseVectorSearchRepository]:
    yield global_vector_repo
