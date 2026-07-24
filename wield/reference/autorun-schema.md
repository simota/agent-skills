# Wield — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Wield-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Wield
  Recipe: automate | control | ui-script | integrate | audit | convert
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output: |
    Script delivered (path/inline), target apps, run command,
    required TCC permissions, dry-run result, destructive guards
  Next: [Tempo (schedule) | Anvil (CLI) | Latch (hook) | Sentinel (security review) | DONE]
  Reason: [why this status; if BLOCKED, the missing permission or app capability]
```
