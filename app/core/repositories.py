from app.retrieval.repository import InMemoryVectorRepo
from app.core.logging import get_logger

logger = get_logger(__name__)
# Single shared instance of vector store (monolithic safe)
global_vector_repo = InMemoryVectorRepo()
logger.info(
    "Initialized global InMemoryVectorRepo (shared across ingestion & retrieval)"
)
