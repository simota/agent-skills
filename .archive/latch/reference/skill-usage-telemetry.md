# Skill Usage Telemetry Hook

A `PreToolUse` hook recipe that logs every skill invocation to a local append-only file, enabling popularity and under-trigger analysis across the ecosystem.

Source: Anthropic Engineering, "Lessons from Building Claude Code: How We Use Skills" (2026) — recommends `PreToolUse` hooks as the primary measurement instrument for skill telemetry.

---

## When to use

- You want data on which skills actually fire in real sessions, not just which are installed.
- Darwin / Prune / Gauge need usage signals to rank skills for evolution, sunset, or recalibration.
- You suspect popular skills exist outside the routing matrix (organic adoption per the Anthropic blog).
- You suspect installed skills never trigger (under-triggering — a candidate for sunset).

## What it does

The hook fires on every `Skill` tool invocation, captures the skill name and timestamp, and appends a JSONL line to `${CLAUDE_PLUGIN_DATA:-$HOME/.claude}/telemetry/skill-usage.jsonl`. The hook is non-blocking (exit 0 always) and runs `async: true` to keep latency off the critical path.

---

## Configuration

### `settings.json` entry

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Skill",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/skill-usage-log.sh",
            "async": true,
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Matcher rationale: `"Skill"` matches only the `Skill` invocation tool. Other tool calls (Read, Write, Bash, Agent) are not logged — telemetry stays scoped.

### Script `~/.claude/hooks/skill-usage-log.sh`

```bash
#!/usr/bin/env bash
set -uo pipefail

DATA_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.claude}/telemetry"
LOG_FILE="$DATA_DIR/skill-usage.jsonl"

mkdir -p "$DATA_DIR"

# Parse stdin once; tolerate missing fields.
INPUT="$(cat)"
SKILL_NAME="$(printf '%s' "$INPUT" | jq -r '.tool_input.skill // .tool_input.name // "unknown"' 2>/dev/null || echo unknown)"
SESSION_ID="$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo unknown)"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
CWD="$(printf '%s' "$INPUT" | jq -r '.cwd // empty' 2>/dev/null || true)"

printf '{"ts":"%s","skill":"%s","session":"%s","cwd":"%s"}\n' \
  "$TS" "$SKILL_NAME" "$SESSION_ID" "$CWD" >> "$LOG_FILE"

exit 0
```

Make it executable: `chmod +x ~/.claude/hooks/skill-usage-log.sh`.

### Notes

- **Append-only** matches the Anthropic blog's recommended persistence pattern. Never truncate; rotate by date if size grows.
- **`async: true`** prevents the hook from blocking the `Skill` tool. Telemetry must never gate execution.
- **`exit 0` always** — telemetry is monitoring, not enforcement. Fail-open per Latch Core Contract.
- **No sensitive fields logged**: skill name, session id, cwd only. Do not capture `args` (may contain user input).
- **`${CLAUDE_PLUGIN_DATA}`**: when running inside a plugin context, this env var points to the plugin's stable data dir. The fallback `$HOME/.claude` keeps personal-environment behavior identical.

---

## Querying the log

### Top-N most-used skills (last 30 days)

```bash
LOG="${CLAUDE_PLUGIN_DATA:-$HOME/.claude}/telemetry/skill-usage.jsonl"
CUTOFF="$(date -u -v-30d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)"

jq -r --arg cutoff "$CUTOFF" 'select(.ts >= $cutoff) | .skill' "$LOG" \
  | sort | uniq -c | sort -rn | head -20
```

### Under-triggered skills (installed but never used in 90 days)

```bash
LOG="${CLAUDE_PLUGIN_DATA:-$HOME/.claude}/telemetry/skill-usage.jsonl"
CUTOFF="$(date -u -v-90d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '90 days ago' +%Y-%m-%dT%H:%M:%SZ)"

# All installed skills (this repo).
ls ~/.claude/skills/ | grep -v '^_' > /tmp/installed.txt

# Skills that fired in the window.
jq -r --arg cutoff "$CUTOFF" 'select(.ts >= $cutoff) | .skill' "$LOG" \
  | sort -u > /tmp/used.txt

# Difference = under-triggered candidates for Prune review.
comm -23 /tmp/installed.txt /tmp/used.txt
```

### Per-session skill chain (for Lore pattern extraction)

```bash
jq -r 'select(.session=="SESSION_ID_HERE") | .skill' "$LOG"
```

---

## Downstream agent handoff

| Agent | Use the data for |
|-------|------------------|
| `Darwin` | Fitness scoring — high-usage skills are protected, low-usage skills enter sunset evaluation. |
| `Prune` | Candidate identification — pair under-triggered list with overlap detection (Jaccard) for merge/sunset proposals. |
| `Gauge` | CQ2 calibration — descriptions of under-triggered skills are candidates for trigger-word rewrites. |
| `Lore` | Cross-session pattern extraction — common skill chains become candidates for Nexus Recipes. |

---

## Privacy and rotation

- The log lives only on the local machine. Never sync `telemetry/` to a remote.
- Add to `.gitignore`: `**/telemetry/`.
- Rotate monthly: `mv skill-usage.jsonl skill-usage-$(date +%Y%m).jsonl`. Old archives can compress with `gzip` once cold.
- Skill names alone are not sensitive, but the combination `(session, cwd, time)` could fingerprint a workflow. Keep the log on encrypted-at-rest disk.

---

## Validation after configuration

1. Backup `settings.json` (Latch Core Contract): `cp ~/.claude/settings.json ~/.claude/settings.json.bak`
2. Validate JSON: `jq . ~/.claude/settings.json`
3. Restart the Claude Code session.
4. Invoke any skill (e.g., `/compass`), then check: `tail -1 ${CLAUDE_PLUGIN_DATA:-$HOME/.claude}/telemetry/skill-usage.jsonl`
5. Expected: a single JSONL line with `skill`, `ts`, `session`, `cwd`.

---

## Anti-patterns

- Do **not** log to stdout — the `PreToolUse` JSON protocol owns stdout. Use the file sink only.
- Do **not** block on missing `jq` — guard with `command -v jq` if portability matters; fall back to a `sed` extraction.
- Do **not** make the hook synchronous — the `Skill` tool path is hot; even 50 ms per call compounds across a session.
- Do **not** capture `tool_input` blindly — user-provided arguments may contain secrets or PII.

---

## Pairing

This recipe pairs with:

- `cull` skill — when telemetry surfaces an unknown skill firing (potential supply-chain malware), route to `cull` for IoC scan.
- `gauge audit CQ2` — descriptions of under-triggered skills are CQ2 fix candidates.
- `chain` skill — supply-chain audit before adopting community skills surfaced by the log.
