"""LLM processing module for handling LLM requests.

This module provides the logic for processing LLM requests, currently
serving as a placeholder with stub responses. It is designed for easy
extension when real OpenAI or Anthropic integrations are implemented.
"""

from app.config import Settings
from app.models import LLMRequest, LLMResponse


def process_prompt(settings: Settings, request: LLMRequest) -> LLMResponse:
    """Process an LLM prompt request and return a response.

    This function checks for available API keys and returns appropriate
    responses. Currently returns stub responses indicating the integration
    point for future real LLM API calls.

    Args:
        settings: Application settings containing API keys and configuration.
        request: The LLM request containing the prompt and optional model.

    Returns:
        LLMResponse: The response containing either a stub message or,
            in future implementations, the actual LLM output.

    Example:
        >>> settings = Settings()
        >>> request = LLMRequest(prompt="Hello, world!")
        >>> response = process_prompt(settings, request)
        >>> response.stub
        True
    """
    model = request.model or "default"

    # Check if OpenAI API key is configured
    if settings.OPENAI_API_KEY:
        # Placeholder for OpenAI integration
        # When implementing, add the actual API call here:
        # - Initialize OpenAI client with settings.OPENAI_API_KEY
        # - Make API call with request.prompt and request.model
        # - Return actual response with stub=False
        return LLMResponse(
            provider="openai",
            model=model,
            output=(
                "OpenAI API key is configured. This is a stub response. "
                "Replace this with actual OpenAI API integration. "
                "The integration point is in backend/api/app/llm.py"
            ),
            stub=True,
            error=None,
        )

    # Check if Anthropic API key is configured
    if settings.ANTHROPIC_API_KEY:
        # Placeholder for Anthropic integration
        # When implementing, add the actual API call here:
        # - Initialize Anthropic client with settings.ANTHROPIC_API_KEY
        # - Make API call with request.prompt and request.model
        # - Return actual response with stub=False
        return LLMResponse(
            provider="anthropic",
            model=model,
            output=(
                "Anthropic API key is configured. This is a stub response. "
                "Replace this with actual Anthropic API integration. "
                "The integration point is in backend/api/app/llm.py"
            ),
            stub=True,
            error=None,
        )

    # No API keys configured - return informative stub
    return LLMResponse(
        provider="stub",
        model=model,
        output=(
            "No LLM API key is configured. Set OPENAI_API_KEY or "
            "ANTHROPIC_API_KEY environment variable to enable LLM integration. "
            "See README.md for configuration instructions."
        ),
        stub=True,
        error="No API key configured",
    )
