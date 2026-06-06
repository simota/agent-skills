# Modern CSS Baseline Status (2025-2026)

Use this matrix to decide whether a CSS feature needs a fallback in generated code.
- **Widely Available** = safe without fallback on modern projects
- **Newly Available** = works in latest browsers; include `@supports` guard for older audiences

## Feature Matrix

| Feature | Baseline Status | Safe Without Fallback? | Source |
|---------|----------------|------------------------|--------|
| CSS Subgrid | **Widely Available** (2026-03) | Yes | [MDN Subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Subgrid) |
| Container Queries (`@container`) | **Widely Available** (2025-08) | Yes | [web.dev Aug 2025](https://web.dev/blog/baseline-digest-aug-2025) |
| CSS Nesting | **Widely Available** (2023) | Yes | [MDN Nesting](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting) |
| `:has()` selector | Newly Available (2023-12; Widely ~2026-06) | Yes (latest) | [State of CSS 2025](https://2025.stateofcss.com/en-US/features/) |
| `color-mix()` | Newly Available (2024; Widely ~2026-11) | Yes (latest) | [Chrome devs](https://developer.chrome.com/docs/css-ui/css-color-mix) |
| `light-dark()` | Newly Available (2024-05; Widely ~2026-11) | Yes (latest) | [web.dev](https://web.dev/articles/baseline-in-action-color-theme) |
| CSS Anchor Positioning | **Newly Available** (2026; Chrome 125+/Firefox 147+/Safari 26+) | Partial — `@position-try` needs Safari 18.4+ | [OddBird 2025](https://www.oddbird.net/2025/10/13/anchor-position-area-update/) / [caniuse](https://caniuse.com/css-anchor-positioning) |
| `@scope` | **Newly Available** (2025-12; Firefox 146+) | Yes (latest) | [web.dev Dec 2025](https://web.dev/blog/web-platform-12-2025) |
| View Transitions (single-doc) | **Newly Available** (2025-10; Chrome 111+/Firefox 133+/Safari 18+) | Yes (latest) | [Chrome devs](https://developer.chrome.com/blog/view-transitions-in-2025) |
| View Transitions (cross-doc) | Partial (Chrome 126+/Safari 18.2+; Firefox TBD 2026) | No — Firefox missing | [MDN](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API) |
| Scroll-Driven Animations (`animation-timeline`) | Partial (Chrome 115+/Firefox 110+/Safari 18+) | Use `@supports` | [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations) |
| CSS Grid Lanes (formerly Masonry) | **Experimental** (Safari 26 ships `display:grid-lanes`; Chrome 140 flag) | No — not cross-browser | [W3C CSS WG 2025-09](https://www.w3.org/blog/CSS/2025/09/18/masonry-update-issues/) |

## Key Changes from Pre-2025 Assumptions

- CSS Masonry spec was renamed to **CSS Grid Lanes** (`display: grid-lanes`). Avoid `masonry` as a value — use `grid-lanes` and `inline-grid-lanes`.
- CSS Anchor Positioning is now multi-browser (Firefox 147+ stable, Jan 2026), but `@position-try` flip behavior requires Safari 18.4+. Use `position-try-fallbacks` with a safe fallback placement for older Safari.
- `@scope` crossed Baseline "Newly Available" in December 2025 with Firefox 146 support.
- Container queries graduated to **Baseline Widely Available** in August 2025 — no fallback needed for modern projects.

## Container Query Authoring Rules

- Prefer `@container` over `@media` for components reused across layout contexts (cards, widgets, sidebars).
- Use `container-type: inline-size` on wrappers; always assign `container-name` when nesting — unnamed queries match the nearest ancestor and cause subtle bugs.
- Avoid >3 levels of nested containment contexts (each adds browser evaluation overhead).
- Keep `@media` for page-level layout and user preferences (`prefers-color-scheme`, `prefers-reduced-motion`).
