# AUTORUN Protocol

This document defines the platform-agnostic automatic execution protocol for Nexus orchestration.

---

## Overview

AUTORUN mode enables Nexus to execute agent chains automatically without manual copy-paste handoffs.
This protocol works across different AI platforms (Claude Code, Codex CLI, Gemini, etc.).

---

## Execution Modes

| Mode | Trigger | Behavior | Platform |
|------|---------|----------|----------|
| AUTORUN_FULL | `## NEXUS_AUTORUN_FULL` | Execute all steps including COMPLEX tasks | All |
| AUTORUN | `## NEXUS_AUTORUN` | Execute SIMPLE tasks only | All |
| GUIDED | `## NEXUS_GUIDED` | Manual agent invocation | All |
| INTERACTIVE | `## NEXUS_INTERACTIVE` | Confirm each step | All |

---

## Agent Spawn Execution

In AUTORUN mode, Nexus spawns each agent as an independent Claude session via the Agent tool:

```
## Nexus Execution: [Goal]
- Chain: Agent1 → Agent2 → Agent3
- Mode: AUTORUN_FULL

### Spawning Step [X/Y]: [AgentName]

Agent(
  name: "[agent-name]-[task-slug]"
  description: "[Short task description]"
  subagent_type: general-purpose
  mode: bypassPermissions
  model: [sonnet|opus|haiku]
  prompt: |
    You are the [AgentName] agent.
    First, read ~/.claude/skills/[agent-name]/SKILL.md and follow its instructions.

    Task: [task_description]
    Context from previous step: [handoff_context]
    Constraints: [constraints]

    When complete, output the result in the following format:
    _STEP_COMPLETE:
      Agent: [AgentName]
      Status: SUCCESS | PARTIAL | BLOCKED | FAILED
      Output: [deliverable]
      Next: [recommended next agent or DONE]
)
```

### Execution Layers

#### Claude Code

| Layer | Method | When | API |
|-------|--------|------|-----|
| **L1: Direct Spawn** | Agent tool (foreground) | 1-4 step sequential chains | `Agent(prompt, mode)` |
| **L2: Parallel Spawn** | Agent tool (background) | 2-3 independent branches | `Agent(prompt, run_in_background: true)` |
| **L3: Rally Delegation** | Spawn Rally as Agent | 4+ workers, complex ownership | `Agent(prompt="You are Rally...")` |

#### Codex CLI

| Layer | Method | When | API |
|-------|--------|------|-----|
| **L1: Direct Spawn** | `spawn_agent` → `wait_agent` | 1-4 step sequential chains | `spawn_agent(prompt)` → `wait_agent(id)` |
| **L2: Parallel Spawn** | Multiple `spawn_agent` → `wait_agent` all | 2-3 independent branches | `spawn_agent` × N → `wait_agent` × N |
| **L3: Rally Delegation** | `spawn_agent` with Rally prompt | 4+ workers, complex ownership | `spawn_agent(prompt="You are Rally...")` |

**Codex Subagent Tools:**
- `spawn_agent` — Spawn a new subagent
- `send_input` — Send additional instructions to a running subagent
- `wait_agent` — Wait for a subagent to complete
- `resume_agent` — Resume a paused subagent
- `close_agent` — Close a subagent's thread

### Layer Selection

```
Steps <= 4 AND sequential?     → L1: Direct Spawn (foreground / spawn_agent)
2-3 independent branches?      → L2: Parallel Spawn (background / spawn_agent × N)
4+ workers OR complex ownership? → L3: Rally Delegation
```

### Model Selection

| Agent Role | model | Context Strategy | Rationale |
|-----------|-------|-----------------|-----------|
| Investigation / read-only (Scout, Lens, Trail) | sonnet | reset | Cost-efficient; focused context |
| Standard implementation (Builder, Artisan, Radar) | sonnet | hybrid | Balanced; receives handoff context |
| High-complexity design (Sentinel, Atlas) | opus | continuous | Precision-critical; deep reasoning |
| Lightweight tasks (Quill, Morph) | haiku | reset | Minimal cost; fresh context |
| Evaluator (Judge, Voyager, Warden in eval mode) | sonnet | reset | Evaluators need only contract + output |
| Generator (revision iteration) | sonnet | continuous | Benefits from feedback accumulation |

**Context Strategy**: `reset` = file-based handoff (fresh context per agent), `continuous` = in-context handoff (accumulated context), `hybrid` = Nexus continuous + spawned agents reset. See `nexus/reference/context-strategy.md` for details.

### Advanced Spawn Options

Agent tool (v2.1.63+) supports additional frontmatter fields for fine-grained control:

| Option | Description | When to Use |
|--------|-------------|-------------|
| `maxTurns` | Maximum agentic turns before stopping | Cost control and runaway prevention. Investigation: 20-30, implementation: 50-80 |
| `effort` | Reasoning effort (`low`/`medium`/`high`/`max`) | Haiku+low for ultra-lightweight tasks, Opus+max for maximum precision |
| `isolation: worktree` | Isolated execution via Git worktree | Prevents file conflicts during L2 parallel runs. Each branch works in its own independent copy |
| `resume` (agent ID) | Resume an existing subagent | Retry after failure or continue additional work. Retains full history |
| `skills` | Pre-inject Skill content | Inject SKILL.md directly instead of telling the prompt to "read" it |
| `memory` | Persistent memory (`user`/`project`/`local`) | Cross-session persistence for routing learning and pattern accumulation |

**Worktree isolation for L2:**
```
# Using worktree during L2 parallel spawn eliminates file conflict risk
Agent(
  name: "builder-feature-a"
  isolation: worktree          # Run in an independent git worktree
  run_in_background: true
  ...
)
Agent(
  name: "builder-feature-b"
  isolation: worktree
  run_in_background: true
  ...
)
# After both complete, merge the worktree changes
```

### Custom Subagent Definitions

By placing a Markdown file in `.claude/agents/` (project) or `~/.claude/agents/` (user), you can pre-define a custom subagent_type. This keeps the spawn-time prompt concise and ensures tool restrictions, model selection, and skill injection are reliably applied.

```yaml
# ~/.claude/agents/scout-agent.md
---
name: scout-agent
description: Bug investigation and root cause analysis. Use proactively for bug reports.
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
maxTurns: 30
memory: project
skills:
  - scout
---
You are the Scout agent. Investigate the root cause of the bug and identify reproduction steps and impact scope.
Do not modify code. When complete, report in the _STEP_COMPLETE format.
```

Predefined agents can be referenced directly via `subagent_type: "scout-agent"`.

---

## Agent Context Injection

When spawning an agent, Nexus provides context through the prompt:

1. **SKILL.md Path**: Tell the agent to read its own SKILL.md first
2. **Task Description**: Clear, specific task with acceptance criteria
3. **Handoff Context**: Results from previous steps in the chain
4. **Constraints**: Guardrail level, file ownership, scope limits
5. **Output Format**: Request `_STEP_COMPLETE` format in the response

The spawned agent reads its own SKILL.md and follows its own methodology autonomously. Nexus does not need to simulate the agent's personality or process.

### Example: Spawning Scout

```
Agent(
  name: "scout-login-bug"
  description: "Investigate login bug root cause"
  subagent_type: general-purpose
  mode: bypassPermissions
  model: sonnet
  prompt: |
    You are the Scout agent.
    First, read ~/.claude/skills/scout/SKILL.md and follow its instructions.

    Task: Investigate the root cause of the login bug.
    Symptom: Users cannot log in
    Constraints: Do not modify code (investigation only)

    When complete, output the result in the following format:
    _STEP_COMPLETE:
      Agent: Scout
      Status: SUCCESS | PARTIAL | BLOCKED | FAILED
      Output: [investigation result]
      Next: [recommended next agent or DONE]
)
```

Scout returns:
```
_STEP_COMPLETE:
  Agent: Scout
  Status: SUCCESS
  Output: Root cause identified - token refresh timing issue in auth middleware
```

### Example: Spawning Scout (Codex CLI)

```
# Step 1: Spawn Scout
scout_id = spawn_agent(
  prompt: |
    You are the Scout agent.
    First, read ~/.claude/skills/scout/SKILL.md and follow its instructions.

    Task: Investigate the root cause of the login bug.
    Symptom: Users cannot log in
    Constraints: Do not modify code (investigation only)

    When complete, output the result in the _STEP_COMPLETE format.
)

# Step 2: Wait for completion
result = wait_agent(scout_id)

# Step 3: Use result to spawn Builder
builder_id = spawn_agent(
  prompt: |
    You are the Builder agent.
    First, read ~/.claude/skills/builder/SKILL.md and follow its instructions.
    Context from previous step: {result}
    ...
)
wait_agent(builder_id)

# Step 4: Cleanup
close_agent(scout_id)
close_agent(builder_id)
  Next: Builder
```

---

## Step Transitions

### Automatic Transition (AUTORUN)

After receiving `_STEP_COMPLETE` from a spawned agent, Nexus automatically:
1. Records the completed step and captures the agent's output
2. Extracts handoff context from the result
3. Spawns the next agent in the chain with accumulated context

### Manual Transition (GUIDED)

After receiving the agent's result, Nexus:
1. Outputs the `## NEXUS_HANDOFF` block to the user
2. Waits for user to confirm continuation
3. Spawns the next agent when confirmed

---

## Guardrail Protocol

Guardrail definitions and configuration for autonomous execution. Used by AUTORUN to decide between continue, pause, recover, and abort during chain execution.

### Guardrail Levels

| Level | Name | Behavior | Use Case |
|-------|------|----------|----------|
| L1 | MONITORING | Log only, no pause | Lint warnings, minor deprecations, coverage drop < 5% |
| L2 | CHECKPOINT | Auto-verify, attempt auto-fix | Test failures < 20%, type errors, low/medium CVEs |
| L3 | PAUSE | Pause branch; auto-recover or escalate | Test failures > 50%, breaking changes, build failures, merge conflicts |
| L4 | ABORT | Immediate stop and rollback | Critical security, data integrity risk, user abort |

### Triggers by Level

**L1 — MONITORING**

| Trigger | Action |
|---------|--------|
| `lint_warning` | Log, continue |
| `minor_deprecation` | Log, continue |
| `style_inconsistency` | Log, auto-fix if possible |
| `coverage_decrease_minor` (< 5%) | Log, continue |

**L2 — CHECKPOINT**

| Trigger | Action |
|---------|--------|
| `test_failure_minor` (< 20%) | Auto-fix attempt → retest (max 3) |
| `security_warning` (non-critical) | Add Sentinel scan |
| `type_error` | Auto-fix attempt (max 2) |
| `performance_regression` (< 10%) | Log, optional Bolt |
| `dependency_vulnerability` (Low/Medium) | Log, suggest update |

**L3 — PAUSE**

| Trigger | Action |
|---------|--------|
| `test_failure_major` (> 50%) | Rollback, re-decompose with Sherpa |
| `breaking_change` | Pause, verify consumers (Ripple) |
| `security_critical` (High) | Pause, require Sentinel |
| `merge_conflict` | Pause, resolve or escalate |
| `build_failure` | Rollback, fix attempt (max 2) |

**L4 — ABORT**

| Trigger | Action |
|---------|--------|
| `critical_security` | Abort, rollback |
| `data_integrity_risk` | Abort, rollback |
| `infinite_loop_detected` | Abort |
| `user_abort` | Abort |

### Configuration by Task Type

| Task Type | Default Level | Pre-checks | Post-checks | Escalate On |
|-----------|--------------|------------|-------------|-------------|
| FEATURE | L2 | — | tests_pass, build_success | test_failure > 50%, security_critical |
| SECURITY | L2 | sentinel_scan | no_new_vulnerabilities, tests_pass | any_security_issue |
| REFACTOR | L2 | — | tests_unchanged, no_behavior_change | test_failure_any |
| API_BREAKING | L3 | ripple_impact_analysis | consumers_updated, migration_ready | consumer_not_updated |
| INCIDENT | L3 | — | service_restored, no_regression | service_not_restored |
| INFRA | L3 | dry_run_if_available | health_checks_pass | health_check_fail |

### Mandatory Checkpoints

| Checkpoint | Phase | Level | Check |
|------------|-------|-------|-------|
| POST_IMPLEMENT | After implementation | L2 | Tests pass, types valid |
| PRE_MERGE | Before aggregate | L2 | No conflicts |
| POST_MERGE | After aggregate | L2 | Combined tests pass |
| PRE_DELIVER | Before delivery | L2 | All acceptance criteria met |

### Escalation Path

```
L1 (Log) → issue persists → L2 (Checkpoint)
  ├─ auto-recovery success → CONTINUE
  └─ recovery failed → L3 (Pause)
      ├─ auto-recovery success → CONTINUE
      ├─ user confirms → CONTINUE/ADJUST
      └─ critical or no resolution → L4 (Abort) → ROLLBACK + STOP
```

### Parallel Execution Guardrails

- Each branch has **independent** L1/L2 guardrails
- L3 pauses **only the affected branch**
- L4 triggers **global abort** across all branches

Branch-level details: `_common/PARALLEL.md`

### Cross-references

- **Parallel branches:** `_common/PARALLEL.md`
- **Harness evolution:** `_common/HARNESS_EVOLUTION.md` (HE-01 tracks L2+ trigger frequency for simplification)
- **Reverse feedback:** `_common/REVERSE_FEEDBACK.md` — high-priority feedback triggers L2; systemic issues (3+) trigger L3
- **Web fetch safety:** `_common/WEB_FETCH_SAFETY.md` — strong injection indicators map to L3/L4

---

## Platform Compatibility

### Tool Abstraction

The protocol uses semantic descriptions instead of platform-specific tool names:

| Action | Description | Claude Code | Codex CLI | Gemini |
|--------|-------------|-------------|-----------|--------|
| Ask user | Request user input | AskUserQuestion | prompt() | input() |
| Run command | Execute shell | Bash | shell() | execute() |
| Read file | Load file content | Read | read() | file.read() |
| Edit file | Modify file | Edit | edit() | file.write() |
| Search code | Find in codebase | Grep/Glob | search() | find() |

### Agent Invocation

Instead of platform-specific agent calls, use semantic triggers:

```yaml
# Platform-agnostic
## NEXUS_AUTORUN_FULL
Add user authentication

# Nexus interprets and executes as:
# 1. Scout (investigate requirements)
# 2. Builder (implement)
# 3. Sentinel (security check)
# 4. Radar (tests)
```

---

## Completion Format

### AUTORUN Completion

```
## NEXUS_COMPLETE
Task: [Task name]
Mode: AUTORUN_FULL
Chain: [Executed chain]

### Summary
- Steps completed: [N]
- Files changed: [List]
- Tests: [PASS/FAIL]

### Results
[Final deliverables]

### Verification
1. [How to verify step 1]
2. [How to verify step 2]
```

### GUIDED Completion

```
## NEXUS_COMPLETE
Task: [Task name]
Mode: GUIDED
Chain: [Executed chain]

### Summary
[Results from manual execution]
```

---

## Design Principles

### Context Externalization

> Context is an external interrogable object, not embedded state. [Source: Anthropic Managed Agents]

Do not embed the full chain history into each agent's prompt. Instead, treat the session as an append-only event log that agents can query:

| Anti-pattern | Pattern |
|---|---|
| Paste all prior step outputs into prompt | Store in `.agents/PROJECT.md`; pass summary + file path reference |
| Irreversible context trimming (discard tokens permanently) | Keep full log external; selectively retrieve what the current step needs |
| Growing prompt with every step | Pass only the state delta from the previous step |

**Practical implementation:**
- `_STEP_COMPLETE` outputs serve as the event log entries
- Each agent receives: task description + previous step's key output + file references
- Full history is always recoverable from `.agents/PROJECT.md` + agent journals
- When a step needs earlier context, it reads the journal file — not the prompt

### Lazy Provisioning (TTFT Optimization)

> Provision execution environments only when the brain actually needs them. [Source: Anthropic Managed Agents]

Delay agent spawning until the orchestrator has decided what to spawn:

```
CLASSIFY → CHAIN_SELECT → (first inference starts immediately)
                          → (agent spawn happens just-in-time for EXECUTE)
```

| Optimization | Effect |
|---|---|
| Start CLASSIFY/CHAIN_SELECT without waiting for agent readiness | Reduces time-to-first-token |
| Spawn agents only when their step is next | Avoids unnecessary resource allocation for steps that may be skipped |
| Use `model: haiku` for investigation steps, `model: opus` for critical steps | Right-size compute per step |

**In practice:** Nexus should complete CLASSIFY and CHAIN_SELECT in its own context before spawning any Agent. Do not pre-spawn agents "just in case."

## Best Practices

1. **Default to AUTORUN_FULL**: For most tasks, automatic execution is preferred
2. **Use GUIDED for learning**: When users want to understand the process
3. **Check guardrails**: AUTORUN_FULL includes safety checks at key points
4. **Preserve context**: Use `_STEP_COMPLETE` to maintain chain context
5. **Report progress**: Show clear step indicators during execution

---

## Migration from Copy-Paste

### Before (Manual)
```
/Nexus task → Copy $Agent prompt → Paste to Agent → Copy response → Paste to Nexus → Repeat
```

### After (Automatic)
```
## NEXUS_AUTORUN_FULL
task
```
→ Nexus spawns each agent via Agent tool → Each agent reads its own SKILL.md → Final result

**Key change**: Each agent runs as an independent Claude session with full access to its own expertise, rather than Nexus simulating the agent's role.

---

## Subagent Context Rules

Understanding context inheritance is critical for reliable chain execution:

| Aspect | Behavior |
|--------|----------|
| **Conversation history** | Subagents do not inherit the parent's conversation history. Pass it explicitly via the prompt |
| **Skills** | Subagents do not inherit the parent's skills. Explicit injection via the `skills` field is required |
| **Permissions** | Inherits parent's permission settings. If parent is `bypassPermissions`, so is the child (cannot be overridden) |
| **Auto mode** | When the parent is in `auto` mode, the child's `permissionMode` is ignored |
| **Auto-compaction** | Triggers automatically at ~95% capacity. Can be changed via `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` |
| **Transcript** | Saved to `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl` |
| **Nesting** | Subagents cannot spawn other subagents (one level only) |

---

## Subagent Lifecycle Hooks

You can monitor subagent lifecycles via `settings.json`. Design and implementation with the Latch agent is recommended.

### Chain Execution Monitoring

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/log-agent-start.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/log-agent-stop.sh" }
        ]
      }
    ]
  }
}
```

### Agent Teams Quality Gate (Rally L3)

| Hook Event | Matcher | Purpose |
|-----------|---------|------|
| `TeammateIdle` | — | Just before a teammate goes idle. Use exit 2 to force continued work |
| `TaskCompleted` | — | On task completion mark. Use exit 2 to block completion and send feedback |

### In-Subagent Hooks (frontmatter definition)

Defining `hooks` within a subagent definition file sets hooks that are active only during that subagent's execution.

```yaml
---
name: safe-builder
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-safe-command.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

When a `Stop` hook is defined in frontmatter, it is automatically converted to `SubagentStop`.

---

## Agent Teams Constraints (Rally L3)

Constraints of Agent Teams (requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`):

| Constraint | Impact |
|------|------|
| Experimental feature | Must be explicitly enabled in settings |
| One team per session | Cannot manage multiple teams concurrently |
| No nesting | Teammates cannot create their own teams |
| Fixed leader | The creating session is the permanent leader (cannot be transferred) |
| Session resume limitation | In-process teammates are not restored by `/resume` |
| Permissions fixed at spawn time | All teammates inherit the leader's permission mode |
| Split-pane | Requires tmux or iTerm2 (VS Code Terminal not supported) |
