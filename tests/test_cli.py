from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import main
from deep_agents_langchain.schemas import ResearchResponse, ResearchSection


def test_render_markdown_formats_sections_and_summary() -> None:
    payload = ResearchResponse(
        original_query="Build an AI roadmap",
        refined_goal="Create an execution-ready AI roadmap",
        sections=[
            ResearchSection(
                heading="Problem framing",
                content="Define the business objective, constraints, and decision timeline.",
            ),
            ResearchSection(
                heading="Execution plan",
                content="Sequence the work across discovery, implementation, validation, and rollout.",
            ),
        ],
        summary="The roadmap is structured into practical sections with a clear execution path.",
        execution_mode="template_fallback",
    ).model_dump()

    rendered = main.render_markdown(payload)

    assert rendered.startswith("# Create an execution-ready AI roadmap")
    assert "## Problem framing" in rendered
    assert "## Summary" in rendered


def test_main_supports_json_output(monkeypatch, capsys) -> None:
    response = ResearchResponse(
        original_query="Build an AI roadmap",
        refined_goal="Create an execution-ready AI roadmap",
        sections=[
            ResearchSection(
                heading="Problem framing",
                content="Define the business objective, constraints, and decision timeline.",
            )
        ],
        summary="The roadmap is structured into practical sections with a clear execution path.",
        execution_mode="template_fallback",
    )

    class StubOrchestrator:
        def run(self, request):
            assert request.output_format == "json"
            return response

    monkeypatch.setattr(main, "DeepAgentOrchestrator", StubOrchestrator)
    monkeypatch.setattr(
        sys,
        "argv",
        ["main.py", "Build an AI roadmap", "--output-format", "json"],
    )

    exit_code = main.main()
    output = capsys.readouterr().out

    assert exit_code == 0
    assert '"execution_mode": "template_fallback"' in output
    assert '"refined_goal": "Create an execution-ready AI roadmap"' in output
