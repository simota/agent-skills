# SessionStart Hook

Reference for Latch's `sessionstart` recipe. Configure the SessionStart event for context preloading, env validation, and per-project warm-up.

---

## 1. SessionStart Event

Fires when:
- Claude Code session begins
- After `/clear` (context wiped)
- After `/compact` (context summarized)

Input schema:
```json
{
  "session_id": "uuid",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/working/dir",
  "hook_event_name": "SessionStart",
  "trigger": "startup" | "clear" | "compact"
}
```

### Output behavior
**stdout** (up to ~10K tokens recommended) is injected into Claude's next-turn context as a system-style message. Use to inject:
- Recent PR list
- Branch + CI status
- Project-specific instructions
- env validation results

---

## 2. Common Use Cases

### Inject recent PR list
```bash
#!/bin/bash
# ~/.claude/scripts/sessionstart-prs.sh
PROJECT=$(basename "$(pwd)")
echo "## Recent PRs (${PROJECT})"
gh pr list --limit 10 --json number,title,state,author \
  --template '{{range .}}- #{{.number}} [{{.state}}] {{.title}} (@{{.author.login}}){{"\n"}}{{end}}' 2>/dev/null \
  || echo "(gh not available)"
```

### Branch + CI status
```bash
echo "## Git Status"
echo "Branch: $(git branch --show-current 2>/dev/null)"
echo "Uncommitted: $(git status --porcelain 2>/dev/null | wc -l | tr -d ' ') files"
echo "Last commit: $(git log -1 --format='%h %s (%cr)' 2>/dev/null)"

echo "## CI Status"
gh run list --limit 3 --json status,conclusion,name \
  --template '{{range .}}- {{.name}}: {{.status}}/{{.conclusion}}{{"\n"}}{{end}}' 2>/dev/null
```

### CLAUDE.md auto-summary (cached)
```bash
# Portable SHA-256 hash (BSD/GNU compatible). See _common/PORTABILITY.md.
_sha256() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; fi; }
CACHE=~/.cache/claude/$(pwd | _sha256 | cut -c1-8)-claude-md-summary.txt

if [ ! -f "$CACHE" ] || [ "$(find CLAUDE.md -newer "$CACHE" 2>/dev/null)" ]; then
  # Refresh cache (run separately by cron, or skip if too slow)
  head -50 CLAUDE.md > "$CACHE"
fi

echo "## Project Brief"
cat "$CACHE" 2>/dev/null
```

### env validation gate
```bash
REQUIRED_NODE="20"
ACTUAL_NODE=$(node -v 2>/dev/null | sed 's/v//' | cut -d. -f1)

if [ "$ACTUAL_NODE" != "$REQUIRED_NODE" ]; then
  echo "BLOCK: Node $REQUIRED_NODE required, found $ACTUAL_NODE" >&2
  exit 2  # blocks session start
fi
```

---

## 3. Trigger Filtering

Use the `trigger` field to differentiate:
```bash
TRIGGER=$(echo "$INPUT" | jq -r .trigger)

case "$TRIGGER" in
  startup)
    # Full initial context (PRs, CI, project brief)
    ./full-context.sh
    ;;
  clear)
    # Restore minimal context only (just project brief)
    ./minimal-context.sh
    ;;
  compact)
    # No re-injection needed (compact already preserved key info)
    exit 0
    ;;
esac
```

---

## 4. Performance Considerations

SessionStart hooks block the session from starting until they exit:
- **Target: < 500ms** total
- Heavy work (LLM summarization, large API calls) → run via cron, hook reads cache
- Network calls (gh, curl) → set short timeout (`--timeout 3`)
- Use `async: false` (default) to ensure stdout is captured

### Cache pattern for slow operations
```bash
CACHE=~/.cache/claude/${PROJECT}-pr-list.txt
MAX_AGE=600  # 10 minutes

if [ ! -f "$CACHE" ] || [ $(($(date +%s) - $(stat -f %m "$CACHE" 2>/dev/null || stat -c %Y "$CACHE"))) -gt $MAX_AGE ]; then
  # Refresh cache asynchronously, return stale meanwhile
  (gh pr list --limit 10 > "$CACHE.new" && mv "$CACHE.new" "$CACHE") &
fi

cat "$CACHE" 2>/dev/null || echo "(cache empty, refreshing)"
```

---

## 5. Configuration

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/scripts/sessionstart-context.sh",
            "timeout": 3000
          }
        ]
      }
    ]
  }
}
```

### Per-project vs global
- Global (`~/.claude/settings.json`): always-on universal context
- Per-project (`.claude/settings.json`): project-specific brief
- Cascade: project hooks add to global, not replace

---

## 6. Composability Pattern

Multiple scripts, one entrypoint:
```bash
#!/bin/bash
# ~/.claude/scripts/sessionstart-context.sh
echo "## Session Context"
echo ""
~/.claude/scripts/_inject-prs.sh
echo ""
~/.claude/scripts/_inject-git.sh
echo ""
~/.claude/scripts/_inject-ci.sh
echo ""
[ -f .claude/sessionstart.sh ] && bash .claude/sessionstart.sh
```

Each `_inject-*.sh` is independently maintainable.

---

## 7. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Hook takes 5+ seconds → session feels slow | Cache slow operations; target <500ms |
| Output exceeds 10K tokens → context wasted | Truncate; head -N or wc-bounded |
| Sensitive data leaked into context (env vars) | Filter explicitly; never `env` dump |
| Running on every `/clear` is unwanted | Trigger-filter for `startup` only |
| Network call hangs | `command -v timeout >/dev/null 2>&1 && timeout 3 gh pr list ... \|\| gh pr list ...` (portable: `timeout` is GNU only; use `gtimeout` or the `run_with_timeout` helper from `_common/PORTABILITY.md` on macOS) |
| jq missing | Use sed/awk fallback or document install |
| Output goes to stderr → not captured | Use stdout for context, stderr only for errors |
| Block exits 2 always → session unusable | Validate before deploying; test exit codes |

---

## 8. Decision Walkthrough Template

```
Triggers to handle:
  □ startup (full context)
  □ clear (minimal restore)
  □ compact (no-op)

Context sources:
  □ Recent PRs (gh)
  □ Git branch + status
  □ CI runs
  □ CLAUDE.md summary
  □ Project-specific (.claude/sessionstart.sh)

Caching strategy:
  □ Per-project cache in ~/.cache/claude/
  □ Cron refresh every N minutes
  □ Cache hit: instant; miss: refresh + return stale

Validation gates:
  □ Node version
  □ Required env vars
  □ Required CLI tools (gh, jq)
  □ Block (exit 2) on failure

Performance budget:
  Total: ___ ms (target <500)
  Per source: ___ ms

Output size cap: ____ tokens (target <10K)
```

---

## 9. References
- Claude Code hooks documentation
- `gh` CLI reference
- bash caching idioms
