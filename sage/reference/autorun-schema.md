# Sage — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Sage-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Sage
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    Task_Type: 1on1 | group | triage | retro | pitch
    Bottleneck: <one-sentence statement of the #1 problem>
    Patterns_Cited:
      - id: <P-XX | AP-XX>
        summary: <one-line summary>
    Anti_Patterns_Detected:
      - id: <AP-XX>
        summary: <one-line summary>
        signals: [<signal_1>, <signal_2>]
    Actions:
      - owner: <user/team>
        task: <observable outcome>
        due: <YYYY-MM-DD>
    Next_Checkpoint: <YYYY-MM-DD>
    Handoff_Target: <Builder | Plea | Sherpa | none>
  Next: <Builder | Plea | Sherpa | DONE>
  Reason: <why this outcome>
```
