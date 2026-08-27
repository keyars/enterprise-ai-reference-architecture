import os

import pytest

from app.rag.models import DocumentChunk
from app.rag.postgres import PostgresVectorStore

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_POSTGRES_INTEGRATION") != "1",
    reason="PostgreSQL integration tests require RUN_POSTGRES_INTEGRATION=1",
)


@pytest.mark.asyncio
async def test_pgvector_round_trip() -> None:
    database_url = os.environ["DATABASE_URL"]
    store = PostgresVectorStore(database_url, dimensions=3)
    await store.initialize()

    document_id = "integration-doc"
    tenant_id = "tenant-a"
    chunks = [
        DocumentChunk(
            id="integration-chunk-1",
            tenant_id=tenant_id,
            document_id=document_id,
            text="enterprise architecture",
            chunk_index=0,
            metadata={"title": "Architecture"},
            embedding=[1.0, 0.0, 0.0],
        ),
        DocumentChunk(
            id="integration-chunk-2",
            tenant_id=tenant_id,
            document_id=document_id,
            text="database operations",
            chunk_index=1,
            metadata={"title": "Database"},
            embedding=[0.0, 1.0, 0.0],
        ),
    ]

    try:
        await store.upsert(chunks)
        results = await store.search([0.95, 0.05, 0.0], top_k=1, tenant_id=tenant_id)

        assert len(results) == 1
        assert results[0].chunk.id == "integration-chunk-1"
        assert results[0].chunk.tenant_id == tenant_id
        assert results[0].score > 0.9

        isolated = await store.search([0.95, 0.05, 0.0], top_k=5, tenant_id="tenant-b")
        assert isolated == []
    finally:
        async with store.pool.acquire() as connection:
            await connection.execute("DELETE FROM rag_chunks WHERE document_id = $1", document_id)
        await store.close()
