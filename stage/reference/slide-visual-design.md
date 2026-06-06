# Slide Visual Design

## Purpose

Design the visual system of a slide deck — typography, color, contrast, image rules, and alignment grid — before applying any framework theme. Visual design is what makes a 6×6-rule slide either elegant or amateurish.

## Scope Boundary

- IN scope: typeface pairing, type scale, color palette, contrast (WCAG AA), image and icon usage rules, alignment grid, whitespace policy, code-block styling.
- OUT of scope: narrative arc (`narrative`), per-slide content writing (`draft`), framework syntax (`marp`/`reveal`/`slidev`), animation timing (delegate to `flow`), brand identity at organization level (delegate to `muse`).

## Core Concepts

### Typography Hierarchy

Use exactly three type roles per deck. More creates noise; fewer flattens hierarchy.

| Role | Function | Suggested Scale (16:9, 1920×1080) |
|------|----------|-----------------------------------|
| Display | Title slide, section dividers | 64–96 pt |
| Heading | Per-slide title | 36–48 pt |
| Body | Bullets, callouts | 24–28 pt minimum |
| Caption | Source citation, footnote | 14–18 pt |

Body must never go below 24 pt. Below 24 pt, the back row stops reading. This is Garr Reynolds's *Presentation Zen* threshold and matches Apple keynote internal style guides.

### Typeface Pairing

Pair one display + one body face. Safe defaults:

| Pairing | Display | Body | Notes |
|---------|---------|------|-------|
| Modern technical | Inter | Inter | Single family, multiple weights — safest |
| Editorial | Playfair Display | Source Sans Pro | Long-form keynotes |
| Friendly product | Poppins | Inter | Consumer / startup |
| Code-heavy | Inter | Inter + JetBrains Mono | Developer talks |
| Japanese-mixed | Noto Sans JP | Noto Sans JP | Use weight 700 (display) / 400 (body); avoid Mincho on stage |

Rules: never mix two display faces; never use Comic Sans, Brush Script, or Papyrus; verify the typeface license allows embedded slide export.

### Color Palette

Build a palette of exactly 5 roles:

| Role | Function | Constraint |
|------|----------|------------|
| Background | Slide background | Single color across deck |
| Foreground | Body text | WCAG AA ≥ 4.5:1 against background |
| Accent | Highlight, key data | Used on ≤ 10% of pixels |
| Muted | Captions, secondary text | WCAG AA ≥ 4.5:1 against background |
| Surface | Cards, code blocks | Differentiated from background by ≥ 1.5:1 |

Verify contrast with WebAIM Contrast Checker or `chroma-js` API. Slide rooms are often dimmer than design environments — check on a projector if possible.

### Dark vs Light Background

| Setting | Recommended |
|---------|------------|
| Bright conference room, daylight | Light background, dark text |
| Theater / dim keynote stage | Dark background, light text |
| Recorded online (Zoom, YouTube) | Light background (tone mapping is harsher on dark) |
| Mixed (in-person + recorded) | Light background; better lowest-common-denominator |

### Alignment Grid

Use a 12-column grid with consistent margins. Default safe area: 10% margin on all sides at 1920×1080 (192 px). Body content lives inside the safe area; only background images bleed.

| Layout | Use Case |
|--------|----------|
| Single column centered | Section divider, big idea |
| 2-column 6/6 | Compare/contrast, before/after |
| 2-column 4/8 or 8/4 | Image + caption, quote + speaker |
| 3-column 4/4/4 | Three principles, three steps |
| 12-column with offset | Full-bleed image with caption block |

### Image Use Rules

- One image at a time. Multi-image collages create visual hierarchy puzzles.
- Full-bleed or contained — never floating with white border on dark background.
- Photos: prefer real, specific over generic stock; avoid handshakes-in-front-of-laptop tropes.
- Diagrams: re-draw from source, do not screenshot. Screenshots from papers are usually illegible at projection size.
- Alt text on every image for screen-reader accessibility (WCAG 1.1.1).
- Source attribution as a 14–18 pt caption when the image is not original.

### Icon System

- One icon family per deck. Lucide, Phosphor, Heroicons, Material Symbols, or Tabler — pick one.
- Icon stroke width consistent across the deck.
- Icon size matches body text x-height (a 24 pt body line pairs with a 24×24 px icon).
- Avoid emoji as icons in professional decks; emoji rendering varies wildly across platforms.

### Code Block Styling

| Setting | Recommended |
|---------|------------|
| Font | JetBrains Mono / Fira Code / Cascadia Code |
| Size | 24 pt minimum on slide; 28 pt for live demo |
| Theme | Match deck (dark deck → dark code; light deck → light code) |
| Highlighting | Use Shiki, Prism, or Highlight.js with one accent color matched to the palette |
| Line count | ≤ 12 lines per slide; if more, split or focus a region |

### Whitespace Policy

Whitespace is not waste. Reynolds's *Presentation Zen* and Edward Tufte's data-ink ratio both demand ≥ 30% empty space per content slide. Tight slides feel anxious; spacious slides feel confident.

## Workflow

1. **Pick background polarity** — light or dark, based on venue (table above).
2. **Choose typeface pairing** — display + body from the safe table.
3. **Build the 5-role color palette** with verified WCAG AA contrast.
4. **Set the type scale** — display / heading / body / caption sizes.
5. **Define the alignment grid** — 12-column, 10% margins by default.
6. **Pick one icon family** and confirm stroke consistency.
7. **Style the code block** — font, theme, accent color, line ceiling.
8. **Whitespace audit** — every prototype slide must have ≥ 30% empty area.

## Output Template

```yaml
visual_system:
  polarity: light | dark
  typography:
    display:
      face: "Inter"
      weight: 700
      size_pt: 72
    heading:
      face: "Inter"
      weight: 600
      size_pt: 40
    body:
      face: "Inter"
      weight: 400
      size_pt: 26
    caption:
      face: "Inter"
      weight: 400
      size_pt: 16
  palette:
    background: "#0F172A"
    foreground: "#F8FAFC"  # contrast 16.1:1
    accent: "#22D3EE"      # used ≤10% of pixels
    muted: "#94A3B8"       # contrast 5.5:1
    surface: "#1E293B"     # contrast 1.6:1 vs bg
  contrast_check: PASS | FAIL(role=...)
  grid:
    columns: 12
    margin_pct: 10
    safe_area_px: [192, 192, 1728, 888]
  icon_family: lucide
  code:
    font: JetBrains Mono
    size_pt: 26
    theme: tokyo-night
  whitespace_audit: PASS | FAIL(slides=[12,15])
```

## Anti-Patterns

- Three or more typefaces — visual cacophony.
- Body text under 24 pt — back row cannot read.
- Accent color used on > 10% of pixels — accent loses meaning.
- Stock photos of laptops, handshakes, lightbulbs, gears — clichés signal low effort.
- Emoji icons in a deck with a real icon family — inconsistent rendering.
- Centered body text in left-aligned bulleted lists — eye loses its anchor.
- Drop shadows on flat-design icons — mixed visual language.
- Comic Sans, Papyrus, Brush Script — ban list, no exceptions.
- Sub-1.5:1 surface contrast against background — code blocks vanish on projector.
- Copying the conference template's logo onto every slide — repetition steals attention from content.

## Deliverable Contract

A visual system is complete when:

- Polarity decided based on venue.
- Type scale has display / heading / body / caption with body ≥ 24 pt.
- Palette has 5 roles with verified WCAG AA contrast for every text role.
- Alignment grid documented (columns, margins, safe area).
- Icon family chosen and stroke confirmed.
- Code block style matches the deck.
- Whitespace audit passes on prototype slides.

Hand off to `theme` (framework-specific theme generation) only after this contract passes.

## Accessibility Baseline (2026-05)

- **WCAG 2.2** (W3C Recommendation, published 2023-10-05) remains the active standard for presentations as of 2026-05. Body text must meet **1.4.3 Contrast (Minimum)** at ≥ 4.5:1 (or 3:1 for large text ≥ 18 pt / 14 pt bold). Non-text UI/graphics elements must meet **1.4.11 Non-text Contrast** at ≥ 3:1.
- For projected slide rooms, target **AAA 1.4.6** at ≥ 7:1 contrast: projector gamma + ambient light routinely drop perceived contrast by 20–30%. Verify on a real projector when feasible.
- ARIA 1.3 is in W3C Working Draft as of 2026; for presentation HTML output (reveal.js, exported Marp HTML), continue authoring against WAI-ARIA 1.2 roles and the WCAG 2.2 SCs. Do not adopt 1.3-only roles until CR.
- **reveal.js 6.0** (2026-03-11) added enforced alt tags for images/videos in the renderer — supply `alt=""` on every slide image to satisfy WCAG 1.1.1 without warnings.
- Marp 4.4 inherits Marpit 3.2 directives; use `<!-- _backgroundImage: ... -->` with HTML `alt` in the underlying Markdown for screen-reader compatibility.
- **PDF/UA (ISO 14289)**: When exporting slides to PDF for distribution, apply PDF/UA in addition to WCAG 2.2. PDF/UA requires tagged PDFs with reading order, alt text on all images, and artifact-tagged decorative elements. US federal WCAG 2.1 AA compliance deadline for digital content is 2026-04-24 (https://technology.berkeley.edu/news/updated-digital-accessibility-policy-requirements). Use Marp CLI's `--pdf` output with browser-based tagged PDF, or export via PowerPoint (from Marp PPTX) → Save as PDF with Document Structure Tags enabled. Marp's `--pptx-editable` flag (LibreOffice required) generates editable PPTX for further accessibility remediation before final PDF export.

## References

- Garr Reynolds, *Presentation Zen* (3rd ed., 2019).
- Edward Tufte, *The Visual Display of Quantitative Information* (2nd ed., 2001).
- Robert Bringhurst, *The Elements of Typographic Style* (4th ed., 2012).
- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2* (Recommendation, 2023-10-05), SC 1.4.3 / 1.4.11 / 1.4.6 — https://www.w3.org/TR/WCAG22/
- Refactoring UI, Adam Wathan & Steve Schoger (2018) — type scale and color role guidance.
- Material Design 3, *Color and Typography* — semantic role pattern.
- Apple Human Interface Guidelines — Keynote typography defaults.
