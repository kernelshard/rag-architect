from fastapi import APIRouter

from app.core.constants import IngestionStatus
from app.ingestion.models import IngestResponse, IngestRequest

router = APIRouter(prefix="/api/v1/ingestion", tags=["ingestion"])


@router.post(
    "/ingest", response_model=IngestResponse, summary="Submit doc to Ingestion"
)
async def ingest_doc(request: IngestRequest) -> IngestResponse:
    # TODO: integrate service call here
    return IngestResponse(
        doc_id=request.doc_id,
        status=IngestionStatus.Accepted,
        message="Ingestion submitted",
    )
