Purpose: Use this file when you are choosing a RAG architecture, defining retrieval quality gates, or auditing RAG anti-patterns.

## Contents
- Architecture taxonomy
- Hybrid Search default
- Chunking and index choices
- RAG anti-patterns
- Evaluation model
- Oracle gates

# RAG Design And Anti-Patterns

## Architecture Taxonomy

| Architecture | Best for | Complexity |
|--------------|----------|------------|
| Vanilla RAG | simple FAQ and Q&A | Low |
| Hybrid RAG | production default | Medium |
| Self-RAG | high factuality with self-checks | Medium |
| Corrective RAG | reliability-critical retrieval recovery | Medium |
| GraphRAG | multi-hop reasoning and global summaries | High |
| Agentic RAG | dynamic multi-step retrieval; brings irrelevant-chunk rate from ~`40%` down to `<8%` on multi-hop benchmarks (2026 surveys) | High |
| Multi-Agent RAG | enterprise multi-domain knowledge | Very high |

Decision flow (2026):
- simple single-corpus Q&A -> Hybrid RAG
- multi-hop reasoning or global summarization -> GraphRAG (Microsoft GraphRAG: entity / relationship graph + multi-level community summaries)
- dynamic strategy adaptation -> Agentic RAG
- self-correction and factuality priority -> Self-RAG or Corrective RAG
- entity-rich relational data -> GraphRAG; question routing across heterogeneous sources -> Agentic RAG

> The 2026 industry consensus narrows production choices to three dominant shapes: **Naive (Vanilla / Hybrid) RAG**, **Agentic RAG**, and **GraphRAG**. Treat anything else as research or a specialisation of one of these three.

## Hybrid Search Default

Production default:
1. query expansion or rewrite
2. dense vector search
3. BM25 keyword search
4. reciprocal-rank fusion
5. cross-encoder reranking
6. top `5-8` chunks for context assembly
7. LLM generation

Single highest-ROI improvement: reranking.

## Chunking And Index Choices

| Strategy | Best for | Size guide |
|----------|----------|------------|
| Fixed-size | general docs | `500-1000` tokens, `50-100` overlap |
| Semantic | long docs with topic shifts | variable by boundary |
| Paragraph | structured docs | `200-500` tokens |
| AST-based | source code | function / class level |
| Hierarchical | complex docs | parent summary + child chunks |
| **Late chunking** (2026 default for context-sensitive corpora) | long docs where chunks must retain full-document context | embed the whole document; pool token-level attention into chunk embeddings; pair with a ColBERT-style late-interaction reranker for highest fidelity |

Rules:
- avoid naive fixed `512`-token splitting without heading preservation;
- preserve document structure for semantic chunking;
- separate indexes by domain when content differs materially;
- if pronouns, definitions, or cross-references span chunk boundaries, prefer late chunking + late interaction over more aggressive overlap.

### Embedding And Vector DB Selection (2026-05 snapshot)

- cost-sensitive simple queries -> `text-embedding-3-small`
- long documents -> `voyage-3` (or `voyage-3-lite` for cost-bounded)
- multilingual -> `Cohere embed-v3` or `BGE-M3`
- highest quality -> `text-embedding-3-large`
- self-hosted -> `BGE-M3`
- **Matryoshka-trained embeddings** -> store at full dimension (e.g., `3072`) for retrieval-critical paths and truncate to `512` / `768` / `1024` for latency- or cost-bounded paths without re-embedding. Default to Matryoshka-compatible models when the system needs both a "premium" and "cheap" retrieval tier.
- **Late-interaction retrievers** (ColBERT v2 family, ColPali for visual docs) -> pair with dense retrieval when reranker budget is tight; they are reranker-grade quality at retrieval-grade latency.

- `<10k` docs or prototype -> `ChromaDB`
- existing PostgreSQL -> `pgvector` (HNSW + half-precision is the default production knob)
- managed production -> `Pinecone`
- self-hosted production -> `Qdrant` or `Weaviate`
- Hybrid Search native fit -> `Weaviate`

## RAG Anti-Patterns

| ID | Anti-pattern | Symptom | Fix |
|----|--------------|---------|-----|
| `RP-01` | retrieval as afterthought | RAG bolted onto a PoC | design retrieval as first-class system with SLOs |
| `RP-02` | naive fixed chunking | blind splits | semantic chunking with heading preservation |
| `RP-03` | monolithic index | all content in one store | split by domain |
| `RP-04` | prompt-heavy, query-light | query pipeline ignored | add rewrite, intent classification, clarification |
| `RP-05` | no evaluation framework | no Recall@K / Precision@K | use 3-tier evaluation |
| `RP-06` | knowledge-base chaos | contradictory or outdated docs | versioning and conflict detection |
| `RP-07` | direct live data connection | unsafe live-source dependency | static / periodic / on-demand tiers |
| `RP-08` | no guardrails | unsafe retrieval/use | source whitelisting and output validation |
| `RP-09` | context overload | entire docs in prompt | top `5-8` chunks only |
| `RP-10` | no reranking | raw retrieval order used | add reranker |
| `RP-11` | retrieval breadth as a proxy for accuracy | dumping a large raw corpus (e.g. grep over 1000+ prior queries/files) into context, expecting accuracy to rise | the bottleneck is concept→entity *mapping*, not access — curate canonical sources + a semantic/definition layer; raw breadth alone moves accuracy `<1%` |

> **Mapping over access** [Source: claude.com — *How Anthropic Enables Self-Service Data Analytics with Claude*]: in a production analytics agent, giving the model raw access to 1000+ historical SQL files improved accuracy by `<1%` — the correct information was present but unmapped. Accuracy came from curated canonical datasets + a compiled semantic layer (definitions as the highest-trust source), not from widening retrieval. When an agent underperforms, suspect ambiguous concept-to-entity mapping before adding more documents to the index.

## Cascade Failure Model

If retrieval, reranking, generation, and guardrails each run at `95%`:
- end-to-end reliability drops to about `81%`.

Independent gates:
- `Recall@5 >= 0.8`
- `Precision@5 >= 0.7`
- `Faithfulness >= 0.8`
- policy violations `< 1%`

## RAG Evaluation

| Tier | Metrics | Threshold |
|------|---------|-----------|
| Retrieval | `Recall@K`, `Precision@K`, `MRR`, `NDCG` | `Recall@5 >= 0.8`, `Precision@5 >= 0.7` |
| Generation | Faithfulness, relevancy, answer correctness | `Faithfulness >= 0.8` |
| Task | deflection, handle time, CSAT | task-specific |

Anti-patterns:
- regenerated test sets
- retrieval and generation scored as a single unit
- vague “accuracy” without component metrics

## GraphRAG Guidance

Use GraphRAG when:
- the answer needs synthesis across many documents,
- the question requires multi-hop reasoning,
- global themes matter more than passage lookup.

## Oracle Gates

- no Retrieval SLO -> block at `DESIGN`
- fixed-size-only chunking -> require semantic review (or late chunking proposal for context-sensitive corpora)
- "accuracy" as sole metric -> require 3-tier evaluation
- no reranker -> require ROI analysis (consider ColBERT-style late interaction as a reranker-light alternative)
- multi-hop questions on entity-rich data without a GraphRAG variant proposed -> require justification
- premium + cheap retrieval tiers needed but no Matryoshka-compatible embedding selected -> require justification
