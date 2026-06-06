# Typography Selection Guide

Purpose: Use this reference when selecting typefaces for a project, defining font pairings, or auditing typography choices for brand alignment and quality.

## Contents

- No Default Fonts Rule
- Brand Personality to Typeface Mapping
- Font Pairing Strategies
- Variable Font Advantages
- Performance Considerations
- Typography Selection Process
- Exception: System Fonts for Body Text

---

## No Default Fonts Rule

**Inter, Roboto, and Arial are banned as primary display fonts.**

These fonts are the default output of AI-generated designs and immediately signal "generic template." They are not bad typefaces — they are overused to the point of visual anonymity.

| Font | Status | Rationale |
|------|--------|-----------|
| Inter | Banned as display font | Default for most AI/SaaS tools. Zero brand differentiation |
| Roboto | Banned as display font | Default Android/Material font. Reads as "Google template" |
| Arial | Banned as display font | System default fallback. No intentional design choice |
| Helvetica | Caution | Acceptable only when the brand has a documented Helvetica tradition |

### What "Display Font" Means

Display font = any typeface used for:
- Hero headlines
- Page titles
- Marketing headings
- Brand-prominent text
- Any text at `--text-2xl` (24px) or larger

### Exception: System Fonts for Body Text

System fonts (including Inter and Roboto) are **acceptable for body text** (`--text-base` and below) when:
- Performance is a primary constraint
- The project uses a `system-ui` stack for body
- Body text is not a brand differentiator

```css
/* Acceptable: system font stack for body */
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Display font must be intentionally chosen */
h1, h2, h3, .display {
  font-family: 'Chosen Display Font', sans-serif;
}
```

---

## Brand Personality to Typeface Mapping

Use this table to guide typeface selection based on brand personality:

| Brand Personality | Typeface Characteristics | Example Families |
|-------------------|------------------------|------------------|
| **Technical / Precise** | Geometric sans, clean terminals | Geist, Space Grotesk, JetBrains Mono |
| **Warm / Approachable** | Rounded terminals, open counters | Nunito, Quicksand, Poppins |
| **Premium / Luxury** | High contrast serif, delicate details | Playfair Display, Cormorant, Libre Baskerville |
| **Bold / Energetic** | Heavy weights, tight spacing | Sora, Manrope, Plus Jakarta Sans |
| **Editorial / Authoritative** | Classic serif, traditional proportions | Source Serif Pro, Lora, Merriweather |
| **Playful / Creative** | Variable weight, unusual details | Fraunces, Bricolage Grotesque, Outfit |
| **Minimal / Restrained** | Neutral sans with distinctive details | Satoshi, General Sans, Switzer |
| **Developer / CLI** | Monospace with personality | Berkeley Mono, Monaspace, Commit Mono |

---

## Font Pairing Strategies

### Strategy 1: Contrast Pairing (Recommended)

Pair typefaces with different classifications for clear hierarchy.

| Display | Body | Effect |
|---------|------|--------|
| Serif display | Sans body | Classic editorial feel |
| Geometric display | Humanist body | Modern but readable |
| Heavy sans display | Light sans body | Strong hierarchy through weight |

### Strategy 2: Superfamily

Use a single type family with enough weight/width range.

| Advantage | Risk |
|-----------|------|
| Guaranteed harmony | Can feel monotone without careful weight management |
| Simpler font loading | Limited personality range |
| Easier maintenance | |

### Strategy 3: Variable Font Single Family

One variable font with wide weight and optional width axes.

| Advantage | Risk |
|-----------|------|
| Single file, many weights | Limited to one family's personality |
| Best performance | Requires browser support (widely available) |
| Fluid responsive typography | |

### Pairing Rules

1. **Maximum 2 font families per project** (display + body)
2. **Never pair two serif fonts** or **two geometric sans fonts**
3. **Ensure sufficient contrast** between display and body weights
4. **Test at actual sizes** — pairings that work at 16px may fail at 48px
5. **Check x-height compatibility** — mismatched x-heights create visual friction

---

## Variable Font Advantages

| Advantage | Detail |
|-----------|--------|
| File size | One file replaces 6-10 static font files |
| Performance | Single HTTP request, fewer layout shifts |
| Design flexibility | Precise weight tuning (e.g., `font-weight: 450`) |
| Responsive typography | Weight can adjust with viewport |
| Animation | Smooth weight/width transitions |

### Recommended Variable Fonts

| Font | Axes | Best For |
|------|------|----------|
| Geist | weight | Developer tools, technical products |
| Satoshi | weight | Minimal, modern interfaces |
| Plus Jakarta Sans | weight | Bold, energetic brands |
| Fraunces | weight, optical size | Creative, editorial |
| Source Serif 4 | weight, optical size | Authoritative, editorial |

```css
/* Variable font with optical sizing */
@font-face {
  font-family: 'Display Font';
  src: url('/fonts/display-variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}
```

---

## Performance Considerations

### Font Loading Strategy

| Strategy | When to Use |
|----------|------------|
| `font-display: swap` | Default. Prevents invisible text |
| `font-display: optional` | Performance-critical pages. May show fallback |
| Preload critical fonts | Hero/above-fold display fonts |
| Subset fonts | When using < 100 characters from a family |

### Performance Budget

| Metric | Target |
|--------|--------|
| Total font weight | < 150KB (all families, compressed) |
| Font files count | ≤ 4 files (prefer variable fonts) |
| First font load | < 100ms on 4G |
| CLS from font swap | < 0.05 |

### Loading Priority

```html
<!-- Preload display font (critical) -->
<link rel="preload" href="/fonts/display.woff2" as="font" type="font/woff2" crossorigin>

<!-- Body font can load normally -->
<link rel="stylesheet" href="/fonts/body.css">
```

---

## Typography Selection Process

### Step 1: Define Brand Personality

Identify 3-5 brand personality keywords using the mapping table above.

### Step 2: Select Display Font

1. Use the personality mapping to narrow to 2-3 candidate families
2. Verify the font is NOT on the banned list
3. Test at hero sizes (`--text-4xl` and `--text-5xl`)
4. Check weight range (need at least regular + bold, prefer variable)
5. Verify licensing for the project context

### Step 3: Select Body Font (or System Stack)

1. If performance is critical → use system font stack for body
2. Otherwise → select a complementary family using pairing strategies
3. Test at body size (`--text-base`) for readability
4. Verify x-height compatibility with display font

### Step 4: Validate

- [ ] Display font is not Inter, Roboto, or Arial
- [ ] Maximum 2 font families
- [ ] Total font weight < 150KB
- [ ] Font pairing tested at actual sizes
- [ ] `font-display: swap` or `optional` set
- [ ] Fallback fonts specified
- [ ] Brand personality reflected in type choices
