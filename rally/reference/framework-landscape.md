# Multi-Agent Framework Landscape (2026-05 snapshot)

> Purpose: Read this when comparing Rally to other frameworks or deciding whether Rally is the correct execution layer.

## Table of Contents

1. Comparison Matrix
2. Rally Fit
3. Cross-Framework Best Practices
4. Selection Tree

## Comparison Matrix

| Framework | Core style | State management | Parallel support | HITL style | Production readiness (2026-05) | Best fit |
|-----------|------------|------------------|------------------|------------|--------------------------------|----------|
| LangGraph | graph-based workflows with conditional edges | graph state + checkpoints | fan-out and fan-in | interrupts | High — LangSmith observability, checkpointing, streaming; overtook CrewAI in GitHub stars in early 2026 | complex conditional workflows with audit-trail and rollback requirements |
| CrewAI | role-based crews with process types | task chains | sequential or hierarchical | limited | Medium — rapidly growing ecosystem, limited checkpointing | rapid role-driven collaboration; intuitive abstractions |
| AutoGen / AG2 | conversation-driven GroupChat | conversation state | group chat | human proxy patterns | Medium — AG2 rewrite is maturing in 2026 | research-grade multi-agent experimentation |
| Google ADK | hierarchical agent trees + LLM agents | session state | `ParallelAgent` | built-in | Early — backed by Vertex AI; **native A2A protocol** lets ADK agents invoke LangGraph / CrewAI agents through a standard task interface | Google Cloud ecosystems and cross-framework interop via A2A |
| OpenAI Agents SDK | handoff-driven | conversation and session | limited built-in support | guardrails | Medium — OpenAI-native | OpenAI-native applications |
| Claude **Managed Agents** (API, beta `managed-agents-2026-04-01`) | managed harness with multiagent sessions, Outcomes (rubric grader), Memory + Dreaming, Webhooks | sandboxed container per agent, server-sent event streaming | platform-managed fan-out | Outcomes rubric in a separate context window | Beta — fully hosted; pay-per-session | unattended multi-day runs, cross-user knowledge persistence, audit-grade orchestration |
| Claude Agent Teams (Claude Code CLI) | lead + teammates inside one workspace | `TaskList + SendMessage` | `TeamCreate + Task` | `plan` plus approval | Stable inside Claude Code | Rally's execution layer for interactive sessions |

## Rally Fit

### Rally strengths

| Area | Rally advantage |
|------|-----------------|
| Execution environment | native inside Claude Code CLI |
| Writable coordination | `exclusive_write` and `shared_read` discipline |
| Structured communication | `TaskList` and `SendMessage` |
| Lifecycle | `TeamCreate -> TeamDelete` supervision |
| Learning | HARMONIZE and TES |

### Use Rally when

1. work happens inside the Claude Code ecosystem
2. file ownership matters
3. existing skill agents such as Builder, Artisan, or Radar should work as teammates
4. structured task orchestration is required

### Prefer another framework when

| Need | Better fit |
|------|------------|
| rich conditional control flow with audit / rollback | LangGraph |
| role-centric business collaboration; rapid POC | CrewAI |
| research-grade multi-agent experimentation | AutoGen or AG2 |
| Google Cloud alignment, cross-framework interop via A2A | Google ADK |
| OpenAI-native application runtime | OpenAI Agents SDK |
| Unattended multi-day autonomous runs, cross-user memory persistence, platform-level audit | Claude Managed Agents (escalate from Nexus / Rally) |

## Cross-Framework Best Practices

1. Start with a single agent, then justify more orchestration.
2. Begin small; `3-5` agents is a reasonable upper starting point.
3. Separate roles clearly.
4. Pass only the minimum necessary context.
5. Design human checkpoints for high-risk actions.

### Human-in-the-Loop Patterns

| Pattern | Rally implementation |
|---------|----------------------|
| pre-approval | `plan` mode |
| escalation on uncertainty | `Ask first` rules |
| audit after execution | `SYNTHESIZE` |
| staged autonomy | `default` -> `bypassPermissions` |

## Selection Tree

```text
What execution environment are you in?
├─ Claude Code CLI (interactive session)             -> Rally
├─ Anthropic API + need for unattended autonomous    -> Claude Managed Agents
│   runs / cross-user memory / platform audit          (escalate from Rally via Nexus)
├─ Python application
│  ├─ complex conditional flow + audit / rollback    -> LangGraph
│  ├─ role-based collaboration / rapid POC           -> CrewAI
│  └─ research or experimentation                    -> AutoGen or AG2
├─ Google Cloud / cross-framework A2A interop        -> Google ADK
└─ OpenAI API                                        -> OpenAI Agents SDK
```
