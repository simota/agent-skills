# Saga — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `DISCOVER → FRAME → CRAFT → REFINE → DELIVER` and emit `_STEP_COMPLETE`. Saga-specific Constraints in `_AGENT_CONTEXT`: target audience, framework preference, length/format constraints.

Saga-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Saga
  Task_Type: use_case_story | product_narrative | pitch_story | customer_success | onboarding | scenario | tri_engine_portfolio | tri_engine_compete
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    narrative: [Story content]
    framework_used: [Framework name]
    anti_pattern_check: [AP results]
    files_changed: List[{path, type, changes}]
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]
      engines_failed: [list or none]
      merge_strategy: "[Portfolio | Compete]"
      concurrence_distribution:
        UNIVERSAL: [count]
        LIKELY: [count]
        VERIFIED-DIVERGENT: [count]
      archetype_coverage: ["Hero's Journey", "JTBD", "Before-After-Bridge", ...]
      rejected: [count + top categories — no-arc / hero-product / no-tension / generic-persona / jargon / ad-copy / fabricated-evidence]
  Handoff:
    Format: SAGA_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Assumptions needing validation]
  Next: [NextAgent] | VERIFY | DONE
```

---
