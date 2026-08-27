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
    document = Document(id="doc-1", title="Guide", content="A " * 1000)
    chunks = chunk_document(document, max_characters=100, overlap=20)
    assert len(chunks) > 1
    assert chunks[0].document_id == "doc-1"
    assert chunks[1].chunk_index == 1


def test_cosine_similarity_identity() -> None:
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0


async def test_ingest_and_query_without_external_services() -> None:
    service = await build_service()
    document = Document(
        id="doc-1",
        title="Architecture Guide",
        content="Enterprise architecture uses clear boundaries between applications and services.",
        metadata={"department": "engineering"},
    )

    indexed = await service.ingest(document)
    response = await service.query(RAGQuery(question="What does enterprise architecture use?"))

    assert indexed >= 1
    assert response.answer.startswith("Local provider response:")
    assert response.sources
    assert response.sources[0].chunk.document_id == "doc-1"
