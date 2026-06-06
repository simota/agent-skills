# Intentional Motion Framework

Purpose: Use this reference when planning motion for a page or view. Limits motion to 2-3 intentional types per view to avoid the "everything animates" anti-pattern.

> **2026 platform default = motion-rich.** Both **Material 3 Expressive** (Android 16, spring-based physics on every default transition) and **Apple Liquid Glass** (iOS 26, depth-aware materials reacting to context and motion) make the *platform itself* motion-rich out of the box. The 2-3 Motion Rule below now means "2-3 *team-authored* motion types on top of whatever the platform is already animating" — not "2-3 motion types total". When the platform contributes a spring on every interaction, team-authored decorative motion needs to clear a higher bar; the budget below tightens, it does not relax.

## Contents

### Reduced-Motion-First Design Philosophy

The design order is inverted: **design reduced-motion first, then add full motion**.

| Priority | Reduced Motion | Full Motion |
|----------|---------------|-------------|
| 1 (Always) | State feedback (success/error/loading) | State feedback + entrance animation |
| 2 (Always) | Focus indicators, active states | + subtle scale/opacity transitions |
| 3 (Optional) | Static layout changes | + slide/fade transitions |
| 4 (Enhancement only) | None | Parallax, scroll-driven, decorative motion |

**Critical rule**: Never disable ALL animation under `prefers-reduced-motion`. Functional feedback (loading spinners, error shakes, success checks) must persist. Only decorative and large-displacement motion should be removed.

```css
/* Base: reduced motion (functional feedback only) */
.button:active { scale: 0.97; }
.toast { opacity: 1; }

/* Enhancement: full motion */
@media (prefers-reduced-motion: no-preference) {
  .button:active { scale: 0.97; transition: scale 0.1s ease; }
  .toast { animation: slide-up 0.3s ease-out; }
}
```

### Purposeful Motion Manifesto

Every animation must answer ONE of these questions:

1. **Where am I?** — Spatial orientation (page transitions, navigation feedback)
2. **What changed?** — State communication (toggle, form validation, data update)
3. **What should I do?** — Attention guidance (onboarding spotlight, CTA pulse)
4. **What's happening?** — Process feedback (loading, progress, async operations)

If an animation answers none of these, it is decorative and should be the first to go under reduced-motion or performance constraints.

- The 2-3 Motion Rule
- Motion Slot System
- Slot Definitions
- Reduced Motion Requirements
- Motion Audit Process
- Common Slot Configurations

---

## The 2-3 Motion Rule

**Every view should have at most 2-3 distinct motion types.** More than 3 creates visual chaos and reduces the effectiveness of each animation.

| Principle | Rule |
|-----------|------|
| Motion budget | Maximum 3 distinct motion types per view |
| Each motion has a job | Entry, feedback, or continuity — no decorative motion |
| Absence is a choice | Not every element needs animation |
| Motion earns attention | If everything moves, nothing stands out |

**"Distinct motion type"** = a unique combination of purpose, timing, and trigger. Two buttons with identical hover effects count as one type. A hover effect and a scroll reveal count as two types.

---

## Motion Slot System

Each view has 3 motion "slots." You must choose which slots to fill. Leaving a slot empty is often the right choice.

| Slot | Purpose | Trigger | Duration Range |
|------|---------|---------|---------------|
| **Slot 1: Hero Entrance** | Draw attention to the primary content | Page load / route change | 300-600ms |
| **Slot 2: Scroll-Linked** | Create depth and progression | Scroll position | Continuous or 200-400ms |
| **Slot 3: Interaction Feedback** | Confirm user actions | Hover / click / focus | 150-250ms |

### Slot Rules

- Fill Slot 3 first (interaction feedback is highest priority)
- Slot 1 is optional (many views don't need a hero entrance)
- Slot 2 is the most dangerous (scroll animations easily become distracting)
- Never fill all 3 slots with heavy animations

---

## Slot Definitions

### Slot 1: Hero Entrance (300-600ms)

The first thing the user sees when entering a view. Use for brand moments and primary content reveal.

| Pattern | Duration | Properties | Use When |
|---------|----------|-----------|----------|
| Fade up | 400ms | opacity, translateY(8-16px) | Default hero entrance |
| Scale reveal | 500ms | opacity, scale(0.95→1) | Image or media hero |
| Stagger reveal | 300ms per item, 80ms stagger | opacity, translateY | Multi-element hero (max 4 items) |
| Clip reveal | 600ms | clip-path | Editorial or premium feel |

**Reduced motion:** Replace with instant opacity fade (150ms) or no animation.

### Slot 2: Scroll-Linked (Continuous or 200-400ms)

Animations triggered or driven by scroll position. These are high-risk for distraction.

| Pattern | Duration | Properties | Use When |
|---------|----------|-----------|----------|
| Scroll fade-in | 200-400ms | opacity, translateY | Content sections entering viewport |
| Sticky transitions | Continuous | position, opacity | Navigation state changes |
| Parallax (subtle) | Continuous | translateY at 0.1-0.3x scroll rate | Background depth (use sparingly) |
| Progress indicator | Continuous | scaleX, width | Reading progress or step progress |

**Reduced motion:** Remove parallax entirely. Keep scroll fade-in as instant appearance. Keep functional indicators.

### Slot 3: Interaction Feedback (150-250ms)

Micro-interactions that confirm user actions. These are the highest-priority motion type.

| Pattern | Duration | Properties | Use When |
|---------|----------|-----------|----------|
| Hover state | 150ms | background-color, opacity, scale(1.02) | Buttons, cards, links |
| Press feedback | 100ms | scale(0.98), background-color | Clickable elements |
| Focus ring | 150ms | outline, box-shadow | Keyboard navigation |
| Toggle state | 200ms | translateX, background-color | Switches, checkboxes |
| Layout transition | 250ms | height, opacity | Expanding/collapsing sections |
| Reveal/tooltip | 200ms | opacity, translateY(4px) | Popovers, tooltips, dropdowns |

**Reduced motion:** Keep hover color changes. Remove scale transforms. Keep focus indicators. Reduce duration to 100ms or instant.

---

## Reduced Motion Requirements

**Every motion slot requires a reduced-motion fallback.** No exceptions.

### Implementation Pattern

```css
/* Default: full motion */
.hero-title {
  opacity: 0;
  transform: translateY(16px);
  animation: hero-enter 400ms ease-out forwards;
}

/* Reduced motion: instant or no animation */
@media (prefers-reduced-motion: reduce) {
  .hero-title {
    opacity: 1;
    transform: none;
    animation: none;
  }
}
```

### Reduced Motion Decision Guide

| Original Motion | Reduced Motion Action |
|----------------|----------------------|
| Position/scale entrance | Remove or instant opacity fade (150ms) |
| Scroll parallax | Remove entirely |
| Hover scale | Remove. Keep color change |
| Toggle slide | Instant state change |
| Loading spinner | Keep (functional, low-intensity) |
| Progress bar | Keep (functional information) |
| Page transition | Instant cut or cross-fade (150ms) |

---

## Motion Audit Process

### Per-View Audit

For each view or page, document the motion types in use:

```markdown
## Motion Audit: [View Name]

### Active Slots
| Slot | Motion Type | Duration | Purpose | Reduced Motion |
|------|-------------|----------|---------|---------------|
| 1 | [type or empty] | [ms] | [purpose] | [fallback] |
| 2 | [type or empty] | [ms] | [purpose] | [fallback] |
| 3 | [type or empty] | [ms] | [purpose] | [fallback] |

### Motion Count
- Total distinct motion types: [N] (must be ≤ 3)
- Reduced motion coverage: [complete / gaps identified]

### Violations
- [ ] No slot exceeds its duration range
- [ ] No decorative-only animations
- [ ] All slots have reduced-motion fallbacks
- [ ] Total distinct types ≤ 3
```

### Red Flags

| Signal | Problem |
|--------|---------|
| > 3 motion types per view | Motion budget exceeded |
| All 3 slots filled with heavy animation | Visual overload |
| Scroll animation on every section | Slot 2 abuse |
| Micro-interactions without reduced-motion | Accessibility gap |
| Animation duration > 600ms | Motion feels sluggish |
| Animation purpose is "it looks cool" | Decorative motion (remove it) |

---

## Common Slot Configurations

### Landing Page (Recommended)

| Slot | Choice | Notes |
|------|--------|-------|
| 1 | Hero fade-up (400ms) | First viewport reveal |
| 2 | Empty or minimal scroll fade-in | Avoid parallax unless brand-critical |
| 3 | Hover/press feedback (150ms) | CTAs and interactive elements |

### App Dashboard

| Slot | Choice | Notes |
|------|--------|-------|
| 1 | Empty | Dashboards should load instantly, no entrance animation |
| 2 | Empty | Data should appear, not animate in |
| 3 | Hover/toggle/expand feedback (150-250ms) | All interactive elements |

### Settings / Admin

| Slot | Choice | Notes |
|------|--------|-------|
| 1 | Empty | No entrance needed |
| 2 | Empty | No scroll animation |
| 3 | Toggle/expand feedback (200ms) | Switches, accordions |

### Editorial / Blog

| Slot | Choice | Notes |
|------|--------|-------|
| 1 | Article title fade (300ms) | Subtle entrance |
| 2 | Reading progress bar (continuous) | Functional scroll indicator |
| 3 | Link hover feedback (150ms) | Minimal |
