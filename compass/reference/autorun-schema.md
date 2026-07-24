# Compass — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Compass-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Compass
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [recommended agents or catalog]
    artifact_type: "recommendation | catalog | comparison | onboarding"
    parameters:
      recommended_agents: "[agent1, agent2]"
      confidence: "high | medium | low"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Next: [Nexus | Architect] | DONE
  Reason: [Why this next step]
```
