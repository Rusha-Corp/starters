"""
Application configuration loaded from environment variables.
Uses pydantic-settings for validation and .env file support.
"""
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = Field(
        default="postgresql://rusha:rusha@db:5432/rusha",
        description="PostgreSQL connection string",
    )
    sqlalchemy_echo: bool = Field(
        default=False,
        description="Enable SQL query logging",
    )

    # Security
    secret_key: str = Field(
        default="change-me-in-production",
        description="Application secret key for JWT/sessions",
    )

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Warn if the default secret key is used (validation happens at runtime)."""
        if v == "change-me-in-production":
            import warnings
            warnings.warn(
                "SECURITY: Default SECRET_KEY detected. "
                "Set SECRET_KEY to a strong random value in production.",
                stacklevel=2,
            )
        if len(v) < 16:
            import warnings
            warnings.warn(
                f"SECURITY: SECRET_KEY is only {len(v)} characters. "
                "Recommend at least 32 characters for production.",
                stacklevel=2,
            )
        return v

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins",
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        description="Log level (DEBUG, INFO, WARNING, ERROR)",
    )
    log_format: str = Field(
        default="text",
        description="Log format (text or json)",
    )

    # Metrics
    metrics_enabled: bool = Field(
        default=True,
        description="Enable Prometheus metrics endpoint",
    )

    # Rate limiting
    rate_limit_enabled: bool = Field(
        default=True,
        description="Enable rate limiting on API endpoints",
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
