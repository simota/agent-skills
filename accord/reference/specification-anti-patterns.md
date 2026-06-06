# Specification Anti-Patterns

Purpose: Use this file when the package structure, collaboration flow, or scope control looks unstable.

## Contents

- `SA-01..12`
- Cross-team failure patterns
- Accord enforcement points

## Specification Anti-Patterns

| ID | Pattern | Failure mode | Guardrail |
|---|---|---|---|
| `SA-01` | L0 Skip | no shared context before detail | never skip `L0` |
| `SA-02` | Kitchen Sink Spec | one package tries to carry everything | split at `10+` requirements and suggest Sherpa |
| `SA-03` | Solution-First Spec | solution appears before the problem | write `Why` first in `L0` |
| `SA-04` | Audience Blindness | all sections use the same language | write `L2` by audience |
| `SA-05` | Static Spec | package drifts from reality | keep status, version, and review flow |
| `SA-06` | Phantom Traceability | matrix exists but links are broken | verify forward and backward links in `BRIDGE` |
| `SA-07` | Wishful BDD | scenarios cannot be tested | require concrete values in `Given/When/Then` |
| `SA-08` | Over-Specified L2 | spec steals implementation choice | keep design/technical detail at the right level |
| `SA-09` | Throw Over the Wall | no feedback loop after delivery | route through review and handoffs |
| `SA-10` | Single Author Spec | one viewpoint dominates | keep team-specific ownership in `L2` |
| `SA-11` | Beautiful but Useless | document looks polished but is not actionable | keep BDD, traceability, and downstream adoption in view |
| `SA-12` | Scope Creep Enabler | scope keeps growing because `Out` is absent | define scope out explicitly in `L0` |
| `SA-13` | NFR Deferral | NFRs listed as `TBD` or deferred past `L1`; discovered at integration causing rework | elicit NFRs at `L1`, require testable `AC` at `L3`, scope-out in `L0` if intentionally excluded |

## Cross-Team Failure Patterns

| Failure | Effect | Accord response |
|---|---|---|
| implicit assumptions | each team works from different premises | list assumptions in `L1` |
| jargon overload | one team cannot read another team's section | use glossary and audience-specific writing |
| one-way delivery | no shared agreement | use `L3` as shared acceptance |
| vague phase labels | scope means different things to different teams | define in/out and delivery slices |
| missing why | prioritization collapses | keep business rationale visible |
| late stakeholder entry | package must be reworked | trigger `STAKEHOLDER_EXPANSION` |

## Accord Enforcement

- no `L0` -> block
- no `Out` section -> warning
- abstract `BDD` -> warning
- `10+` requirements without decomposition -> warning and Sherpa suggestion
