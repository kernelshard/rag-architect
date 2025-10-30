from pydantic import BaseModel, Field

from typing import Any

from app.core.constants import IngestionStatus


class IngestRequest(BaseModel):
    """Payload for document ingestion request"""

    doc_id: str = Field(..., description="Unique identifier for the document.")
    text: str = Field(
        ..., description="Raw text content of the document to be embedded."
    )
    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Optional metadata such as source, author, tag etc.",
    )
    model_config = {
        "json_schema_extra": {
            "example": {
                "doc_id": "doc-123",
                "text": "Hey Sam is building the best RAG pipeline!",
                "metadata": {"author": "Sam", "tags": ["RAG"]},
            }
        }
    }


class IngestResponse(BaseModel):
    """
    Acknowledgement returned after ingestion request is complete.
    """

    doc_id: str = Field(..., description="ID of the ingested document")
    status: str = Field(
        default=IngestionStatus.Accepted, description="Ingestion status"
    )
    message: str = Field(..., description="Ingestion message")

    model_config = {
        "json_schema_extra": {
            "example": {
                "doc_id": "doc-123",
                "status": f"{IngestionStatus.Accepted}",
                "message": "Document has been received.!",
            },
        }
    }
