# PDF Accessibility Anti-Patterns

Purpose: Use this reference when tagged PDF, reading order, alt text, table structure, or assistive-technology compatibility is at risk.

## Contents

- Accessibility anti-pattern catalog
- WCAG/PDF technique map
- PDF/UA rules
- Verification layers

## Accessibility Anti-Pattern Catalog

| ID | Anti-pattern | Signal | Correction |
|----|--------------|--------|-----------|
| `PA-01` | Untagged PDF | Screen readers cannot interpret structure | Generate tagged PDF |
| `PA-02` | Undefined reading order | Content is read in the wrong order | Verify logical order explicitly |
| `PA-03` | Missing or low-quality alt text | Images are meaningless to non-visual users | Provide meaningful alt text; artifact purely decorative images |
| `PA-04` | Undefined table structure | Complex tables are unusable | Mark headers and structure explicitly |
| `PA-05` | Missing form labels | Form purpose is unclear | Set name/role/value clearly |
| `PA-06` | Low contrast | Users cannot read the document | Verify `4.5:1` for normal text and `3:1` for large text |
| `PA-07` | Over-reliance on auto-fix tools | Structural issues survive | Combine automated and manual review |

## WCAG / PDF Technique Map

Priorities to preserve:

- Alt text
- Headings and document structure
- Logical sequence
- Tables
- Language metadata
- OCR for scanned content

Rules:

- Scanned PDFs require `OCR -> tagging -> verification`.
- Do not assume print/export tools create accessible structure automatically.

## PDF/UA Rules

- Tagged structure is mandatory.
- Title and language metadata are mandatory.
- Fonts should be embedded.
- Interactive elements need accessible labeling.

## Verification Layers

1. Automated scan with tools such as `PAC`.
2. Manual review of reading order and alt-text quality.
3. Assistive-tech review when required.
4. User validation for high-risk public documents.
