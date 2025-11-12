from enum import StrEnum


# Ingestion status constants used across the application
class IngestionStatus(StrEnum):
    Accepted = "accepted"
    Processing = "processing"
    Completed = "completed"
    Failed = "failed"


DefaultTopK: int = 5


class GeneratorBackend(StrEnum):
    """
    Supported generator backends.
    Reason: to avoid hardcoding strings across the codebase.
    """

    Mock = "mock"
    OPENAI = "openai"
    Ollama = "ollama"
