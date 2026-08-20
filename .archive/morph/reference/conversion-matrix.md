# Conversion Matrix

Purpose: Use this reference when selecting the best tool for a source/target format pair and estimating likely fidelity loss.

## Contents

- Format-pair matrix
- Scenario-based defaults
- Known limitations
- Dependency checks
- Quick commands

## Format-Pair Matrix

### Markdown As Source

| Target | Preferred tool | Quality | Notes |
|--------|----------------|---------|-------|
| PDF (Japanese, high fidelity) | `pandoc + xelatex` | `★★★★★` | Best typography and font embedding |
| PDF (speed-first) | `pandoc + weasyprint` | `★★★★☆` | Modern CSS support, active maintenance |
| PDF (modern alternative) | `pandoc + typst` | `★★★★★` | Tagged PDF by default (Typst 0.14+), PDF/UA-1 native, fast compilation |
| Word (`.docx`) | `pandoc` | `★★★★☆` | Some style limits |
| HTML | `pandoc` | `★★★★★` | Native and reliable |
| Styled HTML | `pandoc + template/css` | `★★★★★` | Best for publication pages |
| EPUB | `pandoc` | `★★★★☆` | Good for ebook output |

### Word (`.docx`) As Source

| Target | Preferred tool | Quality | Notes |
|--------|----------------|---------|-------|
| PDF | `LibreOffice` | `★★★★★` | Best layout preservation |
| PDF (simple docs only) | `pandoc` | `★★★☆☆` | Use only for uncomplicated files |
| Markdown | `pandoc` | `★★★☆☆` | Complex formatting is lossy |
| HTML | `pandoc` | `★★★★☆` | Basic structure preserved |
| ODT | `LibreOffice` | `★★★★★` | Office-friendly |

### Excel (`.xlsx`) As Source

| Target | Preferred tool | Quality | Notes |
|--------|----------------|---------|-------|
| PDF | `LibreOffice` | `★★★★★` | Sheet-level export |
| CSV | `LibreOffice` | `★★★★★` | Best for raw data extraction |
| HTML | `LibreOffice` | `★★★★☆` | Table structure preserved |

### HTML As Source

| Target | Preferred tool | Quality | Notes |
|--------|----------------|---------|-------|
| PDF (modern CSS) | `Chrome/Puppeteer` | `★★★★★` | Best CSS support |
| PDF (CSS Paged Media) | `weasyprint` | `★★★★☆` | W3C CSS Paged Media, active maintenance |
| PDF (Paged.js) | `pagedjs-cli` | `★★★★☆` | W3C Paged Media polyfill |
| PDF (simple only) | `pandoc` | `★★★☆☆` | Avoid for rich HTML |
| Word (`.docx`) | `pandoc` | `★★★★☆` | Structure preserved |
| Markdown | `pandoc` | `★★★☆☆` | Lossy for complex HTML |

### Diagram Sources

| Source | Target | Preferred tool | Quality |
|--------|--------|----------------|---------|
| draw.io | PDF / PNG / SVG | `draw.io CLI` | `★★★★★` |
| Mermaid | PNG / PDF / SVG | `mermaid-cli` | `★★★★★` |

## Scenario Defaults

| Scenario | Default |
|---------|---------|
| Markdown -> PDF (Japanese business doc) | `pandoc + xelatex` or `pandoc + lualatex` with Japanese template |
| Markdown -> PDF (fast preview) | `pandoc + weasyprint` |
| Word -> PDF | `LibreOffice` |
| HTML -> PDF with modern layout | `Chrome/Puppeteer` |
| HTML -> PDF with CSS Paged Media | `weasyprint` |
| HTML -> PDF with Paged.js | `pagedjs-cli` |
| Batch conversion | `pandoc` scripts or Makefile |
| Accessible PDF (PDF/UA-1) | `pandoc + typst` (Typst 0.14+, Tagged PDF by default) or `pandoc + lualatex` |

## Known Limitations

| Pair | Main risk | Mitigation |
|------|-----------|------------|
| Markdown -> Word | Fine-grained styles and complex tables | Document loss and consider HTML fallback |
| Word -> Markdown | Complex tables and layout are lossy | Expect cleanup and review |
| HTML -> PDF via `wkhtmltopdf` | **Abandoned since 2023 (EOL)** — no security updates, Homebrew cask disabled Dec 2024 | Migrate to `weasyprint`, `Chrome/Puppeteer`, or `pagedjs-cli` |
| Any PDF structural conversion | PDF is not a rich source format | Treat PDF as output-first and use PDF-specific tools for PDF operations |

## Japanese Defaults

- Encoding: `UTF-8`
- Typical page size: `A4`
- Common fonts: `Hiragino`, `Noto Serif CJK JP`, `Noto Sans CJK JP`

## Dependency Checks

```sh
pandoc --version
pandoc --list-input-formats
pandoc --list-output-formats
which xelatex
xelatex --version
soffice --version
weasyprint --version
typst --version
```

## Quick Commands

```sh
# Markdown -> PDF (Japanese)
pandoc input.md -o output.pdf --pdf-engine=xelatex

# Word -> PDF
soffice --headless --convert-to pdf input.docx

# HTML -> PDF (weasyprint)
weasyprint input.html output.pdf

# draw.io -> PDF
/Applications/draw.io.app/Contents/MacOS/draw.io --export --format pdf input.drawio
```
