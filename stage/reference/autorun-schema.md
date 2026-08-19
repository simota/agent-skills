# Stage — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Stage-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Stage
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    framework: "[Marp | reveal.js | Slidev]"
    parameters:
      slide_count: [N]
      duration: "[estimated total time]"
      narrative_pattern: "[Problem-Solution | AIDA | Before-After | Hero's Journey | Tutorial]"
      audience: "[beginner | intermediate | expert]"
    preview_command: "[command to preview]"
  Next: Cue | DONE
  Reason: [Why this next step]
```
