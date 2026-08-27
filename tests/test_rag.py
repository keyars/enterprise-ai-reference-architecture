import pytest

from app.ai.gateway import AIGateway
from app.ai.providers.local import LocalProvider
from app.rag.chunking import chunk_document
from app.rag.embeddings import DeterministicEmbeddingProvider
from app.rag.models import Document, RAGQuery
from app.rag.service import RAGService
from app.rag.store import InMemoryVectorStore, cosine_similarity


async def build_service() -> RAGService:
    return RAGService(
        gateway=AIGateway(LocalProvider()),
        embeddings=DeterministicEmbeddingProvider(),
        store=InMemoryVectorStore(),
    )


def test_chunk_document_creates_overlap() -> None:
    document = Document(id="doc-1", title="Guide", content="A " * 1000, tenant_id="tenant-a")
    chunks = chunk_document(document, max_characters=100, overlap=20)
    assert len(chunks) > 1
    assert chunks[0].document_id == "doc-1"
    assert chunks[0].tenant_id == "tenant-a"
    assert chunks[1].chunk_index == 1


def test_cosine_similarity_identity() -> None:
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0


@pytest.mark.asyncio
async def test_ingest_and_query_without_external_services() -> None:
    service = await build_service()
    document = Document(
        id="doc-1",
        title="Architecture Guide",
        content="Enterprise architecture uses clear boundaries between applications and services.",
        metadata={"department": "engineering"},
        tenant_id="tenant-a",
    )

    indexed = await service.ingest(document)
    response = await service.query(
        RAGQuery(question="What does enterprise architecture use?"),
        tenant_id="tenant-a",
    )

    assert indexed >= 1
    assert response.answer.startswith("Local provider response:")
    assert response.sources
    assert response.sources[0].chunk.document_id == "doc-1"


@pytest.mark.asyncio
async def test_in_memory_store_enforces_tenant_isolation() -> None:
    service = await build_service()
    await service.ingest(
        Document(
            id="doc-a",
            title="Tenant A",
            content="alpha enterprise architecture",
            tenant_id="tenant-a",
        )
    )
    await service.ingest(
        Document(
            id="doc-b",
            title="Tenant B",
            content="beta enterprise architecture",
            tenant_id="tenant-b",
        )
    )

    response = await service.query(
        RAGQuery(question="enterprise architecture", top_k=20),
        tenant_id="tenant-a",
    )

    assert response.sources
    assert {result.chunk.tenant_id for result in response.sources} == {"tenant-a"}
    assert all(result.chunk.document_id != "doc-b" for result in response.sources)


@pytest.mark.asyncio
async def test_query_requires_tenant_id() -> None:
    service = await build_service()
    with pytest.raises(ValueError, match="tenant_id"):
        await service.query(RAGQuery(question="hello"), tenant_id="")
