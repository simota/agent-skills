# Core Defaults, Tiers, and Thresholds

Purpose: parameter reference for generated nexus-autoloop runners. Load this when sizing a loop, picking timeout/retry/budget values, configuring convergence detection, or tuning a tier override.

## Contents

- Core Defaults table (all runner parameters)
- Loop Tiers (Light / Standard / Heavy / Marathon)
- Pre-flight & Health Gates
- 3-Tier Timeout architecture
- Convergence Detection thresholds

## Core Defaults

| Parameter | Default | Rule |
|-----------|---------|------|
| `EXEC_TIMEOUT` | `600` | per-iteration timeout |
| `MAX_ITERATIONS` | `20` | bounded loop length |
| `RETRY_LIMIT` | `3` | bounded retry; safe cap ≤ `5` |
| `RETRY_BACKOFF` | `exponential` | `exponential` (2s, 4s, 8s…) or `linear`; never fixed-interval [Source: dasroot.net] |
| `MAX_LOG_SIZE` | `5242880` | rotate above this size |
| `AUTOCOMMIT` | `true` | preserve dirty-baseline isolation |
| `ADAPTIVE_TIMEOUT` | `false` | enable only with sufficient evidence |
| `SKIP_PREFLIGHT` | `false` | debug-only bypass |
| `BRANCH_ISOLATION` | `true` | dedicated iteration and summary branches |
| `SQUASH_ON_DONE` | `true` | squash on successful completion |
| `LOOP_TIER` | `auto` | override only when necessary |
| `CIRCUIT_BREAKER` | `true` | enable circuit breaker for repeated failures |
| `CIRCUIT_THRESHOLD` | `3` | consecutive same-signature failures to trip |
| `CIRCUIT_COOLDOWN` | `300` | seconds before auto-retry after circuit opens |
| `TOOL_TIMEOUT` | `120` | per-tool invocation timeout |
| `LOOP_TIMEOUT` | `0` | total loop timeout; `0` = unlimited |
| `STRUCTURED_LOG` | `true` | emit JSON Lines to `runner.jsonl` |
| `COST_TRACKING` | `false` | enable token and cost tracking |
| `TOKEN_BUDGET` | `0` | max cost in USD; `0` = unlimited |
| `CHECKPOINT_INTERVAL` | `1` | checkpoint state every N iterations [Source: spaceo.ai] |
| `ESCALATION_THRESHOLD` | `0.3` | human-intervention rate > 30% triggers loop redesign |
| `DEDUP_WINDOW` | `5` | check last N actions for duplicate tool calls |
| `CONVERGENCE_THRESHOLD` | `0.85` | action similarity ratio triggering stuck-loop detection |
| `CONVERGENCE_WINDOW` | `3` | consecutive similar iterations before escalation |
| `BURN_RATE_THRESHOLD` | `3.0` | 5-min token-rate multiplier vs prior window; trips `BURN_RATE_ANOMALY` (AP-17) |
| `USD_PER_ITER_CAP` | `0` | absolute USD cap per iteration; set explicitly for unattended runs |
| `USD_PER_RUN_CAP` | `0` | absolute USD cap per loop run; set explicitly for unattended runs |
| `PLACEHOLDER_GREP` | `true` | grep `TODO` / `pass` / `NotImplementedError` / `return None` in changed src (AP-12) |
| `TESTS_IMMUTABLE` | `true` | `tests/` and `verify.sh` are `chmod 0444` + sha256-pinned (AP-13) |
| `PROMPT_IMMUTABLE` | `true` | `PROMPT.md` sha256-pinned at loop start; mid-run change ABORTs (RP-1; Ralph variant only) |
| `GOAL_IMMUTABLE` | `true` | `goal.md` and AC files sha256-pinned; mid-run change ABORTs (AP-16) |
| `SETTINGS_IMMUTABLE` | `true` | `.claude/settings*.json` sha256-pinned at loop start (AP-20) |
| `ARGV_DEDUP` | `true` | hash tool-call argv and dedup-check the last `DEDUP_WINDOW` calls (AP-21) |
| `ARCH_LINT` | `false` | run `jscpd` / `dependency-cruiser` / `ts-prune` in verify; enable for long loops (AP-18) |
| `PROMPT_CACHE_BREAKPOINTS` | `4` | `cache_control` breakpoints in runner prompt layout; aim for 85-90% cache hit, ≥ 60× input-cost reduction (see `resilience-patterns.md`) |
| `WORKTREE_ISOLATION` | `true` | each iteration runs in `git worktree add` directory; supersedes `BRANCH_ISOLATION` (see `resilience-patterns.md`) |
| `CRITIC_MODEL` | `haiku` | independent critic model invoked after primary iteration (see `resilience-patterns.md`) |

## Loop Tiers

| Tier | AC count | `MAX_ITERATIONS` | `EXEC_TIMEOUT` | `RETRY_LIMIT` | `TOOL_TIMEOUT` | `LOOP_TIMEOUT` |
|------|----------|------------------|----------------|---------------|----------------|----------------|
| Light | `1-3` | `10` | `300` | `2` | `60` | `3000` |
| Standard | `3-6` | `20` | `600` | `3` | `120` | `12000` |
| Heavy | `6-10` | `30` | `900` | `4` | `180` | `27000` |
| Marathon | `10+` | `50` | `1200` | `5` | `240` | `0` |

Tier selection rules:

1. Count ACs in `goal.md`.
2. Upgrade one tier for multi-loop scenarios.
3. Upgrade one tier when `runner.log` already shows `TOOL_FAILURE`.
4. Respect explicit `LOOP_TIER` override.

## Pre-flight & Health Gates

| Check | Threshold | On failure | Bypass |
|-------|-----------|------------|--------|
| Disk space before start | `≥ 100MB` free | `[PREFLIGHT:FAIL]` and abort | `SKIP_PREFLIGHT=true` |
| Disk space during iteration | `≥ 50MB` free | mark `BLOCKED` and stop safely | — |
| Process lock | `.run-loop.lock` PID must be dead or absent | active PID aborts; dead PID auto-clears | — |
| Git health | no rebase in progress when `AUTOCOMMIT=true` | abort or block auto-commit loop | `AUTOCOMMIT=false` |
| Branch state | no detached HEAD when `BRANCH_ISOLATION=true` | abort | `BRANCH_ISOLATION=false` |
| Log size | `runner.log ≤ MAX_LOG_SIZE` | rotate to `runner.log.prev` | — |
| State integrity | `state.env.sha256` matches | auto-run `recover.sh` | — |

## 3-Tier Timeout architecture

Timeouts operate at three independent layers; each has independent fallback behavior. See `executor-engines.md` for engine-specific details.

| Layer | Variable | Scope |
|-------|----------|-------|
| Tool | `TOOL_TIMEOUT` | single tool invocation within executor |
| Iteration | `EXEC_TIMEOUT` | one full iteration |
| Loop | `LOOP_TIMEOUT` | entire loop execution |

## Convergence Detection (Stuck-Loop Guard)

Traditional circuit breakers catch error-code failures but miss **semantic failures** — agents stuck in loops producing 200-status responses with no meaningful progress. [Source: medium.com/@michael.hannecke — Resilience Circuit Breakers for Agentic AI]

| Metric | Threshold | Action |
|--------|-----------|--------|
| Action similarity | `≥ 85%` across `3` consecutive iterations | block; escalate as `CONVERGENCE_STALL` |
| Action oscillation | `≥ 3` A↔B alternation cycles in last `6` iterations | block; escalate as `OSCILLATION_LOOP` |
| Output delta | `< 5%` net change in artifacts across `3` iterations | flag as stalled |
| Token burn rate | `> 2×` median cost per iteration | alert and review |

Detection runs after each iteration. **Similarity** catches same-action repetition. **Oscillation** catches agents alternating between two contradictory actions (A → state favoring B; B → state favoring A) where individual actions differ but net progress is zero. [Source: dev.to/boucle2026 — Stuck Agent Detection from 220 Loops; agentpatterns.tech — Infinite Agent Loop patterns]
