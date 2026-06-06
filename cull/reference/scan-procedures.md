# Scan Procedures

**Purpose:** OS-specific scan commands, passive log inspection, maintainer-side propagation audit, and the hardening checklist.
**Read when:** Running the `scan`, `shai-hulud`, `lockfile`, `propagation`, or `harden` recipe.

All scans are **read-only by default**. Deletion / modification commands belong to `eradication-playbook.md`. Never make outbound network calls to suspected attacker hosts.

---

## Contents

- Pre-scan: scope confirmation
- macOS scan
- Linux scan
- Windows / WSL scan
- Container image scan
- CI runner scan
- Lockfile-only scan (no FS traversal)
- Passive network log inspection
- Maintainer-side propagation audit
- Hardening checklist

---

## Pre-scan: scope confirmation

Before any scan, capture the environment fingerprint. This is also the input to `_STEP_COMPLETE.Output.target`.

```bash
# Identity (no creds emitted)
uname -srm
sw_vers 2>/dev/null || cat /etc/os-release 2>/dev/null
echo "shell=$SHELL user=$USER home=$HOME pwd=$PWD"

# Package managers present
command -v npm pnpm yarn bun deno corepack 2>/dev/null
command -v pip pipx poetry uv 2>/dev/null
command -v gem cargo go 2>/dev/null

# Lockfiles in cwd (no traversal yet)
ls -1 package-lock.json pnpm-lock.yaml yarn.lock npm-shrinkwrap.json \
      requirements.txt Pipfile.lock poetry.lock uv.lock \
      Gemfile.lock Cargo.lock go.sum 2>/dev/null

# Recent install windows
ls -lat ~/.npm/_logs 2>/dev/null | head -10
ls -lat ~/.cache/pnpm 2>/dev/null | head -10
```

If suspected campaign install window known (e.g. Mini Shai-Hulud 2nd: 2026-05-12 onward), narrow scope to artifacts mtime-after that date first; widen if nothing found.

---

## macOS scan

### Persistence: LaunchAgents (per-user)

```bash
# Inventory
ls -la ~/Library/LaunchAgents/ 2>/dev/null
ls -la /Library/LaunchAgents/  2>/dev/null

# IoC match — Mini Shai-Hulud 2nd
find ~/Library/LaunchAgents /Library/LaunchAgents \
  -name 'com.user.gh-token-monitor.plist' 2>/dev/null

# Inspect any unfamiliar plist (read-only)
plutil -p ~/Library/LaunchAgents/<file>.plist
```

Flag every plist whose `ProgramArguments` references `bun`, `deno`, unfamiliar node paths, or scripts under `~/.config/`, `~/.local/`, `/tmp/`.

### IDE-hook implants

```bash
# Project-scoped (cwd) and home-scoped
find . ~/. -maxdepth 6 \( \
    -path '*/.claude/setup.mjs' -o \
    -path '*/.claude/router_runtime.js' -o \
    -path '*/.claude/settings.json' -o \
    -path '*/.vscode/setup.mjs' -o \
    -path '*/.vscode/tasks.json' -o \
    -path '*/.github/workflows/codeql_analysis.yml' \
  \) 2>/dev/null
```

For each match, capture sha256 and mtime before any classification.

### Live processes

```bash
ps -ax -o pid,user,etime,command \
  | grep -E 'tanstack_runner|router_runtime|gh-token-monitor|bun .*router_init' \
  | grep -v grep
```

A live match → grade `ACTIVELY_BLEEDING`. Do not kill yet; document first, then proceed to eradication-playbook.

### Runtime artifacts

```bash
find /tmp -maxdepth 2 -name 'tmp.ts*.lock' -mmin -10080 2>/dev/null    # last 7 days
find /private/tmp -maxdepth 2 -name 'tmp.ts*.lock' -mmin -10080 2>/dev/null
```

### Recent npm install windows

```bash
ls -la ~/.npm/_logs/ | head -30
grep -l 'optionalDependencies' ~/.npm/_logs/*.log 2>/dev/null | head -5
```

### File quarantine staging (read-only check)

```bash
mkdir -p "/tmp/husk-quarantine-$(date -u +%Y%m%dT%H%M%SZ)"
# Do NOT move files yet. The directory is staged for eradication phase.
```

---

## Linux scan

### Persistence: systemd user units

```bash
# Inventory
systemctl --user list-unit-files --no-pager 2>/dev/null | head -50
ls -la ~/.config/systemd/user/ 2>/dev/null

# IoC match — Mini Shai-Hulud 2nd
find ~/.config/systemd/user -name 'gh-token-monitor.service' 2>/dev/null
find ~/.local/bin -name 'gh-token-monitor.sh' 2>/dev/null
find ~/.config/gh-token-monitor -type f 2>/dev/null
```

### Cron + at + anacron

```bash
crontab -l 2>/dev/null
ls -la /etc/cron.{hourly,daily,weekly,monthly}/ 2>/dev/null
at -l 2>/dev/null
```

### Shell rc files

```bash
grep -nE 'curl |wget |source .*\.(sh|mjs)|node -e ' \
  ~/.bashrc ~/.zshrc ~/.profile ~/.bash_profile 2>/dev/null
```

### IDE-hook implants (same as macOS — paths are identical)

### Live processes

```bash
ps -eo pid,user,etime,cmd \
  | grep -E 'tanstack_runner|router_runtime|gh-token-monitor|bun .*router_init' \
  | grep -v grep
```

---

## Windows / WSL scan

### Persistence — Scheduled Tasks

```powershell
Get-ScheduledTask | Where-Object {$_.Author -notmatch 'Microsoft|Adobe|<known>'} `
  | Select TaskName, TaskPath, Author, State
```

### Run keys

```powershell
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
Get-ItemProperty 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run'
```

### WSL distributions

WSL distros are effectively Linux from this skill's perspective. Run the Linux scan inside each distro:

```powershell
wsl -l -v
wsl -d <distro> -- bash -c 'ls ~/.config/systemd/user 2>/dev/null'
```

Distro-side IDE hooks (`.claude/`, `.vscode/`) are reachable from Windows under `\\wsl$\<distro>\home\<user>\` — but always scan from inside the distro to preserve mtime fidelity.

---

## Container image scan

For a built image (not a running container):

```bash
# Layer inventory
docker history --no-trunc <image>:<tag>

# Filesystem snapshot via export (no run)
docker create --name husk-tmp <image>:<tag>
docker export husk-tmp | tar -tvf - \
  | grep -E '(\.claude|\.vscode|gh-token-monitor|router_init)'
docker rm husk-tmp
```

If a malicious package version is in the base image's lockfile, the eradication runbook becomes "rebuild from clean base + repinned lockfile," not "delete files from a running container."

---

## CI runner scan

GitHub Actions runner artifacts (when the runner is yours, not GitHub-hosted ephemeral):

```bash
# Self-hosted runner workspace
find /home/runner /var/lib/github-runner -maxdepth 8 \
  \( -name 'codeql_analysis.yml' -o -name 'setup.mjs' -o -name 'tanstack_runner.js' \) 2>/dev/null

# OIDC token exchange logs (recent, suspicious)
# Check Actions audit log for OIDC issuance to unexpected audiences (npm)
```

For GitHub-hosted ephemeral runners, the eradication target is the workflow config + secrets, not the runner FS — runners are discarded per job. Coordinate with `gear` to rebuild the workflow.

---

## Lockfile-only scan (no FS traversal)

Fast pre-merge check. No `find`, no process inspection, no network.

```bash
# npm
node -e '
const lock = require("./package-lock.json");
const bad = new Set([
  "@tanstack/react-router@<known-bad-version>",
  // populate from reference/ioc-database.md
]);
for (const [name, info] of Object.entries(lock.packages || {})) {
  const v = info.version;
  if (v && bad.has(name.replace(/^node_modules\//,"") + "@" + v)) {
    console.log("MATCH:", name, v, info.resolved);
  }
}
' 2>/dev/null
```

```bash
# pnpm — pnpm-lock.yaml
grep -E '/@tanstack/react-router@|/@nx/' pnpm-lock.yaml | head -20

# yarn — yarn.lock
grep -E '"@tanstack/react-router@' yarn.lock | head -20
```

For Python:

```bash
grep -E '^(<known-bad-package>)==' requirements.txt Pipfile.lock 2>/dev/null
```

Output the exact line and the `resolved` URL (tarball hash if present). Cross-reference against `ioc-database.md` version table.

---

## Passive network log inspection

**Do not probe attacker hosts.** Read locally available logs only.

```bash
# macOS — Unified Log (recent outbound)
log show --predicate 'process == "node" OR process == "bun"' \
  --info --debug --last 7d 2>/dev/null \
  | grep -iE 'git-tanstack|masscan|getsession|filev2'

# Linux — journalctl
journalctl --user --since '7 days ago' 2>/dev/null \
  | grep -iE 'git-tanstack|masscan|getsession|filev2'

# Cross-platform — DNS resolver cache (if any)
# macOS:
sudo killall -INFO mDNSResponder 2>/dev/null
log show --predicate 'process == "mDNSResponder"' --last 7d 2>/dev/null \
  | grep -iE 'git-tanstack|getsession'

# tcpdump capture (if running) — DO NOT initiate new capture if it would alert the attacker
```

Match against the C2 list in `reference/ioc-database.md`. Any positive match → `CONFIRMED`.

---

## Maintainer-side propagation audit

For a maintainer whose npm publish token may have been used:

```bash
# Enumerate your packages (use a separate, uncompromised session to log in)
npm whoami
npm access list packages --json | head

# Check publish history on each package
for pkg in $(npm access list packages --json | jq -r 'keys[]'); do
  echo "=== $pkg ==="
  npm view "$pkg" time --json | jq 'to_entries | sort_by(.value) | reverse | .[0:5]'
done

# Cross-check each recent version's provenance attestation
for pkg in $(npm access list packages --json | jq -r 'keys[]'); do
  v=$(npm view "$pkg" version)
  npm view "$pkg@$v" --json | jq '.dist.attestations // "no-provenance"'
done

# GitHub Actions OIDC issuance audit (org-level)
gh api "orgs/<org>/audit-log?phrase=action:oidc_token_issuance" --paginate \
  | jq '.[] | select(.created_at > "2026-05-01")'
```

A publish you did not initiate **with no SLSA provenance** or with an unexpected audience claim → propagation confirmed. Escalate to `triage` and notify npm (npm security@npmjs.com).

---

## Hardening checklist (independent of grade)

### npm

```bash
# Globally disable lifecycle scripts during install
npm config set ignore-scripts true
# Per-install:
npm ci --ignore-scripts
```

`.npmrc` (project or `~/.npmrc`):

```
ignore-scripts=true
min-release-age=7        # Dependency Cooldown — refuse packages younger than 7 days
fund=false
audit=false              # rely on lockfile pinning + provenance; npm audit is noisy
provenance=true          # require provenance attestation when publishing
```

### pnpm

`pnpm-workspace.yaml` or `.npmrc`:

```
ignore-scripts=true
package-manager-strict=true
minimum-release-age=10080            # minutes (= 7 days)
trust-policy=no-downgrade            # refuse downgrade of trusted packages
```

### yarn (berry)

`.yarnrc.yml`:

```yaml
enableScripts: false
enableHardenedMode: true
checksumBehavior: throw
```

### Python

```bash
pip install --require-hashes -r requirements.txt
# Use uv with hash-locked lock file:
uv pip compile requirements.in -o requirements.txt --generate-hashes
```

### GitHub Actions

- Pin every third-party action to **full commit SHA**, never `@v1` / `@main`.
- Use OIDC for cloud auth (`permissions: id-token: write`), never long-lived AWS / GCP secrets.
- Set workflow-level `permissions:` to least-privilege (`contents: read` default).
- Never use `pull_request_target` with `actions/checkout` of the PR head.
- Enable secret scanning + push protection at the repo level.
- Sign deployment artifacts with Sigstore / Cosign.

### Registry proxy (organization-wide)

- Use Verdaccio / Sonatype Nexus / Artifactory / Takumi Guard as a pinned mirror.
- Reject packages younger than `min-release-age`.
- Reject packages without provenance for security-critical dependencies.
- Quarantine new versions for human review before promotion.

### IDE / Claude Code

- Pin every skill via `chain` `.chain-manifest.json`; re-verify on session start.
- Block `.claude/setup.mjs` / `.vscode/setup.mjs` from being executed at workspace open (Latch hook).
- Disable workspace-trust auto-grant; require explicit "trust this folder" per repo.

### Renovate / Dependabot

Renovate `config.json`:

```json
{
  "minimumReleaseAge": "7 days",
  "configMigration": true,
  "rangeStrategy": "pin",
  "vulnerabilityAlerts": {"enabled": true},
  "packageRules": [
    {"matchManagers": ["npm"], "minimumReleaseAge": "10 days"}
  ]
}
```

### Reporting

Maintain a written incident-response runbook that names:
- Who owns the npm publish token rotation (and the backup human if they're unavailable)
- Where the IoC database lives (`cull/reference/ioc-database.md`)
- The current `ioc_database_version` and last-update date
- Pre-authorized actions: `launchctl unload` / `systemctl --user stop` on a named persistence unit may be auto-executed; everything else requires human sign-off

---

## Output contract for scan

Each scan emits, per matched IoC:

```yaml
- ioc_family: mini-shai-hulud-2nd
  surface: persistence | droplet | lockfile | process | network | git-log
  path_or_evidence: ~/Library/LaunchAgents/com.user.gh-token-monitor.plist
  sha256: <if file>
  mtime: 2026-05-12T14:33:21Z
  size_bytes: 487
  source: https://blog.flatt.tech/entry/mini_shai_hulud_2nd
  source_date: 2026-05-13
```

Aggregate findings, classify grade, and only then proceed to eradication.
