Purpose: Use this file when you are auditing production failure modes, architecture pitfalls, MCP mistakes, or reasoning-compensation needs in LLM systems.

## Contents
- Production challenge categories
- Architecture anti-patterns
- MCP anti-patterns
- Agent anti-patterns
- Reasoning compensations
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

## Reasoning Limit Compensations

- arithmetic -> calculator or spreadsheet
- multi-step logic -> structured reasoning plus step verification
- constraint satisfaction -> explicit checker
- temporal reasoning -> date/time tools with current-time context

Core rule: build a system that works despite model flaws.

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
