# EPUB Generation Reference

Purpose: Generate production-quality EPUB 3.x files with proper structure, navigation, accessibility, and downstream Kindle (KF8/MOBI) compatibility. Cover Pandoc, EPUBCheck, Calibre `ebook-convert`, EPUB Accessibility 1.1, and reflowable vs fixed-layout selection.

## Scope Boundary

- **morph `epub`**: EPUB / KF8 / MOBI generation (this document).
- **morph `pdf` (elsewhere)**: Print-oriented PDF.
- **morph `html` (elsewhere)**: Web-oriented HTML.
- **Builder (elsewhere)**: Custom EPUB authoring tooling.
- **polyglot (elsewhere)**: Multi-language locale handling beyond EPUB.

## EPUB 3.x Structure

```
book.epub (ZIP container)
├── mimetype                       # MUST be first, MUST be uncompressed: application/epub+zip
├── META-INF/
│   └── container.xml              # points to OPF
├── OEBPS/
│   ├── content.opf                # package metadata + manifest + spine
│   ├── nav.xhtml                  # EPUB 3 navigation (replaces toc.ncx)
│   ├── toc.ncx                    # legacy NCX (EPUB 2 fallback)
│   ├── chapter01.xhtml
│   ├── chapter02.xhtml
│   └── styles/main.css
```

EPUB 3.3 (W3C 2023 Recommendation) is current. Major readers: Apple Books, Google Play Books, Kobo, Calibre, Adobe Digital Editions, Thorium.

## Reflowable vs Fixed-Layout

| Type | Use case | Notes |
|------|----------|-------|
| Reflowable | Novels, technical books, long-form text | User controls font / size; default choice |
| Fixed-layout | Picture books, manga, design-heavy | Pre-paginated; ZIP per spread; supports `rendition:layout pre-paginated` |

Default reflowable. Fixed-layout only when typography pixel-perfectness matters.

## Pandoc Workflow

```bash
pandoc book.md \
  -o book.epub \
  --metadata-file=metadata.yml \
  --css=styles/main.css \
  --epub-cover-image=cover.png \
  --toc --toc-depth=2 \
  --epub-chapter-level=1 \
  --epub-embed-font='fonts/NotoSerifJP-*.otf' \
  --resource-path=.:assets \
  --split-level=1
```

`metadata.yml`:
```yaml
title: My Book
creator:
  - role: author
    text: Jane Doe
publisher: Example Press
language: en-US
identifier:
  - scheme: ISBN
    text: 978-0-00000-000-0
date: 2026-04-25
rights: © 2026 Jane Doe
description: Long-form description.
subject:
  - Software Engineering
  - Testing
```

## Manual Manifest Patterns (when not using Pandoc)

```xml
<package version="3.0" xmlns="http://www.idpf.org/2007/opf"
         unique-identifier="bookid" xml:lang="en">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">urn:uuid:...</dc:identifier>
    <dc:title>My Book</dc:title>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-04-25T00:00:00Z</meta>
    <meta property="schema:accessMode">textual,visual</meta>
    <meta property="schema:accessibilityFeature">structuralNavigation,readingOrder,alternativeText</meta>
    <meta property="schema:accessibilityHazard">none</meta>
    <meta property="schema:accessibilitySummary">Heading-structured EPUB with alt text on images.</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="cover" href="cover.png" media-type="image/png" properties="cover-image"/>
    <item id="ch1" href="chapter01.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref="ch1"/>
  </spine>
</package>
```

## EPUB Accessibility 1.1 (W3C 2025)

Required `schema:*` properties:
- `schema:accessMode` — textual / visual / auditory
- `schema:accessibilityFeature` — structuralNavigation / readingOrder / alternativeText / MathML / longDescription / printPageNumbers
- `schema:accessibilityHazard` — none / flashing / motionSimulation
- `schema:accessibilitySummary` — human description

XHTML practice:
- Semantic headings `<h1>`-`<h6>` ordered.
- `<nav epub:type="toc">` for navigation.
- `<img alt="...">` for every image (empty `alt=""` for decorative).
- Tables with `<caption>`, `<thead>`, `<th scope="...">`.
- `<aside epub:type="footnote">` for footnotes.

## Validation

```bash
# Required: pass EPUBCheck (W3C-maintained)
java -jar epubcheck.jar book.epub

# Optional: Ace by DAISY (accessibility audit)
ace book.epub --outdir reports/

# Optional: pagedjs / Thorium for visual review
```

EPUBCheck must exit 0 with no errors. Warnings should be triaged.

## KF8 / MOBI for Kindle

Modern Kindle uses KF8 (essentially EPUB 3 in Amazon's container) or KFX. Conversion via Calibre:

```bash
ebook-convert book.epub book.azw3   # KF8 / AZW3
ebook-convert book.epub book.mobi   # legacy MOBI (older Kindles)
```

Or use Amazon's Kindle Previewer / KindleGen (deprecated; use Kindle Create / KDP upload pipeline).

Notes:
- Amazon prefers EPUB upload via KDP (auto-converts).
- KF8 supports CSS3 subset; some pseudo-elements unsupported.
- Embedded fonts allowed but limit to 5MB per font for size.

## CSS for Reflowable

```css
@namespace epub "http://www.idpf.org/2007/ops";
body { font-family: serif; line-height: 1.6; }
h1 { page-break-before: always; }
h2 { page-break-after: avoid; }
img { max-width: 100%; height: auto; }
.no-break { page-break-inside: avoid; }
a[epub|type~="footnote"] { vertical-align: super; font-size: smaller; }
```

Reader-respect: don't fix font-size in absolute pixels; use `em` / `rem`. Don't disable user-zoom.

## Fixed-Layout Patterns

```xml
<metadata>
  <meta property="rendition:layout">pre-paginated</meta>
  <meta property="rendition:orientation">portrait</meta>
  <meta property="rendition:spread">none</meta>
</metadata>
```

Each XHTML page sized to viewport:
```html
<head>
  <meta name="viewport" content="width=1200, height=1800"/>
</head>
```

## Multilingual / CJK / RTL

- `xml:lang="ja"` on `<html>` for Japanese.
- Vertical writing: `writing-mode: vertical-rl;`
- Embed CJK fonts (NotoSerifJP, NotoSansJP) — readers don't ship them all.
- RTL: `dir="rtl"` + `writing-mode: horizontal-tb` (default for Arabic / Hebrew).

## Workflow

```
SOURCE      →  Markdown / DOCX / HTML / structured AsciiDoc

METADATA    →  identifier (UUID/ISBN), title, creator, language, modified date
            →  accessibility metadata (schema:*)
            →  cover image at 1.6:1 aspect; ≥1600×2560 for retina

CONVERT     →  Pandoc default for most cases
            →  manual OPF for fine control / fixed-layout

CSS         →  reflowable: relative units, page-break hints
            →  fixed-layout: per-page viewport

NAV         →  nav.xhtml with epub:type="toc" + landmarks + page-list
            →  toc.ncx for legacy fallback

A11Y        →  alt text mandatory for non-decorative images
            →  schema:accessibilityFeature populated
            →  EPUBCheck + Ace audit

VALIDATE    →  EPUBCheck pass (errors blocking; warnings triaged)
            →  Test on Apple Books, Kobo, Calibre, Thorium
            →  visual sanity on actual hardware (Kindle, Kobo)

KINDLE      →  Calibre ebook-convert → AZW3 / MOBI
            →  or upload EPUB to KDP

DELIVER     →  ZIP integrity check
            →  filename: title-author-year.epub
            →  checksum for distribution

HANDOFF     →  Builder: custom tooling for batch
            →  Cloak: PII in metadata before publishing
            →  Voice: marketing description
```

## Output Template

```markdown
## EPUB Package: [Title]

### Format Decision
- Layout: [reflowable / fixed-layout] — rationale: [...]
- Source: [Markdown / DOCX / HTML / mixed]

### Metadata
- Identifier: [UUID / ISBN]
- Language: [en-US / ja / ar]
- Accessibility: [schema:accessibilityFeature list]
- Hazards: [none / flashing / ...]

### Tooling
- Primary: pandoc
- Conversion command: [full command line]
- Config files: metadata.yml, css, embedded fonts

### Validation Results
- EPUBCheck: [PASS / N errors / N warnings]
- Ace by DAISY: [score]
- Reader testing: [Apple Books / Kobo / Thorium / Kindle]

### Kindle Variant
- AZW3 via Calibre: [generated / N/A]
- KDP upload tested: [yes/no]

### Deliverables
- book.epub (validated)
- book.azw3 (Kindle, if applicable)
- accessibility-report.html

### Handoffs
- Builder: tooling for repeat builds
- Cloak: scrub PII from EPUB metadata
- Voice: marketing copy
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Fixed-pixel font sizes | Use `em`/`rem`; respect reader settings |
| Embedded raster fonts when SVG/woff2 sufficient | Use woff2 with FontFace + license check |
| `mimetype` compressed inside ZIP | MUST be uncompressed and first entry |
| No `nav.xhtml` (EPUB 2 only with NCX) | EPUB 3 requires nav.xhtml; NCX is fallback |
| Missing `alt` on decorative images | Use `alt=""` (empty) to mark decorative |
| Cover image too small | ≥1600×2560 for retina readers |
| Skipping EPUBCheck | Mandatory; reader rejection follows otherwise |
| Forgetting `schema:accessibilityFeature` | EPUB Accessibility 1.1 conformance fails |
| External resource references (http://...) | Embed all assets; readers may be offline |
| Unescaped HTML entities in XHTML | XHTML is strict XML; well-formedness mandatory |
| Lossy conversion to MOBI ignoring CSS | Test on Kindle hardware; some CSS silently dropped |
| RTL without `dir="rtl"` | Apply at `<html>` and per-paragraph as needed |
| Non-unique identifiers across versions | URN-form UUID; same edition, same UUID |
| Cover not flagged with `properties="cover-image"` | Storefront thumbnails fail otherwise |

## Deliverable Contract

When `epub` completes, emit:

- **Format choice** (reflowable / fixed-layout) with rationale.
- **Conversion command** (pandoc or manual OPF).
- **Metadata file** with accessibility schema.
- **EPUBCheck report** (errors blocking, warnings triaged).
- **Accessibility audit** (Ace by DAISY).
- **Kindle variant** if requested.
- **Reader testing matrix** results.
- **Handoffs**: Builder, Cloak, Voice.

## References

- W3C EPUB 3.3 — w3.org/TR/epub-33/ (2023 Recommendation)
- W3C EPUB Accessibility 1.1 — w3.org/TR/epub-a11y-11/ (2025)
- EPUBCheck — github.com/w3c/epubcheck
- Ace by DAISY — daisy.org/activities/software/ace/
- Pandoc EPUB writer — pandoc.org/MANUAL.html#epub-metadata
- Calibre `ebook-convert` — manual.calibre-ebook.com
- Amazon KDP — kdp.amazon.com (Kindle publishing)
- Apple Books Asset Guide — itunespartner.apple.com
- Kobo Writing Life — kobowritinglife.com
- Thorium Reader — thorium.edrlab.org (testing reader)
- DAISY Consortium — daisy.org (accessibility resource)
- Schema.org accessibility properties — schema.org/docs/accessibility-properties
