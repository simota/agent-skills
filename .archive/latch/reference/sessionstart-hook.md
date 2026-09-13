# SessionStart Hook

Reference for Latch's `sessionstart` recipe. Configure the SessionStart event for context preloading, env validation, and per-project warm-up.

---

## 1. SessionStart Event

Fires when:
- Claude Code session begins or resumes
- After `/clear` (context wiped)
- After `/compact` (context summarized)

Input example (`source` is `startup`, `resume`, `clear`, `compact`, or `fork`):

```json
{
  "session_id": "uuid",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/working/dir",
  "hook_event_name": "SessionStart",
  "source": "startup"
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
[ -f CLAUDE.md ] || exit 0
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/claude"
mkdir -p "$CACHE_DIR" || exit 1
CACHE="$CACHE_DIR/$(pwd | _sha256 | cut -c1-8)-claude-md-summary.txt"

if [ ! -f "$CACHE" ] || [ "$(find CLAUDE.md -newer "$CACHE" 2>/dev/null)" ]; then
  # Refresh cache (run separately by cron, or skip if too slow)
  head -50 CLAUDE.md > "$CACHE"
fi

echo "## Project Brief"
cat "$CACHE" 2>/dev/null
```

### Environment validation advisory
```bash
REQUIRED_NODE="20"
ACTUAL_NODE=$(node -v 2>/dev/null | sed 's/v//' | cut -d. -f1)

if [ "$ACTUAL_NODE" != "$REQUIRED_NODE" ]; then
  echo "WARNING: Node $REQUIRED_NODE required, found $ACTUAL_NODE" >&2
  exit 2  # SessionStart reports this to the user; it does not block the session
fi
```

---

## 3. Trigger Filtering

Read the hook JSON from stdin and dispatch on its `source` field:

```bash
SOURCE=$(jq -r .source) || exit 1

case "$SOURCE" in
  startup|resume|fork)
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

Synchronous SessionStart hooks delay startup until they finish; their errors cannot veto session creation:
- **Target: < 500ms** total
- Heavy work (LLM summarization, large API calls) → run via cron, hook reads cache
- Bound the hook with its `timeout` setting (seconds); use the `run_with_timeout` helper from `_common/PORTABILITY.md` for individual commands. `gh pr list` has no `--timeout` flag.
- Use `async: false` (default) to ensure stdout is captured

### Cache pattern for slow operations
```bash
_sha256() { if command -v sha256sum >/dev/null 2>&1; then sha256sum; elif command -v shasum >/dev/null 2>&1; then shasum -a 256; fi; }
PROJECT_KEY=$(pwd | _sha256 | cut -d ' ' -f1)
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/claude"
mkdir -p "$CACHE_DIR" || exit 1
CACHE="$CACHE_DIR/${PROJECT_KEY}-pr-list.txt"
MAX_AGE=600  # 10 minutes

if [ ! -f "$CACHE" ] || [ $(($(date +%s) - $(stat -c %Y "$CACHE" 2>/dev/null || stat -f %m "$CACHE"))) -gt $MAX_AGE ]; then
  # Refresh cache asynchronously, return stale meanwhile
  (
    CACHE_TMP=$(mktemp "$CACHE.tmp.XXXXXX") || exit 1
    trap 'rm -f "$CACHE_TMP"' EXIT
    gh pr list --limit 10 > "$CACHE_TMP" && mv "$CACHE_TMP" "$CACHE"
  ) >/dev/null 2>&1 &
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
            "timeout": 3
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
| Network call hangs | Use `run_with_timeout 3 gh pr list ...` with the helper from `_common/PORTABILITY.md`; a timeout returns cached data or a notice, never an unbounded retry. |
| jq missing | Use sed/awk fallback or document install |
| Output goes to stderr → not captured | Use stdout for context, stderr only for errors |
| Treating exit 2 as a startup gate | SessionStart cannot block creation; enforce a required environment in the launcher or an appropriate blocking event. |

---

## 8. Decision Walkthrough Template

```
Triggers to handle:
  □ startup / resume / fork (full context)
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
  □ Advisory on failure; enforce any required gate outside SessionStart

Performance budget:
  Total: ___ ms (target <500)
  Per source: ___ ms

Output size cap: ____ tokens (target <10K)
```

---

## 9. References
- [Claude Code hooks reference](https://code.claude.com/docs/en/hooks) — SessionStart input, exit-code behavior, and timeout units (verified 2026-09-13)
- `gh` CLI reference
- bash caching idioms
