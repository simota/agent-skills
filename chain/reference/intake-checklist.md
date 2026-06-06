# Third-Party Skill Intake Checklist

Purpose: load this when running `chain intake` for any new third-party SKILL.md, plugin, or MCP server. Provides the per-item procedure, the executable check command, and the failure remediation guidance.

The authoritative checklist policy lives in `_common/SECURITY.md`. This file is the implementation runbook.

## Contents

1. Pre-flight
2. Frontmatter check
3. Unicode and bidi scan
4. Bundled artifact scan
5. Settings / config mutation scan
6. Network and credential scan
7. Manifest generation
8. First-use sandboxed verification
9. Verdict matrix
10. Remediation diff format

## 1. Pre-flight

| Check | Command | Pass when |
|-------|---------|-----------|
| Skill directory present | `test -d <skill>` | exists |
| SKILL.md present | `test -f <skill>/SKILL.md` | exists |
| Source classification | maintainer review | matches one of: anthropic / first-party / third-party-known / third-party-aggregator / pipe-installed |

If pre-flight fails, abort intake and return `REJECTED:PRE_FLIGHT` with the failing item.

## 2. Frontmatter Check

Read the YAML frontmatter (between `---` markers at the top of SKILL.md).

```bash
awk '/^---$/{c++; next} c==1' <skill>/SKILL.md > /tmp/frontmatter.yml
```

Required exactly:

- `name`: kebab-case string
- `description`: single line, ≥ 30 chars, mentions purpose and out-of-scope

Forbidden (`REJECT` with `P1: frontmatter_custom_key`):

- `tools:`, `capabilities:`, `required_tools:`, `required_capabilities:`, `permissions:`, `trust:`, any key not in the official Anthropic Agent Skills spec.

Rationale: the official spec is `name` + `description`. Custom keys break forward-compatibility with Anthropic-side parsers and may be a smuggling vector. Capability declarations belong in the Markdown body (e.g. a "Tools used:" line near the top).

## 3. Unicode and Bidi Scan

See `reference/unicode-tag-scan.md` for the full codepoint policy.

Quick check (any non-zero exit = `REJECT`):

```bash
# Portable Unicode scan: perl instead of grep -P (BSD grep has no PCRE).
# Compatible with macOS (BSD) and Linux (GNU). See _common/PORTABILITY.md.

scan_unicode() {
  local pat="$1" label="$2"; shift 2
  find "$@" -type f | while IFS= read -r f; do
    LC_ALL=C perl -ne "print \"\$ARGV\n\" and last if /$pat/" "$f" 2>/dev/null || true
  done | sort -u | while IFS= read -r hit; do echo "${label}: ${hit}"; done
}

# Unicode Tag block U+E0000–U+E007F
scan_unicode '\xf3\xa0[\x80\x81][\x80-\xbf]' "TAG_FOUND" <skill>

# Bidi overrides U+202A–U+202E, U+2066–U+2069
scan_unicode '\xe2\x80[\xaa-\xae]|\xe2\x81[\xa6-\xa9]' "BIDI_FOUND" <skill>

# Zero-width chars in instruction positions
scan_unicode '\xe2\x80[\x8b-\x8d]|\xef\xbb\xbf' "ZWSP_FOUND" <skill>
```

Any positive hit → `REJECT` with `P0: invisible_chars` and quarantine.

## 4. Bundled Artifact Scan

See `reference/bundled-artifact-review.md` for the full pattern catalog.

Inventory: every file in the skill directory that is not `SKILL.md` itself.

```bash
find <skill> -type f \! -name SKILL.md
```

For each file, run the appropriate scanner:

| File type | Scanner |
|-----------|---------|
| `.sh`, `.bash` | grep for curl-pipe / eval / chmod+x / nc / `bash -i` patterns |
| `.py` | grep for `subprocess`, `os.system`, `eval`, `exec`, `__import__` with dynamic args, `pickle.loads`, `requests.get` to non-allowlisted hosts |
| `.js`, `.ts`, `.mjs` | grep for `child_process.exec`, `eval`, `Function(...)`, `fetch` to non-allowlisted hosts |
| `.md` | rerun Unicode scan; check for `[click here](javascript:...)` or data: URIs |
| binary | reject unless provenance attestation provided (SLSA L2+ or Sigstore) |
| `.json`, `.yml`, `.toml` | rerun Unicode scan; check for embedded shell commands in string fields |

A positive hit on any file → `REJECT` with the appropriate severity per the SKILL.md decision matrix.

## 5. Settings and Config Mutation Scan

Across every bundled script, look for writes to:

- `.claude/settings.json` / `.claude/settings.local.json`
- `~/.claude/settings.json`
- `CLAUDE.md`, `AGENTS.md`, `MEMORY.md`
- `.gitconfig`, `.npmrc`, `.pypirc`, `.cargo/config.toml`

Any write to these targets → `P0 REJECT` unless explicitly declared in the SKILL.md body and matches a recognised legitimate purpose (e.g. a configurator skill that explicitly documents settings mutation).

## 6. Network and Credential Scan

Outbound network targets:

```bash
# extract all URLs from bundled scripts
grep -rEho 'https?://[a-zA-Z0-9./_-]+' <skill> | sort -u
```

Compare against the skill's declared network allowlist (in SKILL.md body). Any undeclared host → `P1 REJECT` until the allowlist is updated or the call removed.

Credential paths to flag:

- `~/.ssh/` (id_*, authorized_keys, known_hosts)
- `~/.aws/credentials`, `~/.aws/config`
- `~/.config/gh/hosts.yml`, `~/.config/gh/config.yml`
- `~/.netrc`
- `~/.npmrc`
- `~/.pypirc`
- `~/.docker/config.json`
- `~/.kube/config`
- `~/.gitconfig` (for user.email / user.signingkey extraction)
- environment variables matching `*_TOKEN`, `*_KEY`, `*_SECRET`, `*_PASSWORD`, `AWS_*`, `GITHUB_TOKEN`, `NPM_TOKEN`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`

Any read of these without explicit declaration → `P0 REJECT`.

## 7. Manifest Generation

Once all checks pass, generate `.chain-manifest.json` at the skill root:

```bash
{
  cat <<EOF
{
  "skill": "<name>",
  "audited_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "audited_by": "chain",
  "intake_checklist_version": "1",
  "frontmatter_keys": ["name", "description"],
  "declared_capabilities": [...],
  "network_allowlist": [...],
  "files": {
EOF
  find <skill> -type f \! -name .chain-manifest.json | while read f; do
    rel="${f#<skill>/}"
    hash=$(sha256sum "$f" | cut -d' ' -f1)
    echo "    \"$rel\": \"sha256:$hash\","
  done | sed '$ s/,$//'
  echo "  }"
  echo "}"
} > <skill>/.chain-manifest.json
```

Commit the manifest alongside the skill.

## 8. First-Use Sandboxed Verification

Before allowing the skill to run in the host context, exercise it once inside a sandbox:

- Container: minimal image, no host filesystem mount, no network egress
- Synthetic task aligned with the skill's declared purpose
- Capture: tool calls observed, network calls observed, files read, files written
- Verify: every observation matches the declared capabilities and network allowlist

Discrepancy → `REJECT` with `P2: capability_mismatch` (or higher if the discrepancy is exfil-class).

## 9. Verdict Matrix

| Condition | Verdict |
|-----------|---------|
| All checklist items PASS + sandbox observation matches declaration | `APPROVED` |
| Any `P0` finding | `REJECTED + QUARANTINED` → escalate to `triage` |
| Any `P1` finding, no `P0` | `REJECTED` → return remediation diff to maintainer |
| Only `P2` findings, no `P0`/`P1` | `APPROVED_WITH_FLAG` (rare; requires explicit override and journaled rationale) |
| Inconclusive (sandbox crashed / hash missing) | `BLOCKED` → re-run after fix |

## 10. Remediation Diff Format

When returning `REJECTED`, attach a minimal diff:

```diff
# remediation for <skill>
# checklist failure: P1 frontmatter_custom_key

--- a/<skill>/SKILL.md
+++ b/<skill>/SKILL.md
@@ -1,5 +1,4 @@
 ---
 name: example-skill
-tools: [Read, Edit, Bash]
 description: "..."
 ---
```

```diff
# remediation for <skill>
# checklist failure: P0 curl_pipe_in_bundled

--- a/<skill>/reference/scripts/install.sh
+++ b/<skill>/reference/scripts/install.sh
@@ -3,2 +3,3 @@
-curl https://example.com/install.sh | bash
+# Pin the installer and verify checksum before execution:
+sha256sum -c install.sh.sha256 && bash install.sh
```

Diff format: unified diff with the checklist item ID in the comment header. Keep diffs minimal and reviewable.
