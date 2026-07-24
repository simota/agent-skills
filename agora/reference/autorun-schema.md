# Agora — AUTORUN `_STEP_COMPLETE` Schema

When Agora receives `_AGENT_CONTEXT`, parse `task_type`, `description`, and `Constraints`, execute the standard workflow (skip verbose explanations, focus on deliverables), and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Agora
  Task_Type: CURRICULUM | OBJECTIVES | LESSONS | ASSESSMENT | PROGRESS | INSTRUCTOR | ALIGN
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact]
    objective_count: <int>
    blooms_distribution: {Remember: <int>, Understand: <int>, Apply: <int>, Analyze: <int>, Evaluate: <int>, Create: <int>}
    alignment_gaps: <int>
    mvp_vs_stretch: "[separated | n/a]"
  Validations:
    alignment_matrix: "[complete | partial | skipped]"
    measurable_objectives: "[passed | flagged]"
  Next: [Scribe | Matrix | Canvas | Morph | DONE]
  Reason: [Why this next step]
```
