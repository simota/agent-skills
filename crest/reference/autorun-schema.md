# Crest — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Crest-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Crest
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    mode: "[AUDIT | POSITION | PROFILE | NARRATIVE | STRATEGY | CONTENT | VISIBILITY | AI-ERA]"
    parameters:
      niche: "[identified micro-niche]"
      channels: "[target channels]"
      anti_pattern_check: "[AP-1~AP-11 results]"
    files_changed:
      - path: [file path]
        type: [created / modified]
        changes: [brief description]
  Handoff:
    Format: CREST_TO_[NEXT]_HANDOFF
    Content: [Full handoff content for next agent]
  Next: Saga | Prose | Growth | Canvas | DONE
  Reason: [Why this next step]
```
