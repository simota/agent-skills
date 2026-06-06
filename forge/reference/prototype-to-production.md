# Prototype-to-Production Handoff Guide

> Purpose: choose `Throwaway` vs `Evolutionary`, prevent handoff loss, and move validated prototypes toward Builder-ready quality.

## Contents

- Strategy selection
- Handoff pitfalls
- Required handoff package
- `L0-L3` quality ladder
- Tech-debt recording rules

## Strategy Selection

| Dimension | `Throwaway` | `Evolutionary` |
|---|---|---|
| Purpose | Validate a hypothesis fast | Grow a validated slice toward production |
| Code quality target | Low, speed-first | Medium to high, structured from the start |
| Lifetime | Discard after learning | Continue into Builder handoff |
| Risk | Lost learning if undocumented | Lava Flow if debt is hidden |
| Cost profile | Low upfront, rebuild later | Higher upfront, less rewrite later |
| Best fit | High uncertainty | Direction already clear |
| Forge default | `70%` | `30%` |

Decision rules:
- Use `Throwaway` by default when requirements are still exploratory.
- Use `Evolutionary` only when stack, direction, and user value are already clear.
- If requirements are already stable, skip Forge and route directly to Builder.

## Handoff Pitfalls

| ID | Pitfall | What goes wrong | Required mitigation |
|---|---|---|---|
| `HO-01` | Hidden rationale | Builder cannot recover why decisions were made | Record decisions and reasons in `.agents/forge-insights.md` |
| `HO-02` | Prototype mistaken for spec | Stakeholders assume the prototype is shippable | Mark the status explicitly as prototype |
| `HO-03` | Mock / API drift | Real integration requires large rewrites | Align contracts early and keep mocks contract-shaped |
| `HO-04` | Debt inheritance | Temporary shortcuts silently become permanent | Record debt explicitly in `.agents/forge-insights.md` |
| `HO-05` | Missing edge cases | Happy path only; production breaks later | List known edge cases and omissions |
| `HO-06` | Lost design intent | Artisan or Builder has to rediscover interaction choices | Record UI rationale and tradeoffs |
| `HO-07` | Missing test intent | Production teams do not know what to verify | State the target test strategy |

## Required Handoff Package

Required artifacts:

- `Feature.tsx`
- `types.ts`
- `handlers.ts`
- `errors.ts`
- `.agents/forge-insights.md`

Recommended status tags:

- `⚡ PROTOTYPE`
- `🧪 EXPERIMENT`
- `🔁 ITERATE`

## `.agents/forge-insights.md` Template (canonical)

This is the canonical structure for `.agents/forge-insights.md` — used both as the Forge decision/debt log and the Builder handoff brief. Builder-integration consumers reference this template; do not redefine it elsewhere.

```markdown
# Forge Insights: [Feature Name]

## Verified Hypotheses
- [ ] [Hypothesis]
- Result: `CONFIRMED` / `REJECTED` / `NEEDS_MORE_DATA`

## Verified Rules
- [ ] [Domain rule confirmed during prototype, e.g. "Email addresses must be unique"]

## Assumed Rules To Confirm
- [ ] [Rule used during the prototype but not yet verified, e.g. "Is email change rate-limited?"]

## Decision Log
- [Date] [Decision] — Reason: [why]

## Confirmed UI Behavior
- Success: [observed happy-path flow]
- Failure: [observed validation / server / network error handling]

## Tech Debt
- [ ] [file:line] [shortcut] — Reason: [why temporary] · Recommended fix: [next step]

## Known Edge Cases
- [Case]: [impact and current gap]

## Performance Notes
- [Scale tested]: [observed behavior, virtualization / pagination thresholds]

## Test Strategy
- Unit: [what should be covered]
- Integration: [what flow should be covered]

## UI Rationale
- [Decision]: [reason]

## Open Questions
1. [Question for Builder / stakeholder]
```

## `L0-L3` Quality Ladder

| Level | Stage | Minimum quality | Typical phase |
|---|---|---|---|
| `L0` | Concept proof | Works, hardcoded data allowed | `SCAFFOLD -> STRIKE` |
| `L1` | Verifiable | Types separated, mocks separated, basic structure | `COOL` |
| `L2` | Demoable | Loading/error/empty states, responsive basics, realistic mock data | `PRESENT` |
| `L3` | Handoff-ready | Builder package complete, insights complete, debt called out | `-> Builder` |

Typical progression:

- `L0 (2-4h)`: inline mock data, single-file code, minimal debug output.
- `L1 (+2-4h)`: extract `types.ts`, extract `handlers.ts`, split files.
- `L2 (+4-8h)`: add loading, error, and empty states; basic responsiveness; realistic fixtures.
- `L3 (+2-4h)`: add `.agents/forge-insights.md`, `errors.ts`, explicit status tag, and handoff notes.

## Tech-Debt Recording Rules

Classify debt as:

| Type | Example | Risk |
|---|---|---|
| Intentional and documented | Hardcoded token for a non-auth prototype | Predictable |
| Intentional but undocumented | “Temporary” shortcut with no record | Dangerous |
| Unintentional | Hidden anti-pattern introduced during speed work | Hard to detect |

Recording format:

```text
- [ ] [file:line] [temporary implementation] — Reason: [why temporary] · Recommended: [production fix]
```

## Forge Integration Rules

- Run the strategy selection during `SCAFFOLD`.
- If the prototype is `Evolutionary`, plan the `L0 -> L3` progression up front.
- Block Builder handoff if the status tag is missing.
- Warn if `.agents/forge-insights.md` has no tech-debt section.
- Warn if `types.ts` is missing in an `Evolutionary` prototype.
- Warn if known edge cases are not recorded.
