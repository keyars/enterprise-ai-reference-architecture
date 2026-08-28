# Roadmap

## V0.1 — Architecture Foundation

- [x] Repository structure
- [x] Product specification
- [x] FastAPI application foundation
- [x] Health endpoint
- [x] Architecture capability endpoint
- [x] Unit tests
- [x] Docker runtime

## V0.2 — Model Gateway

- [x] Provider-neutral model interface
- [x] OpenAI adapter
- [x] Request/response contracts
- [x] Configuration and secret handling
- [ ] Model error taxonomy

## V0.3 — Enterprise RAG

- [x] Document ingestion
- [x] Text normalization
- [x] Chunking strategy
- [x] Embeddings
- [x] PostgreSQL + pgvector adapter
- [x] Source-aware answers
- [ ] Retrieval evaluation

## V0.4 — Agent Runtime

- [x] Agent abstraction
- [x] Tool registry
- [x] Tool authorization
- [x] Planning/execution boundary
- [x] Bounded agent state for a single run
- [x] Native OpenAI function calling adapter
- [x] Tool execution trace
- [ ] Persistent agent state
- [ ] Advanced guardrails

## V0.5 — Observability & Evaluation

### Observability — implemented

- [x] Request correlation IDs via `X-Request-ID`
- [x] Process-local request counters
- [x] Route-level request counts
- [x] LLM request counters
- [x] Input/output token totals from normalized provider usage
- [x] Request and LLM latency totals
- [x] Provider-level LLM counters
- [x] Non-sensitive `/metrics` endpoint

### Evaluation — remaining

- [ ] Evaluation datasets
- [ ] Retrieval evaluation
- [ ] Automated quality checks

### Cost intelligence — remaining

- [x] Explicit pricing model and deterministic cost calculation utility
- [ ] Versioned provider pricing catalogue
- [ ] Cost aggregation by tenant/model/request
- [ ] Budget and anomaly controls

## V0.6 — Security & Multi-tenancy

### Reference controls — implemented

- [x] API-key authentication mode
- [x] Role-based endpoint authorization
- [x] Tenant identifier validation
- [x] Tenant-scoped in-memory retrieval
- [x] Tenant-scoped PostgreSQL/pgvector retrieval
- [x] Cross-tenant ingestion rejection
- [x] Prompt-injection detection utility
- [x] Sensitive-data redaction utility

### Production hardening — remaining

- [ ] External identity provider integration
- [ ] Persistent RBAC/permission model
- [ ] Database-level row-level security strategy
- [ ] Secret-manager integration
- [ ] Comprehensive audit logging
- [ ] Robust prompt-injection defense and adversarial evaluation
- [ ] DLP policy engine
- [ ] Security review checklist

## V0.7 — Production Integration

- [ ] Integrated reference application
- [ ] Persistent service lifecycle and startup/shutdown management
- [ ] Centralized structured logging
- [ ] Distributed tracing/exporter integration
- [ ] Resilience policies and error taxonomy
- [ ] Background ingestion pipeline
- [ ] API contract/versioning strategy

## V0.8 — Deployment Reference

- [ ] Production Docker image hardening
- [ ] AWS deployment reference
- [ ] Secrets and configuration deployment pattern
- [ ] Database migration strategy
- [ ] Health/readiness probes
- [ ] Performance and reliability guidance

## V1.0 — Production Reference

- [ ] Complete architecture documentation
- [ ] End-to-end reference application
- [ ] CI/CD pipeline
- [ ] Security review and threat model
- [ ] Evaluation suite with representative datasets
- [ ] Operational runbook
- [ ] Performance baseline
- [ ] Disaster recovery guidance

## Verification policy

A milestone is only considered **runtime verified** when the relevant automated tests or deployment checks have actually executed successfully.

> **Implemented ≠ Runtime Verified ≠ Production Ready**

This distinction is intentionally maintained throughout the project.
