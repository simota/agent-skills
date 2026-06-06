# LLM Cost Optimization Reference

Purpose: Tune LLM-API spend without regressing eval scores. Covers per-feature token budget, prompt caching, model-tier routing (haiku / sonnet / opus), batch API vs streaming, context compression, and SLO-backed budget alerts.

## Scope Boundary

- **Oracle `cost`**: LLM-API cost only — tokens in/out, model tier, prompt / semantic caching, batch API, streaming. Scope ends at the LLM provider bill.
- **Ledger (elsewhere)**: cloud infra FinOps — EC2, S3, RDS, vector-DB hosting, GPU node right-sizing, RI/SP, anomaly detection across the cloud bill. Scope starts at the provider bill.

Route to `Ledger` when the question is "is our vector DB oversized?" or "should we reserve GPU capacity?". Stay in Oracle `cost` when the question is "should we cache this prompt?" or "should we route this feature to Haiku?".

## Core Contract

- Every feature ships with a per-feature token budget and a cost dashboard, not just a global spend number.
- Budget alert at `> 120%` forecast; cost-per-query alert at `> 2×` baseline.
- Cheapest viable model first, escalate only on validation failure. Premium models (Opus) should handle `~10%` of queries.
- Stable prompt prefixes come FIRST so prompt caching works; variables go LAST.
- Combined techniques (model routing + prompt cache + semantic cache + batch) land at `70-90%` total savings.

## Token Economics

| Model | Input / 1M | Output / 1M | Speed | Quality | Default use |
|-------|------------|-------------|-------|---------|-------------|
| Claude Opus 4.7 | `$15.00` | `$75.00` | Slow | Highest | Deep reasoning, `~10%` of traffic |
| Claude Sonnet 4.6 | `$3.00` | `$15.00` | Medium | High | Production default |
| Claude Haiku 4.5 | `$0.80` | `$4.00` | Fast | Good | Classification, extraction, tier-1 routing |
| GPT-4o | `$2.50` | `$10.00` | Medium | High | Cross-vendor fallback |
| GPT-4o-mini | `$0.15` | `$0.60` | Fast | Good | High-volume extraction |

Formula: `monthly cost = (input cost + output cost) × requests/day × 30`. Always compute this per feature before shipping.

## Workflow

```
PROFILE   →  measure baseline: tokens in/out, p50/p95 latency, model mix
          →  attribute cost to feature (chat / summarize / search-rerank)
          →  list repetition patterns (stable system prompt, long context)

DESIGN    →  pick default tier (Haiku default, Sonnet on fail, Opus on verify)
          →  set prompt-cache strategy: static prefix first, cache_control breakpoints
          →  decide: streaming (UX SLA < 2s TTFT) vs batch (async, 50% cheaper)
          →  plan semantic cache (similarity >= 0.8) if traffic has repeats

EVALUATE  →  A/B the cheaper route against eval suite; block regression >= 5%
          →  measure cache hit rate; prompt cache should land 45-80% cost/13-31% TTFT
          →  validate batch SLA: finish window fits downstream consumer

SPECIFY   →  hand to Builder: routing logic, cache keys, batch cadence, budget alerts
```

## Prompt Caching (Anthropic)

- **5-minute TTL (default)**: cache stable system prompts, few-shot examples, long context. Cache read = `10%` of input cost. Typical agentic multi-turn sessions land `45-80%` cost reduction and `13-31%` TTFT reduction.
- **1-hour TTL (extended)**: high-stability prefixes (product docs, tool definitions). Costs more to write but persists longer; break even at ~2 hits per hour.
- **Ordering rule**: `system prompt → tool defs → long context → examples → user variable input`. Put `cache_control` on the last token of each stable block.

## Model Routing Patterns

| Pattern | How | Savings |
|---------|-----|---------|
| Fixed tier | Every request → one model | Baseline |
| Task-based routing | Classifier picks tier from task type | `~87%` cost reduction vs all-Opus |
| Cascade (escalation) | Run Haiku first; escalate on low confidence | `~14%` better cost-quality vs fixed |
| Self-consistency escape | Run Haiku 3× vote; escalate if disagreement | Good for high-stakes classification |

Decision cues: routing classifier itself must be cheap (regex / tiny model), else it eats the savings.

## Batch API vs Streaming

| Mode | Cost | Latency | Use when |
|------|------|---------|----------|
| Streaming | Full | TTFT `~500ms`, tokens live | Chat UX, agentic loop feedback |
| Sync non-streaming | Full | Full response before return | Structured output, tool calls |
| Batch API | `-50%` | Up to 24h window | Backfills, nightly summarization, offline eval |

Never put Batch in a user-facing synchronous path. Always put Batch behind an existing async queue.

## Context Compression

- Drop stale tool outputs before each turn.
- Summarize scratchpad at `60%` of context window.
- Replace raw documents with extracted fields when only fields matter.
- For long agentic sessions, compact using a Haiku summarization pass instead of feeding the full transcript.

## Semantic Cache

- Similarity threshold `>= 0.8`; hit rate target `>= 60%` (practical `60-85%`).
- High-repetition workloads (FAQ, classification): up to `73%` cost reduction, `96.9%` latency reduction on cache hits.
- Always attach a version/freshness key — stale cache serving deprecated prices or policies is a worse failure than paying for the call.

## Dashboard Thresholds

- daily spend `> 120%` of budget → alert
- cost per query `> 2×` baseline → alert
- cache hit rate `< 50%` of expected → investigate
- wasted-token cost `> 5%` of total → investigate (retry loops, oversize `max_tokens`)
- unexpected thinking-token spikes → investigate

## Anti-Patterns

- Putting variable user input FIRST in the prompt (breaks prompt caching).
- Defaulting every feature to Opus "to be safe" — `~90%` of traffic does not need it.
- Shipping `max_tokens: 4096` everywhere — output tokens are the expensive axis.
- Treating semantic cache like an exact cache without a freshness key.
- Measuring only global monthly spend — you cannot optimize what you cannot attribute.
- Moving user-facing requests into Batch API to "save money" — it breaks UX SLA.

## Oracle Gates

- No cost estimate → block; require per-feature budget projection.
- Opus for simple extraction/classification → block; require routing justification.
- No caching strategy on stable prompts → block; require prompt-cache plan.
- `max_tokens` default without need analysis → block; require right-sizing.
- No per-feature attribution dashboard → block.

## Handoff

| To | Include |
|----|---------|
| Builder | Routing decision tree, cache key design, `cache_control` placement, budget alert thresholds, rollback to previous tier |
| Beacon | Cost + cache-hit dashboards, `> 120%` budget alert, `> 2×` baseline alert |
| Radar | Eval suite that blocks merges on `>= 5%` quality regression after routing change |
| Ledger | If the non-LLM infra cost (vector DB hosting, GPU inference fleet, egress) dominates the bill |
