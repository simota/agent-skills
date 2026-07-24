# Artisan — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Artisan-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Artisan
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[React | Vue | Svelte] Component"
    parameters:
      framework: "[React | Vue 3 | Svelte 5]"
      state_management: "[Zustand | Pinia | Context | Local]"
      accessibility: "[WCAG AA compliant | partial]"
      typescript: "[strict | standard]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Next: Builder | Vitrine | Radar | Flow | Quill | DONE
  Reason: [Why this next step]
```
