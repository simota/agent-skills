# Motion System Design Patterns

Purpose: Use this file when you are designing, auditing, or expanding a reusable motion system.

## Contents
- `MS-01` to `MS-06`
- Scale design
- Catalog rules
- Audit targets
- Stagger and choreography guidance

## Core Patterns

| ID | Rule | Practical Standard |
|----|------|--------------------|
| `MS-01` | Token-driven motion | Tokenize all duration and easing values |
| `MS-02` | Discrete scale | Use `5-7` duration steps, not continuous `100/150/200/250...` increments |
| `MS-03` | Usage binding | Every token has a named use case |
| `MS-04` | Reduced-motion integrated | Token system includes reduced-motion overrides |
| `MS-05` | Cataloged patterns | Every shared animation has a documented entry |
| `MS-06` | Auditable system | Measure token usage, reduced-motion coverage, and GPU-safe usage |

## Recommended Scale

| Token Tier | Duration | Common Use |
|------------|----------|------------|
| `t1` | `50ms` | instant micro-feedback |
| `t2` | `100ms` | press, checkbox, toggle |
| `t3` | `200ms` | default fades and dropdowns |
| `t4` | `300ms` | modal, panel, card expansion |
| `t5` | `400ms` | page transition or complex sequence |

## Design-System Comparison

| System | Typical Scale |
|--------|---------------|
| Material | `50/100/150/200/250/300/350/400/500ms` |
| IBM Carbon | `70/110/150/240/400ms` |
| Salesforce | `100/200/400ms` |
| Ant Design | `100/200/300ms` |

Use a simple 5-step scale unless the product clearly benefits from a more expressive model.

## Catalog Rules

Document shared motion by:
- Name
- Category (`entry`, `exit`, `micro`, `state`, `scroll`, `page`, `gesture`)
- Duration token
- Easing token
- Animated properties
- Trigger
- Reduced-motion fallback
- Common surfaces

## Audit Targets

| Metric | Target |
|--------|--------|
| Token coverage | `95%+` |
| Reduced-motion coverage | `95%+` |
| GPU-safe property usage | `95%+` |

Priority order:
- `P0`: accessibility violations
- `P1`: performance problems
- `P2`: hard-coded duration or easing
- `P3`: design consistency improvements

## Stagger and Choreography

- Keep stagger intervals in the `30-80ms` range.
- Keep total stagger under `500ms`.
- Sequence multi-part surfaces by role, not by spectacle.
- Typical modal choreography:
  - overlay `150ms`
  - content `200ms` with `50ms` delay
  - title `150ms` with `150ms` delay
  - actions `100ms` with `200ms` delay

## Motion Budget Categories

When planning motion for a view, allocate animations to these 3 budget categories. Each view should use at most 2-3 categories. See [intentional-motion-framework.md](~/.claude/skills/flow/reference/intentional-motion-framework.md) for the full slot system.

| Category | Purpose | Duration Range | Examples |
|----------|---------|---------------|----------|
| **Hero Entrance** | Draw attention to primary content on page load | 300-600ms | Fade up, scale reveal, stagger reveal |
| **Scroll-Linked** | Create depth and progression as user scrolls | Continuous or 200-400ms | Scroll fade-in, sticky transitions, parallax |
| **Interaction Feedback** | Confirm user actions immediately | 150-250ms | Hover, press, toggle, expand, tooltip |

### Budget Rules

- Maximum 3 distinct motion types per view
- Fill Interaction Feedback first (highest priority)
- Hero Entrance is optional — many views don't need it
- Scroll-Linked is the highest risk for distraction
- Every category requires a `prefers-reduced-motion` fallback

### Per-View Motion Audit

```markdown
| Category | Active? | Motion Type | Duration | Reduced Motion |
|----------|---------|-------------|----------|---------------|
| Hero Entrance | [yes/no] | [type] | [ms] | [fallback] |
| Scroll-Linked | [yes/no] | [type] | [ms] | [fallback] |
| Interaction Feedback | [yes/no] | [type] | [ms] | [fallback] |
Total distinct types: [N ≤ 3]
```

## Quality Gate

- No hard-coded motion values in shared surfaces
- No uncataloged reusable animation
- No missing reduced-motion behavior
- No layout-triggering default pattern
- 60fps expectation remains intact
