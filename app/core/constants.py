from enum import StrEnum


class IngestionStatus(StrEnum):
    Accepted = "accepted"
    Processing = "processing"
    Completed = "completed"
    Failed = "failed"
