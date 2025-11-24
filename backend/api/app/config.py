"""Application configuration management using Pydantic BaseSettings.

This module provides centralized configuration handling for the FastAPI application,
loading values from environment variables with sensible defaults.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        APP_NAME: The name of the application.
        APP_VERSION: The version of the application.
        OPENAI_API_KEY: Optional OpenAI API key for LLM integration.
        ANTHROPIC_API_KEY: Optional Anthropic API key for LLM integration.
        LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        ENV: Deployment environment (development, staging, production).
    """

    APP_NAME: str = "Ona Backend API"
    APP_VERSION: str = "0.1.0"
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    ENV: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def load_settings() -> Settings:
    """Load and cache application settings.

    Returns:
        Settings: Cached application settings instance.
    """
    return Settings()

