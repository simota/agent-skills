# AI-Generated Code Security & Modern SAST

Purpose: Use this reference when the target code was AI-generated, AI-assisted, or when AI tooling changes the threat model. Also covers modern SAST landscape and hybrid LLM+SAST approaches.

## Scope Boundary

- **This file (`ai-code-security.md`)** — AI-as-**author** risk: source-level flaws introduced by AI-assisted commits (slopsquatting, hallucinated packages, XSS/SQLi/secrets in generated code), threats against the developer's AI tooling itself (Rules File Backdoor, IDEsaster, MCP supply-chain poisoning), and the modern SAST landscape for catching them.
- **Sibling `ai-security.md`** — AI-as-**integration** risk: runtime LLM integration code paths in the product (prompt injection, RAG indirect injection, tool-use boundary, model-output rendering, PII scrubbing, cost/rate limits, OWASP LLM Top 10 2025 mapping).
- **Overlap clarifier — MCP tool security:** discussed here from the *developer-tooling supply-chain* angle (the dev's IDE/agent ingests a malicious MCP server). For the *product-runtime* angle — your app exposes tools to a model and must allowlist/validate/gate them — see `ai-security.md` "Tool use" row and LLM06 Excessive Agency.

Rule of thumb: if the question is "did an AI write this code, and what could go wrong in *the code itself*?" → here. If the question is "does this code *talk to* an AI at runtime, and what could go wrong at *that boundary*?" → `ai-security.md`.

---

## 1. Risk Snapshot (2025-2026)

| Metric | Value |
|--------|-------|
| AI-generated code containing vulnerabilities | 45-62% |
| XSS failure rate (AI-generated) | 86% |
| Vulnerable Java AI-generated code | 72% |
| XSS rate: AI vs human code | 2.74x |
| Organizations that deployed vulnerable AI code | 81% |
| AI share of production code | 24% (29% in US) |
| AI-suggested packages with known CVEs | 44-49% |

Security of AI-generated code has not improved despite functional accuracy improvements through 2025.

---

## 2. AI Coding Tool Threat Model (2025)

### Rules File Backdoor (March 2025)

- Attacker embeds malicious instructions in `.cursorrules` or `.github/copilot-instructions.md` using Unicode invisible characters
- AI assistant follows the hidden instructions and generates backdoored code
- Propagates through forks/clones — entire supply chain at risk
- **Defense:** Code-review rule files, scan for Unicode invisibles, treat rule files as security-critical

### IDEsaster (December 2025)

- 30+ CVEs across GitHub Copilot, Cursor, Windsurf, Zed, Roo Code, Claude Code, Antigravity CLI, and others
- Three-stage attack chain: prompt injection → auto-approved tool calls → IDE feature abuse (data exfiltration, RCE)
- Example: CVE-2025-54135 (CurXecute) — RCE via Cursor
- **Defense:** Minimize auto-approval scope, sandbox AI agents, patch IDEs immediately

### MCP Tool Security

- 13,000+ MCP servers on GitHub as of 2025
- **Tool Poisoning:** Hidden malicious instructions in MCP tool descriptions, invisible to user but processed by LLM
- **Rug Pull:** MCP tool changes its definition after installation (safe Day 1, malicious Day 7)
- **Tool Redefinition:** Malicious MCP server overwrites legitimate tools in multi-server environments
- Critical CVE: CVE-2025-6514 (mcp-remote, CVSS 9.6) — arbitrary OS command execution
- **Defense:** Sandbox MCP servers, validate all inputs/outputs, require human approval for state changes, monitor tool definition changes

---

## 3. Top 10 AI-Specific Anti-Patterns

| Rank | Pattern | Detection |
|------|---------|-----------|
| 1 | Slopsquatting (hallucinated packages) | Registry lookup |
| 2 | XSS (unescaped output) | Output escaping review |
| 3 | Hardcoded secrets | Regex + entropy |
| 4 | SQL injection (missing parameterization) | Query pattern analysis |
| 5 | Authentication failures (broken auth flow) | Structural review |
| 6 | Missing input validation | Boundary check |
| 7 | Command injection (unsafe shell) | Exec pattern detection |
| 8 | Missing rate limiting | Endpoint analysis |
| 9 | Excessive data exposure (API over-returning) | Response field review |
| 10 | Unrestricted file upload | Type/size limit check |

Language tendencies:
- **Java:** highest failure rate (72%), XSS and log injection
- **Python:** shell injection, unsafe deserialization
- **JS/TS:** XSS, prototype pollution, `eval()` patterns
- **Go:** error-handling gaps, race-adjacent logic

---

## 4. AI Code Review Checklist

### Critical

- [ ] No hardcoded secrets
- [ ] Parameterized SQL and NoSQL
- [ ] Output escaped (no raw `innerHTML`)
- [ ] No user input in shell execution
- [ ] Authorization checks present
- [ ] Rule files (.cursorrules, copilot-instructions.md) reviewed for hidden instructions

### High

- [ ] Boundary validation present
- [ ] No sensitive data in error messages
- [ ] Upload type and size limits
- [ ] Minimal API responses (no over-returning)
- [ ] Rate limiting on exposed endpoints

### Medium

- [ ] Packages exist and are maintained (anti-slopsquatting)
- [ ] Licenses are compatible
- [ ] Deprecated APIs removed
- [ ] Logs do not contain secrets

---

## 5. Modern SAST Landscape (2025-2026)

| Tool | Strength | AI Integration |
|------|----------|----------------|
| `Semgrep` | Rule-based, fast, broad language | Assistant Memories (85% FP reduction), AI-Powered IDOR detection |
| `CodeQL` | Semantic queries, GitHub-native | Copilot Autofix (manual time 1.5h → 28min) |
| `Snyk Code` | IDE-native feedback | DeepCode AI, Agent Fix, BOLA detection |
| `Endor Labs` | Reachability + AI-native SAST | 3-agent system (detect/triage/remediate), 95% FP reduction |
| `Opengrep` | OSS fork of Semgrep (LGPL-2.1) | Community-driven, full Semgrep rule compat |
| `SonarQube` | Quality gate + taint analysis | Mixed quality + security |

### Hybrid LLM+SAST Pipeline

```
1. Run Semgrep/CodeQL (breadth + repeatability)
2. Collect context (data flow, call sites)
3. LLM classifies TP vs FP (contextual reasoning)
4. Merged result for prioritization + repair guidance
```

Key insight: rules provide breadth; LLMs provide contextual reasoning; hybrid is better than either alone.

---

## 6. Sentinel Integration

| Phase | AI-security actions |
|-------|---------------------|
| `SCAN` | Detect unsafe AI patterns (eval, innerHTML, string SQL), non-existent packages, auth-flow gaps, rule file tampering |
| `FILTER` | Apply LLM-assisted FP triage, boost confidence from hybrid evidence |
| `PRIORITIZE` | Boost severity for AI-generated code (2.74x XSS baseline) |
| `SECURE` | Apply safer alternatives, defensive patterns |
| `VERIFY` | Confirm fix did not introduce new AI-specific anti-patterns |

**Source:** [Veracode GenAI Code Security Report 2025](https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/) · [Pillar Security: Rules File Backdoor](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents) · [IDEsaster: 30+ AI IDE Flaws](https://thehackernews.com/2025/12/researchers-uncover-30-flaws-in-ai.html) · [Invariant Labs: MCP Tool Poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) · [Semgrep AI-Powered Detection](https://semgrep.dev/blog/2025/ai-powered-detection-with-semgrep/) · [Endor Labs AI SAST](https://www.endorlabs.com/learn/introducing-ai-sast-that-thinks-like-a-security-engineer) · [OpenSSF: Security Guide for AI Code Assistants](https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions) · [OWASP LLM Top 10:2025](https://genai.owasp.org/llm-top-10/)
