# Plea — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `SCOPE → CAST → CHANNEL → VOICE → COMPILE` and emit `_STEP_COMPLETE`.

Plea-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Plea
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    feature_requests: List[Request]
    personas_used: List[Persona]
    blind_spots_discovered: List[String]
    calibration_distribution: {validated|supported|hypothesis|synthetic-only: count}  # every request tagged
    dont_build_candidates: List[{request, reason}]
    rejection_ledger: {voice-mismatch|criteria-vague|persona-fabricated|feasibility-filtered: count}
    llm_prompts:
      per_request_count: [N — must equal feature_requests count]
      per_report: included
      action_verb_distribution: {ANALYZE|PROPOSE|DESIGN|DRAFT-SPEC|PROTOTYPE|REFINE: count}
    files_changed: List[{path, type, changes}]
    tri_engine: [present only on `multi` — schema in `reference/tri-engine-demand.md`]
  Handoff:
    Format: PLEA_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Synthetic demands diverging from real user voice]
  Next: [NextAgent] | VERIFY | DONE
```

---
