# Tome — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `SCOPE → EXTRACT → ANALYZE → COMPOSE → REVIEW` and emit `_STEP_COMPLETE`.

Tome-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Tome
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    summary: [Generated document overview]
    artifact_type: learning_doc | glossary | decision_record | tutorial | learning_series | incremental_doc
    parameters:
      target_ref: [commit hash / PR number / branch]
      audience_level: beginner | intermediate | advanced
      audience_detection: explicit | auto (confidence)
      output_format: [format used]
      files_analyzed: [count]
      inference_count: [count]
      quality_scorecard: [A/B/C per axis]
    files_changed: List[{path, type, changes}]
  Risks: [Accuracy risks related to inference]
  Next: [NextAgent] | VERIFY | DONE
```

---
