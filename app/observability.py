"""Lightweight, dependency-free observability primitives."""

from collections import defaultdict
from contextvars import ContextVar
from dataclasses import dataclass, field
from time import perf_counter
from uuid import uuid4

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


@dataclass(slots=True)
class RequestTelemetry:
    request_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: float = field(default_factory=perf_counter)
    attributes: dict[str, str] = field(default_factory=dict)

    @property
    def latency_ms(self) -> float:
        return round((perf_counter() - self.started_at) * 1000, 2)


@dataclass(slots=True)
class Metrics:
    """Process-local counters for reference deployments and diagnostics."""

    requests_total: int = 0
    requests_failed: int = 0
    llm_requests_total: int = 0
    input_tokens_total: int = 0
    output_tokens_total: int = 0
    request_latency_ms_total: float = 0.0
    llm_latency_ms_total: float = 0.0
    by_route: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    by_provider: dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def record_request(self, route: str, latency_ms: float, failed: bool) -> None:
        self.requests_total += 1
        self.requests_failed += int(failed)
        self.request_latency_ms_total += latency_ms
        self.by_route[route] += 1

    def record_llm(self, provider: str, input_tokens: int, output_tokens: int, latency_ms: float) -> None:
        self.llm_requests_total += 1
        self.input_tokens_total += input_tokens
        self.output_tokens_total += output_tokens
        self.llm_latency_ms_total += latency_ms
        self.by_provider[provider] += 1

    def snapshot(self) -> dict[str, object]:
        return {
            "requests_total": self.requests_total,
            "requests_failed": self.requests_failed,
            "llm_requests_total": self.llm_requests_total,
            "input_tokens_total": self.input_tokens_total,
            "output_tokens_total": self.output_tokens_total,
            "request_latency_ms_total": round(self.request_latency_ms_total, 2),
            "llm_latency_ms_total": round(self.llm_latency_ms_total, 2),
            "by_route": dict(self.by_route),
            "by_provider": dict(self.by_provider),
        }


metrics = Metrics()


def start_request() -> RequestTelemetry:
    telemetry = RequestTelemetry()
    request_id_var.set(telemetry.request_id)
    return telemetry
