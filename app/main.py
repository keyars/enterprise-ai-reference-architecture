from fastapi import FastAPI

from app.api.ai import router as ai_router
from app.api.rag import router as rag_router

app = FastAPI(
    title="Enterprise AI Reference Architecture",
    description=(
        "A production-oriented reference implementation for enterprise AI "
        "applications using LLMs, RAG, agents, tools, security and observability."
    ),
    version="0.5.1",
)

app.include_router(ai_router)
app.include_router(rag_router)


@app.get("/health", tags=["System"])
async def health() -> dict[str, str]:
    """Return service health information."""
    return {"status": "ok", "service": "enterprise-ai-reference-architecture"}


@app.get("/architecture", tags=["System"])
async def architecture() -> dict[str, object]:
    """Expose the architectural capabilities of the reference implementation."""
    return {
        "version": "0.5.1",
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
            "postgresql-pgvector",
            "ai-agents",
            "tool-calling",
            "memory",
            "authentication-and-rbac",
            "observability",
            "evaluation",
            "cost-accounting",
        ],
    }
