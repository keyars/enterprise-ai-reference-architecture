# Release Verification

A release-oriented change is complete only after the following sequence:

- source committed on a feature branch
- Ruff passes
- full pytest suite passes
- PostgreSQL/pgvector integration tests pass in CI
- pull request is opened against `main`
- pull request is merged
- merged `main` commit is verified by CI

Live infrastructure, identity-provider integration, production traffic, backups, restore tests, and load testing require the corresponding environment and are not implied by a green repository CI run.
