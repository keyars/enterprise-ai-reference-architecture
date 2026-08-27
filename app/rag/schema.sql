CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS rag_chunks (
    id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    document_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    embedding vector(1536) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(tenant_id, document_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS rag_chunks_tenant_document_idx
    ON rag_chunks(tenant_id, document_id);

-- For larger collections, add an ANN index after measuring workload characteristics.
-- Example: CREATE INDEX ... USING hnsw (embedding vector_cosine_ops);
