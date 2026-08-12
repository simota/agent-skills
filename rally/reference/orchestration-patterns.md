# Multi-Agent Orchestration Patterns

> Purpose: Read this when deciding whether Rally should orchestrate the task, or when choosing a coordination style.

## Table of Contents

1. Architecture Levels
2. Pattern Catalog
3. Supervisor vs Swarm
4. Rally Coordination Patterns
5. Decision Tree

## Architecture Levels

| Level | Use when |
|-------|----------|
| Direct model call | single-step work such as classification or summary |
| Single agent + tools | multi-step work within one domain |
| Multi-agent | cross-domain work or true parallelizable work |

Rule: start with the simplest workable solution, then justify extra orchestration.

## Pattern Catalog

| Pattern | Use when | Avoid when | Rally mapping |
|---------|----------|------------|---------------|
| Sequential | stages depend on previous output | work can safely run in parallel | `Pattern C: Pipeline` |
| Concurrent | independent work can fan out and back in | shared writable state is hard to isolate | `Pattern A` or `Pattern B` |
| Group Chat | brainstorming, debate, or checker loops | strict execution control is required | not Rally's default; keep `<= 3` agents |
| Handoff | the best specialist is unknown at the start | routing is already deterministic | `Pattern D: Specialist Team` |
| Magentic | the solution path is unknown in advance | execution is already well-structured | keep with Nexus or Sherpa |

## Supervisor vs Swarm

| Property | Supervisor | Swarm |
|----------|------------|-------|
| Communication | central hub controls messages | agents talk directly |
| Best for | bounded, auditable tasks | exploratory, autonomous tasks |
| Control | high | low |
| Rally position | current Rally model | not Rally default |

Rally stays in the supervisor lane. Hub-spoke is a deliberate safety choice.

## Rally Coordination Patterns

| Pattern | Rally equivalent |
|---------|------------------|
| Shared Context | `shared_read` files |
| Event-Driven Handoffs | `TaskUpdate` and DM notifications |
| Semantic Contracts | shared type or interface files |
| Single-Writer | `exclusive_write` |
| Conflict Detection | ownership conflict checks |
| Observability | `TaskList` monitoring |
| Checkpoint Management | task statuses and shutdown checkpoints |

## Decision Tree

```text
What kind of task is this?
├─ Single-step -> no Rally
├─ Multi-step but one domain -> single agent + tools
└─ Cross-domain and parallelizable -> consider multi-agent
   ├─ Strict dependency chain -> Sequential
   ├─ Independent work units -> Concurrent -> Rally
   ├─ Debate/checker flow -> Group Chat (<= 3 agents)
   ├─ Specialist unknown -> Handoff
   └─ Solution path unknown -> Magentic -> Nexus or Sherpa
```


---

## Core Contract Long Form (SKILL.md excerpt)

- **Worktree isolation**: Agent Teams assign each teammate its own git worktree — a separate working directory and branch sharing the same repository history. This provides physical file safety: teammates can edit overlapping files without interference. The `ownership_map` remains the logical constraint (who is responsible for what); worktree isolation is the execution mechanism (how conflicts are prevented). TaskCreate, SendMessage, and worktree isolation are the three core coordination primitives.

- **Reconciliation before merge**: after fan-in, validate each teammate's output against the original task specification — not just whether it compiled, but whether it answered what was asked. Silent drift (agent output subtly diverging from intent without errors) is the #1 production failure mode in multi-agent pipelines. Use closed-loop validation (check outputs independently against source requirements, not just against each other) — iterative closed-loop designs neutralize 40%+ of faults versus linear pass-through workflows.

- **Convergence detection**: when all teammates hit the same blocker (e.g., same bug, same failing dependency), parallelism collapses — N agents attempting the same fix produces N conflicting patches. Detect convergence early and diversify task targets (assign different test suites, different compilation targets, or use an oracle/reference implementation to partition the problem space). Anthropic's 16-agent C compiler project demonstrated this: agents compiling the Linux kernel all hit the same bug and overwrote each other until the team diversified targets using GCC as an oracle. [Source: Anthropic Engineering — Building a C compiler with a team of parallel Claudes (https://www.anthropic.com/engineering/building-c-compiler)]

- **Budget guardrails**: set a maximum API cost per session. Agent Teams cost `3-4×` the tokens of a single session; subagents cost `1.5-2×`. Multi-agent frameworks commonly exhibit `1.5-7×` token duplication from repeated context propagation — monitor actual token usage against expected baselines. If parallel speedup does not justify the multiplier, prefer subagents or sequential execution. If collective teammate API calls hit the limit, gracefully degrade (complete in-flight work, skip remaining, report partial results) rather than allowing unbounded spend.

---

## Codex CLI Subagent Orchestration

When running on Codex CLI, Rally uses `spawn_agent` / `wait_agent` / `send_input` / `close_agent` instead of Agent Teams API.

### API Mapping

| Claude Code Agent Teams | Codex CLI Subagents | Notes |
|------------------------|---------------------|-------|
| `TeamCreate` | N/A | No explicit team concept |
| `TeamDelete` | `close_agent` × N | Close all subagents |
| Teammate spawn | `spawn_agent(prompt)` | Returns agent ID |
| `TaskCreate` / `TaskUpdate` | `send_input(id, msg)` | Send task via prompt or input |
| `TaskList` / `TaskGet` | `wait_agent(id)` | Wait for completion |
| `SendMessage` (DM) | `send_input(id, msg)` | Direct message to subagent |
| `SendMessage` (broadcast) | `send_input` × N | Loop over all agents |
| Plan approval | N/A | No plan mode in Codex subagents |

### Codex Subagent Parallel Pattern

```
# SPAWN phase - spawn all workers
worker_a = spawn_agent(prompt: "Following the builder instructions in AGENTS.md, implement email validation...")
worker_b = spawn_agent(prompt: "Following the builder instructions in AGENTS.md, implement phone-number validation...")

# MONITOR phase - wait for all
result_a = wait_agent(worker_a)
result_b = wait_agent(worker_b)

# SYNTHESIZE phase - collect results, detect conflicts
# (Rally handles this internally)

# CLEANUP phase
close_agent(worker_a)
close_agent(worker_b)
```

### Configuration

- `agents.max_depth` (default: 1) — controls subagent nesting depth
- Omitted `spawn_agent` fields inherit from parent session (model, sandbox_mode, etc.)
- `nickname_candidates` — set descriptive names for each worker
