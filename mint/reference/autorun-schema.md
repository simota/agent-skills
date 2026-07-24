# Mint — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run factory design / fixture generation / seed creation and emit `_STEP_COMPLETE`. Mint-specific Constraints in `_AGENT_CONTEXT`: library constraints, volume constraints.

Mint-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Mint
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    factories: [Factory descriptions]
    fixtures: [Fixture file descriptions]
    seed_scripts: [Seed script descriptions]
    files_changed: List[{path, type: created, changes}]
  Handoff:
    Format: MINT_TO_[NEXT]_HANDOFF
    Content: [Factories, fixtures, usage docs]
  Risks: [Data integrity, anonymization fidelity vs privacy, volume vs generation time]
  Next: Radar | Voyager | Builder | VERIFY | DONE
```

---
