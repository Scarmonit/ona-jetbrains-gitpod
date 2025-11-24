"""Tests for the health endpoint.

This module contains integration tests for the /health endpoint
to verify that it returns correct status and uptime information.
"""

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_200() -> None:
    """Test that the health endpoint returns HTTP 200 status code."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200


def test_health_endpoint_returns_ok_status() -> None:
    """Test that the health endpoint returns 'ok' status."""
    client = TestClient(app)
    response = client.get("/health")
    data = response.json()

    assert "status" in data
    assert data["status"] == "ok"


def test_health_endpoint_returns_uptime_seconds() -> None:
    """Test that the health endpoint returns uptime_seconds field."""
    client = TestClient(app)
    response = client.get("/health")
    data = response.json()

    assert "uptime_seconds" in data
    assert isinstance(data["uptime_seconds"], float)
    assert data["uptime_seconds"] >= 0


def test_health_endpoint_response_structure() -> None:
    """Test that the health endpoint returns the expected response structure."""
    client = TestClient(app)
    response = client.get("/health")
    data = response.json()

    # Verify all expected fields are present
    expected_fields = {"status", "uptime_seconds"}
    assert set(data.keys()) == expected_fields


def test_info_endpoint_returns_200() -> None:
    """Test that the info endpoint returns HTTP 200 status code."""
    client = TestClient(app)
    response = client.get("/info")

    assert response.status_code == 200


def test_info_endpoint_returns_app_metadata() -> None:
    """Test that the info endpoint returns app metadata."""
    client = TestClient(app)
    response = client.get("/info")
    data = response.json()

    assert "app" in data
    assert "version" in data
    assert "env" in data


def test_llm_endpoint_returns_200() -> None:
    """Test that the LLM endpoint returns HTTP 200 status code."""
    client = TestClient(app)
    response = client.post("/llm", json={"prompt": "test prompt"})

    assert response.status_code == 200


def test_llm_endpoint_returns_stub_without_api_key() -> None:
    """Test that the LLM endpoint returns a stub response without API keys."""
    client = TestClient(app)
    response = client.post("/llm", json={"prompt": "test prompt"})
    data = response.json()

    assert "stub" in data
    assert data["stub"] is True
    assert "provider" in data
    assert "output" in data


def test_llm_endpoint_validates_request() -> None:
    """Test that the LLM endpoint validates the request body."""
    client = TestClient(app)
    response = client.post("/llm", json={})  # Missing required 'prompt' field

    assert response.status_code == 422
