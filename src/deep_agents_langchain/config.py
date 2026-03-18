"""Application configuration and environment validation."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated application settings loaded from environment variables."""

    app_name: str = Field(default="Deep Agents LangChain", min_length=3, alias="APP_NAME")
    environment: str = Field(
        default="development",
        pattern="^(development|staging|production)$",
        alias="ENVIRONMENT",
    )
    default_model: str = Field(default="gpt-4o-mini", min_length=3, alias="DEFAULT_MODEL")
    max_iterations: int = Field(default=3, ge=1, le=10, alias="MAX_ITERATIONS")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0, alias="TEMPERATURE")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8501, ge=1, le=65535, alias="APP_PORT")

    model_config = SettingsConfigDict(
        env_file=(".env",),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings or raise a readable validation error."""

    try:
        return Settings()
    except ValidationError as exc:
        raise RuntimeError(f"Invalid application configuration: {exc}") from exc


def project_root() -> Path:
    """Resolve the repository root from the package path."""

    return Path(__file__).resolve().parents[2]
