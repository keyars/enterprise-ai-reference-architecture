from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["X-Request-ID"]


def test_architecture() -> None:
    response = client.get("/architecture")

    assert response.status_code == 200
    body = response.json()
    assert "llm-gateway" in body["capabilities"]
    assert "security-by-design" in body["principles"]
    assert "request-tracing" in body["capabilities"]


def test_metrics_reports_requests_without_sensitive_content() -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    body = response.json()
    assert body["requests_total"] >= 1
    assert "/health" in body["by_route"] or "/architecture" in body["by_route"]
    assert "api_key" not in body
