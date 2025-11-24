"""
Main FastAPI application module.

Provides health, info, and LLM endpoints for the Ona backend service.
"""

import logging
from datetime import datetime, timezone
from typing import Dict

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .llm import LLMRequest, LLMResponse, complete

# Configure logging
settings = get_settings()
logging.basicConfig(
    level=getattr(logging, settings.py_log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI backend service with LLM integration for the Ona environment",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """Check if the API is running.

    Returns:
        Dictionary with status, timestamp, and version.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.app_version,
    }


@app.get("/info", tags=["Info"])
async def get_info() -> Dict[str, object]:
    """Get information about the service.

    Returns:
        Dictionary with service information including available LLM providers.
    """
    providers = []
    if settings.openai_api_key:
        providers.append("openai")
    if settings.anthropic_api_key:
        providers.append("anthropic")
    if not providers:
        providers.append("stub")

    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.py_env,
        "llm_providers": providers,
        "active_provider": providers[0] if providers else "none",
    }


@app.post("/llm", response_model=LLMResponse, tags=["LLM"])
async def llm_completion(request: LLMRequest) -> LLMResponse:
    """Process an LLM completion request.

    Provider selection order:
    1. OpenAI (if OPENAI_API_KEY is set)
    2. Anthropic (if ANTHROPIC_API_KEY is set)
    3. Stub (fallback when no keys are configured)

    Args:
        request: LLM completion request with prompt.

    Returns:
        LLMResponse with provider, model, output, stub flag, and optional error.

    Raises:
        HTTPException: If prompt validation fails.
    """
    logger.info("Processing LLM request - prompt_length=%d", len(request.prompt))

    try:
        response = await complete(request)
        return response
    except Exception as e:
        logger.exception("Unexpected error during LLM completion")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}",
        ) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
