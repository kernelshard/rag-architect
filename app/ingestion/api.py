from fastapi import APIRouter, Depends

from app.core.interfaces import BaseEmbeddingRepository
from app.ingestion.models import IngestResponse, IngestRequest
from .deps import get_embedding_repo
from .service import ingest_document

router = APIRouter(prefix="/api/v1/ingestion", tags=["ingestion"])


@router.post(
    "/ingest", response_model=IngestResponse, summary="Submit doc to Ingestion"
)
async def ingest_doc(
    request: IngestRequest,
    embedding_repo: BaseEmbeddingRepository = Depends(get_embedding_repo),
) -> IngestResponse:
    """Submit doc to Ingestion"""
    return await ingest_document(request, repo=embedding_repo)
