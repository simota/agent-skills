# AGENTS.md — claude-skills

Cross-tool agent instructions for this repository. Read by **Antigravity CLI (`agy`)**, **Claude Code**, **Cursor**, and any other tool that honors the Agentic AI Foundation `AGENTS.md` standard.

> **Authority order**: `AGENTS.md` (this file, cross-tool common rules) → tool-specific overrides (`CLAUDE.md` for Claude Code, `GEMINI.md` for agy). Tool-specific files should contain only deltas, not duplicates.

---

## Repository Purpose

`claude-skills` is a **prompt engineering repository** of 136+ specialist skill agents. The deliverables are **`SKILL.md` files** (not application code). Each skill lives at `<skill-name>/SKILL.md` with optional `reference/`.

---

## Language Policy

- **Conversation / explanations / summaries**: 日本語 (Japanese).
- **Code, identifiers, APIs, commit messages, protocol markers, schema keys, technical terms, CLI commands, file paths, hashes**: English.
- Output language follows the CLI global config (`settings.json` `language` field, `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`).

---

## Repository Structure

| Path | Purpose |
|------|---------|
| `<skill-name>/SKILL.md` | Each specialist agent's main definition (frontmatter: `name` + `description` only) |
| `<skill-name>/reference/` | Optional supporting docs the skill loads on demand |
| `_common/` | Shared protocols affecting all skills — **modify with care** |
| `_common/CLI_COMPATIBILITY.md` | Cross-CLI compatibility matrix (Claude Code / Codex CLI / agy) |
| `_common/BOUNDARIES.md` | Centralized agent-role boundaries |
| `_common/GIT_GUIDELINES.md` | Commit / PR conventions (authoritative) |
| `_common/HANDOFF.md` | Inter-agent handoff schema |
| `_common/SECURITY.md` | Supply-chain trust boundary |
| `_templates/SKILL_TEMPLATE.md` | Starting template for new skills |
| `.agents/` | Per-skill journals + project log (gitignored) |

---

## Skill Authoring Conventions

1. **Frontmatter discipline**: Each `SKILL.md` MUST contain exactly `name` and `description` keys. Capability declarations belong in the Markdown body (Anthropic Agent Skills spec; `chain` skill rejects custom keys).
2. **Description quality**: `description:` should include 3-5 trigger keywords and the primary use case in ≤2 sentences. Vague descriptions cause tool bloat (40-50K token overhead in multi-skill loadouts).
3. **CAPABILITIES_SUMMARY comment block**: Preserve the existing `<!-- CAPABILITIES_SUMMARY: ... -->` HTML comment format when editing existing skills. New skills follow `_templates/SKILL_TEMPLATE.md`.
4. **References**: Heavy content (checklists, schemas, anti-patterns) goes in `reference/<topic>.md` and is loaded on demand. Keep `SKILL.md` ≤300 lines.
5. **Cross-CLI compatibility**: Skills meant to run on multiple CLIs MUST include a `## Compatibility` section and consult `_common/CLI_COMPATIBILITY.md` instead of hard-coding `Agent(...)` syntax.
6. **Boundaries**: Link to `_common/BOUNDARIES.md` rather than maintaining per-skill role-boundary tables.

---

## Agent Behavior

- **Autonomy**: Clear request → execute. Ambiguous + reversible → pick safe default, document inline, proceed. Ambiguous + irreversible → ask one question.
- **Skill discovery**: Before investigating, implementing, reviewing, refactoring, or documenting by hand, check whether a skill in this repo covers it. Unsure which fits → `compass`. Multi-step chain → `nexus`. Gap with no fit → `architect`.
- **No fabrication**: Verify file paths, APIs, configs, and behavior before asserting. Do not speculate model names, version numbers, or command names that are not documented — mark them "未確認".

---

## Quality

- Before reporting done: run the repo's existing checks where applicable (lint, link-check, format) and re-read your own diff.
- Fix root causes. Do not silence errors, suppress warnings, or bypass checks (`--no-verify`, broad `except`, blanket `any`/`@ts-ignore`).
- If a command or test fails twice with the same error, stop and diagnose.
- Do not add defensive fallbacks for scenarios that cannot happen.

---

## Git Conventions

Authoritative: [`_common/GIT_GUIDELINES.md`](_common/GIT_GUIDELINES.md). Summary:

- **Conventional Commits**: `<type>(<scope>): <description>` (e.g. `feat(nexus): add agy execution layer`).
- **Types**: `feat` / `fix` / `docs` / `style` / `refactor` / `perf` / `test` / `chore` / `ci` / `security`.
- **Scope = skill name** for skill-scoped changes (e.g. `feat(cull): add agy IoC paths`).
- **Imperative mood**, subject ≤50 chars.
- **Never include agent names** in commit messages, PR titles, or PR descriptions.
- **Never** add `Claude Code signatures` or `Co-Authored-By` lines.
- Body explains "why", not "what".

---

## Tool Compatibility

This repository's skills are authored primarily for **Claude Code**, but the `_common/CLI_COMPATIBILITY.md` matrix documents how to adapt for **Codex CLI** and **Antigravity CLI (`agy`)**. Where a skill is CLI-specific, it must state so in its `## Compatibility` section.

### Cross-CLI Spawn Abstraction

| Layer | Claude Code | Codex CLI | agy |
|-------|-------------|-----------|-----|
| Direct spawn | `Agent(prompt, mode: bypassPermissions)` | `spawn_agent(prompt)` → `wait_agent(id)` | `/agent <name> "<task>"` or `agy -p "<prompt>" --dangerously-skip-permissions` (flag mandatory for headless — bypasses default `request-review` gate, equivalent to Claude Code's `bypassPermissions`) |
| Parallel | `Agent(..., run_in_background: true)` × N | multiple `spawn_agent` → `wait_agent` all | multiple `/agent` invocations in TUI |
| Skill root | `~/.claude/skills/` | `~/.codex/skills/` (未確認) | `~/.gemini/antigravity-cli/skills/` |
| Workspace skill root | `<repo>/.claude/skills/` | `<repo>/.agents/skills/` | `<repo>/.agents/skills/` |

Full mapping → `_common/CLI_COMPATIBILITY.md`.

---

## Security

- Do not commit credentials, API keys, or OAuth tokens. The repository explicitly excludes `~/.codex/auth.json`, `~/.gemini/` auth tokens, `~/.claude/credentials.json` from any audit or read.
- Third-party skills, plugins, and MCP servers are subject to the `chain` skill's intake checklist before being adopted.
- MCP server tool descriptions should be SHA-256-pinned where the CLI permits.

---

## Output Conventions

- Repo-relative paths in human-facing references (e.g. `nexus/SKILL.md`, not `/Users/.../nexus/SKILL.md`).
- Mark deferred work with `#TODO(agent): <action>`.
- Cite sources with URL + date when claiming a best practice; prefer "未確認" over invention.

---

## When Tools Disagree

- `AGENTS.md` (this file) takes precedence over silently-inherited tool defaults.
- Tool-specific override files (`CLAUDE.md`, `GEMINI.md`) take precedence over `AGENTS.md` *only on the file's home tool* and *only for delta content*.
- If a rule cannot be expressed cross-tool, document it here as "tool-specific" with a reference to the override file.
