# Contributing

Thank you for contributing to the Enterprise AI Reference Architecture.

## Development workflow

1. Create a focused branch from `main`.
2. Make a small, reviewable change.
3. Add or update automated tests for behavioral changes.
4. Run linting locally:

```bash
ruff check .
```

5. Run the test suite locally:

```bash
pytest
```

6. For PostgreSQL integration tests, start the local database and set:

```bash
RUN_POSTGRES_INTEGRATION=1
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/enterprise_ai
```

7. Open a pull request and wait for GitHub Actions to pass.

## Engineering principles

- Prefer explicit interfaces over provider-specific coupling.
- Keep security decisions outside the model.
- Keep agent execution bounded.
- Test failure paths, not only successful paths.
- Do not commit secrets, credentials or production data.
- Document architectural decisions when introducing a significant new boundary.
- Do not describe an implementation as production-ready until it has appropriate runtime and operational evidence.

## Pull requests

A good pull request should explain:

- what changed
- why it changed
- how it was tested
- any limitations or follow-up work

CI must remain green before merging.
