# Security Guard Hook

Reference for Latch's `security` recipe. PreToolUse hooks for blocking dangerous operations, secret detection, sensitive file protection, and MCP tool ACL.

> Defense-in-depth alongside `_common/BOUNDARIES.md`. Hooks enforce at runtime; agent boundaries inform intent.

---

## 1. PreToolUse Decision Model

PreToolUse hook stdin:
```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash" | "Write" | "Edit" | "mcp__*",
  "tool_input": { ... },
  "session_id": "uuid",
  "cwd": "/path"
}
```

Output (stdout JSON):
```json
{
  "permissionDecision": "allow" | "deny" | "ask" | "defer",
  "reason": "human-readable rationale",
  "updatedInput": { ... }   // optional, only with "allow"
}
```

Or exit code 2 to immediately block (simpler for deny-only logic).

---

## 2. Dangerous Bash Patterns

```bash
#!/bin/bash
# ~/.claude/scripts/security-bash-guard.sh
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r .tool_name)

[ "$TOOL" != "Bash" ] && { echo '{"permissionDecision":"allow"}'; exit 0; }

CMD=$(echo "$INPUT" | jq -r .tool_input.command)

# Patterns to deny
DENY_PATTERNS=(
  'rm -rf /'
  'rm -rf ~'
  'rm -rf \*'
  'chmod -R 777'
  'mkfs\.'
  'dd if=.+of=/dev/'
  ':\(\)\{ :\|:& \};:'  # fork bomb
  'curl .+ \| (sudo )?bash'
  'wget .+ \| (sudo )?bash'
  '> /dev/sda'
)

for PATTERN in "${DENY_PATTERNS[@]}"; do
  if echo "$CMD" | grep -qE "$PATTERN"; then
    jq -n --arg reason "Blocked: matches $PATTERN" \
      '{permissionDecision:"deny",reason:$reason}'
    exit 0
  fi
done

# git push --force to main/master
if echo "$CMD" | grep -qE 'git push.+--force.+(main|master)\b' || \
   echo "$CMD" | grep -qE 'git push.+--force\b.*\b(main|master)\s*$'; then
  jq -n '{permissionDecision:"deny",reason:"Blocked: force-push to main/master"}'
  exit 0
fi

echo '{"permissionDecision":"allow"}'
```

---

## 3. Sensitive File Protection (Write/Edit)

```bash
#!/bin/bash
# ~/.claude/scripts/security-file-guard.sh
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r .tool_name)

case "$TOOL" in
  Write|Edit) ;;
  *) echo '{"permissionDecision":"allow"}'; exit 0 ;;
esac

PATH_VAL=$(echo "$INPUT" | jq -r .tool_input.file_path)

# Sensitive file patterns
SENSITIVE_PATTERNS=(
  '\.env$'
  '\.env\.'
  '/id_rsa$'
  '/id_ed25519$'
  '\.pem$'
  '\.p12$'
  '\.key$'
  '/secrets\.json$'
  '/credentials(\.json)?$'
  '/\.npmrc$'   # may contain auth tokens
  '/\.aws/credentials$'
  '/\.gcloud/credentials\.db$'
)

for PATTERN in "${SENSITIVE_PATTERNS[@]}"; do
  if echo "$PATH_VAL" | grep -qE "$PATTERN"; then
    jq -n --arg p "$PATH_VAL" \
      '{permissionDecision:"ask",reason:"Sensitive file: \($p) requires confirmation"}'
    exit 0
  fi
done

echo '{"permissionDecision":"allow"}'
```

For higher security: use `"deny"` instead of `"ask"`.

---

## 4. Secret Regex in Tool Input

Detect secrets being written/passed:
```bash
#!/bin/bash
# ~/.claude/scripts/security-secret-guard.sh
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r .tool_name)

case "$TOOL" in
  Write|Edit) CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string') ;;
  Bash) CONTENT=$(echo "$INPUT" | jq -r .tool_input.command) ;;
  *) echo '{"permissionDecision":"allow"}'; exit 0 ;;
esac

# Common secret patterns
SECRET_PATTERNS=(
  'AKIA[0-9A-Z]{16}'                               # AWS access key
  'aws_secret_access_key.*[A-Za-z0-9/+=]{40}'      # AWS secret
  'sk-[A-Za-z0-9]{40,}'                            # OpenAI / Stripe / generic
  'sk-ant-api[0-9]{2}-[A-Za-z0-9_-]{90,}'          # Anthropic API key
  'ghp_[A-Za-z0-9]{36}'                            # GitHub PAT
  'github_pat_[A-Za-z0-9_]{82}'                    # GitHub fine-grained PAT
  'xox[baprs]-[A-Za-z0-9-]{10,}'                   # Slack token
  'eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}'  # JWT
  '-----BEGIN [A-Z ]+PRIVATE KEY-----'             # PEM private key
)

for PATTERN in "${SECRET_PATTERNS[@]}"; do
  if echo "$CONTENT" | grep -qE "$PATTERN"; then
    jq -n --arg p "$(echo "$PATTERN" | head -c 30)..." \
      '{permissionDecision:"deny",reason:"Secret detected: \($p)"}'
    exit 0
  fi
done

echo '{"permissionDecision":"allow"}'
```

### Auto-redact (for logging hooks, not for blocking)
```bash
REDACTED=$(echo "$CONTENT" | sed -E 's/(sk-[A-Za-z0-9]{40,})/[REDACTED-OPENAI]/g')
jq -n --arg c "$REDACTED" '{permissionDecision:"allow",updatedInput:{content:$c}}'
```

---

## 5. MCP Tool ACL

```bash
#!/bin/bash
# ~/.claude/scripts/security-mcp-acl.sh
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r .tool_name)

# Only filter MCP tools
[[ "$TOOL" != mcp__* ]] && { echo '{"permissionDecision":"allow"}'; exit 0; }

# Read denylist from env (comma-separated)
DENYLIST="${LATCH_BLOCKED_MCP_TOOLS:-}"

IFS=',' read -ra DENIED <<< "$DENYLIST"
for D in "${DENIED[@]}"; do
  if [ "$TOOL" = "$D" ] || [[ "$TOOL" == "$D"* ]]; then
    jq -n --arg t "$TOOL" \
      '{permissionDecision:"deny",reason:"MCP tool \($t) is on denylist"}'
    exit 0
  fi
done

echo '{"permissionDecision":"allow"}'
```

Usage:
```bash
export LATCH_BLOCKED_MCP_TOOLS="mcp__shell__exec,mcp__notion__delete_page"
```

---

## 6. CI Auto-Deny Escalation

In CI environments, "ask" cannot be answered. Escalate all asks to deny:
```bash
if [ "$CI" = "true" ] || [ -n "$GITHUB_ACTIONS" ]; then
  # In CI, asks become denies
  ORIGINAL_DECISION=$(echo "$DECISION_JSON" | jq -r .permissionDecision)
  if [ "$ORIGINAL_DECISION" = "ask" ]; then
    echo "$DECISION_JSON" | jq '.permissionDecision = "deny" | .reason = "Auto-denied (ask in CI): \(.reason)"'
    exit 0
  fi
fi
```

---

## 7. Compositions

Single hook composing all guards:
```bash
#!/bin/bash
# ~/.claude/scripts/security-all.sh
INPUT=$(cat)

# Run guards in order; first deny wins
for GUARD in bash file secret mcp; do
  RESULT=$(echo "$INPUT" | ~/.claude/scripts/security-${GUARD}-guard.sh)
  DECISION=$(echo "$RESULT" | jq -r .permissionDecision)
  if [ "$DECISION" = "deny" ] || [ "$DECISION" = "ask" ]; then
    echo "$RESULT"
    exit 0
  fi
done

echo '{"permissionDecision":"allow"}'
```

Settings.json:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          { "type": "command", "command": "~/.claude/scripts/security-all.sh", "timeout": 2000 }
        ]
      }
    ]
  }
}
```

---

## 8. Audit Logging (PostToolUse, complementary)

Log all tool uses for security audit:
```bash
#!/bin/bash
# ~/.claude/scripts/security-audit-log.sh
INPUT=$(cat)
LOG=~/.claude/audit/$(date +%Y-%m).jsonl
mkdir -p "$(dirname "$LOG")"
echo "$INPUT" | jq -c '. + {logged_at: now}' >> "$LOG"
exit 0
```

```json
{
  "PostToolUse": [
    {
      "matcher": "",
      "hooks": [{ "type": "command", "command": "~/.claude/scripts/security-audit-log.sh", "async": true }]
    }
  ]
}
```

---

## 9. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Regex too broad → blocks legitimate ops | Test against false-positive corpus |
| Regex too narrow → misses variants | Test with obfuscated examples |
| Hook crashes → tool silently allowed | Always exit 0 with explicit decision; use `set -e` carefully |
| Slow regex → tool feels laggy | Keep <100ms per check |
| Secret patterns hardcoded → outdated | Update list periodically; consider gitleaks rule sync |
| jq missing → hook fails | Document install requirement |
| Asking for confirmation in CI → hangs | Detect `$CI`; auto-deny |
| Allowing `git push --force` to PR branches | Allowlist non-main branches |
| Blocking own .env edit when bootstrapping | Provide `BYPASS=1` env var with explicit user opt-in |
| Logging secrets to audit log | Redact secrets before logging |

---

## 10. Decision Walkthrough Template

```
Threat surface:
  □ Dangerous Bash (rm -rf /, fork bomb, curl|bash)
  □ Sensitive file write (.env, .pem, secrets)
  □ Secret leakage in input (API keys, JWTs, PEM)
  □ MCP tool ACL (denylist via env)

Decision behavior per match:
  □ deny (block + log)
  □ ask (interactive confirm)
  □ allow + redact (updatedInput)

CI behavior:
  □ Escalate ask → deny
  □ Allow opt-out via BYPASS=1 env

Performance budget: <100ms per hook

Audit:
  □ PostToolUse audit log (JSONL with redaction)
  □ Log path: ~/.claude/audit/YYYY-MM.jsonl

Setup:
  □ chmod +x scripts
  □ Test with malicious input examples
  □ Document BYPASS env var usage
  □ Session restart
```

---

## 11. References
- Claude Code hooks documentation
- gitleaks (secret pattern reference)
- OWASP Cheat Sheet: Logging
- AWS / GitHub / OpenAI / Slack secret format docs
- Knight Capital 2012 incident (flag reuse) — referenced by Sweep / Latch
