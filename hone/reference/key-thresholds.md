# Hone — Key Thresholds Reference

**Purpose:** Authoritative thresholds Hone applies during AUDIT. SKILL.md keeps a summary table; this file holds the full text + rationale + source citations.

**Read when:** Auditing CLAUDE.md / GEMINI.md / AGENTS.md size, settings hierarchy, hooks, MCP transport, plugins, or prompt cache hierarchy.

---

## Instruction file sizing

- **CLAUDE.md / GEMINI.md / AGENTS.md body**: ≤ 200 lines **recommended**, ≤ 300 lines **absolute ceiling**. Beyond 300 lines, instruction-following degrades uniformly across models (Arize research, Anthropic best practices).
- **Discrete instruction count per file**: ≤ 150-200 for consistent adherence. Past that, scattered rules start contradicting each other or simply being skipped.
- **Audit verdict mapping**: > 400 lines or hard-rule content (lint/formatter) duplicated as English → **P0**. > 200 lines or any rule expressible as a hook still living in CLAUDE.md → **P1**.

[Source: code.claude.com — Best Practices; alexop.dev — *Stop Bloating Your CLAUDE.md*]

---

## Settings hierarchy

Lowest → highest priority:

```
Plugin defaults  →  User  →  Project  →  Local  →  Managed (policy)
```

Within the **Managed** tier:

```
file-based (managed-settings.json + managed-settings.d/*.json merged alphabetically)
  < MDM / OS-level
  < server-managed
```

- **Permission evaluation order**: `deny → ask → allow`, first match wins.
- **Hook semantics**: hooks can **tighten** restrictions (return `deny`) but cannot **loosen** them — returning `allow` does NOT bypass deny rules from `settings.json`. Deny is immutable, even under `bypassPermissions` mode and even via hooks.
- **Non-interactive mode**: `PermissionRequest` hooks do **not** fire with `-p` — automated pipelines must use `PreToolUse` for permission enforcement.
- **Hook known limitation**: `permissionDecision: "deny"` may be ignored for file-writing tools (e.g., `Edit`). [Source: anthropics/claude-code#37210] — audit flags security-critical deny hooks on `Edit`/`Write` as potentially unreliable.

---

## MCP servers (per-server)

- **Least privilege**: one PAT per server, scoped to the endpoints it actually needs. **66%** of MCP servers have at least one security finding (Practical DevSecOps 2026 scan of 1,808 servers); **43%** had shell injection.
- **Transport**: HTTP-based MCP servers must use **OAuth 2.1** (PKCE mandatory). M2M auth uses client-credentials flow (MCP spec 2025-11-25). **Token passthrough is forbidden** under OAuth 2.1.
- **Version pinning**: pin exact server versions in production; no auto-updates without changelog review and a staging test.
- **OAuth resource binding**: RFC 8707 resource indicators **MUST** appear in both authorization and token requests (MCP spec 2026-03-15). Tokens without resource binding can be replayed against unintended services.
- **OAuth endpoint validation**: validate Dynamic Client Registration and OAuth discovery URLs against known-good registries — CVE-2025-6514 (mcp-remote, CVSS 9.6) showed a malicious `authorization_endpoint` URL achieves command injection.
- **FastMCP OAuth proxy**: do not trust callbacks without consent verification — CVE-2026-27124 (FastMCP, patched 3.2.0) enabled confused-deputy account takeover via a missing consent verification step. [Source: GHSA-rww4-4w9c-7733, 2026-03-31]

---

## Plugins

- **Official Anthropic marketplace** plugins auto-update by default — acceptable.
- **Third-party marketplace** plugins require explicit trust review and version pinning. Auto-updating third-party plugins introduces supply-chain attack risk — **flag as P0** unless trust evidence + pinning are in place.

---

## Codex wire_api

- `wire_api = "chat"` is a **hard error since Feb 2026**. Any custom provider still using `chat/completions` must migrate to the responses API.

---

## Hook handler types

Four types: `command`, `http`, `prompt`, `agent`. Each has distinct audit scope:

- **command**: verify `$CLAUDE_PROJECT_DIR` prefix for portable path resolution across working directories.
- **http**: verify `allowedHttpHookUrls` patterns (no over-broad globs); verify `httpHookAllowedEnvVars` does not expose sensitive env vars to external endpoints.
- **prompt** / **agent**: review model cost and context budget — these handlers call into models and accumulate token spend.

---

## `.claude/rules/` path-scoped rules

- Files with `globs:` YAML frontmatter activate only for matching file patterns.
- **Audit**: verify glob syntax validity and pattern specificity. Flag overly broad `globs: "**/*"` — it defeats path scoping.

---

## Instruction budget waste

- CLAUDE.md / GEMINI.md instructions that duplicate enforcement already provided by linter/formatter tooling (ESLint, Prettier, Ruff, gofmt, etc.) consume context without value.
- **Verdict**: flag as **P2** for removal. The tools already enforce these rules; the instruction text only costs cache budget.

---

## CLAUDE.md / AGENTS.md coexistence drift

- **AGENTS.md** is the Agentic AI Foundation standard, read by 29+ tools.
- **CLAUDE.md** is Claude-native.
- If both exist in a project, audit for content divergence (same rule stated differently in each). Recommend a single source of truth — typically a thin `CLAUDE.md` that imports `AGENTS.md`.

[Source: agents.md; linuxfoundation.org — AAIF]

---

## Periodic re-evaluation cadence

- Schedule **every 3-6 months** and at every major model release.
- Instructions written to work around a prior model's limitations frequently become inert or actively harmful on a newer model.
- Example: a CLAUDE.md rule that instructed an earlier model to break every refactor into single-file changes (to stay on track) can prevent a newer model from making coordinated cross-file edits.
- **Audits older than 6 months should automatically flag** every CLAUDE.md / GEMINI.md / AGENTS.md instruction tied to a specific prior model behavior for re-validation.

[Source: claude.com — *How Claude Code works in large codebases* (2026)]

---

## Anti-bloat audit (per-line test)

For every CLAUDE.md / AGENTS.md line, ask Anthropic's question: **"would Claude actually do this wrong without it?"**

- Lines failing the test belong in a hook, in a skill on-demand reference, or in progressive disclosure (split into a separate small file imported only when needed).
- **P0 finding**: file > 400 lines OR hard-rule content (lint/formatter) duplicated as English.
- **P1 finding**: file > 200 lines OR any rule expressible as a hook still living in CLAUDE.md.

---

## Prompt cache hierarchy (`_common/PROMPT_CACHE_HIERARCHY.md`)

Three-tier classification:

| Tier | Layer | Volatility |
|------|-------|------------|
| **T-static** | `tools` + `system` top | per release, not per request |
| **T-semi-static** | `system` middle (active recipe, `_AGENT_CONTEXT` template) | per task |
| **T-dynamic** | `messages` (user input, ARGUMENTS, timestamps, tool results) | per request |

**Findings:**

- **P0** — cache breakpoint placed on `Date.now()` / ISO timestamp / random ID / per-request data. Single most common cache-buster (90% savings lost per request).
- **P1** — `_common/` load order varies per task (re-ordering invalidates the whole `_common/` prefix); inlined `_common/` excerpts that duplicate cached bytes; per-task MCP tool churn that mutates the `tools` layer.
- **P2** — missing 1-hour-TTL cache breakpoints in long sessions; `reference/` excerpts re-appended below the active recipe block on follow-up turns.

Report cache hit rate from session logs when available; flag any session below 70% hit rate as **P1**.

[Source: platform.claude.com/docs/en/build-with-claude/prompt-caching, `_common/PROMPT_CACHE_HIERARCHY.md`]
