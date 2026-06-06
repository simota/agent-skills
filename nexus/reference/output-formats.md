# Nexus Output Formats Reference

**Purpose:** Canonical final output and handoff templates.
**Read when:** You need exact `NEXUS_COMPLETE`, handoff, or report formatting.

## Contents
- NEXUS_COMPLETE (AUTORUN)
- NEXUS_COMPLETE_FULL (AUTORUN_FULL)
- NEXUS_HANDOFF_V2 (Standard - Required)
- NEXUS_HANDOFF (Legacy - Deprecated)
- NEXUS_HANDOFF (Extended - AUTORUN_FULL)
- _STEP_COMPLETE Format

Final output formats and handoff protocols.

---

## NEXUS_COMPLETE (AUTORUN)

```
## NEXUS_COMPLETE
Task: [Task name]
Type: [BUG|FEATURE|REFACTOR|...]
Chain: [Executed chain]

### Changes
- [File1]: [Change description]
- [File2]: [Change description]

### Verification
- Tests: [PASS/FAIL + details]
- Build: [status]

### How to Verify
1. [Verification step 1]
2. [Verification step 2]

### Risks / Follow-ups
- [Remaining risks]
- [Recommended follow-ups]
```

---

## NEXUS_COMPLETE_FULL (AUTORUN_FULL)

```
## NEXUS_COMPLETE_FULL
Task: [Task name]
Type: [BUG|FEATURE|REFACTOR|...]
Mode: AUTORUN_FULL
Complexity: [SIMPLE|MEDIUM|COMPLEX]

### Execution Summary
- Total Steps: [N]
- Parallel Branches: [N branches if any]
- Duration: [Phases completed]
- Recovery Actions: [N if any]

### Chain Executed
Sequential: [Agent1] → [Agent2] → [Agent3]
Parallel (if any):
  Branch A: [Agent4] → [Agent5]
  Branch B: [Agent6] → [Agent7]
  Merge: [Agent8]

### Changes
- [File1]: [Change description]

### Guardrail Events
| Step | Level | Trigger | Action | Result |
|------|-------|---------|--------|--------|
| 3/7 | L2 | test_failure | auto_fix | SUCCESS |

### Verification
- Tests: [PASS/FAIL + details]
- Build: [status]
- Security: [Sentinel result if applicable]
- Final Guardrail: [L2 CHECKPOINT result]

### Context Summary
- Goal: [Original goal]
- Acceptance: [All criteria met / Partial]
- Key Decisions: [List of major decisions made]

### How to Verify
1. [Verification step 1]
2. [Verification step 2]

### Risks / Follow-ups
- [Remaining risks]
- [Recommended follow-ups]

### Rollback (if needed)
- Rollback available: [Yes/No]
- Command: [git checkout / restore command]
```

---

## NEXUS_HANDOFF_V2 (Standard - Required)

All agents MUST use V2 format with confidence scoring.

**Compliance Levels:** Level 1 (Minimal) requires only `step`, `agent`, `status`, `summary`, `next_agent`, `next_action` — confidence is inferred from status (see `handoff-validation.md` Compliance Levels). Level 2 adds `confidence` as a single number. Level 3 (Full/Claude default) adds `confidence_breakdown` with 3 axes.

```yaml
## NEXUS_HANDOFF
step: [X/Y]
agent: [AgentName]
status: [SUCCESS|PARTIAL|BLOCKED|FAILED]

# REQUIRED: Confidence scoring for auto-routing
confidence: 0.XX  # Overall score (0.0-1.0)
confidence_breakdown:
  task_completion: 0.XX   # How complete is the work
  output_quality: 0.XX    # Quality of artifacts produced
  next_step_clarity: 0.XX # How clear is the next step

summary: |
  [1-3 line summary of work completed]

key_findings:
  - [Finding 1]
  - [Finding 2]

artifacts:
  - type: [file|command|link]
    path: [path]
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

user_confirmations:
  - question: [Previous Q]
    answer: [User's A]

next_agent: [AgentName|DONE]
next_action: [CONTINUE|MERGE|VERIFY|ESCALATE|ABORT]
reason: [Why this next step]
```

### Auto-Routing Rules

| Confidence | Status | Action |
|------------|--------|--------|
| >= 0.75 | SUCCESS | Auto-route to next_agent |
| 0.50-0.74 | SUCCESS/PARTIAL | Route with logged assumptions |
| < 0.50 | any | Pause for user input |
| any | BLOCKED | Present pending_confirmations |
| any | FAILED | Execute recovery chain or escalate |

See `reference/handoff-validation.md` for full validation rules.

---

## NEXUS_HANDOFF (Legacy - Deprecated)

```
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: [AgentName]
- Summary: 1-3 lines
- Key findings / decisions:
  - ...
- Artifacts (files/commands/links):
  - ...
- Risks / trade-offs:
  - ...
- Open questions (blocking/non-blocking):
  - ...
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name]
  - Question: [Question]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] → A: [User's answer]
- Suggested next agent: [AgentName] (reason)
- Next action: CONTINUE
```

**Note**: Legacy format will be auto-migrated to V2 with inferred confidence.
See `handoff-validation.md` for migration rules.

---

## NEXUS_HANDOFF (Extended - AUTORUN_FULL)

```
## NEXUS_HANDOFF
- Step: [X/Y]
- Branch: [branch_id or "main"]
- Agent: [AgentName]
- Summary: 1-3 lines
- Key findings / decisions:
  - ...
- Artifacts (files/commands/links):
  - ...
- Files Modified: [List of files]
- Risks / trade-offs:
  - ...
- Guardrail Events:
  - Level: [L1|L2|L3|L4 or "none"]
  - Trigger: [What triggered if any]
  - Action: [Action taken]
  - Result: [SUCCESS|FAILED|ESCALATED]
- Context Delta:
  - Added: [New knowledge/artifacts]
  - Changed: [Modified state]
- Suggested next agent: [AgentName]
- Next action: [CONTINUE|MERGE|VERIFY|ESCALATE|ABORT]
```

---

## _STEP_COMPLETE Format

```
_STEP_COMPLETE:
  Agent: [Name]
  Branch: [branch_id if parallel, else "main"]
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    type: [Output type]
    summary: [Brief summary]
    files_changed: [List if applicable]
  Handoff:
    Format: [AGENT_TO_AGENT_HANDOFF format]
    Content: [Full handoff for next agent]
  Artifacts:
    - [List of produced artifacts]
  Next: [NextAgent] | VERIFY | DONE
  Reason: [Why this next step]
```
