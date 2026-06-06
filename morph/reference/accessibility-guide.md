# Accessibility Guide

Purpose: Use this reference when the output must meet PDF/UA or WCAG requirements, or when alt text, reading order, contrast, or tagged PDF support matters.

## Contents

- Standards overview
- Tagged PDF creation
- Alt text and reading order
- Contrast and font rules
- Testing tools
- Accessible conversion checklist

## Standards Overview

### PDF/UA

Key requirements:

- Tagged PDF structure
- Logical reading order
- Alternative text for meaningful images
- Document language metadata
- Unicode text
- Title and document metadata

### WCAG 2.1

Key criteria used here:

| Criterion | Level | Requirement |
|-----------|-------|-------------|
| Non-text content | A | Alt text for images |
| Structure and relationships | A | Headings, lists, and tables are programmatic |
| Meaningful sequence | A | Reading order is logical |
| Contrast | AA | `4.5:1` minimum for normal text |
| Page titled | A | Document title exists |
| Language of page | A | Language metadata exists |

## Tagged PDF Creation

```sh
# Basic tagged PDF
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V classoption=tagged \
  --metadata lang=ja \
  --metadata title="Document Title"

# Full accessibility-oriented PDF
pandoc input.md -o output.pdf \
  --pdf-engine=lualatex \
  -V documentclass=article \
  -V classoption=tagged \
  --metadata lang=ja \
  --metadata title="Document Title" \
  --metadata author="Author Name" \
  -V fontsize=12pt \
  -V geometry="margin=25mm" \
  --toc --toc-depth=3
```

Rules:

- Minimum accessible PDF font size: `12pt`.
- Language metadata is required.
- Use tagged output when the document must be accessible.

## Alt Text And Reading Order

- Provide meaningful alt text for informative images.
- Mark decorative images as artifacts when the toolchain supports it.
- Verify reading order with extracted text and manual review.

```sh
pdftotext -layout output.pdf -
```

## Contrast And Font Rules

| Item | Requirement |
|------|-------------|
| Normal text | `4.5:1` |
| Large text | `3:1` minimum practical target; `4.5:1` is acceptable for stricter policies |
| Accessible PDF font size | `12pt` minimum |

## Testing Tools

| Tool | Use |
|------|-----|
| PAC 3 | PDF accessibility scan |
| `pdfinfo` | metadata and tagged status |
| `pdftotext` | reading order review |
| `pdffonts` | font embedding check |

Example:

```sh
pdfinfo output.pdf
pdftotext -layout output.pdf -
pdffonts output.pdf
```

## Accessible Conversion Checklist

- [ ] Tagged PDF generated
- [ ] Language metadata present
- [ ] Title metadata present
- [ ] Alt text reviewed
- [ ] Reading order reviewed
- [ ] Contrast meets `4.5:1`
- [ ] Font size `>= 12pt`
- [ ] Automated scan completed
- [ ] Manual review completed
