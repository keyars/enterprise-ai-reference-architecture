# Roadmap

## V0.1 — Architecture Foundation

- [x] Repository structure
- [x] Product specification
- [x] FastAPI application foundation
- [x] Health endpoint
- [x] Architecture capability endpoint
- [x] Unit tests
- [x] Initial Docker runtime

## V0.2 — Provider-Neutral AI Gateway

- [x] Provider-neutral model interface
- [x] Local provider
- [x] OpenAI adapter
- [x] Request/response contracts
- [x] Configuration and secret handling foundation
- [x] Provider error boundary

## V0.3 — Enterprise RAG Foundation

- [x] Document ingestion
- [x] Text normalization
- [x] Chunking strategy
- [x] Embedding abstraction
- [x] OpenAI embeddings
- [x] Deterministic local embeddings
- [x] In-memory vector retrieval
- [x] Source-aware answers

## V0.5 — PostgreSQL + pgvector

- [x] PostgreSQL vector-store adapter
- [x] pgvector extension initialization
- [x] Persistent chunk upsert
- [x] Cosine-distance retrieval
- [x] Embedding dimension validation
- [x] Reproducible Docker database service
- [x] GitHub Actions PostgreSQL service
- [x] Real pgvector round-trip integration test
- [ ] Production migration system
- [ ] Tenant-aware retrieval filters
- [ ] Document/version persistence model

## V0.6 — Agent Runtime

- [ ] Agent abstraction
- [ ] Tool registry
- [ ] Tool schemas
- [ ] Tool authorization
- [ ] Planning/execution boundary
- [ ] Agent state
- [ ] Guardrails

## V0.7 — Observability & Evaluation

- [ ] Request tracing
- [ ] LLM usage telemetry
- [ ] Token and cost accounting
- [ ] Retrieval telemetry
- [ ] Evaluation datasets
- [ ] Automated quality checks

## V0.8 — Security & Multi-tenancy

- [ ] Authentication
- [ ] RBAC
- [ ] Tenant isolation
- [ ] Prompt-injection protections
- [ ] Sensitive-data controls
- [ ] Audit events

## V0.9 — Production Operations

- [ ] Full Docker application stack
- [ ] Database migrations
- [ ] Health/readiness probes
- [ ] Configuration profiles
- [ ] Operational runbooks

## V1.0 — Production Reference

- [ ] Integrated reference application
- [ ] Complete architecture documentation
- [ ] CI/CD hardening
- [ ] AWS deployment reference
- [ ] Security review checklist
- [ ] Performance and reliability guidance
