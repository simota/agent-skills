# Prototyping Anti-Patterns & Guardrails

> Purpose: keep Forge fast without letting prototypes sprawl, rot, or get mistaken for production code.

## Contents

- `FP-01..10` anti-pattern catalog
- Core principles
- Time-box rules
- Lifecycle decisions
- Minimum quality floor

## Anti-Pattern Catalog

| ID | Anti-pattern | What goes wrong | Guardrail |
|---|---|---|---|
| `FP-01` | Lava Flow | Prototype code survives as untouchable legacy | Give every prototype an explicit lifespan and debt log |
| `FP-02` | Scope creep | “One more thing” prevents completion | Enforce `1 prototype = 1 hypothesis` and a time-box |
| `FP-03` | Perfection trap | Pixel-perfect work kills the speed advantage | Use the `80%` rule |
| `FP-04` | Spaghetti prototype | Zero structure makes iteration and handoff painful | Keep minimum file, type, and naming structure |
| `FP-05` | Mock lock-in | Real APIs require a rewrite later | Define the interface early and keep mocks contract-shaped |
| `FP-06` | Zombie prototype | Unvalidated prototypes pollute the repo | Force `ADOPT / ITERATE / DISCARD` and expiry review |
| `FP-07` | No feedback loop | Direction stays wrong too long | `PRESENT` is mandatory |
| `FP-08` | Duplicate prototype work | Teams repeat the same exploration | Share validated patterns and record decisions |
| `FP-09` | God prototype | Too many hypotheses make the result uninterpretable | Split by hypothesis |
| `FP-10` | No handoff package | Production teams rediscover everything from scratch | Generate `.agents/forge-insights.md` and handoff artifacts |

## Core Principles

### 1. One prototype = one hypothesis

Bad:

```text
"Prototype the whole admin dashboard."
```

Good:

```text
"Does a card layout help users scan account status faster than a dense table?"
```

### 2. Time-box is mandatory

Recommended time-box:

| Prototype type | Time-box |
|---|---|
| Quick check | `2-4 hours` |
| UI component | `4-8 hours` |
| Page / flow | `1-2 days` |
| Full-stack PoC | `2-3 days` |

If the time-box is exceeded:
- Demo the current state anyway.
- Document blockers.
- Decide whether to continue or stop.

### 3. Use the 80% rule

- UI: `80%` visual fidelity is enough.
- Data: happy path is enough unless the hypothesis depends on edge cases.
- Error handling: minimum meaningful states only.
- Testing: manual verification is enough unless the prototype is intended to survive.

## Lifecycle Decisions

```text
CREATE -> DEMO -> VALIDATE -> DECIDE
                           -> ADOPT
                           -> ITERATE
                           -> DISCARD
```

| Decision | When | Action |
|---|---|---|
| `ADOPT` | Hypothesis validated and worth production work | Prepare Builder handoff |
| `ITERATE` | Direction is promising but not yet proven | Reset time-box and narrow scope |
| `DISCARD` | Hypothesis is weak, disproven, or stale | Record learning and remove the prototype |

Stale prototype rule:
- Review prototypes left untouched for more than `2 weeks` for discard.

## Minimum Quality Floor

| Area | Keep | Do not require |
|---|---|---|
| Types | Core interfaces and obvious unions | Full type coverage |
| Structure | Separate component, mocks, and types when reusable | Perfect project architecture |
| Errors | Minimum meaningful error and loading states | Full resilience design |
| Styles | Fast styling that communicates intent | Full token integration |
| Tests | Manual run steps | Complete automated coverage |
| Docs | `.agents/forge-insights.md` | Full specification docs |

## Forge Integration Rules

- Run `FP-01..10` as a checklist during `SCAFFOLD`.
- Block handoff if `.agents/forge-insights.md` is missing.
- Warn if the hypothesis is not explicit.
- Block if `PRESENT` is skipped.
- Warn if the prototype is both over time-box and still growing in scope.
