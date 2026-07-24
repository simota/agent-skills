# Spark — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Spark-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Spark
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Feature Proposal | Opportunity Memo | Prioritization Report | Competitive Gap Spec | Tri-Engine Portfolio | Tri-Engine Compete-Merged RFC]"
    parameters:
      feature_name: "[proposed feature name]"
      target_persona: "[persona name]"
      rice_score: "[calculated score]"
      impact_effort: "[Quick Win | Big Bet | Fill-In | Time Sink]"
      validation_strategy: "[experiment type or validation method]"
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]
      engines_failed: [list or none]
      merge_strategy: "[Portfolio | Compete]"
      concurrence_distribution:
        UNIVERSAL: [count]
        LIKELY: [count]
        VERIFIED-DIVERGENT: [count]
      rejected: [count + top categories — duplicate / hallucination / persona-mismatch / vague-hypothesis]
  Validations:
    - "[persona and JTBD defined]"
    - "[RICE score calculated with assumptions]"
    - "[acceptance criteria specified]"
    - "[no duplication with existing features]"
  Next: Scribe | Builder | Artisan | Forge | Experiment | DONE
  Reason: [Why this next step]
```
