"""Streamlit UI for the Deep Agents LangChain project."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from deep_agents_langchain import DeepAgentOrchestrator
from deep_agents_langchain.schemas import ResearchRequest


st.set_page_config(
    page_title="Deep Agents LangChain",
    layout="wide",
)

st.title("Deep Agents LangChain")
st.caption("A modular LangChain project for research planning and structured synthesis.")

with st.sidebar:
    st.subheader("Run settings")
    audience = st.text_input("Audience", value="general")
    max_sections = st.slider("Max sections", min_value=1, max_value=8, value=4)
    context = st.text_area("Additional context", placeholder="Optional background or constraints")

query = st.text_area(
    "Research query",
    height=160,
    placeholder="Example: Build a go-to-market plan for an AI support copilot in fintech.",
)

if st.button("Run agent", type="primary", use_container_width=True):
    if not query.strip():
        st.error("A query is required.")
    else:
        with st.spinner("Generating structured analysis..."):
            request = ResearchRequest(
                query=query,
                context=context or None,
                audience=audience,
                max_sections=max_sections,
            )
            response = DeepAgentOrchestrator().run(request)

        st.success(f"Completed in `{response.execution_mode}` mode.")
        st.subheader("Refined goal")
        st.write(response.refined_goal)

        for section in response.sections:
            st.markdown(f"### {section.heading}")
            st.write(section.content)

        st.subheader("Summary")
        st.write(response.summary)
