# Frame — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Frame-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Frame
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [handoff package path or inline]
    artifact_type: "[Design Context | Token Map | Code Connect Report | Design System Rules | Screenshot Package | FigJam Package | Full Handoff]"
    parameters:
      figma_url: "[source file URL]"
      file_version: "[version hash]"
      scope: "[page/frame/component path]"
      extraction_type: "[component | token | screenshot | code_connect | design_system | figjam | full]"
      target_agent: "[Muse | Forge | Artisan | Builder | Schema | Canvas | Vision | Vitrine]"
      rate_budget: "[consumed/remaining]"
      code_connect_status: "[mapped | missing | stale]"
      w3c_dtcg_aligned: "[yes | no | partial]"
    completeness_check: "[passed | flagged: [gaps]]"
    stale_mappings: "[none | [component names]]"
  Next: Muse | Forge | Artisan | Builder | Schema | Canvas | Vision | Vitrine | DONE
  Reason: [Why this next step]
```
