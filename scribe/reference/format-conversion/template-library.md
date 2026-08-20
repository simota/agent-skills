# Template Library

Purpose: Use this reference when selecting or applying LaTeX, CSS, or Word reference templates for conversion output.

## Contents

- Template overview
- LaTeX templates
- CSS templates
- Word reference docs
- Variables
- Selection guide

## Template Overview

| Template | Best fit | Engine / target |
|---------|----------|-----------------|
| `corporate-ja.tex` | Business proposals, stakeholder docs | `lualatex` |
| `technical-ja.tex` | Technical specs, API docs | `lualatex` or `xelatex` |
| `report-ja.tex` | Project and status reports | `lualatex` |
| `minimal.tex` | Quick or low-style conversions | `xelatex` |
| `corporate.css` | Business HTML export | HTML |
| `technical.css` | Code-heavy HTML export | HTML |
| `print.css` | Printed HTML | HTML |
| `reference.docx` | Word styling baseline | DOCX |

## LaTeX Templates

```sh
pandoc input.md -o output.pdf --template=corporate-ja.tex --pdf-engine=lualatex
pandoc input.md -o output.pdf --template=technical-ja.tex --pdf-engine=lualatex
pandoc input.md -o output.pdf --template=report-ja.tex --pdf-engine=lualatex
pandoc input.md -o output.pdf --template=minimal.tex --pdf-engine=xelatex
```

## CSS Templates

```sh
pandoc input.md -o output.html -s --css=corporate.css
pandoc input.md -o output.html -s --css=technical.css
pandoc input.md -o output.html -s --css=print.css
```

Default print assumptions:

- `@charset "UTF-8";`
- `A4`
- print-safe margins

## Word Reference Documents

```sh
# Create default reference document
pandoc -o reference.docx --print-default-data-file reference.docx

# Apply reference document
pandoc input.md -o output.docx --reference-doc=reference.docx
```

Rules:

- Use reference docs for style mapping instead of manual post-editing when the workflow will repeat.

## Template Variables

Common variables:

- `title`
- `author`
- `date`
- `lang`
- `keywords`
- `geometry`

Example:

```yaml
title: Document Title
author: Author Name
date: 2026-03-06
lang: ja
keywords:
  - report
  - conversion
```

## Selection Guide

| Situation | Default |
|----------|---------|
| Formal Japanese business PDF | `corporate-ja.tex` |
| Technical specification PDF | `technical-ja.tex` |
| Status or project report PDF | `report-ja.tex` |
| Minimal quick PDF | `minimal.tex` |
| HTML for browser or publication | CSS template |
| Word deliverable with strict styling | `reference.docx` |
