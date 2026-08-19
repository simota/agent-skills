# Cross-Reference And Traceability Guide

Purpose: Use this file when building or validating IDs, link syntax, traceability matrices, and status handling.

## Contents

- ID conventions
- Link syntax
- Traceability matrix
- Completeness rules
- Integrity verification
- Verification timing

## ID Convention

| Level | Prefix | Example | Purpose |
|---|---|---|---|
| `L1` | `US-XXX` | `US-001` | user story |
| `L1` | `REQ-XXX` | `REQ-001` | functional requirement |
| `L1` | `NFR-XXX` | `NFR-001` | non-functional requirement |
| `L2-Dev` | `API-XXX` | `API-001` | API specification |
| `L2-Dev` | `DATA-XXX` | `DATA-001` | data model |
| `L2-Design` | `DESIGN-XXX` | `DESIGN-001` | design requirement |
| `L2-Design` | `FLOW-XXX` | `FLOW-001` | user flow |
| `L3` | `AC-XXX` | `AC-001` | BDD acceptance criterion |

## Link Syntax

Use:

```markdown
**Linked:** REQ-001, DESIGN-002, AC-003
```

## Traceability Matrix

```markdown
| REQ | User Story | API | Data | Design | Flow | Acceptance | Status |
|---|---|---|---|---|---|---|---|
| REQ-001 | US-001 | API-001 | DATA-001 | DESIGN-001 | FLOW-001 | AC-001, AC-002 | Draft |
```

## Status Values

| Status | Meaning |
|---|---|
| `Draft` | initial draft, not reviewed |
| `Review` | under review |
| `Approved` | approved by all required teams |
| `Deprecated` | replaced or intentionally retired |

## Completeness Rules

| Scope | Required links | Optional links |
|---|---|---|
| `Full` | `REQ -> US` and `REQ -> AC` | `API`, `DATA`, `DESIGN`, `FLOW` |
| `Standard` | `REQ -> AC` | `US`, `API`, `DESIGN` |
| `Lite` | `REQ -> AC` only | everything else |

## Integrity Verification

### Forward Traceability

- every `REQ` links to at least one `AC`
- every `US` links to at least one `REQ`
- no orphan `REQ`

### Backward Traceability

- every `AC` links back to at least one `REQ`
- every design element links back to a `REQ`
- every API item links back to a `REQ`

### Cross-Level Consistency

- `L0` scope and `L1` requirements do not conflict
- `L1` non-functional requirements do not contradict `L2-Dev`
- `L2-Design` flows cover the intended `L1` stories
- `L3` covers all `Must` requirements

### Terminology Consistency

- the same concept uses the same name
- a glossary exists when teams use different labels
- team-specific abbreviations are explained

## Common Integrity Issues

| Issue | Detection | Fix |
|---|---|---|
| orphan `REQ` | no linked `AC` | add `AC` or remove the `REQ` |
| orphan `AC` | no linked `REQ` | add `REQ` or remove the `AC` |
| scope drift | `L1` conflicts with `L0 Out` | change scope or remove requirement |
| term conflict | names differ across `L2` sections | align through glossary |
| level gap | `L2` item has no supporting requirement | add explicit `REQ` |

## Verification Timing

| Phase | Check |
|---|---|
| `STRUCTURE` | ID scheme is consistent |
| `ELABORATE` | forward links stay valid while writing |
| `BRIDGE` | run the main traceability review |
| `VERIFY` | run the final consistency and terminology review |
