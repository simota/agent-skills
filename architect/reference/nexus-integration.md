# Nexus Integration

**Purpose:** AUTORUN, hub-mode, and handoff requirements for Nexus compatibility.
**Read when:** You need the exact integration contract with Nexus.

## Contents
- Overview
- Integration Requirements
- Routing Matrix Update
- Category Registration
- NEXUS_HANDOFF Format
- _AGENT_CONTEXT Format
- _STEP_COMPLETE Format
- Execution Flow Integration
- Guardrail Compatibility
- Testing Integration
- Documentation Updates
- Rollback Procedure

---

## Overview

All agents in the ecosystem operate under Nexus's hub-and-spoke pattern.
New agents must be fully compatible with Nexus routing and AUTORUN modes.

---

## Integration Requirements

### 1. AUTORUN Support

Every agent must support autonomous execution:

```yaml
AUTORUN_REQUIREMENTS:
  input:
    - Parse _AGENT_CONTEXT
    - Extract Role, Task, Mode, Chain
    - Understand Input handoff
    - Respect Constraints
    - Know Expected_Output

  execution:
    - Skip verbose explanations
    - Focus on deliverables
    - Work within constraints
    - Handle errors gracefully

  output:
# ...
```

### 2. Hub Mode Support

Every agent must route results through Nexus:

```yaml
HUB_MODE_REQUIREMENTS:
  trigger:
    - Detect "## NEXUS_ROUTING" in input
    - Switch to hub mode

  behavior:
    - Do NOT call other agents directly
    - Do NOT output agent invocation prompts
    - Return all results to Nexus

  output:
    - Append "## NEXUS_HANDOFF" at end
    - Include all required fields
    - Suggest next agent
    - Specify next action
```

### 3. Handoff Standardization

All handoffs must use standard formats:

```yaml
HANDOFF_REQUIREMENTS:
  naming:
    pattern: "[SENDER]_TO_[RECEIVER]_HANDOFF"
    example: "ARCHITECT_TO_QUILL_HANDOFF"

  content:
    required:
      - Summary of work done
      - Files/artifacts created
      - Key decisions made
      - Risks identified
      - Recommended actions

  format:
    - Markdown structure
# ...
```

---

## Routing Matrix Update

When adding a new agent, update the routing matrix:

### Step 1: Identify Task Types

```yaml
TASK_TYPES:
  # Existing types
  BUG: "bug fix"
  FEATURE: "feature development"
  REFACTOR: "refactoring"
  SECURITY: "security"
  PERF: "performance"
  TEST: "testing"
  DOCS: "documentation"
  INFRA: "infrastructure"

  # New type if needed
  NEW_TYPE: "[Description]"
```

### Step 2: Define Primary Chain

```yaml
ROUTING_ENTRY:
  task_type: "[TASK_TYPE]"
  simple_chain:
    - "[Agent1]"
    - "[NewAgent]"
    - "[Agent2]"
  complex_chain:
    - "[Agent1]"
    - "[Sherpa]"
    - "[NewAgent]"
    - "[Agent2]"
    - "[Agent3]"
  additions:
    - condition: "[Condition]"
      add: "[Agent]"
```

### Step 3: Register Triggers

```yaml
TRIGGER_REGISTRATION:
  keywords:
    - "[keyword1]"
    - "[keyword2]"
    - "[keyword3]"

  patterns:
    - "[pattern with wildcards]"

  negative_patterns:
    - "[patterns that should NOT trigger]"
```

---

## Category Registration

Update the agent category listing:

### Nexus Category Table

```yaml
CATEGORY_UPDATE:
  category: "[Category Name]"
  current_agents:
    - "[Existing Agent 1]"
    - "[Existing Agent 2]"
  add_agent: "[NewAgent]"
  updated_list:
    - "[Existing Agent 1]"
    - "[Existing Agent 2]"
    - "[NewAgent]"
```

### Category Documentation

```markdown
## [Category] ([N+1] agents)

Agents that [category purpose].

### [NewAgent]
- **Role**: [One-line role]
- **Input**: [What it receives]
- **Output**: [What it produces]
- **Trigger**: "[Trigger keywords]"
```

---

## NEXUS_HANDOFF Format

Canonical schema (required/recommended/optional fields, examples, rules) lives in `_common/HANDOFF.md` — do not duplicate it here. Architect emits it per that file's format when input contains `## NEXUS_ROUTING`.

---

## _AGENT_CONTEXT Format

Canonical schema lives in `_common/AUTORUN.md`. Architect's own field mapping example:

```yaml
_AGENT_CONTEXT:
  Role: Architect
  Task: Design new validation agent
  Mode: AUTORUN
  Chain: "User → Architect"
  Input:
    purpose: "Validate user input schemas"
    domain: "Input validation"
    expected_output: "Validation rules, error messages"
  Constraints:
    - Must not overlap with Builder's validation
    - Must integrate with existing error handling
  Expected_Output: "SKILL.md, reference/*.md"
```

---

## _STEP_COMPLETE Format

Architect-specific `Output` schema lives in `reference/autorun-schema.md`; general protocol (mode semantics, error handling) lives in `_common/AUTORUN.md`. Do not duplicate the field list here.

---

## Execution Flow Integration

### Where New Agent Fits

```
USER REQUEST
     ↓
NEXUS (Classify + Chain Select)
     ↓
┌─────────────────────────────────┐
│  AGENT CHAIN EXECUTION          │
│                                 │
│  [Agent1] → [Agent2] → [NewAgent] → [Agent3]
│      ↓         ↓           ↓          ↓
│  HANDOFF   HANDOFF     HANDOFF    HANDOFF
│                                 │
└─────────────────────────────────┘
     ↓
NEXUS (Aggregate + Verify)
     ↓
...
```

### Chain Position Considerations

| Position | Characteristics | Examples |
|----------|-----------------|----------|
| **First** | Investigation, requirements | Scout, Spark |
| **Middle** | Core work, transformation | Builder, Forge |
| **Last** | Validation, documentation | Radar, Quill |
| **Parallel** | Independent work | Multiple Builders |

---

## Guardrail Compatibility

New agents must respect guardrail levels:

```yaml
GUARDRAIL_LEVELS:
  L1: # MONITORING
    trigger: "minor_warning, lint_warning"
    action: "Log only, continue execution"
    agent_response: "Note in artifacts, proceed"

  L2: # CHECKPOINT
    trigger: "test_failure < 20%, security_warning"
    action: "Auto-verify, conditional continue"
    agent_response: "Report failures, suggest fixes"

  L3: # PAUSE
    trigger: "test_failure > 50%, breaking_change"
    action: "Pause, attempt auto-recovery"
    agent_response: "Set status BLOCKED, explain issue"

  L4: # ABORT
    trigger: "critical_security, data_integrity_risk"
    action: "Immediate stop, rollback"
    agent_response: "Set status BLOCKED, escalate to user"
# See nexus/reference/guardrails.md for the canonical definitions.
```

---

## Testing Integration

### Manual Testing

1. **Direct Invocation**
   ```
   /[NewAgent] [test task]
   ```

2. **Nexus Chain**
   ```
   /Nexus [task that includes new agent]
   ## NEXUS_AUTORUN
   ```

3. **Verify Handoffs**
   - Check _STEP_COMPLETE format
   - Check NEXUS_HANDOFF format
   - Verify next agent suggestion

### Integration Checklist

- [ ] Agent responds to direct invocation
- [ ] Agent handles _AGENT_CONTEXT
- [ ] Agent outputs _STEP_COMPLETE
- [ ] Agent outputs NEXUS_HANDOFF in hub mode
- [ ] Agent suggests appropriate next agent
- [ ] Agent handles error cases gracefully
- [ ] Agent respects guardrail levels

---

## Documentation Updates

After integration, update:

1. **README.md**
   - Add to agent catalog table
   - Add usage example

2. **nexus/reference/routing-matrix.md**
   - Update routing matrix
   - Update category list

3. **nexus/reference/agent-chains.md**
   - Add new chain templates
   - Update existing chains if affected

---

## Rollback Procedure

If new agent causes issues:

1. **Immediate**: Remove from routing matrix
2. **Temporary**: Add to skip list
3. **Permanent**: Delete SKILL.md and references

```yaml
ROLLBACK_STEPS:
  - Remove from nexus routing matrix
  - Update category tables
  - Remove from README catalog
  - Archive SKILL.md (don't delete immediately)
  - Notify users of deprecation
```
