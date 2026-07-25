# Dock — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `DETECT → SCAFFOLD → IMPLEMENT → ADAPT → VERIFY` and emit `_STEP_COMPLETE`. Dock-specific Constraints in `_AGENT_CONTEXT`: `distribution_channel` (`app_store` | `developer_id` | `both`), `macos_baseline`, `catalyst_or_native`, `document_based` (bool).

Dock-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Dock
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    implementation: [Feature; scene type(s) used; Liquid Glass chrome notes]
    files_changed: List[{path, type, changes}]
  Distribution_Compliance:
    entitlements_scoped: complete | partial | n/a
    hardened_runtime: enabled | n/a
    notarization_ready: yes | no | n/a
    sandbox_least_privilege: confirmed | flagged | n/a
  Handoff:
    Format: DOCK_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Sandbox/entitlement risks, App Review risks, Gatekeeper/notarization risks]
  Next: [NextAgent] | VERIFY | DONE
```

---
