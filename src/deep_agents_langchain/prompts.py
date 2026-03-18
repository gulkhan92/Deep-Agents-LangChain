"""Prompt templates for the deep agent workflow."""

SYSTEM_PROMPT = """
You are a senior AI research strategist.
Produce concise, accurate, and implementation-oriented analysis.
Break the task into practical sections and focus on business value, technical design, risks, and next steps.
""".strip()

PLANNING_PROMPT = """
Create a refined research goal for the following request.

User query: {query}
Audience: {audience}
Additional context: {context}

Return a short refined goal statement followed by {max_sections} section headings.
""".strip()

SYNTHESIS_PROMPT = """
Write a professional report section for this heading.

Refined goal: {goal}
Heading: {heading}
Original query: {query}
Audience: {audience}
Additional context: {context}

The response must be actionable and specific.
""".strip()
