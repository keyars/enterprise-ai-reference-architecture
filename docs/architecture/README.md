# Architecture Overview

The reference architecture is intentionally layered. The first implementation establishes stable boundaries before adding model, retrieval and agent infrastructure.

## Layers

1. **API** — transport, validation and HTTP concerns.
2. **Application** — use cases and orchestration.
3. **Domain** — business concepts and provider-independent contracts.
4. **Infrastructure** — databases, model providers, vector stores, queues and external services.
5. **Cross-cutting concerns** — security, observability, evaluation and cost accounting.

## Architectural direction

```text
Client
  ↓
API Layer
  ↓
Application / Use Cases
  ↓
Domain Contracts
  ↓
Infrastructure Adapters
  ├── LLM Providers
  ├── PostgreSQL / pgvector
  ├── Redis
  ├── Object Storage
  └── External Enterprise APIs
```

The central rule is **dependency inversion**: the domain and application layers should depend on stable interfaces rather than vendor-specific SDKs.

## Evolution path

The architecture starts as a modular application. Components may later be extracted into independently deployable services when scale, reliability or organisational boundaries justify the additional operational complexity.
