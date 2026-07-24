# Atlas — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Atlas-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Atlas
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[ADR | RFC | Dependency Analysis | Debt Assessment | Module Boundary Design | Health Score | Tri-Engine Consensus ADR]"
    parameters:
      analysis_scope: "[module | package | system]"
      coupling_score: "[metric]"
      debt_items: "[count]"
      migration_risk: "[Low | Medium | High]"
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]
      engines_failed: [list or none]
      smell_confidence:
        CONFIRMED: [count]
        LIKELY: [count]
        VERIFIED-CANDIDATE: [count]
      option_perspective:
        CONVERGENT: [count]
        CONVERGENT-PARTIAL: [count]
        DIVERGENT: [count]
      recommended_option_style: "[Layered | Hexagonal | DDD | Event-Driven | Modular-Monolith | Microservices | CQRS | Vertical-Slice | Pipeline | Plugin]"
      dissenting_option_styles: [list of architectural styles preserved as alternatives]
      rejected: [count + top categories — hallucinated-module / already-mitigated / infeasible / anti-pattern]
  Next: Zen | Quill | Sherpa | Canvas | Builder | DONE
  Reason: [Why this next step]
```
