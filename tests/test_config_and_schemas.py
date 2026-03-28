from pathlib import Path
import sys

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from deep_agents_langchain.config import Settings, project_root
from deep_agents_langchain.schemas import ResearchRequest


def test_settings_support_env_aliases() -> None:
    settings = Settings(
        APP_NAME="Deep Agents LangChain",
        ENVIRONMENT="production",
        DEFAULT_MODEL="gpt-4o-mini",
        MAX_ITERATIONS=5,
        TEMPERATURE=0.4,
        APP_HOST="127.0.0.1",
        APP_PORT=9000,
    )

    assert settings.environment == "production"
    assert settings.max_iterations == 5
    assert settings.app_port == 9000


def test_project_root_resolves_repository_root() -> None:
    assert project_root() == ROOT


def test_research_request_normalizes_whitespace_and_context() -> None:
    request = ResearchRequest(
        query="  Build    a   market   entry strategy   ",
        context="   ",
        output_format="json",
    )

    assert request.query == "Build a market entry strategy"
    assert request.context is None
    assert request.output_format == "json"


def test_research_request_rejects_too_short_query() -> None:
    with pytest.raises(ValidationError):
        ResearchRequest(query="AI")
