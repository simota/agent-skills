# Chain — AUTORUN `_STEP_COMPLETE` Schema

When Chain receives `_AGENT_CONTEXT`, parse `task_type` (`intake` / `audit` / `mcp` / `scan` / `recover` / `malware-scan` / `campaign-scan` / `lockfile` / `eradicate` / `rotate` / `harden` / `propagation`), `target` (skill dir / plugin / MCP server / host / repo / image / runner), and `Constraints`. Execute the matching Recipe silently (no verbose progress narration).

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Chain
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: audit_report | malware_report | recovery_runbook | hardening_plan
    verdict: APPROVED | REJECTED | QUARANTINED | null
    target: "<skill-dir, MCP server, host, repo, image, or runner>"
    checklist_pass_rate: "<n>/<total>"
    findings:
      - severity: P0 | P1 | P2
        item: "<checklist item id>"
        rationale: "<one line>"
    manifest_path: "<.chain-manifest.json or null>"
    remediation_diff: "<path or inline or null>"
    infection:
      grade: CLEAN | SUSPECTED | CONFIRMED | ACTIVELY_BLEEDING | null
      findings:
        - ioc_family: "<campaign>"
          surface: persistence | droplet | lockfile | process | network | git-log
          evidence: "<path, package pin, command line, or log line>"
          sha256: "<file hash or null>"
          source: "<advisory URL + date>"
      eradication_status: not_started | in_progress | verified | blocked | null
      rotation_status: not_eligible | ready | issued | verified | null
  Validations:
    intake_checklist_version: "1"
    unicode_scan: "passed | failed"
    bundled_artifact_scan: "passed | failed"
    persistence_stopped_before_delete: true | false | n/a
    callback_probe_avoided: true | n/a
  Next: maintainer | triage | sentinel | gear | vigil | lore | DONE
  Reason: "<why this next step>"
```
