# Codex Review CLI Usage

Operational reference for invoking `codex review`. This file is the single source of truth for **how to run codex review**. For output interpretation, severity mapping, and false-positive filtering see `codex-integration.md`.

---

## Prerequisites

| Item | Requirement | Notes |
|------|-------------|-------|
| Binary | `codex` on `$PATH` **or** at a known fallback path | `codex --version` must succeed. See **Robust availability detection** below — never declare unavailable based on a single `command -v` miss |
| Subcommand | `codex review` | Non-interactive code review mode |
| Authentication | Subscription login (`codex login`) | No API key / `OPENAI_API_KEY` required; do not set or pass API keys |
| Model | Default (no `-m` / `--model` flag) | Always rely on the CLI default — never override the model |
| Working directory | Git repository root | Commands operate on the current git worktree |

**Never** pass `-m`, `--model`, `-c model=...`, or set `OPENAI_API_KEY`. Authentication and model selection are managed by the user's subscription login.

### Robust availability detection

`codex` is commonly installed under `~/.bun/bin/codex` (Bun), `~/.local/bin/codex`, `/usr/local/bin/codex`, `/opt/homebrew/bin/codex`, or via npm/pnpm/yarn global. A subagent's inherited `$PATH` may be narrower than the user's interactive shell — `command -v codex` failing inside a subagent does **not** mean the binary is missing. Always probe fallback paths before declaring unavailability:

```bash
if command -v codex >/dev/null 2>&1; then
  CODEX_BIN="$(command -v codex)"
else
  for p in "$HOME/.bun/bin/codex" "$HOME/.local/bin/codex" "/usr/local/bin/codex" "/opt/homebrew/bin/codex" "$HOME/.npm-global/bin/codex"; do
    [ -x "$p" ] && CODEX_BIN="$p" && break
  done
fi
[ -n "$CODEX_BIN" ] && "$CODEX_BIN" --version || echo "codex: not found in any known location"
```

When invoking via the resolved absolute path, substitute `"$CODEX_BIN"` for `codex` in every subsequent command in this guide.

**Do not classify these as "unavailable":** auth-expired errors, transient network failures, quota errors, slow first-token latency. These are runtime failures — surface the real error rather than silently dropping codex from the engine roster.

If a review-specific model override is ever required, the canonical location is the `review_model` key in `~/.codex/config.toml` — **not** the CLI `-m` flag (Codex CLI official docs, 2026). Per current project policy, leave `review_model` unset and use the session default.

---

## Command Reference

### Syntax

```
codex review [OPTIONS] [PROMPT]
```

`PROMPT` is an optional free-form instruction string. Pass `-` to read the prompt from stdin.

### Flag Matrix

| Flag | Purpose | Required? |
|------|---------|-----------|
| `--base <BRANCH>` | Compare current branch against `<BRANCH>` (PR review) | PR mode |
| `--uncommitted` | Review staged + unstaged + untracked changes | Pre-commit mode |
| `--commit <SHA>` | Review only the diff introduced by `<SHA>` | Commit mode |
| `--title <TITLE>` | Display a commit/PR title in the review summary | Optional |
| `--enable <FEATURE>` | Enable a codex feature flag (repeatable) | Rare |
| `--disable <FEATURE>` | Disable a codex feature flag (repeatable) | Rare |
| `PROMPT` | Inline review instructions | Recommended |
| `-` (as PROMPT) | Read prompt from stdin | For long or file-sourced prompts |

Exactly one of `--base`, `--uncommitted`, `--commit` must be chosen per invocation.

### Canonical Commands

```bash
# PR review against main
codex review --base main "Focus on: bug detection, logic errors, edge cases, security issues"

# PR review against develop with custom focus
codex review --base develop "Check null handling, error propagation, and API contract violations"

# Pre-commit review of local changes
codex review --uncommitted "Identify bugs, security issues, and logic errors before commit"

# Commit-scoped review
codex review --commit <SHA> "Analyze this commit for bugs and issues"

# Read prompt from stdin
echo "Focus on authentication flow and session handling" | codex review --base main -
```

---

## Use Case Cookbook

Pick the recipe that matches the user's request. Every recipe keeps the default model and subscription auth — only the flags and prompt change.

### 1. Standard PR Review

Use when the user says "review this PR", "check the PR", or provides a PR link.

```bash
codex review --base main "Focus on: correctness, security, logic errors, and edge cases. Verify intent alignment with the PR description."
```

Swap `main` for `develop`, `release/*`, or the actual PR base branch when different.

### 2. Pre-Commit Check

Use when the user says "review my changes", "check before commit", or has uncommitted work.

```bash
codex review --uncommitted "Identify bugs, security issues, missing error handling, and logic errors in staged and unstaged changes."
```

If the working tree is clean, fall back to PR review and warn the user.

### 3. Specific Commit Review

Use when the user passes a SHA, says "review commit abc123", or investigates regressions.

```bash
codex review --commit <SHA> "Analyze the changes introduced by this commit for bugs, regressions, and logic errors."
```

### 4. Security-Focused Review

Use when the user asks for "security review", "vulnerability check", or the diff touches auth/payments/data access.

```bash
codex review --base main "Security focus: injection (SQL/NoSQL/command), XSS, SSRF, auth bypass, authorization gaps, hardcoded secrets, unsafe deserialization, missing input validation, insecure crypto, and sensitive data in logs."
```

Route CRITICAL/HIGH findings to Sentinel per the SKILL.md collaboration map.

### 5. Intent-Alignment Review

Use when the user wants to verify that the diff matches the PR description, commit message, or ticket.

```bash
codex review --base main "Verify code changes match the stated intent. Flag unrelated changes, scope creep, and missing changes implied by the description. PR intent: <paste PR title + description here>."
```

### 6. AI-Generated Code Scrutiny

Use when the diff is marked as AI-assisted (Copilot/Cursor/Claude) or the user flags AI origin.

```bash
codex review --base main "Elevated scrutiny for AI-generated code. Check: (1) logic errors in boundary and edge cases, (2) missing input validation and sanitization, (3) hallucinated imports/APIs/classes — verify every imported symbol exists in the codebase, (4) security shortcuts (hardcoded values, permissive CORS, credential exposure), (5) absent defenses (missing parameterized queries, missing URL allowlists, missing output encoding), (6) performance anti-patterns (N+1, missing pagination, synchronous blocking)."
```

### 7. Framework-Specific Review

Append the framework prompt to any base command. Keep mode flags unchanged.

```bash
# React / Next.js
codex review --base main "React/Next.js focus: hook dependency arrays, effect cleanup, server/client boundary (RSC 'use client'), data fetching in server components, hydration mismatches, memoization correctness."

# Express / Node.js
codex review --base main "Express focus: async error propagation to error middleware, missing await, unhandled promise rejections, middleware order, input validation, CORS configuration."

# TypeScript
codex review --base main "TypeScript focus: unsafe 'as' casts, 'any' escapes, discriminated union exhaustiveness, nullability, generic constraints, narrow-once assumption."

# Python
codex review --base main "Python focus: type hints accuracy, exception hierarchy, resource cleanup via context managers, mutable default arguments, async/await correctness."

# Go
codex review --base main "Go focus: error wrapping and handling, goroutine leaks, channel close semantics, context propagation, pointer receiver consistency, race conditions."
```

### 8. Consistency Audit

Use when the user wants cross-file pattern checks.

```bash
codex review --base main "Consistency audit across files: error handling patterns, null-safety style, async patterns, naming conventions, import/export style, error type usage. Report when a dominant pattern (≥70%) has outliers."
```

### 9. Test Quality Review

Use when the diff includes tests or the user asks for test review.

```bash
codex review --base main "Test quality focus: test isolation, flakiness risk, edge case coverage, mock fidelity, readability. Flag tests that depend on ordering, shared state, time, or network."
```

### 10. Large-PR Decomposition Check

Use when `git diff --stat` shows >400 LOC.

```bash
codex review --base main "Cognitive load assessment for a large PR. Identify logical seams where the change could be split into smaller PRs. Group findings by subsystem and call out any cross-cutting concerns that resist decomposition."
```

### 11. Project-Guideline-Gated Review

Use when project-specific review rules exist. Two discovery sources, in order of precedence:

1. **`REVIEW.md`** at repo root (Judge convention — project-specific rules take precedence).
2. **`code_review.md`** referenced from `AGENTS.md` (official Codex CLI convention — Codex follows it automatically when present, without explicit piping).

```bash
# REVIEW.md path (Judge convention) — pipe into stdin
cat REVIEW.md | codex review --base main -

# Append project-specific focuses after REVIEW.md content
(cat REVIEW.md; echo; echo "Additional focus: authentication flow") | codex review --base main -

# AGENTS.md / code_review.md path (Codex native) — no piping needed; Codex discovers and follows
codex review --base main "Focus on correctness and security. Apply project code_review.md guidance."
```

If both exist, prefer `REVIEW.md` + explicit pipe for determinism; `code_review.md` via AGENTS.md is picked up automatically.

### 12. Long or File-Sourced Prompt

Use when the prompt is long, multi-line, or stored in a file.

```bash
# From a prompt file
cat .codex/review-prompt.md | codex review --base main -

# From a heredoc (bash/zsh)
codex review --base main - <<'EOF'
Focus areas:
1. Auth/session handling correctness.
2. Rate-limit bypass risk.
3. Idempotency of retried operations.
4. Audit-log completeness.
EOF
```

### 13. Titled Review Summary

Use when routing the output into a report and a clear header helps the reader.

```bash
codex review --base main --title "PR #1234: Refactor auth middleware" "Focus on authorization regressions."
```

---

## Prompt Structure (Official Best Practice)

OpenAI Codex 2026 guidance recommends framing every review prompt with four elements. Use this template for non-trivial reviews (security, intent alignment, framework-specific, AI-code scrutiny):

| Element | Purpose | Example |
|---------|---------|---------|
| **Goal** | What is being reviewed and why | "Review auth middleware rewrite for correctness and regression risk." |
| **Context** | Relevant files, standards, or prior decisions | "Session tokens must not be logged; see SECURITY.md." |
| **Constraints** | Architectural patterns, non-negotiables | "Must remain backward-compatible with existing session cookies." |
| **Done when** | Acceptance criteria for a clean review | "No CRITICAL/HIGH findings; all auth paths have test coverage." |

Combine into a single prompt string (or stdin doc). Well-structured prompts raise signal and make findings comparable across reviews.

---

## Interactive `/review` Slash Command (Alternative)

Inside an active `codex` TUI session, the `/review` slash command offers the same four review modes as the non-interactive subcommand via a preset picker:

1. Base-branch review
2. Uncommitted changes
3. Specific commit
4. Custom instructions

Follow-up with `/diff` inspects the exact file changes Codex analyzed. Each `/review` appears as its own turn, so you can rerun and compare feedback as code evolves.

**When to use each:**

| Mode | Use When |
|------|----------|
| `codex review ...` (non-interactive) | Judge automation, CI flows, scripted runs, Nexus AUTORUN |
| `/review` (interactive TUI) | Human-driven iterative review, exploratory follow-ups via `/diff` |

Judge primarily uses the non-interactive subcommand. Mention `/review` to the user only when they are already inside a `codex` TUI session.

---

## GitHub-Native Async Review

For PR-comment-triggered reviews (CI/CD integration), the user posts a PR comment:

```
@codex review
```

Codex runs asynchronously and posts the review back as a GitHub review. Judge does **not** invoke `codex review` locally in this mode — verify the GitHub App is installed on the repository and confirm in the PR comment thread that the async review has been dispatched.

Optional focus hint in the comment:

```
@codex review focus on authentication and session handling
```

---

## Decision Flow

```
User request → check git state →
  uncommitted changes present?     → --uncommitted
  user named a SHA?                → --commit <SHA>
  user named a PR or base branch?  → --base <branch>
  async/CI context?                → @codex review in PR comment
  ambiguous?                       → check `git status`, prefer --uncommitted if dirty, else --base main
```

Always pair the mode flag with a focus prompt — bare invocations produce lower-signal output.

---

## Do / Don't

### Do

- Keep authentication implicit via `codex login`; never export `OPENAI_API_KEY` for this flow.
- Omit `-m` / `--model` / `-c model=...`; always use the default model.
- Always pass a focused prompt — it directly raises signal-to-noise ratio.
- Use `-` + stdin for prompts longer than ~200 characters or when sourcing from files.
- Prepend `REVIEW.md` content when the file exists at repo root.
- Pick exactly one of `--base`, `--uncommitted`, `--commit` per invocation.

### Don't

- Don't set `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or any provider API key — subscription auth is already active.
- Don't override the model with `-m`, `--model`, or `-c model=...`.
- Don't combine mode flags (e.g., `--base` and `--uncommitted` together).
- Don't run bare `codex review --base main` without a prompt; always include a focus string.
- Don't invoke `codex review` when the user asked for `@codex review` on GitHub — those are different execution paths.
- Don't rerun the same command to "try again" on flaky output; refine the prompt instead.

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| `command not found: codex` | CLI not on `$PATH` of current shell — but the binary may exist | First try fallback paths (`~/.bun/bin/codex`, `~/.local/bin/codex`, `/usr/local/bin/codex`, `/opt/homebrew/bin/codex`); only ask the user to install if none are executable. Subagents see a narrower PATH than interactive shells |
| Subagent reports "codex unavailable" but user confirms it works | Subagent PATH narrower than interactive shell | Re-run preflight in main Judge context; pass the absolute binary path into the subagent prompt |
| Authentication error | `codex login` session expired | Instruct the user to run `codex login`; do not supply API keys |
| Empty or truncated output | Prompt too vague or diff too large | Add a sharper focus prompt; for >1000 LOC diffs, recommend decomposition before retrying |
| "No changes to review" | Clean working tree or unrelated branch | Verify mode: switch to `--base` or `--commit` as appropriate |
| Base branch not found | Local ref missing | Run `git fetch origin <branch>` first, then retry |
| Reviewer loops on style comments | Prompt lacks correctness focus | Re-run with explicit "Focus on correctness, not style" |

---

## Cross-References

- Antigravity CLI review (alternative engine, cross-engine verification): `antigravity-review-usage.md`.
- Claude Code CLI review (alternative engine, subagent/plan-mode required): `claude-review-usage.md`.
- Output interpretation, severity mapping, override rules, false-positive filtering (engine-agnostic): `codex-integration.md`.
- Framework-specific review prompts and expected findings: `framework-reviews.md`.
- AI-generated code review depth and hallucination checks: `ai-review-patterns.md`.
- PR size cognitive-load thresholds: `review-effectiveness.md`.

### Official Sources (2026)

- Codex CLI Features — <https://developers.openai.com/codex/cli/features>
- Codex CLI Command Reference — <https://developers.openai.com/codex/cli/reference>
- Codex CLI Slash Commands (`/review`) — <https://developers.openai.com/codex/cli/slash-commands>
- Codex Best Practices (prompt structure, `AGENTS.md` + `code_review.md`) — <https://developers.openai.com/codex/learn/best-practices>
- Codex Changelog — <https://developers.openai.com/codex/changelog>
