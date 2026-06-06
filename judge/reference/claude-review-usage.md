# Claude Code CLI Review Usage

Operational reference for using Anthropic's Claude Code CLI as a review engine. This file is the authoritative "how to run a Claude Code review" guide. For Codex CLI see `codex-review-usage.md`; for Antigravity CLI see `antigravity-review-usage.md`. For output interpretation (severity, false-positives) see `codex-integration.md` — those rules apply across engines.

Claude Code is one of the engines in Judge's default multi-engine parallel review. **Default baseline = Claude + Codex (dual-engine, 2 subagents fanned out in a single `Agent` tool message)**; agy is added as an optional third subagent when AVAILABLE at PREFLIGHT — see `tri-engine-review.md`. This file is consumed by the `review-claude` subagent during that fan-out. Use it directly as a single-engine review only when: the user explicitly asks for a Claude-only review, Codex is unavailable, or cross-verification against an already-run engine is needed. The mandatory subagent pattern below still applies in any Claude-based review path to eliminate self-bias.

---

## Prerequisites

| Item | Requirement | Notes |
|------|-------------|-------|
| Binary | `claude` on `$PATH` | `claude --version` must succeed (verified ≥ `2.1.x`) |
| Authentication | Claude Max / Pro / Team / Enterprise subscription login | Use `claude auth login` (add `--sso` for SSO, `--email <addr>` to pre-fill). Browser OAuth on first launch. **Do not** use `--console` (that flag forces Console API billing). **Do not** set `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, or Bedrock/Vertex credentials for this flow |
| Long-lived auth (CI) | `claude setup-token` | Generates a long-lived OAuth token for scripted/CI review runs — still subscription-backed, no API key |
| Model | Default (no `--model` flag) | Always rely on the session default — never override |
| Review context | Subagent or plan mode (or `dontAsk` for locked CI) | Claude-based reviews must avoid self-bias (see Mandatory Subagent Pattern below) |
| Working directory | Git repository root | Review commands operate on the current git worktree |
| Auto mode availability | Max / Team / Enterprise / API plans only | **Not available on Pro**; requires Sonnet 4.6 / Opus 4.6 / Opus 4.7 on Anthropic API (not Bedrock / Vertex / Foundry). If a recipe uses `--permission-mode auto`, confirm the user's plan first |

**Never** pass `--model`, `--bare` (bypasses subscription auth, forces API-key mode), or set `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `AWS_ACCESS_KEY_ID`, `GOOGLE_APPLICATION_CREDENTIALS` for this flow. Authentication is managed by the Claude subscription login. Writes to [protected paths](https://code.claude.com/docs/en/permission-modes#protected-paths) (`.git`, `.vscode`, `.claude`, shell rc files, `.mcp.json`) always prompt regardless of mode — review flows should never write to them anyway.

---

## Mandatory Subagent Pattern

Per Judge's Core Contract, **Claude-based reviews must never run in the main conversation context** — reviewing code you just wrote (or whose history sits in your context) produces self-bias that invalidates findings. Enforce a clean review context by one of:

| Approach | Command pattern | Use when |
|----------|-----------------|----------|
| **Subagent delegation** | From an active Claude session: *"Use a subagent to review …"* | Inside a Claude Code session (interactive or scripted) |
| **Fresh `-p` session** | `claude -p "<review prompt>" --permission-mode plan` in a new shell | Judge-automated, CI, or Nexus AUTORUN flows |
| **Declared custom agent** | `--agents '{"reviewer": {"description": "...", "prompt": "...", "tools": ["Read","Grep","Glob","Bash"]}}'` plus delegation | Repeated runs with a dedicated reviewer persona |
| **Plan mode** | `--permission-mode plan` | Pair with headless mode; Claude reads and reasons only — does not edit source. Other tool prompts may still appear (e.g. network Bash) |
| **`dontAsk` mode** | `--permission-mode dontAsk` | **Locked-down CI**: fully non-interactive, auto-denies any tool not pre-approved via `permissions.allow`. Strictly safer than `plan` for unattended runs |

Headless Judge flows default to **fresh `-p` + `plan` mode**. For CI without any tool approvals, use **`dontAsk`** with a narrow `--allowedTools "Read Grep Glob Bash(git *)"`. Interactive Claude workflows default to **subagent delegation**.

**Auto mode caveat for subagents:** when `--permission-mode auto` is active, any `permissionMode` in a subagent's frontmatter is **ignored** — the classifier governs all subagent actions. Auto mode also aborts headless `-p` runs when the classifier blocks 3 consecutive or 20 total actions. Prefer `plan` or `dontAsk` for predictable Judge automation.

---

## Command Reference

### Syntax

```
claude [OPTIONS] [PROMPT]
claude -p "<prompt>" [OPTIONS]
```

Non-interactive review always uses `-p` plus `--permission-mode plan` for read-only safety.

### Flag Matrix

| Flag | Purpose | Required for review? |
|------|---------|----------------------|
| `-p, --print` | Headless mode — run once and print, then exit | Yes for automation |
| `--permission-mode plan` | Reads only; Claude proposes without editing source. Other tool prompts may still appear | Recommended default for headless review |
| `--permission-mode dontAsk` | Fully non-interactive: auto-denies any tool not pre-approved via `permissions.allow` (read-only Bash is allowed) | Locked-down CI runs; strictly safer than `plan` for unattended |
| `--permission-mode auto` | Classifier-gated auto-approval; aborts under repeated blocks in `-p` (3 consecutive / 20 total). **Requires Max/Team/Enterprise/API plan** + Sonnet 4.6 / Opus 4.6 / Opus 4.7 | Use only when the review must run tools (e.g., run tests) and the user is on a qualifying plan |
| `--output-format <text\|json\|stream-json>` | Output shape for scripted parsing | `json` for CI, `text` for humans |
| `--json-schema '<schema>'` | Enforce strict JSON schema on output | For deterministic CI ingestion |
| `--agents '<json>'` | Inline custom agent definitions | To declare a reviewer persona |
| `--add-dir <dirs...>` | Additional workspace dirs beyond cwd | Multi-repo reviews |
| `--from-pr <number\|url>` | **Resume** a pre-existing session linked to a GitHub PR (only sessions that created the PR via `gh pr create` from within `claude` are linkable) | PR-scoped iterative review follow-up, not first-pass review |
| `-w, --worktree [name]` | Run inside a fresh git worktree | Isolated review runs |
| `--tools <list>` | Scope built-in tool availability (e.g., `Read,Grep,Glob,Bash`) | Tighten what the reviewer can touch |
| `--allowedTools <list>` | Allowlist-style permissions for headless | Combine with `auto` mode |
| `--disallowedTools <list>` | Denylist-style permissions | Block specific risky tools |
| `--max-budget-usd <N>` | Hard spend cap (only with `--print`) | Guardrail for large fan-out |
| `--fallback-model <name>` | Automatic fallback when default is overloaded | CI reliability |

Omit `--model`. Authentication and model selection are resolved from the subscription session.

### Canonical Commands

```bash
# Headless branch review in plan mode (read-only)
claude -p "Review the diff between HEAD and its upstream base. Report bugs, security issues, logic errors, and intent misalignment by severity. Use a fresh perspective — do not assume any prior context." --permission-mode plan

# Headless with JSON output for CI
claude -p "Review the current branch diff. Return findings as JSON." --permission-mode plan

# Strict-schema JSON for deterministic ingestion
claude -p "Review the current branch diff and return findings matching the provided schema." \
  --permission-mode plan \
  --json-schema '{"type":"object","properties":{"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["CRITICAL","HIGH","MEDIUM","LOW","INFO"]},"file":{"type":"string"},"line":{"type":"integer"},"issue":{"type":"string"},"evidence":{"type":"string"},"suggested_fix":{"type":"string"}},"required":["severity","file","issue"]}}},"required":["findings"]}'

# With a custom reviewer agent declared inline
claude -p "Use the reviewer agent to review the current branch diff for bugs, security, and logic errors." \
  --permission-mode plan \
  --agents '{"reviewer":{"description":"Independent code reviewer focused on correctness and security","prompt":"You are a senior code reviewer. Provide severity-ranked findings with file:line, evidence, and suggested fixes. Do not suggest style-only changes.","tools":["Read","Grep","Glob","Bash"]}}'

# Resume a PR-linked session (PR was created via `gh pr create` from a prior claude session)
claude --from-pr 1234 -p "Continue the review on this PR-linked session. Re-check open concerns and report new issues since the last turn." --permission-mode plan
```

---

## Use Case Cookbook

Every recipe pairs `-p` with `--permission-mode plan` unless the review must execute tools. Keep default model and subscription auth.

### 1. Current-Branch Review (PR-equivalent)

```bash
claude -p "Review the diff between HEAD and its upstream base. Focus on correctness, security, logic errors, and edge cases. Report with severity (CRITICAL/HIGH/MEDIUM/LOW/INFO), file:line, evidence, and suggested fix. Treat this as a fresh review — no prior context assumed." --permission-mode plan
```

### 2. Pre-Commit / Uncommitted Changes

```bash
claude -p "Review staged, unstaged, and untracked changes in the working tree (run 'git status' and 'git diff' to enumerate). Identify bugs, security issues, missing error handling, and logic errors before commit. Severity-rank findings." --permission-mode plan
```

### 3. Specific Commit Review

```bash
claude -p "Review only the changes introduced by commit <SHA> (use 'git show <SHA>'). Report bugs, regressions, and logic errors with severity and line references." --permission-mode plan
```

### 4. Resume a PR-Linked Session via `--from-pr`

`--from-pr` **resumes** a Claude Code session that was previously linked to a GitHub PR (sessions are auto-linked when the PR was created via `gh pr create` from within a Claude session). It does **not** initiate a first-pass review from a PR number alone — use recipe 1 (`--base`) or the built-in `/review` command for first-pass PR review.

```bash
claude --from-pr <PR_NUMBER_OR_URL> -p "Continue the review on this PR-linked session. Re-check open concerns, verify intent alignment with the latest PR description, and report new bugs/security/logic issues since the last turn." --permission-mode plan
```

Preconditions: the PR was created from a Claude Code session on the current machine (same local session store) and that session still exists. If `--from-pr` errors with "no linked session," fall back to recipe 1 diffing against the PR's base branch.

### 5. Built-In `/review` Slash Command

Claude Code ships a `review` skill (`/review`) for PR review. Inside an interactive session:

```
/review
```

Judge uses this only when the user is already in a Claude Code TUI. For automation, prefer the headless recipe 1 or 4.

### 6. Built-In `/security-review` Slash Command

Claude Code ships a `security-review` skill for security review of pending changes. Inside a session:

```
/security-review
```

Headless equivalent (use when automating security sweeps):

```bash
claude -p "Activate the security-review skill and review pending changes on the current branch. Focus on injection (SQL/NoSQL/command), XSS, SSRF, auth bypass, authorization gaps, hardcoded secrets, unsafe deserialization, missing input validation, insecure crypto, and sensitive data in logs. Severity-rank findings." --permission-mode plan
```

Route CRITICAL/HIGH findings to Sentinel per SKILL.md collaboration.

### 7. Intent-Alignment Review

```bash
claude -p "Verify code changes on the current branch match the stated intent. Flag unrelated changes, scope creep, and missing changes implied by the description. Intent: <paste PR title + description here>." --permission-mode plan
```

### 8. AI-Generated Code Scrutiny

```bash
claude -p "Elevated scrutiny for AI-generated code on the current branch. Check (1) logic errors at boundaries and edges, (2) missing input validation and sanitization, (3) hallucinated imports/APIs/classes — verify every imported symbol exists in the codebase, (4) security shortcuts (hardcoded values, permissive CORS, credential exposure), (5) absent defenses (missing parameterized queries, missing URL allowlists), (6) performance anti-patterns (N+1, missing pagination, synchronous blocking)." --permission-mode plan
```

### 9. Framework-Specific Review

```bash
# React / Next.js
claude -p "React/Next.js focus for the current branch: hook dependency arrays, effect cleanup, server/client boundary ('use client'), data fetching in server components, hydration mismatches, memoization correctness." --permission-mode plan

# TypeScript
claude -p "TypeScript focus: unsafe 'as' casts, 'any' escapes, discriminated union exhaustiveness, nullability, generic constraints." --permission-mode plan

# Go
claude -p "Go focus: error wrapping, goroutine leaks, channel close semantics, context propagation, race conditions." --permission-mode plan
```

### 10. Consistency Audit

```bash
claude -p "Consistency audit across files touched on the current branch: error handling, null-safety, async patterns, naming, imports, error types. Flag outliers when a dominant pattern (≥70%) exists." --permission-mode plan
```

### 11. Test Quality Review

```bash
claude -p "Test quality focus on test files changed on the current branch: isolation, flakiness risk, edge case coverage, mock fidelity, readability. Flag tests that depend on ordering, shared state, time, or network." --permission-mode plan
```

### 12. Project-Guideline-Gated Review

Claude Code auto-loads `CLAUDE.md` from cwd + parents every session, and Judge-specific rules can live in `REVIEW.md`.

```bash
# CLAUDE.md auto-discovered — just run the review
claude -p "Review the current branch diff following the conventions in CLAUDE.md. Report deviations explicitly." --permission-mode plan

# REVIEW.md piped as additional context
cat REVIEW.md | claude -p "Apply the review guidelines from stdin to the current branch diff. Report deviations and any issues they surface." --permission-mode plan
```

### 13. Three-Engine Cross-Verification

For maximum confidence, run Codex + Antigravity + Claude and cross-reference findings via `codex-integration.md` multi-agent verification rules.

```bash
codex review --base main "Focus on correctness, security, and logic errors." > review-codex.md
agy -p "Activate the code review skill. Review the current branch diff and write findings to review-agy.md." --dangerously-skip-permissions --log-file "$(mktemp -t agy_review.XXXXXX)"  # silent-failure detection — see reference/antigravity-review-usage.md §Silent Failure Detection
claude -p "Review the current branch diff. Output: review-claude.md — include severity, file:line, evidence, suggested fix." --permission-mode plan > review-claude.md
```

Findings flagged by ≥2 engines elevate to high-priority; single-engine findings require verification.

### 14. Fan-Out Across Files

For large diffs where per-file depth matters, parallelize with `-p`:

```bash
for file in $(git diff --name-only origin/main...HEAD); do
  claude -p "Review $file for bugs, security, logic errors, and consistency with surrounding code. Severity-rank findings. File: $file" \
    --permission-mode plan \
    --allowedTools "Read,Grep,Glob" \
    > "review-$(echo $file | tr '/' '_').json"
done
```

`--max-budget-usd` caps fan-out spend for automation safety.

---

## Prompt Structure (Official Best Practice)

Align with Anthropic's Best Practices guide. Effective Claude Code prompts follow:

| Element | Purpose |
|---------|---------|
| **Scope the task** | Which files, which branch, which diff range |
| **Point to sources** | Reference files with `@path/to/file`, link to related git history, CLAUDE.md rules |
| **Reference existing patterns** | Name a file that exemplifies the expected style |
| **Describe the symptom + fixed state** | For regressions: what broke + what "fixed" looks like |

Use `@` to reference files inline — Claude reads them before responding, preserving context efficiency. Keep `CLAUDE.md` lean; rely on the session default and project memory rather than restating conventions per prompt.

---

## Interactive Slash Commands

Inside an active `claude` session:

| Command | Scope |
|---------|-------|
| `/review` | Built-in PR review skill (reviews pending changes) |
| `/security-review` | Built-in security review skill (security-focused) |
| `/trail` (or `Esc` `Esc`) | Trail conversation/code to an earlier checkpoint — useful when review correction loops pollute context |
| `/clear` | Reset context entirely between unrelated review tasks |
| `/compact <instructions>` | Targeted compaction (e.g., `/compact Focus on review findings`) |

Judge primarily uses the headless `-p` form. Mention slash commands only when the user is already inside a `claude` TUI.

---

## Decision Flow

```
User request → check environment →
  claude binary present?                          → (if no) abort, suggest Codex
  already inside a Claude session?                → use subagent delegation ("Use a subagent to review …")
  locked CI with pre-approved tools only?         → --permission-mode dontAsk + --allowedTools "Read Grep Glob Bash(git *)"
  PR URL or number + existing PR-linked local session? → recipe 4 (`--from-pr`, resume only)
  PR URL or number but no prior linked session?   → recipe 1 (`--base <PR base branch>`) or `/review`
  uncommitted changes + pre-commit context?       → recipe 2
  SHA given?                                      → recipe 3
  security-specific ask?                          → recipe 6 (/security-review or headless equivalent)
  branch review default?                          → recipe 1
  JSON required by CI?                            → add `--output-format json` or `--json-schema`
  three-engine cross-verify?                      → recipe 13
  auto mode requested + user on Max/Team/Enterprise/API? → --permission-mode auto (else reject; Pro is not supported)
```

Default headless runs pair with `--permission-mode plan`. For fully unattended CI, prefer `dontAsk` with a narrow `--allowedTools` allowlist. Use `auto` only when the user has a qualifying plan AND the review must run tools beyond reading.

---

## Do / Don't

### Do

- Keep authentication implicit via subscription login; never export `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` for this flow.
- Omit `--model`; always use the session default.
- Always enforce a fresh review context: subagent delegation (interactive) or `-p` + plan mode (headless). Main-context review is forbidden by Judge's Core Contract.
- Pair `-p` with `--permission-mode plan` for read-only safety.
- Reference files with `@path/to/file` instead of pasting contents — preserves context.
- Use `--json-schema` when CI needs deterministic parsing.
- Cap fan-out with `--max-budget-usd`.
- Use `/clear` between unrelated reviews when interactive; in headless, each `-p` invocation is already a fresh session.

### Don't

- Don't set `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, or cloud provider credentials — subscription login is already active.
- Don't pass `--bare` — it bypasses subscription auth and forces API-key mode.
- Don't override the model with `--model`.
- Don't run Claude-based review in the main conversation context (self-bias invalidates findings).
- Don't combine `--permission-mode plan` with tool-mutating requests — the run will stall.
- Don't use `--dangerously-skip-permissions` or `--allow-dangerously-skip-permissions` for reviews — review tasks never justify disabling permissions.
- Don't combine `--permission-mode auto` with non-interactive `-p` unless you accept that the run aborts when the classifier repeatedly blocks actions.

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| `command not found: claude` | CLI not installed or not on `$PATH` | Ask the user to install; fall back to Codex |
| OAuth / login prompt in headless | Subscription session expired | Instruct the user to run `claude` once interactively to re-login; do not supply API keys |
| Review stalls with permission requests | Missing `--permission-mode plan` (or `auto`) in headless | Re-run with `--permission-mode plan`; permission prompts block in `-p` mode |
| Empty or shallow findings | Prompt too vague, CLAUDE.md missing, or context starved | Add goal/scope/pattern references per the Prompt Structure table |
| JSON output malformed | No `--json-schema` and prompt didn't pin the schema | Add `--json-schema '<schema>'` or `--output-format json` with explicit schema in the prompt |
| Self-biased findings | Review ran in the main context | Re-run via `-p` headless or delegate to a subagent; main-context review is forbidden |
| Hits `--max-budget-usd` cap | Fan-out too large or prompt too expensive | Narrow scope, lower effort, or raise the budget deliberately |
| Auto mode aborts mid-run | Classifier blocked 3 consecutive or 20 total actions | Switch to `plan` mode for pure analysis; reserve `auto` for review + test runs |
| Auto mode "unavailable" error | User on Pro plan, or non-Anthropic provider, or non-Sonnet/Opus model | Switch to `plan` or `dontAsk`; auto requires Max/Team/Enterprise/API + Sonnet 4.6 / Opus 4.6 / Opus 4.7 |
| Protected-path prompt during review | Reviewer tried to write `.git`, `.vscode`, `.claude/*` (except commands/agents/skills), shell rc files, or `.mcp.json` | Review flows should never write to these — narrow the prompt to forbid modifications |

---

## Cross-References

- Codex CLI review (default engine): `codex-review-usage.md`.
- Antigravity CLI review (alternative engine): `antigravity-review-usage.md`.
- Output interpretation, severity mapping, override rules, false-positive filtering (engine-agnostic): `codex-integration.md`.
- Framework-specific review prompts: `framework-reviews.md`.
- AI-generated code review depth and hallucination checks: `ai-review-patterns.md`.
- PR size cognitive-load thresholds: `review-effectiveness.md`.

### Official Sources (2026)

- Claude Code Best Practices — <https://code.claude.com/docs/en/best-practices>
- Claude Code CLI Reference (all flags) — <https://code.claude.com/docs/en/cli-reference>
- Claude Code Permission Modes (plan / auto / dontAsk / protected paths) — <https://code.claude.com/docs/en/permission-modes>
- Claude Code Subagents (`.claude/agents/`, `--agents`, bias isolation) — <https://code.claude.com/docs/en/sub-agents>
- Claude Code Skills (`/review`, `/security-review`) — <https://code.claude.com/docs/en/skills>
- Claude Code Headless Mode — <https://code.claude.com/docs/en/headless>
- Claude Code Authentication (`claude auth login`, `setup-token`) — <https://code.claude.com/docs/en/authentication>
- Structured Outputs (`--json-schema`) — <https://code.claude.com/docs/en/agent-sdk/structured-outputs>
- Auto Mode announcement (engineering deep dive) — <https://www.anthropic.com/engineering/claude-code-auto-mode>
