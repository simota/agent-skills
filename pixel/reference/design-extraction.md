# Design Extraction

**Purpose:** Claude Vision prompt strategies for extracting design values (colors, fonts, spacing, layout) from mockup images.
**Read when:** You need to analyze a mockup image and extract implementable CSS values.

## Contents
- Extraction Workflow
- Color Extraction
- Typography Extraction
- Spacing Extraction
- Layout Extraction
- Confidence Level Rules
- Extraction Report Template

---

## Extraction Workflow

```
Image → Global Scan → Section-by-Section → Value Catalog → Confidence Assignment
```

### Multi-Pass Approach (Best Practice)

Single-prompt extraction is less accurate. Use staged passes for better precision:

1. **Pass 1 — Structure Analysis**: Identify semantic HTML structure (header, nav, main, section, aside, footer) and nesting relationships.
2. **Pass 2 — Design Token Extraction**: Extract colors (HEX), font sizes (px), spacing (px), border-radius, shadows as JSON.
3. **Pass 3 — Code Generation**: Use Pass 1 + 2 results as input to generate HTML/CSS.

This multi-pass approach significantly improves extraction quality vs. a single "generate code from this image" prompt.

### Key Prompt Engineering Principles

Based on screenshot-to-code best practices (abi/screenshot-to-code, 71k+ GitHub stars):

- **Provide viewport context**: Always specify the image's viewport width (e.g., "This image is a 1440px desktop view"). This drastically improves pixel value estimation.
- **Apply design system constraints**: Tell the model to snap to a 4px/8px grid, or provide a color palette to match against.
- **Process component-by-component**: Crop and process individual sections rather than the full page for better accuracy.
- **No placeholders**: Instruct the model to write out ALL elements fully. If the mockup shows 15 items, the code must have 15 items.
- **Exact text reproduction**: Use the exact text visible in the screenshot, not summarized versions.
- **Negative instructions**: "Do not guess values. Mark anything you can't clearly read as `[UNKNOWN]`."

### Step 1: Global Scan

Analyze the full mockup image for:
- Overall color palette (background, text, accent colors)
- Typography scale (heading sizes relative to body)
- Layout system (grid columns, max-width, alignment)
- Section boundaries and visual hierarchy

### Step 2: Section-by-Section Extraction

For each identified section:
1. Identify the section type (Hero, Features, etc.)
2. Extract section-specific values
3. Note relationships to adjacent sections (spacing, color transitions)

### Step 3: Value Catalog

Compile all extracted values into a structured catalog with confidence annotations.

---

## Color Extraction

### Strategy

1. **Large uniform areas first**: Backgrounds, solid buttons — highest confidence.
2. **Text colors**: Primary heading, body text, muted/secondary text.
3. **Accent colors**: CTAs, links, highlights, badges.
4. **Borders and dividers**: Typically lighter variants of background.

### Prompt Pattern

When analyzing colors with Claude Vision:

```
この画像のカラーパレットを抽出してください:
1. 背景色（メイン、セカンダリ）
2. テキスト色（見出し、本文、薄いテキスト）
3. アクセントカラー（CTA、リンク、バッジ）
4. ボーダー・ディバイダー色
各色をHEXで推定し、信頼度（HIGH/MEDIUM/LOW）を付けてください。
```

### Common Patterns

| Visual Context | Typical Value | Confidence |
|---------------|--------------|------------|
| Pure white/black background | `#ffffff` / `#000000` | HIGH |
| Near-black text on white | `#111827` or `#1a1a2e` | MEDIUM |
| Gray secondary text | `#6b7280` to `#9ca3af` | MEDIUM |
| Blue accent/CTA | `#2563eb` to `#3b82f6` | MEDIUM |
| Light gray background | `#f9fafb` to `#f3f4f6` | MEDIUM |
| Gradient or overlay | Individual stops | LOW |

### Color Grouping

Group extracted colors into semantic roles. As of 2026-05, `oklch()` and `color-mix(in oklch, …)` are Baseline Widely Available, so use them by default for perceptually uniform derived colors. Reserve hard-coded HEX hover/active variants for cases where the mockup actually pins those values:

```css
:root {
  /* Background */
  --bg-base: #ffffff;         /* HIGH */
  --bg-surface: #f9fafb;     /* MEDIUM */
  --bg-inverse: #111827;     /* HIGH */

  /* Text */
  --text-primary: #111827;   /* MEDIUM */
  --text-secondary: #6b7280; /* MEDIUM */
  --text-inverse: #ffffff;   /* HIGH */

  /* Accent — use color-mix() for derived states */
  --accent-primary: #2563eb; /* MEDIUM */
  --accent-hover: color-mix(in oklch, var(--accent-primary) 85%, black);  /* Derived */
  --accent-subtle: color-mix(in oklch, var(--accent-primary) 12%, white); /* Tint for backgrounds */

  /* Border */
  --border-default: #e5e7eb; /* MEDIUM */
}
```

### Wide-Gamut Mockups (P3 / Rec2020)

If the mockup is exported from a P3-aware tool (Figma export with "Preserve color space", Affinity Designer, ProPhoto RGB Photoshop), expect colors that fall outside sRGB. Annotate them and emit the wide-gamut form alongside the sRGB fallback:

```css
.cta {
  background: #2563eb;                          /* sRGB fallback */
  background: oklch(0.55 0.22 263);             /* P3-aware target */
}
```

Mark wide-gamut extractions as `MEDIUM` at best — the mockup's color profile is often unclear and engines downgrade silently outside `display-p3` color contexts.

### Advanced: Role Detection (VibeMark Pattern)

When possible, detect not just the color value but its semantic role:
- **bg**: Background surfaces
- **text**: Text content colors
- **primary/secondary/accent**: Interactive and emphasis colors
- **border/divider**: Structural separation

This role detection enables automatic dark mode mapping and design token alignment with Muse.

---

## Typography Extraction

### Strategy

1. **Identify the type scale**: Count distinct text sizes visible in the mockup.
2. **Establish a base**: Body text is typically 16px (1rem) — use as reference.
3. **Calculate ratios**: Measure heading sizes relative to body text.
4. **Weight estimation**: Bold (700), Semi-bold (600), Medium (500), Regular (400).

### Prompt Pattern

```
この画像のタイポグラフィを分析してください:
1. 見出しテキストのサイズ（h1, h2, h3推定）
2. 本文テキストのサイズ
3. フォントウェイト（太さ）の推定
4. 行間（line-height）の推定
5. 使用フォントファミリーの推測（可能であれば）
本文を16pxと仮定し、他のサイズを相対的に推定してください。
```

### Size Estimation Table

| Element | Typical Range | Default Estimate | Confidence |
|---------|--------------|-----------------|------------|
| Hero headline | 36-64px | 48px (3rem) | MEDIUM |
| Section heading (h2) | 28-36px | 30px (1.875rem) | MEDIUM |
| Subsection heading (h3) | 20-24px | 20px (1.25rem) | MEDIUM |
| Body text | 14-18px | 16px (1rem) | HIGH (baseline) |
| Small/meta text | 12-14px | 14px (0.875rem) | MEDIUM |
| Button text | 14-18px | 16px (1rem) | MEDIUM |

### Font Family Detection

| Visual Cue | Likely Font Category | Suggestions |
|-----------|---------------------|-------------|
| Geometric, clean | Sans-serif | Inter, Poppins, DM Sans |
| Humanist, warm | Sans-serif | Open Sans, Noto Sans |
| High contrast, serif | Serif | Playfair Display, Merriweather |
| Monospace | Monospace | JetBrains Mono, Fira Code |
| Rounded | Sans-serif | Nunito, Quicksand |

**Important**: Font identification from images is LOW confidence. Always provide 3 candidates and let the user choose. Use variable fonts when available (single file for multiple weights, fewer HTTP requests).

```css
/* LOW: font appears geometric sans-serif — candidates: Inter, Poppins, DM Sans */
font-family: 'Inter', system-ui, -apple-system, sans-serif;
```

### Font Loading Strategy

When generating code, include proper font loading for performance:

```html
<!-- Preload critical font (hero headline weight) -->
<link rel="preload" href="/fonts/heading.woff2" as="font" type="font/woff2" crossorigin>

<!-- Use font-display: optional for zero-CLS font loading -->
<style>
@font-face {
  font-family: 'HeadingFont';
  src: url('/fonts/heading.woff2') format('woff2');
  font-display: optional; /* Prevents CLS; fallback to system font on slow networks */
}

/* Fallback font metrics adjustment to minimize layout shift */
@font-face {
  font-family: 'HeadingFallback';
  src: local('Arial');
  size-adjust: 105%;
  ascent-override: 95%;
}
</style>
```

---

## Spacing Extraction

### Strategy

1. **Identify consistent spacing units**: Look for repeating gaps.
2. **Section padding**: Top/bottom padding of major sections.
3. **Component internal spacing**: Gaps within cards, lists, grids.
4. **Use rem for output**: More maintainable than px.

### Prompt Pattern

```
この画像の余白・間隔を分析してください:
1. セクション間の縦方向の間隔
2. セクション内部のパディング（上下左右）
3. 要素間のギャップ（カード間、リスト項目間など）
4. テキスト間の間隔（見出しと本文の間など）
px単位で推定し、8pxグリッドに丸めてください。
```

### 8px Grid Rounding

Round extracted values to the nearest 8px multiple for consistency:

| Raw Estimate | Rounded | rem | Usage |
|-------------|---------|-----|-------|
| 5-6px | 4px | 0.25rem | Tight inline spacing |
| 7-10px | 8px | 0.5rem | Icon-text gap |
| 11-20px | 16px | 1rem | Component spacing |
| 21-28px | 24px | 1.5rem | Card padding |
| 29-40px | 32px | 2rem | Section internal |
| 50-70px | 64px | 4rem | Section padding (mobile) |
| 80-100px | 96px | 6rem | Section padding (desktop) |

---

## Layout Extraction

### Strategy

1. **Max-width**: Identify the content container width.
2. **Grid system**: Count columns, identify gutter sizes.
3. **Alignment**: Center, left-aligned, or asymmetric.
4. **Flex vs Grid**: Determine which CSS layout model fits.

### Prompt Pattern

```
この画像のレイアウトを分析してください:
1. コンテンツの最大幅（コンテナ幅）
2. カラム数（グリッドの列数）
3. カラム間のガター幅
4. 主なアライメント（中央揃え、左揃えなど）
5. Flexbox vs CSS Gridのどちらが適切か
```

### Container Width Estimation

| Visual Cue | Likely Width | Confidence |
|-----------|-------------|------------|
| Full-width content | 100% | HIGH |
| Narrow text column | 48rem (768px) | MEDIUM |
| Standard content | 64rem (1024px) | MEDIUM |
| Wide content | 72rem (1152px) | MEDIUM |
| Extra wide | 80rem (1280px) | MEDIUM |

### Grid Detection

| Item Count | Likely Grid | CSS |
|-----------|-------------|-----|
| 2 items side by side | 2-column | `grid-template-columns: repeat(2, 1fr)` |
| 3 items in a row | 3-column | `grid-template-columns: repeat(3, 1fr)` |
| 4 items in a row | 4-column or 2x2 | Check if wrapping at mobile |
| 6 items | 3x2 grid | `grid-template-columns: repeat(3, 1fr)` |
| Uneven layout | Asymmetric | `grid-template-columns: 2fr 1fr` or similar |
| Aligned card content across rows (title row, CTA row, etc.) | Subgrid (Baseline 2026-03) | Parent `grid-template-rows: ...`; child `grid-template-rows: subgrid` |
| Staggered "Pinterest" layout | Treat as JS Masonry until native Masonry is Baseline | See `responsive-design.md` — do NOT emit `grid-template-rows: masonry` without a fallback |

### Detect Subgrid Opportunities Early

When extracting card grids, check whether the mockup's titles, descriptions, and CTAs sit on the **same horizontal lines across cards**. If yes, that is a Subgrid signal — emit the Subgrid pattern instead of hard-coded `min-height` workarounds. Confidence is `HIGH` when alignment is visually exact in the mockup, `MEDIUM` when it looks approximate.

---

## Confidence Level Rules

### Assignment Criteria

| Level | When to Assign | Example |
|-------|---------------|---------|
| **HIGH** (≥90%) | Value is clearly identifiable; large, uniform area; binary choice | Solid white background: `#ffffff` |
| **MEDIUM** (70-89%) | Reasonable estimate; multiple similar possibilities | Body text color appears to be `#374151` |
| **LOW** (<70%) | Ambiguous; compressed image; small area; gradient | Font family: "appears to be Inter" |

### Annotation Format in Code

```css
/* HIGH: solid background clearly white */
background-color: #ffffff;

/* MEDIUM: heading appears ~48px, could be 44-52px range */
font-size: 3rem;

/* LOW: font appears geometric sans-serif, verify with designer */
font-family: 'Inter', system-ui, sans-serif;
```

### When to Escalate

- 5+ LOW confidence values in a single section → flag for designer review
- Color values differ by more than 2 shades from expected → re-analyze with focused prompt
- Font size ratio doesn't follow a standard type scale → annotate and suggest common alternatives

---

## Extraction Report Template

```markdown
## Design Extraction Report

### Color Palette
| Role | Value | Confidence | Notes |
|------|-------|------------|-------|
| Background (base) | #ffffff | HIGH | |
| Text (primary) | #111827 | MEDIUM | Could be #1a1a2e |
| Accent | #2563eb | MEDIUM | Blue CTA button |

### Typography
| Element | Size | Weight | Line Height | Confidence |
|---------|------|--------|-------------|------------|
| h1 (Hero) | 3rem | 700 | 1.1 | MEDIUM |
| h2 (Section) | 1.875rem | 700 | 1.2 | MEDIUM |
| Body | 1rem | 400 | 1.6 | HIGH (baseline) |

### Spacing
| Context | Value | Confidence |
|---------|-------|------------|
| Section padding | 5rem top/bottom | MEDIUM |
| Grid gap | 2rem | MEDIUM |
| Component internal | 1.5rem | MEDIUM |

### Layout
| Property | Value | Confidence |
|----------|-------|------------|
| Container max-width | 72rem | MEDIUM |
| Grid columns | 3 | HIGH |
| Alignment | Center | HIGH |

### Font Family
| Detected | Suggestion | Confidence |
|----------|-----------|------------|
| Geometric sans-serif | Inter, Poppins | LOW |
```
