# Enterprise AI Reference Architecture

[![Status](https://img.shields.io/badge/status-architecture%20%26%20MVP-111827?style=for-the-badge)](https://github.com/keyars/enterprise-ai-reference-architecture)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue?style=for-the-badge)](LICENSE)

> **A production-oriented reference architecture for building secure, scalable, observable and cost-aware Enterprise AI applications with LLMs, Retrieval-Augmented Generation (RAG), AI Agents and enterprise data.**

## Why this project exists

Enterprise AI is moving beyond chat interfaces and isolated proofs of concept. Production systems need clear boundaries between applications, models, retrieval, tools, data, security, observability and business workflows.

This project provides a **working reference implementation** together with architecture decisions, security guidance, evaluation patterns and deployment guidance. It is designed for architects, CTOs, engineering leaders and developers who want practical patterns rather than a collection of disconnected AI demos.

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
                              │ Auth / RBAC / Limits │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │   AI Orchestrator    │
                              │ Intent / Plan / Run  │
                              └──────────┬───────────┘
                                         │
                  ┌──────────────────────┼──────────────────────┐
                  │                      │                      │
                  ▼                      ▼                      ▼
          ┌──────────────┐      ┌────────────────┐      ┌──────────────┐
          │     RAG      │      │  Agent Runtime │      │     Tools    │
          │ Retrieval    │      │ Planning/State │      │ APIs / Data  │
          └──────┬───────┘      └───────┬────────┘      └──────┬───────┘
                 │                      │                      │
                 └──────────────────────┼──────────────────────┘
                                        │
                              ┌─────────▼─────────┐
                              │   Model Gateway   │
                              │ Provider-neutral  │
                              └─────────┬─────────┘
                                        │
                         ┌──────────────┼──────────────┐
                         ▼              ▼              ▼
                     OpenAI         Anthropic      Local Models

                 Cross-cutting concerns:
                 Security · Evaluation · Observability · Cost

                 Data plane:
                 PostgreSQL · pgvector · Redis · Object Storage
```

## V1 scope

The first milestone deliberately focuses on a small, executable vertical slice:

- FastAPI service with health and architecture endpoints
- Configuration through environment variables
- Provider-neutral AI gateway boundary
- Clear separation between API, application and infrastructure concerns
- Testable foundation for RAG, agents, tools and observability
- Docker-ready local development
- Architecture documentation and ADRs

The following capabilities will be introduced incrementally rather than mocked prematurely:

1. LLM gateway
2. Document ingestion and RAG
3. Agent runtime and tool calling
4. Conversation and semantic memory
5. Authentication, RBAC and tenant isolation
6. AI observability and tracing
7. Evaluation datasets and automated quality checks
8. Cost accounting
9. AWS deployment reference

## Repository structure

```text
enterprise-ai-reference-architecture/
├── app/
│   ├── api/
│   ├── core/
│   ├── domain/
│   ├── infrastructure/
│   └── main.py
├── docs/
│   ├── architecture/
│   ├── adr/
│   ├── product-specification.md
│   └── roadmap.md
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
├── LICENSE
└── README.md
```

## Getting started

### Requirements

- Python 3.12+
- Git
- Docker (recommended for later milestones)

### Run locally

```bash
python -m venv .venv
source .venv/bin/activate

# Windows PowerShell:
# .venv\\Scripts\\Activate.ps1

pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

### Run tests

```bash
pytest
```

## Design principles

- **Provider-neutral:** application code should not be tightly coupled to one model vendor.
- **Security by design:** identity, authorization, data boundaries and tool permissions are architectural concerns.
- **Observable by default:** model calls, retrieval and tool execution must be measurable.
- **Evaluated, not assumed:** AI quality should be tested with repeatable evaluation datasets.
- **Cost-aware:** token usage, latency and model selection are operational concerns.
- **Incremental complexity:** introduce agents, distributed services and infrastructure only when the use case requires them.
- **Production over demo:** every major capability should have a path from local development to production deployment.

## Documentation

- [Product Specification](docs/product-specification.md)
- [Architecture](docs/architecture/README.md)
- [Roadmap](docs/roadmap.md)
- Architecture Decision Records will live under `docs/adr/`.

## Status

**Current milestone: V0.1 — executable architecture foundation.**

This repository is intentionally being built in public, with each milestone adding a working capability and the corresponding architecture documentation.

## Author

**Keyar Srinivasan** — Director & CTO, O Clock Software Pvt. Ltd.

Technology executive and product engineering leader focused on enterprise software, mobile platforms, cloud architecture, AI-enabled products and engineering systems.

---

<p align="center"><b>Enterprise AI · Software Architecture · AI Agents · RAG · Production Engineering</b></p>
