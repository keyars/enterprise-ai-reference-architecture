from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Reference Architecture",
    description=(
        "A production-oriented reference implementation for enterprise AI "
        "applications using LLMs, RAG, agents, tools, security and observability."
    ),
    version="0.1.0",
)


@app.get("/health", tags=["System"])
async def health() -> dict[str, str]:
    """Return service health information."""
    return {"status": "ok", "service": "enterprise-ai-reference-architecture"}


@app.get("/architecture", tags=["System"])
async def architecture() -> dict[str, object]:
    """Expose the architectural capabilities planned for the reference implementation."""
    return {
        "version": "0.1.0",
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
            "retrieval-augmented-generation",
            "ai-agents",
            "tool-calling",
            "memory",
            "authentication-and-rbac",
            "observability",
            "evaluation",
            "cost-accounting",
        ],
    }
