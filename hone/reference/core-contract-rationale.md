# Core Contract Rationale

Purpose: full rationale, mechanism, and source citations behind the compressed Core Contract bullets in SKILL.md. Read this when a proposal needs cited justification, not just the compressed rule.

## CLAUDE.md / AGENTS.md anti-bloat audit

Apply Anthropic's official rule for every line: "would Claude actually do this wrong without it?". Lines failing that test belong in a hook, in a skill's on-demand reference, or in a `paths:`-scoped rule — **not** in a `@path` import, which loads with CLAUDE.md and leaves startup context unchanged (see `reference/key-thresholds.md` § Anti-bloat audit). P0 finding: file > 400 lines or hard-rule content (lint/formatter) duplicated as English; P1 finding: file > 200 lines or any rule expressible as a hook still living in CLAUDE.md. Route each failing line to its correct mechanism via `_common/MECHANISM_SELECTION.md` ("every time"/"never" → hook; runbook → skill; path-specific → `paths:`-scoped rule). [Source: code.claude.com/docs/en/best-practices; alexop.dev — Stop Bloating Your CLAUDE.md; claude.com — Steering Claude Code]

## AGENTS.md / CLAUDE.md coexistence drift

In multi-tool projects, AGENTS.md is the Agentic AI Foundation standard read by 29+ tools; CLAUDE.md is Claude-native. If both exist, audit for content divergence (same rule stated differently in each file) and recommend a single source of truth (typically a thin `CLAUDE.md` that imports `AGENTS.md`). [Source: agents.md; linuxfoundation.org — AAIF]

## Prompt cache hierarchy audit

Run when auditing a multi-skill orchestration session, large CLAUDE.md / GEMINI.md instructions, or any setup that loads `_common/` shared protocols. Apply `_common/PROMPT_CACHE_HIERARCHY.md`'s three-tier rule: T-static content (tool defs, skill bodies, `_common/` protocols) must sit above T-semi-static (recipe template) which must sit above T-dynamic (user input, ARGUMENTS, timestamps, tool results).

- **P0**: any cache breakpoint placed on a `Date.now()` / ISO timestamp / random ID / per-request data line — the single most common cache-buster (90% savings lost on every request).
- **P1**: `_common/` load order that varies per task (re-ordering invalidates the entire `_common/` prefix); inlined `_common/` excerpts that duplicate the cached bytes; per-task MCP tool churn that mutates the `tools` layer.
- **P2**: missing 1-hour-TTL cache breakpoints in long sessions; reference/ excerpts re-appended below the active recipe block on follow-up turns.

Report cache hit rate from session logs when available; flag sessions below 70% hit rate as P1. [Source: platform.claude.com/docs/en/build-with-claude/prompt-caching, `_common/PROMPT_CACHE_HIERARCHY.md`]

## Periodic config re-evaluation

Schedule every 3-6 months and at every major model release. Instructions written to work around a prior model's limitations frequently become inert or actively harmful on a newer model — e.g. a CLAUDE.md rule that instructed an earlier model to break every refactor into single-file changes (to stay on track) can prevent a newer model from making coordinated cross-file edits. Audits older than 6 months should automatically flag every CLAUDE.md / GEMINI.md / AGENTS.md instruction tied to a specific prior model behavior for re-validation. [Source: claude.com — *How Claude Code works in large codebases* (2026)]


---

## Hook and MCP Audit Rules (SKILL.md excerpt)

- Validate PreToolUse hooks return correct exit codes (0=allow, 2=block) and that security-critical hooks use `permissionDecision: "deny"` which cannot be bypassed even in bypassPermissions mode.

- Verify that automated/CI pipelines do not rely on PermissionRequest hooks (they do not fire with `-p` flag); recommend PreToolUse hooks for non-interactive permission enforcement.

- Verify hook "allow" decisions are not relied upon for security — hooks can tighten (deny) but cannot loosen permissions past deny rules. Flag configurations where a hook "allow" is the sole security gate.

- Flag HTTP hooks with overly broad `allowedHttpHookUrls` patterns; verify `httpHookAllowedEnvVars` does not expose sensitive environment variables to external endpoints.

- Verify MCP OAuth configurations include RFC 8707 resource indicators — tokens without explicit resource binding are vulnerable to mis-redemption attacks where a malicious server replays tokens against unintended services (MCP spec 2026-03-15).
