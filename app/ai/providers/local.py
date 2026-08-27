from app.ai.models import GenerationRequest, GenerationResponse
from app.ai.providers.base import ModelProvider


class LocalProvider(ModelProvider):
    name = "local"

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        model = request.model or "local-deterministic"
        return GenerationResponse(
            text=f"Local provider response: {request.prompt}",
            provider=self.name,
            model=model,
        )
