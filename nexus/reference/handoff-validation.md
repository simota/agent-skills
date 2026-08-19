# Nexus Handoff Validation Reference

**Purpose:** Validation requirements for structured handoffs.
**Read when:** A handoff needs integrity checks, confidence checks, or required-field validation.
**See also:** This file **prevents** divergence at handoff time. To **resolve** conflicts that still occurred after parallel branches merged, see `conflict-resolution.md`.

## Contents
- Overview
- NEXUS_HANDOFF_V2 Required Fields
- Confidence Breakdown Components
- Validation Rules
- Validation Failure Handling
- NEXUS_HANDOFF_V2 Template
- Compliance Levels (incl. V1 migration)
- Validation Event Format
- Integration with Auto-Decision

Validation rules and confidence requirements for agent handoffs.

---

## Overview

Handoff validation ensures consistent, high-quality communication between agents. All agents must use NEXUS_HANDOFF_V2 format with mandatory confidence scoring.

## Communication Invariants

These rules own the actionable safeguards formerly split into a separate communication anti-pattern catalog:

| Invariant | Validation |
|-----------|------------|
| Typed envelope | Reject unknown message types, missing required fields, and schema drift; free-form prose may supplement but never replace the envelope |
| Explicit state | Carry current status, completed work, changed resources, evidence, and unresolved items; never assume execution order or hidden shared state |
| Intent integrity | Preserve the original request or its approved intent contract, acceptance criteria, constraints, and prohibited outcomes |
| Selective context | Pass state deltas and required evidence, not the full conversation history |
| Single ownership | Name one owner for each mutable file/resource and one merge owner for parallel work; non-owners default to read-only |
| Closed next action | `next` must be a declared action or agent with success criteria; ambiguous “handle appropriately” handoffs are invalid |
| Recovery-ready | Persist artifact references and the last verified checkpoint so failure does not make the receiving agent the only copy of state |

Confidence never repairs a missing invariant. A high score with an unresolved Authority, absent success criteria, or conflicting ownership is rejected before routing.

---

## NEXUS_HANDOFF_V2 Required Fields

| Field | Required | Description |
|-------|----------|-------------|
| `step` | ✅ | Current step in chain (X/Y) |
| `agent` | ✅ | Agent name that produced this handoff |
| `status` | ✅ | SUCCESS, PARTIAL, BLOCKED, FAILED |
| `confidence` | ✅ **NEW** | Overall confidence score (0.0-1.0) |
| `confidence_breakdown` | ✅ **NEW** | Component scores |
| `summary` | ✅ | 1-3 line summary of work done |
| `artifacts` | ⚪ | Files, commands, links produced |
| `next_agent` | ✅ | Recommended next agent |
| `next_action` | ✅ | CONTINUE, MERGE, VERIFY, ESCALATE, ABORT |

---

## Confidence Breakdown Components

```yaml
confidence_breakdown:
  task_completion: 0.0-1.0   # How much of the task is done
  output_quality: 0.0-1.0    # Quality of produced artifacts
  next_step_clarity: 0.0-1.0 # How clear the next step is

# Overall confidence = weighted average
# task_completion: 0.40
# output_quality: 0.35
# next_step_clarity: 0.25
```

### Scoring Guidelines

**task_completion:**
| Score | Meaning |
|-------|---------|
| 1.0 | Task fully completed, all acceptance criteria met |
| 0.8 | Task mostly complete, minor items remaining |
| 0.6 | Significant progress, some work remaining |
| 0.4 | Partial progress, major work remaining |
| 0.2 | Started but blocked or early stage |
| 0.0 | No progress made |

**output_quality:**
| Score | Meaning |
|-------|---------|
| 1.0 | Production-ready, tested, documented |
| 0.8 | High quality, minor polish needed |
| 0.6 | Acceptable quality, some improvements possible |
| 0.4 | Functional but needs significant improvement |
| 0.2 | Draft/prototype quality |
| 0.0 | No usable output |

**next_step_clarity:**
| Score | Meaning |
|-------|---------|
| 1.0 | Crystal clear next step, no ambiguity |
| 0.8 | Clear next step with minor details to decide |
| 0.6 | General direction clear, specifics uncertain |
| 0.4 | Multiple possible paths, guidance needed |
| 0.2 | Unclear, user input likely needed |
| 0.0 | Completely blocked, cannot proceed |

---

## Validation Rules

### Pre-routing Validation

Before Nexus routes to next agent, validate:

```yaml
validation_checks:
  required_fields:
    - step: must be "X/Y" format
    - agent: must be valid agent name
    - status: must be enum value
    - confidence: must be 0.0-1.0
    - confidence_breakdown: all three components present
    - summary: non-empty string
    - next_agent: valid agent name or "DONE"
    - next_action: valid enum value

  consistency_checks:
    - status == SUCCESS implies confidence >= 0.70
    - status == FAILED implies next_action in [ESCALATE, ABORT]
    - status == BLOCKED implies pending_confirmations present
    - confidence_breakdown average ≈ confidence (±0.05)
```

### Auto-Routing

Confidence bands (≥ 0.75 auto-route · 0.50-0.74 route with logged assumptions · < 0.50 pause for user input) are canonical in `output-formats.md` § Auto-Routing Rules. Independent of the band, `status == BLOCKED` or a pending confirmation pauses, and `status == FAILED` / `next_action == ESCALATE` escalates.

---

## Validation Failure Handling

When validation fails:

```yaml
validation_failure:
  missing_required_field:
    action: request_resubmit
    message: "Handoff missing required field: [field]"

  invalid_confidence:
    action: request_clarification
    message: "Confidence score [value] inconsistent with status [status]"

  consistency_error:
    action: auto_correct OR request_resubmit
    auto_correct_if: minor_discrepancy
```

---

## NEXUS_HANDOFF_V2 Template

Canonical schema (all fields, including `user_confirmations`) → `output-formats.md` § NEXUS_HANDOFF_V2. Validation below checks conformance to that template.

---

## Compliance Levels

| Level | Fields Required | Use When |
|-------|----------------|----------|
| Level 1 (Minimal) | `step`, `agent`, `status`, `summary`, `next_agent`, `next_action` | Model cannot produce reliable confidence scores |
| Level 2 (Standard) | Level 1 + `confidence` (single number) | Model can estimate overall confidence |
| Level 3 (Full/Claude default) | Level 2 + `confidence_breakdown` (3 axes) | Full scoring capability |

Level 1 confidence inference (applied automatically):

| status | Inferred confidence |
|--------|-------------------|
| SUCCESS | 0.80 |
| PARTIAL | 0.60 |
| BLOCKED | 0.40 |
| FAILED | 0.20 |

Level 2 without breakdown: all three components assumed equal to overall confidence.

A V1 handoff is migrated by applying those same two rules — infer confidence from `status`, distribute it equally across the three components — and is accepted with a logged warning flagging the agent for a V2 update.

---

## Validation Event Format

```yaml
_VALIDATION_EVENT:
  handoff_from: [Agent]
  step: X/Y

  validation_result: [PASS|WARN|FAIL]

  checks:
    required_fields: [PASS|FAIL: field]
    confidence_valid: [PASS|FAIL: reason]
    consistency: [PASS|FAIL: issue]

  action_taken: [proceed|request_resubmit|auto_correct]

  notes: [Any warnings or corrections made]
```

---

## Integration with Auto-Decision

Handoff confidence feeds into routing decisions:

```
Agent completes work
        │
        ▼
┌─────────────────┐
│ NEXUS_HANDOFF   │
│ with confidence │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate        │ → Check all rules
│ Handoff         │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
  PASS      FAIL
    │         │
    ▼         ▼
┌─────────┐  Request
│ Route   │  Resubmit
│ Decision│
└────┬────┘
     │
┌────┴────────────────┐
│ confidence >= 0.75  │ → Auto-route to next_agent
│ confidence 0.50-0.74│ → Route with logged assumption
│ confidence < 0.50   │ → Pause for user input
└─────────────────────┘
```
