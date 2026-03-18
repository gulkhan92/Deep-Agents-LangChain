"""CLI entry point for the project."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from deep_agents_langchain import DeepAgentOrchestrator
from deep_agents_langchain.schemas import ResearchRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Deep Agents LangChain workflow.")
    parser.add_argument("query", help="The research or planning query to analyze.")
    parser.add_argument("--context", default=None, help="Optional supporting context.")
    parser.add_argument("--audience", default="general", help="Target audience for the output.")
    parser.add_argument(
        "--output-format",
        choices=("markdown", "text", "json"),
        default="markdown",
        help="Preferred output style.",
    )
    parser.add_argument(
        "--max-sections",
        type=int,
        default=4,
        help="Maximum number of sections to generate.",
    )
    return parser


def render_markdown(result: dict) -> str:
    lines = [f"# {result['refined_goal']}", ""]
    for section in result["sections"]:
        lines.extend([f"## {section['heading']}", section["content"], ""])
    lines.extend(["## Summary", result["summary"]])
    return "\n".join(lines)


def main() -> int:
    args = build_parser().parse_args()
    request = ResearchRequest(
        query=args.query,
        context=args.context,
        audience=args.audience,
        output_format=args.output_format,
        max_sections=args.max_sections,
    )
    orchestrator = DeepAgentOrchestrator()
    response = orchestrator.run(request)
    payload = response.model_dump()

    if args.output_format == "json":
        print(json.dumps(payload, indent=2))
    elif args.output_format == "text":
        print(render_markdown(payload).replace("#", "").strip())
    else:
        print(render_markdown(payload))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
