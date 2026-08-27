from abc import ABC, abstractmethod

from app.ai.models import GenerationRequest, GenerationResponse


class ModelProvider(ABC):
    """Provider contract used by the AI gateway."""

    name: str

    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        raise NotImplementedError
