# Operation Contract

Purpose: load this when creating or auditing loop artifacts. It defines the minimum contract for `goal.md`, `progress.md`, `done.md`, `state.env`, and the required footer.

Contract version: `1.2.0`

## Contents

- [Contract checklist](#contract-checklist)
- [Footer contract](#footer-contract)
- [Resume contract](#resume-contract)
- [Cost tracking](#cost-tracking)
- [Contract versioning](#contract-versioning)

## Contract Checklist

- `goal.md` must include:
  - goal statement
  - why it matters
  - `3-6` measurable acceptance criteria — **each AC must map to a machine-checkable verify command** (the completion oracle). An AC with no command is not measurable; strengthen it via `vague-goal-handling.md` AC templates before proceeding.
  - **at least one explicit external terminator** beyond the default iteration cap — declare `LOOP_TIMEOUT` (wall clock) and/or `USD_PER_RUN_CAP` (budget). A contract with only `MAX_ITERATIONS` is under-bounded for unattended runs (SKILL Core Contract: termination MUST be enforced externally by iteration cap / timeout / budget).
  - out-of-scope notes
- `progress.md` must record per iteration:
  - UTC timestamp
  - iteration number
  - changed files and summary
  - verification commands and outcomes
  - remaining work
  - decision: `CONTINUE` or `DONE`
- `done.md` must include:
  - completion timestamp
  - acceptance checklist with evidence (verify `PASS`/`SKIP` **and** placeholder-clean changed source — verify alone is not DONE evidence; AP-12)
  - rollback note

### Contract Validation Gates

Before a contract is accepted (and before `generate` consumes it), assert:

| Gate | Rule | On fail |
|------|------|---------|
| AC-oracle completeness | every AC in `goal.md` resolves to a verify command (in `verify.sh` or inline) | classify `ON_GOAL_CONTRACT_WEAK`; strengthen before execution |
| Terminator bound | ≥ 1 of `LOOP_TIMEOUT` / `USD_PER_RUN_CAP` / `USD_PER_ITER_CAP` is `> 0`, or `MAX_ITERATIONS` is explicitly justified for an attended run (`ALLOW_UNBOUNDED_RUN=true`) | reject for unattended runs; the runner itself refuses to start with all three at `0` unless `ALLOW_UNBOUNDED_RUN=true` |
| Measurability | no AC uses generic verbs ("improve", "clean", "better") without a numeric/boolean threshold | apply Three-Hypothesis Protocol (`vague-goal-handling.md`) |
| Scope guard | `goal.md` + AC files are sha256-pinnable (stable, no TODO placeholders) so the runner can enforce `GOAL_IMMUTABLE` (separate AC files via `PIN_PATHS`) | resolve placeholders before pinning |

## Footer Contract

Required response footer:

```text
NEXUS_LOOP_STATUS: READY | CONTINUE | DONE
NEXUS_LOOP_SUMMARY: <single-line summary>
```

Rules:
- `NEXUS_LOOP_STATUS` must use the exact token.
- Keep the summary concise and operational.
- Missing footer defaults to `CONTINUE` in conservative mode.

## Resume Contract

`state.env` should preserve:
- `NEXT_ITERATION`
- `LAST_STATUS`
- `LAST_UPDATED_AT`
- `ORIGIN_BRANCH` when `BRANCH_ISOLATION` is enabled
- `ITER_BRANCH` when `BRANCH_ISOLATION` is enabled
- `LOOP_BASE` (the pinned starting commit used by completion checks, including without branch isolation)
- any session resume flags
- `CONTRACT_VERSION` (current: `1.2.0`)
- `TOTAL_TOKENS` (cumulative token usage across iterations)
- `TOTAL_API_CALLS` (cumulative API call count)
- `ESTIMATED_COST_USD` (cumulative estimated cost)

Companion loop artifacts (not in `state.env`, but part of the resumable contract — written/read by the `generate` runner):

| Artifact | Role | Owner |
|----------|------|-------|
| `.goal.sha256` | pin of `goal.md` at loop start; mid-run mismatch ABORTs, and so does deleting or rewriting the manifest (the runner holds its digest from start) (`GOAL_IMMUTABLE`, AP-16) | runner pins; never hand-edit |
| `.pins.sha256` | manifest pinning `verify.sh`, `PROMPT.md`, `.claude/settings{,.local}.json` and `PIN_PATHS` (directories in Git: tracked + untracked-not-ignored files; symlinks by their target) at loop start; mid-run mismatch ABORTs, and so does deleting or rewriting the manifest (the runner holds its digest from start) (`ARTIFACT_PINS`, AP-13 / AP-20) | runner pins; re-pin via `recover.sh --repin-goal` |
| `dirty-start-paths.nul` | pre-existing dirty paths excluded from auto-commit; taken at loop start, kept across resumes and extended on resume with paths a human dirtied while the loop was stopped, removed at `DONE` | runner only |
| `loop-dirty-paths.nul` | paths the loop itself left uncommitted when it stopped (BLOCKED / interrupted); on resume these stay auto-commit candidates while other newly dirty paths join the baseline; removed at `DONE` | runner only |
| `.squash-pending` | summary + iteration branch of a failed squash (conflict, rejected summary commit, stash restore); reruns stop `[BRANCH:PENDING]` until the human deletes the iteration branch (resolved) or the summary branch (retry) | runner writes; human resolves |
| `.cost-usd` | append-only per-iteration USD floats; runner sums them to enforce `USD_PER_RUN_CAP` / `USD_PER_ITER_CAP` | executor appends; runner reads |
| `.action-sig.log` | per-iteration change signature; `CONVERGENCE_WINDOW` identical lines → `CONVERGENCE_STALL` | runner only |
| `state.env.sha256` | atomic-write integrity guard for `state.env` | runner only |

Recovery priority:
1. `progress.md` timeline
2. `runner.log` status stamps
3. `state.env`

## Cost Tracking

Each iteration should update cumulative resource metrics in `state.env`:

| Field | Type | Description |
|-------|------|-------------|
| `TOTAL_TOKENS` | integer | cumulative token usage across all iterations |
| `TOTAL_API_CALLS` | integer | cumulative API call count |
| `ESTIMATED_COST_USD` | float | cumulative estimated cost in USD |
| `ITER_TOKENS` | integer | token usage for current iteration (reset each iteration) |
| `ITER_API_CALLS` | integer | API calls for current iteration (reset each iteration) |

### Cost Signal: `.cost-usd`

Cumulative `state.env` fields above are for **resume and reporting**. Hard budget **enforcement** uses the append-only `.cost-usd` file: executors that know their per-iteration cost append one USD float line per iteration; the runner sums the file and derives `ESTIMATED_COST_USD = sum(.cost-usd)`. Keeping enforcement file-based (not `state.env`-derived) lets the runner terminate even when an iteration is killed before its `state.env` write completes.

### Budget Alerts and Caps

| Condition | Action | Tier |
|-----------|--------|------|
| `ESTIMATED_COST_USD > TOKEN_BUDGET * 0.8` | emit `[COST:WARN]` in runner.log — _audit/design-time guard — not enforced by the shipped template_ | soft |
| `ESTIMATED_COST_USD > TOKEN_BUDGET` | emit `[COST:BLOCKED]`, set `LAST_STATUS=BLOCKED` — _audit/design-time guard — not enforced by the shipped template_ | soft |
| `sum(.cost-usd) > USD_PER_RUN_CAP` (cap > 0) | `[ABORT]` run; PAUSE, require explicit human resume (no auto-continue) | **hard** |
| `last(.cost-usd) > USD_PER_ITER_CAP` (cap > 0) | `[ABORT]` run; PAUSE, require explicit human resume | **hard** |
| `LOOP_TIMEOUT`, `USD_PER_RUN_CAP`, `USD_PER_ITER_CAP` all `0`/unset | runner refuses to start (`[ABORT]`) unless `ALLOW_UNBOUNDED_RUN=true` — attended runs only (SKILL Never-list) | **hard** |
| a USD cap set but no `.cost-usd` written | the cap cannot fire — pair it with `LOOP_TIMEOUT` for executors that emit no cost | — |

Soft alerts (`COST_TRACKING`, `TOKEN_BUDGET`) are an audit/design-time guard — the shipped template defines neither variable. Hard caps are enforced by the runner whenever the cap is set. For any unattended run, the Terminator-bound validation gate requires ≥ 1 hard cap or `LOOP_TIMEOUT`.

### Cost in Done Report

When cost is tracked (by the executor or a custom runner), `done.md` should include:

```text
## Resource Usage
- Total tokens: {{TOTAL_TOKENS}}
- Total API calls: {{TOTAL_API_CALLS}}
- Estimated cost: ${{ESTIMATED_COST_USD}}
- Iterations: {{actual}} / {{max}}
```

## Contract Versioning

### Version Format

Contracts use semantic versioning: `MAJOR.MINOR.PATCH`

| Component | Incremented when |
|-----------|-----------------|
| `MAJOR` | breaking changes to required fields or footer semantics |
| `MINOR` | new optional fields or sections added |
| `PATCH` | documentation fixes, clarifications |

### Migration Rules

| Scenario | Rule |
|----------|------|
| `state.env` missing `CONTRACT_VERSION` | treat as `1.0.0`, migrate on next write |
| `state.env` has older `MINOR` version | auto-migrate: add new optional fields with defaults |
| `state.env` has older `MAJOR` version | pause and require explicit migration via `recover.sh --migrate` |
| `state.env` has newer version than runner | warn and proceed in read-only mode |
| `1.1.0` → `1.2.0` | no `state.env` field change; companion artifacts (`.goal.sha256`, `.cost-usd`, `.action-sig.log`) are created lazily by the runner — no migration action required |

### Version History

| Version | Date | Changes |
|---------|------|---------|
| `1.0.0` | — | initial contract: `NEXT_ITERATION`, `LAST_STATUS`, `LAST_UPDATED_AT`, branch fields |
| `1.1.0` | 2026-03-22 | add `CONTRACT_VERSION`, cost tracking fields (`TOTAL_TOKENS`, `TOTAL_API_CALLS`, `ESTIMATED_COST_USD`), circuit breaker fields |
| `1.2.0` | 2026-06-12 | AC→verify-oracle + mandatory-terminator checklist requirements; Contract Validation Gates; `.cost-usd` hard-cap enforcement (`USD_PER_RUN_CAP`/`USD_PER_ITER_CAP`); companion artifacts (`.goal.sha256`, `.cost-usd`, `.action-sig.log`); placeholder-clean DONE evidence |


---

## Multi-Loop Rules

- **Parallel loops**: keep separate `state.env`/`progress.md`; block overlapping candidate paths.
- **Sequential loops**: successor `goal.md` references predecessor output and validates prerequisites independently.
- **Loop of loops**: consume only inner `_STEP_COMPLETE`; never write inner loop state directly.

Detail -> `reference/patterns.md`.
