# Logo Construction

## Purpose

A logo is the most demanding SVG asset: it carries brand identity, must work at every size from favicon to billboard, must survive monochrome reproduction, and must respect type licenses. This reference covers logo classification, typographic construction, clear-space and minimum-size rules, and the canonical delivery package.

## Scope Boundary

- IN scope: logo classification, wordmark / monogram / lockup construction, type-license verification, clear-space and min-size, monochrome / single-color variants, social-card / favicon / Open Graph variants, file-format delivery package.
- OUT of scope: full brand identity / system (delegate to `vision`), illustrative mascots (`illustration`), pictograms (`pictogram`), animation (`animate`), color theming details (`theme`), printed materials beyond logo specs (delegate to print partner).

## Core Concepts

### Logo Classification

| Class | Definition | Example |
|-------|-----------|---------|
| Wordmark / Logotype | Stylized typography of the full name | Google, Coca-Cola, FedEx |
| Lettermark / Monogram | 1–4 letter abbreviation | IBM, HBO, NASA |
| Brandmark / Symbol | Abstract or pictorial mark only | Apple, Twitter (bird), Nike (swoosh) |
| Combination | Wordmark + symbol | Adidas, Lacoste, Burger King |
| Lockup | Specific arrangement of marks | logo + tagline; logo + sub-brand |
| Emblem | Mark within a containing shape | Starbucks (siren in circle), NFL teams |
| Dynamic / responsive | Variants for context | MIT Media Lab, AOL |

Pick class based on: name length, market crowding, scalability requirement, brand stage.

### Typographic Construction

For wordmarks / monograms, type choice is the logo:

| Step | Decision |
|------|----------|
| Typeface license | Verify desktop / web / logo / commercial use covered |
| Custom vs licensed | Custom > licensed for permanent identity (no future license risk) |
| Outlines vs live | Outline (convert to paths) for delivery; keep editable source |
| Kerning | Manual kerning per pair; auto-kerning never sufficient for logo |
| Letter spacing | Optical, not metric |
| Baseline | Custom baseline rules per glyph |
| Ligatures | Custom for hero pairs (often 'tt', 'fi', 'ee') |
| Apertures | Tighten / open per legibility test |
| Diacritics | Verify support if international |

Common license traps (verify current EULAs as of 2026-05):

- Many free fonts (Google Fonts / OFL, etc.) actually **permit** logo use under OFL — but the OFL **prohibits selling the font itself**. Verify the specific font's RFN (Reserved Font Name) clause. Some Google Fonts ship under Apache 2.0 (no logo restriction).
- Adobe Fonts: not licensed for logo / trademark use even on commercial subscriptions; explicit prohibition in current EULA.
- MyFonts / Fontspring / Monotype: read the EULA — desktop license covers some uses, "extended" or "logo" license required for trademark filing.
- Custom commission: ~$5K–$50K but resolves licensing forever; AI-typeface tools (e.g., Monotype Font Studio) blur authorship/licensing — confirm explicit grant of rights for trademark use.

### The Logo Grid

Build the logo on a grid — usually proportional to a baseline element (capital height, x-height, or symbol size).

| Grid | Use |
|------|-----|
| Capital-height grid | Wordmarks; relate every dimension to cap height |
| Square grid | Monograms; n × n geometry |
| Golden-ratio | Display logos with spatial harmony |
| Custom / radial | Emblems with rotational symmetry |

The grid is the logo's skeleton; without it, scaling and reproduction drift.

### Clear-Space Rule

Every logo needs a **clear-space margin** — space around the mark where no other element can encroach.

| Method | Example |
|--------|---------|
| Cap-height multiple | "Clear space = 0.5 × cap height" |
| Symbol-width multiple | "Clear space = 1 × symbol width" |
| Brand grid unit | "Clear space = 2 grid units" |

Document in the style guide with a visual diagram. Clear-space violations are the #1 brand misuse.

### Minimum Size

Every logo has a **minimum reproducible size** below which it should never appear.

| Variant | Minimum |
|---------|---------|
| Full color logo | 24 px digital / 1 cm print |
| Monochrome | 16 px digital / 0.5 cm print |
| Favicon | 16 px or 32 px (special simplified variant if needed) |
| App icon | 1024 × 1024 px master, 16 px minimum render |

Below minimum, design a **reduced variant** (often the symbol-only, mono, or simplified version).

### Color Variants

A logo needs at least 5 color variants:

| Variant | Use |
|---------|-----|
| Primary (full color) | Brand-default applications |
| Single-color (brand color) | Print constraints, embossed |
| Mono black | Newspaper, print-on-demand, fax |
| Mono white | Dark backgrounds, photo overlays |
| Knock-out | Reversed for embossing / die-cut |

Verify each at minimum size. Single-color often requires re-design (gradients flatten, multi-color symbols collapse).

### Lockups

Often a logo has multiple official lockups:

| Lockup | Use |
|--------|-----|
| Horizontal (symbol left, wordmark right) | Header, sponsorship banner |
| Stacked (symbol top, wordmark bottom) | Square spaces, social avatar adjacent |
| Symbol-only | Favicon, app icon, profile circle |
| Wordmark-only | Hero typography, business card |
| With tagline | Marketing materials |
| Sub-brand lockup | Product / division extension |

Spec each: alignment, gap, kerning relationship, official scale ratio.

### Asset Delivery Package

A complete logo package:

| File | Purpose |
|------|---------|
| `logo.svg` | Master vector |
| `logo-mono-black.svg` | Single-color black |
| `logo-mono-white.svg` | Single-color white |
| `logo-dark.svg` | Optimized for dark backgrounds |
| `logo@1x.png`, `@2x.png`, `@3x.png` | Raster fallbacks |
| `favicon.svg`, `favicon-16.png`, `favicon-32.png`, `favicon-192.png` | Browser tab |
| `apple-touch-icon-180.png` | iOS home screen |
| `og-image.png` (1200×630) | Open Graph / social cards |
| `twitter-card.png` (1200×600) | X / Twitter |
| `app-icon-1024.png` | iOS / Android master |
| `style-guide.pdf` or `brand.html` | Usage rules |

For business documents: also `.eps` (print partner), `.ai` (designer source), `.pdf` (vector reference).

### Favicon Strategy (2026)

Modern favicon best practices:

```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="icon" href="/favicon-32.png" sizes="32x32" />
<link rel="apple-touch-icon" href="/apple-touch-icon-180.png" />
<link rel="manifest" href="/site.webmanifest" />
```

SVG favicon is the modern default — supported in Chrome 80+ / Firefox 41+ / Safari 16.4+ (2023-03). PNG fallbacks for older browsers and email clients. Modern SVG favicons can use `prefers-color-scheme` inside `<style>` so a single file adapts to light/dark browser chrome.

### Type Outlining

For SVG delivery: convert all type to outlines (paths). Why:

- Recipient doesn't need the typeface installed.
- License compliance (typeface bytes not redistributed).
- Rendering identical across systems.

Keep an editable source file (Illustrator / Figma) with live type for future modifications. Never deliver a logo as live type unless the recipient has signed a font license.

### Trademark Considerations

Once a logo is used commercially:

| Concern | Action |
|---------|--------|
| Registration eligibility | Distinctive enough? Not generic? Search USPTO / JPO / EUIPO. |
| Type license | Confirm logo-use coverage in font EULA (not just desktop / web). |
| Color trademark | Possible but rare (UPS brown, Tiffany blue). |
| Sound mark / motion | Separate filings if used. |
| ™ vs ® | Use ™ before registration; ® only after granted. |
| Renewal | 10-year cycles in most jurisdictions. |

For commercially serious logos, engage a trademark attorney before public launch.

### Versioning

Logos evolve. Version each major change:

| Version | When |
|---------|------|
| v1.0 | Original launch |
| v1.1 | Minor refinement (kerning fix) |
| v2.0 | Major redesign |

Archive prior versions; document the change rationale; coordinate cross-platform rollout to avoid legacy logos surviving in some channels.

### Brand Style Guide Section

The logo section of a brand style guide includes:

1. Logo classification / family overview.
2. Each variant with file links.
3. Clear-space rule with visual.
4. Minimum size rule with visual.
5. Color rules (primary, mono, prohibited variants).
6. 8-10 do / don't examples.
7. Co-branding rules.
8. Where to download.

Without a style guide, the logo is misused within 6 months of release.

## Workflow

1. **Choose class** — wordmark / monogram / brandmark / combination / lockup / emblem.
2. **Verify type license** — covers logo / trademark use; or commission custom.
3. **Set the grid** — cap-height / square / golden-ratio.
4. **Design master** — single canonical version, full vector.
5. **Outline type** — convert live type to paths.
6. **Build clear-space + min-size rules** with visual diagrams.
7. **Generate color variants** — primary / mono black / mono white / knock-out.
8. **Build lockups** — horizontal / stacked / symbol-only / with-tagline.
9. **Test at scale extremes** — favicon (16 px) + billboard (1m+).
10. **Deliver package** — SVG / PNG @1×@2×@3× / favicon set / OG / app icon.
11. **Author style guide** — usage rules, do / don't.
12. **(Optional) trademark filing** — engage attorney before public launch.
13. **Set version cadence** — refinement plan; archive prior versions.

## Output Template

```yaml
logo_construction:
  brand: "Aether Inc."
  class: combination
  symbol: abstract_shield
  wordmark:
    typeface: "Custom commission, based on Söhne Breit"
    license: custom_commercial_perpetual
    type_outlined: yes
  grid: cap_height_grid
  clear_space:
    rule: "0.5 × cap height on all sides"
    diagram_in_style_guide: yes
  minimum_size:
    full_color_digital_px: 24
    full_color_print_cm: 1.0
    monochrome_digital_px: 16
    monochrome_print_cm: 0.5
  variants:
    - primary_full_color
    - mono_black
    - mono_white
    - knock_out
    - dark_background_optimized
  lockups:
    - horizontal: symbol_left_wordmark_right
    - stacked: symbol_top_wordmark_bottom
    - symbol_only: favicon_app_icon
    - wordmark_only: hero_typography
    - with_tagline: marketing_materials
  delivery_package:
    svg: [logo, mono-black, mono-white, dark]
    png_dpi: [1x, 2x, 3x]
    favicon: [svg, 16, 32, 192, 512]
    apple_touch_icon: 180
    og_image: 1200x630
    twitter_card: 1200x600
    app_icon: 1024
    eps_for_print: yes
    ai_source: yes
  trademark:
    filing_planned: yes
    jurisdictions: [us, jp, eu]
    attorney_engaged: yes
  style_guide:
    do_dont_examples: 10
    clear_space_visual: yes
    co_branding_rules: yes
  version: v1.0
  versioning_cadence: review_quarterly
```

## Anti-Patterns

- Using an unlicensed font for logo work — IP risk.
- Live type instead of outlined paths — reproduction breaks.
- No clear-space rule — logo crammed in branded media.
- No minimum size rule — illegible favicons / business cards.
- One color variant only — fails mono print contexts.
- Multi-color symbol that doesn't survive monochrome reduction.
- No favicon — unprofessional in browser tabs.
- Favicon as scaled-down full logo — illegible at 16 px.
- No OG / social card variant — broken social previews.
- App icon designed at small size — fails at 1024 px master.
- Identical lockup spacing across platforms — feels off in some contexts.
- No style guide — logo misused immediately.
- Co-branding rules undocumented — partnerships create logo Frankensteins.
- Using ® before trademark grant — false claim risk.
- No archive of prior versions — lost provenance.
- Logo file delivered as raster PNG only — print partners can't scale.
- Gradient logo without flat fallback — breaks in single-color contexts.
- Drop-shadow logo — flattens awkwardly; vendors interpret differently.
- Using a stock symbol from icon library as logo — attribution / uniqueness risk.
- Tagline locked to logo — can't update tagline without re-doing logo.
- Logo design done by AI without human verification + license clearance — current AI image tools don't guarantee uniqueness or rights.

## Deliverable Contract

A logo construction package is complete when:

- Class chosen and rationale documented.
- Type license covers logo / trademark use.
- Grid system documented.
- Master vector with type outlined.
- Clear-space + min-size rules with diagrams.
- 5+ color variants delivered.
- All required lockups built.
- Tested at scale extremes (16 px and large).
- Full delivery package generated (SVG / PNG / favicon / OG / app icon / EPS / AI).
- Style guide section authored with do / don't examples.
- (Commercial) trademark filing plan + attorney engaged.
- Version + cadence documented.

## References

- Paul Rand, *Thoughts on Design* (1947) — foundational logo principles.
- Saul Bass — corporate identity classics (AT&T, Bell, Continental Airlines).
- Sagi Haviv (Chermayeff & Geismar & Haviv), *Identify* (2011) — logo design methodology.
- Aaron Draplin, *Pretty Much Everything* (2016) — independent designer logo workflow.
- Rob Janoff (designer of Apple logo) — interviews on simplicity.
- Lance Wyman — Mexico City 1968 Olympics + Mexico Metro pictograms / wordmarks.
- Massimo Vignelli — corporate-identity foundational work.
- USPTO Trademark Manual of Examining Procedure (TMEP) — registration guide.
- WIPO Madrid Protocol — international trademark filing.
- Adobe Fonts EULA / Google Fonts License (OFL) / MyFonts EULA — license-comparison reference.
- Brand New (Under Consideration) — UnderConsideration.com — modern logo redesign analysis.
- Logoed (Bill Gardner) — annual showcase.
- The Logo Pond / Logo Lounge annual books — current trends.
- Material Design / Apple HIG / Microsoft Fluent — favicon and app-icon platform standards.
- W3C web app manifest spec — PWA icon delivery.
- favicon.io / RealFaviconGenerator — practical favicon generation.
