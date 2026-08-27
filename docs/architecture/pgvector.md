# PostgreSQL + pgvector Persistence

## Purpose

V0.5 introduced a persistent vector-store adapter while keeping the RAG application layer independent of its storage implementation. V0.5.1 adds a reproducible PostgreSQL + pgvector development service and a real CI integration test.

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

The application controls `top_k`, while PostgreSQL performs ordering and limiting.

## Embedding dimensions

The database vector dimension must exactly match the configured embedding model. The adapter validates dimensions during writes and reads to fail early rather than silently corrupting retrieval quality.

## Reproducible development

The repository provides `docker-compose.yml` with the official pgvector Docker image for PostgreSQL 16:

```bash
docker compose up -d postgres
```

The pgvector project documents the `pgvector/pgvector` image family and PostgreSQL-version-specific tags. citeturn0search0

The default local connection is:

```text
postgresql://postgres:postgres@localhost:5432/enterprise_ai
```

Install the optional driver profile:

```bash
pip install -e ".[dev,postgres]"
```

Run the real integration test with:

```bash
RUN_POSTGRES_INTEGRATION=1 \
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/enterprise_ai \
pytest tests/test_postgres_integration.py -q
```

The test creates the extension/schema, writes vectors, performs a nearest-neighbour search and verifies the expected result.

## Production considerations

- Use connection pooling.
- Keep database credentials in environment/secret management.
- Use a migration system before production deployment.
- Measure query performance before choosing HNSW/IVFFlat indexes and their parameters.
- Apply tenant/document authorization filters at the database query boundary when multi-tenancy is introduced.
- Store document/version metadata needed for source traceability.
- Validate that the configured embedding dimension matches the persisted vector schema during deployment.
