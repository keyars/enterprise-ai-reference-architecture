# Security Architecture

This reference implementation separates security controls from model behavior.

## Implemented controls

- API-key authentication mode (`AUTH_ENABLED=true`)
- constant-time API-key comparison
- tenant identifier validation
- role checks through explicit dependencies
- explicit agent tool allowlists
- tool argument validation
- bounded agent execution
- bounded tool output
- prompt-injection pattern detection
- basic sensitive-data redaction utility

## Important limitations

The authentication implementation is intentionally a reference/demo boundary. It is **not a replacement for an enterprise identity provider**. Production deployments should integrate OIDC/OAuth2, a managed identity provider, short-lived credentials, key rotation, centralized policy and audit logging.

Prompt-injection detection is heuristic. It must be treated as a defense-in-depth signal, not a proof that a prompt is safe.

Sensitive-data redaction contains deterministic patterns for demonstration and testing. It is not a complete DLP system.

## Tenant isolation

Tenant identifiers are validated at the API security boundary. Persistent data isolation must additionally scope every database query by tenant before this architecture can be described as production multi-tenant.
