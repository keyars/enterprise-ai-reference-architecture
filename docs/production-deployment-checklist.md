# Production Deployment Checklist

Use this checklist before describing a deployment as production-ready.

## Application

- [ ] Configuration is supplied through environment or managed secret injection.
- [ ] Authentication uses an external identity provider.
- [ ] Authorization policies are reviewed.
- [ ] Tenant isolation is verified with integration tests.
- [ ] Tool permissions follow least privilege.
- [ ] Rate limits are configured.

## Data

- [ ] PostgreSQL backups are enabled.
- [ ] Restore testing is completed.
- [ ] Database migrations are versioned and tested.
- [ ] Tenant data retention is defined.
- [ ] Audit retention is defined.

## Observability

- [ ] Request correlation IDs are available.
- [ ] Metrics are exported to a durable monitoring system.
- [ ] Distributed traces are exported.
- [ ] Error alerts are configured.
- [ ] AI token/cost telemetry is monitored.

## Deployment

- [ ] Container runs as non-root.
- [ ] Health and readiness checks are configured.
- [ ] Resource limits are defined.
- [ ] Secrets are not baked into images.
- [ ] TLS is terminated securely.
- [ ] Load testing is completed against a representative environment.
- [ ] Rollback procedure is tested.

A green CI pipeline verifies the repository's automated checks. It does not by itself satisfy this deployment checklist.
