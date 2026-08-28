# Security Model

## Trust boundaries

1. The client supplies credentials and a tenant identifier.
2. Authentication establishes a principal.
3. Authorization evaluates the principal's roles.
4. RAG retrieval receives the authenticated tenant context.
5. Vector storage filters records by tenant before returning results.

## Current reference controls

- Explicit tenant-bound API credentials
- Constant-time API-key comparison
- Role checks at dependency boundaries
- Tenant validation
- Tenant-scoped vector retrieval
- Prompt-injection detection heuristics
- Sensitive-data redaction helpers
- Bounded audit metadata
- Request correlation IDs

## Important limitations

The default reference configuration is not an external identity-provider integration. Production deployments should replace local API-key authentication with an OIDC/OAuth2-compatible identity provider, durable policy management, managed secrets, and centralized audit storage.

The prompt-injection detector is a defense-in-depth heuristic, not a complete security boundary. Tool authorization and least privilege remain mandatory even when input appears safe.
