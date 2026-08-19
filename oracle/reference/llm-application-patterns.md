Purpose: Use this file when you are choosing agent architecture, MCP design, structured-output strategy, or multi-agent boundaries.

## Contents
- Agent patterns
- Reliability principles
- MCP rules
- Tool and schema design
- Caching and multi-agent rules
- Oracle gates

# LLM Application Patterns

## Agent Architecture Patterns

| ID | Pattern | Best for | Main risk |
|----|---------|----------|-----------|
| `AP-01` | ReAct (Thought → Action → Observation loop) | dynamic reasoning with tool use | loops and drift |
| `AP-02` | Plan-and-Execute (planner + separate executor) | long, auditable multi-step tasks; secure plan-then-execute resists prompt injection by isolating the executor | rigid plans |
| `AP-03` | Specialized Multi-Agent | composite domains | handoff failure |
| `AP-04` | Router | diverse input types | misclassification |
| `AP-05` | Supervisor / Orchestrator | coordinated child agents | bottlenecks |
| `AP-06` | **CodeAct** (model emits Python / TS to call tools and compose actions; "code is the action") | data-shape-heavy or tool-graph-heavy tasks where token-by-token JSON tool calls become brittle | sandbox blast radius — require an isolated runtime |
| `AP-07` | Reflexion (act → self-critique → revise) | tasks where the model can score its own output against an explicit rubric | reflection without ground truth amplifies bias |
| `AP-08` | Tree-of-Thoughts | very hard reasoning where multiple branches must be compared | cost explosion; gate with budget |

Default (2026):
- use **Plan-and-Execute** for predictable multi-step work; default to the "secure plan-then-execute" variant when the input can be attacker-controlled;
- use **ReAct** only for dynamic sub-tasks bounded by a step ceiling;
- use **CodeAct** when the same task in ReAct would require chained JSON tool calls with brittle field plumbing — emit code, run it in a sandbox, observe the result;
- use agents when branching is dynamic, and fixed workflows when the path is predictable.

### Agentic Workflows vs Agentic Loops

The 2026 framing distinguishes **Agentic Loops** (open-ended Think→Act, agent decides everything) from **Agentic Workflows** (structured, stateful, verifiable software modules with bounded planning + bounded execution). Treat workflows as the default and loops as an opt-in for genuinely open-ended sub-tasks. Composio, Microsoft Agent Framework, and OpenAI Agents SDK have all converged on this distinction during 2026.

## Reliability Principles

| Principle | Required behavior |
|-----------|-------------------|
| Structured outputs | JSON schema on all machine-read outputs |
| Validation at every step | pass/fail gate per stage |
| Immutable audit trail | log tool calls and rationale |
| Least privilege | read-only default, minimal tool scope |
| Cost and latency caps | circuit breakers and budget ceilings |

### Failure Modes

| Failure | Detection | Mitigation |
|---------|-----------|------------|
| Format drift | schema validation | structured outputs |
| Plan divergence | step monitoring | bounded reasoning loop |
| Ambiguity loops | loop count | explicit tool-choice schema |
| Silent errors | quality sampling | embedded validation |
| Tool abuse | audit log | usage policy and permissions |
| Cost explosion | spend monitoring | cost ceiling and breaker |
| State corruption | snapshot diff | explicit state handling |

## MCP Design

### Core Primitives

- Tools: actions
- Resources: read-only structured context
- Prompts: reusable templates

### MCP Best Practices

| Rule | Detail |
|------|--------|
| single responsibility | one server = one clear domain |
| secure transport | `stdio` for local, Streamable HTTP for networked |
| idempotent tools | client request IDs and deterministic results |
| pagination | keep list responses small |
| confirmation | require approval for writes, deletes, or spending |
| output schemas | structured outputs for efficient context usage |
| human + model readability | JSON for machines, readable blocks for humans |

### MCP Security

- never pass raw user input without sanitization
- validate tool results before adding them to context
- rate-limit per server
- audit every tool call
- split permissions by capability

## Tool And Structured Output Design

Rules:
- descriptions must say when to call the tool;
- required parameters should be minimal;
- use enums and defaults where possible;
- return actionable error messages;
- validate all outputs with a schema before downstream use.

Scale limits — **tool selection accuracy degrades past 30-50 available tools**, and a multi-server MCP setup can burn ~55k tokens in definitions before any work happens. Past ~10 tools or ~10k tokens of definitions, stop hand-tuning descriptions and switch mechanism: tool search + `defer_loading` (loads only the 3-5 tools a request needs, ~85%+ definition-token reduction, and preserves the prompt cache), programmatic tool calling (many sequential calls collapse into one sandboxed script), or the advisor tool (server-side Plan-and-Execute). Full contract, type strings, and per-tool model-support gotchas → `reference/advanced-tool-use.md`.

## Caching And Multi-Agent Rules

### Cache Strategy

| Strategy | Use case | Expected hit rate |
|----------|----------|------------------|
| exact cache | repeated classification / FAQ | `40-70%` |
| semantic cache | similar chat queries | `10-30%` |
| prompt cache | stable system prompts and tool definitions | up to `90%` input-cost reduction |
| KV cache | multi-turn prefixes | provider-managed |

Prompt-cache traps specific to tool-heavy designs: a changed tool list invalidates the cached prefix (Opus 5 lifts this with the `mid-conversation-tool-changes-2026-07-01` beta), a changed `effort` value invalidates it (effort shapes the rendered prompt — hold it constant within a cached conversation), and `defer_loading: true` tools are excluded from the prefix entirely, so adding them is cache-safe but they cannot carry `cache_control`.

### Multi-Agent Rules

- one agent = one clear responsibility;
- use structured interfaces, not free-form inter-agent prose;
- isolate failures;
- keep orchestration centralized;
- light agents `<3k` tokens are preferred;
- `25k+` custom agents are bottlenecks.

## Streaming And UX

- token streaming for chat
- progressive loading for long generation
- optimistic UI only when downstream semantics are safe
- user cancellation support for long tasks

## Oracle Gates

- no structured-output schema -> block at `DESIGN`
- no per-step validation -> require validation-embedded plan
- no cost cap -> require budget ceiling
- multi-agent design with implicit communication -> require structured interfaces
- attacker-controllable input feeds into a Plan-and-Execute design without a hardened executor (no tool allow-list, no I/O sandboxing) -> block; require the secure plan-then-execute variant
- `AP-06` CodeAct without an isolated runtime (separate process, network egress controls, FS scoping) -> block; CodeAct without sandbox is `LLM-RCE-as-a-feature`


---

## Critical Decision Rules Long Form (SKILL.md excerpt)

| Area | Rule |
|---|---|
| Prompt Engineering | `prompt` | ✓ | Prompt design and optimization | `reference/prompt-engineering.md` |
| Evaluation Framework | `eval` | | Evaluation framework (LLM output quality) | `reference/evaluation-observability.md` |
| Prompt       | use `3-5` few-shot examples only when they measurably help; prefer constrained decoding for structured outputs (reduces iteration rate from `38.5%` to `12.3%`); for Claude, use XML tags (`<instructions>`, `<context>`, `<examples>`) over Markdown for unambiguous parsing — avoid aggressive language ("CRITICAL!", "YOU MUST", "NEVER EVER") which overtriggers newer Claude models and degrades output quality; LLM reasoning performance degrades around `3k` tokens — keep prompt sweet spot at `150-300` words for most tasks; structure prompts for caching: static content first, variable last (`45-80%` cost / `13-31%` TTFT reduction via prompt caching); on current Claude models, adaptive thinking is the mechanism (on by default on Opus 5 / Sonnet 5) — extended thinking / `budget_tokens` is deprecated; the `effort` parameter controls thinking depth (Opus 5 defaults to `high`; `xhigh` is the recommended start for coding/agentic work and cannot be combined with disabled thinking), agentic multi-step loops benefit most; do not add "verify your work" instructions — Opus 5 self-verifies and they cause over-verification |
| RAG          | default to Hybrid Search; keep context to top `5-8` chunks; require `Recall@5 >= 0.8`, `Precision@5 >= 0.7`, `Faithfulness >= 0.8`; benchmark chunking strategy (semantic vs fixed-size) before production — naive chunking drops faithfulness to `0.47-0.51`; validate vector store inputs against poisoning attacks (BadRAG, TrojanRAG per OWASP LLM08) |
| RAG architecture | standard retrieve-then-generate RAG is increasingly obsolete for static corpora `< 1M` tokens — default to Context-Augmented Generation (CAG) unless data changes frequently; for dynamic multi-hop workflows, evaluate Agentic RAG with structured retrieval; hybrid RAG+CAG creates complexity explosion (dual refresh cycles, routing logic, cross-pipeline debugging) — justify before adopting; `40-60%` of RAG implementations fail to reach production — treat retrieval quality, governance, and observability as first-class concerns from day one, not afterthoughts |
| Evaluation   | fixed test sets only; regressions `>= 5%` block merge or rollout; LLM-as-judge needs a different judge model or human calibration; prefer pairwise comparison over single-score for higher consistency; guard against position bias (`40%` GPT-4 inconsistency), verbosity bias (`~15%` inflation), self-enhancement bias (`5-7%` boost); TNR `< 25%` means judges miss invalid outputs — add adversarial test cases; for high-stakes evals, use multi-agent judge debate (multiple judges deliberate, then vote) for higher human alignment than single-judge scoring; LLM judges are vulnerable to adversarial prompt manipulation — validate judge inputs and monitor for score distribution anomalies; for agentic systems, evaluate goal completion rate and tool usage efficiency across multi-step workflows, not just single-turn accuracy; set `max_turns` based on task complexity (`3-5` for focused tasks, `8-10` for multi-step workflows); ensure traceability — link every eval score to the exact prompt version, model version, and dataset version |
| Cost         | budget alert `> 120%`; wasted-token cost target `< 5%`; model routing dispatches to cheapest adequate model (`87%` cost reduction, premium models handle only `~10%` of queries); consider cascade routing (route → escalate on low confidence) for `14%` better cost-quality tradeoffs vs fixed routing; semantic cache: similarity threshold `>= 0.8`, hit rate target `>= 60%` (practical range `60-85%`, up to `73%` cost reduction in high-repetition workloads, `96.9%` latency reduction on cache hits); prompt caching: static prefix first (`45-80%` cost savings); combined techniques deliver `70-90%` total savings |
| Agent design | prefer custom agents `< 3k` tokens; `25k+` agents need redesign; measure compounding layer failure (`95%` per layer = `77%` at 5 layers) across retrieval, reranking, generation, tool calls, and validation; design MCP tools as domain-aware actions (e.g., `submit_expense_report`) not generic CRUD — agents reason better with semantic tool names and descriptive metadata (schema, cost, permissions); keep MCP tool descriptions under `2KB` (Claude Code truncates at this limit) — front-load the most important usage context |
