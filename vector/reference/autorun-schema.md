# Vector — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Vector-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Vector
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [report path or inline]
    artifact_type: "[Execution Log | Data Collection | Form Submission | Screenshot Package | Video Recording | HAR Export | Bug Reproduction]"
    parameters:
      target_url: "[URL]"
      steps_completed: "[count]"
      screenshots: "[count]"
      data_collected: "[format and count]"
      errors_detected: "[console/network error count]"
  Next: Triage | Builder | Lens | Bolt | Echo | DONE
  Reason: [Why this next step]
```
