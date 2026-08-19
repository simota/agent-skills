# User Story Smells And Prioritization Pitfalls

Purpose: Use this file when stories, backlog slices, or MoSCoW priorities look weak or inflated.

## Contents

- `USS-01..09`
- `MP-01..05`
- Backlog anti-patterns
- Accord quality gates

## User Story Smells

| ID | Smell | Failure mode | Guardrail |
|---|---|---|---|
| `USS-01` | everything must be a story | technical work is forced into the wrong format | allow the right work item format |
| `USS-02` | multi-page story | story becomes a mini requirements document | keep the story as a conversation anchor |
| `USS-03` | missing acceptance criteria | completion is undefined | add AC before work starts |
| `USS-04` | AC/DoD confusion | feature and team-wide quality are mixed | keep AC feature-specific |
| `USS-05` | giant story | cannot finish within one sprint | split vertically |
| `USS-06` | technical-layer split | no end-to-end value | slice by user outcome |
| `USS-07` | no ready definition | under-refined work enters delivery | require value, size, AC, and context |
| `USS-08` | no refinement | details freeze too early or never mature | refine continuously |
| `USS-09` | forgotten conversation | story becomes a static document | keep the conversation active |

## MoSCoW Pitfalls

| ID | Pitfall | Failure mode | Guardrail |
|---|---|---|---|
| `MP-01` | everything is `Must` | prioritization collapses | keep `Must <= 60%` |
| `MP-02` | stakeholder disagreement | teams rank differently | align priorities together |
| `MP-03` | one-time prioritization | priorities do not respond to change | re-evaluate iteratively |
| `MP-04` | urgency equals importance | strategic work is displaced | separate urgency from importance |
| `MP-05` | no success definition | ranking is subjective | derive priority from `L0` KPI and value |

## Must Ratio Check

Warning signs:

- `Must` exceeds `60%`
- `Could` or `Won't` are nearly empty
- teams say everything blocks release

## Backlog Anti-Patterns

| Pattern | Failure mode | Accord response |
|---|---|---|
| bloated backlog | `100+` items and no usable priority order | trigger decomposition |
| stale backlog | old items remain forever | use `Deprecated` status |
| estimate everything up front | high change cost | estimate progressively |
| no epic or theme layer | no visible business linkage | anchor in `L0` and `L1` |
| hidden tech debt | risk stays invisible | expose it in `L2-Dev` |

## Accord Quality Gates

- no AC -> not ready
- `Must > 60%` -> warning
- technical-layer slicing -> recommend vertical slicing
- priority with no KPI rationale -> warning
