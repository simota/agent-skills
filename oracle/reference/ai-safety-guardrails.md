Purpose: Use this file when you are designing guardrails, reviewing OWASP LLM risks, or defining hallucination, bias, and PII controls.

## Contents
- OWASP LLM Top 10
- Defense-in-depth guardrails
- Hallucination and grounding
- Agent and MCP safety
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
