import pytest

from app.rag.models import DocumentChunk
from app.rag.postgres import PostgresVectorStore


@pytest.mark.asyncio
async def test_postgres_store_requires_initialization() -> None:
    store = PostgresVectorStore("postgresql://example", dimensions=3)
    chunk = DocumentChunk(
        id="chunk-1",
        document_id="doc-1",
        text="hello",
        chunk_index=0,
        embedding=[1.0, 0.0, 0.0],
    )

    with pytest.raises(RuntimeError, match="initialize"):
        await store.upsert([chunk])


@pytest.mark.asyncio
async def test_postgres_store_validates_dimensions_before_database_access() -> None:
    store = PostgresVectorStore("postgresql://example", dimensions=3)
    store.pool = object()

    chunk = DocumentChunk(
        id="chunk-1",
        document_id="doc-1",
        text="hello",
        chunk_index=0,
        embedding=[1.0, 0.0],
    )

    with pytest.raises(ValueError, match="dimension"):
        await store.upsert([chunk])
