# Anvil — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Anvil-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Anvil
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[CLI Command | TUI Component | Tool Config | Doctor Command | Completion Script | Project Scaffold | Cross-Platform Handler]"
    parameters:
      target_language: "[Node.js | Python | Go | Rust]"
      cli_contract: "[command signature and flags summary]"
      tty_behavior: "[TTY-aware | non-TTY fallback]"
      exit_code_contract: "[0 = success, non-zero categories]"
      cross_platform_notes: "[Windows/macOS/Linux compat notes]"
  Validations:
    - "[help text present and accurate]"
    - "[non-TTY behavior verified]"
    - "[exit codes tested]"
    - "[CTRL+C cleanup verified]"
  Next: Gear | Radar | Quill | Judge | DONE
  Reason: [Why this next step]
```
