# Agent Orchestration

Purpose: Use this file when Vision must route work across design agents, business validation, or quality pre-validation.

Contents:
- Design-agent boundaries
- Delegation patterns
- Accord validation flow
- Warden quality-prevalidation flow

## Design-Agent Boundaries

| Aspect | Vision | Muse | Palette | Flow | Forge | Echo |
|--------|--------|------|---------|------|-------|------|
| Primary focus | direction | tokens and visual system | UX and usability | motion | prototype | persona validation |
| Writes code | never | yes | yes | yes | yes | never |
| Token decisions | define | implement | consume | consume | consume | review impact |
| Accessibility | require baseline | implement tokens | verify UX | respect motion rules | implement states | validate from user view |

## Core Delegation Patterns

| Pattern | Flow |
|---------|------|
| Full redesign | `Vision -> Muse -> Palette -> Flow -> Forge -> Echo` |
| UX issue resolution | `Vision -> Palette -> Flow` |
| Trend application | `Vision -> Muse -> Palette -> Flow` |
| New product design | `Researcher -> Vision -> Muse -> Forge -> Echo` |
| Design system construction | `Vision -> Muse -> Palette -> Forge` |
| Design review cycle | `Lens -> Vision -> [Muse/Palette/Flow] -> Lens -> Echo` |

## Delegation Packet

Every delegation should include:
- context and chosen direction
- constraints and non-goals
- scope and priority
- success criteria
- explicit handoff artifact expected

## Business-Validated Design (`Vision <-> Accord`)

Use this pattern when:
- redesign scope affects `3+ pages`
- budget or timeline meaningfully constrains the UI direction
- stakeholder expectations could conflict with design quality

Flow:
1. `Accord` provides business constraints.
2. `Vision` creates `3+` options that respect those constraints.
3. `Vision` requests impact validation from `Accord`.
4. `Vision` adjusts if business fit is weak.
5. `Vision` delegates only after the direction is business-valid.

## Quality Pre-validated Design (`Vision <-> Warden`)

Use this pattern before major delegation.

V.A.I.R.E. dimensions:

| Dimension | What to check | Common failure |
|-----------|---------------|----------------|
| `Value` | clear user value | style over substance |
| `Agency` | user control preserved | forced flows, hidden options |
| `Identity` | brand coherence | trend-chasing breaks brand |
| `Resilience` | edge states handled | happy-path only |
| `Echo` | fit to target personas | mismatch with user expectations |

Rules:
- `PASS` -> proceed
- `CONDITIONAL` -> fix conditions, then proceed
- `FAIL` -> revise before delegation
- max `2` rounds per direction
- `Agency` or `Resilience` failure cannot be overridden
