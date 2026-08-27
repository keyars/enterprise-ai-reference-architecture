"""Provider usage and configurable cost estimation."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelPricing:
    input_per_million: float
    output_per_million: float


PRICING: dict[str, ModelPricing] = {
    "gpt-5.5": ModelPricing(1.25, 10.0),
    "text-embedding-3-small": ModelPricing(0.02, 0.0),
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float | None:
    pricing = PRICING.get(model)
    if pricing is None:
        return None
    return round(
        input_tokens / 1_000_000 * pricing.input_per_million
        + output_tokens / 1_000_000 * pricing.output_per_million,
        8,
    )
