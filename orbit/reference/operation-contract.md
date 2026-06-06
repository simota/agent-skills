# Operation Contract

Purpose: load this when creating or auditing loop artifacts. It defines the minimum contract for `goal.md`, `progress.md`, `done.md`, `state.env`, and the required footer.

Contract version: `1.1.0`

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
  - `3-6` measurable acceptance criteria
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
  - acceptance checklist with evidence
  - rollback note

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
- any session resume flags
- `CONTRACT_VERSION` (current: `1.1.0`)
- `TOTAL_TOKENS` (cumulative token usage across iterations)
- `TOTAL_API_CALLS` (cumulative API call count)
- `ESTIMATED_COST_USD` (cumulative estimated cost)

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

### Budget Alerts

| Condition | Action |
|-----------|--------|
| `ESTIMATED_COST_USD > TOKEN_BUDGET * 0.8` | emit `[COST:WARN]` in runner.log |
| `ESTIMATED_COST_USD > TOKEN_BUDGET` | emit `[COST:BLOCKED]`, set `LAST_STATUS=BLOCKED` |
| `TOKEN_BUDGET` is `0` or unset | no budget enforcement |

Budget enforcement requires `COST_TRACKING=true` in runner configuration.

### Cost in Done Report

When `COST_TRACKING=true`, `done.md` should include:

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

### Version History

| Version | Date | Changes |
|---------|------|---------|
| `1.0.0` | — | initial contract: `NEXT_ITERATION`, `LAST_STATUS`, `LAST_UPDATED_AT`, branch fields |
| `1.1.0` | 2026-03-22 | add `CONTRACT_VERSION`, cost tracking fields (`TOTAL_TOKENS`, `TOTAL_API_CALLS`, `ESTIMATED_COST_USD`), circuit breaker fields |
