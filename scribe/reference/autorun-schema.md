# Scribe — AUTORUN `_STEP_COMPLETE` Schema

When Scribe receives `_AGENT_CONTEXT`, parse `task_type`, `description`, and `Constraints`, execute the standard workflow, and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Scribe
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact]
    parameters:
      task_type: "[task type]"
      scope: "[scope]"
      artifact_type: "[PRD | SRS | HLD | LLD | Checklist | Test Spec | Agent Spec | Full | Standard | Lite Unified Specification Package]"
      teams: ["[audience/team]"]
      requirement_count: "[number or N/A]"
      traceability_completeness: "[percentage or N/A]"
      bdd_scenario_count: "[number or N/A]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Handoff: "[target agent or N/A]"
  Next: Sherpa | Builder | Artisan | Radar | Voyager | Judge | Canvas | Scribe | Lore | PDM | DONE
  Reason: [Why this next step]
```
