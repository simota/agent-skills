# Rapid Iteration Methodology

> Purpose: keep Forge cycles short, demoable, and decision-oriented.

## Contents

- Stage timing
- Speed tactics
- Progressive build pattern
- Feedback cadence
- Pivot rules

## Stage Timing

| Prototype type | `SCAFFOLD` | `STRIKE` | `COOL` | `PRESENT` | Total |
|---|---:|---:|---:|---:|---:|
| Quick check | `30 min` | `1-2h` | `30 min` | `30 min` | `2-4h` |
| UI component | `1h` | `4-6h` | `1h` | `1h` | `7-9h` |
| Page / flow | `2h` | `8-12h` | `2h` | `1h` | `1-2 days` |
| Full-stack PoC | `4h` | `12-16h` | `4h` | `2h` | `2-3 days` |

## Speed Tactics

| Tactic | Why it helps | Use when |
|---|---|---|
| Hardcode first | Removes API waiting time | Data-dependent UI |
| Write Tailwind utilities inline | Avoids context switching | Fast UI work |
| Single-file first | Minimizes navigation | Quick checks |
| Copy-paste is allowed | Speed beats DRY in prototypes | Throwaway work |
| Reuse existing UI primitives | Skip styling from zero | Component prototypes |
| Fixed-seed Faker data | Stable demos and screenshots | Repeated demos |
| Template `MSW` handlers | Instant CRUD-like mocks | API-dependent UI |
| Build one vertical slice | Keeps each iteration demoable | Pages and flows |
| Use AI for boilerplate | Speeds structure, not judgment | Repetitive scaffolding |

## Progressive Build Pattern

Build in this order:

1. Static layout with hardcoded data
2. Basic interaction with state
3. Mock data flow with inline mocks or `MSW`
4. Loading / error / empty states

Run a `COOL` check after each step:
- Does it compile?
- Does it render?
- Does the main interaction work?
- Is the concept obvious to another person?

## Feedback Cadence

| Feedback loop | Frequency | Goal |
|---|---|---|
| Self-check | Every `30 minutes` | Catch breakage early |
| Pair check | Every `2-4 hours` | Direction check |
| Stakeholder demo | `PRESENT` phase | Force `ADOPT / ITERATE / DISCARD` |

`PRESENT` structure:

1. Hypothesis in one sentence
2. Demo the happy path
3. Show 1-2 meaningful variations
4. State what was learned
5. Ask for `ADOPT / ITERATE / DISCARD`

## MVP Slicing Rules

Prefer vertical slices:

- Good: one user-visible slice that can be demoed end-to-end
- Bad: all UI first, all logic later, all APIs last

Include:
- Core interaction
- Minimum context to understand the idea
- One happy path

Exclude unless the hypothesis depends on them:
- Auth and permissions
- Full accessibility work
- Performance optimization
- Animation polish
- Full responsive coverage

## Pivot Rules

Iterate when:
- Direction looks right but needs refinement
- New evidence suggests a narrower next test
- Stakeholders request specific, bounded follow-up

Discard when:
- The hypothesis is clearly disproven
- The approach is technically infeasible for the intended path
- Business priority changed
- The prototype exceeds the time-box twice without clearer learning

## Forge Integration Rules

- Set the time-box before coding.
- Use progressive build order by default.
- Require a `COOL` check at least every `30 minutes`.
- Force scope review after `3` iterations.
