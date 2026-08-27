import pytest

from app.rag.models import DocumentChunk
from app.rag.postgres import PostgresVectorStore


def make_chunk(embedding: list[float]) -> DocumentChunk:
    return DocumentChunk(
        id="chunk-1",
        tenant_id="tenant-a",
        document_id="doc-1",
        text="hello",
        chunk_index=0,
        embedding=embedding,
    )


@pytest.mark.asyncio
async def test_postgres_store_requires_initialization() -> None:
    store = PostgresVectorStore("postgresql://example", dimensions=3)

    with pytest.raises(RuntimeError, match="initialize"):
        await store.upsert([make_chunk([1.0, 0.0, 0.0])])


@pytest.mark.asyncio
async def test_postgres_store_validates_dimensions_before_database_access() -> None:
    store = PostgresVectorStore("postgresql://example", dimensions=3)
    store.pool = object()

    with pytest.raises(ValueError, match="dimension"):
        await store.upsert([make_chunk([1.0, 0.0])])


@pytest.mark.asyncio
async def test_postgres_store_requires_tenant_for_search() -> None:
    store = PostgresVectorStore("postgresql://example", dimensions=3)
    store.pool = object()

    with pytest.raises(ValueError, match="tenant_id"):
        await store.search([1.0, 0.0, 0.0])
