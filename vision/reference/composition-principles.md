# Composition Principles

Purpose: Use this reference when defining page composition, hero sections, layout structure, or image strategy for any design direction.

## Contents

- First Viewport Rule
- Hero Contract
- Layout Restraint
- Image Strategy
- Page Structure
- Composition Audit Checklist

---

## First Viewport Rule

The first viewport is a **single composition**, not a dashboard.

| Principle | Rule |
|-----------|------|
| Single focus | One visual anchor, one message, one action |
| No dashboard default | Never open with cards, stats, or metadata grids |
| Composition over information density | Prioritize visual hierarchy over content volume |
| Scroll earns complexity | Detail and density belong below the fold |

**Test:** Screenshot the first viewport. If it looks like a dashboard or admin panel, it fails.

---

## Hero Contract

Every hero section must satisfy this contract:

| Element | Required | Rules |
|---------|----------|-------|
| Brand signal | Yes | Logo, color, or typography that identifies the brand within 2 seconds |
| Headline | Yes (1 only) | Product language, not design commentary. Maximum 12 words |
| Subline | Yes (1 only) | Supports the headline with a benefit or clarification. Maximum 25 words |
| CTA | Yes (1 primary) | One clear action. Secondary CTA optional but visually subordinate |
| Visual | Yes (1 only) | Full-bleed image default. Real product photo preferred over illustration |

**Prohibited in hero:**
- Card grids or card clusters
- Statistics or metric displays
- Metadata or tag lists
- Multiple competing visuals
- Decorative gradient backgrounds as the main visual element

**Full-bleed image default:** Unless the brand direction explicitly requires contained images, hero images should extend to viewport edges.

---

## Layout Restraint

### Default: No Cards

Cards are not a layout tool. They are interactive containers.

| Use cards when | Do NOT use cards when |
|---------------|----------------------|
| Content is individually actionable (click, expand, select) | Displaying static information sections |
| Items are peers in a collection (products, team members) | Wrapping text blocks for visual separation |
| Content needs to be compared side by side | Creating visual rhythm (use spacing instead) |
| Content can be reordered or filtered | Filling empty space |

### Section Purpose Rule

**One section = one purpose.** If a section serves two purposes, split it into two sections.

| Anti-pattern | Fix |
|-------------|-----|
| Feature grid + testimonials in one section | Separate into Features section + Social Proof section |
| Pricing table + FAQ combined | Separate into Pricing section + FAQ section |
| Hero with embedded feature highlights | Hero section + Features section below |

### Layout Anti-Patterns

| Pattern | Problem | Alternative |
|---------|---------|-------------|
| Pill clusters | Visual noise, low information density | Categorized list or simple text grouping |
| Stat strips (3-4 numbers in a row) | Generic, low-trust without context | Inline stats within narrative sections |
| Icon rows (feature icons in grid) | Undifferentiated, forgettable | Feature sections with real descriptions |
| Card grids as default layout | Lazy composition, no hierarchy | Purpose-driven sections with clear hierarchy |
| Stacked cards as page structure | Everything looks equally important | Varied section layouts with visual weight |

---

## Image Strategy

### Hierarchy of Image Quality

1. **Real product photography** — highest trust, strongest brand signal
2. **Custom illustration** — brand-aligned, distinctive when well-executed
3. **Curated stock photography** — acceptable for supporting sections, not heroes
4. **AI-generated imagery** — acceptable for concepts and mood, requires brand review
5. **Generic 3D renders** — low trust, high "template" risk
6. **Decorative gradients** — never as main visual; acceptable as subtle background treatment

### Image Rules

| Rule | Rationale |
|------|-----------|
| Product photos over fake 3D | Real imagery builds trust and recognition |
| No decorative gradients as hero visual | Gradients signal "no real content yet" |
| Images must support the message | Every image should reinforce the headline or section purpose |
| Busy images never behind text | Text over complex images fails readability and accessibility |
| Alt text required for all meaningful images | Accessibility baseline |

---

## Page Structure

Standard page flow for marketing and product pages:

```
┌─────────────────────────────┐
│  HERO                       │  Brand + Headline + CTA + Visual
│  (First Viewport)           │  Single composition
├─────────────────────────────┤
│  SUPPORT                    │  Social proof, key benefits,
│  (Trust & Context)          │  or problem statement
├─────────────────────────────┤
│  DETAIL                     │  Features, how-it-works,
│  (Depth & Evidence)         │  use cases, pricing
│  (Multiple sections OK)     │
├─────────────────────────────┤
│  FINAL CTA                  │  Reinforced action with
│  (Closure)                  │  summary value proposition
└─────────────────────────────┘
```

### Structure Rules

| Rule | Detail |
|------|--------|
| Hero → Support → Detail → Final CTA | This order is the default. Deviations require rationale |
| Each section has one job | Name the job. If you can't name it in 3 words, split the section |
| Visual weight decreases downward | Hero is heaviest; Detail sections are lighter |
| CTA appears twice minimum | Once in Hero, once at page end |
| No orphan sections | Every section must connect to the narrative above or below |

---

## Intrinsic Layout (2025-2026)

The paradigm has shifted from "Responsive Design" to "Intrinsic Design." A component does not know the viewport size; it only knows its container size.

### Container Queries (93.92% global browser support, Dec 2025)

Use `@container` instead of `@media` for component-level responsiveness:
```css
.card-wrapper { container-type: inline-size; }

@container (min-width: 400px) {
  .card { display: grid; grid-template-columns: 1fr 2fr; }
}
```

### Fluid Typography with clamp()

Single declaration scales smoothly between min and max:
```css
h1 { font-size: clamp(1.5rem, 4vw, 3rem); }
```

### Intrinsic Sizing with CSS Grid

Content defines layout, not arbitrary breakpoints:
```css
.grid {
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
}
```

---

## Composition Audit Checklist

Use this checklist when reviewing any page or screen composition:

```markdown
## Composition Audit

### First Viewport
- [ ] Single composition (not a dashboard)
- [ ] Clear visual anchor
- [ ] One headline, one subline, one CTA
- [ ] Brand identifiable within 2 seconds

### Hero Contract
- [ ] Satisfies all 5 required elements
- [ ] No prohibited elements present
- [ ] Image is full-bleed (or justified deviation)

### Layout
- [ ] No default card grids
- [ ] Each section has one named purpose
- [ ] No pill clusters, stat strips, or icon rows
- [ ] Cards used only for interactive/actionable content

### Images
- [ ] Real product photos preferred
- [ ] No decorative gradients as main visual
- [ ] No busy images behind text
- [ ] All images support the section message

### Page Flow
- [ ] Hero → Support → Detail → Final CTA structure
- [ ] Visual weight decreases downward
- [ ] CTA appears at least twice
- [ ] No orphan sections
```
