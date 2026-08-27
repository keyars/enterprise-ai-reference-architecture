from time import perf_counter

from app.ai.gateway import AIGateway
from app.ai.models import GenerationRequest
from app.rag.chunking import chunk_document
from app.rag.embeddings import EmbeddingProvider
from app.rag.models import Document, RAGQuery, RAGResponse
from app.rag.store import VectorStore


class RAGService:
    def __init__(self, gateway: AIGateway, embeddings: EmbeddingProvider, store: VectorStore) -> None:
        self.gateway = gateway
        self.embeddings = embeddings
        self.store = store

    async def ingest(self, document: Document) -> int:
        chunks = chunk_document(document)
        vectors = await self.embeddings.embed([chunk.text for chunk in chunks])
        enriched = [chunk.model_copy(update={"embedding": vector}) for chunk, vector in zip(chunks, vectors, strict=True)]
        await self.store.upsert(enriched)
        return len(enriched)

    async def query(self, request: RAGQuery) -> RAGResponse:
        started = perf_counter()
        [question_embedding] = await self.embeddings.embed([request.question])
        sources = await self.store.search(question_embedding, request.top_k)

        context = "\n\n".join(
            f"[Source {index}: {result.chunk.metadata.get('title', result.chunk.document_id)}] {result.chunk.text}"
            for index, result in enumerate(sources, start=1)
        )
        prompt = (
            "Answer the user's question using only the supplied context. "
            "If the context does not contain enough information, say so clearly. "
            "Cite supporting sources using [Source N].\n\n"
            f"Context:\n{context or '[No relevant sources found]'}\n\n"
            f"Question: {request.question}"
        )
        generation = await self.gateway.generate(
            GenerationRequest(
                prompt=prompt,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )
        )
        latency_ms = round((perf_counter() - started) * 1000, 2)
        return RAGResponse(
            answer=generation.text,
            sources=sources,
            provider=generation.provider,
            model=generation.model,
            latency_ms=latency_ms,
        )
