# Breakpoint Extraction

Reference for Frame's `breakpoint` recipe. Extract responsive breakpoints from multi-frame Figma designs (mobile/tablet/desktop), Layout Grid analysis, and Constraints inheritance.

> Designers do not always provide all breakpoints. Inferred values are LOW confidence — flag explicitly.

---

## 1. Discovery Workflow

```
get_metadata          → list all frames, identify breakpoint candidates by name
                        (e.g., "Hero - Mobile 375", "Hero - Desktop 1440")
get_design_context    → for each candidate, fetch layout + constraints
```

Heuristics for grouping frames as "same component, different breakpoint":
- Same root component or page name
- Frame name suffix: `Mobile`, `Tablet`, `Desktop`, or width values (`375`, `768`, `1440`)
- Identical child structure with different sizes

---

## 2. Layout Grid → CSS Grid

Figma Layout Grid types:
| Figma | CSS equivalent |
|---|---|
| Columns (count + gutter + margin) | `display: grid; grid-template-columns: repeat(N, 1fr); gap: G; padding: M;` |
| Rows | `grid-template-rows` |
| Grid (uniform cells) | `grid-template: ...` |

### Extraction template
```yaml
frame: Hero - Desktop 1440
breakpoint_inferred: 1440
layout_grid:
  type: columns
  count: 12
  gutter: 24px
  margin: 80px

css:
  display: grid
  grid-template-columns: repeat(12, 1fr)
  gap: 24px
  padding-inline: 80px
  max-width: 1280px  # = 1440 - 80*2
  margin-inline: auto
```

### Per-breakpoint comparison
```yaml
breakpoints:
  mobile-375:    { columns: 4, gutter: 16, margin: 16 }
  tablet-768:    { columns: 8, gutter: 20, margin: 32 }
  desktop-1440:  { columns: 12, gutter: 24, margin: 80 }
```

---

## 3. Constraint Inheritance

Figma Constraints (`Left`, `Right`, `Center`, `Scale`, `Stretch`) on each layer inform CSS layout choice:

| Figma constraint | CSS pattern |
|---|---|
| Left + Top | `position: absolute; left: X; top: Y;` (avoid; refactor to flex) |
| Left + Right (horizontal) | `width: 100%` (stretches) |
| Center horizontally | `margin-inline: auto` or flex `justify-content: center` |
| Top + Bottom (vertical) | `height: 100%` |
| Scale | `width: %` (proportional) |

### Auto Layout (preferred)
If Auto Layout is used, prefer:
```css
display: flex;  /* horizontal/vertical based on layout direction */
gap: <itemSpacing>px;
padding: <paddingTop>px <paddingRight>px <paddingBottom>px <paddingLeft>px;
align-items: <primaryAxisAlignItems>;
justify-content: <counterAxisAlignItems>;
```

---

## 4. Breakpoint Value Inference

### From frame widths
- 320, 375 → mobile
- 414, 480 → large mobile
- 768 → tablet
- 1024, 1280 → laptop
- 1440, 1920 → desktop

### Standardization
Map detected widths to standard tier:

| Detected | Recommended breakpoint |
|---|---|
| 320-414 | `(min-width: 0)` (mobile-first default) |
| 600-768 | `(min-width: 768px)` |
| 900-1024 | `(min-width: 1024px)` |
| 1200-1440 | `(min-width: 1280px)` |
| 1600+ | `(min-width: 1536px)` |

### Output: media query stack
```css
/* Mobile-first */
.hero { display: grid; grid-template-columns: 1fr; gap: 16px; padding: 16px; }

@media (min-width: 768px) {
  .hero { grid-template-columns: repeat(8, 1fr); gap: 20px; padding: 32px; }
}

@media (min-width: 1280px) {
  .hero { grid-template-columns: repeat(12, 1fr); gap: 24px; padding-inline: 80px; max-width: 1280px; margin-inline: auto; }
}
```

---

## 5. Container Query Candidates

Identify components that appear in multiple slots with different widths within the same breakpoint:

| Signal | Indicates |
|---|---|
| Same component used in sidebar (300px) and main (800px) | Container query candidate |
| Card component in 1col / 2col / 3col grids on same page | Container query candidate |
| Modal / drawer with content that should adapt to drawer width | Container query candidate |

### Output
```yaml
container_query_candidates:
  - component: Card
    contexts: [sidebar(300px), main(800px), modal(600px)]
    recommendation: "Use @container card (min-width: ...) instead of @media"
```

---

## 6. Confidence Annotation

Every derived breakpoint must be tagged:

```css
/* HIGH: Designer explicitly provided 375 / 768 / 1440 frames */
@media (min-width: 768px) { ... }

/* LOW: Derived from desktop-only mockup; tablet behavior inferred */
@media (min-width: 768px) { ... }
```

---

## 7. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Single mockup → assume default breakpoints | Mark all derived breakpoints LOW; recommend designer review |
| Frame width interpreted as breakpoint trigger | Designer width = display, breakpoint trigger may differ; cross-check |
| Auto Layout `direction: HORIZONTAL` mapped to `flex-direction: column` for mobile | Mobile may need vertical reflow — check designer intent per breakpoint |
| Grid `gutter` interpreted as `gap` only | Gutters affect column-width math; verify columns + gutter + margin sum |
| Margin treated as `padding` always | Container max-width + auto margin can be cleaner |
| Ignoring `Layout Grid` count (designer set 12-col but used 8) | Read actual children, not just grid definition |
| Constraint `Scale` mistakenly mapped to fixed px | Use `%` or `fr` units |
| Not checking sticky / fixed positioning constraints | Sticky elements need explicit z-index + positioning |
| Container queries adopted everywhere → browser overhead | Limit to actual multi-context components |

---

## 8. Decision Walkthrough Template

```
Source frames identified:
  □ Mobile (width: ____)
  □ Tablet (width: ____)
  □ Desktop (width: ____)
  □ Wide (width: ____)

Per-frame layout extraction:
  □ Layout Grid (count + gutter + margin)
  □ Auto Layout direction + spacing
  □ Constraints (children)

Breakpoint inference:
  Standard mapping: ____
  Custom breakpoints needed: ____

Container query candidates:
  - Component: ____  Contexts: [____]
  - Component: ____  Contexts: [____]

Confidence:
  HIGH count: ____ (designer-provided)
  LOW count:  ____ (inferred)

Output:
  □ CSS media query stack (mobile-first)
  □ Container query for multi-context components
  □ Auto Layout → flex translation
  □ Layout Grid → CSS Grid translation
  □ Designer review request for LOW values

Handoff:
  □ Pixel for visual fidelity verification
  □ Artisan for production component implementation
```

---

## 9. References
- Figma Layout Grid documentation
- Figma Constraints API
- Figma Auto Layout properties
- CSS Grid Layout Module Level 2
- CSS Container Queries (`@container`)
- W3C CSS Logical Properties (`padding-inline`, `margin-inline`)
