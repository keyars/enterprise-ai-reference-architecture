from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["X-Request-ID"]


def test_readiness_endpoint() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_metrics_endpoint_is_non_sensitive() -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    body = response.json()
    assert "requests_total" in body
    assert "input_tokens_total" in body
    assert "api_key" not in str(body).lower()


def test_audit_endpoint_excludes_credentials() -> None:
    response = client.get("/audit")
    assert response.status_code == 200
    assert "secret" not in response.text.lower()
    assert "authorization" not in response.text.lower()
