# Loop Execution Learning (REFINE)

Purpose: load this when Orbit analyzes completed loops, adapts defaults, or syncs reusable execution patterns to Lore and Judge.

## Contents

1. REFINE workflow
2. Learning triggers
3. Loop Effectiveness Score
4. Adaptation rules
5. Safety guardrails
6. Integration points
7. Templates
8. Regression eval harvest

## REFINE Workflow

`OBSERVE -> MEASURE -> ANALYZE -> IMPROVE -> SAFEGUARD -> JOURNAL`

| Phase | Purpose | Key actions |
|-------|---------|-------------|
| `OBSERVE` | collect execution results | capture iterations, final status, failures, recoveries, interventions, timings, contract quality, resource usage (tokens/cost), circuit breaker events |
| `MEASURE` | evaluate effectiveness | calculate LES against recent tier history |
| `ANALYZE` | identify patterns | detect success patterns, failure sequences, and parameter fit |
| `IMPROVE` | propose changes | suggest parameter, template, or taxonomy changes with rationale and rollback plan |
| `SAFEGUARD` | validate changes | check failure-catalog anti-patterns, pattern consistency, evidence threshold, and snapshot |
| `JOURNAL` | preserve learning | write journal record and sync to Lore and Judge |

## Learning Triggers

| ID | Condition | Scope |
|----|-----------|-------|
| `RF-01` | every completed loop | lightweight |
| `RF-02` | same tier hits `BLOCKED` or `MAX_ITER` `3+` times | full |
| `RF-03` | user overrides parameters | full |
| `RF-04` | Judge sends feedback | medium |
| `RF-05` | Lore sends loop-pattern notification | medium |
| `RF-06` | `30+` days since the last full REFINE cycle | full |

Priority:
- `RF-02` and `RF-03` override lighter triggers.
- `RF-01` data is still consumed by a concurrent full or medium cycle.

## Loop Effectiveness Score (LES)

```text
LES = Completion_Rate × 0.30
    + Iteration_Economy × 0.25
    + Recovery_Effectiveness × 0.20
    + Contract_Quality × 0.15
    + User_Autonomy × 0.10
```

### Components

| Component | Weight | Definition |
|-----------|--------|------------|
| `Completion_Rate` | `0.30` | fraction of loops reaching `DONE` for the tier |
| `Iteration_Economy` | `0.25` | `1 - (actual_iterations / max_iterations)` |
| `Recovery_Effectiveness` | `0.20` | fraction of failures recovered without user intervention |
| `Contract_Quality` | `0.15` | measurable-AC ratio times goal-clarity score |
| `User_Autonomy` | `0.10` | fewer user interventions per iteration scores higher |

#### Resource Efficiency Bonus

When `COST_TRACKING=true`, an optional resource efficiency modifier can be applied:

```text
Resource_Efficiency = 1 - (actual_cost / budget_cost)
LES_adjusted = LES * (1 + Resource_Efficiency * 0.05)
```

This modifier has a maximum impact of `±0.05` on the final LES, rewarding cost-efficient loops without dominating the score.

### Grading Scale

| Grade | LES range | Meaning |
|-------|-----------|---------|
| `A` | `>= 0.90` | excellent |
| `B` | `>= 0.80` | good |
| `C` | `>= 0.70` | adequate |
| `D` | `>= 0.60` | below standard |
| `F` | `< 0.60` | poor |

LES is valid only after `>= 3` completed loops of the same tier. Below that, report `INSUFFICIENT_DATA`.

## Adaptation Rules

### Allowed Scope by Grade

| Current grade | Allowed adaptation | Approval |
|---------------|--------------------|----------|
| `A` | no auto-change | human required |
| `B` | no auto-change | human required |
| `C` | parameter adjustments within tier bounds | auto with snapshot |
| `D` | parameter adjustments plus contract-template suggestions | auto with snapshot |
| `F` | full review across parameters, contracts, and tier assignment | auto with snapshot |

### Adaptation Types

| Type | Max per session |
|------|-----------------|
| parameter default change | `3` total |
| tier-threshold adjustment | `1` |
| contract-template addition | `1` |
| failure-catalog refinement | `1` |
| verification-gate tightening | `1` |
| default-script enhancement | `1` |

### Adaptive Timeout Algorithm

When `ADAPTIVE_TIMEOUT=true`, timeout values are dynamically adjusted based on historical execution data.

#### Algorithm

```text
effective_timeout = max(
  EXEC_TIMEOUT,
  min(
    moving_average(last_N_durations) + 1.5 * stddev(last_N_durations),
    EXEC_TIMEOUT * 3
  )
)
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `N` (window size) | `5` | number of recent timings to consider |
| multiplier | `1.5σ` | standard deviation multiplier for safety margin |
| floor | `EXEC_TIMEOUT` | never go below the configured base timeout |
| ceiling | `EXEC_TIMEOUT * 3` | never exceed 3x the configured base timeout |

#### Integration with REFINE Cycle

The adaptive timeout feeds into the REFINE cycle at the `OBSERVE` and `ANALYZE` phases:

| Phase | Adaptive timeout data used |
|-------|---------------------------|
| `OBSERVE` | collect per-iteration durations and timeout effectiveness |
| `MEASURE` | include timeout-hit rate in Iteration_Economy calculation |
| `ANALYZE` | detect timeout trends (increasing = possible complexity drift, decreasing = efficiency gain) |
| `IMPROVE` | propose base `EXEC_TIMEOUT` adjustment when adaptive values consistently differ `> 50%` from base |

#### Tier-Specific Bounds

| Tier | Base `EXEC_TIMEOUT` | Adaptive floor | Adaptive ceiling |
|------|---------------------|----------------|------------------|
| Light | `300` | `300` | `900` |
| Standard | `600` | `600` | `1800` |
| Heavy | `900` | `900` | `2700` |
| Marathon | `1200` | `1200` | `3600` |

#### Safety Rules

- Adaptive timeout is disabled until `>= 3` timing data points exist.
- If `3` consecutive iterations hit the adaptive ceiling, emit `[ADAPTIVE:WARN]` and propose tier upgrade.
- Timeout data is stored in `${LOOP_DIR}/.iter-timings.log` (one duration per line in seconds).
- The `REFINE` cycle may propose changing `ADAPTIVE_TIMEOUT` from `false` to `true` when sufficient data exists (RF-01 lightweight record).

Application process:
1. propose
2. validate
3. snapshot
4. apply
5. monitor next `3` executions

## Safety Guardrails

| Mechanism | Rule |
|-----------|------|
| evidence threshold | no adaptation with fewer than `3` data points |
| auto-adaptation ceiling | `LES >= B` requires human approval |
| change-volume limit | maximum `3` parameter changes per session |
| rollback snapshot | save state before every adaptation |
| diminishing returns | `3` consecutive LES improvements `< 0.02` pauses REFINE |
| Lore sync | all reusable patterns must be shared |
| anti-pattern invariant | reject any change violating `AP-1` to `AP-11` |

### Rollback Protocol

1. detect regression when LES drops `>= 0.05`
2. restore the snapshot
3. record the rollback event and cause
4. share the negative pattern with Lore

## Integration Points

| Partner | Direction | Data |
|---------|-----------|------|
| Lore | Orbit -> Lore | loop-execution patterns, taxonomy data, LES trends |
| Lore | Lore -> Orbit | validated cross-agent loop patterns |
| Judge | Orbit -> Judge | LES and completion metrics |
| Judge | Judge -> Orbit | quality feedback |
| Nexus | Orbit -> Nexus | loop-performance reports |
| Builder | Orbit -> Builder | script-template improvement patches |
| Guardian | Orbit -> Guardian | commit-scope policy refinements |

### Lore Sync Protocol

```yaml
ORBIT_TO_LORE_PATTERN:
  type: LOOP_EXECUTION_PATTERN
  pattern_name: <name>
  source_data:
    tier: <tier>
    sample_size: <int>
    les_impact: <float>
  pattern_detail: <description>
  confidence: <HIGH | MEDIUM | LOW>
  actionable: <bool>
```

## Templates

### Feedback Record

```markdown
## Loop Feedback Record — <loop_id>

**Date:** YYYY-MM-DD
**Tier:** <Light | Standard | Heavy | Marathon>
**Final Status:** <DONE | BLOCKED | MAX_ITER | USER_ABORT>
**Iterations:** <actual> / <max>
**LES:** <score> (Grade: <A-F>)
```

### Adaptation Log

```markdown
## Adaptation Log — <date>

**Trigger:** <RF-xx>
**Current LES:** <score> (Grade: <grade>)
**Target LES:** <expected score>

### Change
- **Type:** <adaptation type>
- **Detail:** <specific change>
- **Rationale:** <why this change>

### Safeguard Check
- Anti-pattern compliance: PASS / FAIL
- Pattern consistency: PASS / FAIL
- Evidence threshold (≥ 3): PASS / FAIL
- Snapshot saved: <path>

### Outcome (post-monitoring)
- LES after 3 executions: <score>
- Rollback needed: YES / NO
```


## Regression Eval Harvest

Use this when a loop fires `RECOVER`, `CIRCUIT_OPEN`, `CONVERGENCE_STALL`, `OSCILLATION_LOOP`, `VALIDATOR_GAP`, `REWARD_HACK`, `GOAL_DRIFT`, `BURN_RATE_ANOMALY`, or `PERMISSION_HIJACK`. The failed trace is more valuable than any synthetic test.

Steps:

1. **Snapshot the trace** — capture the failing iteration's `progress.md` entry, `state.env`, last `EXEC_TIMEOUT` worth of `runner.log`, and any `decisions.md` delta.
2. **Distil to a single behavioural assertion** — rewrite the failure as a one-line claim the next runner must satisfy. Example: `loop must abort within 30s when tests/ file mtime changes during an iteration` (AP-13 regression).
3. **Append to `.agents/orbit-eval.md`** under a section keyed by failure class. This file is append-only; never edit historical entries.
4. **Wire into next GENERATE** — when generating a new loop in the same project, read `.agents/orbit-eval.md` and inject the relevant behavioural assertions into the generated `verify.sh` as additional checks.
5. **Trajectory-level eval, not final-output eval** — record the *sequence of actions* that led to the failure, not just the final state. Final-output checks miss `OSCILLATION_LOOP` and `BURN_RATE_ANOMALY`, which are sequence-shaped failures. [Source: augmentcode.com — Best AI Agent Evaluation Tools; augmentcode.com — Agent Observability for AI Coding]

Eval entry format:

```markdown
### <failure-class> | <ISO8601 first observed> | severity <P0|P1|P2>

**Trigger conditions:** <what state of the loop produced this failure>
**Behavioural assertion:** <one-line claim the next runner must satisfy>
**Verify check (bash one-liner or test name):** <executable check>
**Source incident:** loop-dir `<path>`, iter `<id>`
**Mitigation status:** active | retired (date) | superseded by <other entry>
```

Lifecycle:
- Each entry stays *active* until 3 consecutive future loops in the same project pass the assertion without intervention.
- After 3 clean passes, mark *retired* and date-stamp; do not delete (kept for audit).
- If a later incident matches a retired entry, reactivate and append a delta entry referencing the original.

Connect to `RF-02`: when `RF-02` fires (same tier blocked 3+ times), the eval harvest is the first step of the full REFINE cycle.
