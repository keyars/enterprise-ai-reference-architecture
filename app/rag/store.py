import math
from collections.abc import Sequence

from app.rag.models import DocumentChunk, SearchResult


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Embedding dimensions must match")
    numerator = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


class VectorStore:
    async def upsert(self, chunks: Sequence[DocumentChunk]) -> None:
        raise NotImplementedError

    async def search(self, embedding: Sequence[float], top_k: int = 5) -> list[SearchResult]:
        raise NotImplementedError


class InMemoryVectorStore(VectorStore):
    """Reference vector store used for local development and automated tests."""

    def __init__(self) -> None:
        self._chunks: dict[str, DocumentChunk] = {}

    async def upsert(self, chunks: Sequence[DocumentChunk]) -> None:
        for chunk in chunks:
            if not chunk.embedding:
                raise ValueError(f"Chunk {chunk.id} has no embedding")
            self._chunks[chunk.id] = chunk

    async def search(self, embedding: Sequence[float], top_k: int = 5) -> list[SearchResult]:
        if top_k <= 0:
            return []
        ranked = [
            SearchResult(chunk=chunk, score=cosine_similarity(embedding, chunk.embedding))
            for chunk in self._chunks.values()
        ]
        ranked.sort(key=lambda result: result.score, reverse=True)
        return ranked[:top_k]
