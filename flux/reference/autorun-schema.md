# Flux — AUTORUN `_STEP_COMPLETE` Schema

When Flux receives `_AGENT_CONTEXT`, parse `task_type`, `description`, `problem_statement`, `constraints`, `work_mode`, and `Constraints`, choose the correct work mode, run the pipeline, and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Flux
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [reframing package path or inline]
    artifact_type: "[Reframing Package | Assumption Map | Perspective Shift Report | Cross-Domain Insight | Tri-Engine Reframe Portfolio]"
    parameters:
      cynefin_domain: "[Clear | Complicated | Complex | Chaotic | Disorder]"
      work_mode: "[DEEP | RAPID | LENS]"
      frameworks_applied: "[list of frameworks used]"
      reframed_statements_count: "[3-5]"
      blind_spots_detected: "[count]"
      serendipity_injections: "[count]"
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]
      engines_failed: [list or none]
      merge_strategy: "[Portfolio | Compete]"   # Portfolio is the default for Flux
      concurrence_distribution:
        UNIVERSAL: [count]
        LIKELY: [count]
        VERIFIED-DIVERGENT: [count]
      novelty_distribution:
        HIGH: [count]
        MEDIUM: [count]
      top_billed_divergent: [count of VERIFIED-DIVERGENT × HIGH reframes promoted to top section]
      assumption_roots: [count of distinct original_assumptions surfaced across engines]
      rejected: [count + top categories — ASN-fail / hallucinated-domain / synonym-substitution / bias-inherited]
  Handoff:
    Format: FLUX_TO_[NEXT]_HANDOFF
    Content: [Full handoff content]
  Artifacts:
    - [Reframed problem statements]
    - [Insight Matrix]
    - [Blind Spot Report]
  Risks:
    - [Risk 1]
  Next: Magi | Spark | Magi | Atlas | Lore | DONE
  Reason: [Why this next step]
```
