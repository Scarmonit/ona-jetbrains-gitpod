"""Tests for the configuration module.

This module contains tests to verify that the Settings class correctly
loads and handles environment variables.
"""

import os
from unittest.mock import patch

from app.config import Settings, load_settings


def test_settings_default_values() -> None:
    """Test that Settings has correct default values."""
    settings = Settings()

    assert settings.APP_NAME == "Ona Backend API"
    assert settings.APP_VERSION == "0.1.0"
    assert settings.LOG_LEVEL == "INFO"
    assert settings.ENV == "development"
    assert settings.OPENAI_API_KEY is None
    assert settings.ANTHROPIC_API_KEY is None


def test_settings_loads_env_variables() -> None:
    """Test that Settings correctly loads environment variables."""
    env_vars = {
        "APP_NAME": "Test App",
        "APP_VERSION": "2.0.0",
        "LOG_LEVEL": "DEBUG",
        "ENV": "production",
        "OPENAI_API_KEY": "test-openai-key",
        "ANTHROPIC_API_KEY": "test-anthropic-key",
    }

    with patch.dict(os.environ, env_vars, clear=False):
        settings = Settings()

        assert settings.APP_NAME == "Test App"
        assert settings.APP_VERSION == "2.0.0"
        assert settings.LOG_LEVEL == "DEBUG"
        assert settings.ENV == "production"
        assert settings.OPENAI_API_KEY == "test-openai-key"
        assert settings.ANTHROPIC_API_KEY == "test-anthropic-key"


def test_settings_partial_env_override() -> None:
    """Test that Settings correctly handles partial environment overrides."""
    env_vars = {
        "OPENAI_API_KEY": "my-api-key",
    }

    with patch.dict(os.environ, env_vars, clear=False):
        settings = Settings()

        # Overridden value
        assert settings.OPENAI_API_KEY == "my-api-key"

        # Default values
        assert settings.APP_NAME == "Ona Backend API"
        assert settings.ENV == "development"


def test_load_settings_returns_settings_instance() -> None:
    """Test that load_settings returns a Settings instance."""
    # Clear the cache to ensure we get a fresh instance
    load_settings.cache_clear()

    settings = load_settings()

    assert isinstance(settings, Settings)


def test_load_settings_caching() -> None:
    """Test that load_settings returns cached instance."""
    # Clear the cache first
    load_settings.cache_clear()

    settings1 = load_settings()
    settings2 = load_settings()

    # Both should be the same cached instance
    assert settings1 is settings2
