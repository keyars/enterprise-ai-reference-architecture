from openai import AsyncOpenAI

from app.ai.models import GenerationRequest, GenerationResponse, Usage
from app.ai.providers.base import ModelProvider


class OpenAIProvider(ModelProvider):
    name = "openai"

    def __init__(self, api_key: str, default_model: str = "gpt-5.5", timeout: float = 30.0) -> None:
        self.default_model = default_model
        self.client = AsyncOpenAI(api_key=api_key, timeout=timeout)

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        model = request.model or self.default_model
        response = await self.client.responses.create(
            model=model,
            input=request.prompt,
            temperature=request.temperature,
            max_output_tokens=request.max_tokens,
        )
        usage = response.usage
        return GenerationResponse(
            text=response.output_text,
            provider=self.name,
            model=model,
            usage=Usage(
                input_tokens=getattr(usage, "input_tokens", 0) if usage else 0,
                output_tokens=getattr(usage, "output_tokens", 0) if usage else 0,
                total_tokens=getattr(usage, "total_tokens", 0) if usage else 0,
            ),
        )
