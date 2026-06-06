# Workflow Design Anti-Patterns

Purpose: Audit workflow structure, trigger shape, execution graphs, and YAML quality before they become expensive or unsafe.

## Contents

- Workflow structure
- Trigger design
- Execution flow
- YAML quality

## Workflow Structure

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `WD-01` | Monolithic workflow | single workflow exceeds `500+` lines | split jobs, then extract reusable workflows where justified |
| `WD-02` | YAML indentation trap | steps silently scope wrong | run `actionlint` and use YAML-aware editing |
| `WD-03` | `ubuntu-latest` dependency | runner updates break CI unexpectedly | pin explicit runner versions such as `ubuntu-24.04` |
| `WD-04` | No concurrency control | duplicate runs on the same PR | add `concurrency` and `cancel-in-progress: true` for PR workflows |
| `WD-05` | Trigger overfire | all pushes on all branches run the full workflow | add branch filters, path filters, and job-level routing |
| `WD-06` | `workflow_run` chain depth | chain reaches `3+` workflows | keep preferred depth `<=2`; redesign before it reaches `3` |
| `WD-07` | Workflow file change trap | workflow edits trigger unexpected runs | test with `workflow_dispatch` and design filters with workflow-file changes in mind |

## Trigger Design

- Do not use `pull_request_target` to run fork PR code.
- Do not run schedules as full builds unless the scheduled check truly needs it.
- Filter `pull_request` activity types to the smallest useful set.
- Treat `repository_dispatch` as an authenticated API surface and validate its source.
- Add `merge_group` whenever merge queue is turned on.

## Execution Flow

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `EF-01` | Serial everything | CI time is the sum of all jobs | parallelize independent jobs and prefer a diamond graph |
| `EF-02` | No fail-fast strategy | failures cascade through scripts | use `set -eo pipefail`; use `continue-on-error` intentionally only |
| `EF-03` | Matrix explosion | matrix grows to `100+` jobs | prune combinations with `include` / `exclude`, split tiers by event |
| `EF-04` | Conditional logic mess | complex nested `if:` becomes unreadable | precompute flags or route by separate jobs |

## YAML Quality

- Normalize environment names to avoid case-sensitive protection mismatches.
- Pass untrusted expressions through `env:` before shell use.
- Set `defaults.run.shell` or per-step `shell:` when cross-platform behavior matters.
- Replace magic strings with shared `env:` values or reusable workflow inputs.
