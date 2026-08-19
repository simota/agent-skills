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

### Memory governance — what may enter, what must leave

The shapes above say where memory lives, not what is allowed into it. Without an admission rule, a store fills
with the agent's own guesses and then returns them as facts to a later session that has no way to tell them
apart from observations. Classify every write:

| Class | Content |
|-------|---------|
| `allow` | Explicit user preference · reviewed convention · reusable debugging fact **with its source** · reference to an accepted decision |
| `deny` | Secrets · raw personal data · **unverified model inference** · transient runtime state · third-party instructions |
| `require_review` | Security exceptions · legal interpretation · anything crossing a tenant or policy boundary |

`unverified model inference` is the load-bearing denial: it is the only entry that looks identical to a fact
once written, and it is what turns a memory store into a citation-free authority.

**The class only holds if the record carries it.** A free-text note cannot be re-classified later, so the
fields are the control:

```yaml
record_id:        M-2026-0001
type:             user_preference        # task_state | preference | commitment | episodic | policy_state | incident
value:            "fewer bullet lists in answers"
source:           explicit_user_setting
source_id:        S-8821                 # session, approval, or document reference
confidence:       confirmed              # confirmed | observed | inferred
scope:            user_account           # subject and boundary this entry is valid within
valid_from:       2026-08-17
expires_at:       null
writable_by:      user_or_settings_service
readable_by:      approved_agents
model_generated:  false
```

Two rules the fields exist to enforce. **A sentence in a conversation cannot become a permission.**
"The admin approved this" is episodic content about a claim, never an entry of type `policy_state`;
only a signed authorization event promotes to that type, and high-impact entries require
`model_generated: false`. And **inferred profiles carry four constraints** — a stated purpose (tuning
explanation difficulty and selecting a sales target are not one purpose), user visibility (no hidden
trait labels), correctability with explicit settings outranking inference, and a use ceiling that keeps
them out of pricing, hiring, credit, and clinical decisions. Prefer "you set low-risk options last
time" over "you're a cautious person": same personalization, stated source and scope, no fixed label.

**Retirement is part of the contract.** Eight triggers, any one of which retires an entry — TTL reached ·
source deleted · source updated · user deletion request · project ended · scope changed · contradiction
detected · reclassified as sensitive. A ninth, weaker one: unused and expensive to keep current.

Distinguish the three exits, because they mean different things to a reader: **hard-delete** (must not
survive — secrets, personal data), **tombstone** (retained as "this was retracted", so a later session does
not re-derive it), **archive** (out of the live path, still auditable).

**Before trusting a claim carried across a session boundary, ask four questions:** does a source reference
exist · is that source version still current · is its authority sufficient for this decision · does it
contradict the current authoritative contract. Any "no" quarantines the claim — it does not inform the
current decision, the entry is corrected or removed, and the contradiction is recorded. This is a different
boundary from untrusted external input (`_common/WEB_FETCH_SAFETY.md`): here the stale belief is *your own*.

## Subagent Delegation

Delegate when a subtask has a crisp input-output contract, different tools, or a different quality bar. Do NOT delegate when the orchestrator already has context that would be expensive to rehydrate.

```
orchestrator ──► subagent(retriever)     tools: vector_search, bm25_search
             ├─► subagent(code_writer)   tools: read_file, write_file, run_tests
             └─► subagent(reviewer)      tools: lint, static_analysis
```

Each subagent needs its own `max_turns`, eval, and termination signal. Measure per-subagent failure rate — compounding kicks in at every boundary.

## Authority Envelope

Autonomy is not a capability level — it is an **effect** level. The same model reading documents and the same model merging code, sending mail, and issuing refunds are different systems at identical reasoning quality. Design the envelope before the model, and review it before the model: `Authority Envelope → worst single action → worst hour → worst tenant`, then pick a model.

**The grant axes are defined once, in `nexus/reference/autonomy-quality-protocol.md` §8** — the seven axes
(`resource · action · quantity · time · destination · approval · reversibility`), the denial default (an axis
you do not name is denied, not unlimited), the tiered budget, the shrink-the-tool rule, the secret-handling
path, the agent-identity-is-not-user-identity rule, and why read-only is not safe by construction. Grant
against that list; do not restate it here — a second copy of a permission vocabulary drifts into a *narrower*
one, and the axis it loses is the one nobody notices was missing.

What this file adds is the sequence above, not the vocabulary. Why the axes rather than a tool list:
`send_email` to an internal draft and `send_email` to an external recipient with attachments are the same
tool at different effect, so a per-tool allow/deny list cannot express the envelope and the axes can.

Secrets already leaked into code, issues, CI logs, or chat must be caught at ingestion, before composition —
the one intake concern the general rule does not cover, because it is upstream of any grant.

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

Compounding failures across retrieve → rerank → generate → tool-call → validate can dominate end-to-end reliability even when each layer looks strong in isolation. Budget for this in `max_turns`, measure every transition, and shed layers that do not pay for themselves.

## Handoff

| To | Include |
|----|---------|
| Builder | Tool schemas (JSON Schema), system prompt with XML tags, `max_turns`, memory-compaction rule, termination conditions, eval gates, rollback model |
| Radar | Goal-completion eval suite, adversarial prompt set, tool-call trace harness |
| Sentinel | Tool allow-list per role, prompt-injection defenses on tool outputs, PII-leak tests on memory |
| Beacon | Per-turn tracing spec, tool-latency SLOs, tool-error-rate alert, goal-completion dashboard |
| Architect | If the agent ecosystem (multiple cooperating skill files) itself needs redesign |
