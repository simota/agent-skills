Purpose: Use this file when you are designing guardrails, reviewing OWASP LLM risks, or defining hallucination, bias, and PII controls.

## Contents
- OWASP LLM Top 10
- Defense-in-depth guardrails
- Hallucination and grounding
- Agent and MCP safety
- Identity as an attack surface
- PII and bias handling
- Oracle gates

# AI Safety And Guardrails

## OWASP Top 10 For LLM Applications (2025)

| ID | Threat | Key mitigations |
|----|--------|-----------------|
| `LLM01` | Prompt Injection | instruction/data separation, input sanitization, pattern blocking |
| `LLM02` | Sensitive Information Disclosure | input/output validation, PII masking |
| `LLM03` | Supply Chain | verified sources, integrity checks, signed SBOM |
| `LLM04` | Data Poisoning | provenance tracking, trusted-source validation |
| `LLM05` | Improper Output Handling | output sanitization, context-aware encoding, sandboxing |
| `LLM06` | Excessive Agency | least privilege, approval gates, action audit |
| `LLM07` | System Prompt Leakage | keep secrets external, prompt isolation |
| `LLM08` | Vector And Embedding Weaknesses | access controls, partitioning, source validation |
| `LLM09` | Misinformation | verified-source grounding, cross-checks, human review |
| `LLM10` | Unbounded Consumption | rate limits, timeouts, resource monitoring |

## Defense In Depth

Pipeline:
1. input guardrails
2. model call
3. output guardrails

### Input Guardrails

- prompt-injection detection
- PII detection and pre-LLM redaction
- topic boundary checks
- input-length ceilings
- rate limiting

### Output Guardrails

- factuality or citation checks
- PII redaction
- output sanitization
- format validation
- confidence thresholds

## Hallucination Controls

| Strategy | Reliability |
|----------|-------------|
| source attribution | High |
| retrieval verification | High |
| entailment / NLI checks | High |
| self-consistency | Medium-High |
| self-scored confidence | Medium |

Grounding rules:
- answer only from provided context;
- cite factual claims;
- state uncertainty explicitly;
- do not extrapolate beyond source evidence.

Faithfulness targets:
- Faithfulness `> 0.95` for grounded production answers
- Answer relevancy `> 0.85`
- Context precision `> 0.80`
- Context recall `> 0.80`

## Agent And MCP Safety

- least privilege by default
- human approval for state changes, external actions, or spending
- tool-call audit logs
- one bounded responsibility per agent
- cost and time caps per execution

MCP-specific:
- OAuth 2.1 for HTTP transport
- never echo secrets
- validate parameters before execution
- require confirmation for state-changing or cost-incurring actions
- offer dry-run mode for destructive actions

## Identity As An Attack Surface

`LLM01` covers instruction injection. The rest of this surface is what an attacker reaches when the
agent decides **who it is, who is speaking, and what it already agreed to** from natural language.
Six entry points; the last three are the ones a prompt-injection checklist usually misses:

| Surface | The attack | The control |
|---|---|---|
| `instruction` | user / admin / developer / fetched-content instructions share one context | provenance tags, instruction-vs-data channel separation |
| `identity` | "this is from the administrator", a low-privilege agent signing as a high-privilege one | authenticated subject + scope + audience + expiry; never a name in prose |
| `memory` | poisoned or wrong facts persisted, then read back as established | typed writes with source and expiry (`reference/agent-design.md` § Memory governance) |
| `tool` | tool output and instruction arrive in the same string | schema-validated arguments, narrow tools, output treated as data |
| `relationship` | trust, intimacy, urgency, or authority used to relax a boundary | relationship may affect explanation and ordering, **never authentication or permission** |
| `update` | model, prompt, policy, or connector change shifts safety properties silently | behavior-regression suite per bundle change, not per prompt edit |

**Relationship must not convert into permission.** "A long-standing user, so skip the confirmation",
"an angry customer, so exceed the refund cap", "they always help me, so disclose it" are the same bug
in three costumes. A known caller may earn *less re-explaining*; it never earns *less authentication*.

**Typed memory is a boundary, not a schema preference.** Free-text persona/preference memory and
permission, approval, or identity facts do not share a store. A conversational sentence — "the admin
approved this" — must not be promotable into permission memory; only a signed authorization event is.
Follow the write rules in `reference/agent-design.md` § Memory governance; the addition here is that
`model_generated` and `source_type` are load-bearing fields, and high-impact entries require
`model_generated: false`.

**Diagnose an "it started behaving strangely" report in effect order, not symptom order.** Tone is the
last thing to look at, and severity is set by effect, rights, and recoverability — never by how
off-brand the output read:

1. did any real effect occur (send, purchase, delete, permission change, disclosure)
2. which agent ID and version executed it
3. what permission, approval, and credential were in force
4. which memory was read, and what was written
5. what the provenance of the inputs was, external content included
6. what changed in model / prompt / policy / connector / UI
7. reproduce in isolation, then contain (stop, quarantine, revoke)
8. recover (undo or compensate, notify, regression test, record residual risk)

Steps 1-6 answer whether the cause was injection, memory poisoning, a silent model update, or a UI
identity display — four different fixes that all present as "the persona changed".

[Source: AgentDojo (Debenedetti et al., 2024) for the indirect-injection surface; OWASP Agentic
Application Top 10 for the agentic framing — see `probe/reference/llm-agent-security-2026.md`]

## PII Handling

| Category | Action |
|----------|--------|
| direct identifiers | redact before LLM |
| contact info | redact or mask |
| financial data | redact before LLM |
| health data | redact before LLM |
| names | context-dependent handling |

Rules:
- preserve reversible mapping only if a legitimate downstream need exists;
- keep tenant isolation and data residency requirements explicit.

## Bias Evaluation

| Dimension | Flag threshold |
|-----------|----------------|
| gender | `> 20%` variance |
| race / ethnicity | `> 20%` variance |
| age | `> 20%` variance |
| socioeconomic context | `> 20%` variance |

Cadence: quarterly audits for production systems.

## Compliance Baseline

- trace prompt/model/dataset versions
- retain immutable audit trails
- apply PII masking and tenant isolation
- require human approval for high-risk decisions
- disclose AI involvement where regulation requires it

## Oracle Gates

- no output validation -> block at `DESIGN`
- no prompt-injection defense -> require input guardrails
- no least-privilege design -> block at `DESIGN`
- secrets inside system prompts -> externalize
- no PII handling -> require redaction strategy
