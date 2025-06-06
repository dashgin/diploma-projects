"""
Configuration settings for the AI Feedback Service.
"""

from typing import Annotated, Any

from pydantic import (
    AnyUrl,
    BeforeValidator,
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """Settings for the AI service."""

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Feedback Service"

    # Model paths
    ERROR_CLASSIFIER_MODEL_PATH: str = Field(
        default="/app/app/models/error_classifier",
        description="Path to the error classifier model",
    )

    # Model configurations
    SEMANTIC_MODEL_NAME: str = Field(
        default="all-MiniLM-L6-v2",
        description="Name of the sentence transformer model to use",
    )
    FALLBACK_MODEL_NAME: str = Field(
        default="distilbert-base-uncased",
        description="Fallback model to use if no custom model is found",
    )

    # Similarity threshold
    SIMILARITY_THRESHOLD: float = Field(
        default=0.5,
        description="Threshold for determining general understanding based on semantic similarity",
    )

    # Logging
    LOG_LEVEL: str = Field(
        default="INFO", description="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )

    # CORS settings
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()  # type: ignore
