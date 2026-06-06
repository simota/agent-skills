# Agent Teams API Quick Reference

> Purpose: Read this when Rally needs exact tool syntax, parameter names, or API-level constraints.

## Table of Contents

1. Tool Overview
2. Team Tools
3. Task Tools
4. Messaging
5. Data Structures
6. Constraints and Notes

## Tool Overview

| Tool | Use for |
|------|---------|
| `TeamCreate` | create the team context and task directory |
| `Agent` | spawn a teammate into the team |
| `TaskCreate` | create work items |
| `TaskUpdate` | assign owners, statuses, and dependencies |
| `TaskList` | inspect all tasks |
| `TaskGet` | inspect one task |
| `SendMessage` | DM, `broadcast`, shutdown, or plan approval |
| `TeamDelete` | delete the team after shutdown |

## Team Tools

### `TeamCreate`

```yaml
TeamCreate:
  team_name: string      # required team name
  description: string    # optional team description
  agent_type: string     # optional lead type
```

Creates:
- `~/.claude/teams/{team-name}/config.json`
- `~/.claude/tasks/{team-name}/`

### `Agent` (spawn teammate)

```yaml
Agent:
  subagent_type: string      # required teammate type
  team_name: string          # required team name
  name: string               # unique name inside the team
  description: string        # required 3-5 word summary
  prompt: string             # required task and context
  mode: string               # optional permission mode
  model: string              # optional model id
  run_in_background: boolean # optional async spawn flag
  isolation: string          # optional "worktree" for git worktree isolation
```

#### `subagent_type`

| Type | Tools |
|------|-------|
| `general-purpose` | full toolset |
| `Explore` | read-only |
| `Plan` | read-only |
| `Bash` | shell only |

#### `mode`

| Mode | Meaning |
|------|---------|
| `bypassPermissions` | auto-approve tools for low-risk work |
| `plan` | teammate must request plan approval |
| `default` | ask the user when approval is needed |
| `acceptEdits` | auto-approve file edits |
| `dontAsk` | run without asking |
| `auto` | automatic permission handling |

#### `model`

| Model | Meaning |
|-------|---------|
| `sonnet` | default |
| `opus` | highest capability |
| `haiku` | lightest option |

> Model ID reference (2026-05 snapshot): `opus` = `claude-opus-4-7`, `sonnet` = `claude-sonnet-4-6`, `haiku` = `claude-haiku-4-5-20251001`. Use the short names above when spawning teammates so future model bumps propagate automatically.

> **Opus 4.8 note for parallel work.** Opus 4.8 defaults to fewer subagent spawns and more in-line reasoning. When the lead teammate is on Opus 4.8, state the parallel-fan-out trigger explicitly in the spawn prompt (per `_common/OPUS_48_AUTHORING.md` P4) and pin an output-length envelope so completion reports stay comparable across teammates.

#### `isolation`

| Value | Meaning |
|-------|---------|
| `"worktree"` | Run the teammate in an isolated git worktree (independent copy of the repo). The worktree is auto-cleaned if no changes are made; if changes exist, the worktree path and branch are returned. |

Use `isolation: "worktree"` when teammates may edit overlapping files or when you want a clean merge workflow.

## Task Tools

### `TaskCreate`

```yaml
TaskCreate:
  subject: string        # required imperative title
  description: string    # required task details
  activeForm: string     # recommended in-progress label
  metadata: object       # optional key-value metadata
```

### `TaskUpdate`

```yaml
TaskUpdate:
  taskId: string         # required task id
  status: string         # pending | in_progress | completed | deleted
  subject: string        # optional title update
  description: string    # optional description update
  activeForm: string     # optional active label update
  owner: string          # teammate name
  addBlockedBy: [string] # task ids that block this task
  addBlocks: [string]    # task ids blocked by this task
  metadata: object       # optional metadata
```

### `TaskList`

```yaml
TaskList: {}
```

Expected fields:
- `id`
- `subject`
- `status`
- `owner`
- `blockedBy`

### `TaskGet`

```yaml
TaskGet:
  taskId: string
```

## Messaging

### Direct message

```yaml
SendMessage:
  type: "message"
  recipient: string
  content: string
  summary: string
```

### Broadcast

```yaml
SendMessage:
  type: "broadcast"
  content: string
  summary: string
```

### Shutdown request

```yaml
SendMessage:
  type: "shutdown_request"
  recipient: string
  content: string
```

### Shutdown response

```yaml
SendMessage:
  type: "shutdown_response"
  request_id: string
  approve: boolean
  content: string
```

### Plan approval response

```yaml
SendMessage:
  type: "plan_approval_response"
  request_id: string
  recipient: string
  approve: boolean
  content: string
```

### `TeamDelete`

```yaml
TeamDelete: {}
```

`TeamDelete` fails if active members remain.

## Data Structures

### `config.json`

```json
{
  "team_name": "feature-auth",
  "description": "Parallel implementation team for auth",
  "members": [
    {
      "name": "backend-impl",
      "agentId": "abc-123",
      "agentType": "general-purpose"
    }
  ]
}
```

Always reference teammates by `name`, not `agentId`.

### Task directory

`~/.claude/tasks/{team-name}/` stores the team task list. Manage it through `TaskList`, `TaskGet`, `TaskCreate`, and `TaskUpdate`.

## Constraints and Notes

### Team size

- Recommended: `2-4`
- Hard maximum: `10`
- `5+` requires user confirmation

### Cost

- Every teammate is a separate Claude instance.
- `broadcast` costs `N x` direct messages.
- Use `haiku` aggressively for lightweight work.

### Message delivery

- Teammate messages are delivered automatically.
- Teammates become `idle` at the end of a turn; this is normal.
- You can message an idle teammate and wake it back up.

### Hub-spoke rule (recommended pattern)

- Rally is the hub. All planned coordination flows through Rally.
- The API allows peer DM between teammates, and DM summaries are included in idle notifications visible to Rally.
- Rally's recommended practice is hub-spoke: teammates should not initiate peer DMs unless explicitly instructed. This keeps coordination predictable and observable.

### File operations

- `Explore` and `Plan` cannot edit files.
- Use `general-purpose` for implementation.
- Ownership is enforced by prompt discipline, not by the API itself.

### Display modes

- `in-process`: shown inside the main process
- `split-pane`: shown in an IDE-integrated split view

Display mode is currently chosen by the system.

### Teammate self-discovery

Teammates can read `~/.claude/teams/{team-name}/config.json` to discover other team members, their names, and agent types. This enables situational awareness without requiring Rally to relay the full roster.

### Task claim ordering

When multiple tasks are available for a teammate to claim, prefer claiming by task ID order (lowest ID first). This prevents starvation and ensures predictable progress.

### Structured JSON messages prohibited

Teammates must not send structured JSON status messages (e.g., `{"type":"idle",...}`). Use natural language in `SendMessage.content`. The system handles structured status tracking internally.

### `summary` field requirements

The `summary` field is **required** for `message` and `broadcast` types. It must be a concise 5-10 word preview of the message content. The system uses `summary` in idle notifications and message previews.

### Relationship to Claude Managed Agents (2026-04 beta)

As of 2026-04, Anthropic ships a fully managed agent harness for running Claude as an autonomous agent through the API. Multiagent sessions and `Outcomes` are in public beta under the `managed-agents-2026-04-01` beta header. The vocabulary maps cleanly onto Rally's local hub-spoke model:

| Managed Agents feature | Rally analogue | When to stay local vs escalate |
|------------------------|------------------|--------------------------------|
| **Multiagent Orchestration** (lead agent fan-out to specialists with their own model / prompt / tools) | `Agent` spawn with `team_name`, hub-spoke discipline | Stay local for in-session work; escalate when the workload runs unattended for days or needs platform-level audit |
| **Outcomes** (rubric + separate grader in its own context window) | Rally's evaluator pattern + `_common/HANDOFF.md` rubric fields | Escalate when grading must be tamper-resistant or shared across user accounts |
| **Memory + Dreaming** (per-agent memory refined between sessions, shared learnings across agents) | `_common/JOURNAL.md` + Lore's `MEMORY.md` curation | Escalate when learnings must persist across users or be audited centrally |
| **Webhooks** (completion notifications) | `_STEP_COMPLETE` handoff back to Nexus / Mend | Escalate when external systems (incident bot, deploy gate) must be triggered without keeping a session open |

Rally itself does not call the Managed Agents endpoints; Nexus surfaces the escalation recommendation in `NEXUS_COMPLETE` when the workload pattern actually justifies the managed platform.
