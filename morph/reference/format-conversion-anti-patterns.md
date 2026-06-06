# Format Conversion Anti-Patterns

Purpose: Use this reference when the main risk is wrong tool choice, hidden loss, unsupported source features, or false assumptions about conversion fidelity.

## Contents

- Anti-pattern catalog
- LaTeX and Markdown pitfalls
- PDF engine selection
- Morph review checklist

## Anti-Pattern Catalog

| ID | Anti-pattern | Signal | Correction |
|----|--------------|--------|-----------|
| `FC-01` | Treating PDF as a normal source format | Structural recovery is poor | Treat PDF as output-first; use PDF-specific ops only |
| `FC-02` | Trusting the intermediate representation too much | Complex layout disappears | Document incompatible elements before conversion |
| `FC-03` | Tool mismatch | Wrong tool for the format pair | Follow the conversion matrix |
| `FC-04` | Hidden dependencies | Missing fonts, engines, or packages | Verify dependencies before conversion |
| `FC-05` | Skipping verification | Broken output ships | Run VERIFY for structure, visual, content, and metadata |
| `FC-06` | Assuming lossless conversion | Structural/styling loss ignored | Declare lossy vs lossless expectations explicitly |
| `FC-07` | Single-tool absolutism | Everything is forced through one tool | Choose per format pair |

## LaTeX And Markdown Pitfalls

- Bibliography often needs explicit `--citeproc --bibliography=refs.bib`.
- Complex figures and tables may need pre-cleanup.
- Some LaTeX macros and numbering conventions will not survive direct conversion.
- Markdown cannot express every layout detail; template or HTML assist may be necessary.

## PDF Engine Selection

| Engine | Strength | Risk | Use it for |
|--------|----------|------|------------|
| `xelatex` / `lualatex` | High-quality typesetting | heavier dependencies | Japanese or structured PDFs |
| `Chrome/Puppeteer` | Best modern CSS support | limited paged-media features vs dedicated tools | HTML-driven PDFs |
| `wkhtmltopdf` | Fast and lightweight | limited modern CSS | simple HTML PDFs |
| `LibreOffice` | Layout fidelity for Office docs | less scriptable than Pandoc-only flow | Word/Excel to PDF |
| `Prince` / `WeasyPrint` | Better paged-media control | licensing/support trade-offs | print-grade HTML PDFs |

## Morph Review Checklist

- `FC-01`: reject PDF as a structural source conversion unless the task is PDF-native.
- `FC-03`: confirm the selected tool matches the format pair.
- `FC-04`: check fonts, engines, and packages before conversion.
- `FC-05`: never skip verification.
- `FC-06`: state expected feature loss before delivery.
