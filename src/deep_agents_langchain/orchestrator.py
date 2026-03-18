"""Application orchestration layer."""

from .config import get_settings
from .schemas import ResearchRequest, ResearchResponse
from .services.research_service import ResearchService


class DeepAgentOrchestrator:
    """Facade used by both CLI and UI entry points."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.research_service = ResearchService(self.settings)

    def run(self, request: ResearchRequest) -> ResearchResponse:
        return self.research_service.run(request)
