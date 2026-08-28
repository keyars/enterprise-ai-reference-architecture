from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.agents.api import router as agents_router
from app.api.ai import router as ai_router
from app.api.rag import router as rag_router
from app.audit import record_event
from app.audit import snapshot as audit_snapshot
from app.observability import metrics, start_request

app = FastAPI(
    title="Enterprise AI Reference Architecture",
    description=(
        "A production-oriented reference implementation for enterprise AI "
        "applications using LLMs, RAG, agents, tools, security and observability."
    ),
    version="0.7.0",
)


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    telemetry = start_request()
    try:
        response = await call_next(request)
        failed = response.status_code >= 500
        metrics.record_request(request.url.path, telemetry.latency_ms, failed)
        record_event(
            "HTTP_REQUEST",
            "failure" if failed else "success",
            resource=request.url.path,
        )
        response.headers["X-Request-ID"] = telemetry.request_id
        return response
    except Exception:
        metrics.record_request(request.url.path, telemetry.latency_ms, True)
        record_event("HTTP_REQUEST", "error", resource=request.url.path)
        raise


app.include_router(ai_router)
app.include_router(rag_router)
app.include_router(agents_router)


@app.get("/health", tags=["System"])
async def health() -> dict[str, str]:
    """Liveness endpoint: confirms the process is serving requests."""
    return {"status": "ok", "service": "enterprise-ai-reference-architecture"}


@app.get("/ready", tags=["System"])
async def readiness() -> JSONResponse:
    """Readiness endpoint for traffic management.

    The reference application has no mandatory external dependency that is
    initialized by the application lifecycle, so readiness is currently tied
    to successful application startup. Dependency-specific checks belong here
    when production adapters are enabled.
    """
    return JSONResponse({"status": "ready", "service": "enterprise-ai-reference-architecture"})


@app.get("/metrics", tags=["System"])
async def metrics_endpoint() -> JSONResponse:
    """Return non-sensitive process-local operational counters."""
    return JSONResponse(metrics.snapshot())


@app.get("/audit", tags=["System"])
async def audit_endpoint() -> JSONResponse:
    """Return bounded audit metadata without request bodies or credentials."""
    return JSONResponse(audit_snapshot())


@app.get("/architecture", tags=["System"])
async def architecture() -> dict[str, object]:
    """Expose the architectural capabilities of the reference implementation."""
    return {
        "version": "0.7.0",
        "principles": [
            "provider-neutral",
            "security-by-design",
            "observable-by-default",
            "evaluated-not-assumed",
            "cost-aware",
            "production-over-demo",
        ],
        "capabilities": [
            "llm-gateway",
            "openai-provider",
            "document-chunking",
            "embeddings",
            "semantic-retrieval",
            "retrieval-augmented-generation",
            "agent-runtime",
            "controlled-tool-calling",
            "request-tracing",
            "llm-usage-telemetry",
            "audit-events",
        ],
    }
