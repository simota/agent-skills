# Quality Assurance Guide

Purpose: Use this reference when scoring conversion fidelity, grading outputs, or setting up manual or automated verification — the **per-conversion** measurement step.
Pair with: `conversion-calibration.md` for the **cross-conversion** learning loop that consumes these scores (record schema, tool-effectiveness tracking, calibration rules, pattern library).

## Contents

- Quality metrics
- Grade thresholds
- Verification process
- Quality report template
- Regression testing

## Quality Metrics

| Metric | Weight | Meaning |
|-------|--------|---------|
| Structure Fidelity | `30%` | Heading, list, table, and code structure retention |
| Visual Fidelity | `25%` | Fonts, layout, spacing, and styling match intent |
| Content Integrity | `30%` | No missing text, images, links, or data |
| Metadata Preservation | `15%` | Title, author, date, keywords, and other metadata survive |

## Grade Thresholds

| Score | Grade | Meaning | Action |
|------|-------|---------|--------|
| `90-100` | `A` | Ready for distribution | Ship |
| `80-89` | `B` | Minor issues | Review before delivery |
| `70-79` | `C` | Noticeable issues | Fix before delivery |
| `60-69` | `D` | Significant issues | Reconvert with fixes |
| `<60` | `F` | Unacceptable | Investigate root cause |

## Verification Process

### Pre-Conversion

```sh
file input.md
stat input.md
grep -c "^#" input.md
grep -c "^\\*" input.md
grep -c "!\\[" input.md
grep -c "\\[.*\\](" input.md
```

### During Conversion

```sh
pandoc input.md -o output.pdf --pdf-engine=xelatex -v 2>&1 | tee conversion.log
```

### Post-Conversion

```sh
pdfinfo output.pdf
pdffonts output.pdf
pdfimages -list output.pdf
pdftotext output.pdf output.txt
```

## Quality Report Template

```md
# Conversion Quality Report

## Summary
- Source:
- Target:
- Tool:
- Template:
- Grade:

## Metric Scores
- Structure:
- Visual:
- Content:
- Metadata:
- Overall:

## Warnings
- 

## Recommended Fixes
- 
```

## Regression Testing

Rules:

- Keep a feature-rich test document that includes headings, lists, tables, code, images, links, and metadata.
- Re-run the same test set after tool, template, or dependency updates.
- Compare both score and artifact quality, not only exit status.

Example:

```sh
pandoc test-features.md -o test-output.pdf --pdf-engine=xelatex
pandoc test-features.md -o test-output.docx
pandoc test-features.md -o test-output.html -s
```
