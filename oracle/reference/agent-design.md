# Agent System Design Reference

Purpose: Design application-level LLM agents — the tool-use loops running INSIDE the user's product. Covers tool-call schemas, context/memory, subagent delegation, termination, and the common failure modes that kill agents in production. Evaluation-first: every agent ships with a goal-completion eval before the loop is widened.

## Scope Boundary

- **Oracle `agent`**: application-level agents. The agent is a feature of the user's product (customer-support copilot, code reviewer, data analyst). Scope = tool-use loop, schemas, memory, termination.
- **Architect (elsewhere)**: designs the SKILL AGENT ecosystem itself — the `.claude/skills/*/SKILL.md` files, inter-agent handoffs, and the Nexus hub. That is a different layer: the agents ARE the SKILL files.
- **Nexus (elsewhere)**: runtime orchestration across already-designed skill agents.

If the user's question is "how do I wire Claude to call my tools and decide when to stop?" → Oracle `agent`. If it is "how should I carve up my skill ecosystem and who hands off to whom?" → `Architect`.

## Core Contract

- Measure goal-completion rate and tool-usage efficiency, not just single-turn accuracy.
- Compounding failure budget: at `95%` per layer, a 5-step agent delivers only `77%` end-to-end — set `max_turns` accordingly (`3-5` focused, `8-10` multi-step).
- Tools are domain-aware actions (`submit_expense_report`), not generic CRUD (`post /records`) — semantic naming improves selection accuracy.
- Keep the system prompt plus tool descriptions under budget. Each MCP tool description under `2KB` (Claude Code truncates beyond this); front-load the most important usage context.
- Custom agents under `3k` tokens outperform sprawling ones; agents above `25k` tokens need redesign.

## Workflow

```
PROFILE   →  name the task: single-turn, multi-step, long-horizon
          →  list candidate tools with read/write/cost/permission tiers
          →  define goal-completion criterion + termination signal
          →  set token budget per turn and max_turns ceiling

DESIGN    →  author tool-call schemas (JSON Schema with descriptions and examples)
          →  choose memory shape: transient / scratchpad / episodic / long-term KV
          →  decide: single-agent loop vs orchestrator + subagents
          →  layer guardrails (input validation, tool allow-list per role, output filter)

EVALUATE  →  run goal-completion eval (not just BLEU / per-step accuracy)
          →  measure tool-call precision / recall / redundant-call rate
          →  inject adversarial prompts + malformed tool outputs
          →  check termination: no-op loops, tool-hopping, premature stop

SPECIFY   →  hand off to Builder with schemas, max_turns, eval gates, rollback plan
```

## Tool-Call Schema Patterns

```jsonc
// Good: domain-aware, typed, explicit cost/permission hints
{
  "name": "submit_expense_report",
  "description": "Submit a finalized expense report for manager approval. Use AFTER user confirms amounts. One call per report. Cost tier: write-low.",
  "input_schema": {
    "type": "object",
    "properties": {
      "report_id": { "type": "string", "description": "UUID from draft_expense_report" },
      "employee_id": { "type": "string" },
      "total_amount_cents": { "type": "integer", "minimum": 0 }
    },
    "required": ["report_id", "employee_id", "total_amount_cents"]
  }
}
```

- Describe WHEN to call, not just WHAT the tool does.
- List pre-conditions (`AFTER user confirms`), idempotency, and cost tier in the description.
- Prefer narrow-scoped tools over generic `execute_sql`.

## Memory Shapes

| Shape | When | Risk |
|-------|------|------|
| Transient (turn-local) | Simple Q&A, retrieval single-shot | Forgets across turns |
| Scratchpad (session-local) | Multi-step reasoning, tool chaining | Grows unbounded — compact at 60% context |
| Episodic (per-session key) | Assistants that resume work | Stale memory leads to wrong actions |
| Long-term KV (cross-session) | Personalization, CRM-style recall | PII governance + drift risk |

Compact aggressively: summarize prior turns when the scratchpad approaches `60%` of the context window. Claude reasoning degrades around `3k` tokens of instructions — do not let accumulated scratchpad crowd the instruction budget.

## Subagent Delegation

Delegate when a subtask has a crisp input-output contract, different tools, or a different quality bar. Do NOT delegate when the orchestrator already has context that would be expensive to rehydrate.

```
orchestrator ──► subagent(retriever)     tools: vector_search, bm25_search
             ├─► subagent(code_writer)   tools: read_file, write_file, run_tests
             └─► subagent(reviewer)      tools: lint, static_analysis
```

Each subagent needs its own `max_turns`, eval, and termination signal. Measure per-subagent failure rate — compounding kicks in at every boundary.

## Termination Conditions

Explicitly declare all three:

1. **Goal reached** — tool returns success / user confirms / structured output validates.
2. **Budget exhausted** — `max_turns` hit, token ceiling hit, wall-clock deadline.
3. **Safety trip** — guardrail fires, tool error rate exceeds threshold, repeated no-op.

Always implement the budget + safety terminators; goal-reached alone is how agents loop forever.

## Common Agent Failure Modes

- **Infinite tool loop** — agent re-calls the same tool with the same args. Detect via hash of (tool, args) across recent turns; break on repeat.
- **Tool-hopping** — model tries every tool before picking one. Mitigate with tool descriptions that specify WHEN, and with `tool_choice: "auto"` plus few-shot selection examples.
- **Context bloat** — prior tool outputs crowd out the instruction. Summarize or drop stale tool results before each turn.
- **Premature stop** — model returns prose instead of calling the next required tool. Mitigate with structured-output termination (schema-validated final answer) not free-text.
- **Permission drift** — agent calls a write tool in a read-only session. Enforce at the server boundary, not in the prompt.
- **Silent tool failure** — tool returns `null` or `""`, agent hallucinates success. Require tools to return explicit status codes.
- **Compounding errors** — 5-layer pipeline at `95%` per layer = `77%` end-to-end. Measure and report each layer.

`90%` of agentic-RAG production projects failed in 2024 on this compounding path (retrieve → rerank → generate → tool-call → validate). Budget for it in `max_turns` and shed layers that do not pay for themselves.

## Handoff

| To | Include |
|----|---------|
| Builder | Tool schemas (JSON Schema), system prompt with XML tags, `max_turns`, memory-compaction rule, termination conditions, eval gates, rollback model |
| Radar | Goal-completion eval suite, adversarial prompt set, tool-call trace harness |
| Sentinel | Tool allow-list per role, prompt-injection defenses on tool outputs, PII-leak tests on memory |
| Beacon | Per-turn tracing spec, tool-latency SLOs, tool-error-rate alert, goal-completion dashboard |
| Architect | If the agent ecosystem (multiple cooperating skill files) itself needs redesign |
