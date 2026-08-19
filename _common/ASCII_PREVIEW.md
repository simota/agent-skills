# ASCII UI Preview Protocol

Canonical protocol for confirming a proposed UI change **before writing code**. When a change alters visible layout or structure, render an ASCII wireframe of the proposed result — a Before/After pair when modifying existing UI — so the user or hub can confirm intent at near-zero cost. A rejected wireframe costs seconds to redraw; a rejected implementation costs a rebuild.

This is a cross-cutting protocol: it is not owned by one specialist. Whichever skill is about to implement a structural UI change runs this gate, then proceeds to code only after confirmation (or after emitting the wireframe as non-blocking evidence, per mode — see below).

---

## Trigger Conditions

Run this protocol when the change matches any row below.

| Trigger | Example |
|---------|---------|
| New screen/page/component | Adding a settings page, a new modal |
| Element addition/removal/reposition | Adding a search bar, removing a sidebar item, moving a CTA above the fold |
| Layout or navigation restructure | Switching from tabs to a sidebar, reordering nav items |
| Responsive breakpoint restructuring | Collapsing a 3-column layout to a mobile drawer |
| Form/flow step changes | Splitting a single-page checkout into multi-step |

## Skip Conditions

Skip the wireframe when any row below applies — do not render one out of habit.

| Condition | Why |
|-----------|-----|
| Style-only tweak (color, typography, spacing token) with no structural delta | Nothing to preview — pixels shift, not structure |
| Logic-only change with no visible UI delta | No layout is affected |
| A confirmed visual mockup already exists as source of truth (image, Figma frame — e.g., pixel `reproduce`) | Redundant with an already-approved reference |
| Emergency hotfix | Confirmation latency outweighs the risk of a minor layout miss |

If uncertain whether a change is structural, default to rendering — the cost of an unnecessary wireframe is a few lines of text; the cost of a skipped one is a coding pass built on a misunderstood layout.

---

## Rendering Rules

- Use box-drawing characters (`┌─┐│└┘├┤`) for regions and containers.
- Max width: 80 columns. Wrap or omit detail rather than exceed it.
- One wireframe per viewport, and only when the change is responsive-specific (e.g., mobile vs. desktop nav collapse). Do not render both viewports for a change that affects only one.
- Mark changed regions with a right-margin annotation: `◆ NEW`, `◆ MOVED`, `◆ REMOVED`.
- Label interactive elements at wireframe fidelity: `[Button]`, `[___input___]`, `(•) radio`, `[x] checkbox`.
- Keep fidelity at structure and hierarchy — not pixel styling, not color, not exact spacing.
- For advanced layouts (multi-panel dashboards, nested grids, complex forms), route to the `canvas` skill rather than freehand-drawing an elaborate frame.

---

## Worked Example

Adding a search bar to a header.

**Before:**
```
┌────────────────────────────────┐
│ Logo        Home  About  Login │
└────────────────────────────────┘
```

**After:**
```
┌────────────────────────────────────────────┐
│ Logo   [___search...___]  Home About Login │ ◆ NEW
└────────────────────────────────────────────┘
```

---

## Mode Semantics

| Mode | Behavior |
|------|----------|
| Interactive / Guided execution | Blocking confirmation gate: present the wireframe, ask one focused question, wait for the response before implementing |
| AUTORUN / AUTORUN_FULL | Non-blocking evidence: embed the wireframe in the step output (or the `_STEP_COMPLETE` `Output` field) so the user can review post-hoc; do not stall the chain waiting for approval |

## Confirmation Semantics

- Ask at most one clarifying question per wireframe.
- If the user rejects the wireframe, revise the wireframe — never start coding on a rejected layout.
- The confirmed wireframe travels in handoff context to downstream agents, the same way a verified image reading travels under `_common/IMAGE_INPUT.md` — downstream agents inherit the confirmed structure instead of re-deriving or guessing it.
