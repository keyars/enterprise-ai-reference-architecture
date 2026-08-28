from dataclasses import dataclass
from time import perf_counter

from app.ai.models import GenerationRequest, GenerationResponse
from app.ai.providers.base import ModelProvider
from app.observability import metrics


@dataclass(slots=True)
class AIGateway:
    provider: ModelProvider

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        started = perf_counter()
        response = await self.provider.generate(request)
        latency_ms = round((perf_counter() - started) * 1000, 2)
        metrics.record_llm(
            provider=response.provider,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            latency_ms=latency_ms,
        )
        return response.model_copy(update={"latency_ms": latency_ms})
