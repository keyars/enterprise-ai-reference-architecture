from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str
    title: str
    content: str = Field(min_length=1)
    metadata: dict[str, str] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    id: str
    document_id: str
    text: str
    chunk_index: int
    metadata: dict[str, str] = Field(default_factory=dict)
    embedding: list[float] = Field(default_factory=list)


class SearchResult(BaseModel):
    chunk: DocumentChunk
    score: float


class RAGQuery(BaseModel):
    question: str = Field(min_length=1, max_length=10_000)
    top_k: int = Field(default=5, ge=1, le=20)
    model: str | None = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1, le=32_000)


class RAGResponse(BaseModel):
    answer: str
    sources: list[SearchResult]
    provider: str
    model: str
    latency_ms: float | None = None
