# Production Readiness

This reference implementation distinguishes executable guarantees from deployment-specific guarantees.

## Verified in CI

- API linting and automated tests
- Health and readiness endpoints
- Request correlation IDs
- Process-local request and LLM metrics
- Bounded audit metadata
- Tenant-scoped RAG retrieval
- PostgreSQL/pgvector integration tests

## Deployment-specific work

The following require a real environment and are intentionally not represented as completed by the reference code alone:

- OIDC/JWT integration with an external identity provider
- Persistent authorization policy management
- Durable audit storage and retention controls
- Distributed OpenTelemetry export
- Managed secret storage
- Production rate limiting and WAF policy
- AWS infrastructure deployment
- Load testing against production-like workloads
- Disaster recovery and restore testing

## Health model

`GET /health` is a liveness check. It verifies that the application process is serving requests.

`GET /ready` is the traffic-readiness contract. It currently returns ready because this reference application does not initialize a mandatory external dependency during startup. When a production adapter owns PostgreSQL, a queue, or another mandatory dependency, its availability check should be added to this endpoint.

Do not use `/ready` as evidence that every external dependency is healthy unless those dependency checks have actually been implemented.
