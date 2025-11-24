"""
Configuration module for the FastAPI backend.

Loads environment variables and provides typed configuration.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        app_name: Name of the application.
        app_version: Version of the application.
        debug: Enable debug mode.
        py_env: Python environment (development, production).
        py_log_level: Logging level (DEBUG, INFO, WARNING, ERROR).
        openai_api_key: OpenAI API key for LLM integration.
        anthropic_api_key: Anthropic API key for LLM integration.
        openai_model: OpenAI model to use for completions.
        anthropic_model: Anthropic model to use for completions.
        llm_timeout: Timeout in seconds for LLM API calls.
        max_prompt_length: Maximum allowed prompt length in characters.
    """

    app_name: str = "Ona FastAPI Backend"
    app_version: str = "1.0.0"
    debug: bool = False
    py_env: str = "development"
    py_log_level: str = "INFO"

    # LLM Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    anthropic_model: str = "claude-3-5-sonnet-latest"
    llm_timeout: float = 30.0
    max_prompt_length: int = 4000

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings.

    Returns:
        Settings instance with loaded configuration.
    """
    return Settings()
