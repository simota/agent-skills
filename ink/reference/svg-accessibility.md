# SVG Accessibility Reference

Purpose: Annotate SVG assets so assistive technology exposes the right amount of information — and hides the rest. Distinguish decorative from informative icons, pick the correct ARIA pattern, and verify with real screen readers before handoff.

## Standards Baseline (2026-05)

- **WCAG 2.2** — W3C Recommendation since **2023-10-05**. Adds 9 new success criteria (focus appearance, dragging movements, target size 2.4.11, consistent help, redundant entry, accessible authentication). Note: **SC 4.1.1 Parsing is obsolete in WCAG 2.2** (modern browsers no longer require valid HTML for AT). Meeting 2.2 AA also satisfies 2.1 AA.
- **WAI-ARIA 1.2** — W3C Recommendation since **2023-06-06**; current stable target.
- **WAI-ARIA 1.3** — First Public Working Draft **2024-01-23**, still in Working Draft. New: `aria-description`, `aria-braillelabel`, `aria-brailleroledescription`, `suggestion` / `comment` / `mark` roles, multi-IDref `aria-details`. Do not depend on 1.3-only features in production until Candidate Recommendation.
- **SC 1.4.11 Non-text Contrast** — meaningful icons require ≥ 3:1 against adjacent colors.
- **SC 2.5.8 Target Size (Minimum)** — interactive icon targets ≥ 24×24 CSS px (AA); 44×44 (AAA, SC 2.5.5).

## Scope Boundary

- **ink `a11y`**: ARIA attributes on SVG elements, `<title>` / `<desc>` authoring, decorative-vs-informative decision, focus management for interactive SVG controls, screen-reader verification notes.
- **Palette (elsewhere)**: broader usability and interaction-level a11y audit (focus order, keyboard navigation across the whole page, cognitive load).
- **Prose (elsewhere)**: the natural-language content of `aria-label` and `<title>` — wording, tone, translation strings.
- **Artisan (elsewhere)**: applying `aria-label` on the *control* (button/link) that wraps an icon.

If the question is "what should the label say?" → Prose. If it is "where should the label attach, and via which attribute?" → `a11y`.

## Decorative vs Informative Decision

| Question | Answer | Pattern |
|----------|--------|---------|
| Is there adjacent visible text that conveys the same meaning? | Yes | Decorative — `aria-hidden="true"` |
| Is the icon inside a labeled control (button with `aria-label`)? | Yes | Decorative on the icon — label the control |
| Is the icon the sole carrier of meaning? | Yes | Informative — `role="img"` + accessible name |
| Is the icon purely visual flourish? | Yes | Decorative — `aria-hidden="true"` |
| Is the icon an interactive control (click target)? | Yes | Use `<button>`/`<a>` wrapper, label the wrapper |

Default every new icon to **decorative**. Only elevate to informative when no other element carries the meaning.

## Workflow

1. **Classify** the icon using the matrix above.
2. **Decorative** → add `aria-hidden="true"` and stop.
3. **Informative standalone** → add `role="img"` + `<title>` + `aria-labelledby` pointing at the title's `id`.
4. **Informative inside control** → strip all ARIA from the SVG, label the control.
5. **Interactive SVG** (rare) → use `role="button"`, `tabindex="0"`, keyboard handlers, visible focus ring.
6. **Verify** with at least one screen reader (NVDA, VoiceOver, or Orca).

## Decorative Pattern

```xml
<!-- Icon next to visible text — icon is decorative -->
<button>
  <svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16">
    <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2"/>
  </svg>
  Add item
</button>
```

Screen reader announces: "Add item, button." The icon is silent — correct.

## Informative Standalone Pattern

```xml
<!-- No adjacent text, no wrapping control — icon must carry meaning -->
<svg role="img" aria-labelledby="warning-title" viewBox="0 0 24 24">
  <title id="warning-title">Warning: payment overdue</title>
  <path d="M12 2l10 18H2z" fill="currentColor"/>
</svg>
```

Screen reader announces: "Warning: payment overdue, image." Exposing status correctly.

## `<title>` vs `aria-label` vs `aria-labelledby`

| Technique | Support | Notes |
|-----------|---------|-------|
| `<title>` alone | Widely supported but announced inconsistently — treat as tooltip only | Always pair with `aria-labelledby` for reliable AT exposure |
| `aria-label="..."` | Reliable across NVDA / VO / JAWS | Hides the `<title>` text from AT (label wins) — still ship `<title>` for hover tooltip |
| `aria-labelledby="id"` + `<title id="id">` | Most reliable; text is localizable and referenceable | Preferred pattern for informative SVG |

Recommended default for informative SVG: `role="img"` + `<title id="x">` + `aria-labelledby="x"`.

## `<title>` vs `<desc>`

- `<title>` — short accessible name (equivalent to alt text). One per element, first child. Keep ≤ 80 chars.
- `<desc>` — longer description (equivalent to `aria-describedby`). Use only for charts, diagrams, or complex illustrations.

```xml
<svg role="img" aria-labelledby="chart-title" aria-describedby="chart-desc">
  <title id="chart-title">Q3 revenue by region</title>
  <desc id="chart-desc">Bar chart. North: 42M, EU: 38M, APAC: 29M. Trend up vs Q2.</desc>
  <!-- bars -->
</svg>
```

## Icon-Only Button (Very Common)

```xml
<!-- WRONG: labeling the icon, not the control -->
<button>
  <svg role="img" aria-label="Close"><path .../></svg>
</button>

<!-- RIGHT: label the control, hide the icon -->
<button aria-label="Close dialog" type="button">
  <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M6 6l12 12M6 18L18 6"/></svg>
</button>
```

Rule: when a focusable element wraps an icon, **label the focusable element**. The icon is then decorative.

## Interactive SVG Controls

Avoid this pattern when a native `<button>` will do. If an SVG element itself must be interactive:

```xml
<g role="button" tabindex="0" aria-label="Select node"
   onclick="..." onkeydown="if(event.key==='Enter'||event.key===' '){...}">
  <circle cx="50" cy="50" r="20"/>
</g>
```

Requirements: `role="button"`, `tabindex="0"`, accessible name, keyboard activation on Enter and Space, visible focus indicator (`:focus-visible { outline: 2px solid ... }`), pointer-cursor style.

## Focus Management

- SVG `<a>` must have `href` to be keyboard-focusable; use `xlink:href` only for legacy.
- Never put `tabindex="0"` on a decorative SVG — pollutes focus order.
- Visible focus indicator is required (WCAG 2.4.7). Do not rely solely on `title` tooltips.

## Screen Reader Verification

| Tool | Platform | Why use |
|------|----------|---------|
| NVDA | Windows | Most rigorous; open source; primary reference |
| VoiceOver | macOS / iOS | Real mobile behavior (iOS); quick to test via `Cmd+F5` |
| JAWS | Windows | Enterprise reality-check — still dominant in regulated industries |
| Orca | Linux | Coverage check; rarely surfaces unique issues |

Minimum before handoff: **NVDA + Firefox** and **VoiceOver + Safari**. Confirm the accessible name is announced and no redundant "graphic graphic" doubling occurs.

## Anti-Patterns

- `role="img"` on decorative icons — forces AT to announce a meaningless graphic.
- `<title>` alone on an informative icon — relying on tooltip-only exposure (JAWS ignores in some modes).
- Labeling both the icon and the wrapping button — screen readers announce twice ("Close, Close dialog").
- `aria-label` on a `<g>` without `role="img"` — no accessible-name mapping on a generic group.
- Color-only differentiation (red X vs green check) without text alternative — fails WCAG 1.4.1.
- Invisible focus outline on interactive SVG — fails WCAG 2.4.7.
- Translating the accessible name inline in the SVG file — harder to localize than owning the string in the app.

## Handoff

**To Prose:** the set of label strings per icon, in all supported locales.
**To Artisan:** which ARIA attributes belong on the SVG vs on the wrapping component, keyboard activation contract for interactive SVG, WCAG 2.2 target-size (SC 2.5.8 ≥ 24×24 CSS px) and focus-appearance (SC 2.4.11) compliance.
**To Palette:** a11y audit checklist — announced names, focus order, keyboard operability, contrast for meaningful icons (≥ 3:1 WCAG 1.4.11), target-size (WCAG 2.5.8).
**To Vitrine:** accessibility story per icon (decorative vs informative variants) plus axe-core snapshot for visual regression.
