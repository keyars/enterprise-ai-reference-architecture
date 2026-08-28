# Release Checklist

Before merging a release-oriented change:

1. Confirm the change is on a feature branch.
2. Run Ruff locally.
3. Run the complete pytest suite.
4. Confirm PostgreSQL/pgvector integration tests execute in CI.
5. Review changed files for secrets and generated artifacts.
6. Open a pull request against `main`.
7. Merge only after the required CI checks pass.
8. Verify the resulting `main` commit and CI run.

A merged pull request proves source integration; it does not prove a live production deployment.
