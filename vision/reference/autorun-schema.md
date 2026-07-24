# Vision — AUTORUN `_STEP_COMPLETE` Schema

When Vision receives `_AGENT_CONTEXT`, parse `task_type`, `description`, and `Constraints`, execute the standard workflow, and return `_STEP_COMPLETE`.

The `pair` recipe is INTERACTIVE and cannot run unattended — under AUTORUN, run UNDERSTAND, draft the ordered decision plan + the first decision's options, and set `Next: USER` (pair-ready) rather than locking decisions without confirmation.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Vision
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact]
    parameters:
      task_type: "[task type]"
      scope: "[scope]"
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]
      engines_failed: [list or none]
      merge_strategy: "[Portfolio | Compete]"
      concurrence_distribution:
        UNIVERSAL: [count]
        LIKELY: [count]
        VERIFIED-DIVERGENT: [count]
      spectrum_coverage:
        positions: [list of distinct spectrum_position values across surviving directions]
        spread_ok: [true | false]
      rejected: [count + top categories — brand-drift / persona-mismatch / a11y / hallucination / vague-outcome / ai-trust]
      lead_recommendation: "[direction concept_name]"
      challenger: "[direction concept_name or none]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Next: [recommended next agent or DONE]
  Reason: [Why this next step]
```
