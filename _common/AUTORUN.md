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

## Internal Role Execution

In AUTORUN mode, Nexus executes each agent's role internally:

```
## Nexus Execution: [Goal]
- Chain: Agent1 → Agent2 → Agent3
- Mode: AUTORUN_FULL

### Executing Step [X/Y]: [AgentName]

_AGENT_CONTEXT:
  Role: [AgentName]
  Task: [Specific task]
  Guidelines: [Key points from AgentName's SKILL.md]

[Execute as AgentName following their methodology]

_STEP_COMPLETE:
  Agent: [AgentName]
  Status: SUCCESS | PARTIAL | BLOCKED
  Output: [Results]
  Next: [NextAgent] | VERIFY | DONE
```

---

## Agent Context Injection

When executing as a specific agent, Nexus should:

1. **Load Agent Personality**: Adopt the agent's philosophy and approach
2. **Follow Agent Process**: Execute according to their defined methodology
3. **Use Agent Outputs**: Generate outputs in the agent's expected format
4. **Respect Boundaries**: Honor the agent's "Always/Ask first/Never" rules

### Example: Executing as Scout

```
_AGENT_CONTEXT:
  Role: Scout
  Task: Investigate login bug
  Guidelines:
    - Start from symptoms, dig to root cause
    - Use 5-Why Analysis
    - Assess impact before recommending fixes

[Scout Investigation]
Symptom: Users cannot log in
→ Why? Invalid session token
→ Why? Token not refreshed
→ Why? Refresh endpoint returns 401
→ Why? Auth middleware rejects expired tokens
→ Root Cause: Token refresh timing issue

_STEP_COMPLETE:
  Agent: Scout
  Status: SUCCESS
  Output: Root cause identified - token refresh timing
  Next: Builder
```

---

## Step Transitions

### Automatic Transition (AUTORUN)

After `_STEP_COMPLETE`, Nexus automatically:
1. Records the completed step
2. Updates context with findings
3. Proceeds to the next agent in chain

### Manual Transition (GUIDED)

After step completion, Nexus:
1. Outputs the `## NEXUS_HANDOFF` block
2. Waits for user to invoke next agent
3. Continues when `## NEXUS_HANDOFF` is provided

---

## Error Handling in AUTORUN

| Error | Level | Action |
|-------|-------|--------|
| Minor issue | L1 | Log and continue |
| Test failure <20% | L2 | Auto-fix attempt |
| Test failure >50% | L3 | Rollback and retry |
| Critical error | L4 | Abort and report |

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
→ Nexus executes all steps internally → Final result

**Key change**: Users no longer need to manually copy-paste between agents.
