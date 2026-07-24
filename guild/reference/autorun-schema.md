# Guild — AUTORUN `_STEP_COMPLETE` Schema

When Guild receives `_AGENT_CONTEXT`, parse `task_type`, `description`, and `Constraints`, execute the standard workflow (skip verbose explanations, focus on deliverables), and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Guild
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact]
    artifact_type: "[Hiring Strategy | Job Description | Competency Matrix | Interview Rubric | Scorecard | Onboarding Plan | Performance Review | Culture Doc | Hiring Risk / Bias Checklist | Hiring Package]"
    parameters:
      role_id: "[R-001]"
      seniority: "[level]"
      employment_type: "[full-time | contractor | part-time | intern]"
  Validations:
    artifact_consistency: "[passed | flagged]"
    labor_law_review_flagged: "[yes | n/a]"
  Next: [Oath | Scribe | Prose | Cast] | DONE
  Reason: [Why this next step]
```
