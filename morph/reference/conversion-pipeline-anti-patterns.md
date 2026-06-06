# Conversion Pipeline Anti-Patterns

Purpose: Use this reference when building CI/CD, Docker, artifact storage, batch conversion, or automated quality gates around Morph workflows.

## Contents

- Pipeline anti-pattern catalog
- Container and CI rules
- Quality automation
- Versioning rules

## Pipeline Anti-Pattern Catalog

| ID | Anti-pattern | Signal | Correction |
|----|--------------|--------|-----------|
| `PP-01` | Hidden environment dependencies | Local success, CI failure | Containerize or pin dependencies explicitly |
| `PP-02` | Committing generated artifacts | PDFs or DOCX are versioned in git | Publish as CI artifacts instead |
| `PP-03` | Rebuilding on every change | Irrelevant changes trigger conversion | Use path filters such as docs/templates changes only |
| `PP-04` | No quality gate | Broken output reaches delivery | Add automated output checks |
| `PP-05` | No error handling | Pipeline continues after failed conversion | Fail clearly, notify, and retain rollback path |
| `PP-06` | Markdown dialect mismatch | Rendering differs per tool | Standardize dialect and lint inputs |
| `PP-07` | Hardcoded templates in scripts | Style changes require script surgery | Externalize templates and variables |

## Container And CI Rules

- Prefer pinned images such as `pandoc/extra:3.1.12`, not `latest`.
- Package required fonts and conversion tools in the build environment.
- Store generated artifacts in CI, not the source repository.
- Trigger conversion jobs only on relevant path changes.

## Quality Automation

Minimum levels:

1. Output exists and is non-empty.
2. Structure and asset checks pass.
3. Fidelity checks pass for distributed docs.
4. Accessibility checks pass for public docs.

Rules:

- Level 1-2 should be automated by default.
- Add accessibility automation and manual review when required.

## Versioning Rules

- Pin Pandoc, LaTeX, Mermaid CLI, and similar tooling.
- Re-run regression tests after tool or image upgrades.
- Keep snapshot or comparison output for conversion-quality regressions.
