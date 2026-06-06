# Search Quality Evaluation Reference

Purpose: Run a disciplined offline + online evaluation program for ranking quality. Offline metrics (nDCG, MRR, MAP, Precision@k, Recall@k) catch regressions pre-deploy; online signals (CTR, position-bias-corrected engagement, reformulation rate) catch what judgments miss. Without both, ranking changes ship blind.

Read when: setting up search quality measurement, curating a golden query set, choosing a click model, designing a ranking A/B test, or wiring regression gates for retrieval / re-ranker changes.

## Scope Boundary

- **Seek `eval`**: search retrieval evaluation — ranking quality metrics, golden-query sets, click models, offline + online methodology.
- **Experiment (separate skill)**: general A/B test statistics — power, sample size, SRM detection, CUPED variance reduction. Seek `eval` provides the metric; Experiment provides the stat framework.
- **Oracle `eval` (separate skill)**: LLM-output evaluation — faithfulness, grounding, factuality, hallucination detection. Applies to generation quality, not retrieval quality. Separate domain — do not conflate.

Rule of thumb: if you are judging "is this document relevant to the query?" → Seek `eval`. If you are judging "is the LLM's answer grounded in the retrieved context?" → Oracle `eval`.

---

## Offline Metrics

Canonical source of truth for ranking metrics in the Seek skill. Other Seek references (`rerank-design.md`, etc.) point here rather than redefining.

| Metric | Formula | When to use | Typical target |
|--------|---------|-------------|----------------|
| Precision@k | Relevant in top-k / k | False positives costly (one-shot answer, legal, medical) | P@5 ≥ 0.70 (0.80 for high-stakes) |
| Recall@k | Relevant in top-k / total relevant | Completeness matters (RAG candidate pool, patent search) | R@20 ≥ 0.80 (≥ 0.90 for RAG) |
| MRR | mean(1 / rank of first relevant) | Single-answer / known-item search (FAQ, navigation) | MRR ≥ 0.60 (≥ 0.70 high-bar) |
| MAP | mean AP across queries | Overall ordering quality, binary judgments | MAP ≥ 0.50 |
| nDCG@k | `DCG@k / IDCG@k` where `DCG@k = Σ relevance_i / log2(i + 1)` for i=1..k | Graded relevance (3- or 5-point) — production default for product / web search | nDCG@10 ≥ 0.70 baseline, ≥ 0.85 high-traffic |

Graded judgments (0-3 or 0-4) unlock nDCG and are worth the annotation cost; binary-only setups miss the "good but not perfect" signal that drives most ranking improvements.

---

## Golden-Query Set

Curate **50-200 representative queries** covering:

- Head queries (top 10% by volume) — weighted heavily.
- Torso queries (next 30%) — coverage of the long body.
- Tail queries (random sample) — regression safety.
- Known-hard queries (typos, ambiguous intent, multi-term).
- Zero-result queries — verify fallback behavior.
- Category-balanced samples (so a single vertical does not dominate the metric).

For each query, collect 20-50 candidate docs and grade them. Rotate and refresh 10-20% quarterly — query distributions drift.

### Manual Annotation

```yaml
JUDGMENT_SET:
  size: 100-200 queries
  annotators: 2-3 per query (for inter-annotator agreement, target κ ≥ 0.6)
  scale:
    0: "Not relevant"
    1: "Partially relevant"
    2: "Highly relevant"
    # Extend to 0-3 or 0-4 for nDCG sensitivity
  format:
    - query: "how to reset password"
      judgments:
        - doc_id: "doc_123"
          relevance: 2
          annotator: "A"
        - doc_id: "doc_456"
          relevance: 1
          annotator: "A"
```

Gold standard, expensive. Annotator pool of one (κ < 0.4) means the judgments themselves are noise — always use ≥ 2 annotators with disagreement adjudication.

### LLM-as-Judge

Cheap, acceptable if agreement κ ≥ 0.6 against 20-50 expert-labeled calibration pairs.

```python
JUDGE_PROMPT = """
Rate the relevance of the following document to the query.

Query: {query}
Document: {document}

Rate on a scale of 0-2:
0 = Not relevant
1 = Partially relevant
2 = Highly relevant

Respond with only the number.
"""

async def llm_judge(query: str, document: str) -> int:
    response = await llm.generate(
        JUDGE_PROMPT.format(query=query, document=document)
    )
    return int(response.strip())
```

### Click-Derived Pseudo-Labels

Weak signal — always pass through a click model (next section) for debiasing before treating as relevance.

```sql
-- Click-through rate as weak relevance signal (debias with click model before use)
SELECT
  query,
  result_id,
  clicks::float / impressions AS ctr,
  avg_position,
  CASE
    WHEN clicks::float / impressions > 0.1 THEN 2
    WHEN clicks::float / impressions > 0.03 THEN 1
    ELSE 0
  END AS estimated_relevance
FROM search_analytics
WHERE impressions > 10
GROUP BY query, result_id;
```

### Golden Query File Format

```jsonl
{"query": "wireless headphones", "expected_top_3": ["prod_123", "prod_456", "prod_789"], "min_ndcg": 0.8}
{"query": "ワイヤレスイヤホン", "expected_top_3": ["prod_123", "prod_456"], "min_ndcg": 0.7}
{"query": "bluetooth earbuds noise cancelling", "expected_top_3": ["prod_789", "prod_012"], "min_ndcg": 0.75}
```

---

## Click Models

Raw CTR is biased: position 1 gets clicks whether or not it is the best result. Debias with an explicit click model:

| Model | Assumption | Use when |
|-------|-----------|----------|
| Cascade | User scans top-down, stops at first click | Short result lists, one-click intent |
| Position-Based Model (PBM) | Click = examination × relevance, examination depends only on position | Default — simple and robust |
| Dynamic Bayesian Network (DBN) | Adds perseverance parameter after click | Long sessions, multi-click queries |
| User Browsing Model (UBM) | Examination depends on distance from last click | Mixed browsing behavior |

Output: a debiased relevance estimate per (query, doc) pair, usable as training signal for `rerank` and as a pseudo-judgment for nDCG.

---

## Online Signals

Offline metrics miss novelty, diversity, and actual user satisfaction. Track online:

- **CTR@k** (position-bias-corrected).
- **MRR of clicks** — proxy for how deep users scan before clicking.
- **Abandonment rate** — sessions with zero clicks (bad signal, but confounded by "user found answer in snippet").
- **Query reformulation rate** — user refines within 30s (strong bad signal).
- **Dwell time** on clicked result — proxy for satisfaction (>30s = good).
- **Result-page return rate** — user comes back and clicks another result (bad).
- **Null-result rate** — queries with zero hits (critical for tail coverage).

---

## Offline Evaluation Pipeline

```python
class SearchEvaluator:
    def __init__(self, judgment_set: dict, search_fn):
        self.judgments = judgment_set
        self.search = search_fn

    def evaluate(self, k: int = 10) -> dict:
        metrics = {"ndcg": [], "mrr": [], "precision": [], "recall": []}

        for query, expected in self.judgments.items():
            results = self.search(query, top_k=k)
            result_ids = [r.id for r in results]

            metrics["ndcg"].append(self._ndcg(result_ids, expected, k))
            metrics["mrr"].append(self._mrr(result_ids, expected))
            metrics["precision"].append(self._precision(result_ids, expected, k))
            metrics["recall"].append(self._recall(result_ids, expected, k))

        return {name: sum(vals)/len(vals) for name, vals in metrics.items()}
```

---

## A/B Test Design for Ranking

Ranking changes are harder to A/B than feature changes. Patterns:

- **Interleaving** (Team-Draft Interleaving, TDI): mix rankings A and B into a single list, attribute clicks. 10-100× more sensitive than split traffic; preferred when applicable.
- **Split traffic**: standard 50/50 when ranker change affects latency or UI. Use CUPED (Experiment skill) to reduce variance.
- **Switchback**: alternate ranker per time window — use when personalization cross-contamination is a risk.
- **Shadow mode**: score both rankers, serve ranker A, log ranker B's top-K. Catches catastrophic regressions pre-launch.

Delegate power analysis, sample-size calculation, SRM detection, and variance-reduction to `Experiment`. Seek `eval` supplies the metric (interleaving win-rate or Δ-CTR with position correction) and the click model.

### Interleaving Example

```
Control results:   [A, B, C, D, E]
Treatment results: [C, F, A, G, B]
Interleaved:       [A, C, B, F, D, G, E]
                    ↑C ↑T ↑C ↑T ↑C ↑T ↑C

User clicks on C (position 2, from Treatment) → Treatment wins this impression
```

### Standard A/B Design Spec

```yaml
AB_TEST_DESIGN:
  method: interleaving  # Preferred for search A/B tests
  variants:
    control: "Current search configuration"
    treatment: "New ranking/retrieval changes"
  metrics:
    primary: "Interleaving win-rate (or position-bias-corrected CTR@3)"
    guardrail: "Zero-result rate must not increase > 5%"
  duration: "2 weeks minimum"
  traffic_split: "50/50"
  significance: "p < 0.05"
```

---

## Reranker Evaluation Hooks

When evaluating a Stage-2 re-ranker (see `rerank-design.md` for model selection and pipeline), reuse this skill's metric definitions and click-model output:

- **Acceptance metric set**: nDCG@10, MRR, Recall@K of the re-ranked top-K, plus position-bias-corrected online CTR.
- **Training data**: feed the debiased relevance estimates from the click-model output (PBM/DBN) into LambdaMART or cross-encoder fine-tuning.
- **Regression gate**: shadow-score new re-ranker against production traffic for 1-3 days, then interleaving A/B; require win-rate > 55% with p < 0.05.
- **Leakage rule**: never train the re-ranker on the same queries used in the golden set. Same-query (q, doc) pairs across train/eval = leakage.

The re-ranker design owns model choice, latency budget, and feature engineering; `eval` owns the metric, the click-model debiasing, and the gating thresholds.

---

## Evaluation Workflow

```
1. Build golden set (50-200 queries, graded 0-3).
2. Baseline: run current ranker on golden set → nDCG@10, MRR, Recall@20.
3. Candidate ranker: same run → Δ metrics.
4. If Δ nDCG@10 > +1% absolute AND no per-category regression > 2% → proceed.
5. Shadow-score in production for 1-3 days — watch null-result and latency.
6. Interleaving A/B → win-rate with 95% CI (Experiment).
7. Gate: interleaving win-rate > 55% with p < 0.05 → ship.
8. Post-launch: monitor nDCG drift weekly, CTR + reformulation daily.
```

---

## Regression Testing

### Relevance Regression Test

```yaml
REGRESSION_TEST:
  trigger: "On index mapping, analyzer, embedding model, or ranker change"
  golden_set: "tests/search/golden_queries.jsonl"
  thresholds:
    ndcg_at_10: ">= 0.72"
    mrr: ">= 0.65"
    zero_result_rate: "<= 0.05"
  action_on_failure: "Block deployment, alert search team"
```

Snapshot nDCG per query per ranker commit and hand off to `Radar` for the executable test suite.

---

## Diagnostic Queries

When search quality drops, investigate with:

```yaml
DIAGNOSTIC_CHECKLIST:
  - Zero-result queries: "What queries return no results?"
  - Low-click queries: "What queries have CTR < 1%?"
  - Position bias: "Are users only clicking position 1?"
  - Query reformulation: "Are users rephrasing queries?"
  - Filter impact: "Do filters eliminate too many results?"
  - Freshness: "Are stale documents ranked too high?"
  - Language mismatch: "Are Japanese queries matching English docs?"
```

---

## Anti-Patterns

- Single aggregate nDCG with no per-segment breakdown — hides category-level regressions.
- Training the ranker on the same queries used for evaluation (leakage).
- Ignoring position bias and declaring CTR uplift a win.
- No zero-result monitoring — a "better" ranker that also increases null-rate is a loss.
- Annotator pool of one — inter-annotator agreement κ < 0.4 means the judgments themselves are noise.
- Metric monoculture — shipping on nDCG alone, ignoring recall degradation for RAG candidate pools.
- Conflating Seek `eval` (ranking quality) with Oracle `eval` (LLM faithfulness) — they measure different stages of the RAG pipeline.

---

## Paired Deliverables

Every `eval` program ships:

1. Golden-query set spec: query selection, annotation rubric, grade scale.
2. Offline metric plan: primary (nDCG@k) + secondary (MRR, Recall@k), per-segment breakdown.
3. Click-model choice + debiasing pipeline.
4. Online signal dashboard spec.
5. A/B design (interleaving vs split + variance reduction) — cross-ref to `Experiment`.
6. Regression-gate thresholds with per-segment floors.

---

## Handoff

- To `Experiment`: stat framework — power, sample size, SRM, CUPED. Provide the metric definition.
- To `Radar`: regression test suite — snapshot nDCG per query per ranker commit.
- To `Beacon`: SLO for retrieval quality (nDCG drift > threshold → alert) and null-result rate.
- To `Stream`: click-log + judgment-log ingestion with session / position / dwell fields.
- To `Builder`: logging schema in the serving path — query, ranker version, shown docs, positions, click events.
- Boundary with Oracle `eval`: Seek `eval` ends at the ranked list; Oracle `eval` starts at the LLM-generated answer. Cross-link, do not overlap.
