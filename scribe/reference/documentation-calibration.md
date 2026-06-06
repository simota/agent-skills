# Documentation Calibration System (INSCRIBE)

Purpose: Use this file after document creation or during periodic review to improve template choice, handoff quality, and requirement precision.

Contents:

- RECORD
- EVALUATE
- CALIBRATE
- PROPAGATE
- Ecosystem integration

## Overview

`RECORD -> EVALUATE -> CALIBRATE -> PROPAGATE`

INSCRIBE closes the loop between document creation and downstream implementation outcomes. Use it to measure whether Scribe outputs were adopted, accurate, and actionable.

## RECORD

After each document, record:

```yaml
Document: [document-id]
Type: [PRD | SRS | HLD | LLD | Impl Checklist | Test Spec | Review Checklist]
Feature: [feature name]
Requirements_Count: [count]
Acceptance_Criteria_Count: [count]
Template_Used: [full | minimal]
Sections_Included: [list]
Quality_Checklist_Score:
  structure: [pass | partial | fail]
  content: [pass | partial | fail]
  testability: [pass | partial | fail]
  traceability: [pass | partial | fail]
Downstream_Handoff: [Sherpa | Builder | Radar | Voyager | Judge | None]
```

Track at minimum:

- specification adoption
- requirement completeness
- template effectiveness
- document accuracy
- handoff quality
- revision frequency

## EVALUATE

### Adoption Rate

`Documents Referenced by Downstream Agents / Total Documents Created`

| Range | Interpretation | Action |
|------|----------------|--------|
| `> 0.85` | High-impact documentation | Keep current approach. |
| `0.60-0.85` | Moderate adoption | Review handoff format and audience fit. |
| `< 0.60` | Low adoption | Revisit usefulness, scope, and information density. |

### Requirement Accuracy

`Requirements Implemented as Specified / Total Requirements`

| Range | Interpretation | Action |
|------|----------------|--------|
| `> 0.90` | Excellent | Preserve the pattern. |
| `0.75-0.90` | Good | Tighten ambiguous areas. |
| `< 0.75` | Weak | Rework clarity and testability. |

### Common Evaluation Triggers

- Builder requests clarification
- Radar cannot derive tests from the spec
- Shipped feature diverges from the document
- The same spec is revised multiple times
- Quarterly documentation review

## CALIBRATE

### Rules

1. Wait for `3+ documents` before changing effectiveness scores.
2. Limit changes to `±0.15` per cycle.
3. Decay adjustments by `10%` per quarter toward defaults.
4. Explicit user or project preferences override calibrated defaults.

### Pattern Effectiveness

| Pattern | Adoption Impact | Best For |
|------|------------------|----------|
| `REQ-XXX` IDs | High | All document types |
| Given-When-Then acceptance criteria | High | PRD, SRS, Test Spec |
| `IMPL-XXX` with I/O contract | High | Implementation checklists |
| Inline diagrams | Medium | HLD, SRS |
| Traceability matrix | Medium | Multi-document work |
| Minimal templates | High | Small enhancements and bug fixes |

### Document Size Calibration

| Document Type | Default Size | Calibrated Range | Guidance |
|--------------|--------------|------------------|----------|
| PRD (full) | `200-400 lines` | `150-350 lines` | Shorter docs increased adoption. |
| PRD (minimal) | `30-80 lines` | `40-80 lines` | Under `40` lines often missed edge cases. |
| SRS | `200-500 lines` | `200-400 lines` | Over `400` lines reduced read-through. |
| HLD | `150-300 lines` | `100-250 lines` | Prefer diagrams over prose. |
| LLD | `200-400 lines` | `200-350 lines` | Add code-shaped examples only when clarifying a design choice. |
| Test Spec | `100-300 lines` | `100-250 lines` | Tables outperform prose for execution. |

## PROPAGATE

Record reusable findings in `.agents/scribe.md`:

```markdown
## YYYY-MM-DD - INSCRIBE: [Document Type]

**Documents assessed**: N
**Overall adoption rate**: X%
**Key insight**: [description]
**Calibration adjustment**: [template/pattern: old -> new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Scribe
date: YYYY-MM-DD
summary: [documentation insight]
affects: [Scribe, Accord, Sherpa]
priority: MEDIUM
reusable: true
-->
```

Quick rule for small documents:

- If a document has fewer than `3 requirements`, record observations but do not recalibrate weights from that document alone.

## Ecosystem Integration

| Signal | Action |
|------|--------|
| Adoption improving | Keep template selection and writing pattern. |
| Adoption degrading | Rework template density, audience alignment, or handoff structure. |
| Template repeatedly underperforming | Prefer an alternative template for that context. |
| High requirement accuracy | Propagate the pattern to Lore. |
| Low downstream usage | Adjust detail level or handoff completeness. |
| Reusable documentation pattern | Emit `EVOLUTION_SIGNAL` and share with Lore, Accord, or Sherpa. |
