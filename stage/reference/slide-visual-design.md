# Slide Visual System Delta

Purpose: Stage `visual` decision, accessibility, and theme-handoff contract. General typography, color, grid, and whitespace theory is model-known.

## Inputs

- venue, room size, projector/display, lighting, recording/export formats
- audience distance and accessibility needs
- existing brand/theme assets and font licenses
- framework constraints from Marp, reveal.js, or Slidev

## Required Decisions

- Define named roles for background, foreground, accent, muted text, and surfaces.
- Define display, heading, body, caption, and code roles only as needed; validate at the actual output resolution and viewing distance.
- Use one alignment system, one icon family, and a documented image/citation policy.
- Measure contrast and projected legibility; do not rely on universal point sizes, margin percentages, or whitespace ratios.
- Verify glyph coverage, font embedding rights, alt text, reading order, and export behavior.

## Accessibility Baseline

- Text contrast: WCAG 2.2 SC 1.4.3 (`4.5:1`, or `3:1` for qualifying large text).
- Non-text contrast: WCAG 2.2 SC 1.4.11 (`3:1`) where applicable.
- Distributed PDF must be tagged with correct reading order, alt text, and decorative artifacts handled per PDF/UA requirements.
- Confirm current renderer/export support in primary documentation; do not freeze reveal.js/Marp behavior in this reference.

## Deliverable

Provide polarity rationale, role-based typography and palette tokens, measured contrast, grid/safe-area rules, image/icon/code policies, accessibility/export checks, and prototype-slide evidence. Hand off to Stage `theme` only after the visual system passes on representative slides.
