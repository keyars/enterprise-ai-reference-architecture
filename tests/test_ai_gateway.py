from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_uses_normalized_response_contract() -> None:
    response = client.post("/ai/generate", json={"prompt": "Explain RAG in one sentence."})

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "local"
    assert payload["model"] == "local-deterministic"
    assert payload["text"]
    assert "usage" in payload
    assert payload["latency_ms"] is not None
