"""Minimal, non-sensitive audit event sink for the reference application."""

from dataclasses import asdict, dataclass
from time import time
from typing import Any

from app.observability import request_id_var


@dataclass(frozen=True, slots=True)
class AuditEvent:
    action: str
    outcome: str
    subject: str = "anonymous"
    tenant_id: str = "-"
    resource: str = "-"
    request_id: str = "-"
    timestamp: float = 0.0


_events: list[AuditEvent] = []
_MAX_EVENTS = 1_000


def record_event(
    action: str,
    outcome: str,
    *,
    subject: str = "anonymous",
    tenant_id: str = "-",
    resource: str = "-",
) -> AuditEvent:
    event = AuditEvent(
        action=action,
        outcome=outcome,
        subject=subject,
        tenant_id=tenant_id,
        resource=resource,
        request_id=request_id_var.get(),
        timestamp=time(),
    )
    _events.append(event)
    if len(_events) > _MAX_EVENTS:
        del _events[: len(_events) - _MAX_EVENTS]
    return event


def snapshot() -> list[dict[str, Any]]:
    """Return audit metadata without request bodies, credentials or secrets."""
    return [asdict(event) for event in _events]


def clear() -> None:
    _events.clear()
