"""Provider usage and caller-supplied cost estimation.

Prices intentionally are not hard-coded because provider pricing changes.
Production deployments should load an approved pricing catalogue/configuration.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelPricing:
    input_per_million: float
    output_per_million: float


def estimate_cost(
    pricing: ModelPricing,
    input_tokens: int,
    output_tokens: int,
) -> float:
    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("Token counts cannot be negative")
    return round(
        input_tokens / 1_000_000 * pricing.input_per_million
        + output_tokens / 1_000_000 * pricing.output_per_million,
        8,
    )
