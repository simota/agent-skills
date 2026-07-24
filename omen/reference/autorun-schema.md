# Omen — AUTORUN `_STEP_COMPLETE` Schema

Parse `_AGENT_CONTEXT` from the orchestrator to determine analysis scope, target system, and work mode. If `_AGENT_CONTEXT` specifies a LENS domain, restrict analysis to that domain.

```yaml
_STEP_COMPLETE:
  Agent: Omen
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [pre-mortem report / FMEA table]
    parameters:
      work_mode: "[DEEP | RAPID | LENS]"
      failure_modes_count: "[count]"
      critical_rpn_count: "[RPN > 200 or AP=H count]"
      max_rpn: "[highest RPN]"
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]
      engines_failed: [list or none]
      pattern_type: "D"                          # Divergence-primary
      concurrence_distribution:
        UNIVERSAL: [count]
        LIKELY: [count]
        VERIFIED-DIVERGENT: [count]
      severity_9_clusters: [count]               # CRITICAL gate triggers
      composite_priority_top_N:                  # top N clusters by concurrence_weight × RPN
        - cluster_id: "FM-NNN"
          engine_concurrence: "[codex+agy+claude] | [codex+agy] | [codex-verified] | ..."
          composite_priority: "[number]"
          rpn_max: "[number]"
          rpn_variance: "[max-min across engines, calibration disagreement signal]"
          severity_critical: "[true if any S≥9 in cluster, else false]"
      divergent_spotlight:                       # VERIFIED-DIVERGENT modes that survived grounding
        - cluster_id: "FM-NNN"
          surfaced_by: "codex | agy | claude"
          blindspot_class: "[failure class the other engines structurally missed]"
      rejected: [count + top categories — hallucination / implausible / already-mitigated / out-of-scope]
  Next: [Ripple | Magi | Triage | Beacon | Radar | Sentinel | DONE]
  Reason: [Why this next step]
```
