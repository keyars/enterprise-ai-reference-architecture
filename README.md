# Enterprise AI Reference Architecture

[![Status](https://img.shields.io/badge/status-V0.4%20%7C%20Enterprise%20RAG-111827?style=for-the-badge)](https://github.com/keyars/enterprise-ai-reference-architecture)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Responses%20API-412991?style=for-the-badge&logo=openai&logoColor=white)](https://platform.openai.com/)
[![RAG](https://img.shields.io/badge/RAG-Enterprise%20Reference-111827?style=for-the-badge)](#enterprise-rag)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue?style=for-the-badge)](LICENSE)

> **A production-oriented reference architecture for building secure, scalable, observable and cost-aware Enterprise AI applications with LLMs, Retrieval-Augmented Generation (RAG), AI Agents and enterprise data.**

## Why this project exists

Enterprise AI is moving beyond chat interfaces and isolated proofs of concept. Production systems need clear boundaries between applications, models, retrieval, tools, data, security, observability and business workflows.

This project provides a **working reference implementation** together with architecture decisions, security guidance, evaluation patterns and deployment guidance. It is designed for CTOs, architects, engineering leaders and developers who want practical patterns rather than disconnected AI demos.

## Architecture

```text
                              ┌──────────────────────┐
                              │        Client        │
                              │ Web / API / Service  │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │      API Layer       │
                              │ Validation / Limits  │
                              └──────────┬───────────┘
                                         │
                              ┌──────────▼───────────┐
                              │   RAG Orchestrator   │
                              │ Retrieve → Context   │
                              └──────┬─────────┬─────┘
                                     │         │
                                     ▼         ▼
                              ┌──────────┐  ┌─────────────┐
                              │ Embedding│  │ AI Gateway  │
                              │ Provider │  │ Model Layer │
                              └────┬─────┘  └──────┬──────┘
                                   │               │
                                   ▼               ▼
                              ┌──────────┐    ┌──────────┐
                              │  Vector  │    │   LLM    │
                              │  Store   │    │ Provider │
                              └──────────┘    └──────────┘

                    Cross-cutting concerns:
                    Security · Evaluation · Observability · Cost
```

## Enterprise RAG

V0.4 introduces a complete retrieval-augmented generation pipeline that can run without external services for development and tests, while providing an adapter for production OpenAI embeddings.

```text
Document
   ↓
Normalization
   ↓
Chunking + Metadata
   ↓
Embedding Provider
   ↓
Vector Store
   ↓
Semantic Retrieval
   ↓
Context Assembly
   ↓
AI Gateway
   ↓
Grounded Answer + Sources
```

### Current RAG capabilities

- Deterministic document normalization and chunking
- Configurable chunk size and overlap
- Embedding provider abstraction
- OpenAI embedding adapter
- Deterministic local embeddings for offline development and tests
- In-memory vector store using cosine similarity
- Grounded prompt construction
- Source metadata and retrieval scores in API responses
- Document ingestion endpoint
- RAG query endpoint
- Automated RAG tests without an API key

The in-memory vector store is intentionally a development/test implementation. PostgreSQL + pgvector is planned for the persistent production reference.

## API

### Generate with an LLM

```http
POST /ai/generate
Content-Type: application/json
```

### Ingest a document

```http
POST /rag/documents
Content-Type: application/json
```

Example:

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

### Query the knowledge base

```http
POST /rag/query
Content-Type: application/json
```

Example:

```json
{
  "question": "What should enterprise systems establish?",
  "top_k": 5,
  "temperature": 0.2
}
```

The response contains the generated answer plus the retrieved source chunks and similarity scores.

## Provider architecture

The application remains provider-neutral:

```text
                         AI Gateway
                              │
                       ModelProvider
                              │
                ┌─────────────┼─────────────┐
                │             │             │
              Local        OpenAI       Future Provider
```

The same principle applies to embeddings:

```text
                     EmbeddingProvider
                              │
                 ┌────────────┴────────────┐
                 │                         │
              Local                     OpenAI
          deterministic demo           embeddings
```

## Configuration

Copy `.env.example` to `.env`.

For a real OpenAI-backed run:

```text
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-5.5
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TIMEOUT_SECONDS=30
```

Without an API key, the local LLM and deterministic embedding implementations keep the RAG flow runnable for development and automated testing.

**Never commit `.env` or API credentials to source control.**

## Getting started

### Requirements

- Python 3.12+
- Git
- OpenAI API key for real model and embedding execution (optional for local development)

### Install

```bash
python -m venv .venv
source .venv/bin/activate

# Windows PowerShell:
# .venv\\Scripts\\Activate.ps1

pip install -e ".[dev]"
```

### Run

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

### Test

```bash
pytest
```

### Lint

```bash
ruff check .
```

## Roadmap

- [x] V0.1 — Architecture foundation
- [x] V0.2 — Provider-neutral AI Gateway
- [x] V0.3 — OpenAI provider integration
- [x] V0.4 — RAG pipeline foundation
- [ ] V0.5 — PostgreSQL + pgvector persistence
- [ ] V0.6 — Agent runtime and controlled tool calling
- [ ] V0.7 — Observability, tracing and AI evaluation
- [ ] V0.8 — Authentication, RBAC and multi-tenancy
- [ ] V0.9 — Security and AI guardrails
- [ ] V1.0 — Production deployment reference and AWS architecture

## Design principles

- **Provider-neutral:** business logic should not be tightly coupled to one model vendor.
- **Security by design:** identity, authorization, data boundaries and tool permissions are architectural concerns.
- **Observable by default:** model calls, retrieval and tool execution must be measurable.
- **Evaluated, not assumed:** AI quality should be tested with repeatable datasets.
- **Cost-aware:** token usage, latency and model selection are operational concerns.
- **Incremental complexity:** introduce distributed services and infrastructure only when justified.
- **Production over demo:** every major capability should have a path from local development to production.

## Repository structure

```text
enterprise-ai-reference-architecture/
├── app/
│   ├── ai/
│   │   ├── gateway.py
│   │   ├── models.py
│   │   └── providers/
│   │       ├── base.py
│   │       ├── local.py
│   │       └── openai.py
│   ├── api/
│   │   ├── ai.py
│   │   └── rag.py
│   ├── core/
│   │   └── config.py
│   ├── rag/
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── models.py
│   │   ├── service.py
│   │   └── store.py
│   └── main.py
├── docs/
│   ├── architecture/
│   │   ├── ai-gateway.md
│   │   └── rag.md
│   ├── adr/
│   ├── product-specification.md
│   └── roadmap.md
├── tests/
│   ├── test_ai_gateway.py
│   ├── test_openai_provider.py
│   └── test_rag.py
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
├── LICENSE
└── README.md
```

## Documentation

- [Product Specification](docs/product-specification.md)
- [AI Gateway Architecture](docs/architecture/ai-gateway.md)
- [RAG Architecture](docs/architecture/rag.md)
- [Roadmap](docs/roadmap.md)
- Architecture Decision Records: `docs/adr/`

## Author

**Keyar Srinivasan** — Director & CTO, O Clock Software Pvt. Ltd.

Technology executive and product engineering leader focused on enterprise software, mobile platforms, cloud architecture, AI-enabled products and engineering systems.

---

<p align="center"><b>Enterprise AI · RAG · AI Agents · Software Architecture · Production Engineering</b></p>
