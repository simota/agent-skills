# Voice — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Voice-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Voice
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact]
    artifact_type: "[NPS Report | CSAT Report | CES Report | Exit Survey Report | Multi-Channel Report | Feedback Analysis]"
    parameters:
      task_type: "[task type]"
      scope: "[scope]"
      survey_type: "[NPS | CSAT | CES | Exit | Multi-Channel | Widget]"
      channels_analyzed: "[list of channels]"
      sample_size: "[number of responses or signals]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Next: [recommended next agent or DONE]
  Reason: [Why this next step]
```
