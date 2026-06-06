# Linear-Style Restraint Mode

Purpose: Use this reference when the design direction calls for restrained, minimal, high-confidence UI — the "Linear aesthetic" of calm surfaces, strong typography, and minimal chrome.

## Contents

- Restraint Principles
- Surface Hierarchy
- Typography in Restraint Mode
- Color in Restraint Mode
- Chrome Reduction
- Card Usage Rules
- App UI vs Marketing Guidance
- Restraint Mode Checklist

---

## Restraint Principles

Linear-style restraint is not minimalism for its own sake. It is **confidence expressed through reduction** — every element earns its place, and whitespace is an active design decision.

| Principle | Implementation |
|-----------|---------------|
| Calm surface hierarchy | Flat or near-flat surfaces; elevation used sparingly for interactive states |
| Strong typography + spacing | Typography and spacing do the heavy lifting instead of borders and chrome |
| Minimal color palette | 1-2 accent colors maximum; neutrals carry the interface |
| Minimal chrome | Borders, shadows, and decorative elements reduced to functional minimum |
| Cards for interaction only | Cards wrap actionable content, not static information |
| Density through clarity | Achieve information density through clear hierarchy, not cramming |

---

## Surface Hierarchy

### Layering Rules

| Layer | Background | Use |
|-------|-----------|-----|
| Base | `--color-bg-base` | Page background |
| Raised | `--color-bg-raised` | Sections needing subtle distinction |
| Interactive | `--color-bg-interactive` | Hoverable/clickable containers |
| Overlay | `--color-bg-overlay` | Modals, popovers, dropdowns |

### Rules

- Maximum 3 surface levels visible simultaneously
- Prefer background color shifts over borders for section separation
- Shadows only for overlays and floating elements (popovers, dropdowns)
- No decorative shadows on static content containers

---

## Typography in Restraint Mode

Typography carries the entire hierarchy when chrome is removed.

| Role | Weight/Size Strategy |
|------|---------------------|
| Page title | Largest size, medium or bold weight |
| Section header | Clear size step down, medium weight |
| Body text | Base size, regular weight, generous line-height |
| Secondary text | Smaller size or muted color, never both simultaneously |
| Interactive labels | Medium weight, base or small size |

### Spacing as Hierarchy

| Relationship | Spacing Strategy |
|-------------|-----------------|
| Heading to body | `--space-2` to `--space-3` (tight coupling) |
| Section to section | `--space-12` to `--space-16` (clear separation) |
| Related items in a group | `--space-4` to `--space-6` |
| Unrelated adjacent elements | `--space-8` to `--space-12` |

---

## Color in Restraint Mode

### Palette Constraints

| Role | Token | Rule |
|------|-------|------|
| Background | `--color-bg-*` | Neutral only. No colored backgrounds for sections |
| Primary text | `--color-text-primary` | High contrast, near-black or near-white |
| Muted text | `--color-text-muted` | Lower contrast for secondary information |
| Accent | `--color-accent` | 1 accent color. Used for CTAs, links, active states only |
| Surface | `--color-bg-surface` | Subtle differentiation from base background |

### Rules

- Maximum 2 accent colors in the entire interface
- Accent colors appear only on interactive elements and key focal points
- No colored section backgrounds (use neutral surface shifts)
- Status colors (success/warning/error) are the only additional color allowed

---

## Chrome Reduction

"Chrome" = borders, shadows, icons, decorative elements, and visual embellishments that are not content.

### Reduction Strategy

| Element | Restrained Approach |
|---------|-------------------|
| Borders | Remove default borders. Use subtle dividers only when spacing alone fails to separate |
| Shadows | Reserve for overlays (modals, dropdowns). No shadows on cards or static containers |
| Icons | Use sparingly. Icons should add meaning, not decoration. No icon-for-every-menu-item |
| Badges/Pills | Use for status only, not for categorization or decoration |
| Dividers | 1px, low-contrast. Prefer spacing over dividers when possible |
| Background patterns | None. Solid colors or very subtle gradients only |

---

## Card Usage Rules

In restraint mode, cards have strict usage criteria:

### Use Cards When

- Content is individually clickable or expandable
- Items form a browsable collection (e.g., projects, documents, settings groups)
- Content has distinct interactive states (hover, selected, active)

### Do NOT Use Cards When

- Displaying a feature list (use a clean list layout)
- Wrapping text sections (use spacing and typography)
- Creating visual interest (use hierarchy and whitespace)
- Showing statistics (use inline data within context)

### Card Styling in Restraint Mode

```
- Border: 1px subtle or none
- Shadow: none (hover state may add subtle shadow)
- Border-radius: small (4-8px)
- Padding: generous (--space-4 to --space-6)
- Background: --color-bg-raised or --color-bg-interactive
```

---

## App UI vs Marketing Guidance

### App UI (Restrained)

| Aspect | Rule |
|--------|------|
| Navigation | Minimal chrome. Text-based nav over icon-heavy sidebars |
| Content areas | Clean surfaces, strong typography hierarchy |
| Data display | Tables and lists over card grids |
| Empty states | Subtle illustration + clear action, not decorative |
| CTAs | One primary action per view. Secondary actions are text-styled |

### Marketing Pages (Restrained)

| Aspect | Rule |
|--------|------|
| Hero | Full-bleed image or solid background. Single composition |
| Sections | Generous whitespace between. No card-based feature grids |
| Social proof | Integrated into narrative, not separate card testimonials |
| Pricing | Clean table or simple tier layout, not feature-comparison matrices |
| Footer | Minimal. Organized links without excessive categorization |

---

## Restraint Mode Checklist

```markdown
## Restraint Mode Audit

### Surfaces
- [ ] Maximum 3 surface levels visible
- [ ] No decorative shadows on static content
- [ ] Background shifts preferred over borders

### Typography
- [ ] Typography carries hierarchy (not chrome)
- [ ] Clear size/weight steps between heading levels
- [ ] Generous spacing between sections

### Color
- [ ] Maximum 2 accent colors total
- [ ] Accent only on interactive/focal elements
- [ ] No colored section backgrounds

### Chrome
- [ ] Borders removed where spacing suffices
- [ ] Icons used for meaning, not decoration
- [ ] No decorative badges or pills
- [ ] No background patterns

### Cards
- [ ] Cards used only for interactive content
- [ ] No card grids for static feature lists
- [ ] Card styling follows restraint rules (no shadow, subtle border)

### Overall
- [ ] Every element earns its place
- [ ] Whitespace is intentional, not leftover
- [ ] Design communicates confidence through reduction
```
