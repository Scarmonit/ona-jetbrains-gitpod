"""Pydantic models for API request and response validation.

This module defines the data models used across the API endpoints,
ensuring type safety and automatic validation of request/response data.
"""

from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response model for the health check endpoint.

    Attributes:
        status: Current health status of the service (e.g., "ok").
        uptime_seconds: Time in seconds since the application started.
    """

    status: str = Field(..., description="Health status of the service")
    uptime_seconds: float = Field(
        ..., description="Time in seconds since application start"
    )


class InfoResponse(BaseModel):
    """Response model for the application info endpoint.

    Attributes:
        app: The name of the application.
        version: The current version of the application.
        env: The deployment environment (development, staging, production).
    """

    app: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")
    env: str = Field(..., description="Deployment environment")


class LLMRequest(BaseModel):
    """Request model for the LLM proxy endpoint.

    Attributes:
        prompt: The user prompt to send to the LLM.
        model: Optional model identifier (e.g., "gpt-4", "claude-3").
    """

    prompt: str = Field(..., description="The prompt to send to the LLM")
    model: Optional[str] = Field(
        default=None, description="Optional model identifier"
    )


class LLMResponse(BaseModel):
    """Response model for the LLM proxy endpoint.

    Attributes:
        provider: The LLM provider (e.g., "openai", "anthropic", "stub").
        model: The model used for generation.
        output: The generated output or stub message.
        stub: Indicates if this is a stub response (no real LLM call made).
        error: Optional error message if the request failed.
    """

    provider: str = Field(..., description="LLM provider name")
    model: str = Field(..., description="Model identifier used")
    output: str = Field(..., description="Generated output or stub message")
    stub: bool = Field(..., description="Whether this is a stub response")
    error: Optional[str] = Field(
        default=None, description="Error message if request failed"
    )
