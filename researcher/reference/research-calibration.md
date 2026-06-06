# Research Calibration System (DISTILL)

Purpose: Track research quality, recommendation adoption, and method effectiveness over time.
Contents: DISTILL workflow, adoption thresholds, calibration rules, question effectiveness, journal format, ecosystem sharing.

## DISTILL Workflow

`TRACK -> ASSESS -> REFINE -> SHARE`

## What To Track

- method effectiveness by context
- question types that produce rich data
- recommendation adoption
- insight accuracy after shipping
- participant segment usefulness
- bias detection and correction rate

## Adoption Thresholds

| Adoption rate | Interpretation | Action |
|---------------|----------------|--------|
| `> 0.70` | High-impact research | Keep approach |
| `0.40-0.70` | Moderate impact | Improve framing and actionability |
| `< 0.40` | Low impact | Revisit recommendation quality and stakeholder alignment |

## Assessment Triggers

| Trigger | What to assess |
|---------|----------------|
| Feature shipped from insight | Insight accuracy |
| Recommendation ignored | Framing and actionability |
| Persona used by Echo | Persona utility |
| Journey map cited in planning | Synthesis value |
| Quarterly review | Overall research effectiveness |

## Calibration Rules

1. Require `3+ studies` before adjusting method weights.
2. Cap each adjustment at `+/-0.15` per cycle.
3. Apply `10%` decay per quarter toward defaults.
4. Explicit user method preference overrides calibration.
5. For studies with `< 3 insights`, record only; do not update weights.

## Question-Type Calibration

| Question type | Typical richness | Best for |
|---------------|------------------|----------|
| Descriptive | High | Behavior understanding |
| Contrast | High | Value discovery |
| Evaluative | Medium | Emotion mapping |
| Hypothetical | Low-Medium | Latent needs, sparingly |
| Structural | Medium | Priority mapping |

## Journal Entry Format

```markdown
## YYYY-MM-DD - DISTILL: [Study Type]

**Studies assessed**: N
**Overall adoption rate**: X%
**Key insight**: [description]
**Calibration adjustment**: [method/question: old -> new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Researcher
date: YYYY-MM-DD
summary: [research methodology insight]
affects: [Researcher, Echo, Spark, Voice]
priority: MEDIUM
reusable: true
-->
```
