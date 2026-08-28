"""Application authentication, authorization and AI safety policies."""

from dataclasses import dataclass
import hashlib
import hmac
import os
import re

from fastapi import Header, HTTPException


TENANT_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}")


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str
    roles: frozenset[str]
    tenant_id: str


@dataclass(frozen=True, slots=True)
class ApiCredential:
    secret: str
    subject: str
    tenant_id: str
    roles: frozenset[str]


def _load_credentials() -> tuple[ApiCredential, ...]:
    """Load explicit API credentials from AUTH_CREDENTIALS.

    Format: secret:subject:tenant:role1,role2;secret2:subject2:tenant2:user
    The legacy AUTH_API_KEY(S) variables remain supported for local development.
    """
    raw = os.getenv("AUTH_CREDENTIALS", "").strip()
    credentials: list[ApiCredential] = []
    if raw:
        for item in raw.split(";"):
            parts = item.strip().split(":")
            if len(parts) != 4:
                raise RuntimeError("AUTH_CREDENTIALS entries must be secret:subject:tenant:roles")
            secret, subject, tenant_id, roles_text = parts
            roles = frozenset(role.strip().lower() for role in roles_text.split(",") if role.strip())
            if not secret or not subject or not TENANT_PATTERN.fullmatch(tenant_id) or not roles:
                raise RuntimeError("AUTH_CREDENTIALS contains an invalid credential")
            credentials.append(ApiCredential(secret, subject, tenant_id, roles))
        return tuple(credentials)

    legacy = os.getenv("AUTH_API_KEYS", os.getenv("AUTH_API_KEY", ""))
    return tuple(
        ApiCredential(
            secret=k.strip(),
            subject=hashlib.sha256(k.strip().encode()).hexdigest()[:16],
            tenant_id="local",
            roles=frozenset({"user"}),
        )
        for k in legacy.split(",")
        if k.strip()
    )


def auth_enabled() -> bool:
    return os.getenv("AUTH_ENABLED", "false").lower() == "true"


def _validate_tenant(tenant_id: str | None) -> str:
    if not tenant_id or not TENANT_PATTERN.fullmatch(tenant_id):
        raise HTTPException(status_code=400, detail="Invalid tenant identifier")
    return tenant_id


def authenticate(api_key: str | None, tenant_id: str | None) -> Principal:
    if not auth_enabled():
        return Principal("local-development", frozenset({"admin"}), tenant_id or "local")

    requested_tenant = _validate_tenant(tenant_id)
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    for credential in _load_credentials():
        if hmac.compare_digest(api_key, credential.secret):
            if credential.tenant_id != requested_tenant:
                raise HTTPException(status_code=403, detail="Credential is not authorized for tenant")
            return Principal(credential.subject, credential.roles, credential.tenant_id)

    raise HTTPException(status_code=401, detail="Invalid API key")


def require_roles(*required: str):
    required_roles = frozenset(role.lower() for role in required)

    def dependency(
        x_api_key: str | None = Header(default=None),
        x_tenant_id: str | None = Header(default=None),
    ) -> Principal:
        principal = authenticate(x_api_key, x_tenant_id)
        if required_roles and not principal.roles.intersection(required_roles):
            raise HTTPException(status_code=403, detail="Insufficient role")
        return principal

    return dependency


def detect_prompt_injection(text: str) -> bool:
    patterns = (
        r"ignore\s+(all|any|the)\s+previous\s+instructions",
        r"reveal\s+(the\s+)?system\s+prompt",
        r"developer\s+message",
        r"disable\s+(all\s+)?safety",
        r"bypass\s+(security|authorization|policy)",
    )
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def redact_sensitive_data(text: str) -> str:
    patterns = [
        (r"\b[A-Z]{5}\d{4}[A-Z]\b", "[PAN_REDACTED]"),
        (r"\b\d{12}\b", "[AADHAAR_REDACTED]"),
        (r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", "[EMAIL_REDACTED]"),
        (r"\b(?:\+?91[-\s]?)?[6-9]\d{9}\b", "[PHONE_REDACTED]"),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    return text
