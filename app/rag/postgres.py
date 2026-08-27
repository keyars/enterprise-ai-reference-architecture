"""Persistent PostgreSQL/pgvector store.

This adapter keeps persistence concerns behind the VectorStore abstraction.
It requires PostgreSQL with the pgvector extension and the asyncpg driver.
"""

import json
from collections.abc import Sequence

from app.rag.models import DocumentChunk, SearchResult
from app.rag.store import VectorStore


class PostgresVectorStore(VectorStore):
    """PostgreSQL vector store backed by pgvector.

    The embedding dimension is configurable, but must match the embedding model
    used by the application. The schema is created explicitly by the application
    rather than relying on an ORM migration magic layer.
    """

    def __init__(self, database_url: str, dimensions: int) -> None:
        self.database_url = database_url
        self.dimensions = dimensions

    async def initialize(self) -> None:
        import asyncpg

        self.pool = await asyncpg.create_pool(self.database_url)
        async with self.pool.acquire() as connection:
            await connection.execute("CREATE EXTENSION IF NOT EXISTS vector")
            await connection.execute(
                f"""
                CREATE TABLE IF NOT EXISTS rag_chunks (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    metadata JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                    embedding vector({self.dimensions}) NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    UNIQUE(document_id, chunk_index)
                )
                """
            )
            await connection.execute(
                "CREATE INDEX IF NOT EXISTS rag_chunks_document_idx ON rag_chunks(document_id)"
            )

    async def upsert(self, chunks: Sequence[DocumentChunk]) -> None:
        if not chunks:
            return
        if not hasattr(self, "pool"):
            raise RuntimeError("PostgresVectorStore.initialize() must be called first")
        for chunk in chunks:
            if len(chunk.embedding) != self.dimensions:
                raise ValueError(
                    f"Embedding dimension {len(chunk.embedding)} does not match "
                    f"configured dimension {self.dimensions}"
                )

        async with self.pool.acquire() as connection, connection.transaction():
            for chunk in chunks:
                await connection.execute(
                    """
                    INSERT INTO rag_chunks
                        (id, document_id, chunk_index, text, metadata, embedding)
                    VALUES ($1, $2, $3, $4, $5::jsonb, $6::vector)
                    ON CONFLICT (id) DO UPDATE SET
                        document_id = EXCLUDED.document_id,
                        chunk_index = EXCLUDED.chunk_index,
                        text = EXCLUDED.text,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding
                    """,
                    chunk.id,
                    chunk.document_id,
                    chunk.chunk_index,
                    chunk.text,
                    json.dumps(chunk.metadata),
                    _vector_literal(chunk.embedding),
                )

    async def search(self, embedding: Sequence[float], top_k: int = 5) -> list[SearchResult]:
        if top_k <= 0:
            return []
        if not hasattr(self, "pool"):
            raise RuntimeError("PostgresVectorStore.initialize() must be called first")
        if len(embedding) != self.dimensions:
            raise ValueError(
                f"Embedding dimension {len(embedding)} does not match configured dimension {self.dimensions}"
            )

        async with self.pool.acquire() as connection:
            rows = await connection.fetch(
                """
                SELECT id, document_id, chunk_index, text, metadata,
                       1 - (embedding <=> $1::vector) AS score
                FROM rag_chunks
                ORDER BY embedding <=> $1::vector
                LIMIT $2
                """,
                _vector_literal(embedding),
                top_k,
            )

        return [
            SearchResult(
                chunk=DocumentChunk(
                    id=row["id"],
                    document_id=row["document_id"],
                    chunk_index=row["chunk_index"],
                    text=row["text"],
                    metadata=_decode_metadata(row["metadata"]),
                ),
                score=float(row["score"]),
            )
            for row in rows
        ]

    async def close(self) -> None:
        if hasattr(self, "pool"):
            await self.pool.close()


def _decode_metadata(value: object) -> dict:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        parsed = json.loads(value)
        if isinstance(parsed, dict):
            return parsed
    raise TypeError("Stored metadata must decode to a JSON object")


def _vector_literal(values: Sequence[float]) -> str:
    return "[" + ",".join(str(float(value)) for value in values) + "]"
