# Skill Quarantine Hook Recipe

Purpose: load this when designing a hook that intercepts skill / plugin / MCP-server loading and runs a pre-flight audit before Claude is allowed to invoke them. Complements `security-guard-hook.md`, which guards tool calls; this recipe guards the skill / plugin / MCP discovery surface.

Authoritative trust-boundary policy: `_common/SECURITY.md`. Audit agent: `chain`.

## When to use

- A new third-party SKILL.md was added to `~/.claude/skills/` or a project's `.claude/skills/`.
- A plugin marketplace install (`/install`, `npm install --global @anthropic-ai/claude-code-plugin-*`) is about to run.
- An MCP server is being registered in `mcp.json` for the first time, or a previously-registered MCP server's tool descriptions changed between sessions.
- A `git pull` brought new skill files into the repo and they have not been audited.

## When NOT to use

- Runtime tool-call guards: use `security-guard-hook.md` (the existing PreToolUse security guard).
- Notification / observability: use `notification-hook.md`.
- Session-start context loading: use `sessionstart-hook.md`.

## Threat Model

| Attack | Defense in this hook |
|--------|----------------------|
| **SkillJect** (SKILL.md with 3 lines that exfiltrates SSH keys) | Reject load if SKILL.md content matches `chain` `P0` patterns |
| **Unicode Tag hidden instructions** | Reject any file containing `U+E0000`–`U+E007F` |
| **Frontmatter drift** (custom keys like `tools:`, `capabilities:`) | Reject any frontmatter key outside `name`/`description` |
| **MCP tool description rug-pull** | Compare current tool description sha256 against pinned manifest; block on mismatch |
| **Silent skill update** | Compare current file sha256 against `.chain-manifest.json`; block on mismatch |
| **Marketplace plugin hijack** | Require `chain intake` approval before allowing a plugin marketplace install |

## Hook Event Selection

| Event | Use for | Notes |
|-------|---------|-------|
| `SessionStart` | Initial repo-wide audit, build the skill manifest cache, fail-fast on hash drift | runs once per session; cheap if cached |
| `PreToolUse` (matcher: `Bash` with `npm install` / `pip install` / plugin marketplace patterns) | Block install-time supply-chain hooks | gates the install command itself |
| `PreToolUse` (matcher: `Skill`) | Block load of unaudited skills at invocation | per-skill-load latency |
| `PostToolUse` (matcher: `Write|Edit`, paths under `**/SKILL.md` or `.claude/skills/**`) | Trigger re-audit after a skill is modified | post-write asynchronous re-check |
| `UserPromptSubmit` | Detect `/install`-style commands before they reach a tool call | early intercept |

Recommended baseline: combine **SessionStart** (cache-warming + drift detection) and **PreToolUse** with the `Skill` matcher (per-invocation enforcement).

## Recipe A: SessionStart drift detection

```bash
# ~/.claude/hooks/skill-drift-check.sh
#!/usr/bin/env bash
set -euo pipefail

skills_root="${HOME}/.claude/skills"
project_skills="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/skills"
manifest_cache="${HOME}/.cache/claude/skill-manifests.tsv"
mkdir -p "$(dirname "$manifest_cache")"

# Portable SHA-256 hash (BSD/GNU compatible)
sha256_hash() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$@"
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 "$@"
  else echo "[ERROR] sha256sum/shasum not found" >&2; return 1; fi
}

drift_count=0
unaudited_count=0

for root in "$skills_root" "$project_skills"; do
  [[ -d "$root" ]] || continue
  # Portable alternative to find -printf '%h\0' (GNU only)
  while IFS= read -r skill_dir; do
    name=$(basename "$skill_dir")
    manifest="${skill_dir}/.chain-manifest.json"
    if [[ ! -f "$manifest" ]]; then
      echo "[skill-drift] UNAUDITED: $name" >&2
      ((unaudited_count++))
      continue
    fi
    # compute current sha of SKILL.md and compare with manifest
    cur=$(sha256_hash "${skill_dir}/SKILL.md" | cut -d' ' -f1)
    pinned=$(jq -r '.files["SKILL.md"]' "$manifest" | sed 's|^sha256:||')
    if [[ "$cur" != "$pinned" ]]; then
      echo "[skill-drift] HASH_MISMATCH: $name (expected $pinned, got $cur)" >&2
      ((drift_count++))
    fi
  done < <(find "$root" -maxdepth 2 -name SKILL.md -type f | while IFS= read -r f; do dirname "$f"; done | sort -u)
done

if [[ $drift_count -gt 0 ]]; then
  cat <<EOF
[skill-drift] $drift_count skill(s) drifted from pinned manifest.
Action required:
  1. Inspect the diff for each drifted skill.
  2. Run \`/chain audit <skill>\` to re-audit before continuing.
  3. Do NOT proceed with operations that invoke drifted skills.
EOF
  exit 2  # SessionStart exit 2 blocks startup
fi

if [[ $unaudited_count -gt 0 ]]; then
  echo "[skill-drift] WARN: $unaudited_count unaudited skill(s). Run \`/chain intake\`." >&2
  # exit 0 (warn only) — do not block, but surface
fi

exit 0
```

`settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "~/.claude/hooks/skill-drift-check.sh"
      }
    ]
  }
}
```

## Recipe B: PreToolUse plugin-install gate

Block plugin marketplace installs unless an explicit acknowledgment env var is set.

```bash
# ~/.claude/hooks/plugin-install-gate.sh
#!/usr/bin/env bash
set -euo pipefail
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command // ""')

# Match plugin-marketplace install patterns
if echo "$cmd" | grep -qE 'claudemarketplaces\.com|@anthropic-ai/claude-code-plugin|claude plugin (install|add)'; then
  if [[ "${CLAUDE_PLUGIN_INSTALL_ACK:-}" != "1" ]]; then
    cat <<EOF
{"permissionDecision":"deny","permissionDecisionReason":"Plugin install requires audit. Run \`/chain intake <source>\` first, then re-run with CLAUDE_PLUGIN_INSTALL_ACK=1 in your environment for this session."}
EOF
    exit 0
  fi
fi

# Otherwise allow
echo '{}'
```

`settings.json` matcher: `Bash` (per-command via PreToolUse with stdin JSON contract).

## Recipe C: MCP tool description re-verification

Run at SessionStart immediately after Recipe A.

```bash
# ~/.claude/hooks/mcp-pinning-check.sh
#!/usr/bin/env bash
set -euo pipefail

mcp_dir="${HOME}/.claude/mcp"
pin_file="${HOME}/.cache/claude/mcp-tool-pins.tsv"
mkdir -p "$(dirname "$pin_file")"

# Portable SHA-256 hash (BSD/GNU compatible)
sha256_hash() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$@"
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 "$@"
  else echo "[ERROR] sha256sum/shasum not found" >&2; return 1; fi
}

mismatch=0
for tool_json in "$mcp_dir"/*/tools.json; do
  [[ -f "$tool_json" ]] || continue
  server=$(basename "$(dirname "$tool_json")")
  cur=$(sha256_hash "$tool_json" | cut -d' ' -f1)
  # Portable tab-prefixed grep: perl instead of grep -P (unavailable on macOS BSD grep)
  pinned=$(perl -ne "print (split /\t/, \$_)[1] if /^\Q${server}\E\t/" "$pin_file" 2>/dev/null || true)
  if [[ -z "$pinned" ]]; then
    echo "[mcp-pinning] PINNING $server: $cur" >&2
    printf '%s\t%s\n' "$server" "$cur" >> "$pin_file"
  elif [[ "$cur" != "$pinned" ]]; then
    echo "[mcp-pinning] MISMATCH: $server (expected $pinned, got $cur) — RUG_PULL_SUSPECTED" >&2
    mismatch=$((mismatch + 1))
  fi
done

[[ $mismatch -eq 0 ]] || exit 2
exit 0
```

`settings.json`: combine with Recipe A under `SessionStart`.

## Allowlist Format

When a maintainer explicitly approves a skill that fails one of the static patterns (e.g. a configurator skill that *must* mutate `settings.json`), record the approval in a per-host allowlist file at `~/.claude/skill-allowlist.json`:

```json
{
  "skills": {
    "configurator": {
      "approved_at": "2026-05-12T00:00:00Z",
      "approved_by": "<user>",
      "exemptions": ["settings_mutation"],
      "manifest_sha256": "..."
    }
  }
}
```

The hook reads this file and exempts the listed skills from the matching checks. Any change to `~/.claude/skill-allowlist.json` itself should be tracked via git and reviewed.

## False-Positive Mitigation

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| All skills flagged as `UNAUDITED` after `git pull` | manifests not yet generated | run `chain intake` per skill, commit manifests |
| `HASH_MISMATCH` on every session start | line-ending drift between OS (CRLF vs LF) | normalise via `.gitattributes` `text eol=lf`; recompute manifest |
| `RUG_PULL_SUSPECTED` after MCP server upgrade | MCP server legitimately updated tool description | confirm with maintainer, re-pin via deleting the offending row in `mcp-tool-pins.tsv` |
| SessionStart blocked when offline | hook tries to verify against remote registry | implement local-only verification path |

## Hand-off to Chain

When the hook detects an unaudited or drifted state, it should surface to the user and recommend the `chain` recipe to run next. Do not attempt cleanup inside the hook itself.

```bash
echo "Next: /chain intake <skill>   (or /chain audit <skill> for drift)" >&2
```

## Hook Timeouts and Failure Modes

- Drift check: ≤ 5s typical for ≤ 100 skills; cache the manifest read.
- MCP pinning: ≤ 2s typical.
- Use `async: false` for the SessionStart hooks so that startup is blocked on a `P0` finding.
- Use `async: true` for PostToolUse re-audit triggers (informational, non-blocking).

## See Also

- `reference/security-guard-hook.md` — runtime tool-call guard (different scope; `Bash`, `Write`, `Edit` of secrets).
- `reference/sessionstart-hook.md` — general SessionStart patterns; this skill-quarantine hook follows the same harness.
- `_common/SECURITY.md` — authoritative trust-boundary spec.
- `chain/SKILL.md` — the audit agent invoked by `/chain intake`, `/chain audit`, `/chain mcp`, `/chain scan`, `/chain recover`.
