# Pandoc Recipes

Purpose: Use this reference when Pandoc is the chosen tool and you need canonical commands, templates, filters, metadata handling, or batch automation.

## Contents

- Core conversions
- PDF recipes
- Metadata and templates
- HTML and Word recipes
- Batch automation
- Filters and debugging

## Core Conversions

```sh
# Markdown -> PDF
pandoc input.md -o output.pdf

# Markdown -> PDF (Japanese)
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V CJKmainfont="Hiragino Mincho ProN"

# Markdown -> PDF with TOC
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --toc --toc-depth=3

# Markdown -> Word
pandoc input.md -o output.docx

# Markdown -> HTML
pandoc input.md -o output.html -s
```

## PDF Recipes

### Professional Document

```sh
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --toc \
  --metadata-file=metadata.yaml \
  --template=corporate-ja.tex
```

### Technical Document

```sh
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --template=technical-ja.tex \
  --highlight-style=tango
```

### Print-Optimized PDF

```sh
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V fontsize=12pt \
  -V geometry="margin=25mm"
```

## Metadata And Templates

```yaml
title: Document Title
author: Author Name
date: 2026-03-06
keywords:
  - conversion
  - report
lang: ja
```

```sh
# Apply metadata file
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --metadata-file=metadata.yaml

# Export default LaTeX template
pandoc -D latex > template.tex

# Apply custom template
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --template=template.tex
```

## HTML And Word Recipes

```sh
# HTML with CSS
pandoc input.md -o output.html -s --css=corporate.css

# DOCX with reference document
pandoc input.md -o output.docx --reference-doc=reference.docx

# DOCX with TOC
pandoc input.md -o output.docx --toc --reference-doc=reference.docx
```

## Batch Automation

```bash
#!/bin/bash
# convert-all.sh
OUTPUT_DIR="${2:-out}"
FORMAT="${3:-pdf}"
mkdir -p "$OUTPUT_DIR"
for file in "$1"/*.md; do
  filename=$(basename "$file" .md)
  pandoc "$file" -o "$OUTPUT_DIR/$filename.$FORMAT" --pdf-engine=xelatex
done
```

```make
SOURCES := $(wildcard *.md)
PDFS := $(SOURCES:.md=.pdf)
PANDOC_OPTS := --pdf-engine=xelatex --toc -V CJKmainfont="Hiragino Mincho ProN"

pdf: $(PDFS)

%.pdf: %.md
	pandoc $< -o $@ $(PANDOC_OPTS)
```

```sh
find . -name "*.md" | parallel pandoc {} -o {.}.pdf
```

## Defaults Files (Pandoc 3.9+)

Pandoc defaults files (YAML or JSON) centralize all conversion options. Variable interpolation now works in the `defaults` field, so defaults files can extend each other.

```yaml
# defaults/pdf-ja.yaml
from: markdown
to: pdf
pdf-engine: xelatex
toc: true
toc-depth: 3
metadata-file: metadata.yaml
template: corporate-ja.tex
variables:
  CJKmainfont: "Hiragino Mincho ProN"
  geometry: "margin=25mm"
  fontsize: 12pt
```

```sh
# Apply defaults file
pandoc input.md -d defaults/pdf-ja.yaml -o output.pdf
```

Defaults files that extend others (variable interpolation, Pandoc 3.9+):

```yaml
# defaults/pdf-print.yaml
defaults: pdf-ja.yaml   # extends base defaults
variables:
  geometry: "margin=15mm"
```

Source: https://pandoc.org/MANUAL.html#defaults-files

## Pandoc 3.9 WASM

Pandoc 3.9 (February 2026) compiles to WebAssembly. A full browser GUI is available at https://pandoc.org/app (includes Typst-based PDF output). Lua filters work in WASM; JSON filters do not. Use this for client-side conversion pipelines or prototyping without local Pandoc install.

Source: https://github.com/jgm/pandoc/discussions/11439

## Filters And Debugging

```sh
# Citation processing
pandoc input.md -o output.pdf --citeproc --bibliography=refs.bib

# Lua filter (preferred over JSON filters — runs in embedded interpreter, no external deps)
pandoc input.md -o output.pdf --lua-filter=uppercase-headers.lua

# Inspect intermediate LaTeX
pandoc input.md -t latex -o debug.tex

# Resource path
pandoc input.md -o output.pdf --resource-path=.:images:assets
```

Rules:

- Use `pandoc` when the source is structurally clean and the target pair is supported.
- Prefer template and metadata files over long inline flag chains when the workflow will recur.
- For large documents or frequent builds, script or make the conversion instead of repeating ad hoc commands.
- Use Lua filters over JSON filters — they run in Pandoc's embedded Lua interpreter with no external dependencies.
- For speed-first PDF from Markdown, use `pandoc + weasyprint`; do NOT use `wkhtmltopdf` (EOL since 2023).
- For Tagged PDF / PDF/UA-1 output, use `pandoc + typst` (Typst 0.14+ emits tagged PDF by default). Source: https://typst.app/blog/2025/typst-0.14/
