# Specification Calibration System

Purpose: Use this file when running `UNIFY`, measuring specification effectiveness, or tuning scope heuristics.

## Contents

- UNIFY loop
- logging schema
- evaluation metrics
- calibration rules
- section effectiveness
- propagation format

## UNIFY Loop

`RECORD -> EVALUATE -> CALIBRATE -> PROPAGATE`

- run after each delivered package
- run a deeper review every `3` specs or quarterly, whichever comes first
- record to `.agents/accord.md`

## RECORD Schema

```yaml
Spec: [spec-id]
Scope: [Full | Standard | Lite]
Feature_Complexity: [High | Medium | Low]
Teams_Involved: [Biz+Dev+Design | Biz+Dev | Dev+Design | Biz+Design | Single]
Requirements_Count: [N]
BDD_Scenarios_Count: [N]
Sections_Used:
  L0: [yes/no]
  L1: [yes/no]
  L2_Biz: [yes/no]
  L2_Dev: [yes/no]
  L2_Design: [yes/no]
  L3: [yes/no]
Traceability_Completeness: [0-100%]
Cross_Team_Alignment:
  biz_understanding: [High/Medium/Low]
  dev_understanding: [High/Medium/Low]
  design_understanding: [High/Medium/Low]
Revisions_Required: [count]
Downstream_Handoff: [Sherpa/Builder/Radar/Voyager/Canvas/None]
```

## Evaluation Metrics

### Alignment

`Alignment = (Biz + Dev + Design understanding) / 3`

| Result | Interpretation |
|---|---|
| all High | excellent package |
| mixed | moderate alignment, inspect wording and coverage |
| any Low | weak package, inspect the failing audience |

### Scope Accuracy

| Range | Interpretation |
|---|---|
| `> 0.85` | scope heuristic is working well |
| `0.70-0.85` | some over- or under-scoping |
| `< 0.70` | review complexity indicators |

### Evaluation Triggers

| Trigger | Inspect |
|---|---|
| teams ask for clarification after delivery | wording and audience fit |
| package needs `3+` revision rounds | scope or missing sections |
| downstream agent cannot use the package directly | output shape and detail level |
| implementation drifts from the spec | requirement completeness and BDD quality |
| quarterly review | aggregate effectiveness |

## Calibration Rules

1. do not change heuristics before at least `3` specs exist
2. maximum adjustment per cycle: `+/-0.15`
3. decay adjustments by `10%` each quarter toward default values
4. explicit user instruction overrides all calibrated defaults

## Section Effectiveness Defaults

```yaml
section_effectiveness:
  L0_vision: 0.95
  L1_requirements: 0.95
  L2_biz: 0.80
  L2_dev: 0.90
  L2_design: 0.75
  L3_bdd: 0.90
  L3_traceability: 0.70
```

## Writing Pattern Hints

| Pattern | Typical effect | Best fit |
|---|---|---|
| problem-first `L0` | very high | all scopes |
| explicit MoSCoW in `L1` | high | `Standard`, `Full` |
| visual user flow in `L2-Design` | high | UI-heavy work |
| inline technical example in `L2-Dev` | high | API-heavy work |
| BDD with concrete values | very high | all scopes |
| shared glossary | medium to high | `Full` or terminology-heavy work |

## Propagation Format

```markdown
## YYYY-MM-DD - UNIFY: [Scope x Teams]

**Specs assessed**: N
**Average alignment**: [High/Medium/Low]
**Key insight**: [insight]
**Calibration adjustment**: [old -> new]
**Apply when**: [future context]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Accord
date: YYYY-MM-DD
summary: [specification insight]
affects: [Accord, Scribe, Lore]
priority: MEDIUM
reusable: true
-->
```

## Context Library

| Context | Best scope | Typical strong sections |
|---|---|---|
| new product feature across 3 teams | `Full` | all `L2` + full `L3` |
| API extension for Biz + Dev | `Standard` | `L2-Dev`, `L2-Biz`, `L3` |
| UI improvement for Design + Dev | `Standard` | `L2-Design`, `L2-Dev`, `L3` |
| business-impacting bug fix | `Lite` | compact `L0`, key `L3` |
| infra change for Dev only | `Lite` | inline `L2-Dev`, key `L3` |

## Quick UNIFY

Use this when fewer than `3` specs exist:

```markdown
## Quick UNIFY

**Specs assessed**: 1
**Scope**: Standard
**Note**: [observation]
**Action**: No weight change yet
```
