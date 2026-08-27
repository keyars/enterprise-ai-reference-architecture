from collections.abc import Sequence

from app.core.config import settings


class EmbeddingProvider:
    async def embed(self, texts: Sequence[str]) -> list[list[float]]:
        raise NotImplementedError


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str, model: str | None = None) -> None:
        from openai import AsyncOpenAI

        self.client = AsyncOpenAI(api_key=api_key, timeout=settings.openai_timeout_seconds)
        self.model = model or settings.openai_embedding_model

    async def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        response = await self.client.embeddings.create(model=self.model, input=list(texts))
        return [item.embedding for item in sorted(response.data, key=lambda item: item.index)]


class DeterministicEmbeddingProvider(EmbeddingProvider):
    """Small local embedding substitute for tests and offline demonstrations.

    It is deliberately deterministic and is not intended to represent production
    semantic quality. Production deployments should use a real embedding model.
    """

    dimensions = 64

    async def embed(self, texts: Sequence[str]) -> list[list[float]]:
        import hashlib
        import math

        vectors: list[list[float]] = []
        for text in texts:
            vector = [0.0] * self.dimensions
            tokens = text.lower().split()
            for token in tokens:
                digest = hashlib.sha256(token.encode("utf-8")).digest()
                for offset in (0, 4, 8):
                    index = int.from_bytes(digest[offset:offset + 2], "big") % self.dimensions
                    vector[index] += 1.0
            norm = math.sqrt(sum(value * value for value in vector)) or 1.0
            vectors.append([value / norm for value in vector])
        return vectors
