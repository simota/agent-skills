# Summon — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Summon-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Summon
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [reading path or inline]
    artifact_type: "[Channeled Reading | Conclave | Critique | Figure Roster]"
    parameters:
      recipe: "[channel | conclave | critique | roster]"
      figures: "[names]"
      attestation_mix: "[# ATTESTED / # INFERRED / # SPECULATIVE]"
      ethics_gate: "[passed | refused | escalated]"
  Validations:
    quotes_fabricated: "none"
    disclaimer_present: "[yes | no]"
  Next: Magi | Riff | Scribe | DONE
  Reason: [Why this next step]
```
