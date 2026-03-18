# Deep Agents LangChain

Deep Agents LangChain is a professionally structured Python project for building research and planning workflows with LangChain. It provides a reusable application foundation for turning user prompts into structured, section-based outputs through validated inputs, modular orchestration, and separate execution interfaces for CLI and web usage.

The codebase is designed to be maintainable, extensible, and production-friendly. It emphasizes clean boundaries between application layers, predictable data models, and a workflow that can run both with a live LLM and in a deterministic fallback mode when API credentials are not available.

## Key Highlights

- Modular architecture with clear separation of configuration, schemas, orchestration, and service logic
- Strict Pydantic-based validation for environment settings and runtime request payloads
- Shared orchestration layer reused by both `main.py` and `app.py`
- Dedicated CLI entry point for terminal-based execution
- Dedicated Streamlit interface for interactive usage
- Deterministic fallback mode when `OPENAI_API_KEY` is not configured
- Clean starting point for adding tools, retrieval, memory, evaluators, and multi-agent workflows

## Architecture Overview

The repository follows a layered structure so each concern remains isolated and easy to evolve:

- `config.py` handles environment-driven application settings and validation
- `schemas.py` defines the request and response contracts used across the application
- `prompts.py` centralizes prompt templates used by the workflow
- `services/` contains the business logic for model selection and structured research generation
- `orchestrator.py` provides the application facade consumed by both user entry points
- `main.py` exposes the workflow through a command-line interface
- `app.py` exposes the same workflow through a Streamlit web application

This structure keeps the code professional and scalable, while making it straightforward to test, refactor, or extend individual layers independently.

## Project Structure

```text
.
├── app.py
├── main.py
├── README.md
├── requirements.txt
├── src/
│   └── deep_agents_langchain/
│       ├── __init__.py
│       ├── config.py
│       ├── orchestrator.py
│       ├── prompts.py
│       ├── schemas.py
│       └── services/
│           ├── __init__.py
│           ├── llm_factory.py
│           └── research_service.py
└── tests/
    └── test_research_service.py
```

## Core Capabilities

### 1. Validated Input and Configuration Management

The project uses Pydantic and `pydantic-settings` to enforce strong validation for:

- environment variables
- runtime request payloads
- sectioned response objects

This reduces configuration drift, prevents malformed inputs, and improves runtime reliability.

### 2. Shared Research Workflow

The central workflow is implemented once and reused across interfaces. The process includes:

- request validation
- planning and refinement of the user goal
- section-by-section synthesis
- structured response generation

This makes the system easier to maintain and ensures consistent behavior between the CLI and the web app.

### 3. Dual Execution Interfaces

The repository separates execution concerns cleanly:

- `main.py` is intended for terminal, scripting, and automation use cases
- `app.py` is intended for interactive exploration through Streamlit

Both entry points rely on the same orchestration and service layers, avoiding duplicated logic.

### 4. Safe Fallback Behavior

If an OpenAI API key is not configured, the application still runs using a deterministic fallback response path. This is useful for:

- local development
- UI and CLI testing
- validation of the project structure before connecting live model access

## Installation

### Prerequisites

- Python 3.11 or 3.12 recommended
- `pip`
- An OpenAI API key if you want live model-based output

### Setup

1. Create a virtual environment:

```bash
python3.11 -m venv .venv
```

2. Activate the environment:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create your environment file:

```bash
cp .env.example .env
```

5. Add your API credentials to `.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

## Running the Project

### Run the CLI

```bash
python main.py "Build a market-entry strategy for an AI finance assistant" --audience executives --max-sections 4
```

### Run the Streamlit Application

```bash
streamlit run app.py
```

### Run the Test Suite

```bash
pytest
```

## Example Use Cases

This project can serve as a foundation for:

- AI research assistants
- business strategy generation tools
- planning and analysis copilots
- internal knowledge workflow prototypes
- multi-step agent systems built on LangChain

## Extensibility

The current implementation is intentionally structured as a strong base for future growth. It can be extended to support:

- external tools and APIs
- document retrieval and RAG pipelines
- agent memory
- evaluation and scoring layers
- multi-agent task decomposition
- LangGraph-based workflow coordination

## Professional Engineering Notes

- The codebase is organized for readability and long-term maintainability
- Business logic is isolated from interface code
- Validation is enforced at the boundary of the system
- The project includes a testable service layer and a minimal automated test
- The repository is suitable as a starter template for more advanced agent applications

## Notes

- Without an OpenAI API key, the system runs in deterministic fallback mode
- Python 3.11 or 3.12 is recommended for the best current LangChain compatibility
