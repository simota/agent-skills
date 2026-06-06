# OWASP API Security Top 10 2023

Purpose: Use this file when API scope exists and you need a concise test strategy for API1-API10, including manual-vs-automated priority and Probe-specific emphasis.

> **Currency note (2026-05)**: OWASP API Security Top 10 **2023** remains the active, published edition — there is no successor list yet (the next refresh cycle is in active community discussion at `owasp.org/API-Security/`). Treat the 2023 numbering as authoritative. For complementary AI/agent surfaces, pair with **OWASP Top 10 for LLM Applications 2025 v2.0** (released 2024-11-18) and **OWASP Top 10 for Agentic Applications** (released 2025-12-09, see `reference/llm-agent-security-2026.md`).
> **BOLA prevalence update (2026-02)**: Wallarm's *2026 API ThreatStats Report* found that **43% of all 2025 additions to CISA KEV (106 / 245) were API-related**, **97% of API vulns are exploitable in a single request**, and **52% of disclosed API breaches in 2025 traced to broken authentication**. BOLA remains the #1 risk by attack volume.

## Contents

- API1-API10 summary
- Test emphasis by risk
- Automation and manual split
- Probe quality gates

## API1-API10 Summary

| Risk | Name | Severity | Probe priority |
| --- | --- | --- | --- |
| `API1` | Broken Object Level Authorization (`BOLA`) | `CRITICAL` | Highest |
| `API2` | Broken Authentication | `CRITICAL` | Highest |
| `API3` | Broken Object Property Level Authorization (`BOPLA`) | `HIGH` | High |
| `API4` | Unrestricted Resource Consumption | `HIGH` | High |
| `API5` | Broken Function Level Authorization (`BFLA`) | `HIGH` | High |
| `API6` | Unrestricted Access to Sensitive Business Flows | `HIGH` | High |
| `API7` | Server Side Request Forgery (`SSRF`) | `HIGH` | High |
| `API8` | Security Misconfiguration | `MEDIUM-HIGH` | Medium |
| `API9` | Improper Inventory Management | `MEDIUM` | Medium |
| `API10` | Unsafe Consumption of APIs | `MEDIUM` | Medium |

## Test Emphasis By Risk

| Risk | What to test | Automation | Manual need |
| --- | --- | --- | --- |
| `API1` `BOLA` | Object ID tampering, UUID predictability, ownership checks | Partial | Required |
| `API2` | JWT handling, lockout, MFA gaps, reset flows | Partial | Required |
| `API3` `BOPLA` | Mass assignment, excess response data | Partial | Required |
| `API4` | Rate limits, payload size, pagination abuse | Good | Recommended |
| `API5` `BFLA` | Admin endpoints, method switching, role escalation | Partial | Required |
| `API6` | Coupon abuse, bots, scraping, business-flow abuse | Weak | Required |
| `API7` `SSRF` | Internal URL fetch, metadata endpoints, redirect bypass | Good | Recommended |
| `API8` | CORS, headers, defaults, debug exposure | Good | Recommended |
| `API9` | Old versions, shadow APIs, deprecated assets | Partial | Required |
| `API10` | Unsafe third-party API trust, schema mismatch, weak validation | Weak | Required |

## Probe-Specific Defaults

- Always include `API1` / `BOLA` when API scope exists.
- Prioritize `API1`, `API2`, `API5`, and `API7` before medium-priority misconfiguration checks.
- Treat `API6` and `API10` as business-context-heavy: automation is not enough.
- When the API exposes LLM-backed endpoints (chat, RAG, agent tool-call surfaces), cross-test with **OWASP Top 10 for LLM 2025 v2.0** (LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM06 Excessive Agency, LLM08 Vector and Embedding Weaknesses) and **OWASP Top 10 for Agentic Applications 2025** (ASI01 Agent Goal Hijacking, indirect instruction injection via RAG content). Wallarm's *2026 API ThreatStats* found **36% of AI vulnerabilities overlap with API vulnerabilities** and MCP-related vulns grew 270% Q2-Q3 2025.

## Quality Gates

| Condition | Required action |
| --- | --- |
| `BOLA` not tested | Warn; this is the most common API attack family |
| Only automated API scanning used | Add manual authorization and business-flow tests |
| Auth context missing | Mark coverage as partial |
| No inventory/version review | Warn for `API9` blind spot |
