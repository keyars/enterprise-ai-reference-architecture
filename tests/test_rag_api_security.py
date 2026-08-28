from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rag_ingest_requires_tenant_header_match() -> None:
    response = client.post(
        "/rag/documents",
        headers={"X-Tenant-ID": "tenant-a"},
        json={
            "id": "api-doc",
            "title": "API Guide",
            "content": "Tenant scoped API document.",
            "tenant_id": "tenant-a",
        },
    )

    assert response.status_code == 201
    assert response.json()["document_id"] == "api-doc"


def test_rag_ingest_rejects_cross_tenant_document() -> None:
    response = client.post(
        "/rag/documents",
        headers={"X-Tenant-ID": "tenant-a"},
        json={
            "id": "cross-tenant-doc",
            "title": "Unauthorized",
            "content": "This document belongs to another tenant.",
            "tenant_id": "tenant-b",
        },
    )

    assert response.status_code == 403


def test_rag_query_uses_authenticated_tenant_context() -> None:
    response = client.post(
        "/rag/query",
        headers={"X-Tenant-ID": "tenant-a"},
        json={"question": "hello"},
    )

    assert response.status_code == 200
    sources = response.json()["sources"]
    assert all(source["chunk"]["tenant_id"] == "tenant-a" for source in sources)
