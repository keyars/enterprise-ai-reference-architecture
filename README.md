# Enterprise AI Reference Architecture

[![Status](https://img.shields.io/badge/status-V0.6.0%20%7CAgent%20Runtime-111827?style=for-the-badge)](https://github.com/keyars/enterprise-ai-reference-architecture)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![RAG](https://img.shields.io/badge/RAG-Enterprise-111827?style=for-the-badge)](#enterprise-rag)
[![pgvector](https://img.shields.io/badge/PostgreSQL%20%2B%20pgvector-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://github.com/pgvector/pgvector)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue?style=for-the-badge)](LICENSE)

> A production-oriented reference architecture for secure, scalable and observable enterprise AI applications using LLMs, RAG, agents, tools and enterprise data.

## Purpose

This repository is built incrementally. Each capability is separated into implementation status and runtime verification status. A capability is never described as runtime-verified until an actual execution environment reports success.

## Current architecture

```text
Client
  |
  v
FastAPI
  |
  +--> AI Gateway --------------------> Model Provider
  |
  +--> RAG Service
  |      |
  |      +--> Embedding Provider
  |      +--> VectorStore
  |              +--> In-Memory
  |              +--> PostgreSQL + pgvector
  |
  +--> Agent Runtime
         |
         +--> Tool Registry
         +--> Authorization
         +--> Native Function Calling
         +--> Bounded Execution Loop
         +--> Tool Trace
```

## V0.6 Agent Runtime

V0.6 introduces a real bounded agent execution loop rather than a prompt-only agent abstraction.

### Implemented

- Explicit `ToolDefinition` contracts
- Tool registry with duplicate-registration protection
- Explicit per-request tool allowlist
- Authorization check before every tool execution
- Native OpenAI Responses API function-calling adapter
- Structured tool-call parsing
- Function-call output continuation
- Bounded maximum agent steps
- Tool execution trace
- Tool-output size limit
- Deterministic test provider for agent-loop tests
- Example `add_numbers` tool

### Agent flow

```text
User Request
    |
    v
Agent Runtime
    |
    v
Model Provider
    |
    +---- final answer -------------------> Response
    |
    +---- function call
              |
              v
        Authorization
              |
              v
          Tool Registry
              |
              v
         Tool Execution
              |
              v
       function_call_output
              |
              +----------> Model Provider
```

The runtime intentionally does not implement unrestricted autonomous execution. Tools must be registered and explicitly allowed for the request.

### API

```http
POST /agents/run
Content-Type: application/json
```

Example:

```json
{
  "prompt": "Calculate 27 + 15 and explain the result.",
  "allowed_tools": ["add_numbers"],
  "max_steps": 5,
  "temperature": 0.2
}
```

The agent endpoint requires `OPENAI_API_KEY` because this implementation uses native provider tool calling. Without a configured key it returns HTTP 501 rather than silently pretending that local text generation is equivalent to tool calling.

## Enterprise RAG

The RAG layer implements:

```text
Document
   |
Normalization
   |
Chunking + Metadata
   |
Embedding Provider
   |
VectorStore
   |
Cosine Similarity Retrieval
   |
Context Assembly
   |
AI Gateway
   |
Grounded Answer + Sources
```

Implemented components include document ingestion, configurable chunking, embedding-provider abstraction, deterministic local embeddings, OpenAI embeddings, an in-memory vector store, PostgreSQL + pgvector persistence, source metadata and similarity scores.

## PostgreSQL + pgvector

Local development uses PostgreSQL 16 with the pgvector Docker image:

```bash
docker compose up -d postgres
```

Install PostgreSQL support:

```bash
pip install -e ".[dev,postgres]"
```

Run the real integration test:

```bash
RUN_POSTGRES_INTEGRATION=1 \
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/enterprise_ai \
pytest tests/test_postgres_integration.py -q
```

The CI workflow provisions PostgreSQL + pgvector and runs the integration test after linting.

## Configuration

```text
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.5
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TIMEOUT_SECONDS=30
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/enterprise_ai
```

Never commit credentials or `.env` files.

## Verification policy

The repository distinguishes:

- **Implemented:** code and corresponding tests exist.
- **Runtime verified:** the code has actually executed successfully in CI or another explicit runtime environment.
- **Pending:** not implemented or not yet verified.

At the time of this milestone, the most recent PostgreSQL CI run had a real PostgreSQL service start successfully, but the workflow failed during Ruff linting before tests ran. Therefore V0.5.1 remains runtime-unverified until a later CI run passes.

## Current status

| Milestone | Implementation | Runtime Verified |
|---|---:|---:|
| V0.1 Architecture Foundation | ✅ | 🟡 |
| V0.2 AI Gateway | ✅ | 🟡 |
| V0.3 OpenAI Provider | ✅ | 🟡 |
| V0.4 RAG Foundation | ✅ | 🟡 |
| V0.5 PostgreSQL + pgvector | ✅ | 🟡 |
| V0.5.1 Reproducible pgvector CI | ✅ | 🟡 |
| **V0.6 Agent Runtime** | **✅** | **🟡 Pending CI** |

## Next

- Persistent agent state and memory
- Observability and tracing
- Token and cost accounting
- AI evaluation framework
- Authentication and RBAC
- Multi-tenancy
- Prompt-injection protections
- Sensitive-data controls
- Production migrations
- Full application Docker stack
- AWS deployment reference

## Documentation

- [Product Specification](docs/product-specification.md)
- [AI Gateway Architecture](docs/architecture/ai-gateway.md)
- [RAG Architecture](docs/architecture/rag.md)
- [PostgreSQL + pgvector Architecture](docs/architecture/pgvector.md)
- [Roadmap](docs/roadmap.md)

## Author

**Keyar Srinivasan** — Director & CTO, O Clock Software Pvt. Ltd.
