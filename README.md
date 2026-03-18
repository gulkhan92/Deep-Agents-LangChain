# Deep Agents LangChain

A production-style starter project for building structured AI agent workflows with LangChain. The repository includes:

- a reusable service layer under `src/`
- strict Pydantic-based input validation
- a CLI entry point in `main.py`
- a separate Streamlit UI in `app.py`
- environment-driven configuration
- a basic test suite

## Project Structure

```text
.
├── app.py
├── main.py
├── requirements.txt
├── src/
│   └── deep_agents_langchain/
│       ├── config.py
│       ├── orchestrator.py
│       ├── prompts.py
│       ├── schemas.py
│       └── services/
│           ├── llm_factory.py
│           └── research_service.py
└── tests/
    └── test_research_service.py
```

## Features

- Modular architecture with clear separation of configuration, schemas, orchestration, and service logic
- Safe fallback mode when no OpenAI API key is configured
- Reusable workflow shared by both CLI and UI entry points
- Structured output with sectioned analysis
- Ready for extension with tools, memory, retrieval, or LangGraph-style coordination

## Setup

1. Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
```

Add your `OPENAI_API_KEY` to `.env` to enable live LLM generation.

## Run the CLI

```bash
python main.py "Build a market-entry strategy for an AI finance assistant" --audience executives --max-sections 4
```

## Run the Streamlit App

```bash
streamlit run app.py
```

## Run Tests

```bash
pytest
```

## Notes

- Without an OpenAI API key, the project still runs in deterministic fallback mode.
- The current implementation focuses on a professional foundation that can be extended with search, retrieval, multi-agent decomposition, or evaluation pipelines.
- Python 3.11 or 3.12 is recommended for the cleanest LangChain runtime compatibility today.
