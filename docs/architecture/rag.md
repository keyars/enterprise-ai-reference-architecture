# Enterprise RAG Architecture

## Purpose

The RAG subsystem separates document ingestion, chunking, embeddings, vector storage, retrieval and generation. This keeps retrieval concerns independent from the LLM provider.

## Flow

```text
Document
   ↓
Normalization
   ↓
Chunking + Metadata
   ↓
Embedding Provider
   ↓
Vector Store
   ↓
Semantic Search
   ↓
Context Assembly
   ↓
AI Gateway
   ↓
Grounded Answer + Sources
```

## Current implementation

V0.4 includes:

- deterministic chunking with overlap
- provider abstraction for embeddings
- OpenAI embeddings adapter
- deterministic local embeddings for offline development and tests
- in-memory vector store with cosine similarity
- grounded prompt construction
- source metadata returned with answers
- FastAPI document ingestion and query endpoints

## Production evolution

The in-memory store is intentionally a development/test implementation. The production reference will add PostgreSQL with `pgvector`, persistent document records, tenant-aware filtering, document versioning, ingestion jobs and retrieval evaluation.

## Grounding contract

The generation prompt instructs the model to use only retrieved context and to acknowledge when the context is insufficient. Sources are included as numbered context blocks so generated answers can reference `[Source N]`.

This is a grounding mechanism, not a guarantee against hallucination. Production deployments must combine it with evaluation, access controls, prompt-injection defenses and monitoring.
