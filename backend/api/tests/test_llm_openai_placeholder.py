"""
Tests for OpenAI LLM integration.

These tests are skipped if OPENAI_API_KEY is not set in the environment.
They verify real API integration when credentials are available.
"""

import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

# Skip all tests in this module if OPENAI_API_KEY is not set
pytestmark = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set - skipping OpenAI integration tests",
)


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_llm_openai_real_call(client):
    """Test LLM endpoint makes real OpenAI call when key is set.

    This test only runs if OPENAI_API_KEY is configured.
    """
    response = client.post(
        "/llm",
        json={"prompt": "Say 'test' and nothing else."},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "openai"
    assert data["stub"] is False
    # Either we get output or an error, but not both empty
    assert data["output"] or data["error"]


def test_info_shows_openai_provider(client):
    """Test info endpoint shows OpenAI as active provider."""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "openai" in data["llm_providers"]
    assert data["active_provider"] == "openai"
