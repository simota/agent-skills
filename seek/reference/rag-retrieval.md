# RAG Retrieval Layer Reference

**Purpose:** Chunking-aware retrieval design for the retrieval layer of RAG pipelines — anti-patterns, spec template, and multi-stage retrieval.
**Read when:** Running the `rag` recipe or designing chunking, reranking, or context assembly for a RAG system.

---

## RAG Retrieval Anti-Patterns

| Anti-Pattern | Impact | Fix |
|-------------|--------|-----|
| Naive fixed-size chunking | Splits mid-sentence, loses context | Use semantic or recursive chunking with overlap |
| Missing chunk context | Chunks lack surrounding context needed to determine relevance | Use Contextual Retrieval — prepend per-chunk context before embedding and BM25 indexing; reduces retrieval failures by ~49%, or ~67% with reranking — [anthropic.com/news/contextual-retrieval](https://www.anthropic.com/news/contextual-retrieval) |
| Vector-only retrieval (no reranking) | Semantically plausible but suboptimal chunks | Add cross-encoder (BGE v2-m3, Cohere Rerank 3.5) or ColBERT reranker over top-k |
| Embedding rot (stale embeddings) | Silent drift toward hallucination | Re-embed on model update; version embeddings |
| No retrieval evaluation | Cannot detect degradation | Track Recall@20 ≥ 0.80 and Precision@5 ≥ 0.70 |
| Domain-mismatched embeddings | Weak representations for specialized content | Fine-tune or benchmark domain-specific models |
| Ignoring chunk overlap | Adjacent context lost at boundaries | 10-20% overlap between chunks |

## Chunking-Aware Retrieval Spec

```yaml
RAG_RETRIEVAL_SPEC:
  chunking:
    strategy: "[fixed-size / semantic / recursive / document-aware]"
    chunk_size: "[256-1024 tokens typical]"
    overlap: "[10-20% of chunk_size]"
  retrieval:
    method: "[vector / hybrid / multi-stage]"
    top_k_initial: 20
    top_k_reranked: 5
  reranking:
    model: "[cross-encoder / cohere-rerank / none]"
    threshold: "[minimum score to include]"
  context_assembly:
    max_tokens: "[context window budget]"
    dedup: true
    ordering: "[relevance / chronological / source-grouped]"
```

## Multi-Stage Retrieval

```
Stage 1: Sparse retrieval (BM25) → 100 candidates
Stage 2: Dense retrieval (vector) → 100 candidates
Stage 3: Fusion (RRF) → Top 50
Stage 4: Reranking (cross-encoder) → Top 10
Stage 5: Context assembly → Final context for LLM
```
