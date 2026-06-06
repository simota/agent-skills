# Notification Hook

Reference for Latch's `notification` recipe. Configure the Notification event for desktop, Slack, Discord, and sound alerts on permission requests, idle warnings, and sub-agent completion.

---

## 1. Notification Event

Fires when Claude Code needs to surface something to the user:
- Tool permission request waiting for approval
- Long-running idle (default 60s+)
- SubagentStop (sub-agent finished)
- Custom messages from skills

Input schema (stdin JSON):
```json
{
  "session_id": "uuid",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/working/dir",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash"
}
```

---

## 2. Output Channel Patterns

### macOS desktop notification
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r .message | xargs -I {} osascript -e 'display notification \"{}\" with title \"Claude Code\" sound name \"Glass\"'",
            "async": true
          }
        ]
      }
    ]
  }
}
```

### terminal-notifier (cleaner UX, requires `brew install terminal-notifier`)
```json
{
  "hooks": [{
    "type": "command",
    "command": "jq -r .message | xargs -I {} terminal-notifier -title 'Claude' -message {} -sound Tink -group claude-code"
  }]
}
```

### Slack incoming webhook
```bash
#!/bin/bash
# ~/.claude/scripts/notify-slack.sh
PAYLOAD=$(cat)
MESSAGE=$(echo "$PAYLOAD" | jq -r .message)
curl -sS -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d "{\"text\":\"🤖 Claude: ${MESSAGE}\"}" > /dev/null
```

```json
{
  "hooks": [{
    "type": "command",
    "command": "~/.claude/scripts/notify-slack.sh",
    "async": true
  }]
}
```

### Discord webhook
Same pattern, different payload:
```bash
curl -sS -X POST "$DISCORD_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d "{\"content\":\"🤖 Claude: ${MESSAGE}\"}" > /dev/null
```

### Sound only (system bell)
```bash
afplay /System/Library/Sounds/Glass.aiff
```

---

## 3. Matcher Patterns

Use `matcher` to filter by message content (regex):

```json
{
  "Notification": [
    { "matcher": "permission", "hooks": [{ "command": "..." }] },
    { "matcher": "idle for [0-9]+s", "hooks": [{ "command": "..." }] },
    { "matcher": "Subagent completed", "hooks": [{ "command": "..." }] }
  ]
}
```

Common patterns:
- `permission` — permission requests
- `idle for` — idle warnings
- `Subagent completed` — subagent finished
- `error|failed` — error notifications
- `^$` — match all (no filter)

---

## 4. Deduplication Logic

Avoid notification spam (same message firing repeatedly):

```bash
#!/bin/bash
# ~/.claude/scripts/notify-dedupe.sh

# Portable SHA-256 hash (BSD/GNU compatible). See _common/PORTABILITY.md.
sha256_hash() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$@"
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 "$@"
  else echo "[ERROR] sha256sum/shasum not found" >&2; return 1; fi
}

PAYLOAD=$(cat)
MESSAGE=$(echo "$PAYLOAD" | jq -r .message)
HASH=$(echo "$MESSAGE" | sha256_hash | cut -c1-8)

CACHE="${TMPDIR:-/tmp}/claude-notify-${HASH}"
NOW=$(date +%s)

if [ -f "$CACHE" ]; then
  LAST=$(cat "$CACHE")
  if [ $((NOW - LAST)) -lt 300 ]; then
    # Same message within 5 minutes, skip
    exit 0
  fi
fi

echo "$NOW" > "$CACHE"
terminal-notifier -title 'Claude' -message "$MESSAGE"
```

---

## 5. Time-Based Mute Rules

Quiet hours (22:00-07:00):
```bash
HOUR=$(date +%H)
if [ "$HOUR" -ge 22 ] || [ "$HOUR" -lt 7 ]; then
  # Silent: log only, no sound
  echo "$(date) $MESSAGE" >> ~/.claude/notify-quiet.log
  exit 0
fi
```

DND profile (skip during focus blocks):
```bash
if [ -f ~/.claude/dnd-active ]; then
  exit 0  # silent
fi
```

---

## 6. Per-Project Rules

```bash
PROJECT=$(basename "$(jq -r .cwd <<< "$PAYLOAD")")
case "$PROJECT" in
  "personal-blog") exit 0 ;;     # mute all notifications
  "production-api") FORCE_SOUND="Sosumi" ;;  # urgent sound
  *) FORCE_SOUND="Glass" ;;
esac
```

---

## 7. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Synchronous notifications block Claude | Always set `async: true` |
| Same message fires every 30s | Deduplication via hash + timestamp cache |
| Webhook URL committed to git | Use env var; `.env` gitignored; never inline |
| Slack webhook rate-limit (1 req/sec) | Throttle via lock file |
| Notification fires during deep work | Time-based mute + DND file |
| Forgetting to `chmod +x` script | `chmod +x ~/.claude/scripts/*.sh` |
| jq missing on some systems | Document install requirement |
| Notification fires for noisy events (every Bash) | Filter via `matcher` regex |

---

## 8. Decision Walkthrough Template

```
Channels needed:
  □ macOS desktop (osascript / terminal-notifier)
  □ Slack (#channel: ____)
  □ Discord (#channel: ____)
  □ Sound only

Filters:
  □ Permission requests only
  □ Idle warnings only
  □ Subagent completion
  □ All notifications

Deduplication: ✓ / ✗ (window: ____ min)
Time-based mute: ✓ / ✗ (hours: ____)
Per-project rules: ✓ / ✗

Async: ✓ (always recommended)

Setup:
  □ chmod +x scripts
  □ env vars for webhooks
  □ test with `echo '{"message":"test"}' | bash script.sh`
  □ session restart
```

---

## 9. References
- Claude Code hooks documentation
- terminal-notifier (macOS)
- Slack Incoming Webhooks
- Discord Webhooks API
