# Design Methodology

Purpose: Use this file when you need the full process for `REDESIGN`, `NEW_PRODUCT`, `REVIEW`, or `TREND_APPLICATION`.

Contents:
- Mode-specific process steps
- Shared phase model
- Warden pre-check rules
- Warden handoff templates

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

## Warden Pre-check

Before delegating implementation work, request a V.A.I.R.E. pre-check from `Warden`.

Result handling:

| Result | Action |
|--------|--------|
| `PASS` | proceed to delegation |
| `CONDITIONAL` | address flagged items and document mitigations |
| `FAIL` | return to `ENVISION`, revise, and resubmit |

Skip conditions:
- minor component-level changes with scope `< 1 page`
- token value adjustments inside an existing system
- trend work explicitly marked `low risk`

Escalation:
- maximum `2` pre-check rounds per direction
- if still `FAIL` after `2` rounds, escalate with Warden's concerns documented
- `FAIL` on `Agency` or `Resilience` always requires resolution

## Warden Handoff Templates

```markdown
## VISION_TO_WARDEN_PRECHECK

- Direction summary: [selected direction]
- Principles: [3-5 principles]
- Token strategy: [color/type/spacing/motion summary]
- Component priorities: [top priorities]
- Constraints: [brand/business/technical constraints]
- Open risks: [known concerns]
```

```markdown
## WARDEN_TO_VISION_FEEDBACK

- Result: PASS | CONDITIONAL | FAIL
- Value: [notes]
- Agency: [notes]
- Identity: [notes]
- Resilience: [notes]
- Echo: [notes]
- Required changes: [list]
- Recheck needed: Yes | No
```
