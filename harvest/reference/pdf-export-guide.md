# PDF Export Guide

Purpose: Use this reference when Harvest must turn Markdown or HTML reports into stable PDF output without changing the report content.

## Contents

- Preferred export paths
- Repo scripts and assets
- Tool selection
- Mermaid handling
- Troubleshooting

## Preferred Export Paths

Use this order unless the request explicitly requires another tool:

| Priority | Path | Use when |
|----------|------|----------|
| 1 | `scripts/html-to-pdf.sh` | You already have HTML output and want the most robust repo-native path |
| 2 | `node scripts/puppeteer-pdf.js input.html output.pdf` | You have Node/Puppeteer available and need HTML -> PDF |
| 3 | `md-to-pdf` | You only have Markdown and need a fast direct export |
| 4 | `pandoc` | You need higher-quality typesetting or LaTeX-based control |
| 5 | `marp --pdf` (Marp CLI) | Slide-shaped report from Markdown front-matter (`marp.app`) |
| 6 | ASCII + browser print | Mermaid or CSS compatibility is poor and a safe fallback is needed |

Pandoc 3.x notes (`pandoc.org/releases.html`):
- 3.8.3 added `asciidoc`, `pptx`, `xlsx` as input formats and `bbcode` as output.
- 3.9 added WASM-targeted builds for in-browser conversion.
- `--pdf-engine` accepts `groff`, `lualatex`, `xelatex`, `wkhtmltopdf`, `weasyprint`, `typst`. For Japanese reports, `lualatex` or `xelatex` with system CJK fonts remains the most reliable path; `typst` is a fast modern alternative when LaTeX is unavailable.

## Repo Scripts And Assets

| Asset | Role |
|------|------|
| `scripts/html-to-pdf.sh` | A4 HTML -> PDF conversion with method selection and validation |
| `scripts/puppeteer-pdf.js` | Puppeteer fallback for HTML -> PDF |
| `styles/harvest-style.css` | Report styling for PDF-friendly layout |
| `templates/client-report.html` | HTML shell for client reports |

## Tool Selection

### HTML -> PDF

```bash
./scripts/html-to-pdf.sh client-report-YYYY-MM-DD.html
./scripts/html-to-pdf.sh --method chrome client-report-YYYY-MM-DD.html output.pdf
```

Notes:
- Default timeout is `60s`.
- Supported methods: `chrome`, `wkhtmltopdf`, `puppeteer`.
- The script validates file existence, minimum size, and PDF magic number.

### Direct Markdown -> PDF

```bash
md-to-pdf client-report-YYYY-MM-DD.md --stylesheet styles/harvest-style.css
```

### Pandoc

```bash
pandoc client-report-YYYY-MM-DD.md -o report.pdf \
  --pdf-engine=lualatex \
  -V geometry:margin=20mm
```

## Mermaid Handling

Use one of these strategies:

| Strategy | Use when |
|----------|----------|
| Native rendering | `md-to-pdf` or browser-based export can execute Mermaid safely |
| Pre-render to SVG | You need deterministic PDF output |
| ASCII fallback | Rendering is unstable or PDF portability matters more than visual richness |

ASCII fallback is the safest default for client-facing PDF reports.

## Troubleshooting

| Problem | Action |
|--------|--------|
| Japanese text is garbled | Use system Japanese fonts and the repo stylesheet |
| Mermaid does not render | Pre-render diagrams or switch to ASCII |
| Output file is too small | Treat as failed export and retry with another method |
| Output is not a valid PDF | Fail the export; do not claim success |
| CSS layout breaks across pages | Prefer HTML template + stylesheet + Chrome/Puppeteer path |
