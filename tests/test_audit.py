from app.audit import clear, record_event, snapshot
from app.observability import request_id_var


def test_audit_event_captures_safe_context() -> None:
    clear()
    token = request_id_var.set("request-123")
    try:
        event = record_event(
            "DOCUMENT_QUERY",
            "success",
            subject="alice",
            tenant_id="tenant-a",
            resource="/rag/query",
        )
    finally:
        request_id_var.reset(token)

    assert event.request_id == "request-123"
    assert event.subject == "alice"
    assert event.tenant_id == "tenant-a"
    assert snapshot()[0]["action"] == "DOCUMENT_QUERY"


def test_audit_sink_is_bounded() -> None:
    clear()
    for index in range(1_005):
        record_event("TEST", "success", resource=str(index))
    events = snapshot()
    assert len(events) == 1_000
    assert events[0]["resource"] == "5"


def test_audit_does_not_store_request_body_or_credentials() -> None:
    clear()
    record_event("AUTHENTICATION", "failure", subject="anonymous", resource="/rag/query")
    event = snapshot()[0]
    assert "api_key" not in event
    assert "password" not in event
    assert "request_body" not in event
