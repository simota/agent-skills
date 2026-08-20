# Compete — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Compete-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Compete
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Landscape | Benchmark | SWOT | Win/Loss | Battle Card | Strategy | Calibration | Tri-Engine Matrix | Tri-Engine Battle Card | Tri-Engine Positioning | Tri-Engine Landscape]"
    parameters:
      analysis_shape: "[landscape | benchmark | response | win_loss | strategy | calibration | multi]"
      competitor_count: "[number]"
      confidence: "[high | medium | low]"
      sources_cited: "[number]"
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]
      engines_failed: [list or none]
      artifact_merged_into: "[Feature Matrix | Battle Card | Positioning Map | SWOT | Landscape | LLM Visibility | Win/Loss]"
      coverage_distribution:
        UNIVERSAL: [count]
        LIKELY: [count]
        VERIFIED-DIVERGENT: [count]
      uncommon_competitors: [count of VERIFIED-DIVERGENT competitors surfaced in callout]
      rejected: [count + top categories — hallucination / defunct / category-mismatch / out-of-scope / alias-fold]
  Handoff: "[target agent or N/A]"
  Next: Spark | Growth | Canvas | Magi | Lore | Field | DONE
  Reason: [Why this next step]
```
