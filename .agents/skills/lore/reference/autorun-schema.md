# Lore — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Lore-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Lore
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [report path or inline]
    artifact_type: "[Harvest Report | Synthesis Report | METAPATTERNS Update | LORE_INSIGHT | Audit Report | Contradiction Resolution]"
    parameters:
      patterns_discovered: "[count]"
      patterns_promoted: "[count]"
      contradictions_found: "[count]"
      stale_patterns: "[count]"
      consumers_notified: ["[agent list]"]
  Next: Architect | Darwin | Sigil | Nexus | Mend | Triage | DONE
  Reason: [Why this next step]
```
