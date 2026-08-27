# Enterprise AI Reference Architecture

[![Status](https://img.shields.io/badge/status-V0.5.1%20%7C%20pgvector-111827?style=for-the-badge)](https://github.com/keyars/enterprise-ai-reference-architecture)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![RAG](https://img.shields.io/badge/RAG-Enterprise-111827?style=for-the-badge)](#enterprise-rag)
[![pgvector](https://img.shields.io/badge/PostgreSQL%20%2B%20pgvector-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://github.com/pgvector/pgvector)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue?style=for-the-badge)](LICENSE)

> **A production-oriented reference architecture for building secure, scalable, observable and cost-aware Enterprise AI applications with LLMs, RAG, AI Agents and enterprise data.**

## Purpose

This project is a working reference implementation for enterprise AI engineering. It focuses on explicit architecture boundaries between the API, model providers, embeddings, retrieval, vector persistence and future agent, security and observability layers.

The repository is being built incrementally. A capability is marked complete only when its implementation and corresponding tests exist; runtime verification is reported separately.

## Current Architecture

```text
Client
  │
  ▼
FastAPI
  │
  ├──────────────► AI Gateway ─────► Model Provider
  │
  ▼
RAG Service
  │
  ├── Document Chunking
  │
  ├── Embedding Provider
  │
  └── VectorStore
          │
          ├── In-Memory Store
          │
          └── PostgreSQL + pgvector
```

## Enterprise RAG

The RAG layer implements:

```text
Document
   ↓
Normalization
   ↓
Chunking + Metadata
   ↓
Embedding Provider
   ↓
VectorStore
   ↓
Cosine Similarity Retrieval
   ↓
Context Assembly
   ↓
AI Gateway
   ↓
Grounded Answer + Sources
```

### Implemented

- Document and chunk contracts
- Configurable chunking
- Embedding provider abstraction
- OpenAI embedding adapter
- Deterministic local embedding implementation for offline tests
- In-memory vector store
- PostgreSQL + pgvector adapter
- Persistent chunk upsert
- pgvector cosine-distance retrieval
- Embedding-dimension validation
- RAG orchestration
- Source metadata and similarity scores
- Document ingestion API
- RAG query API

## PostgreSQL + pgvector

The persistent adapter uses PostgreSQL with the `vector` extension and keeps persistence behind the `VectorStore` abstraction.

The official pgvector project documents Docker images for supported PostgreSQL major versions; this repository uses the `pgvector/pgvector:pg16` image for reproducible development and CI. citeturn0search0

### Start the database

```bash
docker compose up -d postgres
```

The database is available at:

```text
postgresql://postgres:postgres@localhost:5432/enterprise_ai
```

### Install PostgreSQL support

```bash
pip install -e ".[dev,postgres]"
```

### Run the PostgreSQL integration test

```bash
RUN_POSTGRES_INTEGRATION=1 \
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/enterprise_ai \
pytest tests/test_postgres_integration.py -q
```

The integration test creates the pgvector schema, writes real vectors, performs cosine-similarity retrieval and verifies the returned nearest chunk.

## API

### Health

```http
GET /health
```

### Generate

```http
POST /ai/generate
```

### Ingest a document

```http
POST /rag/documents
```

```json
{
  "id": "architecture-001",
  "title": "Enterprise Architecture Guide",
  "content": "Enterprise systems should establish clear boundaries between applications, services and data.",
  "metadata": {
    "department": "engineering"
  }
}
```

### Query RAG

```http
POST /rag/query
```

```json
{
  "question": "What should enterprise systems establish?",
  "top_k": 5,
  "temperature": 0.2
}
```

## Provider Architecture

The application remains provider-neutral:

```text
AI Gateway
    │
    └── ModelProvider
          ├── Local Provider
          └── OpenAI Provider
```

Embeddings follow the same pattern:

```text
EmbeddingProvider
    ├── Deterministic Local Provider
    └── OpenAI Embedding Provider
```

Vector persistence follows the same boundary:

```text
VectorStore
    ├── InMemoryVectorStore
    └── PostgresVectorStore
```

## Configuration

Copy `.env.example` to `.env`.

For real OpenAI execution:

```text
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-5.5
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TIMEOUT_SECONDS=30
```

For PostgreSQL:

```text
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/enterprise_ai
```

Never commit credentials or `.env` files.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Run the standard test suite:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

## CI

GitHub Actions now provisions a real PostgreSQL + pgvector service, installs the PostgreSQL dependency profile, runs Ruff, and then executes the test suite including the pgvector round-trip integration test.

A CI failure is treated as a failure — it is never described as passing until GitHub reports a successful run.

## Repository Status

| Milestone | Implementation | Runtime Verified |
|---|---|---|
| V0.1 Architecture Foundation | ✅ | 🟡 |
| V0.2 AI Gateway | ✅ | 🟡 |
| V0.3 OpenAI Provider | ✅ | 🟡 |
| V0.4 RAG Foundation | ✅ | 🟡 |
| V0.5 PostgreSQL + pgvector Adapter | ✅ | 🟡 |
| V0.5.1 Reproducible pgvector CI/Development | ✅ | 🟡 Pending current CI |

### Pending

- [ ] Agent runtime
- [ ] Controlled tool calling
- [ ] Agent state and memory
- [ ] Observability and tracing
- [ ] Token and cost accounting
- [ ] AI evaluation framework
- [ ] Authentication and RBAC
- [ ] Multi-tenancy
- [ ] Prompt-injection protections
- [ ] Sensitive-data controls
- [ ] Production migrations
- [ ] Full application Docker stack
- [ ] AWS deployment reference
- [ ] V1 production reference

## Documentation

- [Product Specification](docs/product-specification.md)
- [AI Gateway Architecture](docs/architecture/ai-gateway.md)
- [RAG Architecture](docs/architecture/rag.md)
- [PostgreSQL + pgvector Architecture](docs/architecture/pgvector.md)
- [Roadmap](docs/roadmap.md)

## Author

**Keyar Srinivasan** — Director & CTO, O Clock Software Pvt. Ltd.

Technology executive and product engineering leader focused on enterprise software, cloud architecture, AI-enabled products, mobile platforms and engineering systems.

---

<p align="center"><b>Enterprise AI · RAG · AI Agents · Software Architecture · Production Engineering</b></p>
