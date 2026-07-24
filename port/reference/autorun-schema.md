# Port — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). Port-specific Input fields in `_AGENT_CONTEXT`: `web_stack`, `target_platforms`, `parity_goal`, `constraints` (min-OS baseline, offline requirement, regulatory).

Port-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Port
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [blueprint path or inline]
    artifact_type: Blueprint | Survey | Parity Matrix | Architecture Map | Roadmap | Risk Matrix
    parameters:
      web_stack: [detected stack]
      target_platforms: ["iOS", "Android"]
      parity_summary: "Full=N Adapted=N Deferred=N Dropped=N"
      offline_tier_default: T0 | T1 | T2 | T3
      phase_count: [N phases]
      ios_min: [iOS NN]
      android_min: [API NN]
  Validations:
    completeness: complete | partial | blocked
    quality_check: passed | flagged | skipped
  Handoffs:
    - target: Native;    content: [per-platform implementation spec ref]
    - target: Scaffold;  content: [project skeleton spec ref]
    - target: Gateway;   content: [mobile API contract spec ref]
  Risks: [High-impact risk and mitigation]
  Next: Native | Scaffold | Gateway | Schema | Launch | DONE
```
