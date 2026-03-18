"""LLM construction utilities."""

from langchain_openai import ChatOpenAI

from ..config import Settings


def build_chat_model(settings: Settings) -> ChatOpenAI | None:
    """Build an OpenAI chat model when credentials are available."""

    if not settings.openai_api_key:
        return None

    return ChatOpenAI(
        model=settings.default_model,
        temperature=settings.temperature,
        api_key=settings.openai_api_key,
    )
