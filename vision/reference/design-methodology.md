# Design Methodology

Purpose: Use this file when you need the full process for `REDESIGN`, `NEW_PRODUCT`, `REVIEW`, or `TREND_APPLICATION`.

Contents:
- Mode-specific process steps
- Shared phase model

## Mode Processes

### `REDESIGN`
- Visual audit of the current state
- **Composition audit**: evaluate first viewport, hero contract compliance, layout restraint, and page structure against `reference/composition-principles.md`
- Competitive and trend analysis
- Define principles
- Create `3+` directions
- Detail the selected direction
- Define style guide and token direction
- Prioritize components
- Prepare delegation plan

Output: direction doc plus component specifications

### `NEW_PRODUCT`
- integrate research and personas
- create moodboards
- define color, typography, spacing, and motion foundations
- **composition audit**: apply first-viewport rule, hero contract, and page structure from `reference/composition-principles.md`
- draft wireframes with composition principles enforced
- define token architecture
- instruct prototype work

Output: design-system foundation plus wireframes

### `REVIEW`
- run Nielsen's 10 heuristics
- audit visual consistency
- run trend-gap analysis
- run accessibility checks
- prioritize fixes
- assign next agents

Output: improvement report plus action items

### `TREND_APPLICATION`
- select applicable trends
- check brand alignment
- propose phased rollout
- pick pilot targets
- recommend testing approach when uncertainty is material

Output: trend application plan plus before/after concepts

## Shared Phases

| Phase | Key question |
|-------|--------------|
| `UNDERSTAND` | what business, user, brand, and technical constraints shape the design? |
| `ENVISION` | what `3+` directions could solve the problem? |
| `SYSTEMATIZE` | what tokens, components, states, and breakpoints define the system? |
| `DELEGATE` | which agents should execute what, in which order? |
| `VALIDATE` | what evidence shows the direction is coherent, usable, and safe? |


---

## Per-Recipe Behavior Notes

Referenced from `SKILL.md` -> Subcommand Dispatch.

- `direction`: 3+ options + trade-offs; always attach business-outcome metrics (task-success / time-on-task / conversion lift) to each option.
- `redesign`: In REDESIGN mode, modernize the current state while preserving brand consistency. Ask First if scope is 3+ pages. Always reference the `brand` subcommand result if present.
- `trend`: TREND_APPLICATION mode — limit to 2026 trends (AI-driven UI / Calm UI / Adaptive Systems / DTCG v2025.10); changes that break product identity are forbidden. Present a before/after concept diagram.
- `system`: Superset of NEW_PRODUCT. Always produce a distribution plan to Muse/Palette/Flow/Forge. Make the Core → Brand → Product token hierarchy explicit.
- `brand`: Vision strategy + brand alignment. Always define primary palette / typography pair / 5 voice keywords / 5 anti-keywords. Apply orchestrated inheritance for multi-brand. Always read the Compete report if present.
- `moodboard`: Pre-ENVISION stage. For each of 3-5 directional axes, gather reference images / palette / fonts / tone keywords; narrow 9 candidates → 3 finalists. List the differentiation axis and risk per finalist.
- `audit`: REVIEW mode. Output Nielsen 10 heuristics / WCAG 2.2 AA contrast & focus & target-size as pass/fail; detect token drift and prioritize the remediation backlog (P1/P2/P3) by effort × impact.
- `multi`: Tri-engine design-direction generation — parallel Codex/Antigravity/Claude subagents (each 2–3 directions from a loose prompt), Concurrence-Divergence scoring, aesthetic-spectrum coverage, GROUND checks (brand-fit / persona-fit / WCAG 2.2 AA / reference-existence / outcome-link / AI disclosure), and mandatory downstream handoff stubs. Portfolio merge is default; use `multi --compete` only when the user explicitly wants a single direction. Details → Multi-Engine Mode below and `reference/tri-engine-direction.md`.
- `pair`: Interactive co-design (INTERACTIVE — the dialogue is the deliverable). Vision drives, user navigates; propose 2-3 options → choose → produce/delegate → confirm one decision at a time. Runs within any Operating Mode; distinct from `multi` (one-shot portfolio) and `direction` (batch doc). VERIFY: one decision at a time (no full-direction dump), every option carrying rationale + trade-offs + a measurable outcome metric + WCAG 2.2 AA note (never "looks better"); Vision wrote no code (artifacts come from delegated cluster skills — Muse/Forge/Flow/Palette/Frame/Prose); per-decision user-choice + confirmation gate before production (never auto-lock, even under AUTORUN — draft the plan, return `Next: USER`); bounded by max-decisions (12) / user-stop / direction-locked / diminishing-returns; VALIDATE (dark-pattern / WCAG / handoff-readiness) at close. Full contract → `reference/co-design-pair.md`.

