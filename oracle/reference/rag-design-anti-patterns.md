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

**"GraphRAG" is a family, not a technique.** They differ in what they cost to build and what they can prove:

| Variant | Retrieval shape | Build cost | Best for |
|---------|----------------|-----------|----------|
| Existing knowledge graph | traverse a curated graph | low (already built) | domains with a maintained ontology |
| Text-to-KG extraction | LLM builds the graph from the corpus | **high, and recurring on every corpus update** | stable corpora worth the extraction pass |
| Text-centric, graph-guided | passages retrieved, graph only steers expansion | low | multi-hop where the answer text still lives in passages |
| Community-based global | summarize clusters, answer from summaries | high build, cheap query | "what are the themes across everything" |
| Hierarchical summary | multi-level rollups | medium | corpus too large to read, questions at varying altitude |
| Memory-graph retrieval | entities/episodes accumulated across sessions | ongoing | recall about *this* user or system, not about a corpus |

**Decision rule: never adopt "GraphRAG" by name.** Choose on three axes — the **question type** (passage
lookup vs multi-hop vs global synthesis), the **construction and update cost** (extraction reruns on every
corpus change are the dominant lifetime cost, not query time), and whether the answer must **backtrace to a
source** (a community summary usually cannot; a passage can). If the question type is passage lookup, vector
retrieval wins and the graph is pure tax.

**Construction quality is the hidden failure surface.** Extraction precision/recall on entities and
relations, entity collision (two things merged) vs fragmentation (one thing split), edge audit sampling, and
community stability across rebuilds — a graph nobody measured is a confident-looking source of false
relations. Collision and fragmentation are **not symmetric**: for anything feeding a permission or safety
decision, bias resolution toward fragmentation (deny/miss) over collision (merge/over-permit).

**Graph retrieval has its own bias.** Vector retrieval skews to whatever embeds near the query; graph
retrieval skews to **high-degree hubs and short paths** — popular nodes appear in every answer regardless of
relevance. Normalize by degree, require path diversity, and run counterevidence queries; this is a different
axis from result-position bias and is not fixed by the same debiasing.

**Selection beats integration when the margin is small.** Running every route in parallel and fusing is the
expensive default. Compare on a Pareto frontier — quality, p95 latency, cost per query — and if hybrid buys
half a point for ten times the cost, route to one engine instead. Falling back (graph timeout → vector or
lexical) is fine, but record `graph_unavailable` in the answer's limitations rather than silently degrading.

## Oracle Gates

- no Retrieval SLO -> block at `DESIGN`
- fixed-size-only chunking -> require semantic review (or late chunking proposal for context-sensitive corpora)
- "accuracy" as sole metric -> require 3-tier evaluation
- no reranker -> require ROI analysis (consider ColBERT-style late interaction as a reranker-light alternative)
- multi-hop questions on entity-rich data without a GraphRAG variant proposed -> require justification
- premium + cheap retrieval tiers needed but no Matryoshka-compatible embedding selected -> require justification
