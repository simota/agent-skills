Purpose: Use this file when you are auditing production failure modes, architecture pitfalls, MCP mistakes, or reasoning-compensation needs in LLM systems.

## Contents
- Production challenge categories
- Architecture anti-patterns
- MCP anti-patterns
- Agent anti-patterns
- Reasoning compensations
- Graceful degradation ladder
- Security threat matrix
- Oracle gates

# LLM Production Anti-Patterns

## Production Challenge Categories

| ID | Category | Mitigation |
|----|----------|------------|
| `LP-01` | hallucination | grounding, citations, low temperature where appropriate |
| `LP-02` | prompt injection | instruction/data separation, sanitization, least privilege |
| `LP-03` | context-window limits | chunking `400-800` tokens, top `5-8` retrieval, summaries |
| `LP-04` | non-determinism | fixed parameters, exact model pinning, logging |
| `LP-05` | cost and latency | model tiering, caching, compression, streaming |
| `LP-06` | bias and fairness | diverse testing, `>20%` deviation flag, quarterly audits |
| `LP-07` | privacy and data leakage | PII masking, tenant isolation, auto-deletion |
| `LP-08` | reasoning limits | tool calls, validation layers, specialist models |

## Architecture Anti-Patterns

| ID | Problem | Fix |
|----|---------|-----|
| `LA-01` | over-complexity | start simplest and escalate only when needed |
| `LA-02` | multi-task per request | one request = one logical task |
| `LA-03` | framework over-reliance | prefer domain-specific tools when warranted |
| `LA-04` | model infallibility assumption | validate all outputs |
| `LA-05` | no output handling | sanitize and schema-validate outputs |
| `LA-06` | floating model names | pin exact versions |
| `LA-07` | over-privileged agents | least privilege and action audit |
| `LA-08` | supply-chain blindness | dependency and server audits |

## MCP Anti-Patterns

| ID | Problem | Fix |
|----|---------|-----|
| `MA-01` | god server | one server = one domain |
| `MA-02` | no input validation | sanitize and validate parameters |
| `MA-03` | unconfirmed state changes | require confirmation and dry-run |
| `MA-04` | secret leakage | never return secrets |
| `MA-05` | missing output schemas | structured outputs for tools |
| `MA-06` | no rate limiting | rate and cost ceilings |

## Agent Anti-Patterns

| ID | Problem | Fix |
|----|---------|-----|
| `AA-01` | god agent | single responsibility |
| `AA-02` | implicit communication | structured interfaces |
| `AA-03` | failure propagation | fault isolation |
| `AA-04` | distributed decisions | orchestration layer |
| `AA-05` | infinite loops | max steps, breaker, ceiling |
| `AA-06` | heavy custom agents | keep agents `<3k` tokens where possible |
| `AA-07` | **cost cascade** — a slow primary is not cancelled when the fallback starts, so both run; a retry above a fallback above a retry multiplies the same request | share one budget across primary *and* fallback, **cancel the superseded attempt**, and count a fallback against the original request's ceiling — not as a fresh one |
| `AA-08` | **tool shopping after a denial** — a refused effect is retried through a broader tool or a differently-shaped call | treat the second attempt as the same denial, not a new request (`nexus/reference/guardrails.md` § Permission Request Envelope) |

## Reasoning Limit Compensations

- arithmetic -> calculator or spreadsheet
- multi-step logic -> structured reasoning plus step verification
- constraint satisfaction -> explicit checker
- temporal reasoning -> date/time tools with current-time context

Core rule: build a system that works despite model flaws.

## Graceful Degradation Ladder

Decide what to lose *before* the outage. Graceful degradation is not keeping the feature alive at any cost — it is pre-deciding, per level, the value that survives, the actions that are forbidden, what the user is told, and what must be true to climb back.

| Level | State | Keeps | Stops |
|-------|-------|-------|-------|
| `L0` | normal | primary model + retrieval + tools, evaluated auto-actions | — |
| `L1` | quality degraded | fallback/small model, shortened context, read-only and drafts | consequential auto-actions, low-priority features |
| `L2` | function degraded | search results, templates, rules, existing FAQ, manual workflow | generated answers |
| `L3` | safe stop | intake queue, human escalation | the feature — serving stale cache or a second provider is worse than stopping |

**Degradation matrix** — one row per trigger, filled before launch:

| Trigger | Keep | Stop | User-visible state | Exit criterion |
|---------|------|------|--------------------|----------------|
| primary model outage | search, fallback-model drafts | auto-actions | limited quality | fallback passes eval, or primary recovers |
| retrieval outage | general explanation, intake | citation-required answers | evidence unavailable | index/source healthy |
| tool outage | draft, plan | execution | execution held | tool health + state reconciled |
| policy engine outage | read-only | external send, writes | safe mode | policy decisions restored |
| semantic-failure spike | search, human queue | auto-generation and auto-action | quality under investigation | canary fix passes eval |
| cost budget exceeded | small model, async | high-cost features | usage limited | budget approved or optimized |

**The failure this prevents:** switching to the fallback model without telling downstream, so a degraded-quality output retains full-authority auto-execution. **Quality degradation must propagate to authority degradation** — every level in the ladder re-states its allowed and disallowed actions, not just its model.

**Safe default ≠ most restrictive default.** Each level offers the user a next action: related documents instead of an answer, a saved draft instead of a send, a diff plus runbook instead of a change, a queue ID and ETA instead of a result. Rehearse the ladder in a game day; a degradation path that has never been executed is a design builder.

## Security Threat Matrix

| Threat | Defense |
|--------|---------|
| prompt injection | instruction/data separation and sanitization |
| unsafe output handling | escaping, sanitization, sandboxing |
| sensitive info disclosure | PII masking and filtering |
| excessive agency | least privilege and approval gates |
| data poisoning | source authentication and quality checks |
| system prompt leakage | externalized secrets and prompt isolation |
| vector weaknesses | access controls and partitioning |

## Oracle Gates

- no output validation -> block at `DESIGN`
- model version not pinned -> require exact version
- no permission design -> require least privilege
- arithmetic or logic task without tool compensation -> add one
- overly broad MCP server -> split by domain
- agent without step cap -> add circuit breaker
- fallback model without a matching authority reduction -> block; degraded quality keeps full auto-action
- no degradation matrix (keep / stop / user-visible state / exit criterion per trigger) -> block at `DESIGN`
