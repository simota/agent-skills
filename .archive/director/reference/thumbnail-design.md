# Thumbnail Design Reference

Purpose: Design per-platform thumbnails for demo videos. Cover aspect ratios (YouTube 1280×720, LinkedIn 1200×627, X 1600×900, Product Hunt 1200×1200), composition principles (face + text + product), contrast + legibility, A/B test matrix, and CTR optimization.

## Scope Boundary

- **director `thumbnail`**: Thumbnail design for demos (this document).
- **director `demo` / `voiceover` / `captions` (elsewhere)**: Video production phases.
- **growth (elsewhere)**: SEO / CTR optimization strategy (complementary).
- **funnel (elsewhere)**: Landing-page visuals (different domain).
- **ink / sketch (elsewhere)**: Illustration / AI image generation (asset-layer tools).

## Why Thumbnails Matter

YouTube: 90% of top-performing videos use custom thumbnails. CTR correlates strongly with thumbnail quality. A ×2 CTR improvement typically doubles view-through.

For LinkedIn / X / Product Hunt: thumbnail is the *only* pre-click signal. Static preview image = entire marketing asset.

## Platform Spec Matrix

| Platform | Aspect | Size | File | Notes |
|----------|--------|------|------|-------|
| YouTube | 16:9 | 1280×720 | JPG / PNG, ≤2MB | Most important platform |
| LinkedIn | ~1.91:1 | 1200×627 | JPG / PNG | Article + post preview |
| X (Twitter) | 16:9 | 1600×900 | JPG / PNG, ≤5MB | Summary card + video |
| Instagram feed | 4:5 | 1080×1350 | JPG / PNG | Vertical bias |
| Instagram story | 9:16 | 1080×1920 | JPG / PNG | Fullscreen vertical |
| TikTok cover | 9:16 | 1080×1920 | JPG | Vertical |
| Product Hunt | 1:1 | 1200×1200 | JPG / PNG / GIF | Square gallery |
| Vimeo | 16:9 | 1280×720 | JPG / PNG | Same as YouTube |
| Slack / Discord preview | 16:9 | 1280×720 | any | Default OG-image |
| OG image (web) | 1.91:1 | 1200×630 | JPG / PNG | Site share |

Generate thumbnails for *all* target platforms. Reusing a 16:9 thumbnail on 1:1 Product Hunt crops the sides.

## Core Composition Principles

### Rule of Thirds + Focal Point

Place key subject at one of four intersection points (not dead-center). Eye-tracking research: viewers scan F-pattern, attention lands at upper-left or upper-right third.

### Three-Element Rule

Most high-CTR thumbnails have:
1. **Face** (expressive, looking at viewer or product)
2. **Product** (clear UI screenshot, logo, or key visual)
3. **Text overlay** (3-5 words max, hook / promise)

Optional: Emotion marker (arrow, circle, emoji) — don't overuse.

### Big Bold Text

| Rule | Value |
|------|-------|
| Max words | **3-5** |
| Font weight | **Bold / Extra Bold** |
| Size | **Large enough to read on mobile** (70+ pt at 1280×720) |
| Contrast | **≥ 7:1** text vs background (WCAG AAA) |
| Outline / shadow | **1-3px stroke** for readability against busy background |
| Font family | Sans-serif (Inter, Montserrat, Bebas, Impact) |

Text should be readable at **120px wide** (mobile thumbnail). Test by scaling to 10%.

### Color

- High-contrast palette (complementary or split-complementary)
- Brand color + contrasting accent
- Avoid: muted / similar-value schemes
- YouTube popular: red / yellow / blue accents on dark BG

### Face Expression

Face with clear emotion (surprise, joy, curiosity, concern) → CTR boost of 20-40% vs neutral.

- Eyes looking at camera → direct engagement
- Eyes looking at product → directs viewer attention
- Open mouth / raised eyebrows = high energy
- Avoid deadpan neutral face

## Per-Platform Compositional Bias

| Platform | Style |
|----------|-------|
| YouTube | Face + big bold text + arrow / circle; high contrast; "MrBeast" style works |
| LinkedIn | Professional; product-first; minimal text; no "clickbait" |
| X | Short text + product screenshot; dark-mode-compatible |
| Product Hunt | Product-centric 1:1; tagline below hero |
| TikTok | Vertical face + text; trending aesthetic; no watermarks |
| Instagram | Cohesive grid-feed look; consistent brand palette |

A demo thumbnail for YouTube should not directly transplant to LinkedIn without restyling.

## A/B Test Variants

For high-stakes demos, produce 3-5 variants and A/B test. Axes:

| Axis | A variant | B variant |
|------|-----------|-----------|
| Face vs no face | Hero with face | Product-only |
| Text position | Top-left | Bottom-right |
| Emotion | Surprise | Calm + confident |
| Text wording | "See how it works" | "5 min to launch" |
| Background color | Light | Dark |
| Product prominence | Foreground | Faded / subtle |

YouTube Studio supports thumbnail A/B testing natively (since 2023-2024). Rotate every 48-72h, pick winner by CTR.

## File Optimization

```bash
# Optimize JPG (YouTube accepts up to 2MB; aim smaller)
cwebp -q 85 thumbnail.png -o thumbnail.webp    # webp, small
imageoptim thumbnail.jpg                        # JPG quality
oxipng -o 4 thumbnail.png                       # PNG

# Verify dimensions
magick identify thumbnail.jpg
```

Target ≤ 300KB for web OG-image (fast preview load), ≤ 2MB for YouTube.

## Mobile Preview Test

Thumbnail appears at ~180×100px on mobile YouTube feed. Test by scaling to 15%.

```
Desktop preview: 1280×720 (full)
Tablet:          640×360
Mobile feed:     180×100
Embed card:      120×68
```

If text is unreadable at 180×100 → enlarge font or reduce word count.

## Accessibility

- Text-background contrast ≥ 4.5:1 (WCAG AA) or 7:1 (AAA)
- Color-blind safe: don't rely on red/green contrast alone
- Avoid flashing / high-motion patterns (photosensitive epilepsy)
- Provide ALT text when embedded in articles / social cards

## Tools

| Tool | Use |
|------|-----|
| Figma | Vector design, template library |
| Photoshop | Raster + retouching |
| Canva | Quick templates, 1-person teams |
| Midjourney / DALL-E / Gemini | AI background / concept generation |
| TubeBuddy / VidIQ | YouTube A/B thumbnail testing |
| Thumbnail Preview extension | Browser preview at multiple sizes |

## Workflow

```
INPUT        →  demo video
             →  brand palette / font from Vision or Muse

PLATFORM     →  identify all target platforms + aspect ratios
             →  one master file → per-platform exports

CONCEPT      →  three-element audit: Face + Product + Text
             →  emotion + message alignment with scenario

COMPOSE      →  figma / photoshop template per platform
             →  safe area (text not at edge; YouTube duration pill)
             →  rule of thirds

TEXT         →  3-5 words, bold, 70+ pt
             →  WCAG contrast check

FACE         →  expressive, looking at camera or product
             →  color-graded to match palette

PRODUCT      →  clear UI screenshot, framed
             →  minimize UI chrome; focus on hero interaction

VARIANTS     →  3-5 A/B candidates
             →  different axes (emotion / text / composition)

MOBILE TEST  →  scale to 15% + preview
             →  text still readable, face still recognizable

OPTIMIZE     →  file size: ≤ 300KB OG, ≤ 2MB YouTube
             →  format: JPG default, PNG for flat graphics

DELIVER      →  per-platform PSD/AI source + exported JPG/PNG
             →  A/B candidates labeled for rotation

A/B TEST     →  YouTube Studio thumbnail test OR manual rotation
             →  rotate 48-72h per variant
             →  winner criteria: CTR ≥ 2x second-best

HANDOFF      →  growth: CTR tracking + A/B results
             →  director `voiceover` / `captions`: final bundle
             →  Builder: CDN upload + embed pipeline
             →  funnel: landing-page hero alignment
```

## Output Template

```markdown
## Thumbnail Plan: [Demo / Video]

### Master Inputs
- Video title: [string]
- Key message / hook: [one sentence]
- Brand palette: [primary + accent hex]
- Font: [family from Muse]
- Face asset: [photo / rendered / stock]
- Product visual: [UI screenshot / logo]

### Platform Exports
| Platform | Size | Variant count |
|----------|------|---------------|
| YouTube | 1280×720 | 3 A/B |
| LinkedIn | 1200×627 | 1 |
| X | 1600×900 | 1 |
| Product Hunt | 1200×1200 | 1 |
| OG image | 1200×630 | 1 |

### Design
- Composition: Rule of thirds with face at upper-right intersection
- Text: "5 min setup" (3 words, 90pt, Montserrat ExtraBold, white + black stroke)
- Background: Dark gradient #0A1E3F → #1E3A8A
- Face: Expressive, eyes at camera
- Product: UI screenshot, bottom-center, 40% opacity overlay

### A/B Variants
| Variant | Hook | Composition | Primary axis |
|---------|------|-------------|--------------|
| A | "5 min setup" | Face left, product right | Emotion |
| B | "Launch faster" | Product dominant, face small | Product-first |
| C | "Watch this demo" | Face centered, text bottom | Direct CTA |

### Mobile Preview Check
- [ ] Text readable at 15% scale
- [ ] Face recognizable
- [ ] Brand color visible
- [ ] Product frame identifiable

### File Budget
- YouTube: 1.2 MB JPG (under 2 MB limit)
- OG: 180 KB JPG (under 300 KB)
- All: sRGB color profile

### Accessibility
- Text contrast: [ratio] (AA / AAA)
- Color-blind safe: [yes / no]
- No flashing / high-motion

### Handoffs
- growth: CTR tracking
- director bundle: final package
- Builder: CDN upload
- funnel: landing-page hero alignment
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Reusing video frame as thumbnail | Custom design always |
| 10+ words in text overlay | Cap at 3-5; simplify |
| Text at image edge (cropped on preview) | Safe area 60px inset |
| Duration pill overlaps text | YouTube shows duration bottom-right; keep clear |
| Neutral face | Expressive emotion (surprise / joy / confidence) |
| Low contrast (gray on gray) | WCAG AA minimum; prefer AAA |
| Platform crop ignored (1:1 Product Hunt) | Per-platform export |
| No mobile preview test | Scale to 15% before declaring done |
| Misleading thumbnail (clickbait) | Honest; mismatch hurts retention |
| Photo without brand palette | Color-grade to match brand |
| Tiny product screenshot buried in corner | Either hero it or omit; half-measures confuse |
| Every video has identical template | Recognizable brand, but vary hooks |
| Dropping face because "unprofessional" | Face with confidence + professional palette works on LinkedIn |
| Red-green contrast only | Colorblind-safe palette |
| Skipping A/B test on high-stakes demos | Rotate 3 variants; pick CTR winner |
| File >2MB for YouTube | Upload rejected; compress |
| PNG for photo-heavy thumbnails | JPG is smaller; PNG for flat graphics |
| Source design not committed | Figma / PSD source in repo alongside exports |

## Deliverable Contract

When `thumbnail` completes, emit:

- **Master inputs** (title, hook, brand, face, product).
- **Platform exports matrix** (per-platform aspect + variants).
- **Design spec** (composition, text, colors, face, product placement).
- **A/B variants** with axes.
- **Mobile preview check**.
- **File budget** + format per platform.
- **Accessibility** (contrast, color-blind, photosensitivity).
- **Handoffs**: growth, director bundle, Builder, funnel.

## References

- YouTube Creator Academy thumbnail guidelines — creatoracademy.youtube.com
- YouTube Studio thumbnail A/B test — support.google.com/youtube/answer
- LinkedIn video post spec — linkedin.com/help/linkedin
- X Cards (Summary with Large Image) — developer.twitter.com/en/docs
- Product Hunt asset guide — producthunt.com/ship
- Open Graph protocol — ogp.me
- "5 Principles of Effective Thumbnail Design" — TubeBuddy blog
- "MrBeast's Thumbnail Strategy" — YouTube creator analysis
- *Typography Essentials* — Ina Saltz
- *Universal Principles of Design* — Lidwell, Holden, Butler
- WCAG 2.1 Success Criterion 1.4.3 Contrast — w3.org/TR/WCAG21
- Figma templates — figma.com/community (search "YouTube thumbnail")
- Canva Video Thumbnail gallery — canva.com
- TubeBuddy / VidIQ A/B tools — tubebuddy.com, vidiq.com
- "Eye Tracking and Web Design" — Nielsen Norman Group
- Color Contrast Checker — webaim.org/resources/contrastchecker
- Coolors / Adobe Color — palette generators
- Midjourney / DALL-E / Google Gemini — AI image generation (concept bg)
- "How Thumbnails Boost CTR" — YouTube Creator Insider research
- "Small Screen Legibility" — Apple HIG, Material Design guidelines
