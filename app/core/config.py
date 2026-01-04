from pydantic import Field
from pydantic_settings import BaseSettings

from app.core.constants import GeneratorBackend


class Settings(BaseSettings):
    APP_NAME: str = "rag_mastery"
    ENV: str = Field(default="development", alias="ENV")
    DEBUG: bool = Field(default=True, alias="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", alias="LOG_LEVEL")
    HOST: str = Field(default="0.0.0.0", alias="HOST")
    PORT: int = Field(default=8000, alias="PORT")
    USE_REAL_GENERATOR: bool = False
    GENERATOR_BACKEND: GeneratorBackend = GeneratorBackend.Mock

    VECTOR_STORE: str = "memory"  # Options: "memory", "sqlite", "pinecone", etc.
    VECTOR_STORE_PATH: str = "var/vector_store.sqlite"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",  # ignore unknown env vars
        "populate_by_name": True,  # allowing alias mapping
        "use_enum_values": True,  # store enum values directly
    }


# Singleton settings instance
settings = Settings()
