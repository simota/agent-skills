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

---

Behavior notes per Recipe:
- `prd`: Establish business context first. State in-scope/out-of-scope, KPIs, and success metrics explicitly. Target 8-12 pages for MVP.
- `srs`: Apply the IEEE 29148 quality gate. Attach measurable thresholds to NFRs (e.g., P95 ≤ 200ms).
- `hld`: Describe system composition, deployment, and scaling strategy. Link to Atlas ADRs for reference.
- `lld`: Module design, data structures, and sequence diagrams. Detail granularity for immediate implementation.
- `testspec`: Given/When/Then format. Must include test scope, data, and traceability matrix.
- `adr`: The GENERAL ADR-writing recipe, for any agent or human. An accepted ADR is immutable — superseded, never edited. Application/module-level architecture decisions (dependency direction, layer boundary, pattern choice) go to `Atlas`, which owns the tradeoff analysis and authors those ADRs itself. Format, numbering, and supersede chain -> `reference/adr-writing.md`.
- `runbook`: Authors the runbook artifact, which `Triage` consumes at first response and `Mend` executes during remediation. Scribe neither diagnoses nor executes. Cross-link the upstream postmortem or incident ticket. Required sections and authoring flow -> `reference/runbook-writing.md`.
- `api-doc`: Turns a Gateway-authored OpenAPI 3.1 spec into the human-facing reference. Gateway `openapi` owns the spec (the YAML contract); Scribe owns the documentation surface — handoff direction is Gateway -> Scribe. Publishing targets and required surfaces -> `reference/api-documentation.md`.
- `unified`: Run the full unified workflow or one normalized mode. `vision` produces one-page `L0`; `requirements` creates testable `L1`; `detail` translates audience-specific `L2`; `ac` runs Three Amigos / Example Mapping for `L3`; `story-map` builds a walking skeleton and release slices; `stakeholder` maps Power × Interest and engagement; `raci` assigns exactly one accountable owner per row using RACI/DACI/RAPID.
