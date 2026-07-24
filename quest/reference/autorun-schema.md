# Quest — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `FRAME → PILLARS → LOOP → SYSTEMS → BALANCE → HANDOFF` and emit `_STEP_COMPLETE`.

Quest-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Quest
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    game_design: [pillars, core loop, mechanics, balance tables, economy]
    files_changed: List[{path, type, changes}]
  Handoff:
    Format: QUEST_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Dominant strategies, economy imbalances, scope risks]
  Next: Tick | Forge | Matrix | VERIFY | DONE
  Reason: [Why this Status/Next; if BLOCKED/FAILED, what is needed to unblock]
```

---
