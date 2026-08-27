"""Lightweight, dependency-free observability primitives."""

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


def start_request() -> RequestTelemetry:
    telemetry = RequestTelemetry()
    request_id_var.set(telemetry.request_id)
    return telemetry
