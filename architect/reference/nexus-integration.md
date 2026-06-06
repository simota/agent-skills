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

### Required Fields

```yaml
NEXUS_HANDOFF_FIELDS:
  required:
    - Step: "[X/Y]"                    # Current step / total steps
    - Agent: "[AgentName]"             # This agent's name
    - Summary: "[1-3 lines]"           # What was done
    - "Key findings / decisions"       # List of key items
    - "Artifacts"                      # Files, links, commands
    - "Risks / trade-offs"             # Identified risks
    - "Open questions"                 # Blocking/non-blocking
    - "Suggested next agent"           # With reason
    - "Next action"                    # CONTINUE/VERIFY/DONE

  conditional:
    - "Pending Confirmations"          # If user input needed
    - "User Confirmations"             # If user responded
```

### Format Template

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: [AgentName]
- Summary: [1-3 lines describing outcome]
- Key findings / decisions:
  - [Finding 1]
  - [Finding 2]
  - [Decision 1]
- Artifacts (files/commands/links):
  - [Artifact 1]
  - [Artifact 2]
- Risks / trade-offs:
  - [Risk 1]
  - [Trade-off 1]
- Open questions (blocking/non-blocking):
// ...
```

---

## _AGENT_CONTEXT Format

### Required Fields

```yaml
_AGENT_CONTEXT:
  Role: "[AgentName]"           # Agent being invoked
  Task: "[Specific task]"       # What to do
  Mode: "AUTORUN"               # Execution mode
  Chain: "[Previous agents]"    # Context of chain
  Input: "[Handoff content]"    # From previous agent
  Constraints:
    - "[Constraint 1]"
    - "[Constraint 2]"
  Expected_Output: "[What Nexus expects]"
```

### Example

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

### Required Fields

```yaml
_STEP_COMPLETE:
  Agent: "[AgentName]"
  Status: "SUCCESS | PARTIAL | BLOCKED | FAILED"
  Output:
    [key]: "[value]"
    files_changed:
      - path: "[path]"
        type: "[created/modified/deleted]"
        changes: "[description]"
  Handoff:
    Format: "[SENDER]_TO_[RECEIVER]_HANDOFF"
    Content: "[Full handoff content]"
  Artifacts:
    - "[Artifact 1]"
  Risks:
# ...
```

### Status Definitions

| Status | Meaning | Next Action |
|--------|---------|-------------|
| SUCCESS | Task completed fully | Proceed to next agent |
| PARTIAL | Task partially done | May need retry or skip |
| BLOCKED | Cannot proceed | Needs user input or different agent |
| FAILED | Task failed | Error recovery or abort |

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
  L1:
    trigger: "lint_warning"
    action: "Log, continue"
    agent_response: "Note in artifacts, proceed"

  L2:
    trigger: "test_failure < 20%"
    action: "Auto-verify, conditional continue"
    agent_response: "Report failures, suggest fixes"

  L3:
    trigger: "test_failure > 50%, breaking_change"
    action: "Pause, auto-recover"
    agent_response: "Set status BLOCKED, explain issue"
# ...
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

2. **nexus/SKILL.md**
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
