# Reverse Feedback Protocol

Standard protocol for downstream-to-upstream feedback between agents. This enables a self-correcting ecosystem where quality issues flow back to the agent best positioned to fix them.

---

## Overview

In normal workflow, agents pass deliverables downstream (e.g., Builder → Radar → Judge). Reverse feedback flows the opposite direction: a downstream agent reports an issue back to the upstream agent whose output caused the problem.

```
Normal flow:     Builder ──code──→ Radar ──tests──→ Judge
Reverse flow:    Builder ←──untestable code──← Radar
```

---

## When to Trigger Reverse Feedback

| Condition | Example | Priority |
|-----------|---------|----------|
| Upstream output has quality defects | Palette finds a11y issues in Muse's tokens | high |
| Upstream assumption was incorrect | Builder finds Scout's RCA was wrong | high |
| Upstream deliverable is incomplete | Radar can't test because Builder left gaps | medium |
| Upstream pattern is inconsistent | Judge finds naming violations in SKILL.md | medium |
| Upstream approach could be improved | Zen suggests better patterns for Builder | low |

---

## Standard Reverse Feedback Format

All reverse feedback between agents must use this template:

```yaml
REVERSE_FEEDBACK:
  Source_Agent: "[Agent reporting the issue]"
  Target_Agent: "[Agent whose output has the issue]"
  Feedback_Type: quality_issue | incorrect_output | incomplete_deliverable | pattern_inconsistency | improvement_suggestion
  Priority: high | medium | low
  Context:
    original_task: "[What the source agent was working on]"
    discovery: "[How the issue was found during source agent's work]"
  Issue:
    description: "[Clear, specific description of the problem]"
    evidence:
      - file: "[File path]"
        line: "[Line number or range]"
        detail: "[What's wrong here]"
    impact: "[What breaks or degrades because of this issue]"
  Suggested_Action:
    action: "[Specific fix the target agent should perform]"
    urgency: immediate | next_cycle | backlog
  Resolution_Expected:
    format: "[What the fix deliverable should look like]"
    notify_on_completion: true
```

---

## Priority Handling

| Priority | Response Time | Action | Guardrail Level |
|----------|--------------|--------|-----------------|
| **high** | Immediate | Fix in current session, notify source agent | L2 (Checkpoint) |
| **medium** | Next cycle | Add to improvement queue, fix in next session | L1 (Monitoring) |
| **low** | Backlog | Document for next ecosystem-wide review | L1 (Monitoring) |

---

## Common Reverse Feedback Scenarios

### Quality Issues (downstream discovers defect in upstream output)

| Source → Target | Scenario | Priority |
|-----------------|----------|----------|
| Palette → Muse | Contrast failure in design tokens | high |
| Radar → Builder | Untestable code structure (tight coupling, no DI) | high |
| Judge → Architect | SKILL.md structural or content issues | medium |
| Sentinel → Builder | Security vulnerability in implementation | high |
| Voyager → Artisan | E2E failure due to component defects | high |
| Flow → Muse | Motion token doesn't match animation needs | medium |
| Vitrine → Muse | Hardcoded values discovered in component stories | medium |
| Warden → Vision | V.A.I.R.E. quality standard violation in design | high |
| Canon → Gateway | API spec violates OpenAPI/REST standards | medium |

### Incorrect Output (downstream proves upstream conclusion was wrong)

| Source → Target | Scenario | Priority |
|-----------------|----------|----------|
| Builder → Scout | Root cause analysis was incorrect | high |
| Artisan → Forge | Prototype has incompatible architecture | medium |
| Radar → Scout | Bug reproduction steps don't reproduce | high |
| Voyager → Radar | Unit test passes but E2E reveals real bug | medium |

### Incomplete Deliverable (downstream cannot proceed)

| Source → Target | Scenario | Priority |
|-----------------|----------|----------|
| Radar → Builder | Missing edge case handling prevents testing | medium |
| Guardian → Builder | Uncommittable code (lint/type failures) | high |
| Voyager → Builder | Missing API endpoints for E2E flow | high |
| Artisan → Forge | Prototype missing critical interaction patterns | medium |
| Gear → Builder | Build fails due to missing dependencies | high |

---

## Processing Workflow

When an agent receives reverse feedback:

```
1. RECEIVE    → Parse feedback template, identify priority and source
2. VALIDATE   → Confirm the reported issue is reproducible
3. ASSESS     → Determine scope (isolated issue vs systemic pattern)
4. ACT        → Fix the issue or propose alternative approach
5. NOTIFY     → Inform source agent of resolution via handoff
6. PREVENT    → Update process/checks to prevent recurrence
```

### Decision Tree

```
RECEIVE feedback
  │
  ├─ Priority: high
  │   └─ VALIDATE → ACT immediately → NOTIFY source
  │
  ├─ Priority: medium
  │   └─ VALIDATE → Queue for next cycle → NOTIFY when fixed
  │
  └─ Priority: low
      └─ Log → Schedule for review
```

---

## Recording in Handoffs

### In NEXUS_HANDOFF (reporting feedback to Nexus)

```yaml
Reverse_Feedback_Sent:
  - target: "[Target agent name]"
    type: "[Feedback type]"
    priority: "[high | medium | low]"
    issue: "[Brief one-line description]"

Reverse_Feedback_Received:
  - source: "[Source agent name]"
    type: "[Feedback type]"
    priority: "[high | medium | low]"
    status: "[resolved | pending | deferred]"
    action_taken: "[Brief description of fix]"
```

### In _STEP_COMPLETE (AUTORUN mode)

```yaml
_STEP_COMPLETE:
  Agent: [AgentName]
  Status: SUCCESS
  Output: [Results]
  Feedback_Sent: [count of reverse feedback items sent]
  Feedback_Resolved: [count of reverse feedback items resolved]
  Next: [NextAgent]
```

---

## Integration with Existing Protocols

### With INTERACTION.md

Add `ON_REVERSE_FEEDBACK` as an INTERACTION_TRIGGER:

```yaml
ON_REVERSE_FEEDBACK:
  timing: ON_RECEIVE
  template:
    questions:
      - question: "Downstream agent reported an issue. How to handle?"
        header: "Feedback"
        options:
          - label: "Fix immediately (Recommended)"
            description: "Address the reported issue now"
          - label: "Schedule for next cycle"
            description: "Add to improvement queue"
          - label: "Reject with reason"
            description: "Provide explanation why feedback is not applicable"
        multiSelect: false
```

### With AUTORUN.md (Guardrail Protocol)

- High priority reverse feedback triggers **L2 checkpoint** (auto-fix attempt per the Guardrail Protocol section in `_common/AUTORUN.md`)
- Systemic issues (3+ feedback items on same pattern) trigger **L3 pause**

### With AUTORUN.md (Execution Modes)

- In **AUTORUN_FULL** mode: high priority feedback is auto-processed
- In **GUIDED** mode: user confirms feedback handling approach
- In **INTERACTIVE** mode: user approves each feedback response

---

## Agent Implementation Checklist

To fully support reverse feedback, agents should have:

1. **CAPABILITIES_SUMMARY**: Include `reverse_feedback_processing` capability
2. **INTERACTION_TRIGGERS**: Add `ON_REVERSE_FEEDBACK` trigger with YAML template
3. **Handoff formats**: Add receiving templates for feedback from known partners
4. **Daily process**: Include "Check for pending reverse feedback" step
5. **COLLABORATION_PATTERNS**: List reverse feedback flows with `(reverse feedback)` annotation

Agents that reference this pattern: **Architect**, **Muse** (adoption is limited; protocol is available for all agents to use via standard handoff flows)
