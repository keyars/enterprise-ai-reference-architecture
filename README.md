# Enterprise AI Reference Architecture

[![CI](https://github.com/keyars/enterprise-ai-reference-architecture/actions/workflows/ci.yml/badge.svg)](https://github.com/keyars/enterprise-ai-reference-architecture/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![pgvector](https://img.shields.io/badge/pgvector-enabled-336791?style=flat-square)](https://github.com/pgvector/pgvector)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue?style=flat-square)](LICENSE)

> **A production-oriented reference architecture for building secure, scalable, observable and cost-aware Enterprise AI applications with LLMs, Retrieval-Augmented Generation (RAG), AI Agents and enterprise data.**

This repository is a **working software architecture reference**, not a collection of isolated AI demos. It demonstrates how an enterprise AI platform can separate model providers, retrieval, persistence, agent execution, tools, security boundaries and operational concerns so that individual capabilities can evolve without tightly coupling the application to one implementation.

## Why this project exists

Enterprise AI systems need considerably more than an LLM call. A production architecture must account for:

- model-provider abstraction
- retrieval and grounded generation
- persistent enterprise knowledge
- controlled tool execution
- authentication and authorization boundaries
- observability and operational telemetry
- evaluation and quality measurement
- cost management
- security and data isolation
- repeatable deployment

The project builds these concerns incrementally, with executable code, automated tests and architecture documentation for each major milestone.

## Architecture

```text
                              ┌──────────────────────┐
                              │       Clients        │
                              │ Web / API / Service  │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │      API Layer       │
                              │ Validation / Policy  │
                              └──────────┬───────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         │                               │
                         ▼                               ▼
                 ┌───────────────┐              ┌────────────────┐
                 │   AI Gateway  │              │  Agent Runtime │
                 │ Provider-neutral│            │ Bounded / Safe │
                 └───────┬───────┘              └───────┬────────┘
                         │                               │
             ┌───────────┼───────────┐             ┌────┴─────┐
             │           │           │             │          │
             ▼           ▼           ▼             ▼          ▼
          OpenAI       Local     Future       Tool Registry  RAG
          Provider    Provider   Providers       │            │
                                                  │            │
                                                  ▼            ▼
                                            Authorized     Retrieval
                                              Tools        Pipeline
                                                               │
                                                               ▼
                                                       PostgreSQL
                                                         + pgvector

                         Cross-cutting concerns
              Security · Evaluation · Observability · Cost
```

## Current implementation

### AI Gateway

- Provider-neutral model interface
- Local deterministic provider for offline development
- OpenAI provider adapter
- Typed generation contracts
- Configurable model and generation parameters
- Normalized usage information
- Latency measurement

### Retrieval-Augmented Generation

- Document and chunk domain models
- Deterministic overlapping text chunking
- Embedding provider abstraction
- Local deterministic embeddings for offline tests
- OpenAI embedding provider
- Vector-store abstraction
- In-memory vector store
- PostgreSQL + pgvector vector store
- Cosine-similarity retrieval
- Source metadata propagation
- RAG orchestration

### Agent Runtime

- Bounded execution loop
- Native structured tool-calling boundary
- Explicit tool registry
- Per-request tool allowlist
- Tool authorization checks
- Tool argument validation
- Bounded tool output
- Agent execution trace
- Deterministic runtime tests

### Persistence and infrastructure

- PostgreSQL 16 development environment
- pgvector extension
- Async connection pooling
- Persistent RAG chunk storage
- Docker Compose development infrastructure
- GitHub Actions CI
- Ruff linting
- Automated unit and integration tests

## Request flows

### Standard AI generation

```text
Client
  ↓
FastAPI
  ↓
AI Gateway
  ↓
ModelProvider
  ↓
OpenAI / Local Provider
  ↓
Normalized Response
```

### Enterprise RAG

```text
Document
  ↓
Normalize
  ↓
Chunk
  ↓
Embed
  ↓
PostgreSQL + pgvector
  ↓
Semantic Retrieval
  ↓
Context Assembly
  ↓
AI Gateway
  ↓
LLM
  ↓
Grounded Answer + Sources
```

### Controlled agent execution

```text
User Request
     ↓
Agent Runtime
     ↓
Model
     ↓
Tool Request
     ↓
Authorization
     ↓
Argument Validation
     ↓
Tool Execution
     ↓
Bounded Output
     ↓
Model Continuation
     ↓
Final Response
```

## Technology stack

| Area | Technology |
|---|---|
| Language | Python 3.12+ |
| API | FastAPI |
| Validation | Pydantic / Pydantic Settings |
| LLM integration | OpenAI API + provider abstraction |
| RAG | Custom retrieval pipeline |
| Database | PostgreSQL 16 |
| Vector search | pgvector |
| PostgreSQL driver | asyncpg |
| Local infrastructure | Docker Compose |
| Testing | pytest + pytest-asyncio |
| Code quality | Ruff |
| CI | GitHub Actions |

## Repository structure

```text
enterprise-ai-reference-architecture/
├── app/
│   ├── agents/
│   │   ├── default_tools.py
│   │   └── runtime.py
│   ├── ai/
│   │   ├── gateway.py
│   │   ├── models.py
│   │   ├── tools.py
│   │   └── providers/
│   │       ├── base.py
│   │       ├── local.py
│   │       └── openai.py
│   ├── api/
│   ├── core/
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── models.py
│   │   ├── postgres.py
│   │   ├── schema.sql
│   │   ├── service.py
│   │   └── store.py
│   └── main.py
├── docs/
│   ├── architecture/
│   ├── adr/
│   ├── product-specification.md
│   └── roadmap.md
├── tests/
├── .env.example
├── .github/workflows/ci.yml
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── pyproject.toml
└── README.md
```

## Getting started

### Requirements

- Python 3.12+
- Git
- Docker Desktop or Docker Engine + Compose

### Install the project

```bash
python -m venv .venv
source .venv/bin/activate

# Windows PowerShell:
# .venv\Scripts\Activate.ps1

pip install -e ".[dev,postgres]"
```

### Configure environment

Copy `.env.example` to `.env` and provide the values required for the capability you want to run.

**Never commit API keys or other secrets.**

### Run the API

```bash
uvicorn app.main:app --reload
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### Start PostgreSQL + pgvector

```bash
docker compose up -d postgres
```

The repository's PostgreSQL adapter expects the `vector` extension to be available.

### Run tests

```bash
pytest
```

The PostgreSQL integration test is executed when the CI environment sets `RUN_POSTGRES_INTEGRATION=1` and supplies `DATABASE_URL`.

### Run linting

```bash
ruff check .
```

## API surface

The current application exposes the foundational service endpoints and AI/RAG capabilities implemented in the repository. Use the generated OpenAPI documentation at `/docs` as the authoritative interactive API contract for the current checkout.

## Design principles

### 1. Provider independence

Business/application code should depend on an internal model-provider contract rather than vendor-specific SDK calls.

### 2. Explicit boundaries

AI generation, retrieval, tools, persistence and infrastructure remain separate concerns with explicit interfaces between them.

### 3. Security by design

Authorization must be enforced by the application rather than delegated to the model. Tool access is explicitly allowlisted and arguments are validated before execution.

### 4. Bounded autonomy

Agent execution is deliberately bounded by a maximum step count and controlled tool permissions. The model is not given unrestricted authority over the host application.

### 5. Observable systems

AI applications must expose enough operational information to understand latency, usage, retrieval behavior, tool execution and failures.

### 6. Evaluated systems

AI quality should be measured using repeatable evaluation datasets rather than inferred from a small number of successful demonstrations.

### 7. Incremental complexity

Distributed systems, autonomous agents and infrastructure should be introduced because the use case requires them—not simply because the technology is available.

## Security model — current and planned

Current implementation includes explicit tool authorization, argument validation, bounded agent execution and bounded tool output.

The following are intentionally **not yet represented as completed production controls**:

- authentication
- role-based access control
- tenant isolation
- production secret management
- prompt-injection defense system
- data-loss prevention controls
- comprehensive audit logging

These remain on the roadmap and will be implemented as dedicated milestones rather than described as already solved.

## Roadmap

```text
V0.1  Architecture Foundation                 ✅
V0.2  Provider-Neutral AI Gateway             ✅
V0.3  Real LLM Provider                       ✅
V0.4  RAG Foundation                          ✅
V0.5  PostgreSQL + pgvector                   ✅
V0.5.1 Docker + pgvector CI                   ✅
V0.6  Agent Runtime + Tool Calling            ✅
V0.7  Observability + Cost Intelligence       ⏳
V0.8  AI Evaluation Framework                 ⏳
V0.9  Security + Authentication + RBAC        ⏳
V0.10 Multi-tenancy + Data Isolation          ⏳
V0.11 Production Deployment / AWS             ⏳
V1.0  Production Reference Architecture       ⏳
```

### Verification policy

A milestone is only considered **runtime verified** when the relevant automated tests or deployment checks have actually executed successfully.

> **Implemented ≠ Runtime Verified ≠ Production Ready**

This distinction is intentionally maintained throughout the project.

## Documentation

- [Product Specification](docs/product-specification.md)
- [Roadmap](docs/roadmap.md)
- [Architecture Documentation](docs/architecture/README.md)
- [PostgreSQL + pgvector Architecture](docs/architecture/pgvector.md)

Architecture Decision Records will be maintained under `docs/adr/` as architectural decisions are introduced.

## Contributing

Contributions, architectural discussions and improvements are welcome. Please read `CONTRIBUTING.md` before submitting changes.

## License

This project is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) for details.

## Author

**Keyar Srinivasan**  
Director & CTO, O Clock Software Pvt. Ltd.

Technology executive and product engineering leader focused on enterprise software, mobile platforms, cloud architecture, AI-enabled products and engineering systems.

---

<p align="center">
  <strong>Enterprise AI · Software Architecture · LLMs · RAG · AI Agents · Production Engineering</strong>
</p>
