# LLM and Agentic Application Security — 2026 Reference

Purpose: Use this file when the Probe target embeds an LLM endpoint, a RAG retriever, an agentic / tool-calling workflow, or an MCP (Model Context Protocol) server. Defines the authoritative top-10 lists, mandatory dynamic checks, and tooling for 2026-05.

> Scope clarification: This file covers **runtime / DAST** validation of LLM and agent endpoints. Static review of prompts, model configs, and tool registries belongs to Sentinel. RAG / retrieval architecture design belongs to Seek. AI/ML evaluation, prompt engineering, and MLOps belong to Oracle. Probe attacks the deployed system to confirm exploitability.

## Active Authoritative Lists (2026-05)

| List | Version | Released | Source |
| --- | --- | --- | --- |
| OWASP Top 10 for LLM Applications | **v2.0 (2025 edition)** | 2024-11-18 | `genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/` |
| OWASP Top 10 for Agentic Applications | **1st edition** | 2025-12-09 | `genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-...` |
| OWASP API Security Top 10 | **2023** (still current) | 2023-06 | `owasp.org/API-Security/` |
| OWASP Top 10 (Web) | **2025** (RC announced 2025-11-06 at Global AppSec DC) | 2025-11 | `owasp.org/Top10/2025/` |

> **Why this matters for Probe**: Wallarm's *2026 API ThreatStats Report* (2026-02-17) found **2,185 AI-related vulnerabilities in 2025**, of which **786 (36%) overlap with API vulnerabilities**. **315 MCP-specific vulnerabilities** were tracked with 270% Q2→Q3 growth. Any API engagement that excludes the LLM / agent layer now systematically under-reports risk.

## OWASP Top 10 for LLM Applications 2025 (v2.0)

| ID | Risk | Probe primary dynamic check |
| --- | --- | --- |
| LLM01 | Prompt Injection | Direct payloads (`Ignore prior...`), system-prompt extraction probes |
| LLM02 | Sensitive Information Disclosure | Coax model to reveal system prompt, secrets, embedded PII |
| LLM03 | Supply Chain | Model / adapter / dataset provenance; signed weights |
| LLM04 | Data and Model Poisoning | Poisoned fine-tune / RAG corpus / feedback loop validation |
| LLM05 | Improper Output Handling | Downstream sink injection (XSS from model output, SQL from generated query) |
| LLM06 | Excessive Agency | Tool-call scope, allow-list enforcement, dry-run vs execute |
| LLM07 | System Prompt Leakage | Side-channel extraction, error-message leak |
| LLM08 | Vector and Embedding Weaknesses | RAG poisoning, embedding inversion, authz on retrieval |
| LLM09 | Misinformation | Output groundedness, citation verification |
| LLM10 | Unbounded Consumption | Token-bomb, recursive prompts, context-window saturation |

## OWASP Top 10 for Agentic Applications (2025-12)

The OWASP GenAI Security Project released the inaugural list on 2025-12-09. It targets autonomous AI systems with goals, memory, tools, and the ability to act across systems. Cited identifiers are widely referenced as `ASI##` (Agentic System Issue) — confirm exact numbering against the OWASP source before publishing the final Probe report.

| ID | Risk | Probe primary dynamic check |
| --- | --- | --- |
| ASI01 | **Agent Goal Hijacking** | Plant indirect-injection payloads in tool outputs / RAG content / emails; observe whether agent goal mutates. EchoLeak-style copilot exfiltration is the canonical real-world example. |
| (others) | Tool / Memory / Cascade / Identity / Privilege / Trust risks | See OWASP source for the full 10; map each to a runtime probe before claiming agent coverage. |

> The numbering and titles of items beyond ASI01 are evolving in vendor write-ups; **always cite directly from `genai.owasp.org`** in the final report rather than relying on a third-party summary.

## MCP (Model Context Protocol) Specific Checks

When the target exposes an MCP server (HTTP or stdio):

- **`tools/list` enumeration without auth** — confirm the server requires auth or scopes the tool catalogue per identity.
- **Tool-name shadowing** — register a tool with the same name as a trusted one; verify the client refuses or warns.
- **Tool-description injection** — embed adversarial prompts in the tool description; verify the agent does not execute them as instructions.
- **`resources/read` traversal** — request paths outside the documented resource roots.
- **`prompts/list` exposure** — system prompts leaking via prompt registry.
- **Unauthenticated session establishment** — the spec recommends but does not mandate per-session auth; confirm deployment-level enforcement.

## Recommended Tooling (2026-05)

| Tool | Role | Version pin |
| --- | --- | --- |
| **Garak** (NVIDIA, OSS) | LLM vulnerability scanner — 37+ probe modules covering prompt injection, jailbreaks, toxicity, hallucination, data leakage | `v0.14.0` (2026-02) |
| **PyRIT** (Microsoft, OSS) | Multi-turn / multi-modal red-teaming; crescendo, TAP attack chains; integrates with Azure AI Foundry | Track `github.com/Azure/PyRIT/releases` |
| **Promptfoo** | 50+ vulnerability types, CI/CD-first integration; OWASP LLM Top 10 and Agentic Top 10 plugins | Track `promptfoo.dev/docs/red-team/owasp-agentic-ai/` |
| **DeepTeam** (Confident AI) | LLM red-teaming framework with OWASP Top 10 for LLM and Agentic plugins | Track `trydeepteam.com/docs/frameworks-...` |
| **Akto** | Agent / API security platform with agentic-AI testing module | `github.com/akto-api-security/akto` |

## Workflow (LLM / Agent Slice)

```
PLAN      → confirm scope: which LLM endpoints, which tools / MCP servers, which RAG corpora
          → declare attack classes: direct-PI, indirect-PI, goal hijack, data poisoning, excess agency
          → mandatory: 2+ identities (low-priv user, privileged user) for authz tests
          → AI safety: tests are run against a non-production / sandboxed model where possible

SCAN      → Garak default probe set (LLM01-LLM10 coverage)
          → PyRIT multi-turn jailbreak chains where scoped
          → Indirect injection: plant marker text in RAG-ingestable docs; observe agent
          → Tool-call boundary: invoke disallowed tools / out-of-scope arguments
          → MCP enumeration + tool-shadow test
          → Vector store: poisoned-doc retrieval + authz cross-tenant probe

VALIDATE  → reproduce each finding with the smallest payload
          → label Confirmed vs Unconfirmed (LLM behavior is stochastic — require N≥3 reproductions before "Confirmed")
          → CVSS v4.0 with Threat metric reflecting public PoC availability

REPORT    → per-finding: payload, response, attack chain, CVSS, SLA, remediation
          → handoff: Builder (fix), Oracle (model / safety-tuning), Sentinel (static prompt audit), Cloak (PII exposure)
```

## Stochasticity and Proof Standards

LLM outputs are non-deterministic. Probe MUST:

- Run each confirming payload **at least 3 times** with `temperature` set to the production value (and again at `temperature=0` when feasible).
- Report success rate (e.g. `3/3`, `2/5`) — single-shot success is "Unconfirmed".
- Capture full prompts, responses, model name, version, and `temperature` / `top_p` parameters as evidence.
- Pin model identifiers (e.g. `gpt-5.1-2026-03`, `claude-opus-4-7@20260415`) — silent model upgrades invalidate prior reports.

## Anti-Patterns

- Testing only the chat UI and skipping the backend tool registry — most agent damage is via tool execution, not text output.
- Relying on a single benign jailbreak (`DAN`) — modern guardrails block these; use Garak / PyRIT for current-generation chains.
- Treating a passing Promptfoo / Garak CI run as proof of safety — these tools are upper-bound checks. Manual red-teaming is required for high-impact agents.
- Forgetting MCP — many 2025-2026 deployments expose tool catalogues without auth because the spec is permissive.
- Confusing LLM02 (model leaks data) with API3 / BOPLA (API leaks data) — both apply to LLM-backed APIs.

## Handoff

- **→ Builder**: confirmed exploit + remediation pattern (output filter, tool allow-list, prompt-shielding library) + SLA.
- **→ Oracle**: when fix requires model fine-tuning, safety-tuning, or RAG-retrieval redesign.
- **→ Sentinel**: static prompt / config audit for similar issues in source.
- **→ Seek**: when RAG retrieval / vector store authz is structurally broken.
- **→ Cloak**: when LLM leaks PII or training-data secrets — GDPR / CCPA notification clock starts.
- **→ Triage**: critical (e.g. agent confirmed to exfiltrate via tool call, ASI01 reproducible at `≥ 80%`).
- **→ Vigil**: convert confirmed payloads / tool-call patterns into Sigma / detection rules.
