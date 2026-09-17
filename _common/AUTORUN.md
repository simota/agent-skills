# AUTORUN Protocol

> **Tier:** `spine` — in effect on every run. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

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

In AUTORUN mode, Nexus delegates each specialist step through the verified host interface, preserving independent contexts and the existing authority boundary.

The canonical outcome brief is defined once in `nexus/reference/hub-authoring.md` § Agent Spawn Template. Carry its ACs, scope, authority, prohibited outcomes and completion bound; tool directions are conditional and forced-thinking directives are retired.

### Execution Layers

`nexus/reference/execution-layers.md` defines L1 direct, L2 parallel and L3 coordinated execution. Bind actual tools through `_common/CLI_COMPATIBILITY.md`; do not infer API names or capability from another CLI. Join dependencies, isolate writers and keep independent verification.

### Model Selection

Follow `nexus/reference/hub-authoring.md` § Model Selection and `_common/CLI_COMPATIBILITY.md` §4. Inherit the authorized model/effort, verify current stable alternatives when needed, and never escalate cost or permissions automatically.

**Context Strategy** (orthogonal to model choice): `reset` = file-based handoff (fresh context per agent), `continuous` = in-context handoff (accumulated context), `hybrid` = Nexus continuous + spawned agents reset. Typical pairing — investigation/evaluator → `reset`, standard implementation → `hybrid`, high-complexity design/revision generator → `continuous`. See `nexus/reference/context-strategy.md` for details.

### Advanced Spawn Options

Use only supported host options for capacity/turn limits, effort, isolated workspaces, resume, skill injection and memory. Do not copy custom-agent frontmatter into SKILL.md. An isolated worktree prevents direct write collisions, not semantic conflicts; verify the merged revision and inherited constraints. No permission-mode changes are implied by AUTORUN.


## Agent Context Injection

When spawning an agent, Nexus provides context through the prompt:

1. **SKILL.md Path**: Tell the agent to read its own SKILL.md first
2. **Task Description**: Clear, specific task with acceptance criteria
3. **Handoff Context**: Results from previous steps in the chain
4. **Constraints**: Guardrail level, file ownership, scope limits
5. **Output Format**: Request `_STEP_COMPLETE` format in the response

The spawned agent reads its own SKILL.md and follows its own methodology autonomously. Nexus does not need to simulate the agent's personality or process.

## Default Completion Schema

When `_AGENT_CONTEXT` is supplied, read its task, context and constraints, execute the owning skill's workflow, and emit `_STEP_COMPLETE`. Use a skill-specific schema when one is explicitly supplied; otherwise use the default below. `Agent` is the current owner, not a hard-coded specialist. Skipped validation is reported, never counted as passed.

```yaml
_STEP_COMPLETE:
  Agent: <owner>
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact]
    parameters:
      task_type: "[task type]"
      scope: "[scope]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Next: [recommended next agent or DONE]
  Reason: [Why this next step]
```

`Next` recommends a transition; it does not delegate permission or bypass the hub's routing and project-local availability gates. Spawn mechanics and examples are owned by `nexus/reference/hub-authoring.md`, with host syntax bound through `_common/CLI_COMPATIBILITY.md`.

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

**Defined in `nexus/reference/guardrails.md` § Guardrail Levels** — L1 MONITORING · L2 CHECKPOINT · L3 PAUSE ·
L4 ABORT, together with the goal-impact classification rule that decides minor vs major. Read the levels
there; this file supplies only the trigger→action catalog below. Do not restate the level semantics here —
the two copies contradicted each other for as long as both existed.

### Triggers by Level

Per the classification rule in `guardrails.md`: **minor** = the step's goal is still reachable by a local fix
→ attempt the fix and continue; **major** = it is not → stop and reconsider. The percentages below are rough
guidelines, not fixed thresholds.

**L1 — MONITORING**

| Trigger | Action |
|---------|--------|
| `lint_warning` | Log, continue |
| `minor_deprecation` | Log, continue |
| `style_inconsistency` | Log, auto-fix if possible |
| `coverage_decrease` (minor — goal unaffected; ~<5% guideline) | Log, continue |

**L2 — CHECKPOINT**

| Trigger | Action |
|---------|--------|
| `test_failure` (minor — goal reachable by local fix; ~<20% guideline) | Auto-fix attempt → retest (max 3) |
| `security_warning` (non-critical) | Add Sentinel scan |
| `type_error` | Auto-fix attempt (max 2) |
| `performance_regression` (minor; ~<10% guideline) | Log, optional Bolt |
| `dependency_vulnerability` (Low/Medium) | Log, suggest update |

**L3 — PAUSE**

| Trigger | Action |
|---------|--------|
| `test_failure` (major — goal not reachable by local fix; ~>50% guideline) | Rollback, re-decompose with Sherpa |
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

You can monitor subagent lifecycles via `settings.json`. Design and implementation with Hone's hooks Recipes is recommended.

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

## Lifecycle

- **failure:** F1: fixed generation directives and automatic permission bypass contradicted runtime-scoped authority.
- **effect:** Authorization and completion gates remain while engine-specific details use the compatibility adapter.
- **owner:** Nexus
- **removal:** Retire adapter references only when an equivalent runtime contract preserves scoped permissions, mode gates and completion checks.
