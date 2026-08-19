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
- **Optimize cost per *successful task*, never cost per request** — a cheap call that gets retried, escalated, and hand-corrected is not cheap.

## Cost per Successful Task

Per-request price is the denominator of the wrong ratio. The unit that decides architecture is:

```
Cost per Successful Task =
    model calls
  + retrieval / tool calls
  + retry & fallback
  + validation & eval
  + human review / correction
  + failed-task rework
  + allocated platform & operations
```

Define "successful" identically to the eval gate (`reference/evaluation-observability.md`) — a returned response is not a completed task.

The six cost centers a token-price comparison omits:

| Center | What accrues | Watch |
|--------|--------------|-------|
| Inference | input/output tokens, images, audio | history, retrieved docs, tool results, agent reflection |
| Retrieval | index, storage, embedding, re-index, reranker | update frequency drives re-index; per-tenant indexes multiply storage |
| Platform | gateway, tracing, secrets, policy | shared control that also widens the failure domain |
| Evaluation | dataset upkeep, judge calls, human samples, adversarial runs | scale the gate to change risk — light for wording, heavy for new tool authority |
| Operations | on-call, incident, audit, correction of wrong answers | low-probability × high-blast-radius still justifies prevention spend |
| Change | migration, vendor switch, prompt re-tuning, regression re-baselining | the recurring price of not being locked in |

**Human review is not `count × minutes`.** It carries expert opportunity cost, training, approval fatigue, queue delay, reviewer variance, and exposure to unpleasant content. Automation that emits many low-quality candidates *raises* total cost; track adoption rate, edit distance, rejection rate, review time, and misses. When verifying generated output takes longer than writing it, the feature is cost-negative regardless of token price.

**Counter-example worth remembering.** A support-classification feature moved to a small model: token spend fell ~60%, mean accuracy held, but ambiguous cases mis-routed, adding reprocessing, human escalation, and customer wait — **cost per successful task rose 18%**. Mean-preserving tier changes still shift the tail; evaluate value, reliability, cost, and latency per task, not per token.

### Segment the lead time, or you cannot spend the budget

Cost per Successful Task tells you the ratio is bad. It never tells you **where** — and the reflex answer
("the model is too slow / too weak") is wrong often enough to be expensive. Measure the elapsed path from
*task ready* to *accepted* as segments, not as one number:

| Segment | Ends when | A long segment usually means |
|---------|-----------|------------------------------|
| `context_discovery` | the agent has the files/facts it needs | poor discoverability, no repo map, authority unclear across sources |
| `first_useful_diff` | a candidate change exists | ambiguous intent, missing acceptance criteria, over-broad scope |
| `targeted_verification` | the narrow check runs and reports | no fast targeted check, or the agent cannot discover the command |
| `full_gate` | the complete local/CI gate passes | serial gate, cold environment, unrelated failures mixed in |
| `review` | a human accepts | diff too large, several concerns bundled, evidence missing from the handoff |

Record per segment: **wall-clock** and **human attention** as separate quantities, plus intervention count and
rework count. They move independently — a change can cut wall-clock while raising the attention a human must
spend, which is a regression the total conceals.

**Rules.**

1. **Improve the dominant segment.** Optimizing a non-dominant one converts spend into no change — the classic
   version is making generation faster when verification and review own most of the elapsed time.
2. **Local speedups can be pure push-down.** Faster output that enlarges diffs raises review and rework;
   parallelism that multiplies merge conflicts raises integration. Re-measure the *whole* path after a change,
   not the segment you touched.
3. **Pair the primary metric with guardrails.** Optimizing time-to-green alone rewards narrowing what gets
   checked; optimizing acceptance rate alone rewards sending only easy tasks. Carry regression escape, rework,
   human attention, and cost alongside — a faster path that leaks defects is not adopted.

**Cross-boundary note.** Everything below `platform` in the table above leaves the LLM-provider bill and therefore the `cost` recipe's Scope Boundary. Oracle still *counts* it when comparing designs — routing an option to `Ledger` for infra pricing does not license comparing designs on inference price alone.

### Cognitive Budget — what the reviewer can actually audit

Tokens, latency, and money all bound the machine. None bounds the human who has to accept the output, and on
review-heavy work that is the binding constraint long before the context window is. Budget it explicitly:

| Dimension | Bounds |
|-----------|--------|
| `primary_source_count` | How many distinct sources a reviewer must open to check the claim |
| `citation_length` | How much of each must be read |
| `decision_count` | Judgment calls the reviewer is being asked to ratify at once |
| `unresolved_question_count` | Open items they must hold in mind |
| `diff_size` | Change surface per review unit |
| `tool_switches` | Context switches required to verify |
| `evidence_reproduction_time` | Wall-clock to re-run the evidence themselves |

More output that does not reduce time-to-first-judgment is not higher quality — it is cost moved from the
model's bill to the reviewer's. A `Maintenance Budget` applies the same logic to metadata: any field an owner
cannot realistically keep current is a future staleness incident, not a control.

### Hard gates apply before optimization, never against it

Split the budget in two and keep the order:

```yaml
hard_gates:            # pass/fail — never traded for tokens, latency, or price
  quality_floor: {overall_acceptance, critical_slice_floor, schema_validity, unauthorized_action: 0}
  security: {max_sensitivity, forbidden_categories}
  authority: {minimum_for_decision}
  freshness: {runtime_max_age}
  scope: {...}
optimization:          # targets — tuned freely, only after the gates pass
  {token, latency, monetary, cognitive, maintenance}
```

**Fix the Quality Floor before the optimization starts, and version it.** The floor is the minimum quality the
system may not fall below *after* the change — a set, not a single score: overall acceptance, an independent
floor per critical slice, schema validity, and the counts that must stay at zero (unauthorized tool action,
unsupported policy claim). A candidate that misses the floor leaves the feasible set; it is not scored lower
and then rescued by a cheaper price. Compare on cost, latency, and tail *only within* the set that already
passes.

Two failure modes bracket this. A vague floor lets a quality loss be reclassified after the fact as an
acceptable trade-off — the release already shipped, so the bar moves to meet it. A floor higher than the risk
justifies is just as expensive: it pins every request to the largest model and adds human review that catches
nothing. Derive it from use case and risk, and have Product, domain expert, Security, and the on-call owner
agree to it.

Two procedural consequences:

- **Every optimization experiment records `workload_version` and `quality_floor_version`.** A result measured
  against a different workload mix or a different floor is not comparable to the baseline — "we tested that
  last quarter" is how a regression re-enters.
- **Lowering the floor is a requirements change with its own approval, never a performance result.** A change
  that passes only after the bar moves has not improved anything; it has renegotiated what counts as working.
  Route it back as a scope decision with a named approver, and re-baseline before the next comparison.

When the composed context overflows, degrade in this order — each step preserves more meaning than the next:

1. Drop exact duplicates → 2. drop superseded / expired → 3. convert to pointer → 4. source-preserving extract
→ 5. make low-impact evidence on-demand → 6. split by phase → 7. re-route model/tool → 8. shrink scope and
flag the owner.

Naive summarization is not on this list. It is the step that silently drops the counter-evidence and the one
critical exception, and it is indistinguishable from success until the decision is already wrong.

## Token Economics

> Claude rows verified against `platform.claude.com/docs/en/about-claude/pricing` on **2026-07-25**. OpenAI GPT-5.6 rows verified against `platform.openai.com/pricing` on **2026-08-19** and show standard short-context rates. Check each vendor's official page before quoting because prices and service tiers change.

| Model | Input / 1M | Output / 1M | Speed | Quality | Default use |
|-------|------------|-------------|-------|---------|-------------|
| Claude Fable 5 | `$10.00` | `$50.00` | Slow | Highest | Frontier reasoning, long-running agents |
| Claude Opus 5 | `$5.00` | `$25.00` | Moderate | Highest | Complex agentic coding, `~10%` of traffic |
| Claude Sonnet 5 | `$2.00` → `$3.00` | `$10.00` → `$15.00` | Fast | High | Production default (intro pricing through 2026-08-31, then standard) |
| Claude Haiku 4.5 | `$1.00` | `$5.00` | Fastest | Good | Classification, extraction, tier-1 routing |
| GPT-5.6 Sol | `$5.00` | `$30.00` | Medium | Highest | Frontier cross-vendor fallback |
| GPT-5.6 Terra | `$2.50` | `$15.00` | Medium | High | General cross-vendor fallback |
| GPT-5.6 Luna | `$1.00` | `$6.00` | Fast | Good | Lower-cost cross-vendor routing |
| GPT-4o-mini | `$0.15` | `$0.60` | Fast | Good | High-volume extraction |
| Gemini 3.7 Flash (High) | `TBD (needs confirmation)` | `TBD (needs confirmation)` | Fast | Good | High-volume extraction (Gemini) |

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
- Making token spend a team KPI — it drives context-trimming that raises retries, human correction, and total cost.
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
