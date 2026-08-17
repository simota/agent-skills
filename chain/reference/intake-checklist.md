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
6b. MCP server intake (risk tier + evaluation card)
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

## 6b. MCP Server Intake (in addition to §1-6)

§1-6 detect a *tampered* artifact. They say nothing about whether a **well-behaved** server should be
connected at all — an honestly-built server with a production database token is a production-mutation grant
no checksum will flag. Run this section for every MCP server, including ones that pass §1-6 cleanly.

**Host sandbox does not extend to the server.** A host running `workspace-write` connected to a server
holding a production API token has a production blast radius. Track the control plane per tool, not per host.

### Risk tier (assign before connecting)

| Tier | Capability | Typical | Required controls |
|------|-----------|---------|-------------------|
| `R0` | local read-only, static data, no network | public docs read | declaration only |
| `R1` | authenticated read | issues, observability, internal docs | credential scope review; may surface confidential data |
| `R2` | limited write | issue/comment create, branch ops | approval per side-effecting call; external state changes and notifications are not undoable |
| `R3` | infrastructure / production mutation | cloud resources, deploy, database write | explicit human approval, dedicated credential, audit log, environment isolation — never auto-approved |

Tier is set by the **widest tool the server exposes**, not by the tool the task intends to call. A server
whose read tools are needed and whose write tools are merely present is `R2`, not `R1` — unless the write
tools are removed or denied server-side.

### When not to connect

Reject when a single CLI command suffices · a repository file read suffices · write scope cannot be narrowed ·
server owner or update policy unknown · secret storage unknown · tool results cannot be verified · a native
integration offers clearer permission and audit · the team cannot maintain it.

### Evaluation Card (required; store alongside `.chain-manifest.json`)

```yaml
server_id:
purpose:
owner:                      # a person, not a team alias with no on-call
source_repository:
package_and_version:        # pinned; digest where the transport supports it
transport:                  # stdio | remote-http — record the boundary each implies
tools:
  read: []
  write: []                 # empty is a meaningful answer; state it explicitly
credentials:                # scope, not the value
network_destinations: []    # allowlisted; "any" is a rejection
data_classification:        # highest class reachable through any tool
host_sandbox_relation:      # inside | outside the host sandbox
risk_tier:                  # R0-R3 from the table above
approval_policy:
logging:                    # audit log + side-effect ID availability
update_policy:              # who updates, on what trigger; auto-update = P1
rollback_and_removal:
verification_status:        # executed | documentation-verified | not-executed
```

**A card with `verification_status: not-executed` cannot yield `APPROVED`** — it caps at
`APPROVED_WITH_FLAG` under §9, and `R3` never reaches even that without human approval on record.
Removal is part of intake: a server whose removal has never been tested is a dependency, not an integration.

### Token handling (check explicitly — passing tests do not surface these)

- **No token passthrough.** The host's own token is never forwarded to the server, and the server's token is
  never forwarded to a downstream API unchanged. Each hop issues its own credential; a passed-through token
  carries the *caller's* full permission set, which is always wider than the call.
- **Audience is bound and verified.** The token names the tool/API it is for, and the receiver checks that it
  is the intended audience. A token accepted without an audience check is usable anywhere it is replayed.
- **No confused deputy.** The server must not perform privileged actions on behalf of a caller purely because
  *it* is authorized — the caller's authority is what decides, and the server holding a broad credential is
  not the caller's authority. Servers that act with their own standing credential on unauthenticated or
  weakly-scoped requests are `P0`.

Failures map to §9 as: undeclared network destination or credential scope → `P0` · token passthrough,
missing audience binding, or confused-deputy exposure → `P0` · unpinned version or
auto-update → `P1` · missing owner, logging, or removal test → `P2` · tool schema changed since the card was
written → re-run intake, do not amend the card in place.

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
