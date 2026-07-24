# Chain — AUTORUN `_STEP_COMPLETE` Schema

When Chain receives `_AGENT_CONTEXT`, parse `task_type` (`intake` / `audit` / `mcp` / `scan` / `recover`), `target` (skill dir / plugin / MCP server), and `Constraints`. Execute the matching Recipe silently (no verbose progress narration). Return `_STEP_COMPLETE` with the audit verdict.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Chain
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: audit_report
    verdict: APPROVED | REJECTED | QUARANTINED
    target: "<skill-dir or MCP server>"
    checklist_pass_rate: "<n>/<total>"
    findings:
      - severity: P0 | P1 | P2
        item: "<checklist item id>"
        rationale: "<one line>"
    manifest_path: "<.chain-manifest.json or null>"
    remediation_diff: "<path or inline or null>"
  Validations:
    intake_checklist_version: "1"
    unicode_scan: "passed | failed"
    bundled_artifact_scan: "passed | failed"
  Next: maintainer | triage | sentinel | lore | DONE
  Reason: "<why this next step>"
```
