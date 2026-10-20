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
| `LOOP_TIMEOUT` | `0` | total loop timeout in whole seconds; `0` = unlimited. When `LOOP_TIMEOUT`, `USD_PER_RUN_CAP` and `USD_PER_ITER_CAP` are all `0`, the runner refuses to start; a non-integer `LOOP_TIMEOUT` / `EXEC_TIMEOUT` / `KILL_GRACE` (e.g. `1m`, `2.5`) or non-numeric USD cap is `[ABORT]` |
| `ALLOW_UNBOUNDED_RUN` | `false` | `true` lets a run start with all three external limits at `0` — attended runs only |
| `KILL_GRACE` | `10` | seconds between `SIGTERM` and `SIGKILL`; a command limit of `N` sends `SIGTERM` at `N - min(KILL_GRACE, N/2)` and `SIGKILL` at `N`. On runner shutdown the job's whole process group gets `SIGTERM`, then `SIGKILL` after `KILL_GRACE` + 1 s; descendants still in the group when the job's top process exits get `SIGTERM`, then `SIGKILL` after the same grace or at the command limit, whichever comes first |
| `PROJECT_ROOT` | launch directory | runner `cd`s here before running anything; the executor's working directory |
| `STRUCTURED_LOG` | `true` | emit JSON Lines to `runner.jsonl` |
| `COST_TRACKING` | — (not in template) | token and cost tracking — _audit/design-time guard — not enforced by the shipped template_ |
| `TOKEN_BUDGET` | — (not in template) | soft cost alert threshold — _audit/design-time guard — not enforced by the shipped template_; use `USD_PER_RUN_CAP` for enforcement |
| `CHECKPOINT_INTERVAL` | `1` | checkpoint state every N iterations [Source: spaceo.ai] |
| `ESCALATION_THRESHOLD` | `0.3` | human-intervention rate > 30% triggers loop redesign |
| `DEDUP_WINDOW` | `5` (design value) | check last N actions for duplicate tool calls — _audit/design-time guard — not enforced by the shipped template_ |
| `CONVERGENCE_THRESHOLD` | `0.85` (design value) | action similarity ratio — _audit/design-time guard — not enforced by the shipped template_; the runner detects exact signature repetition via `CONVERGENCE_WINDOW` |
| `CONVERGENCE_WINDOW` | `3` | consecutive iterations with an identical signature (HEAD tree + worktree diff + verify result) → `CONVERGENCE_STALL`, runner stops `BLOCKED` |
| `BURN_RATE_THRESHOLD` | `3.0` (design value) | 5-min token-rate multiplier vs prior window; `BURN_RATE_ANOMALY` (AP-17) — _audit/design-time guard — not enforced by the shipped template_ |
| `USD_PER_ITER_CAP` | `0` | absolute USD cap per iteration; fires only when the executor appends its cost to `.cost-usd` |
| `USD_PER_RUN_CAP` | `0` | absolute USD cap per loop run; fires only when the executor appends its cost to `.cost-usd` |
| `PLACEHOLDER_GREP` | `true` | grep `TODO` / `pass` / `NotImplementedError` / `return None` in changed src (AP-12) |
| `GOAL_IMMUTABLE` | `true` | `goal.md` sha256-pinned (`.goal.sha256`) at first start; checked before and after every executor run against the value the runner read at start, so deleting or regenerating `.goal.sha256` mid-run does not hide a change; change → `BLOCKED` (AP-16). AC files outside `goal.md` are pinned only via `PIN_PATHS` |
| `ARTIFACT_PINS` | `true` | sha256 manifest (`.pins.sha256`) taken at first start and checked before and after every executor run: `verify.sh` and `PROMPT.md` in `LOOP_DIR` and `PROJECT_ROOT`, `PROJECT_ROOT/.claude/settings.json`, `PROJECT_ROOT/.claude/settings.local.json` (creating an absent one counts), plus `PIN_PATHS` (a symlink — a pinned path itself or one inside a pinned directory — is pinned by its target); change — or deleting/rewriting `.pins.sha256`, whose digest the runner holds from start — → `[ABORT]`; pins are checked before `verify.sh` runs, and it runs as a pin-matched copy (`.verify-pinned.*` beside it, so `$0` is that copy), `BLOCKED` (AP-13 / AP-20 / RP-1). Re-pin with `recover.sh --repin-goal` |
| `PIN_PATHS` | empty | extra `PROJECT_ROOT`-relative files or directories to pin, colon-separated — set `PIN_PATHS=tests` to pin a `tests/` tree; the template does not know the test path otherwise. In a Git work tree a directory pin covers tracked and untracked-not-ignored files, so ignored build output (`tests/__pycache__`) is not a mutation |
| `ARGV_DEDUP` | `true` (design value) | hash tool-call argv and dedup-check the last `DEDUP_WINDOW` calls (AP-21) — _audit/design-time guard — not enforced by the shipped template_ |
| `ARCH_LINT` | `false` | run `jscpd` / `dependency-cruiser` / `ts-prune` in verify; enable for long loops (AP-18) |
| `PROMPT_CACHE_BREAKPOINTS` | `4` | `cache_control` breakpoints in runner prompt layout; aim for 85-90% cache hit, ≥ 60× input-cost reduction (see `resilience-patterns.md`) |
| `WORKTREE_ISOLATION` | — (not in template) | each iteration in a `git worktree add` directory (see `resilience-patterns.md`) — _audit/design-time guard — not enforced by the shipped template_; the shipped runner isolates with `BRANCH_ISOLATION` |
| `CRITIC_MODEL` | — (not in template) | independent critic model reviewing an iteration (see `resilience-patterns.md`) — _audit/design-time guard — not enforced by the shipped template_; wire it into `verify.sh` to enforce |

## Loop Tiers

| Tier | AC count | `MAX_ITERATIONS` | `EXEC_TIMEOUT` | `RETRY_LIMIT` | `TOOL_TIMEOUT` | `LOOP_TIMEOUT` |
|------|----------|------------------|----------------|---------------|----------------|----------------|
| Light | `3` | `10` | `300` | `2` | `60` | `3000` |
| Standard | `4-5` | `20` | `600` | `3` | `120` | `12000` |
| Heavy | `6` | `30` | `900` | `4` | `180` | `27000` |
| Marathon | upgrade only | `50` | `1200` | `5` | `240` | `0` |

Tier selection rules:

1. Count ACs in `goal.md` (the contract allows `3-6`; a goal with more ACs is split at CONTRACT, never up-tiered — `operation-contract.md`). `Marathon` is reached only via rules 2-4.
2. Upgrade one tier for multi-loop scenarios.
3. Upgrade one tier when `runner.log` already shows `TOOL_FAILURE`.
4. Respect explicit `LOOP_TIER` override.

## Pre-flight & Health Gates

| Check | Threshold | On failure | Bypass |
|-------|-----------|------------|--------|
| Disk space before start | `≥ 100MB` free | `[PREFLIGHT:FAIL]` and abort | `SKIP_PREFLIGHT=true` |
| Disk space during iteration | `≥ 50MB` free | mark `BLOCKED` and stop safely | — |
| Process lock | `.run-loop.lock` PID must be dead or absent | active PID aborts; dead PID auto-clears | — (runs after the disk check: a low-disk abort leaves a stale lock in place) |
| Git health | no rebase in progress when `AUTOCOMMIT=true` | abort or block auto-commit loop | `AUTOCOMMIT=false` |
| Branch state | no detached HEAD when `BRANCH_ISOLATION=true` (and `AUTOCOMMIT=true`) | `[ABORT] detached HEAD` before any iteration | `BRANCH_ISOLATION=false` |
| External terminator | at least one of `LOOP_TIMEOUT` / `USD_PER_RUN_CAP` / `USD_PER_ITER_CAP` `> 0` | `[ABORT]` before pre-flight | `ALLOW_UNBOUNDED_RUN=true` (attended runs only) |
| Log size | `runner.log ≤ MAX_LOG_SIZE` | rotate to `runner.log.prev` | — |
| State integrity | `state.env.sha256` matches | auto-run `recover.sh`; every `DONE` checkpoint (recovered or not) is re-gated on resume — a failed gate continues, or stops `BLOCKED` past `MAX_ITERATIONS` | — |

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
| Identical signature (runner) | same HEAD tree + worktree diff + verify result for `CONVERGENCE_WINDOW` (`3`) iterations | runner stops `BLOCKED`, `[CONVERGENCE:STALL]` |
| Action similarity | `≥ 85%` across `3` consecutive iterations | escalate as `CONVERGENCE_STALL` — _audit/design-time guard — not enforced by the shipped template_ |
| Action oscillation | `≥ 3` A↔B alternation cycles in last `6` iterations | escalate as `OSCILLATION_LOOP` — _audit/design-time guard — not enforced by the shipped template_ |
| Output delta | `< 5%` net change in artifacts across `3` iterations | flag as stalled — _audit/design-time guard — not enforced by the shipped template_ |
| Token burn rate | `> 2×` median cost per iteration | alert and review — _audit/design-time guard — not enforced by the shipped template_ |

The runner's signature check runs after each iteration; the other rows are applied by Orbit when auditing `runner.log` / `.action-sig.log` evidence, or by a custom runner that implements them. **Similarity** catches same-action repetition. **Oscillation** catches agents alternating between two contradictory actions (A → state favoring B; B → state favoring A) where individual actions differ but net progress is zero. [Source: dev.to/boucle2026 — Stuck Agent Detection from 220 Loops; agentpatterns.tech — Infinite Agent Loop patterns]


---

### Circuit Breaker

Single principle: **detect a stall or circular pattern, then stop** — applied below to repeated identical retry failures and unresolved summit-loop debate.

| State | Condition | Behavior |
|-------|-----------|----------|
| `CLOSED` | `< CIRCUIT_THRESHOLD` consecutive same failures | normal retry policy |
| `HALF_OPEN` | `OPEN` cooldown elapsed | allow one probe; success → `CLOSED`, failure → `OPEN` |
| `OPEN` | same-signature failures reach `CIRCUIT_THRESHOLD`, or a probe fails | block until `CIRCUIT_COOLDOWN` elapses, emit `BLOCKED` |

State file `${LOOP_DIR}/.circuit-state`; reset via `recover.sh --reset-circuit` or deletion; `OPEN` → `HALF_OPEN` after `CIRCUIT_COOLDOWN` seconds. Detail → `reference/failure-catalog.md`.



## Agent Tennis Circuit Breaker (summit Phase 5)

Same principle applied to team debate: fires after `>= 3` unresolved turns between Improvement and Verification teams. Action: exit loop, deliver with an unresolved-finding caveat, escalate — never skipped. See `nexus/reference/summit-recipe.md` §Phase 5.

