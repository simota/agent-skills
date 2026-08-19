# Cull — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Cull-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Cull
  Task_Type: scan | shai-hulud | lockfile | eradicate | rotate | harden | propagation
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    grade: CLEAN | SUSPECTED | CONFIRMED | ACTIVELY_BLEEDING
    target: "<host | repo path | container image | CI runner ID>"
    findings:
      - ioc_family: "<e.g. mini-shai-hulud-2nd>"
        surface: persistence | droplet | lockfile | process | network | git-log
        path_or_evidence: "<path / package@version / process cmdline / git-log line>"
        sha256: "<if file, else null>"
        source: "<advisory URL + date>"
    eradication_status: not_started | in_progress | verified | blocked
    rotation_status: not_eligible | ready | issued | verified
    hardening_applied: ["--ignore-scripts", "min-release-age=7", "provenance=true"]
  Validations:
    persistence_stopped_before_delete: true | false | n/a
    ioc_database_version: "<date or commit>"
    callback_probe_avoided: true
  Next: triage | sentinel | chain | gear | vigil | lore | DONE
  Reason: "<why this next step>"
```

---
