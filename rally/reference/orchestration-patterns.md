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

### Rally Mapping

| Orchestration style | Rally pattern |
|---------------------|---------------|
| Concurrent | Frontend/Backend Split, Feature Parallel |
| Sequential | Pipeline |
| Handoff | Specialist Team |
| Group Chat | not Rally default |
| Magentic | not Rally; hand off upstream |
