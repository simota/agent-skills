# Morph Conversion Workflow

Purpose: Use this reference when preparing a reproducible conversion job, including source analysis, tool configuration, logging, verification, and delivery.

## Contents

- Source analysis template
- Conversion config template
- Conversion log template
- Verification checklist
- Delivery template

## 1. ANALYZE — Source Analysis

```md
## Source Analysis: [filename]
- Format:
- Target:
- Headings:
- Lists:
- Tables:
- Code blocks:
- Images: [count, formats]
- Links / references:
- Metadata present:
- Potential fidelity risks:
- Missing dependencies:
```

## 2. CONFIGURE — Conversion Config

```yaml
source: input.md
target: output.pdf
tool: pandoc
options:
  pdf-engine: xelatex
  toc: true
  metadata-file: metadata.yaml
template: corporate-ja.tex
quality_profile: standard
```

## 3. CONVERT — Conversion Log

```md
## Conversion Log
- Source:
- Target:
- Tool:
- Template:
- Start time:
- End time:
- Output:
- Warnings:
- Errors:
- Substitutions:
```

Rules:

- Fail explicitly when conversion errors occur.
- Do not silently continue after a broken conversion.

## 4. VERIFY — Quality Checklist

- [ ] Headings preserved
- [ ] Lists preserved
- [ ] Tables preserved or loss documented
- [ ] Code blocks readable
- [ ] Images resolved
- [ ] Links preserved
- [ ] Metadata present
- [ ] Target-specific checks completed

## 5. DELIVER — Completion Template

```md
## Conversion Complete
- Source:
- Target:
- Output path:
- Tool and template:
- Quality grade:
- Known limitations:
- Accessibility / archival status:
- Next action:
```
