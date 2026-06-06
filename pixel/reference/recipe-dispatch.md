# Recipe Subcommand Dispatch — Behavior Notes

Detailed behavior per recipe. SKILL.md keeps the dispatch table; this file holds the per-recipe expansion.

## reproduce (default)

Full SCAN → EXTRACT → COMPOSE → VERIFY → REFINE flow. Extract design values with confidence levels, generate HTML/CSS, run visual verification, iterate up to 3 times.

## verify

Compare existing implementation against mockup only. Skip directly to VERIFY phase and emit a comparison report — no code generation.

## gap

Produce the detailed 8-dimension × 5-severity × 9-root-cause gap analysis report (Markdown + JSON). See `gap-analysis-report.md`.

## audit

Fidelity scoring + audit report formatted for Canon (WCAG/standards mapping) or Judge (review) handoff.

## responsive

Read `responsive-design.md` first. Derive responsive variants from a single-viewport mockup.
- Fluid typography via `clamp(min, vw-based, max)`.
- `@container` for component-level responsiveness; `@media` for page-level layout.
- Prefer Tailwind-aligned breakpoints (640 / 768 / 1024 / 1280 / 1536); compute additional ones only when content width demands it.
- Mark every derived value as **LOW confidence** and recommend designer confirmation.

## dark

Read `dark-mode-derivation.md` first. Derive a dark-mode variant from a light-mode mockup.
- Map via semantic tokens (`--color-bg`, `--color-fg`, `--color-surface-1`); invert at the token layer, not per-rule.
- Support both `prefers-color-scheme: dark` and `[data-theme="dark"]` attribute toggle.
- Re-verify WCAG AA contrast (4.5:1 normal / 3:1 large) for every text and UI pair.
- Never use pure `#000` backgrounds — depth disappears. Use low-saturation bases like `#0d0d12`–`#1a1a24`.

## animation

Read `animation-extraction.md` first. Extract micro-interactions from mockup signals (motion blur, ghost frames, multi-keyframe heuristics).
- Define `hover` / `focus` / `active` / `disabled` states in CSS.
- Token transitions: `--motion-fast 150ms`, `--motion-base 250ms`, `--motion-slow 400ms`.
- Recommended easing: `--ease-out cubic-bezier(0.16, 1, 0.3, 1)`.
- Wrap in `@media (prefers-reduced-motion: reduce)` for the disable path.
- Animate `transform` and `opacity` only (composite-only). Layout-trigger properties (`width`, `height`, `top`) are forbidden.
- Scroll-driven animations (`animation-timeline: scroll()` / `view()`) are available in Chrome 115+ / Firefox 110+ / Safari 18+ — add a `@supports (animation-timeline: scroll())` guard.
- View Transitions API (single-doc) is Baseline Newly Available (Oct 2025) — use `document.startViewTransition()` + `@starting-style`.
- Cross-doc View Transitions are Firefox-unsupported; gate with `@media (prefers-reduced-motion: no-preference)` fallback.
