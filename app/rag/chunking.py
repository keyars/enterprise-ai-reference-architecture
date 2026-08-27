import re

from app.rag.models import Document, DocumentChunk


def normalize_text(text: str) -> str:
    """Normalize whitespace while preserving readable paragraph boundaries."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_document(document: Document, max_characters: int = 1_200, overlap: int = 150) -> list[DocumentChunk]:
    """Split a document into deterministic, overlapping text chunks."""
    if max_characters <= 0:
        raise ValueError("max_characters must be positive")
    if overlap < 0 or overlap >= max_characters:
        raise ValueError("overlap must be >= 0 and smaller than max_characters")

    text = normalize_text(document.content)
    if not text:
        return []

    chunks: list[DocumentChunk] = []
    start = 0
    index = 0
    while start < len(text):
        end = min(start + max_characters, len(text))
        if end < len(text):
            boundary = max(text.rfind("\n\n", start, end), text.rfind(". ", start, end))
            if boundary > start + max_characters // 2:
                end = boundary + (2 if text[boundary:boundary + 2] == ". " else 0)

        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(
                DocumentChunk(
                    id=f"{document.id}:{index}",
                    document_id=document.id,
                    chunk_index=index,
                    text=chunk_text,
                    metadata={"title": document.title, **document.metadata},
                    tenant_id=document.tenant_id,
                )
            )
            index += 1

        if end >= len(text):
            break
        start = max(0, end - overlap)

    return chunks
