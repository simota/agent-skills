# Trawl — AUTORUN `_STEP_COMPLETE` Schema

When `_AGENT_CONTEXT` is present in the input, parse the following fields:

```yaml
_AGENT_CONTEXT:
  Role: Trawl
  Task: <delegated task description>
  Context: <handoff data from previous step>
  Constraints: <boundaries and requirements>
  Expected_Output: <format and content expected>
```

Execute the appropriate design flow, skip verbose explanation, and emit:

```yaml
_STEP_COMPLETE:
  Agent: Trawl
  Task_Type: ARCHITECTURE | FRONTIER | SCHEDULER | COMPLIANCE | EXTRACTION | OBSERVABILITY | LINK_GRAPH
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output: <summary of deliverables>
  Handoff: <next agent if applicable>
  Next: <suggested follow-up action>
  Reason: <why this outcome>
```
