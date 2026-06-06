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
- Backward Compatibility
- Validation Event Format
- Integration with Auto-Decision

Validation rules and confidence requirements for agent handoffs.

---

## Overview

Handoff validation ensures consistent, high-quality communication between agents. All agents must use NEXUS_HANDOFF_V2 format with mandatory confidence scoring.

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

### Auto-Routing Rules

```yaml
auto_routing:
  proceed_if:
    - confidence >= 0.75
    - status == SUCCESS
    - next_action == CONTINUE

  pause_if:
    - confidence < 0.50
    - status == BLOCKED
    - pending_confirmations present

  escalate_if:
    - status == FAILED
    - next_action == ESCALATE
    - confidence < 0.30
```

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

```yaml
## NEXUS_HANDOFF
step: X/Y
agent: [AgentName]
status: [SUCCESS|PARTIAL|BLOCKED|FAILED]

confidence: 0.XX
confidence_breakdown:
  task_completion: 0.XX
  output_quality: 0.XX
  next_step_clarity: 0.XX

summary: |
  [1-3 line summary of work completed]

key_findings:
  - [Finding 1]
  - [Finding 2]

artifacts:
  - type: [file|command|link]
    path: [path or URL]
    description: [what it is]

risks:
  - [Risk 1]
  - [Risk 2]

open_questions:
  - blocking: [true|false]
    question: [Question]

pending_confirmations:  # Only if status == BLOCKED
  - trigger: [INTERACTION_TRIGGER]
    question: [Question]
    options: [List]
    recommended: [Option]

next_agent: [AgentName|DONE]
next_action: [CONTINUE|MERGE|VERIFY|ESCALATE|ABORT]
reason: [Why this next step]
```

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

## Backward Compatibility

The Compliance Levels above formalize the backward compatibility rules:

```yaml
v1_to_v2_migration:
  if_missing_confidence:
    infer_from:
      - status: SUCCESS → confidence: 0.80
      - status: PARTIAL → confidence: 0.60
      - status: BLOCKED → confidence: 0.40
      - status: FAILED → confidence: 0.20

    log_warning: true
    request_update: true  # Flag agent for V2 update

  if_missing_breakdown:
    assume_equal_distribution: true
    # All three components = overall confidence
```

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
