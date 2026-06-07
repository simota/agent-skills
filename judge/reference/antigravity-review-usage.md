# Antigravity CLI Review Usage

Operational reference for using Google's Antigravity CLI as a review engine. This file is the authoritative "how to run an Antigravity CLI (`agy`) review" guide. For Codex CLI, see `codex-review-usage.md`. For output interpretation (severity mapping, false-positive filtering), see `codex-integration.md` — those rules apply across engines.

**agy is the OPTIONAL third engine** in Judge's default multi-engine parallel review. The default baseline is Claude + Codex (dual-engine); when agy is AVAILABLE at PREFLIGHT, a third subagent (`review-agy`) joins the fan-out for tri-engine mode — see `tri-engine-review.md` for the full algorithm. This file is consumed by the `review-agy` subagent during that fan-out. Use it directly as a single-engine review only when: the user explicitly requests an Antigravity CLI-only review, both Claude and Codex are unavailable, cross-verification against an already-run engine is needed, or the repository's GitHub Actions use the `gemini-cli` extension and local parity is desired. **When agy is UNAVAILABLE or RUNTIME-BROKEN, Judge runs in dual-engine mode without aborting** — this file is simply not consumed.

---

## Prerequisites

| Item | Requirement | Notes |
|------|-------------|-------|
| Binary | `agy` on `$PATH` **or** at a known fallback path | `agy --version` must succeed. See **Robust availability detection** below — never declare unavailable based on a single `command -v` miss. The `code-review` extension runs on current `0.38.x` CLI builds; upgrade to the latest release (`npm i -g @google/gemini-cli@latest`) if `agy plugin install` returns "unknown command" |
| Authentication | Google account login (OAuth browser flow) | Subscription-backed login; **do not** set `GEMINI_API_KEY`, `GOOGLE_API_KEY`, or Vertex env vars for this flow |
| Model | Default (no `-m` / `--model` flag) | Always rely on the CLI default — never override |
| Extension | `code-review` extension installed | `agy plugin install https://github.com/gemini-cli-extensions/code-review` |
| Working directory | Git repository root | Review commands operate on the current git worktree |
| Approval mode | `--dangerously-skip-permissions` for headless runs | Required for non-interactive automation; for read-only analysis, phrase the prompt to forbid writes ("do not modify any files") |

**Never** pass `-m`, `--model`, set `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `GOOGLE_CLOUD_PROJECT`, or `GOOGLE_CLOUD_LOCATION` for this flow. Authentication is managed by the user's Google subscription login.

### Robust availability detection

`agy` is commonly installed under `~/.local/bin/agy`, `/usr/local/bin/agy`, `/opt/homebrew/bin/agy`, or via the official curl install script (`curl -fsSL https://antigravity.google/cli/install.sh | bash`). A subagent's inherited `$PATH` is often narrower than the user's interactive shell — `command -v agy` failing inside a subagent does **not** mean the binary is missing. Always probe fallback paths before declaring unavailability:

```bash
if command -v agy >/dev/null 2>&1; then
  AGY_BIN="$(command -v agy)"
else
  for p in "$HOME/.local/bin/agy" "/usr/local/bin/agy" "/opt/homebrew/bin/agy" "$HOME/.bun/bin/agy"; do
    [ -x "$p" ] && AGY_BIN="$p" && break
  done
fi
[ -n "$AGY_BIN" ] && "$AGY_BIN" --version || echo "agy: not found in any known location"
```

When invoking via the resolved absolute path, substitute `"$AGY_BIN"` for `agy` in every subsequent command in this guide.

**Do not classify these as "unavailable":** auth-expired errors, OAuth re-login prompts, missing `code-review` extension (install it instead — runtime fixable), transient network failures, quota errors. These are runtime failures — surface the real error rather than silently dropping the engine from the roster.

Verify the extension once:

```bash
agy plugin list | grep code-review
# If absent:
agy plugin install https://github.com/gemini-cli-extensions/code-review
```

---

## Command Reference

### Syntax

```
agy -p "<prompt>" [OPTIONS]
```

Non-interactive review always uses `-p` (prompt) plus `--dangerously-skip-permissions`. The `code-review` plugin (if installed via `agy plugin install`) is auto-loaded; there is no `-e`/`--extensions` flag in Antigravity CLI.

### Flag Matrix (verified against `agy --help` v1.0.2 + official DEV.to examples, 2026-05)

| Flag | Purpose | Required for review? |
|------|---------|----------------------|
| `-p, --print, --prompt <STR>` | Headless prompt — runs once and exits | Yes |
| `--dangerously-skip-permissions` | Auto-approve all tool actions (needed for headless) | Yes for headless |
| `--output-format <FMT>` | Structured output (e.g. `json`) — **UNRELIABLE (2026-06)**: availability inconsistent across installs ("flag not defined" reports), schema undocumented | No — request JSON inside the §9.2 artifact file instead |
| `--add-dir <PATH>` | Add a directory to the workspace (repeatable) | When review spans multiple repos |
| `--sandbox` | Run in a sandbox with terminal restrictions enabled | For isolated/risky reviews |
| `-c, --continue` | Continue the most recent conversation | For iterative review sessions |
| `--conversation <ID>` | Resume a previous conversation by ID | For long-running reviews |
| `-i, --prompt-interactive <STR>` | Run an initial prompt interactively and continue | When user wants to follow up |
| `--log-file <PATH>` | Override CLI log file path | For debugging or audit trails |
| `--print-timeout <DURATION>` | Timeout for print mode wait (default 5m0s) | When prompt may take >5 min |

Authentication is resolved from the Google login session — do not supply API keys. There is no `-m`/`--model`, no `--approval-mode`, no `-e`/`--extensions` flag. Plugin loading is implicit once installed via `agy plugin install`.

**File reference syntax**: always use `@<path>` (e.g. `@docs/spec.md`) inside the prompt. Bare path strings trigger silent subagent timeouts at the 60s cap — main agent stays alive while the delegated read dies and produces `exit 0` + empty stdout. v1.0.2 changelog: "restricted the default 60-second interaction timeout specifically to subagents, preventing the main agent from being unconditionally capped."

**⚠ Pre-flight Notification (mandatory)**: before the first `agy -p ... --dangerously-skip-permissions` review of a session, emit the Pre-flight Notification per `_common/CLI_COMPATIBILITY.md §9.1`. This recommends running `/update-config` once to allowlist the Bash pattern in `settings.json` `permissions.allow` — the combination of agy's autonomous tool use plus Claude Code's Bash spawn would otherwise bypass approval gates on both layers. The notification is informational and does not block headless review.

### Canonical Commands

```bash
# Headless review of the current branch using the code-review extension
agy -p "Activate the code review skill and review all code changes on the current branch. Report bugs, security issues, logic errors, and intent misalignment with severity." --dangerously-skip-permissions

# Write the review to a file for downstream processing
agy -p "Activate the code review skill, review the current branch diff, and write the findings to code-review.md." --dangerously-skip-permissions

# Structured JSON output (for CI pipelines — write JSON to an ABSOLUTE-path artifact file;
# stdout never flushes to non-TTY (issue #115) and --output-format json is unreliable)
agy -p "Review the current branch diff. Write findings as JSON ({severity, file, line, issue, suggested_fix}) to the absolute path /tmp/agy-review.json, ending the file with a final line <<<END_OF_OUTPUT>>>. Print only 'DONE /tmp/agy-review.json' to stdout." --dangerously-skip-permissions

# Plan mode (read-only, no writes to disk)
agy -p "Review the current branch diff and summarize risks; do not modify any files."
```

---

## Use Case Cookbook

Pick the recipe that matches the user's request. Every recipe uses Google login + default model — only the prompt and flags change. Keep `--dangerously-skip-permissions` unless noted. The `code-review` plugin must be installed beforehand via `agy plugin install`.

### 1. Current-Branch Review (PR-equivalent)

Use when the user says "review this branch", "review my PR with Gemini", or wants an alternative to Codex PR review.

```bash
agy -p "Activate the code review skill. Review all diffs on the current branch vs its upstream base. Focus on correctness, security, logic errors, and edge cases. Report findings with severity (CRITICAL/HIGH/MEDIUM/LOW/INFO), file:line, evidence, and suggested fix." --dangerously-skip-permissions
```

### 2. Pre-Commit / Uncommitted Changes

Use when the user has uncommitted work and wants a Gemini pre-commit check.

```bash
agy -p "Activate the code review skill. Review staged, unstaged, and untracked changes in the working tree. Identify bugs, security issues, missing error handling, and logic errors before commit. Severity-rank findings." --dangerously-skip-permissions
```

### 3. Specific Commit Review

Use when the user passes a SHA.

```bash
agy -p "Activate the code review skill. Review only the changes introduced by commit <SHA>. Report bugs, regressions, and logic errors with severity and line references." --dangerously-skip-permissions
```

Substitute `<SHA>` with the actual commit hash.

### 4. Pull Request Review (GitHub MCP-backed)

Use when the user provides a PR URL and the repo has the GitHub MCP server enabled. The extension exposes `/pr-code-review`.

```bash
# Via env vars
REPOSITORY=owner/repo PULL_REQUEST_NUMBER=1234 \
  agy -p "/pr-code-review" --dangerously-skip-permissions

# Or inline
agy -p "/pr-code-review https://github.com/owner/repo/pull/1234" --dangerously-skip-permissions

# With focus areas
REPOSITORY=owner/repo PULL_REQUEST_NUMBER=1234 \
ADDITIONAL_CONTEXT="Focus on authentication and session handling." \
  agy -p "/pr-code-review" --dangerously-skip-permissions
```

If the GitHub MCP server is not configured, fall back to recipe 1 (current-branch review) after checking out the PR branch locally.

### 5. Security-Focused Review

```bash
agy -p "Activate the code review skill. Security focus: injection (SQL/NoSQL/command), XSS, SSRF, auth bypass, authorization gaps, hardcoded secrets, unsafe deserialization, missing input validation, insecure crypto, and sensitive data in logs. Severity-rank findings." --dangerously-skip-permissions
```

Route CRITICAL/HIGH findings to Sentinel per SKILL.md collaboration.

### 6. Intent-Alignment Review

```bash
agy -p "Activate the code review skill. Verify code changes on the current branch match the stated intent. Flag unrelated changes, scope creep, and missing changes implied by the description. Intent: <paste PR title + description here>." --dangerously-skip-permissions
```

### 7. AI-Generated Code Scrutiny

```bash
agy -p "Activate the code review skill. Elevated scrutiny for AI-generated code. Check (1) logic errors in boundary/edge cases, (2) missing input validation and sanitization, (3) hallucinated imports/APIs/classes — verify every imported symbol exists in the codebase, (4) security shortcuts (hardcoded values, permissive CORS, credential exposure), (5) absent defenses, (6) performance anti-patterns." --dangerously-skip-permissions
```

### 8. Framework-Specific Review

Append framework focus to any recipe. Keep `--dangerously-skip-permissions`.

```bash
# React / Next.js
agy -p "Activate the code review skill. React/Next.js focus: hook dependency arrays, effect cleanup, server/client boundary ('use client'), data fetching in server components, hydration mismatches, memoization correctness." --dangerously-skip-permissions

# TypeScript
agy -p "Activate the code review skill. TypeScript focus: unsafe 'as' casts, 'any' escapes, discriminated union exhaustiveness, nullability, generic constraints." --dangerously-skip-permissions

# Go
agy -p "Activate the code review skill. Go focus: error wrapping, goroutine leaks, channel close semantics, context propagation, race conditions." --dangerously-skip-permissions
```

### 9. Consistency Audit

```bash
agy -p "Activate the code review skill. Consistency audit across files: error handling patterns, null-safety style, async patterns, naming, imports, error types. Report outliers when a dominant pattern (≥70%) exists." --dangerously-skip-permissions
```

### 10. Test Quality Review

```bash
agy -p "Activate the code review skill. Test quality focus: isolation, flakiness risk, edge case coverage, mock fidelity, readability. Flag tests that depend on ordering, shared state, time, or network." --dangerously-skip-permissions
```

### 11. Project-Guideline-Gated Review

```bash
# REVIEW.md (Judge convention) piped via stdin
cat REVIEW.md | agy -p "Activate the code review skill. Apply the guidelines from stdin to the current branch diff." --dangerously-skip-permissions

# AGENTS.md / GEMINI.md (Gemini native) — Gemini auto-discovers GEMINI.md and AGENTS.md in the workspace
agy -p "Activate the code review skill. Review the current branch diff following project AGENTS.md and GEMINI.md conventions." --dangerously-skip-permissions
```

### 12. Cross-Engine Verification

Use when the user wants dual-engine review (Codex + Antigravity) to elevate confidence on findings.

```bash
# Run both sequentially, writing to distinct files for diffing
codex review --base main "Focus on bugs, security, and logic errors." > review-codex.md
agy -p "Activate the code review skill. Review the current branch diff and write findings to review-agy.md." --dangerously-skip-permissions
```

Apply the multi-agent verification rules in `codex-integration.md` — findings flagged by both engines elevate to high-priority.

### 13. Structured JSON Output for CI

```bash
# Write JSON to an absolute-path artifact — stdout is not a reliable channel (issue #115)
agy -p "Activate the code review skill. Review the current branch diff. Write strict JSON to the absolute path /tmp/agy-review-ci.json: {\"findings\":[{\"severity\":\"CRITICAL|HIGH|MEDIUM|LOW|INFO\",\"file\":\"...\",\"line\":N,\"issue\":\"...\",\"evidence\":\"...\",\"suggested_fix\":\"...\"}]}. End the file with a final line <<<END_OF_OUTPUT>>>." --dangerously-skip-permissions
```

---

## Prompt Structure (Recommended)

Align with the Codex 2026 best practice: structure every non-trivial review prompt with four elements. This applies identically to Gemini.

| Element | Purpose |
|---------|---------|
| **Goal** | What is being reviewed and why |
| **Context** | Relevant files, standards, prior decisions |
| **Constraints** | Architectural patterns, non-negotiables |
| **Done when** | Acceptance criteria for a clean review |

Gemini also auto-discovers `GEMINI.md` and `AGENTS.md` in the workspace — keep repo-wide review norms there rather than repeating them in every prompt.

---

## Interactive Slash Commands

Inside an active `agy` TUI session (with `code-review` extension loaded), two slash commands are available:

| Command | Scope |
|---------|-------|
| `/code-review` | Review code changes on the current branch |
| `/pr-code-review [url\|env]` | Review a GitHub pull request (requires GitHub MCP server) |

Judge primarily uses the headless `-p` form. Mention slash commands to the user only when they are already inside a `agy` TUI session.

---

## Decision Flow

```
User request → check environment →
  agy binary present?                            → (if no) abort, suggest Codex
  code-review extension installed?               → (if no) suggest install command, ask to proceed
  PR URL given + GitHub MCP enabled?             → recipe 4 (/pr-code-review)
  uncommitted changes + pre-commit context?      → recipe 2
  SHA given?                                     → recipe 3
  branch review default?                         → recipe 1
  JSON required by CI?                           → add `-o json`
```

Always pair the prompt with `--dangerously-skip-permissions` for headless runs unless the user explicitly asks for plan mode.

---

## Do / Don't

### Do

- Keep authentication implicit via Google login; never export `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `GOOGLE_CLOUD_PROJECT`, or `GOOGLE_CLOUD_LOCATION` for this flow.
- Omit `-m` / `--model`; always use the default model.
- Pair `-p` with `--dangerously-skip-permissions` for headless runs; tools require auto-approval in non-interactive mode.
- Install the `code-review` plugin once via `agy plugin install <url>`; loading is implicit on subsequent runs.
- Place repo-wide review conventions in `GEMINI.md` or `AGENTS.md` instead of restating them per prompt.
- For CI-consumed structured output, pin the JSON schema in the prompt itself (Antigravity CLI has no `--output-format` flag — output shape comes from the prompt).
- For analysis-only with zero write risk, phrase the prompt to forbid writes ("do not modify any files; report only").

### Don't

- Don't set any provider API key or cloud project env var — subscription login is already active.
- Don't override the model with `-m`, `--model`.
- Don't run headless without `--dangerously-skip-permissions`; tools will block awaiting approval and the run will hang.
- Don't rely on `/pr-code-review` unless the repo has the GitHub MCP server configured.
- Don't use Gemini when the user explicitly asked for Codex, or vice-versa. Fall back only on explicit unavailability.
- Don't pass flags from Gemini CLI that Antigravity CLI does not support — no `--yolo` (renamed to `--dangerously-skip-permissions`), no `-e`/`--extensions` (use `agy plugin install`), no `--approval-mode`, no `-m`/`--model`. Note: `--output-format` IS supported (hidden — absent from `agy --help` but documented in official Google DEV.to examples). Use `agy --help` plus DEV.to as joint references — `--help` alone is insufficient.

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| `command not found: agy` | CLI not on `$PATH` of current shell — but the binary may exist | First try fallback paths (`~/.local/bin/agy`, `/usr/local/bin/agy`, `/opt/homebrew/bin/agy`, `~/.bun/bin/agy`); only ask the user to install if none are executable. Subagents see a narrower PATH than interactive shells |
| Subagent reports "agy unavailable" but user confirms it works | Subagent PATH narrower than interactive shell | Re-run preflight in main Judge context; pass the absolute binary path into the subagent prompt |
| Authentication prompt or failure | Google login session expired | Instruct the user to run `agy` once interactively to re-login; do not supply API keys |
| Extension missing | `code-review` not installed | Run `agy plugin install https://github.com/gemini-cli-extensions/code-review` and retry |
| Hang with no output | Missing `--dangerously-skip-permissions` in headless mode | Re-run with `--dangerously-skip-permissions`; tool approvals were blocking |
| **Exit 0 with empty stdout (silent failure)** | **agy CLI v1.0.0 does not surface server-side errors (`RESOURCE_EXHAUSTED` 429 quota / OAuth token revoked / upstream agent executor error) to stdout — it writes them only to the CLI log and exits 0** | **Always invoke with `--log-file <path>` (see "Silent Failure Detection" below). On empty stdout, grep the log for `RESOURCE_EXHAUSTED`, `429`, `Resets in`, `error getting token`, `agent executor error`. Quota → wait for `Resets in NhNm` window or request overage. Auth → run `agy` interactively once to refresh login. Treat as `RUNTIME-BROKEN`, not `UNAVAILABLE`** |
| `mcp_config.json` parse error | `~/.gemini/config/mcp_config.json` is missing or empty (0-byte file or truncated JSON) | Initialize with `printf '{}\n' > ~/.gemini/config/mcp_config.json`. The CLI logs `Failed to load JSON config file ... unexpected end of JSON input` and continues, but MCP-backed flows (e.g., `/pr-code-review`) will fail downstream |
| `/pr-code-review` fails | GitHub MCP server not configured | Fall back to recipe 1 after checking out the PR branch locally |
| Empty or shallow findings | Prompt too vague or no GEMINI.md context | Structure prompt with goal/context/constraints/done-when; add a `GEMINI.md` or `AGENTS.md` if missing. **Note**: distinguish from "Exit 0 with empty stdout" above — shallow ≠ zero |
| JSON output malformed | Prompt did not specify strict schema | Restate the exact JSON schema in the prompt and retry |

### Silent Failure Detection

`agy` silently swallows several runtime-fatal errors to its log file while exiting 0 with empty stdout — quota exhaustion (`RESOURCE_EXHAUSTED` 429 with a `Resets in NhNm` window), OAuth token expiry, upstream model unavailability, corrupt `mcp_config.json`. **Additionally: agy REQUIRES a TTY — from a socket-stdin shell (Claude Code `Bash`, CI, cron) `agy -p` hangs to `exit 124` with no artifact/log, and `script -q /dev/null agy ...` fails with `tcgetattr/ioctl: Operation not supported on socket` (verified 2026-06-08, agy 1.0.6). And (unfixed through v1.0.6, issue #115) `agy -p` never flushes its response to a non-TTY stdout, so a SUCCESSFUL review also produces `exit 0 + empty stdout` when piped.** Capture must therefore give agy a real pty (`python3 pty.spawn`) and use the file-handoff protocol (`_common/CLI_COMPATIBILITY.md §9.2`), not stdout.

**Mandatory pattern for headless invocations** (prompt must mandate the artifact write per §9.2; agy gets a real pty via python pty.spawn — `script -q /dev/null` does NOT work here):

```bash
OUT="/tmp/agy-review.md"; LOG="/tmp/agy-review.log"
rm -f "$OUT"
# Prompt ends with: "Write your COMPLETE findings to the absolute path /tmp/agy-review.md,
#   final line <<<END_OF_OUTPUT>>>; print only a one-line status to stdout."
# Write the prompt to /tmp/agy-review.prompt first, then:
python3 - "$LOG" <<'PY' || true
import pty, sys
pty.spawn(["agy","-p",open("/tmp/agy-review.prompt").read(),"--dangerously-skip-permissions",
           "--log-file",sys.argv[1],"--print-timeout","15m"])
PY

if ! { [ -s "$OUT" ] && grep -q '<<<END_OF_OUTPUT>>>' "$OUT"; }; then
  # Fallback: transcript harvest, then log grep (full chain: CLI_COMPATIBILITY §9.2)
  grep -E "RESOURCE_EXHAUSTED|Resets in|error getting token|agent executor error|unexpected end of JSON input" "$LOG" | head -5
  echo "VERDICT: agy produced no verifiable artifact. Treat as RUNTIME-BROKEN (not UNAVAILABLE). Skip this engine for this review and surface the log excerpt in the integration report."
fi
```

Engine concurrence tags (`[codex+agy+claude]`) must not be emitted when `review-agy` returned empty output — record `agy: RUNTIME-BROKEN (reason: <quota|auth|mcp_corrupt>)` in the rejections ledger instead.

---

## Cross-References

- Codex CLI review (default engine): `codex-review-usage.md`.
- Claude Code CLI review (alternative engine, subagent/plan-mode required): `claude-review-usage.md`.
- Output interpretation, severity mapping, override rules, false-positive filtering (engine-agnostic): `codex-integration.md`.
- Framework-specific review prompts: `framework-reviews.md`.
- AI-generated code review depth: `ai-review-patterns.md`.
- PR size cognitive-load thresholds: `review-effectiveness.md`.

### Official Sources (2026)

- Antigravity CLI — <https://github.com/google-gemini/gemini-cli>
- Antigravity CLI Code-Review Extension — <https://github.com/gemini-cli-extensions/code-review>
- Antigravity CLI Codelab (Code Review & Security Analysis) — <https://codelabs.developers.google.com/gemini-cli-code-analysis>
- Antigravity CLI — Gemini Code Assist docs — <https://developers.google.com/gemini-code-assist/docs/gemini-cli>
- Antigravity CLI Plan Mode — <https://geminicli.com/docs/cli/plan-mode/>
