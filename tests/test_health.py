from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_architecture() -> None:
    response = client.get("/architecture")

    assert response.status_code == 200
    body = response.json()
    assert "llm-gateway" in body["capabilities"]
    assert "security-by-design" in body["principles"]
