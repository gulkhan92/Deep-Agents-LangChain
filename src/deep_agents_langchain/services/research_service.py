"""Core research workflow service."""

from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from ..config import Settings
from ..prompts import PLANNING_PROMPT, SYNTHESIS_PROMPT, SYSTEM_PROMPT
from ..schemas import ResearchRequest, ResearchResponse, ResearchSection
from .llm_factory import build_chat_model


class ResearchService:
    """Run a structured research workflow using LangChain with a safe fallback."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.model = build_chat_model(settings)

    def run(self, request: ResearchRequest) -> ResearchResponse:
        if self.model is None:
            return self._fallback_response(request)
        return self._live_response(request)

    def _live_response(self, request: ResearchRequest) -> ResearchResponse:
        planning_prompt = ChatPromptTemplate.from_messages(
            [("system", SYSTEM_PROMPT), ("human", PLANNING_PROMPT)]
        )
        synthesis_prompt = ChatPromptTemplate.from_messages(
            [("system", SYSTEM_PROMPT), ("human", SYNTHESIS_PROMPT)]
        )
        parser = StrOutputParser()

        planning_chain = planning_prompt | self.model | parser
        plan_text = planning_chain.invoke(
            {
                "query": request.query,
                "audience": request.audience,
                "context": request.context or "None provided",
                "max_sections": request.max_sections,
            }
        )

        parsed_goal, headings = self._parse_plan(plan_text, request.max_sections)
        sections: list[ResearchSection] = []

        for heading in headings:
            synthesis_chain = synthesis_prompt | self.model | parser
            content = synthesis_chain.invoke(
                {
                    "goal": parsed_goal,
                    "heading": heading,
                    "query": request.query,
                    "audience": request.audience,
                    "context": request.context or "None provided",
                }
            )
            sections.append(ResearchSection(heading=heading, content=content.strip()))

        summary = (
            f"This report addresses '{request.query}' for a {request.audience} audience "
            f"with {len(sections)} execution-ready sections."
        )

        return ResearchResponse(
            original_query=request.query,
            refined_goal=parsed_goal,
            sections=sections,
            summary=summary,
            execution_mode="live_llm",
        )

    def _parse_plan(self, plan_text: str, max_sections: int) -> tuple[str, list[str]]:
        lines = [line.strip("- ").strip() for line in plan_text.splitlines() if line.strip()]
        goal = lines[0] if lines else "Deliver a practical response to the user's request."
        headings = lines[1 : max_sections + 1]
        if not headings:
            headings = [
                "Problem framing",
                "Recommended architecture",
                "Execution plan",
                "Key risks and mitigations",
            ][:max_sections]
        return goal, headings

    def _fallback_response(self, request: ResearchRequest) -> ResearchResponse:
        sections = [
            ResearchSection(
                heading="Problem framing",
                content=(
                    f"The request centers on '{request.query}'. The first step is to define "
                    "the decision to be made, the operating constraints, and the success criteria."
                ),
            ),
            ResearchSection(
                heading="Recommended architecture",
                content=(
                    "Use a layered agent workflow with explicit input validation, a planning step, "
                    "sectioned synthesis, and a presentation layer that can be reused across CLI and UI entry points."
                ),
            ),
            ResearchSection(
                heading="Execution plan",
                content=(
                    "Start with requirements capture, convert the problem into validated inputs, "
                    "generate a clear plan, and then produce structured output that can be tested and persisted."
                ),
            ),
            ResearchSection(
                heading="Key risks and mitigations",
                content=(
                    "Main risks include vague scope, unvalidated inputs, and inconsistent output shape. "
                    "Mitigate these with Pydantic models, deterministic section templates, and observable logging."
                ),
            ),
        ][: request.max_sections]

        return ResearchResponse(
            original_query=request.query,
            refined_goal=f"Create an actionable analysis plan for: {request.query}",
            sections=sections,
            summary="Fallback mode is active because no OpenAI API key is configured. The project remains fully runnable.",
            execution_mode="template_fallback",
        )
