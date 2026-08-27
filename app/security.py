"""Application security policies used by protected endpoints."""

import hashlib
import hmac
import os
import re
from dataclasses import dataclass

from fastapi import Header, HTTPException


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str
    roles: frozenset[str]
    tenant_id: str


_SECRET = os.getenv("AUTH_API_KEY", "")
_API_KEYS = {k.strip() for k in os.getenv("AUTH_API_KEYS", _SECRET).split(",") if k.strip()}


def auth_enabled() -> bool:
    return os.getenv("AUTH_ENABLED", "false").lower() == "true"


def authenticate(api_key: str | None, tenant_id: str | None) -> Principal:
    if not auth_enabled():
        return Principal("local-development", frozenset({"admin"}), tenant_id or "local")
    if not api_key or not any(hmac.compare_digest(api_key, valid) for valid in _API_KEYS):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    if not tenant_id or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", tenant_id):
        raise HTTPException(status_code=400, detail="Invalid tenant identifier")
    # Deterministic demo RBAC mapping; production identity providers should replace it.
    digest = hashlib.sha256(api_key.encode()).hexdigest()
    roles = frozenset({"admin"}) if digest.endswith("0") else frozenset({"user"})
    return Principal(subject=digest[:16], roles=roles, tenant_id=tenant_id)


def require_roles(*required: str):
    def dependency(
        x_api_key: str | None = Header(default=None),
        x_tenant_id: str | None = Header(default=None),
    ) -> Principal:
        principal = authenticate(x_api_key, x_tenant_id)
        if required and not principal.roles.intersection(required):
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
