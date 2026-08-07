# Boundaries Rationale

Purpose: full justification and source citations behind the compressed `Never` list in SKILL.md. The SKILL.md list states the rule; this file explains why.

- **Approve MCP servers using broad-scope PATs without flagging** — over-privileged MCP permissions can cascade into shell access and data exfiltration (CoSAI 2025 white paper documents this as a primary MCP attack vector); 66% of scanned MCP servers have at least one security finding (43% shell injection).
- **Ignore tool poisoning risk** — malicious modification of MCP tool metadata/descriptors can redirect agent behavior to compromised endpoints, leading to data leaks or system compromise (Praetorian 2025 research).
- **Accept token passthrough in MCP configurations** — reusing tokens not explicitly issued for a specific MCP server bypasses security controls and breaks audit trails (OAuth 2.1 specification explicitly forbids this).
- **Skip MCP OAuth endpoint validation** — CVE-2025-6514 (mcp-remote, CVSS 9.6) demonstrated that a malicious `authorization_endpoint` URL achieves command injection; always verify OAuth discovery URLs against known-good registries.
- **Trust FastMCP OAuth proxy callbacks without consent verification** — CVE-2026-27124 (FastMCP, patched 3.2.0): missing consent verification in the OAuth proxy callback enables confused-deputy account takeover — an attacker-initiated auth flow can hijack a victim's MCP session (CWE-441). [Source: github.com/PrefectHQ/fastmcp security advisory GHSA-rww4-4w9c-7733, 2026-03-31]
- **Recommend `allow: ["*"]` or equivalent wildcard permissions** — 36.9% of AI CLI tool bugs stem from API/integration/configuration errors (arxiv:2603.20847), and overly permissive settings amplify their blast radius.
- **Accept CLAUDE.md files >300 lines without flagging** — instruction-following quality degrades uniformly as instruction count exceeds ~150-200 (Arize research, Anthropic best practices).
- **Accept MCP Dynamic Client Registration (DCR) endpoints without verification** — compromised DCR endpoints enable token theft; always validate DCR discovery URLs against known-good registries.
- **Accept MCP OAuth tokens without RFC 8707 resource indicators** — the MCP 2026-03-15 specification mandates resource parameter inclusion in both authorization and token requests to prevent token mis-redemption; tokens without resource binding can be replayed against unintended servers.
- **Accept third-party marketplace plugins with auto-update enabled without flagging** — auto-updating third-party plugins can introduce supply chain attacks; flag for manual version review and source trust verification.
