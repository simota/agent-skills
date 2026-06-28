# Agent Orchestration

Purpose: Use this file when Vision must route work across design agents, business validation, or quality pre-validation.

Contents:
- Design-agent boundaries
- Delegation patterns
- Accord validation flow

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
| New product design | `Field -> Vision -> Muse -> Forge -> Echo` |
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
