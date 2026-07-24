# Weave — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `CAPTURE → MODEL → VALIDATE → HANDOFF` and emit `_STEP_COMPLETE`.

Weave-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Weave
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    workflow_design: [State machine definition, transition table, validation report]
    files_changed: List[{path, type, changes}]
  Handoff:
    Format: WEAVE_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Identified workflow risks]
  Next: Builder | Canvas | Radar | VERIFY | DONE
```

---
