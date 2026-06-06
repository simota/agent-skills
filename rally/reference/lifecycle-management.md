# Lifecycle Management

> Purpose: Read this when executing Rally's 7-phase lifecycle, handling teammate failures, or shutting the team down safely.

## Table of Contents

1. Phase Summary
2. Phase Details
3. Error Scenarios

## Phase Summary

| Phase | Goal | Mandatory action |
|-------|------|------------------|
| `ASSESS` | decide whether Rally is appropriate | reject false parallelism early |
| `DESIGN` | choose team pattern and ownership | present design through `ON_TEAM_DESIGN` when needed |
| `SPAWN` | create the team and teammates | `TeamCreate` before any `Agent` spawn |
| `ASSIGN` | create tasks and dependencies | set `owner`, `status`, and `addBlockedBy` correctly |
| `MONITOR` | supervise progress | poll `TaskList`, respond to failures, and interpret `idle` correctly |
| `SYNTHESIZE` | merge results and verify quality | trigger `ON_RESULT_CONFLICT` if outputs collide |
| `CLEANUP` | end the session safely | `shutdown_request` each teammate, then `TeamDelete` |

## Phase Details

### `ASSESS`

Use Rally only when:

- `2+` independent units exist, or
- staged parallelism is possible through `blockedBy`, and
- parallel gain is likely to exceed coordination cost.

Reject Rally when all work writes the same files, only one task exists, or the task is investigation-only.

### `DESIGN`

1. Select a pattern from `reference/team-design-patterns.md`.
2. Choose teammate names, `subagent_type`, model, and mode.
3. Declare ownership via `reference/file-ownership-protocol.md`.
4. Ask through `ON_TEAM_DESIGN` when design approval is required.

### `SPAWN`

1. Run `TeamCreate`.
2. Spawn teammates via `Agent` with `run_in_background: true`. Optionally use `isolation: "worktree"` for file-overlap scenarios.
3. Teammates can self-discover other members by reading `~/.claude/teams/{team-name}/config.json`.
4. Confirm the prompt includes:
   team name and role, task, `exclusive_write` and `shared_read`, conventions, dependencies, completion criteria, and `TaskUpdate` instructions.

### `ASSIGN`

1. Create tasks with `TaskCreate`.
2. Wire dependencies through `TaskUpdate.addBlockedBy`.
3. Set the owner and move the task to `in_progress`.
4. DM the owner when blockers are cleared.

### `MONITOR`

Use this loop until all tasks finish:

- `completed` -> prepare for synthesis
- `in_progress` -> normal; process idle notifications
- `pending` + unblocked -> assign or nudge the owner
- `blocked` -> resolve the blocker or re-sequence work

`idle` means waiting. It does not mean done.

When multiple tasks are available for a teammate, prefer claiming by task ID order (lowest ID first) to prevent starvation.

### `SYNTHESIZE`

1. Collect completed tasks and `files_changed`.
2. Check the ownership map.
3. Verify build, tests, and lint or type checks.
4. Fire `ON_RESULT_CONFLICT` if same-file edits or incompatible outputs appear.

### `CLEANUP`

1. Confirm all tasks are complete.
2. Send `shutdown_request` to each teammate.
3. Wait for `approve: true`.
4. Run `TeamDelete`.
5. Report team composition, completed tasks, changed files, verification results, and remaining risks.

## Error Scenarios

### Teammate Hang

Symptom: still `in_progress`, no progress, no meaningful replies.

Response:
1. DM a status check up to `2` times.
2. If still no response, send `shutdown_request`.
3. If shutdown still fails, stop the task and replace the teammate.
4. Reassign the task.

### Teammate Failure

Symptom: task reports failure or becomes blocked with an error.

Response:
1. Confirm next action via `ON_TEAMMATE_FAILURE` when needed.
2. Retry with more context.
3. Retry with reduced scope.
4. Replace the teammate.
5. Skip and report if replacement is not justified.

### All Teammates Failed

Response:
1. Send `shutdown_request` to all teammates.
2. Run `TeamDelete`.
3. Report alternatives:
   sequential fallback, reduced scope, or prerequisite review.

### Shutdown Rejected

Response:
1. Check the rejection reason.
2. Wait if tasks remain.
3. Report to the user if the reason is unclear or unresolved.
