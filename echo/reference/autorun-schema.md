# Echo — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Echo-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Echo
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Emotion Journey | Dark Pattern Audit | Cross-Persona Analysis | Visual Review | Accessibility Audit | Latent Needs Report | Tri-Engine Persona × Step Matrix]"
    parameters:
      persona: "[persona name or list when multi-persona]"
      environment: "[device, connectivity, context]"
      emotion_range: "[min to max score]"
      friction_count: "[number]"
      dark_patterns_found: "[count or none]"
      a11y_issues: "[count or none]"
    ab_hypotheses: ["[hypothesis descriptions]"]
    latent_needs: ["[JTBD findings]"]
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]
      engines_failed: [list or none]
      personas_in_matrix: [list of persona_id]
      steps_in_matrix: [list of step_id]
      confidence_distribution:
        CONFIRMED: [count]
        LIKELY: [count]
        VERIFIED-DIVERGENT: [count]
      perspective_distribution:
        CONVERGENT: [count]
        DIVERGENT: [count]
      cross_persona_distribution:
        CROSS-PERSONA-UNIVERSAL: [count]
        CROSS-PERSONA-SEGMENT: [count]
        PERSONA-SPECIFIC: [count]
      calibration_distribution:
        validated: [count]
        supported: [count]
        hypothesis: [count]
        synthetic-only: [count]
      dark_pattern_auto_promoted: [count]
      rejected: [count + top categories — hallucination / voice-mismatch / already-mitigated / needs-info]
  Next: Palette | Experiment | Growth | Canvas | Spark | Scout | DONE
  Reason: [Why this next step]
```
