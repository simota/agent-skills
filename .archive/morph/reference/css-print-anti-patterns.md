# CSS Print And Paged Media Anti-Patterns

Purpose: Use this reference when HTML/CSS-driven PDF output has pagination, print styling, or paged-media compatibility problems.

## Contents

- Print anti-pattern catalog
- Tool compatibility
- Page layout rules
- Development workflow

## Print Anti-Pattern Catalog

| ID | Anti-pattern | Signal | Correction |
|----|--------------|--------|-----------|
| `CP-01` | Uncontrolled page breaks | Tables, images, or code split across pages | Use `break-before`, `break-after`, and `break-inside: avoid` |
| `CP-02` | Ignoring widows and orphans | Isolated lines appear at page edges | Use `widows: 3; orphans: 3;` |
| `CP-03` | Printing dark theme as-is | Ink-heavy, low-readability pages | Switch to light print styling in `@media print` |
| `CP-04` | Trusting modern CSS everywhere | PDF tool ignores newer syntax | Add legacy fallbacks |
| `CP-05` | Trusting browser preview as final output | Real PDF differs from preview | Verify in the actual PDF engine |
| `CP-06` | Unhandled long strings | URLs or code overflow containers | Add `word-break` and `overflow-wrap` fallbacks |
| `CP-07` | Mis-scoped `@page` rules | Page settings are ignored | Keep `@page` in global print styles |

## Tool Compatibility

| Feature | Browser preview | Dedicated PDF engines | Chrome PDF |
|--------|------------------|-----------------------|------------|
| `@page` basics | limited | strong | limited |
| page counters | weak | strong | weak |
| break control | good | good | good |
| modern CSS | strong | mixed | strong |

Rule:

- Browser preview is for early iteration only.
- Final validation must run in the actual PDF engine.

## Page Layout Rules

- Default Japanese print size: `A4`.
- Use print-specific margins and page rules.
- Show URLs only when they add value in printed output.
- Keep non-print UI hidden with explicit print styles.

## Development Workflow

1. DevTools print simulation for fast iteration.
2. Browser print preview for rough page breaks.
3. Real PDF generation for final validation.
