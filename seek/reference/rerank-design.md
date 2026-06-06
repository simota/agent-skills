# Re-ranking Design Reference

Purpose: Design a second-stage re-ranker that improves precision at the top of any retrieval result set — BM25, vector, or hybrid. The first stage optimizes recall with cheap scoring over millions of candidates; the re-ranker spends more compute on the top-N to sharpen ordering. Applicable to product search, log search, internal docs search, and RAG retrieval alike.

## Scope Boundary

- **Seek `rerank`**: second-stage re-ranking design for any retrieval system. Model selection (cross-encoder, LTR), feature engineering, latency budget, click-feedback loop, offline training pipeline.
- **Seek `rag` (separate)**: full RAG retrieval layer — chunking, multi-stage retrieval, context assembly. `rag` embeds `rerank` as its final sharpening step; it does not replace it.
- **Oracle `embed` (separate skill)**: LLM-RAG embedding layer — chunk → embed → retrieve against vector store. Defers to Seek `rerank` whenever re-ranker depth is needed.

If the question is "does the top-K contain the right answer?" → `rerank`. If it is "are we retrieving the right candidate pool at all?" → `vector` / `hybrid`.

## Model Selection

| Approach | Typical model | Strength | Weakness |
|----------|--------------|----------|----------|
| Cross-encoder | BGE Reranker v2-m3, Cohere Rerank 3.5, jina-reranker-v2 | Highest NDCG — joint query-doc attention | O(N) inference; 30-100ms for N=50 |
| Late interaction | ColBERTv2, jina-colbert-v2 | Precomputable doc vectors, token-level match | Storage cost — multi-vector per doc |
| Learning to Rank | LambdaMART (LightGBM LTR, XGBoost `rank:pairwise`) | Uses handcrafted features + click signals | Requires labeled / click data |
| LLM-as-reranker | Frontier LLM with listwise prompt | Zero-shot, explainable | Cost + latency — rarely production-viable |
| Cohere Rerank API | Cohere Rerank 3.5 (managed) | No infra, 100+ languages, multi-format | Vendor dependency, per-call cost |

**Cohere Rerank 3.5** (released Dec 2024): SOTA on multilingual retrieval and reasoning, supports lengthy documents, tables, JSON, code, and email formats, 4096 context length, available on Azure AI Foundry — [cohere.com/blog/rerank-3pt5](https://cohere.com/blog/rerank-3pt5)

Default picks:
- Cold start / no click data → **BGE Reranker v2-m3** (open, multilingual) or **Cohere Rerank 3.5**.
- Mature system with click logs → **LambdaMART** on engineered features — typically beats cross-encoder when signal is rich.
- Very large top-N (>200) → **ColBERT late interaction** (precomputed) or 2-tier (cross-encoder over top-50 of a fast reranker).

## Two-Stage Pipeline

```
Query
  └─ Stage 1: Recall-optimized retrieval
       └─ BM25 / vector / hybrid (RRF) → top-N candidates  (N = 50-200)
  └─ Stage 2: Precision-optimized re-ranking
       └─ Cross-encoder OR LambdaMART over (query, doc) pairs → top-K  (K = 5-20)
  └─ Final ranked list → UI / LLM context
```

Sizing rule: N should be large enough that recall@N is a ceiling on the achievable NDCG@K. Measure recall@50, recall@100, recall@200 offline before fixing N.

## Latency Budget

| Stage | Typical budget (P95) |
|-------|----------------------|
| Stage 1 retrieval | 20-80ms |
| Feature extraction (LTR) | 5-20ms |
| Stage 2 model inference | 30-100ms (cross-encoder, N=50) / 2-10ms (LambdaMART, N=100) |
| Total search request | 100-250ms end-to-end |

If the total P95 budget is <100ms (e.g. e-commerce instant search), cross-encoders over N>20 will blow it — pick LambdaMART or reduce N. Always batch Stage-2 scoring on GPU for cross-encoders.

## LambdaMART Feature Set

Effective LTR requires 20-80 features. Minimum set:

- **Textual**: BM25 score, TF-IDF score, field-level BM25 (title / body / tags), exact-match boolean, query-term coverage.
- **Semantic**: vector cosine similarity, ColBERT MaxSim.
- **Document quality**: popularity (log views), freshness (days since publish), authority (PageRank / inbound links), length.
- **Query-doc interaction**: term proximity, query-term position in title, category match.
- **Personalization** (if applicable): user-doc CTR prior, session dwell time, category affinity.

Train with `rank:pairwise` or `rank:ndcg` objective. Validate on held-out queries, not held-out (query, doc) pairs — same-query pairs leak.

## Click-Feedback Loop

Re-rankers degrade if not re-trained on fresh click data. Standard loop:

```
1. Log (query, shown_docs[], clicked_doc, position, dwell_time)
2. Debias clicks with a click model (Cascade / DBN / PBM) → implicit relevance
3. Merge with any explicit judgments from `eval`'s golden set
4. Retrain LambdaMART weekly / cross-encoder monthly
5. Shadow-score new model against production; promote via A/B (`Experiment`)
```

Without click-model debiasing, the reranker learns "position bias" — docs shown first get clicked more regardless of relevance, and the model reinforces the existing ranking. Always correct.

## Anti-Patterns

- Cross-encoder over N=500 on CPU — P95 blows past 500ms.
- Training LambdaMART on raw clicks without position-bias correction.
- Re-ranking the final K=10 only (too late — Stage 1 already dropped the right doc).
- Using the same judgment set for training and NDCG evaluation.
- Shipping a re-ranker without a rollback feature flag — re-rankers can silently regress NDCG when training data drifts.
- Treating Oracle `embed` as a re-ranker substitute — embeddings give you recall, not precision ordering.

## Paired Deliverables

Every `rerank` design ships:

1. Stage-1 retrieval spec (top-N, recall@N target).
2. Stage-2 model choice + rationale (cross-encoder / LTR / ColBERT).
3. Feature list (for LTR) or model ID + dimensions (for neural).
4. Latency budget table with per-stage P95.
5. Training / re-training plan: data source, click-model debiasing, cadence.
6. Evaluation hookup — defer metric definitions (nDCG@k, MRR, MAP, Precision@k, Recall@k), golden-query curation, and click-model selection to `reference/evaluation-methods.md`; A/B stat framework (power, SRM, CUPED) to `Experiment`.

## Handoff

- To `Builder`: feature-extraction pipeline, model-serving API (batched inference), fallback-to-Stage-1 behavior when the re-ranker times out.
- To `Stream`: click-log ingestion with session / position / dwell fields.
- To `eval` (Seek): NDCG@10, MRR, and position-bias-corrected online CTR as the acceptance metric set — full definitions, targets, and pipeline in `reference/evaluation-methods.md` (canonical metric source).
- To `Experiment`: A/B design — interleaving preferred over split traffic for ranking changes; reuse its CUPED variance reduction for low-traffic surfaces.
- From Oracle `embed` (inbound): when Oracle RAG design reaches "we need a re-ranker", it routes here; return a re-ranker spec that plugs into the RAG top-K.
