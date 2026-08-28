# CI Verification Policy

A milestone is considered verified only when the GitHub Actions run for the corresponding commit completes successfully.

## Required checks

- Ruff linting
- Full pytest suite
- PostgreSQL/pgvector integration tests when the CI service is available

## Status vocabulary

- **Implemented**: source code and tests have been committed.
- **CI verified**: the corresponding commit completed the required CI checks successfully.
- **Environment verified**: the feature was exercised against the target deployment environment.

A CI-green result does not imply that AWS, an external identity provider, production observability, or production-scale performance has been validated.
