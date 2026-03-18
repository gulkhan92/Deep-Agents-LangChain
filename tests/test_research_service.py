from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from deep_agents_langchain.config import Settings
from deep_agents_langchain.schemas import ResearchRequest
from deep_agents_langchain.services.research_service import ResearchService


def test_fallback_response_returns_bounded_sections() -> None:
    service = ResearchService(Settings())
    request = ResearchRequest(query="Design an AI roadmap for a mid-sized SaaS company")

    response = service.run(request)

    assert response.original_query == request.query
    assert 1 <= len(response.sections) <= request.max_sections
    assert response.summary
