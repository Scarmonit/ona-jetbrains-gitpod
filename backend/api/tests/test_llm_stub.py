"""
Tests for LLM stub functionality.

These tests verify that the LLM endpoint returns stub responses
when no API keys are configured.
"""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client_no_keys():
    """Create a test client with no LLM API keys configured."""
    # Clear any existing API keys from environment
    env_patch = {
        "OPENAI_API_KEY": "",
        "ANTHROPIC_API_KEY": "",
    }

    with patch.dict(os.environ, env_patch, clear=False):
        # Need to reimport to pick up new settings
        from app.config import get_settings

        get_settings.cache_clear()

        from app.main import app

        yield TestClient(app)

        # Clear cache after test
        get_settings.cache_clear()


def test_health_endpoint(client_no_keys):
    """Test health endpoint returns ok status."""
    response = client_no_keys.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "version" in data


def test_info_endpoint_no_keys(client_no_keys):
    """Test info endpoint shows stub provider when no keys configured."""
    response = client_no_keys.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "llm_providers" in data
    assert "stub" in data["llm_providers"]
    assert data["active_provider"] == "stub"


def test_llm_stub_response(client_no_keys):
    """Test LLM endpoint returns stub response when no keys configured."""
    response = client_no_keys.post(
        "/llm",
        json={"prompt": "Hello, world!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "stub"
    assert data["model"] == "none"
    assert data["stub"] is True
    assert data["error"] is None
    assert "stub response" in data["output"].lower() or "real llm" in data["output"].lower()


def test_llm_empty_prompt_rejected(client_no_keys):
    """Test that empty prompts are rejected."""
    response = client_no_keys.post(
        "/llm",
        json={"prompt": ""},
    )
    assert response.status_code == 422  # Validation error


def test_llm_missing_prompt_rejected(client_no_keys):
    """Test that missing prompt is rejected."""
    response = client_no_keys.post(
        "/llm",
        json={},
    )
    assert response.status_code == 422  # Validation error


def test_llm_prompt_too_long_rejected(client_no_keys):
    """Test that prompts exceeding max length are rejected."""
    long_prompt = "a" * 5000  # Exceeds 4000 char limit
    response = client_no_keys.post(
        "/llm",
        json={"prompt": long_prompt},
    )
    assert response.status_code == 422  # Validation error
