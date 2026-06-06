# Guardian Collaboration & Routing Reference

Purpose: Define Guardian's standard collaboration flows and auto-routing rules in one place. Covers the unified Pattern → Priority → Target → Blocking matrix, trigger thresholds, multi-route orchestration, response handling, AUTORUN behavior, and analytics.

## Contents

- Pattern catalog
- Unified routing matrix (Pattern → Priority → Target → Blocking)
- Trigger thresholds
- Multi-route orchestration
- Response handling
- Orbit boundary
- Bidirectional handoff matrix
- AUTORUN behavior
- Analytics

## Pattern Catalog

| Pattern | Flow | Use when | Guardian output |
|---------|------|----------|-----------------|
| A | `Plan -> Guardian -> Builder` | planning is complete and commit strategy is needed | branch name, commit structure, PR size forecast |
| B | `Builder -> Guardian -> Judge` | implementation is done and PR prep is needed | signal/noise breakdown, PR package, squash report |
| C | `Guardian <-> Zen` | `noise_ratio > 0.30` or cleanup is required | noise separation plan |
| D | `Guardian -> Canvas` | PR or dependency visualization helps review | diagrams or structure map |
| E | `Guardian <-> Scout` | merge-conflict or technical context is unclear | conflict-aware commit strategy |
| F | `Guardian <-> Judge` | dependency changes, AI-suspected code, or unfamiliar imports need validation | pre-commit quality gate |
| G | `Guardian <-> Atlas` | `3+` modules or new coupling are involved | architecture impact report |
| H | `Guardian -> Radar` | high-risk files or coverage gaps require test support | coverage-focused handoff |
| I | `Guardian -> Zen` | hotspot refactoring is safer before PR | cleanup recommendation |
| J | `Guardian -> [auto]` | routing conditions are met | prioritized handoff package |
| K | `Guardian -> predictions` | pre-review Judge/Zen issues should be anticipated | predictive quality report |

## Unified Routing Matrix

Priority order (lowest number = highest priority). When multiple routes fire, run blocking routes before non-blocking, and follow the sequential requirements in **Multi-Route Orchestration**.

| Priority | Target | When to use (trigger) | Pattern(s) | Blocking |
|----------|--------|------------------------|------------|----------|
| 1 | **Sentinel** | `security_classification == CRITICAL`, `SENSITIVE` with auth changes, dangerous patterns, secret exposure risk | (security escalation) | **yes** |
| 2 | **Radar** | `coverage_gap > 0.40`, hotspot `< 50%` coverage, critical file with no tests, `regression_risk > 0.70`, high-risk files needing test support | H | no |
| 3 | **Zen** | `noise_ratio > 0.30`, `formatting_files > 20`, `import_reorder_files > 10`, `whitespace_only_changes > 5`, hotspot refactor safer before PR | C, I | no |
| 4 | **Atlas** | `cross_module_changes > 3`, new inter-module coupling, shared-core change | G | usually no |
| 5 | **Scout** | conflict ambiguity, unclear root cause, contradictory evidence, merge-conflict context unclear | E | context-dependent |

Noise evaluation rule: auto-route to Zen if `1 HIGH` trigger fires or `2 MEDIUM` triggers fire.

### Other routing targets (not in priority matrix)

| Target | When to use | Pattern | Blocking |
|--------|-------------|---------|----------|
| **Builder** | implement commit or branch structure (Pattern A outbound) | A | no |
| **Judge** | review-ready PR package; pre-commit quality gate when dependency changes / AI-suspected code / unfamiliar imports | B, F | no |
| **Canvas** | visualize dependency or split structure | D | no |
| **Sherpa** | XXL or MEGA work decomposition | (size-driven) | no |
| **Probe** | runtime security verification | (security follow-up) | context-dependent |
| **Ripple** | dedicated impact analysis | (blast-radius follow-up) | no |
| **Harvest** | release-note or historical report follow-up | (reporting only) | no |
| **predictions** | pre-review Judge/Zen issue anticipation | K | no |

## Trigger Thresholds

- Pattern C: `noise_ratio > 0.30`
- Pattern F: dependency files changed, AI-suspected code `>10%`, unfamiliar imports, or substantial logic changes
- Pattern G: cross-module changes `3+`
- Pattern H: risk `> 65`, hotspot overlap, coverage gap, or regression history

## Multi-Route Orchestration

Sequential requirements:
- `Sentinel` before all other routes when security is blocking
- `Scout` before commit strategy when root cause is unclear
- `Zen` before `Judge` when noise meaningfully distorts reviewability

Parallel routing is allowed only for non-blocking routes.

## Response Handling

When a downstream handoff returns:
- `Sentinel`: update blocking status and security classification
- `Zen`: recompute noise ratio and PR quality
- `Radar`: recompute coverage and regression risk
- `Atlas`: update structural risk and split recommendation
- `Scout`: update commit boundaries and conflict strategy

## Orbit-Guardian Squash Boundary

Guardian handles non-loop squash analysis and PR-prep squash recommendations.

Orbit owns:
- loop-iteration squash execution
- autonomous loop rebase
- loop artifact isolation

Guardian owns:
- pairwise squash scoring
- commit grouping
- message synthesis
- attribution checks
- post-squash verification guidance

Rule:
- Guardian may review Orbit output
- Guardian must not re-squash Orbit loop commits structurally

## Bidirectional Handoff Matrix

### Input Partners

| Partner | Handoff token | Purpose |
|---------|---------------|---------|
| Plan | `PLAN_TO_GUARDIAN_HANDOFF` | convert plan into branch and commit strategy |
| Builder | `BUILDER_TO_GUARDIAN_HANDOFF` | prepare PR-ready structure from finished code |
| Judge | `JUDGE_TO_GUARDIAN_HANDOFF` | incorporate review findings |
| Judge | `JUDGE_TO_GUARDIAN_FEEDBACK` | calibrate prediction accuracy |
| Zen | `ZEN_TO_GUARDIAN_HANDOFF` | learn accepted or rejected cleanup patterns |
| Scout | `SCOUT_TO_GUARDIAN_HANDOFF` | add RCA and conflict context |
| Atlas | `ATLAS_TO_GUARDIAN_HANDOFF` | add architecture impact |
| Harvest | `HARVEST_TO_GUARDIAN_HANDOFF` | use historical PR/report feedback |
| Ripple | `RIPPLE_TO_GUARDIAN_HANDOFF` | incorporate blast-radius analysis |

### Output Partners

| Partner | Handoff token | Purpose |
|---------|---------------|---------|
| Builder | `GUARDIAN_TO_BUILDER_HANDOFF` | implement commit or branch structure |
| Judge | `GUARDIAN_TO_JUDGE_HANDOFF` | review-ready PR package |
| Canvas | `GUARDIAN_TO_CANVAS_HANDOFF` | visualize dependency or split structure |
| Sherpa | `GUARDIAN_TO_SHERPA_HANDOFF` | break down XXL or MEGA work |
| Sentinel | `GUARDIAN_TO_SENTINEL_HANDOFF` | blocking security review |
| Probe | `GUARDIAN_TO_PROBE_HANDOFF` | runtime security verification |
| Atlas | `GUARDIAN_TO_ATLAS_HANDOFF` | structural impact analysis |
| Radar | `GUARDIAN_TO_RADAR_HANDOFF` | coverage and regression mitigation |
| Zen | `GUARDIAN_TO_ZEN_HANDOFF` | noise cleanup or hotspot refactor |
| Ripple | `GUARDIAN_TO_RIPPLE_HANDOFF` | dedicated impact analysis |
| Harvest | reporting follow-up | use Harvest when release-note or historical report support is needed |

Include the squash report in `GUARDIAN_TO_JUDGE_HANDOFF` when squash analysis was performed.

## AUTORUN Behavior

AUTORUN may:
- generate route recommendations
- emit non-blocking handoffs
- block and stop on security-critical or approval-gated cases

Pause when:
- two or more blocking routes compete
- a route would imply history rewrite or release-affecting PR restructuring

## Analytics

Target health metrics:
- auto-handoff rate `> 80%`
- successful resolution rate `> 95%`
- false positive rate `< 5%`

Canonical analytics heading:

```markdown
## Handoff Route Analytics

### Route Distribution
- Sentinel: 12%
- Radar: 28%
- Zen: 34%

### Manual Override Analysis
- 2 overrides this month
```
