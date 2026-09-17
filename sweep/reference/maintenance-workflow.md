# Maintenance Scans and Grove Handoffs

## Scope and Baseline

Use the requested PR/base revision, not an arbitrary `HEAD~N`. Incremental scans cover changed/deleted/renamed paths **and their dependents**; a whole-graph result must not be labeled changed-files-only. Full scans cover the declared project boundary. Record the actual tool/version/configuration and exit status; do not mutate manifests during detection or suppress failing commands. Dependency audits load `reference/dependency-cleanup.md`.

For large monorepos, partition by workspace/language/owner (including CODEOWNERS), collect evidence per area, and verify cross-workspace/public consumers before merging candidate lists. Follow the SKILL's small approved batches; two agreeing tools do not establish independent evidence when they use the same incomplete graph.

## Grove Reception

For `GROVE_TO_SWEEP_HANDOFF`, verify existence, primary-tool evidence, git activity and the SKILL confidence score. Accept ≥70 into the **queue**, defer 50–69 for manual verification, and return <50 with the still-referenced/conflicting-evidence note. Acceptance is not deletion authorization. Tag accepted candidates `source: grove-handoff` and return:

```yaml
SWEEP_TO_GROVE_FEEDBACK:
  handoff_date: "YYYY-MM-DD"
  processed: 0
  accepted: 0
  deferred: 0
  rejected: 0
  notes: []
```

## Persisted Schema

Write `SCAN_BASELINE` in `.agents/sweep.md`. Numbers below describe integer fields, not observed results; replace with measurements. Incremental scans merge into the current baseline; full scans replace it. Record actual deletions, reclaimed space and false positives after implementation, never count proposals as deletions.

```yaml
SCAN_BASELINE:
  date: "YYYY-MM-DD"
  scan_type: "full"  # or "incremental"
  tool: "<actual tool>"
  total_files_scanned: 0
  candidates_found: 0
  candidates_by_confidence:
    batch_delete: 0
    individual_review: 0
    manual_review: 0
    skipped: 0
  deleted_this_cycle: 0
  space_reclaimed_kb: 0
  false_positives: 0
  categories:
    dead_code: 0
    orphan_assets: 0
    unused_deps: 0
    config_remnants: 0
    duplicates: 0
    build_artifacts: 0
```

## Trend Tracking

| Metric | Good | Watch | Alert |
|--------|------|-------|-------|
| Candidate rate | `<3%` | `3-5%` | `>5%` |
| False positive rate | `<10%` | `10-20%` | `>20%` |
| Stale file growth | decreasing | flat | increasing |
| Cleanup velocity | increasing | flat | decreasing |

If alert conditions persist, escalate to Grove for a structural audit.

## Cleanup Health Targets

Record these local targets with observed denominators in `SCAN_BASELINE`; do not treat them as permission to delete a still-reachable file.

| Metric | Target |
|---|---|
| Dead Code Rate | <5% |
| Detection Accuracy | >80% |
| False Positive Rate | <20% |
| Time to Cleanup | <2 sprints |
| Regression Rate After Cleanup | <1% |
