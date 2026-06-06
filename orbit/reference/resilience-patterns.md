# Resilience Patterns (2026 baseline)

Purpose: source-of-truth for the resilience principles cited in `SKILL.md` Core Contract and Boundaries. Load this when reasoning about retry/circuit/idempotency design, checkpoint strategy, durable execution, prompt-cache layout, worktree isolation, independent critic, or Ralph-style loops. Single-pass citation references are consolidated here so the SKILL body can stay concise.

## Contents

- Cost & autonomy primitives
- Retry / timeout / circuit triad
- Idempotency + task/system state split
- Context-overflow controls (memory pointer pattern, terminal states)
- External-enforcement principle
- OpenTelemetry GenAI conventions
- Durable execution (checkpoint-and-replay)
- Atomic checkpoint writes
- Filesystem-as-memory vs conversation-resend
- Ralph Loop semantics
- Codex CLI engine check (nexus apex Phase 6)
- Tri-engine improvement loop (nexus summit Phase 5)
- Prompt-cache breakpoint layout
- Worktree iteration isolation
- Independent critic model

## Cost & autonomy primitives

- **Primary efficiency metric**: cost-per-completed-task = LLM calls + tool executions + human escalations. Cost-per-token alone hides escalation amplification. [Source: medium.com/data-science-collective — AI Agents Stack 2026]
- **Bounded autonomy**: every loop must define operational limits, escalation paths, and an audit trail. [Source: machinelearningmastery.com — Agentic AI Trends 2026]
- **Staged rollout**: sandbox → gated tools → monitoring → full autonomy; only promote when intervention rate falls below `ESCALATION_THRESHOLD`.

## Retry / timeout / circuit triad

- Combine retry + timeout + circuit breaker as a single resilience unit. Retries without circuit breaker amplify cascading failure. [Source: dasroot.net — Building Resilient Systems 2026; cordum.io — AI Agent Circuit Breaker Pattern 2026]
- Use **exponential backoff** (`2s, 4s, 8s…`) not fixed interval; fixed retry ties up threads and exhausts pools. [Source: medium.com/@rafaeljcamara — Downstream Resiliency Patterns]
- Circuit breakers must be **per service**, not per service instance — per-instance breakers miss systemic failure. [Source: oneuptime.com — Circuit Breaker Patterns 2026]
- Never stack retry layers across load balancer + service code + client library — 2-3× call volume on failing endpoints. [Source: medium.com/@michael.hannecke — Resilience Circuit Breakers for Agentic AI]

## Idempotency + task/system state split

- Every effectful tool invocation needs an **idempotency key**; retry without idempotency risks double-execution of side effects. [Source: fast.io — AI Agent State Checkpointing]
- **Separate task state** (workflow checkpoints, artifacts) from **system state** (policies, budgets, permissions). Mixing them makes agents "remember" the wrong things. Long-running agent tasks fail 15-30% of the time (API timeouts, rate limits, network blips); proper checkpointing cuts wasted reprocessing by ≥ 60%. [Source: fast.io — AI Agent State Checkpointing]

## Context-overflow controls

- **Memory pointer pattern**: tool outputs > `1KB` MUST be stored externally and passed as short references. Reduces per-call payload from 200KB+ to under 100 bytes; context-window overflow is the most common agent failure mode. [Source: arxiv.org/abs/2511.22729 — Solving Context Window Overflow in AI Agents; dev.to/aws — Why AI Agents Fail: 3 Failure Modes]
- **Clear terminal states** (`SUCCESS` / `FAILED`) in every tool response schema. Ambiguous feedback ("more results may be available") is the documented root cause of same-tool retry loops; clear states reduced calls from 14 → 2 in production. [Source: dev.to/aws]

## External-enforcement principle

Generated runner scripts MUST enforce termination externally (iteration cap, timeout, budget). An agent stuck in a reasoning loop cannot reliably break itself out — never rely on the agent's self-assessment to stop. [Source: agentpatterns.tech — Infinite Agent Loop; getmaxim.ai — Troubleshooting Agent Loops]

## OpenTelemetry GenAI conventions

Recommend OpenTelemetry GenAI semantic conventions (`gen_ai.*` span attributes) for loop telemetry when `STRUCTURED_LOG=true`. Standardized spans enable cross-tool observability integration. [Source: opentelemetry.io — AI Agent Observability]

## Durable execution (checkpoint-and-replay)

For RECOVER mode and any multi-step workflow:

- Persist the result of each completed step so recovery replays from the last checkpoint, never re-executes from scratch.
- Re-execution wastes tokens AND risks non-idempotent side effects; durable replay cuts recovery cost by ≥ 90% on multi-step workflows.
- Production platforms (2026): **Temporal** (Series C: $300M @ $5B valuation, Feb 2026), **Inngest**, **AWS Lambda Durable Functions** (GA late 2025), **Cloudflare Workflows** (GA late 2025). All provide step-level checkpointing and built-in retries.

[Source: inngest.com — Durable Execution for AI Agents; aws.amazon.com — Lambda Durable Functions; dbos.dev — Durable Execution Crashproof AI Agents; thenewstack.io — Temporal Replay 2026; agentmarketcap.ai — Durable Agent Execution 2026]

## Atomic checkpoint writes

Write state to a temporary file, then `rename` to the target path. A crash mid-write leaves only the temp file — never a corrupt checkpoint. [Source: breyta.ai — Fault-Tolerant AI Agent Flows; fast.io — AI Agent State Checkpointing]

## Filesystem-as-memory vs conversation-resend

For any `MAX_ITERATIONS ≥ 20` runner, prefer **filesystem-as-memory**:

- State lives in tracked files (`progress.md`, `fix_plan.md`, git history); context is fresh every iteration.
- Conversation-resend models (e.g. naive `/loop` patterns) replay full history → token cost scales linearly.
- Documented incident: conversation-resend burned $6,000 in 20h; filesystem-as-memory equivalents cost $14-23 for comparable durations.

[Source: ghuntley.com/ralph; pageai.pro — Long-running AI coding agents; intelligenttools.co — Claude Code 8-Hour Loop]

## Ralph Loop semantics

When a goal explicitly invokes Ralph Loop shapes (`PROMPT.md`, `<promise>COMPLETE</promise>`, `cat PROMPT.md | claude`, `ghuntley`-style scripts), follow `reference/ralph-loop-pattern.md`:

- `PROMPT.md` is immutable.
- Plan and build modes are separate files.
- `AGENTS.md` capped at 60 operational lines.
- Build/test serialises through a single subagent.
- Ralph applies only to green-field codebases.

[Source: ghuntley.com/ralph]

## Codex CLI engine check (nexus apex Phase 6)

When driving apex Phase 6, Orbit's engine is **fixed to Codex CLI** (`spawn_agent` / `wait_agent` / `send_input` / `resume_agent` / `close_agent`). Before consuming the loop contract, verify:

1. Codex CLI is reachable.
2. `agents.max_depth >= 2`.
3. All five subagent tools are permitted.

If the check fails, emit a runner-handoff error — do NOT silently fall back to Claude Code Agent. apex's cost and convergence model assumes Codex execution. [Source: `nexus/reference/apex-recipe.md` §Engine availability check; developers.openai.com/codex/subagents]

## Tri-engine improvement loop (nexus summit Phase 5)

Orbit runs a tri-engine parallel cycle (Claude / Codex / agy branches) for up to `max_loops = 3` iterations (default from `mission_charter.yaml`). Arbiter: **magi**. Exit when ANY of:

- All CONFIRMED/LIKELY CRITICAL findings resolved.
- Agent Tennis circuit breaker tripped.
- Cost budget projected overrun.

[Source: `nexus/reference/summit-recipe.md` §Phase 5]

## Prompt-cache breakpoint layout

Lay out generated runner prompts with `cache_control` breakpoints at stable boundaries (system → tool schema → goal/AC → recent context tail). Aim for `PROMPT_CACHE_BREAKPOINTS=4`. Comparable 2026 workloads report **91.8% cache hit** and **≥ 60× input-cost reduction** vs unbreakpointed (which sustain ~3% hit). [Source: aicheckerhub.com — Anthropic Prompt Caching 2026; projectdiscovery.io — Cut LLM Cost with Prompt Caching]

## Worktree iteration isolation

Each iteration runs in a dedicated `git worktree`. Success → squash-merge back; failure → leave the worktree path in stderr for forensic inspection. `WORKTREE_ISOLATION=true` is the default and supersedes `BRANCH_ISOLATION` for parallel-safe runners. Rollback becomes a single `git worktree remove`. [Source: towardsdatascience.com — AI Agents Need Their Own Desk; codeline.co — Sandcastle Isolation]

## Independent critic model

Gate DONE through an independent critic model (`CRITIC_MODEL=haiku` by default): a different model + different system prompt reviews the iteration output. Only critic-approved iterations advance to the DONE Evidence Gate. Same-model self-eval inherits the same blind spots and produces shallow agreement; an independent critic catches false-DONE that conventional verify cannot. [Source: genta.dev — Agentic Design Patterns; addyosmani.com — Self-Improving Agents]
