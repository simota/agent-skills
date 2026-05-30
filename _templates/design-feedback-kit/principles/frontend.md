# Frontend (Web) Principles — deltas only

Web-specific rules layered on top of `core.md`. Add an entry here only when the rule is web-specific (responsive, pointer+keyboard, browser, SEO/a11y semantics). Shared rules belong in `core.md`. Schema: `_templates/principle-entry.md`. ID prefix: `P-FE-<slug>`.

---

### P-FE-keyboard-focus — Fully keyboard-operable, visible focus
- **Statement:** Every interactive element is reachable and operable by keyboard with a visible focus ring (never `outline: none` without a replacement).
- **Rationale:** WCAG 2.4.7 / keyboard users; web's primary a11y vector. [Source: baseline — WCAG 2.2]
- **Scope:** frontend
- **Tags:** a11y, navigation
- **Source feedback:** baseline
- **Do:** custom `:focus-visible` style with ≥3:1 contrast.
- **Don't:** remove focus outlines for aesthetics.
- **Token:** —
- **Status:** accepted · **Added:** 2026-01-01 · **Last reviewed:** 2026-01-01

### P-FE-responsive-320 — Layout holds from 320px to wide desktop
- **Statement:** No horizontal scroll or clipped content at 320px; touch targets ≥44×44px on coarse pointers.
- **Rationale:** Mobile-web majority; responsive contract. [Source: baseline]
- **Scope:** frontend
- **Tags:** layout, a11y
- **Source feedback:** baseline
- **Do:** fluid layouts, container queries, `min()`/`clamp()`.
- **Don't:** fixed pixel widths that overflow narrow viewports.
- **Token:** —
- **Status:** accepted · **Added:** 2026-01-01 · **Last reviewed:** 2026-01-01

---

<!-- PROMOTE step appends new web-specific principles above this line. -->

## Archive (deprecated)

<!-- Superseded principles move here. ENFORCE ignores this section. -->
