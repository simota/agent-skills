# Canvas — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Canvas-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Canvas
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Mermaid | draw.io | ASCII] Diagram"
    parameters:
      diagram_type: "[flowchart | sequence | class | ER | state | C4 | diff | journey | etc.]"
      mode: "[Standard | Reverse | C4 | Diff | Echo | Library]"
      node_count: "[number]"
      format: "[Mermaid | draw.io | ASCII]"
  Next: Quill | Atlas | Sherpa | DONE
  Reason: [Why this next step]
```
