# Scribe Document Type Selection

Moved out of `scribe/SKILL.md` so it loads when it is needed rather than on
every invocation. The text is unchanged.

---

| Type               | Use When                                          | Output Path                       | Read This                                                                         |
| ------------------ | ------------------------------------------------- | --------------------------------- | --------------------------------------------------------------------------------- |
| `PRD`              | Business scope, user needs, goals, non-goals      | `docs/prd/PRD-[name].md`          | `reference/prd-template.md`             |
| `SRS`              | Technical behavior, interfaces, constraints, NFRs | `docs/specs/SRS-[name].md`        | `reference/srs-template.md`             |
| `HLD`              | System architecture, components, deployment       | `docs/design/HLD-[name].md`       | `reference/design-template.md`       |
| `LLD`              | Module design, data structures, sequences, config | `docs/design/LLD-[name].md`       | `reference/design-template.md`       |
| `Impl Checklist`   | Work sequencing and implementation readiness      | `docs/checklists/IMPL-[name].md`  | `reference/checklist-template.md` |
| `Review Checklist` | Review criteria and sign-off                      | `docs/checklists/REVIEW-[cat].md` | `reference/checklist-template.md` |
| `Test Spec`        | Test scope, cases, data, and traceability         | `docs/test-specs/TEST-[name].md`  | `reference/test-spec-template.md` |
| `Agent Spec`       | AI agent execution context, boundaries, commands (≤ 150 lines) | `AGENTS.md` or `docs/specs/AGENT-[name].md` | `reference/srs-template.md` |
| `Unified Spec`     | Multiple audiences need one staged source of truth | `docs/specs/UNIFIED-[name].md` | `reference/unified-spec/unified-template.md` |
| `Story Map`        | A flat backlog needs an end-to-end walking skeleton and release slices | `docs/specs/STORY-MAP-[name].md` | `reference/unified-spec/user-story-mapping.md` |
| `Stakeholder Map`  | Power/interest, engagement, and information flow need definition | `docs/specs/STAKEHOLDERS-[name].md` | `reference/unified-spec/stakeholder-map.md` |
| `Responsibility Matrix` | Governance needs one accountable owner per item/decision | `docs/specs/RACI-[name].md` | `reference/unified-spec/raci-matrix.md` |
