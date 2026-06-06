# Color System And Dark Mode Anti-Patterns

Purpose: Use this reference when dark mode feels harsh, inaccessible, visually noisy, or structurally inconsistent.

## Contents

- Dark mode anti-patterns
- Glare and halation guidance
- Contrast recommendations
- Inclusive color checks
- Muse review checklist

## Dark Mode Anti-Patterns

| ID | Anti-pattern | Signal | Risk | Correction |
|----|--------------|--------|------|-----------|
| `DM-01` | Pure black surfaces | Background uses `#000000` | Eye strain and halation | Use dark gray such as `#121212+` |
| `DM-02` | Insufficient contrast | Text fails WCAG AA | Readability and accessibility failure | Enforce `4.5:1` for text and `3:1` for large text |
| `DM-03` | Over-saturated accents | Light-mode accent copied directly to dark mode | Flicker and fatigue | Reduce saturation by `10-20%` and raise lightness when needed |
| `DM-04` | Broken elevation | Surfaces look flat or indistinguishable | Loss of hierarchy | Express elevation through surface steps |
| `DM-05` | Unadapted imagery | Light-background assets glow on dark screens | Visual disruption | Provide dark variants or soften backgrounds |
| `DM-06` | Forced dark mode | User cannot choose theme | Accessibility and preference issues | Offer `System / Light / Dark` |
| `DM-07` | Invisible focus | Focus rings disappear in dark mode | Keyboard navigation fails | Tokenize focus colors per theme |

## Glare And Halation Guidance

- Avoid extreme white-on-black pairings unless required by brand and verified carefully.
- Reduce pure-white surfaces and unadapted light imagery.
- Treat accent saturation and lightness as separate tuning knobs.
- Comfortable contrast often falls around `7:1-12:1`; values `15:1+` can feel harsher than necessary on dark surfaces.

## Contrast Recommendations

| UI role | Requirement |
|--------|-------------|
| Body text | `4.5:1+` |
| Large text | `3:1+` |
| Links and actions | `4.5:1+` |
| Error / success / warning status text | `4.5:1+` |

Suggested dark-theme ranges:

- Background: `#121212-#1E1E1E`
- Primary body text: `#E0E0E0-#F5F5F5`
- Body text size: `min 16px`
- Body letter-spacing: `0.01-0.02em` when needed for legibility

## Inclusive Color Checks

- Verify low-vision readability.
- Do not rely on color alone for meaning.
- Keep focus and status indicators perceivable in all themes.

## Muse Review Checklist

- `DM-01`: move pure black toward a safer dark gray.
- `DM-02`: adjust token values until contrast passes.
- `DM-03`: reduce accent saturation in dark mode.
- `DM-07`: add theme-specific focus tokens.
