# Ascent — AUTORUN `_STEP_COMPLETE` Schema

When Ascent receives `_AGENT_CONTEXT`, parse `task_type`, `description`, and `Constraints`, execute the standard workflow (skip verbose explanations, focus on deliverables), and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Ascent
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact or path]
    recipe: "[direction | self | market | learn | jobsearch | package]"
    parameters:
      route: "[recommended career route]"
      target_role: "[target role / work-style]"
      region: "[region / work mode]"
  Validations:
    grounding: "[grounded in user experience | assumptions flagged]"
    sources: "[market/salary claims cited | none required]"
    consistency: "[cross-artifact check passed | partial]"
  Next: Crest | Scribe | Prose | Canvas | DONE
  Reason: [Why this next step]
```
