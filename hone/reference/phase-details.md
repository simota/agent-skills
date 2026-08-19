# Workflow Phase Details

Purpose: full FETCH / AUDIT / PROPOSE phase detail, including the current, authoritative list of audit item codes per category. This supersedes any code listing in `reference/audit-checklist.md` that is missing newer codes (CCS6-11, CCH3-8, CCG1-3, CCPL1-4, CCI5-7) — treat this file as the current source of truth for item-code coverage until `audit-checklist.md` is resynced.

**FETCH** collects:
- Latest target CLI version and supported models
- Current recommended configuration patterns
- Known deprecated settings or feature flags
- New features available since last config update

**AUDIT** evaluates:
- Model settings (M1-M3): currency, reasoning_effort, verbosity
- Trust levels (T1-T5): stale paths, over-trust, wildcards
- Wire API (W1): `wire_api = "chat"` detection in custom providers (hard error since Feb 2026)
- Feature flags (F1-F3): coverage, deprecation, new features
- MCP servers (C1-C4): accessibility, necessity, secrets, versions
- Rules (R1-R3): duplicates, validity, staleness
- AGENTS.md (A1-A3): clarity, priority, redundancy
- Instructions (I1-I2): existence, currency
- **Antigravity-specific** (when target includes Gemini):
  - Antigravity Model (GM1-GM3): currency, API tier compatibility, capability support
  - Antigravity Safety (GS1-GS2): threshold appropriateness, over-permissive/restrictive
  - Antigravity Extensions (GE1-GE4): accessibility, necessity, secrets, versions
  - Antigravity Instructions (GI1-GI3): GEMINI.md existence, currency, progressive disclosure via `@file.md` imports and boundary markers for large instruction sets
  - Antigravity Auth (GA1-GA2): auth configuration, hardcoded key detection
- **Claude Code-specific** (when target includes Claude Code):
  - Claude Code Model (CCM1-CCM2): model currency, model-task alignment
  - Claude Code Permissions (CCP1-CCP5): overly permissive allow, missing deny, pattern syntax, global vs project, wildcard `allow: ["*"]` detection
  - Claude Code MCP Servers (CCS1-CCS10): accessibility, secrets in env, necessity, version currency, scope, PAT least-privilege audit, tool poisoning risk (metadata integrity), OAuth 2.1 transport compliance (PKCE for user-facing, client-credentials for M2M), token passthrough detection, version pinning
  - Claude Code Instructions (CCI1-CCI7): CLAUDE.md existence, quality, global/project consistency, staleness, line count (≤200 recommended / ≤300 max), mechanism placement (`@path` imports organize but do not defer — only `paths:`-scoped `.claude/rules/` modules and skill bodies load on demand), advisory-vs-hook triage (rules that must always execute → convert to hooks)
  - Claude Code Commands (CCK1-CCK2): custom command validity, usefulness
  - Claude Code Hooks (CCH1-CCH8): structural validity, security (design/debug switches to Hone `hook*` recipes), exit code correctness (0/2), `permissionDecision: "deny"` usage for security-critical gates (caveat: may be ignored for Edit/Write tools per anthropics/claude-code#37210), non-interactive mode coverage (PermissionRequest hooks do not fire with `-p`; flag pipelines that depend on them), HTTP hook URL validation (`allowedHttpHookUrls` patterns, env var exposure via `httpHookAllowedEnvVars`), hook tighten-only semantics verification (hooks returning "allow" do not bypass deny rules), handler type audit (command/http/prompt/agent — verify `$CLAUDE_PROJECT_DIR` usage for portable paths, validate prompt/agent handlers for cost implications)
  - Claude Code Auth (CCA1-CCA2): authentication configured, API key not hardcoded
  - Claude Code Settings Hierarchy (CCG1-CCG3): override conflict detection (user/project/local/managed), managed policy compliance, managed-settings.d/ drop-in fragment merge order verification (alphabetical sort, later filenames win)
  - Claude Code Plugins (CCPL1-CCPL4): source verification (official vs third-party marketplace), marketplace trust and subscription review, auto-update configuration (flag third-party auto-update as supply chain risk), plugin permission scope audit
  - Claude Code MCP OAuth Resource Binding (CCS11): RFC 8707 resource indicator presence in OAuth configurations, token binding verification

**PROPOSE** generates:
- Priority-ordered proposals (P0 first)
- Before/After diff for each change
- Safety classification per proposal
- Source citations with tier
