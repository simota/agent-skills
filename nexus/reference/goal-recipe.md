# Nexus Goal Setup Recipe Reference

**Purpose:** Configuration helper chain for `/goal` autonomous long-running execution on Claude Code (v2.1.139+) and Codex CLI (experimental `[features] goals = true`).
**Read when:** User invokes `/nexus goal` or asks to set up, audit, or tune `/goal` for the first time, generate use-case-specific launch recipes, or harden existing setup with hooks and permission boundaries.

## Contents
- Overview
- When to Use the Goal Recipe
- Invocation Modes
- Platform Detection
- Use Case Templates
- Chain Phases (1 → 6)
- Conditional Agent Inclusion
- Hook Templates
- Launch Command Recipes
- AUTORUN Chain Template
- Output Format
- Failure Modes
- Cost and Latency Profile

---

## Overview

The `goal` recipe is a **lightweight setup helper**. It does not implement features or run `/goal` for the user — it produces a tailored configuration package:

1. Which CLI to target (Claude Code / Codex / both)
2. Which use case (ci-headless / long-dev / parallel-experiment / safe-bounded)
3. Audit diff of current config (Hone)
4. Hook configuration for completion verification and notification (Latch)
5. CLAUDE.md or AGENTS.md additions when missing (Scribe, conditional)
6. Ready-to-run launch command with verification checklist

The user is the executor. Nexus never edits `~/.claude/` or `~/.codex/` directly under this recipe.

## When to Use the Goal Recipe

Use `goal` when the user:
- Wants to set up `/goal` for the first time
- Asks for the right hooks / permissions / sandbox combination for autonomous runs
- Needs a launch command for CI, long dev, parallel experiments, or sensitive repos
- Wants to audit existing `/goal` setup against best practices

Route elsewhere when:
- User wants to actually run `/goal` for a task — that is just the underlying CLI, not Nexus
- User wants generic CLI config audit without `/goal` context → `hone` directly
- User wants generic hook design without `/goal` context → `latch` directly

## Invocation Modes

| Form | Behavior |
|------|----------|
| `/nexus goal` | Detect platform from filesystem; ask for use case if confidence < 0.7 |
| `/nexus goal platform=<claude\|codex\|both>` | Skip platform detection |
| `/nexus goal use_case=<ci-headless\|long-dev\|parallel-experiment\|safe-bounded>` | Skip use-case classification |
| `/nexus goal platform=<X> use_case=<Y>` | Skip both, go directly to AUDIT |
| `/nexus goal minimal` | Skip Latch (hooks) and Scribe (context-md); deliver launch command only |

Default when unspecified: detect platform, ask for use case if ambiguous, default to `safe-bounded`.

## Platform Detection

Inline detection (no agent spawn). Apply in order:

| Signal | Action |
|---|---|
| `CLAUDE.md` exists in cwd | Claude Code is primary |
| `AGENTS.md` exists in cwd | Codex CLI is primary |
| Both `CLAUDE.md` and `AGENTS.md` exist | Multi-platform — ask user to pick primary |
| Only `~/.claude/settings.json` exists globally | Claude Code |
| Only `~/.codex/config.toml` exists globally | Codex CLI |
| Both global configs exist, no project marker | Ask user once |
| Neither global config exists | Stop: instruct user to install Claude Code or Codex CLI first |

Emit `PLATFORM = claude-code | codex | both` for downstream phases.

## Use Case Templates

| Use Case | When | Boundaries | Key Features |
|---|---|---|---|
| `ci-headless` | Unattended CI/CD, GitHub Actions, scheduled tasks, cron | Hard turn/budget limits, no interactive approval, structured output | `claude -p` / `codex exec`, `--output-format json` (+ file redirect) / `--json` + `-o <path>`, exit code propagation. ⚠ `--max-turns` / `--max-budget-usd` absent from current headless docs (2026-06) — verify via `claude --help` before use |
| `long-dev` | Multi-hour refactor, migration, large feature work | Resumable sessions, context compaction, project context | CLAUDE.md / AGENTS.md, `/compact`, `--resume <name>` / `codex resume --last`, named sessions, status line |
| `parallel-experiment` | A/B approach comparison, alt-design exploration, spike runs | Isolated sessions, branched goals, worktrees | `/branch` (Claude Code), `/fork` (Codex), git worktree isolation, parallel `/goal` in separate sessions |
| `safe-bounded` | Production-adjacent, sensitive repo, junior operator | Strict permissions, sandboxed filesystem, gated approvals, explicit deny rules | Permission rules with `deny` (Claude Code), Codex `sandbox_mode = workspace-write` + `approval_policy = on-request`, profile lock |

Default if user unspecified: `safe-bounded` (least-privilege wins).

## Chain Phases

### Phase 1 — PLATFORM_DETECT (inline, no agent)

- Run platform detection rules above
- Emit `PLATFORM` and write to chain state
- If neither CLI is detected, stop with an install instruction

### Phase 2 — USE_CASE_CLASSIFY (inline or single user question)

- Signal scan: presence of `.github/workflows/`, recent `claude --resume` usage, git worktrees, etc.
- If confidence ≥ 0.7 → auto-select use case
- Else → ask user one focused question with the four options

### Phase 3 — AUDIT (Hone)

**Agent:** Hone
**Inputs:** `PLATFORM`, `USE_CASE`, optional repo path
**Outputs:** Before/After diff covering:

- Claude Code: `~/.claude/settings.json` (permission rules, hooks, status line), `CLAUDE.md`, MCP server registrations
- Codex CLI: `~/.codex/config.toml` (`[features]`, `[profiles]`, `[mcp_servers]`, `[agents]`, `[tui]`, `notify`), `AGENTS.md`, `~/.codex/hooks.json`
- Cross-platform: env vars, shell aliases, CI tokens

Hone never edits files; it produces diff suggestions only.

### Phase 4 — HOOKS (Latch)

**Agent:** Latch
**Inputs:** `PLATFORM`, `USE_CASE`, audit findings
**Outputs:** Hook configuration snippets ready to install:

| Hook | Purpose | Both Platforms |
|---|---|---|
| Completion verification | Run tests, check build, validate exit code at goal stop | Stop hook + PostToolUse hook |
| Notification | Desktop / Slack / webhook on goal completion | Stop hook + `notify` (Codex) |
| Budget alert | Warn at token/cost threshold | PreToolUse hook (Claude Code), TUI notification (Codex) |
| Guard | Block dangerous commands during `/goal` | PreToolUse hook with `deny` patterns |

See **Hook Templates** below for concrete snippets.

### Phase 5 — CONTEXT_DOCS (Scribe, conditional)

**Agent:** Scribe
**Include when:** CLAUDE.md / AGENTS.md missing OR lacks `/goal`-friendly conventions (observable completion vocabulary, danger zones, dependency commands).

**Outputs:** Draft additions for:

- Project goals and observable completion criteria vocabulary
- Test commands and their exit-code semantics
- Danger zones (files / dirs to avoid auto-edits)
- Compaction-friendly summary anchors

### Phase 6 — DELIVER (Nexus inline)

Aggregate all outputs into the Output Format below. Verify schema (`PLATFORM`, `USE_CASE`, diff, hooks, launch command all present). Emit `NEXUS_COMPLETE`.

## Conditional Agent Inclusion

| Agent | Include when | Skip when |
|---|---|---|
| Hone (Phase 3) | Default | Brand-new install with no existing config — replace with template diff |
| Latch (Phase 4) | Default | User passed `minimal` flag, or use case is `parallel-experiment` (hooks would clash across forks) |
| Scribe (Phase 5) | CLAUDE.md / AGENTS.md missing or thin | Existing context doc already declares observable completion criteria and danger zones |

Minimum chain: Hone alone (1 agent). Typical chain: Hone + Latch (2 agents). Maximum chain: Hone + Latch + Scribe (3 agents).

## Hook Templates

### Claude Code: Stop hook for completion verification + notification

`~/.claude/settings.json` excerpt:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "if npm test --silent > /tmp/goal-test.log 2>&1; then osascript -e 'display notification \"/goal completed: tests pass\" with title \"Claude Code\"'; else osascript -e 'display notification \"/goal stopped: tests failing\" with title \"Claude Code\"'; fi"
      }]
    }]
  }
}
```

### Claude Code: PreToolUse hook for budget guard

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/budget-check.sh"
      }]
    }]
  }
}
```

### Codex CLI: hooks via `~/.codex/config.toml`

```toml
[features]
hooks = true
goals = true

[[hooks.Stop]]
type = "command"
command = "/usr/local/bin/notify-goal-done.sh"
timeout_ms = 5000

[[hooks.PostToolUse]]
type = "command"
command = "bash -c 'npm test --silent'"
timeout_ms = 60000
```

**Known constraint:** Codex hooks reliably fire on the shell tool but not on `apply_patch` and many MCP calls. Account for this when designing completion verification. (Source: github.com/openai/codex Issue #16732)

### Codex CLI: top-level `notify` (hooks feature not required)

```toml
notify = ["python3", "/path/to/notify.py"]
```

The script receives `agent-turn-complete` and similar events as JSON on stdin.

## Launch Command Recipes

### ci-headless — Claude Code

```bash
# ⚠ 2026-06 re-verification: --max-turns / --max-budget-usd are NOT in the current
# headless docs (code.claude.com/docs/en/headless) — verify with `claude --help` before
# relying on them; cost is surfaced read-only via total_cost_usd in the JSON output.
# Capture: --output-format json + FILE REDIRECT (not pipe) per _common/CLI_COMPATIBILITY.md §9.3.
claude -p \
  --permission-mode auto \
  --output-format json \
  "/goal all tests in tests/ pass and lint is clean" > /tmp/goal-run.json
```

### ci-headless — Codex CLI

```bash
codex exec \
  --profile goal-ci \
  -c features.goals=true \
  -a on-request \
  -s workspace-write \
  --json \
  -o last.txt \
  "/goal Migrate API v1 to v2 until all contract tests pass"
```

Companion `~/.codex/config.toml`:

```toml
[profiles.goal-ci]
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

### long-dev — Claude Code

```bash
# Start
claude --name "refactor-auth-module" \
  "/goal every auth handler compiles, type checks, and tests pass"

# Resume after break
claude --resume "refactor-auth-module"
```

CLAUDE.md should declare: test commands, type-check command, danger zones.

### long-dev — Codex CLI

```bash
# Start
codex --profile goal-dev "/goal complete the auth migration"

# Resume
codex resume --last
```

### parallel-experiment

Open two terminals (or git worktrees) and run independent `/goal` sessions:

- Session A: `claude --name "approach-a" "/goal approach-a satisfies criteria X"`
- Session B: `claude --name "approach-b" "/goal approach-b satisfies criteria X"`

Compare via `/resume` session picker. For Codex use `codex resume --last` per worktree.

### safe-bounded — Codex CLI profile

```toml
[profiles.goal-safe]
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[profiles.goal-safe.sandbox_workspace_write]
writable_roots = ["./src", "./tests"]
network_access = false
```

Launch:

```bash
codex --profile goal-safe "/goal <objective>"
```

### safe-bounded — Claude Code

`~/.claude/settings.json` permission rules:

```json
{
  "permissions": {
    "allow": ["Bash(npm test)", "Bash(npm run lint)", "Read", "Edit", "Write"],
    "deny": ["Bash(rm -rf *)", "Bash(git push *)", "Bash(curl *)"],
    "ask": ["Bash(*)"]
  }
}
```

## AUTORUN Chain Template

```yaml
recipe: goal
mode: AUTORUN_FULL
state:
  PLATFORM: <claude-code | codex | both>
  USE_CASE: <ci-headless | long-dev | parallel-experiment | safe-bounded>

steps:
  - phase: PLATFORM_DETECT
    execution: inline
    confidence_threshold: 0.7
    ask_on_low_confidence: true

  - phase: USE_CASE_CLASSIFY
    execution: inline
    default: safe-bounded
    ask_on_low_confidence: true

  - phase: AUDIT
    agent: hone
    inputs: [PLATFORM, USE_CASE, repo_path]
    expected_output: before_after_diff

  - phase: HOOKS
    agent: latch
    inputs: [PLATFORM, USE_CASE, audit_findings]
    expected_output: hook_snippets
    skip_when: minimal_flag OR use_case == parallel-experiment

  - phase: CONTEXT_DOCS
    agent: scribe
    inputs: [PLATFORM, USE_CASE, audit_findings]
    expected_output: context_md_additions
    skip_when: context_md_already_sufficient

  - phase: DELIVER
    execution: inline
    output_format: see below
```

## Output Format

```markdown
## Nexus Execution Report

**Task**: `/goal` setup
**Platform**: <claude-code | codex | both>
**Use case**: <ci-headless | long-dev | parallel-experiment | safe-bounded>
**Chain**: Hone → Latch → Scribe?
**Mode**: AUTORUN_FULL

### Audit (Hone)
<Before/After diff of settings.json or config.toml, plus CLAUDE.md / AGENTS.md gaps>

### Hooks (Latch)
<Stop / PostToolUse / PreToolUse snippets to install, with file path and rationale>

### Context docs (Scribe, if applicable)
<CLAUDE.md or AGENTS.md additions in fenced markdown blocks>

### Launch command
```bash
<exact command to run>
```

### Verification checklist
- [ ] Hooks installed and validated with `claude --debug` / `codex /hooks`
- [ ] Permission rules / sandbox settings applied
- [ ] CLAUDE.md / AGENTS.md updated with completion criteria vocabulary
- [ ] Launch command dry-run with a safe dummy goal completed successfully
- [ ] Notification path tested (desktop / Slack / webhook)

### Summary
<1-3 sentence summary, recommended next action>
```

## Failure Modes

| Failure | Response |
|---|---|
| Platform unknown after detection + ask | Stop with install instructions; do not guess |
| `/goal` version too old (Claude Code < v2.1.139) | Emit upgrade instruction; do not produce launch command |
| Codex CLI lacks `[features] goals = true` | Include the toggle step in the audit diff; warn it is experimental |
| Existing hooks conflict with proposed hooks | Surface conflicts in Latch output; ask user to resolve before applying |
| Permission rules would deny the test command | Flag in audit; recommend explicit `allow` entry before launch |
| `apply_patch` / MCP hook gap (Codex known issue) | Note in hooks output; recommend completion verification on shell tool path only |

## Cost and Latency Profile

- Spawns: 1-3 agents (Hone, Latch optional, Scribe optional)
- Typical wall time: 2-4 minutes
- Token cost: low — read-only audit and template generation
- Confirmation gates: at most one (use-case classification when ambiguous)

This is a **lightweight Recipe**. Far below Apex. Suitable for `AUTORUN_FULL` in nearly all cases.
