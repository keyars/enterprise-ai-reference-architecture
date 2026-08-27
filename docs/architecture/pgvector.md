# PostgreSQL + pgvector Persistence

## Purpose

V0.5 adds a persistent vector-store adapter while keeping the RAG application layer independent of its storage implementation.

```text
RAGService
    |
    v
VectorStore interface
    |
    +--> InMemoryVectorStore   (tests / offline)
    |
    +--> PostgresVectorStore   (persistent)
                                  |
                                  v
                         PostgreSQL + pgvector
```

## Data model

Each indexed chunk stores:

- stable chunk ID
- document ID
- chunk index
- source text
- JSON metadata
- embedding vector
- creation timestamp

The `(document_id, chunk_index)` pair is unique so a document can be re-indexed without producing duplicate positions.

## Retrieval

The adapter uses pgvector's cosine-distance operator (`<=>`) and converts distance to cosine similarity with `1 - distance` for the API's normalized search result.

The application controls `top_k`, while the database performs ordering and limiting.

## Embedding dimensions

The database vector dimension must exactly match the configured embedding model. The adapter validates dimensions during writes and reads to fail early rather than silently corrupting retrieval quality.

## Production considerations

- Use connection pooling.
- Keep database credentials in environment/secret management.
- Add migrations rather than modifying production schemas ad hoc.
- Measure query performance before choosing HNSW/IVFFlat indexes and their parameters.
- Apply tenant/document authorization filters at the database query boundary when multi-tenancy is introduced.
- Store document/version metadata needed for source traceability.

## Local development

A later Docker milestone will provide a complete PostgreSQL + pgvector service. The current adapter can already target any PostgreSQL instance where the `vector` extension is installed.
