# Triggers and Events

Purpose: Choose the right GitHub Actions event, filter it safely, and avoid unsafe or over-coupled trigger graphs.

## Contents

- Event selection
- Trigger limits and gotchas
- Filtering rules
- Safe fork PR handling
- Common patterns
- Decision ladder

## Event Selection

| Event | Use it for | Key notes |
|------|-------------|-----------|
| `push` | standard branch or tag CI | Default for direct branch activity. |
| `pull_request` | normal PR CI | Safe default for forks because secrets are restricted. |
| `pull_request_target` | metadata-only automation on fork PRs | Runs in base-repo context. Never checkout untrusted fork code. |
| `merge_group` | merge queue validation | Required when merge queue is enabled. Use `types: [checks_requested]`. |
| `workflow_dispatch` | manual runs, rollback, replay, or testing | Supports typed inputs. Max `25` input keys (raised from `10` on Dec 4, 2025) and total input payload `65,535` characters. |
| `repository_dispatch` | cross-repo or external system trigger | Requires a PAT or GitHub App token. `GITHUB_TOKEN` cannot trigger it. Same 25-input cap as `workflow_dispatch`. |
| `workflow_run` | post-success follow-up workflow | Use only when the upstream workflow already finished. Keep preferred chain depth `<=2`. |
| `workflow_call` | reusable workflow entry point | Use when another workflow owns the top-level trigger. Cannot be combined with the Repository Rules "required workflow" gate — required workflows need `pull_request` and/or `merge_group`. |
| `schedule` | nightly, weekly, or periodic checks | IANA timezone support is GA as of March 2026 (`timezone: 'America/New_York'`); defaults to UTC if omitted. Default branch only, minimum practical interval `5 minutes`, auto-disabled after `60 days` of repo inactivity (commits / issues / PRs reset the timer — scheduled runs themselves do not). Scheduler lag of 15 min - 2+ h during peak hours is normal and independent of timezone. |
| `merge_group` | merge queue validation | Required when merge queue is enabled. Use `types: [checks_requested]`. |
| `issue_comment` | ChatOps comments | Filter hard and treat comment bodies as untrusted input. |

## Trigger Limits And Gotchas

- `workflow_dispatch` inputs are capped at `25` keys (raised from `10` on Dec 4, 2025) and `65,535` characters total. Same cap applies to `repository_dispatch.client_payload`.
- `repository_dispatch` needs a token that can call the API. `GITHUB_TOKEN` cannot trigger another workflow through this event.
- `workflow_run` should filter by upstream conclusion:

```yaml
if: github.event.workflow_run.conclusion == 'success'
```

- Workflow-level `paths` filters can skip the whole workflow only. For job-level routing, use `dorny/paths-filter`.
- Merge queue checks must include `merge_group`; `pull_request` alone is not enough. Misalignment between the required check name on the `pull_request` run and the `merge_group` run will block the queue indefinitely.
- "Required Workflows" (the legacy org-level setting) was retired Oct 18, 2023 — required workflows are now configured via **Repository Rules / Rulesets**. Rulesets evaluate the workflow against `pull_request` and/or `merge_group` triggers; reusable workflows entered via `workflow_call` cannot be made required.
- `schedule` honors `timezone:` (IANA) as of March 2026 — write `timezone: 'Asia/Tokyo'` next to the cron expression instead of pre-computing UTC offsets. Scheduler lag (15 min - 2+ h) still applies during peak hours.
- `pull_request_target` treats all fork-controlled data as hostile: titles, branch names, labels, artifacts, **the Actions cache** (May 2026 TanStack incident), and code.

## Filtering Rules

| Need | Recommended rule |
|------|-------------------|
| Limit branch scope | `branches:` or `branches-ignore:` on the event |
| Limit tag scope | `tags:` or `tags-ignore:` on the event |
| Skip whole workflow by paths | workflow-level `paths:` / `paths-ignore:` |
| Skip jobs by changed files | `dorny/paths-filter` job outputs |
| Skip noisy PR activities | `types: [opened, synchronize, reopened]` |
| Merge queue support | add `merge_group` alongside PR triggers |

Rule: do not mix `branches` with `branches-ignore` for the same event. Use negation inside `branches` when you need both inclusion and exclusion.

## Safe Fork PR Handling

Use `pull_request` for normal CI on forks. Use `pull_request_target` only when you need base-repo permissions for metadata workflows such as labeling or comment-driven automation.

Secrets are **not** available to `pull_request` workflows triggered from forks — that is the platform safety guarantee. Reaching for `pull_request_target` to "get secrets back" is the exact failure mode that Mini Shai-Hulud (Sept 2025 - May 2026) repeatedly exploited; route deployments through `workflow_run` after the trusted `push`/merge instead.

Safe pattern:

```yaml
on:
  pull_request_target:
    types: [opened, synchronize, labeled]

jobs:
  metadata-only:
    permissions:
      pull-requests: write
      contents: read
    steps:
      - run: echo "Label, comment, or gate only. Do not checkout fork code."
```

Unsafe patterns (do not ship):

```yaml
# Checkout of fork-controlled head in pull_request_target context
- uses: actions/checkout@<sha>
  with:
    ref: ${{ github.event.pull_request.head.sha }}
```

```yaml
# Restoring an Actions cache key that a fork PR can influence
- uses: actions/cache@<sha>
  with:
    key: build-${{ github.event.pull_request.head.ref }}
```

Both leak base-repo secrets / OIDC tokens to fork-controlled code paths.

## Common Patterns

| Scenario | Pattern |
|----------|---------|
| Standard CI | `push` + `pull_request` |
| Release on tag | `push.tags` with `v*` patterns |
| Nightly health check | `schedule` plus minimal workload guard |
| Manual rollback or replay | `workflow_dispatch` with explicit inputs |
| Cross-repo trigger | `repository_dispatch` with source validation in `client_payload` |
| Post-success deploy/report | `workflow_run` with explicit upstream name and conclusion filter |
| Merge queue | `pull_request` + `merge_group` + required check alignment |
| Comment-based command | `issue_comment` plus strict command prefix and actor guard |

## Decision Ladder

1. Start with `push` and `pull_request`.
2. Add `merge_group` if merge queue exists, and make sure the required check name matches the `pull_request` run.
3. Use `workflow_dispatch` for manual replay, rollback, or safe testing (up to 25 typed inputs).
4. Use `repository_dispatch` when another repo or an external system must trigger the workflow.
5. Use `workflow_run` only for post-success chaining, and redesign if the chain wants to reach depth `3`.
6. Use `pull_request_target` only for metadata workflows that never execute untrusted fork code, never restore a cache key influenced by fork data, and never grant write tokens beyond the metadata surface (`pull-requests: write` at most).
7. Use `schedule` with `timezone:` for periodic jobs; expect scheduler drift and re-arm the 60-day idle disable by keeping the repo active (real commits / PRs, not keep-alive bumps).
