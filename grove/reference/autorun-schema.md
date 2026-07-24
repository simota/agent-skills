# Grove — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Grove-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Grove
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Structure Plan | Audit Report | Docs Scaffold | Migration Plan | Monorepo Audit | Convention Profile]"
    parameters:
      language: "[detected language]"
      framework: "[detected framework]"
      repo_type: "[single | monorepo | polyrepo]"
      health_score: "[0-100]"
      health_grade: "[A | B | C | D | F]"
      anti_patterns_found: ["[AP-XXX: description]"]
      migration_level: "[L1 | L2 | L3 | L4 | L5 | N/A]"
    drift_detected: "[none | list]"
  Next: Scribe | Gear | Guardian | Sweep | DONE
  Reason: [Why this next step]
```
