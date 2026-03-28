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


def test_fallback_response_respects_requested_section_limit() -> None:
    service = ResearchService(Settings())
    request = ResearchRequest(
        query="Design an AI roadmap for a mid-sized SaaS company",
        max_sections=2,
    )

    response = service.run(request)

    assert len(response.sections) == 2
    assert response.sections[0].heading == "Problem framing"
    assert response.execution_mode == "template_fallback"


def test_parse_plan_uses_defaults_when_headings_are_missing() -> None:
    service = ResearchService(Settings())

    goal, headings = service._parse_plan("", max_sections=3)

    assert goal == "Deliver a practical response to the user's request."
    assert headings == [
        "Problem framing",
        "Recommended architecture",
        "Execution plan",
    ]


def test_parse_plan_trims_bullets_and_honors_max_sections() -> None:
    service = ResearchService(Settings())
    plan_text = """
    Refined goal
    - Section one
    - Section two
    - Section three
    """.strip()

    goal, headings = service._parse_plan(plan_text, max_sections=2)

    assert goal == "Refined goal"
    assert headings == ["Section one", "Section two"]
