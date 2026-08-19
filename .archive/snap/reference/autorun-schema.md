# Snap — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Snap-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Snap
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    recipe: "[xcuitest | identifier | screenshot | appstore | page-object | ci | farm | xcresult]"
    deliverable: "[primary artifact]"
    files_changed: List[{path, type, changes}]
    test_target: "[name of XCUITest target]"
    identifier_taxonomy: "[convention used or proposed]"
    screenshot_scope: "[per-failure | checkpoint | appstore | none]"
    device_matrix: "[simulator devices + languages exercised]"
    xcresult_path: "[path or null]"
  Validations:
    build_check: "[passed | failed | n/a]"
    flake_audit: "[passed | flagged | skipped]"
    privacy_manifest: "[complete | partial | n/a]"
  Next: Native | Voyager | Gear | Launch | Judge | VERIFY | DONE
  Reason: [why this next step]
```
