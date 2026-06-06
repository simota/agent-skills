# Gear: Nexus Integration Templates

## AUTORUN Input Context (from Nexus)

```yaml
_AGENT_CONTEXT:
  Role: Gear
  Task: "[from Nexus]"
  Mode: "AUTORUN"
  Chain:
    Previous: "[previous agent or null]"
    Position: "[step X of Y]"
    Next_Expected: "[next agent or DONE]"
  History:
    - Agent: "[previous agent]"
      Summary: "[what they did]"
  Constraints:
    Area: "[Dependencies / CI/CD / Docker / Observability / Monorepo]"
    Scope: "[specific files or packages]"
    Risk_Tolerance: "[low / medium / high]"
  Expected_Output:
    - Configuration changes
    - Build verification results
    - Handoff data for next agent
```

## AUTORUN Output Format (to Nexus)

```yaml
_STEP_COMPLETE:
  Agent: Gear
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    area: "[Dependencies / CI/CD / Docker / Observability / Monorepo]"
    action: "[What was done]"
    files_changed:
      - "[file path]"
    verification:
      build: "[pass/fail]"
      tests: "[pass/fail]"
      lint: "[pass/fail]"
    risk_level: "[Low / Medium / High]"
  Artifacts:
    - "[List of created/modified files]"
  Risks:
    - "[Potential issues or side effects]"
  Next: Radar | Shift | Sentinel | Launch | VERIFY | DONE
  Reason: "[Why this next step]"
```

## Nexus Hub Mode (NEXUS_HANDOFF)

When user input contains `## NEXUS_ROUTING`, return results via this format:

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: Gear
- Summary: 1-3 lines
- Key findings / decisions:
  - Area: [Dependencies / CI/CD / Docker / Observability / Monorepo]
  - Action: [What was done]
  - Risk: [Low / Medium / High]
- Artifacts (files/commands/links):
  - [Changed files]
  - [Verification results]
- Risks / trade-offs:
  - [Potential issues]
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name if any]
  - Question: [Question for user]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] -> A: [User's answer]
- Open questions (blocking/non-blocking):
  - [Clarifications needed]
- Suggested next agent: [AgentName] (reason)
- Next action: Paste this response to Nexus
```
