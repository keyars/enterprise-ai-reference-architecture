# Enterprise AI Reference Architecture

[![Status](https://img.shields.io/badge/status-V0.3%20%7C%20LLM%20Provider-111827?style=for-the-badge)](https://github.com/keyars/enterprise-ai-reference-architecture)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Responses%20API-412991?style=for-the-badge&logo=openai&logoColor=white)](https://platform.openai.com/)
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

## Current implementation

### V0.1 — Architecture foundation

- FastAPI service
- Health endpoint
- Architecture metadata endpoint
- Configuration foundation
- Testable project structure

### V0.2 — Provider-neutral AI Gateway

- `ModelProvider` abstraction
- Normalized generation request/response contracts
- Deterministic local provider
- AI gateway latency measurement
- Automated gateway tests

### V0.3 — OpenAI Provider

The gateway now supports a real OpenAI adapter while preserving the provider-neutral application boundary.

```text
Application
     │
     ▼
 AI Gateway
     │
     ▼
ModelProvider
     │
     ├───────────────┐
     ▼               ▼
 Local           OpenAI
 Provider        Provider
```

When `OPENAI_API_KEY` is configured, `/ai/generate` uses the OpenAI provider. Without credentials, the same endpoint remains runnable through the deterministic local provider.

The OpenAI adapter uses the official Python SDK and the Responses API, and normalizes model output and token usage into the repository's internal response contract. citeturn0search7turn0search10

## API

### Generate

```http
POST /ai/generate
Content-Type: application/json
```

Example:

```json
{
  "prompt": "Explain Retrieval-Augmented Generation in one paragraph.",
  "temperature": 0.2
}
```

The response is normalized regardless of the underlying provider:

```json
{
  "text": "...",
  "provider": "openai",
  "model": "gpt-5.5",
  "usage": {
    "input_tokens": 42,
    "output_tokens": 96,
    "total_tokens": 138
  },
  "latency_ms": 742.31
}
```

## Configuration

Copy `.env.example` to `.env` and provide an API key only when you want to use the OpenAI provider.

```text
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-5.5
OPENAI_TIMEOUT_SECONDS=30
```

**Never commit `.env` or API credentials to source control.**

The repository deliberately keeps provider configuration outside application business logic.

## Getting started

### Requirements

- Python 3.12+
- Git
- An OpenAI API key for real model execution (optional; local provider works without one)

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

The OpenAI provider test uses a mocked SDK response, so tests do not require network access or an API key.

## V1 roadmap

1. **V0.4 — Enterprise RAG**
   - document ingestion
   - parsing and chunking
   - embeddings
   - PostgreSQL + pgvector
   - retrieval pipeline
   - source citations

2. **V0.5 — Agent Runtime**
   - tool contracts
   - planning
   - controlled tool execution
   - agent state
   - workflow boundaries

3. **V0.6 — Observability & Evaluation**
   - tracing
   - token/cost accounting
   - evaluation datasets
   - retrieval and answer quality metrics

4. **V0.7 — Security & Multi-tenancy**
   - authentication
   - RBAC
   - tenant isolation
   - prompt/data security

5. **V1.0 — Production Reference Architecture**
   - Docker deployment
   - AWS reference architecture
   - operational guidance
   - production readiness checklist

## Design principles

- **Provider-neutral:** application code should not be tightly coupled to one model vendor.
- **Security by design:** identity, authorization, data boundaries and tool permissions are architectural concerns.
- **Observable by default:** model calls, retrieval and tool execution must be measurable.
- **Evaluated, not assumed:** AI quality should be tested with repeatable evaluation datasets.
- **Cost-aware:** token usage, latency and model selection are operational concerns.
- **Incremental complexity:** introduce agents, distributed services and infrastructure only when the use case requires them.
- **Production over demo:** every major capability should have a path from local development to production deployment.

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
│   │   └── ai.py
│   ├── core/
│   │   └── config.py
│   └── main.py
├── docs/
│   ├── architecture/
│   ├── adr/
│   ├── product-specification.md
│   └── roadmap.md
├── tests/
│   ├── test_ai_gateway.py
│   └── test_openai_provider.py
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
- [Architecture](docs/architecture/README.md)
- [Roadmap](docs/roadmap.md)
- Architecture Decision Records will live under `docs/adr/`.

## Status

**Current milestone: V0.3 — production LLM provider integration.**

This repository is intentionally being built in public, with each milestone adding a working capability and the corresponding architecture documentation.

## Author

**Keyar Srinivasan** — Director & CTO, O Clock Software Pvt. Ltd.

Technology executive and product engineering leader focused on enterprise software, mobile platforms, cloud architecture, AI-enabled products and engineering systems.

---

<p align="center"><b>Enterprise AI · Software Architecture · AI Agents · RAG · Production Engineering</b></p>
