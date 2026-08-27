"""Provider-neutral contracts for AI generation."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GenerationRequest:
    """Input contract shared by all model providers."""

    messages: list[dict[str, str]]
    model: str | None = None
    temperature: float = 0.2
    max_tokens: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GenerationResponse:
    """Normalized model response returned by the AI gateway."""

    text: str
    model: str
    provider: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    latency_ms: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
