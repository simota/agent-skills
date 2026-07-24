# Native — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `DETECT → SCAFFOLD → IMPLEMENT → ADAPT → VERIFY` and emit `_STEP_COMPLETE`. Native-specific Constraints in `_AGENT_CONTEXT`: `target_platforms`, `ios_baseline`, `android_baseline`, `target_sdk`, `offline_tier`.

Native-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Native
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    implementation: [Feature per platform; Liquid Glass / M3 Expressive notes]
    files_changed: List[{path, type, changes}]
  Privacy_Compliance:
    privacy_manifest: complete | partial | n/a
    data_safety: complete | partial | n/a
    ai_disclosure_ui: present | n/a
  Handoff:
    Format: NATIVE_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Platform-specific risks, store-review risks]
  Next: [NextAgent] | VERIFY | DONE
```

---
