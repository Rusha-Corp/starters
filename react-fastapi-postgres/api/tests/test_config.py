"""Tests for application configuration and settings."""
import os
import pytest
from config import Settings, get_settings


class TestSettings:
    """Test Settings class defaults and validation."""

    def test_default_database_url_is_set(self):
        """Settings should have a database URL configured."""
        settings = Settings()
        assert settings.database_url is not None
        assert len(settings.database_url) > 0

    def test_default_secret_key(self):
        """Default secret key should be set (even if insecure for production)."""
        settings = Settings()
        assert settings.secret_key is not None
        assert len(settings.secret_key) > 0

    def test_default_cors_origins(self):
        """Default CORS origins should include localhost."""
        settings = Settings()
        assert isinstance(settings.cors_origins, list)
        assert "http://localhost:3000" in settings.cors_origins

    def test_default_log_level_is_valid(self):
        """Log level should be a valid level string."""
        settings = Settings()
        assert settings.log_level in ("DEBUG", "INFO", "WARNING", "ERROR")

    def test_default_metrics_enabled(self):
        """Metrics should be enabled by default."""
        settings = Settings()
        assert settings.metrics_enabled is True

    def test_environment_override(self):
        """Settings should be overridable via environment variables."""
        original = os.environ.get("LOG_LEVEL")
        os.environ["LOG_LEVEL"] = "DEBUG"
        try:
            # Clear lru_cache so new Settings() picks up env var
            get_settings.cache_clear()
            settings = Settings()
            assert settings.log_level == "DEBUG"
        finally:
            if original is not None:
                os.environ["LOG_LEVEL"] = original
            else:
                os.environ.pop("LOG_LEVEL", None)
            get_settings.cache_clear()

    def test_get_settings_is_cached(self):
        """get_settings should return the same cached instance."""
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2
