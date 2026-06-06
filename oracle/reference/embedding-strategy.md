# Embedding Strategy Reference

Purpose: Design the RAG embedding pipeline — the retrieval half that the generator reads. Covers text chunking, embedding model selection, vector index choice, cross-encoder re-ranking, and hybrid BM25+vector retrieval. `80%` of RAG failures trace to this layer, not to the generator.

## Scope Boundary

- **Oracle `embed`**: the embedding slice of the RAG pipeline — chunk, embed, index, retrieve, re-rank. Output is the top-k context passed to the generator.
- **Oracle `rag` (sibling)**: the full RAG pipeline — retrieval + generation + faithfulness evals + orchestration. `rag` hands off TO `embed` when chunking / indexing / re-rank is the bottleneck.
- **Seek (elsewhere)**: full-stack search architecture — query understanding, multi-index fan-out, faceting, relevance ops, A/B search. Scope includes non-LLM search products.

Route here when the diagnosis is "retrieval is missing the right chunk" or "Faithfulness dropped". Route to `Seek` when the product is a search engine, not an LLM answer pipeline. Route to `rag` for the end-to-end retrieve-then-generate architecture.

## Core Contract

- Thresholds: `Recall@5 >= 0.8`, `Precision@5 >= 0.7`, `Faithfulness >= 0.8`. Below these, the generator cannot compensate.
- Naive fixed-size chunking drops faithfulness to `0.47-0.51` vs `0.79-0.82` with benchmarked chunking — always benchmark.
- Re-ranking with a cross-encoder typically lifts nDCG@10 by `10-30%` for the same candidate pool.
- Hybrid (BM25 + dense) beats dense-only in most enterprise corpora where exact-term recall matters (IDs, SKUs, error codes).
- Version the index: (chunker_version, embedder_version, schema_version). Stale indexes silently degrade quality.

## Workflow

```
PROFILE   →  corpus: size, doc types, avg length, update cadence, query style
          →  labels: have eval set? (if not, build one — 50-200 Q/A pairs minimum)
          →  measure baseline: Recall@k, Precision@k, nDCG@10 on current retrieval

DESIGN    →  pick chunker (fixed / recursive / semantic / structural)
          →  pick embedder (domain fit, dimension, multilingual, cost)
          →  pick index (HNSW / IVF / flat) sized to corpus
          →  pick re-ranker (cross-encoder vs LLM-rerank; latency budget)
          →  decide hybrid: BM25 + dense with RRF fusion (k = 60 default)

EVALUATE  →  measure Recall@5, Precision@5, nDCG@10, Faithfulness against baseline
          →  sweep chunk size, overlap, k, re-rank cutoff — pick on eval, not vibe
          →  adversarial: paraphrase queries, inject distractors, test long-tail

SPECIFY   →  hand to Builder / Stream: ingestion spec with versioning, refresh plan
```

## Chunking Strategies

| Strategy | How | Use when | Skip when |
|----------|-----|----------|-----------|
| Fixed-size (tokens) | Split every N tokens with M overlap | Fast baseline, uniform prose | Loses semantic boundaries |
| Recursive | Split on hierarchy (paragraph → sentence → token) | Mixed docs, code + prose | Requires tuning per doc type |
| Semantic | Split at embedding-distance jumps | Long-form articles, books | Extra embed pass, higher cost |
| Structural | Split on headings / tables / list items | Markdown, docs, HTML | Unstructured text |
| Proposition | LLM extracts standalone facts as chunks | FAQ, claims, citations | Expensive at ingest |

Defaults: recursive with `chunk_size=512 tokens, overlap=64 tokens` for prose; structural for Markdown / HTML; proposition when the generator needs citations.

## Embedding Model Selection

| Model | Dim | Strength | Watch-out |
|-------|-----|----------|-----------|
| OpenAI text-embedding-3-large | 3072 | General English, long context | Dimension cost, no fine-tune |
| OpenAI text-embedding-3-small | 1536 | Cheap, good enough baseline | Weaker on domain jargon |
| Voyage voyage-3 / voyage-3-large | 1024 / 2048 | Strong on code + technical | Paid API |
| Cohere embed-v3 (English/multi) | 1024 | Multilingual, strong retrieval | API lock-in |
| bge-m3 (BAAI) | 1024 | Multilingual + dense/sparse/colbert unified | Self-host infra |
| nomic-embed-text-v2 | 768 | Open weights, fast | Smaller headroom |

Cue: if eval shows recall gap on domain jargon (medical / legal / code), try a domain-tuned embedder before tuning chunks.

## Vector Index Choice

| Index | Best for | Tradeoff |
|-------|----------|----------|
| Flat (brute force) | `< 100k` vectors | Exact, zero tuning, slow at scale |
| HNSW | `100k - 100M` vectors, low-latency | Memory-heavy, tuning params (M, efSearch) |
| IVF (+PQ) | `> 10M` vectors, memory-bound | Slight recall drop, cheaper RAM |
| ScaNN / DiskANN | Very large, disk-backed | Ops complexity |

Default: HNSW with `M=16-32, efConstruction=200, efSearch=64` as a starting point; benchmark efSearch vs Recall@10 on your eval set.

## Re-Ranking with Cross-Encoders

- Cross-encoders score (query, chunk) pairs and re-rank the top `N` from the retriever. Typical N = 20-100 candidates → return top `5-8`.
- Options: Cohere Rerank 3 / rerank-v3.5 (API), Voyage rerank-2 (API), bge-reranker-v2-m3 (self-host), jina-reranker-v2 (self-host).
- Latency budget: cross-encoder adds `50-200ms` for N=50 candidates at small batch size. If the product has a streaming-TTFT SLO, measure before committing.
- LLM-as-reranker (ask Sonnet/Haiku to rank) is an option when labelled data is scarce, but costs more and adds variance.

## Hybrid BM25 + Vector

- Run BM25 and dense retrieval in parallel over the same chunks.
- Fuse with Reciprocal Rank Fusion (RRF): `score(d) = sum(1 / (k + rank_i(d)))`, default `k = 60`.
- Hybrid wins most clearly when queries contain exact identifiers (error codes, SKUs, legal-statute numbers). Log a few production queries before dismissing BM25.
- Alternative: weighted linear fusion (`alpha * dense + (1-alpha) * sparse`) — tune alpha on eval.

## Anti-Patterns

- Shipping one chunk size for every doc type in a mixed corpus.
- Picking an embedder by leaderboard score without testing on your domain.
- Skipping re-ranking because "the embedder is good" — re-rank is usually the cheapest Recall@5 win.
- Ignoring BM25 on corpora full of identifiers, codes, or names.
- Running the same index through schema changes without a version bump — retrieval silently serves stale shapes.
- No eval set — every change becomes a vibe check.
- OWASP LLM08 blind spot: accepting chunks from untrusted sources without content validation (BadRAG / TrojanRAG poisoning).

## Oracle Gates

- No chunking benchmark → block; require at least two strategies measured side-by-side.
- No re-rank stage when latency budget allows one → require justification.
- No hybrid consideration on a corpus with identifier queries → require BM25 A/B.
- No index-version scheme → block; require (chunker, embedder, schema) version tuple.
- No vector-input validation → require poisoning-defense plan (Sentinel handoff).

## Handoff

| To | Include |
|----|---------|
| Oracle `rag` | Retrieval-layer specs (chunker, embedder, index, re-rank, fusion), Recall/Precision/Faithfulness baseline; `rag` composes the end-to-end pipeline |
| Stream | Ingestion pipeline spec — chunk cadence, re-embed triggers, schema version, backfill plan |
| Builder | Retrieval API contract (top_k, filters, score cutoff), cache rules, fallback behavior |
| Radar | Eval harness: Q/A set, Recall@5, Precision@5, Faithfulness, adversarial distractor tests |
| Sentinel | Vector-input validation rules, poisoning-defense (BadRAG / TrojanRAG), PII-scrub at ingest |
| Seek | If the product scope is a full search engine (query understanding, faceting, multi-index fan-out), not an LLM-RAG pipeline |
