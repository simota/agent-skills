# Nest — AUTORUN `_STEP_COMPLETE` Schema

```yaml
_STEP_COMPLETE:
  Agent: Nest
  Task_Type: AUDIT | RESTRUCTURE | CLAUDE_HIERARCHY | NAMING | GREENFIELD
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output: <summary of deliverables>
  Metrics:
    token_cost_before: <estimated tokens>
    token_cost_after: <estimated tokens>
    discovery_score: <0-100>
    cache_topology_score: <0-100>
  Handoff: <next agent if applicable>
  Next: <suggested follow-up action>
  Reason: <why this outcome>
```
