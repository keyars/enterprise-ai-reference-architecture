from abc import ABC, abstractmethod

from app.ai.models import (
    GenerationRequest,
    GenerationResponse,
    ToolCallingRequest,
    ToolCallingResponse,
)


class ModelProvider(ABC):
    """Provider contract used by the AI gateway."""

    name: str

    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        raise NotImplementedError


class ToolCallingProvider(ModelProvider):
    """Provider contract for native structured tool calling."""

    @abstractmethod
    async def generate_with_tools(self, request: ToolCallingRequest) -> ToolCallingResponse:
        raise NotImplementedError
