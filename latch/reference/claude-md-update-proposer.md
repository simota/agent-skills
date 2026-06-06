# Stop Hook — CLAUDE.md Update Proposer Recipe

Pattern for a **Stop hook** that runs at the end of each Claude Code session, diffs the session's accumulated learnings against the project's `CLAUDE.md`, and surfaces a structured update proposal. The hook is **non-blocking** by design — it never auto-edits `CLAUDE.md`, only proposes.

[Source: claude.com — *How Claude Code works in large codebases* (2026)](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start)

---

## 1. Why a Stop Hook (not a slash command)

A slash command is opt-in; it only runs when the user remembers. The Stop event fires deterministically at session end, which is precisely when the freshest information about "what we just learned" is still in context. The agent has just produced output, debugged something, or made a decision — that is the only moment when the gap between `CLAUDE.md` and reality is most visible.

A blocking variant (`exit 2`) would be hostile — sessions must always be terminable. Use a **non-blocking advisory** that prints a proposal to stderr and exits 0.

## 2. Event Selection

| Choice | Rationale |
|--------|-----------|
| Event: `Stop` | Fires before the main agent stops; final-state proposal is most relevant here. |
| Matcher: `*` or omit | The proposal should run on every session — drift is universal. |
| Type: `command` (or `prompt` for richer reasoning) | Command for fast no-cost runs; prompt for sessions where the agent should compose the proposal itself. |
| Timeout: 10s (command) / 30s (prompt) | Stop hooks must not hang shutdown. |
| `async: true` | Recommended — never block session termination on advisory output. |
| `exit 0` always | This is advisory, not enforcement. Never `exit 2`. |

## 3. Command Hook Sketch

```bash
#!/usr/bin/env bash
# Stop hook: propose CLAUDE.md updates from the just-finished session.
# Non-blocking; writes proposal to stderr and exits 0.

set -uo pipefail

CLAUDE_MD="${CLAUDE_PROJECT_DIR:-.}/CLAUDE.md"
PROPOSAL_DIR="${CLAUDE_PROJECT_DIR:-.}/.claude/proposals"
mkdir -p "$PROPOSAL_DIR"

# Read Stop event JSON from stdin
input=$(cat)
session_id=$(printf '%s' "$input" | jq -r '.session_id // "unknown"')
transcript=$(printf '%s' "$input" | jq -r '.transcript_path // ""')

# Skip if no transcript (early-exit cases, e.g. ctrl-C)
[ -z "$transcript" ] && exit 0

# Lightweight heuristic: detect candidate "rules we should have known"
# - Repeated apologies ("I should have")
# - Repeated tool failures of the same shape
# - New file types or build commands encountered for the first time
candidates=$(grep -E '(should have|forgot to|now I see that|the convention here is)' "$transcript" 2>/dev/null | head -20)

[ -z "$candidates" ] && exit 0

ts=$(date -u +%Y%m%dT%H%M%SZ)
out="$PROPOSAL_DIR/claude-md-proposal-$ts-$session_id.md"

{
  echo "# CLAUDE.md update proposal — session $session_id"
  echo
  echo "## Candidates extracted from this session"
  echo
  printf '%s\n' "$candidates" | sed 's/^/- /'
  echo
  echo "## Recommended action"
  echo "- Review each candidate."
  echo "- Add to \`$CLAUDE_MD\` only those that are project-durable (not session-specific)."
  echo "- For rule-shaped items that can run automatically, consider a hook instead of a CLAUDE.md line."
} > "$out"

# Surface to stderr so the user sees it on shutdown
echo "[CLAUDE.md proposer] Drafted update proposal: $out" >&2
exit 0
```

## 4. Prompt Hook Variant (richer)

Use a `prompt` hook when the proposal benefits from synthesis rather than pattern matching:

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Read the session transcript at $ARGUMENTS. Identify up to 3 durable, project-specific rules that would have prevented friction in this session and are NOT already in CLAUDE.md. Output each as: rule line, evidence quote, and whether it should be in CLAUDE.md or in a hook. If none, output 'no proposal'. Maximum 200 words.",
          "timeout": 30,
          "async": true
        }
      ]
    }
  ]
}
```

The prompt hook consumes token quota; reserve it for projects where session quality justifies the model invocation.

## 5. Filtering Rules (what NOT to propose)

The proposer must filter aggressively. Most session-level observations are not durable rules:

| Reject if | Why |
|-----------|-----|
| The rule restates a linter / formatter / type-checker rule | Anti-bloat — tooling already enforces it. |
| The rule mentions a specific file path or function name | Likely tactical, not project-wide. |
| The rule's "why" is "I made this mistake once" | Anecdote, not pattern. Wait for 3+ recurrences. |
| The rule duplicates content already in CLAUDE.md / AGENTS.md | Duplicate. |
| The rule expresses a preference rather than a constraint | Style drift, not project rule. |
| The rule is reversible by a hook | Author the hook instead (Latch). |

## 6. Pairing with Hone

Hone audits the *quality* of an existing CLAUDE.md (line count, density, instruction budget). This proposer feeds *new candidate content* into that audit cycle. Recommended chain when proposals accumulate:

`Stop hook produces proposal → user reviews → if 3+ accepted, route to Hone for re-audit of CLAUDE.md density and progressive-disclosure split.`

## 7. Anti-Patterns

- ❌ Auto-edit `CLAUDE.md` from the hook — gives Claude write authority over its own instructions, a self-modification footgun.
- ❌ Block session shutdown on `exit 2` — Stop hooks must never trap the user.
- ❌ Write proposals to the session's *visible* output channel (stdout JSON) — corrupts the protocol; write to stderr or a proposal file.
- ❌ Run on every prompt — accumulates noise; use `Stop` specifically so it summarizes once per session.

## 8. When This Recipe Is the Wrong Tool

- The team already runs a formal retrospective process — duplicate channel.
- The project has no `CLAUDE.md` yet — start there first (route to `Sigil` or `Hone`).
- The session is non-interactive / CI / `-p` flag — Stop hooks still fire, but the proposal has no human reviewer; output to a long-lived log or skip.

---

Pair this recipe with the SessionStart recipe (`reference/sessionstart-hook.md`) for a full open/close lifecycle: SessionStart loads context, Stop proposes durable updates from what was learned.
