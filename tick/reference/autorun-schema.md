# Tick — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `FRAME → DESIGN → IMPLEMENT → INTEGRATE → VERIFY` and emit `_STEP_COMPLETE`.

Tick-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Tick
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    game_architecture: [loop type, entity architecture, state model, netcode model]
    determinism: deterministic | non-deterministic-by-design
    files_changed: List[{path, type, changes}]
  Handoff:
    Format: TICK_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Determinism gaps, frame-budget risks, sync edge cases]
  Next: Bolt | Radar | Judge | VERIFY | DONE
```

---
