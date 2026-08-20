# Scribe Recipe Registry

The full Recipe table for `scribe`. `scribe/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| PRD | `prd` | ✓ | Product Requirements Document (business goals, user needs, scope) | `reference/prd-template.md` |
| SRS | `srs` | | Software Requirements Specification (technical requirements, interfaces, NFRs) | `reference/srs-template.md` |
| HLD | `hld` | | High-Level Design (system architecture, component design) | `reference/design-template.md` |
| LLD | `lld` | | Low-Level Design (module details, data structures, sequences) | `reference/design-template.md` |
| Test Spec | `testspec` | | Test specification (scope, cases, data, traceability) | `reference/test-spec-template.md` |
| ADR | `adr` | | Architecture Decision Record (Nygard/MADR format, ADR numbering, immutability, supersede chain) | `reference/adr-writing.md` |
| Runbook | `runbook` | | Operational runbook (symptom → triage → recover → verify, escalation, idempotency) | `reference/runbook-writing.md` |
| API Doc | `api-doc` | | Human-readable API reference from OpenAPI (code samples, error catalog, auth flow, versioning) | `reference/api-documentation.md` |
| Unified Spec | `unified` | | Full/Standard/Lite cross-team package with staged L0-L4 elaboration | `reference/unified-spec/unified-template.md` |
| Format Conversion | `convert` |  | Convert a document between Markdown, Word, Excel, PDF, and HTML | `reference/format-conversion/conversion-matrix.md`, `reference/format-conversion/pandoc-recipes.md`, `reference/format-conversion/format-conversion-anti-patterns.md` |
