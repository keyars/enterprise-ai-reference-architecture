"""Model provider interfaces and a deterministic local provider for development."""

from abc import ABC, abstractmethod

from .models import GenerationRequest, GenerationResponse


class ModelProvider(ABC):
    """Contract implemented by concrete LLM providers."""

    name: str

    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate a normalized response."""
        raise NotImplementedError


class LocalEchoProvider(ModelProvider):
    """Deterministic provider used for tests and local architecture validation."""

    name = "local-echo"

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        user_messages = [m["content"] for m in request.messages if m.get("role") == "user"]
        text = user_messages[-1] if user_messages else "No user message supplied."
        return GenerationResponse(
            text=f"Echo: {text}",
            model=request.model or "local-echo-v1",
            provider=self.name,
            metadata={"deterministic": True},
        )
