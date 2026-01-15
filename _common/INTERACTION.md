# Interaction Rules (Common Definition)

This file defines the common interaction control rules that all agents reference.

---

## INTERACTION_MODE (Execution Modes)

| Mode | Trigger | Behavior | Interaction Timing |
|------|---------|----------|-------------------|
| AUTORUN | `## NEXUS_AUTORUN` + SIMPLE assessment | Fully automatic execution | Error cases only |
| GUIDED | Default or `## NEXUS_GUIDED` | Confirm at decision points | Per INTERACTION_TRIGGERS |
| INTERACTIVE | `## NEXUS_INTERACTIVE` | Confirm at every step | Always confirm |
| Kickoff | (No mode specified) | Chain design only | Initial confirmation only |

---

## QUESTION_FORMAT (AskUserQuestion Tool Compliant)

**Required:** All questions must use the `AskUserQuestion` tool format.

### Tool Specification

```yaml
questions: # Array of 1-4 questions (required)
  - question: "Question text (ends with ?, clear and specific)"
    header: "Short label"  # Max 12 chars, displayed as chip/tag
    options:  # 2-4 options ("Other" is auto-added)
      - label: "Option name"  # 1-5 words
        description: "Explanation of this option"
      - label: "Option name"
        description: "Explanation of this option"
    multiSelect: false  # true allows multiple selections
```

### Question Design Guidelines

| Rule | Description | Example |
|------|-------------|---------|
| header max 12 chars | Displayed as chip/tag | "Exec Mode", "Fix Strategy" |
| options 2-4 items | "Other" is auto-added, don't include | 3 options is standard |
| Recommended first | Add "(Recommended)" to label | "Use mock data (Recommended)" |
| description shows impact | Explain outcome of selection | "Safely proceed with mock data" |
| multiSelect cautiously | Only true when not mutually exclusive | Feature selection etc. |

---

## COMPLEXITY_ASSESSMENT (Complexity Evaluation)

Criteria for assessing task complexity and auto-selecting execution mode.

| Indicator | SIMPLE | COMPLEX |
|-----------|--------|---------|
| Estimated steps | 1-2 | 3+ |
| Files affected | 1-3 | 4+ |
| Security related | No | Yes |
| Infrastructure change | No | Yes |
| Requirement ambiguity | Clear | Ambiguous |
| Breaking change | No | Yes |
| External API change | No | Yes |

### Assessment Logic

```
IF any(COMPLEX indicators) THEN
  → GUIDED or INTERACTIVE required
ELSE IF all(SIMPLE indicators) AND user specified NEXUS_AUTORUN THEN
  → AUTORUN allowed
ELSE
  → GUIDED (default)
```

---

## INTERACTION_TRIGGER_TYPES (Trigger Timing Types)

Timing types for interaction triggers defined by each agent.

| Timing | Description | Use Case |
|--------|-------------|----------|
| BEFORE_START | Confirm before starting work | Requirements, policy decisions |
| ON_DECISION | Confirm at important decisions | When multiple options exist |
| ON_RISK | Confirm when risk detected | Security, breaking changes |
| ON_AMBIGUITY | Confirm when ambiguity found | Unclear specifications |
| NEVER | No confirmation needed | Routine tasks |

---

## STANDARD_TRIGGERS (Standard Trigger Definitions)

Standard triggers available to all agents.

### BEFORE_PRODUCTION_DATA

When production data access is required.

```yaml
questions:
  - question: "Production data access is required. How do you want to proceed?"
    header: "Data Access"
    options:
      - label: "Use mock data (Recommended)"
        description: "Safely proceed with mock data for investigation"
      - label: "Access production data"
        description: "Use actual data but requires caution"
      - label: "Skip this task"
        description: "Proceed to next step without data access"
    multiSelect: false
```

### ON_SECURITY_RISK

When a security risk is detected.

```yaml
questions:
  - question: "A security risk has been detected. How do you want to handle it?"
    header: "Security"
    options:
      - label: "Audit with Sentinel (Recommended)"
        description: "Request review from security specialist agent"
      - label: "Proceed with awareness"
        description: "Continue at your own risk"
      - label: "Stop work"
        description: "Halt work for safety"
    multiSelect: false
```

### ON_BREAKING_CHANGE

When a breaking change is required.

```yaml
questions:
  - question: "A breaking change is required. Do you want to proceed?"
    header: "Breaking Change"
    options:
      - label: "Review impact first (Recommended)"
        description: "Display list of affected code"
      - label: "Execute change"
        description: "Proceed with implementation including breaking change"
      - label: "Maintain compatibility"
        description: "Consider alternatives to avoid breaking change"
    multiSelect: false
```

### ON_MULTIPLE_APPROACHES

When multiple implementation approaches exist.

```yaml
questions:
  - question: "Multiple implementation approaches are available. Which do you prefer?"
    header: "Approach"
    options:
      - label: "[Approach A] (Recommended)"
        description: "[Reason for recommendation]"
      - label: "[Approach B]"
        description: "[Characteristics/trade-offs]"
      - label: "[Approach C]"
        description: "[Characteristics/trade-offs]"
    multiSelect: false
```

---

## CONFIRMATION_RECORD (Confirmation Recording Format)

Format for recording interaction results. Include in NEXUS_HANDOFF.

### Pending Confirmations (Awaiting Confirmation)

Record unconfirmed interaction triggers when agent returns to Nexus.

```yaml
Pending Confirmations:
  - trigger: "ON_BREAKING_CHANGE"
    question: "A breaking change is required. Do you want to proceed?"
    options:
      - "Review impact first (Recommended)"
      - "Execute change"
      - "Maintain compatibility"
    recommended: "Review impact first (Recommended)"
```

### User Confirmations (Confirmed)

Record user responses. Used for handoff to subsequent agents.

```yaml
User Confirmations:
  - question: "Production data access is required. How do you want to proceed?"
    answer: "Use mock data (Recommended)"
    timestamp: "2024-01-08T10:30:00"
```

---

## ESCALATION_RULES (Escalation Rules)

Escalation when interaction cannot resolve issues.

| Level | Condition | Action |
|-------|-----------|--------|
| Level 1 | Minor unknowns | Auto-proceed with safest option |
| Level 2 | Multiple valid options | Confirm with AskUserQuestion |
| Level 3 | Blocking unknowns | Pause work, user confirmation required |
| Level 4 | Unresolved after 3 escalations | Abort work, recommend manual handling |

---

## OUTPUT_LANGUAGE

All question text, options, and descriptions must be output in **Japanese**.
