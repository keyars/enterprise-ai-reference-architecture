"""Document ingestion and retrieval-augmented generation endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from app.ai.gateway import AIGateway
from app.ai.providers.local import LocalProvider
from app.ai.providers.openai import OpenAIProvider
from app.core.config import settings
from app.rag.embeddings import DeterministicEmbeddingProvider, OpenAIEmbeddingProvider
from app.rag.models import Document, RAGQuery, RAGResponse
from app.rag.service import RAGService
from app.rag.store import InMemoryVectorStore
from app.security import Principal, require_roles

router = APIRouter(prefix="/rag", tags=["RAG"])
_store = InMemoryVectorStore()


def create_rag_service() -> RAGService:
    if settings.openai_api_key:
        gateway = AIGateway(
            OpenAIProvider(
                api_key=settings.openai_api_key,
                default_model=settings.openai_model,
                timeout=settings.openai_timeout_seconds,
            )
        )
        embeddings = OpenAIEmbeddingProvider(settings.openai_api_key)
    else:
        gateway = AIGateway(LocalProvider())
        embeddings = DeterministicEmbeddingProvider()
    return RAGService(gateway, embeddings, _store)


@router.post("/documents", status_code=201)
async def ingest_document(
    document: Document,
    principal: Principal = Depends(require_roles("admin", "user")),  # noqa: B008
) -> dict[str, object]:
    """Chunk and index a document within the authenticated tenant."""
    if document.tenant_id != principal.tenant_id:
        raise HTTPException(status_code=403, detail="Document tenant does not match authenticated tenant")
    try:
        count = await create_rag_service().ingest(document)
        return {"document_id": document.id, "chunks_indexed": count}
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Document ingestion failed") from exc


@router.post("/query", response_model=RAGResponse)
async def query_rag(
    request: RAGQuery,
    principal: Principal = Depends(require_roles("admin", "user")),  # noqa: B008
) -> RAGResponse:
    """Retrieve relevant document chunks only from the authenticated tenant."""
    try:
        return await create_rag_service().query(request, tenant_id=principal.tenant_id)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="RAG request failed") from exc
