# Communication Patterns

> Purpose: Read this when sending teammate messages, choosing DM vs `broadcast`, or standardizing teammate reports.

## Table of Contents

1. Message Type Guide
2. Rally -> Teammate Templates
3. Teammate -> Rally Templates
4. Broadcast Templates
5. `plan_approval_response`

## Message Type Guide

| Type | `SendMessage.type` | Use for | Cost | Default |
|------|--------------------|---------|------|---------|
| Direct message | `message` | instructions, questions, blocker updates, progress checks | Low | Yes |
| Broadcast | `broadcast` | emergency or team-wide state change only | High (`N x`) | No |
| Shutdown request | `shutdown_request` | teammate termination | Low | Once per teammate |
| Plan approval | `plan_approval_response` | respond to a teammate in `plan` mode | Low | Only when requested |
| Shutdown response | `shutdown_response` | teammate confirms or rejects shutdown | Low | Only when requested |

### Message content rules

- `summary` is **required** for `message` and `broadcast` types (5-10 word preview).
- Do not send structured JSON status messages (e.g., `{"type":"idle",...}`). Use natural language in `content`.

### DM vs `broadcast`

| Situation | Choice |
|-----------|--------|
| One teammate is affected | DM |
| Several teammates are affected differently | separate DMs |
| Everyone must react immediately | `broadcast` |

Use `broadcast` only for shared-file updates, emergency stop instructions, or a true team-wide policy change.

## Rally -> Teammate Templates

### Task Start Instruction

```yaml
SendMessage:
  type: "message"
  recipient: "[teammate_name]"
  content: |
    ## Task Start Instruction

    Please begin work on task "[task_name]".

    ### Overview
    [Specific task description]

    ### File Ownership
    - exclusive_write: [pattern list]
    - shared_read: [pattern list]

    ### Completion Criteria
    1. [Criterion 1]
    2. [Criterion 2]

    ### Notes
    - [Any notes]

    When done, mark your task as completed via TaskUpdate.
  summary: "Start instruction for [task_name]"
```

### Blocker Resolved Notification

```yaml
SendMessage:
  type: "message"
  recipient: "[teammate_name]"
  content: |
    Blockers for task "[task_name]" have been resolved.

    Prerequisite task results:
    - [Summary of prerequisite results]
    - Reference files: [file paths]

    Please begin work. Set your task to in_progress via TaskUpdate.
  summary: "Blocker resolved, start work"
```

### Additional Context

```yaml
SendMessage:
  type: "message"
  recipient: "[teammate_name]"
  content: |
    Sharing additional information.

    [Additional context content]

    Please continue work with this information in mind.
  summary: "Additional context provided"
```

### Progress Check

```yaml
SendMessage:
  type: "message"
  recipient: "[teammate_name]"
  content: |
    Please report progress on task "[task_name]".
    Share your current status and remaining estimate.
  summary: "Progress check request"
```

## Teammate -> Rally Templates

### Completion Report

```markdown
## Task Completion Report

**Task:** [task name]
**Status:** Complete

### Changed Files
- [file path 1]: [change description]
- [file path 2]: [change description]

### Test Results
- [test result summary]

### Notes
- [anything noteworthy]
```

### Failure Report

```markdown
## Failure Report

**Task:** [task name]
**Status:** Blocked

### Problem
[Problem details]

### What Was Tried
1. [Attempt 1]
2. [Attempt 2]

### Help Needed
[What is required]
```

### Question

```markdown
## Question

**Task:** [task name]

### Question
[The question]

### Options
A: [Option A]
B: [Option B]

### Recommendation
[If any]
```

## Broadcast Templates

### Shared File Update

```yaml
SendMessage:
  type: "broadcast"
  content: |
    [SHARED FILE UPDATE]

    The following shared files have been updated:
    - [file path]: [change description]

    Please reference the latest version and continue your work.
    Report to Rally if this impacts your work.
  summary: "Shared file update notification"
```

### Emergency Stop

```yaml
SendMessage:
  type: "broadcast"
  content: |
    [EMERGENCY STOP]

    Due to [reason], please temporarily halt all work.
    Save your current work state and stand by until further notice.
  summary: "Emergency stop instruction"
```

## `plan_approval_response`

Use this only when a teammate was spawned with `mode: "plan"`.

### Approve

```yaml
SendMessage:
  type: "plan_approval_response"
  request_id: "[request ID]"
  recipient: "[teammate_name]"
  approve: true
```

### Reject

```yaml
SendMessage:
  type: "plan_approval_response"
  request_id: "[request ID]"
  recipient: "[teammate_name]"
  approve: false
  content: |
    Please address the following:
    1. [Fix point 1]
    2. [Fix point 2]

    Please resubmit your plan after corrections.
```

## Peer DM (teammate-to-teammate)

The API allows teammates to send direct messages to each other. DM summaries are included in idle notifications visible to Rally.

Rally's recommended practice is hub-spoke: teammates should not initiate peer DMs unless explicitly instructed. If peer DM is enabled for a specific workflow:

- Rally retains visibility through idle notification summaries.
- Instruct teammates to CC Rally on important decisions.
- Monitor for coordination drift during `MONITOR` phase.

## Teammate -> Rally SendMessage Templates

### Completion Report

```yaml
SendMessage:
  type: "message"
  recipient: "rally"
  content: |
    ## Task Completion Report

    **Task:** [task name]
    **Status:** Complete

    ### Changed Files
    - [file path 1]: [change description]

    ### Test Results
    - [test result summary]

    ### Notes
    - [anything noteworthy]
  summary: "Task [name] completed"
```

### Failure Report

```yaml
SendMessage:
  type: "message"
  recipient: "rally"
  content: |
    ## Failure Report

    **Task:** [task name]
    **Status:** Blocked

    ### Problem
    [Problem details]

    ### What Was Tried
    1. [Attempt 1]

    ### Help Needed
    [What is required]
  summary: "Task [name] blocked, need help"
```

## Shutdown Response

```yaml
SendMessage:
  type: "shutdown_response"
  request_id: "[request ID from shutdown_request]"
  approve: true
  content: "All tasks complete, ready to shut down."
```

Cross-agent handoff headers such as `## SHERPA_TO_RALLY_HANDOFF` and `## RALLY_TO_NEXUS_HANDOFF` live in `reference/integration-patterns.md`.
