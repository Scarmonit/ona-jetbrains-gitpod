"""
LLM integration module for the FastAPI backend.

Provides real OpenAI and Anthropic API integration with fallback to stub mode.
Provider selection order: OpenAI (if key set) > Anthropic (if key set) > Stub.
"""

from __future__ import annotations

import hashlib
import logging
from typing import TYPE_CHECKING, Optional

import httpx
from pydantic import BaseModel, Field

from .config import get_settings

if TYPE_CHECKING:
    from .config import Settings

logger = logging.getLogger(__name__)


class LLMRequest(BaseModel):
    """Request model for LLM completion.

    Attributes:
        prompt: The input prompt for the LLM (max 4000 chars by default).
    """

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Input prompt for the LLM",
    )


class LLMResponse(BaseModel):
    """Response model for LLM completion.

    Attributes:
        provider: The LLM provider used (openai, anthropic, or stub).
        model: The specific model used for completion.
        output: The generated text output.
        stub: Whether this is a stub response (no real LLM call).
        error: Error message if the call failed, None otherwise.
    """

    provider: str = Field(..., description="LLM provider used")
    model: str = Field(..., description="Model used for completion")
    output: str = Field(..., description="Generated text output")
    stub: bool = Field(..., description="Whether this is a stub response")
    error: Optional[str] = Field(None, description="Error message if call failed")


def _get_prompt_hash_prefix(prompt: str) -> str:
    """Get SHA256 hash prefix of prompt for secure logging.

    Args:
        prompt: The prompt text.

    Returns:
        First 8 characters of SHA256 hash.
    """
    return hashlib.sha256(prompt.encode()).hexdigest()[:8]


async def _call_openai(prompt: str, settings: "Settings | None" = None) -> LLMResponse:
    """Call OpenAI Chat Completions API.

    Args:
        prompt: The input prompt.
        settings: Optional settings override.

    Returns:
        LLMResponse with the completion result.
    """
    if settings is None:
        settings = get_settings()

    logger.debug(
        "OpenAI request - prompt_length=%d, hash_prefix=%s",
        len(prompt),
        _get_prompt_hash_prefix(prompt),
    )

    try:
        async with httpx.AsyncClient(timeout=settings.llm_timeout) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.openai_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1024,
                },
            )

            if response.status_code != 200:
                error_text = response.text
                logger.error("OpenAI API error: %d - %s", response.status_code, error_text)
                return LLMResponse(
                    provider="openai",
                    model=settings.openai_model,
                    output="",
                    stub=False,
                    error=f"OpenAI API error: {response.status_code}",
                )

            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

            if not content:
                logger.warning("OpenAI returned empty response")
                return LLMResponse(
                    provider="openai",
                    model=settings.openai_model,
                    output="",
                    stub=False,
                    error="OpenAI returned empty response",
                )

            return LLMResponse(
                provider="openai",
                model=settings.openai_model,
                output=content,
                stub=False,
                error=None,
            )

    except httpx.TimeoutException:
        logger.error("OpenAI request timed out")
        return LLMResponse(
            provider="openai",
            model=settings.openai_model,
            output="",
            stub=False,
            error="Request timed out",
        )
    except httpx.RequestError as e:
        logger.error("OpenAI request failed: %s", str(e))
        return LLMResponse(
            provider="openai",
            model=settings.openai_model,
            output="",
            stub=False,
            error=f"Request failed: {str(e)}",
        )
    except (KeyError, IndexError, TypeError) as e:
        logger.error("Failed to parse OpenAI response: %s", str(e))
        return LLMResponse(
            provider="openai",
            model=settings.openai_model,
            output="",
            stub=False,
            error="Failed to parse response",
        )


async def _call_anthropic(prompt: str, settings: "Settings | None" = None) -> LLMResponse:
    """Call Anthropic Messages API.

    Args:
        prompt: The input prompt.
        settings: Optional settings override.

    Returns:
        LLMResponse with the completion result.
    """
    if settings is None:
        settings = get_settings()

    logger.debug(
        "Anthropic request - prompt_length=%d, hash_prefix=%s",
        len(prompt),
        _get_prompt_hash_prefix(prompt),
    )

    try:
        async with httpx.AsyncClient(timeout=settings.llm_timeout) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.anthropic_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1024,
                },
            )

            if response.status_code != 200:
                error_text = response.text
                logger.error("Anthropic API error: %d - %s", response.status_code, error_text)
                return LLMResponse(
                    provider="anthropic",
                    model=settings.anthropic_model,
                    output="",
                    stub=False,
                    error=f"Anthropic API error: {response.status_code}",
                )

            data = response.json()
            content_blocks = data.get("content", [])
            content = ""
            for block in content_blocks:
                if block.get("type") == "text":
                    content = block.get("text", "")
                    break

            if not content:
                logger.warning("Anthropic returned empty response")
                return LLMResponse(
                    provider="anthropic",
                    model=settings.anthropic_model,
                    output="",
                    stub=False,
                    error="Anthropic returned empty response",
                )

            return LLMResponse(
                provider="anthropic",
                model=settings.anthropic_model,
                output=content,
                stub=False,
                error=None,
            )

    except httpx.TimeoutException:
        logger.error("Anthropic request timed out")
        return LLMResponse(
            provider="anthropic",
            model=settings.anthropic_model,
            output="",
            stub=False,
            error="Request timed out",
        )
    except httpx.RequestError as e:
        logger.error("Anthropic request failed: %s", str(e))
        return LLMResponse(
            provider="anthropic",
            model=settings.anthropic_model,
            output="",
            stub=False,
            error=f"Request failed: {str(e)}",
        )
    except (KeyError, IndexError, TypeError) as e:
        logger.error("Failed to parse Anthropic response: %s", str(e))
        return LLMResponse(
            provider="anthropic",
            model=settings.anthropic_model,
            output="",
            stub=False,
            error="Failed to parse response",
        )


def _create_stub_response() -> LLMResponse:
    """Create a stub response when no LLM provider is configured.

    Returns:
        LLMResponse with stub information.
    """
    return LLMResponse(
        provider="stub",
        model="none",
        output="Stub response. Set OPENAI_API_KEY or ANTHROPIC_API_KEY for real LLM calls.",
        stub=True,
        error=None,
    )


async def complete(request: LLMRequest) -> LLMResponse:
    """Process an LLM completion request.

    Provider selection order:
    1. OpenAI (if OPENAI_API_KEY is set)
    2. Anthropic (if ANTHROPIC_API_KEY is set)
    3. Stub (fallback when no keys are configured)

    Args:
        request: The LLM completion request.

    Returns:
        LLMResponse with the completion result.
    """
    settings = get_settings()
    prompt = request.prompt

    # Provider selection order: OpenAI > Anthropic > Stub
    if settings.openai_api_key:
        logger.info("Using OpenAI provider")
        return await _call_openai(prompt, settings)

    if settings.anthropic_api_key:
        logger.info("Using Anthropic provider")
        return await _call_anthropic(prompt, settings)

    logger.info("No LLM provider configured, returning stub response")
    return _create_stub_response()
