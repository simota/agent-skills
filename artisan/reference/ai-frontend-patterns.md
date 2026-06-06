# AI Frontend Patterns

Purpose: Use this reference when building frontend pages with AI-assisted generation, particularly landing pages and marketing sites using React + Tailwind.

## Contents

- Why React + Tailwind Works for AI Generation
- Composition-Aware Component Templates
- Layout Anti-Patterns
- Tailwind Token Alignment Guide
- AI-Generated Page Checklist

---

## Why React + Tailwind Works for AI Generation

| Advantage | Detail |
|-----------|--------|
| Inline styling | Tailwind classes in JSX keep style close to structure, reducing context-switching |
| Predictable output | Utility classes produce consistent, reviewable results |
| Token alignment | Tailwind's spacing/color scale maps directly to design tokens |
| Component composition | React's component model enables reusable, composable page sections |
| AI readability | AI models generate more reliable code when style is co-located with markup |

### The AI Generation Problem

AI-generated frontends default to common patterns: card grids, icon rows, stat strips. These patterns are over-represented in training data. **Explicit composition constraints** are needed to break out of this default.

---

## Composition-Aware Component Templates

### Hero Section Template

```tsx
interface HeroProps {
  headline: string;
  subline: string;
  ctaLabel: string;
  ctaHref: string;
  image: {
    src: string;
    alt: string;
  };
  secondaryCta?: {
    label: string;
    href: string;
  };
}

function Hero({ headline, subline, ctaLabel, ctaHref, image, secondaryCta }: HeroProps) {
  return (
    <section className="relative min-h-[80vh] flex items-center">
      {/* Full-bleed image */}
      <img
        src={image.src}
        alt={image.alt}
        className="absolute inset-0 w-full h-full object-cover"
      />
      {/* Content overlay */}
      <div className="relative z-10 max-w-3xl mx-auto px-6 py-24 text-center">
        <h1 className="text-5xl font-bold tracking-tight text-white">
          {headline}
        </h1>
        <p className="mt-4 text-xl text-white/80 max-w-xl mx-auto">
          {subline}
        </p>
        <div className="mt-8 flex items-center justify-center gap-4">
          <a href={ctaHref} className="rounded-lg bg-white px-6 py-3 font-semibold text-gray-900 hover:bg-gray-100 transition-colors">
            {ctaLabel}
          </a>
          {secondaryCta && (
            <a href={secondaryCta.href} className="text-white underline underline-offset-4 hover:text-white/80 transition-colors">
              {secondaryCta.label}
            </a>
          )}
        </div>
      </div>
    </section>
  );
}
```

**Key constraints:**
- Single composition: one image, one headline, one subline, one CTA
- Full-bleed image by default
- No cards, stats, or metadata in hero
- Secondary CTA is visually subordinate (text link, not button)

### Content Section Template

```tsx
interface SectionProps {
  purpose: string; // Named purpose for the section (used as data attribute for auditing)
  children: React.ReactNode;
  background?: 'base' | 'raised';
}

function Section({ purpose, children, background = 'base' }: SectionProps) {
  return (
    <section
      data-purpose={purpose}
      className={cn(
        'py-16 md:py-24 px-6',
        background === 'raised' && 'bg-gray-50 dark:bg-gray-900'
      )}
    >
      <div className="max-w-5xl mx-auto">
        {children}
      </div>
    </section>
  );
}
```

**Key constraints:**
- `purpose` prop forces naming the section's single job
- No card wrapper by default
- Background variation through color, not cards or borders

### Page Composition Template

```tsx
function LandingPage() {
  return (
    <main>
      {/* Hero: Brand + Headline + CTA + Visual */}
      <Hero {...heroProps} />

      {/* Support: Trust & Context */}
      <Section purpose="social-proof">
        {/* Testimonials, logos, or key benefit */}
      </Section>

      {/* Detail: Depth & Evidence */}
      <Section purpose="features" background="raised">
        {/* Feature descriptions — NOT a card grid */}
      </Section>

      <Section purpose="how-it-works">
        {/* Process or workflow explanation */}
      </Section>

      {/* Final CTA: Closure */}
      <Section purpose="final-cta" background="raised">
        {/* Reinforced action with summary */}
      </Section>
    </main>
  );
}
```

---

## Layout Anti-Patterns

### What AI Generates by Default (and Why It's Wrong)

| Anti-Pattern | AI Default | Problem | Better Approach |
|-------------|------------|---------|-----------------|
| Card grid hero | 3-4 feature cards at top of page | No visual anchor, no hierarchy | Single hero composition |
| Pill cluster | Horizontal scrolling tags/categories | Visual noise, low information density | Categorized list or text grouping |
| Stat strip | `100+` / `50K` / `99.9%` in a row | Generic, unverifiable, low trust | Stats integrated into narrative context |
| Icon row | Grid of icons with captions | Undifferentiated, forgettable | Feature sections with real descriptions |
| Bento grid | Asymmetric card grid for features | Complex layout with uniform visual weight | Sequential sections with varied layouts |
| Testimonial carousel | Auto-rotating quotes | Hidden content, lost control | 1-2 highlighted testimonials |

### Detection in Code Review

```
// Red flags in AI-generated code:
// 1. "grid grid-cols-3" in hero section → card grid default
// 2. "flex flex-wrap gap-2" with short text items → pill cluster
// 3. Three <div> siblings with large numbers → stat strip
// 4. "grid grid-cols-4" with icon + text pattern → icon row
// 5. "grid-cols-2 md:grid-cols-3 lg:grid-cols-4" → default responsive grid
```

---

## Tailwind Token Alignment Guide

Map design tokens to Tailwind utility classes for consistent usage:

### Color Tokens

| Token Role | Tailwind Class | Usage |
|-----------|---------------|-------|
| Background (base) | `bg-white dark:bg-gray-950` | Page background |
| Background (surface) | `bg-gray-50 dark:bg-gray-900` | Raised sections |
| Primary text | `text-gray-900 dark:text-gray-50` | Headings, body |
| Muted text | `text-gray-500 dark:text-gray-400` | Secondary info |
| Accent | `text-blue-600 dark:text-blue-400` | Links, CTAs, active states |

### Spacing Tokens

| Token | Tailwind | Usage |
|-------|----------|-------|
| `--space-1` (4px) | `gap-1`, `p-1` | Icon-to-text spacing |
| `--space-2` (8px) | `gap-2`, `p-2` | Button padding, tight groups |
| `--space-4` (16px) | `gap-4`, `p-4` | Card padding, form spacing |
| `--space-6` (24px) | `gap-6`, `p-6` | Section internal spacing |
| `--space-12` (48px) | `py-12` | Section separation (mobile) |
| `--space-16` (64px) | `py-16`, `md:py-24` | Section separation (desktop) |

### Typography Tokens

| Token | Tailwind | Usage |
|-------|----------|-------|
| `--text-sm` (14px) | `text-sm` | Metadata, helper text |
| `--text-base` (16px) | `text-base` | Body text |
| `--text-xl` (20px) | `text-xl` | Small headings |
| `--text-3xl` (30px) | `text-3xl` | Section headings |
| `--text-5xl` (48px) | `text-5xl` | Hero headline |

---

## AI-Generated Page Checklist

Use this checklist when reviewing any AI-generated frontend page:

```markdown
## AI Frontend Review

### Composition
- [ ] Hero is a single composition (not a card grid)
- [ ] One visual anchor in first viewport
- [ ] Hero satisfies: brand + headline + subline + CTA + visual
- [ ] No cards/stats/metadata in hero section

### Layout
- [ ] No default card grids for non-interactive content
- [ ] Each section has a named `purpose`
- [ ] No pill clusters, stat strips, or icon rows
- [ ] Cards used only for actionable/comparable items

### Page Structure
- [ ] Follows Hero → Support → Detail → Final CTA flow
- [ ] CTA appears at least twice (hero + end)
- [ ] Visual weight decreases down the page
- [ ] Each section serves one purpose

### Tailwind Usage
- [ ] Spacing follows 8px grid (p-2, p-4, p-6, not p-3, p-5)
- [ ] Color classes use semantic roles (not arbitrary values)
- [ ] Dark mode classes present for all color utilities
- [ ] Responsive breakpoints follow mobile-first

### Typography
- [ ] Display font is intentionally chosen (not Inter/Roboto/Arial)
- [ ] Clear heading hierarchy (size + weight steps)
- [ ] Body text ≥ 16px on mobile
```
