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

> Claude rows verified against `platform.claude.com/docs/en/about-claude/pricing` on **2026-07-25**. Non-Anthropic rows still need verification — check each vendor's official page before quoting.

| Model | Input / 1M | Output / 1M | Speed | Quality | Default use |
|-------|------------|-------------|-------|---------|-------------|
| Claude Fable 5 | `$10.00` | `$50.00` | Slow | Highest | Frontier reasoning, long-running agents |
| Claude Opus 5 | `$5.00` | `$25.00` | Moderate | Highest | Complex agentic coding, `~10%` of traffic |
| Claude Sonnet 5 | `$2.00` → `$3.00` | `$10.00` → `$15.00` | Fast | High | Production default (intro pricing through 2026-08-31, then standard) |
| Claude Haiku 4.5 | `$1.00` | `$5.00` | Fastest | Good | Classification, extraction, tier-1 routing |
| GPT-5.5 | `TBD (needs confirmation)` | `TBD (needs confirmation)` | Medium | High | Cross-vendor fallback |
| GPT-4o-mini | `$0.15` | `$0.60` | Fast | Good | High-volume extraction |
| Gemini 3.6 Flash (High) | `TBD (needs confirmation)` | `TBD (needs confirmation)` | Fast | Good | High-volume extraction (Gemini) |

Claude cost modifiers (multiply the base rates above):

| Modifier | Effect |
|----------|--------|
| Batch API | **0.5×** input and output (Opus 5 → `$2.50` / `$12.50`) |
| Cache write, 5 min | 1.25× input |
| Cache write, 1 h | 2× input |
| Cache read (hit) | **0.1×** input — pays off after one read on the 5-min tier |
| Fast mode (research preview, Opus 5 only) | 2× both (`$10` / `$50`); stacks with caching, excludes Batch |
| `inference_geo: "us"` | 1.1× all categories |
| 1M context window | **No premium** — a 900k-token request bills at the same per-token rate as 9k |

Minimum cacheable prompt on Opus 5 is **512 tokens**, so short system prompts now cache.

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
- **Minimum cacheable prompt is 512 tokens on Opus 5** (down from 1,024), so short system prompts now cache.
- **Three silent invalidators** — each renders into the prompt, so changing it mid-conversation costs a full cache write instead of a 0.1× read: (1) `effort`; (2) the `tools` array (Opus 5 lifts this with the `mid-conversation-tool-changes-2026-07-01` beta); (3) `task_budget` if you mutate it per turn. Pick each once per conversation. `defer_loading: true` tools are exempt — they never enter the cached prefix.

## Agentic Loop Cost Control

Four levers, in the order to reach for them. Verified 2026-07-25.

| Lever | What it bounds | Hard or soft |
|-------|---------------|--------------|
| `effort` | Reasoning **depth per step** — and all tokens, including tool-call volume | Soft, calibrated |
| `task_budget` (beta `task-budgets-2026-03-13`) | Total **breadth across the loop** — thinking + tool calls + tool results + output | **Soft/advisory** — the model paces against a countdown it can see and finishes gracefully |
| `max_tokens` | Generated tokens **per request** | **Hard** — truncates with `stop_reason: "max_tokens"` |
| Per-message thinking nudge | Depth on **one turn**, cache-safe | Soft, wording-sensitive |

- `effort` and `task_budget` are orthogonal: **depth vs breadth.** Use `task_budget` for the pacing target and `max_tokens` as the runaway ceiling; neither constrains the other.
- **Size a budget from measurement, not a default**: run representative tasks with no budget, then start at the **p99** of per-task spend. Minimum `total` is 20,000 tokens.
- **A too-small budget looks like a refusal.** The model may decline outright, de-scope hard, or stop early rather than begin work it cannot finish. On unexpected refusals after adding a budget, raise the budget before touching other parameters.
- Do not mirror the countdown client-side — decrementing `remaining` while resending full history under-reports the budget and makes the model quit early. Pass `remaining` only across a compaction/context rewrite.
- Not on Claude Code / Cowork, and not on Sonnet 5: `task_budget` is Messages API + Opus 5 / Fable 5 / Mythos 5 / Opus 4.8 / Opus 4.7 only.
- **Attribute spend before tuning:** `usage.output_tokens_details.thinking_tokens` separates reasoning from deliverable output. Over-thinking → lower `effort`; over-writing → prompt an explicit length envelope (effort does *not* shorten visible output). Billed thinking is the full internal reasoning, not the summarized text you see — the `display` setting never changes the bill.
- On `stop_reason: "max_tokens"`, the fix depends on the cause: raise `max_tokens` if the reasoning was needed, lower `effort` if it was over-thought.

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
