"""FastAPI application entry point.

This module creates and configures the FastAPI application with health,
info, and LLM proxy endpoints. It uses a lifespan context manager to
track application uptime.
"""

import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, status
from pydantic import ValidationError

from app.config import load_settings
from app.llm import process_prompt
from app.logging_config import get_logger, setup_logging
from app.models import HealthResponse, InfoResponse, LLMRequest, LLMResponse


# Global variable to store application start time
_start_time: float = 0.0


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for application startup and shutdown.

    Captures the start time for uptime calculation and performs any
    necessary initialization and cleanup.

    Args:
        app: The FastAPI application instance.

    Yields:
        None: Yields control to the application.
    """
    global _start_time
    _start_time = time.perf_counter()

    # Load settings and configure logging at startup
    settings = load_settings()
    setup_logging(settings.LOG_LEVEL)

    logger = get_logger(__name__)
    logger.info(
        f"Starting {settings.APP_NAME} v{settings.APP_VERSION} "
        f"in {settings.ENV} environment"
    )

    yield

    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Ona Backend API",
    version="0.1.0",
    description=(
        "Production-ready FastAPI backend service with health checks, "
        "info endpoint, and LLM proxy placeholder."
    ),
    lifespan=lifespan,
)


def get_uptime_seconds() -> float:
    """Calculate the application uptime in seconds.

    Returns:
        float: The number of seconds since the application started.
    """
    return time.perf_counter() - _start_time


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check endpoint",
    description="Returns the current health status and uptime of the service.",
)
async def health_check() -> HealthResponse:
    """Check the health status of the application.

    Returns:
        HealthResponse: The health status and uptime in seconds.
    """
    return HealthResponse(
        status="ok",
        uptime_seconds=get_uptime_seconds(),
    )


@app.get(
    "/info",
    response_model=InfoResponse,
    tags=["Info"],
    summary="Application info endpoint",
    description="Returns application metadata including name, version, and environment.",
)
async def app_info() -> InfoResponse:
    """Get application information.

    Returns:
        InfoResponse: Application name, version, and environment.
    """
    settings = load_settings()
    return InfoResponse(
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        env=settings.ENV,
    )


@app.post(
    "/llm",
    response_model=LLMResponse,
    tags=["LLM"],
    summary="LLM proxy endpoint",
    description=(
        "Process a prompt through the configured LLM provider. "
        "Returns a stub response if no API key is configured."
    ),
)
async def llm_proxy(request: LLMRequest) -> LLMResponse:
    """Process an LLM prompt request.

    Args:
        request: The LLM request containing the prompt and optional model.

    Returns:
        LLMResponse: The LLM response or stub message.

    Raises:
        HTTPException: If request validation fails or an unexpected error occurs.
    """
    logger = get_logger(__name__)

    try:
        settings = load_settings()
        response = process_prompt(settings, request)
        logger.info(
            f"LLM request processed: provider={response.provider}, "
            f"stub={response.stub}"
        )
        return response
    except ValidationError as e:
        logger.error(f"Validation error in LLM request: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}",
        )
    except Exception as e:
        logger.exception(f"Unexpected error processing LLM request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the request.",
        )
