"""Provider-neutral AI gateway."""

from .models import GenerationRequest, GenerationResponse
from .providers import ModelProvider


class AIGateway:
    """Application-facing boundary that hides model-provider details."""

    def __init__(self, provider: ModelProvider) -> None:
        self._provider = provider

    @property
    def provider_name(self) -> str:
        return self._provider.name

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate text through the configured provider."""
        if not request.messages:
            raise ValueError("At least one message is required.")
        return await self._provider.generate(request)
