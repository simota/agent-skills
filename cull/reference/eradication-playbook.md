# Eradication Playbook

**Purpose:** Ordered removal sequence for confirmed infections, followed by dependency-ordered credential rotation.
**Read when:** Producing the `eradicate` or `rotate` recipe output.

**Load-bearing rule:** Stop persistence **before** deleting files, and verify eradication **before** rotating any credential. The Mini Shai-Hulud 2nd `gh-token-monitor` fires `rm -rf ~/` on HTTP 40x token-validity responses; rotating a credential it watches before stopping the watcher causes total data loss.

---

## Contents

- Phase 0: Pre-eradication evidence capture
- Phase 1: Stop persistence
- Phase 2: Quarantine droplets
- Phase 3: Delete (with second-scan verification)
- Phase 4: Reset IDE and CI state
- Phase 5: Verify clean before rotation
- Phase 6: Credential rotation (dependency-ordered)
- Phase 7: Re-onboarding and monitoring
- Rotation order: rationale
- Common mistakes

---

## Phase 0: Pre-eradication evidence capture

Before any destructive action, record evidence. The hash is the chain of custody; the deletion is irreversible.

```bash
QDIR="/tmp/husk-quarantine-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$QDIR/manifest" "$QDIR/files"

# Manifest header
{
  echo "host=$(hostname)"
  echo "user=$USER"
  echo "utc=$(date -u +%FT%TZ)"
  echo "ioc_database_version=<commit-or-date from cull/reference/ioc-database.md>"
} > "$QDIR/manifest/header.txt"

# For each matched file (do NOT delete yet):
for f in <list of matched paths>; do
  sha256sum "$f" >> "$QDIR/manifest/sha256.txt"
  stat -f '%N %m %z' "$f" 2>/dev/null >> "$QDIR/manifest/stat.txt"  # macOS
  stat -c '%n %Y %s' "$f" 2>/dev/null >> "$QDIR/manifest/stat.txt"  # Linux
done
```

If any file is suspected to be still actively read by an attacker process (Stage-2 payload), do not `cat` or `cp` it raw — the attacker may notice fs access. Snapshot via `cp --reflink=always` (Linux btrfs/xfs) or APFS clone (macOS) when possible.

---

## Phase 1: Stop persistence

**This is the load-bearing step. Do not skip.**

### macOS — LaunchAgent

```bash
# Stop and unload
launchctl unload ~/Library/LaunchAgents/com.user.gh-token-monitor.plist
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.user.gh-token-monitor.plist 2>/dev/null

# Verify nothing is still running
ps -ax | grep -E 'gh-token-monitor|tanstack_runner|router_runtime' | grep -v grep
# Should be empty.
```

### Linux — systemd user

```bash
systemctl --user stop gh-token-monitor 2>/dev/null
systemctl --user disable gh-token-monitor 2>/dev/null
systemctl --user daemon-reload

# Verify
ps -eo pid,cmd | grep -E 'gh-token-monitor|tanstack_runner|router_runtime' | grep -v grep
```

### Linux — cron / shell rc

If cron entries or `.bashrc` lines were matched, comment them out (do not delete yet — they're evidence). Use a single in-place edit guarded by backup:

```bash
cp ~/.bashrc "$QDIR/files/.bashrc.bak"
sed -i.before-husk -E '/<exact malicious line pattern>/s/^/# HUSK-DISABLED /' ~/.bashrc
```

### Live process kill (only after unit-file disable)

If persistence is disabled but the process is still running:

```bash
# Identify
ps -eo pid,cmd | grep -E 'gh-token-monitor|tanstack_runner|router_runtime' | grep -v grep

# Kill (SIGTERM first; SIGKILL only if SIGTERM ignored)
kill <PID>
sleep 2
kill -KILL <PID> 2>/dev/null
```

**Verification gate:** No matching process exists in `ps`. No LaunchAgent / systemd unit references the dropped binary. If either condition fails, re-run Phase 1; do not advance to Phase 2.

---

## Phase 2: Quarantine droplets

Move (not copy) matched files into the quarantine directory, preserving paths:

```bash
for f in <list of matched paths>; do
  rel=$(echo "$f" | sed -e "s|^$HOME/|HOME/|" -e "s|^/|ROOT/|")
  mkdir -p "$QDIR/files/$(dirname "$rel")"
  mv "$f" "$QDIR/files/$rel"
done

# Verify the originals are gone and quarantine is intact
find <original paths> -maxdepth 0 2>/dev/null   # should be empty
ls -la "$QDIR/files"
```

**Files to quarantine for Mini Shai-Hulud 2nd:**

```
~/Library/LaunchAgents/com.user.gh-token-monitor.plist   # macOS
~/.config/systemd/user/gh-token-monitor.service          # Linux
~/.config/gh-token-monitor/                              # Linux dir
~/.local/bin/gh-token-monitor.sh                         # Linux
<repo>/.claude/setup.mjs
<repo>/.claude/router_runtime.js
<repo>/.claude/settings.json    # only if confirmed-malicious; preserve user settings otherwise
<repo>/.vscode/setup.mjs
<repo>/.vscode/tasks.json       # only if confirmed-malicious
<repo>/.github/workflows/codeql_analysis.yml   # only if attacker-added per git-log
/tmp/tmp.ts018051808.lock
```

For `.claude/settings.json` and `.github/workflows/codeql_analysis.yml` specifically: these paths can be legitimate. Confirm via git history (`git log --diff-filter=A --name-only -- <path>`) — if the author is unknown or matches the attacker masquerade pattern (`claude <claude@users.noreply.github.com>`), quarantine. Otherwise audit content before deciding.

---

## Phase 3: Delete (with second-scan verification)

After quarantine, the original paths are already empty (Phase 2 used `mv`). The droplets remain in `$QDIR` as evidence; do not `rm -rf` the quarantine directory.

Re-run the scan with `--verify-clean`:

```bash
# Run the same scan procedure that produced the original findings
# Expect: zero matches.
```

If matches reappear (a watcher you missed, a Stage-1 launcher re-dropping Stage-2), return to Phase 1 with the new evidence.

### Reinstall affected packages clean

For each compromised npm package, identify the last-known-clean version (from the package's official postmortem; for TanStack Router: the version immediately before the compromised release per the project's postmortem URL in `ioc-database.md`):

```bash
# Drop the current install entirely
rm -rf node_modules pnpm-lock.yaml package-lock.json yarn.lock

# Reinstall pinned to clean versions + lifecycle scripts disabled
npm ci --ignore-scripts
# OR
pnpm install --ignore-scripts --frozen-lockfile
```

For container images: rebuild the image with the clean lockfile and re-deploy; do not patch a running container.

---

## Phase 4: Reset IDE and CI state

### Claude Code workspace

- Restart the IDE / CLI after `.claude/` quarantine. Hooks loaded into memory will otherwise persist.
- Run `chain` `intake` recipe on the now-cleaned `.claude/` directory to regenerate `.chain-manifest.json`.

### VS Code

- Restart with `--disable-extensions` once to confirm a clean process tree.
- Audit installed extensions: `code --list-extensions --show-versions` — flag any extension you did not personally install.

### GitHub repo

```bash
# Audit recently-added workflow files
git log --diff-filter=A --name-only --since='30 days' -- .github/workflows/

# Audit suspicious commits
git log --since='30 days' --author='claude <claude@users.noreply.github.com>'

# Force-pushes to release tags (suspicious)
git reflog show --all --since='30 days' | grep -i 'force'
```

If attacker commits are present in the history, coordinate with `trail` for full archaeology and with `triage` for the disclosure decision before any cleanup of public refs.

### CI runners

- Self-hosted: rebuild from a clean image; do not "clean" an existing runner.
- Ephemeral (GitHub-hosted): rotate the workflow's `permissions:` to least-privilege, audit `secrets:` for unused entries, and re-pin all third-party actions to full commit SHA.

---

## Phase 5: Verify clean before rotation

**Rotation is blocked until verification passes.**

```yaml
verify_clean_gate:
  - persistence_units_disabled: true       # systemctl / launchctl confirms
  - persistence_processes_absent: true     # ps confirms
  - droplets_in_quarantine: true
  - droplet_originals_absent: true
  - second_scan_zero_matches: true
  - lockfile_pins_clean: true              # reference/ioc-database.md cross-reference
  - npm_install_redone_without_scripts: true
  - ide_restarted: true
```

All eight must be `true`. If any is `false` or `unknown`, rotation is `not_eligible`.

---

## Phase 6: Credential rotation (dependency-ordered)

Rotate in this order. The order is dependency-driven: identity providers first (since downstream tokens may be re-issued from them), then long-tail secrets, then wallets last (because wallet rotation may require on-chain transactions that themselves need a clean signing key).

### 6.1 Cloud identity providers (highest priority)

| Order | Provider | Action |
|-------|----------|--------|
| 1 | AWS IAM access keys | `aws iam delete-access-key` + reissue; rotate `~/.aws/credentials` |
| 2 | AWS SSM Parameter Store | Audit recent reads; rotate any values matching exfil window |
| 3 | AWS Secrets Manager | Same as SSM |
| 4 | AWS STS session tokens | Wait for expiry; do not re-issue from compromised IAM key |
| 5 | GCP Application Default Credentials | `gcloud auth revoke && gcloud auth login` |
| 6 | Azure CLI tokens | `az logout && az login`; rotate service principals used recently |
| 7 | Kubernetes service-account tokens / kubeconfig | Rotate cluster admin first, then user kubeconfig |
| 8 | HashiCorp Vault | Revoke all leases from compromised IP; rotate root token if necessary |

### 6.2 SCM and package registries

| Order | Provider | Action |
|-------|----------|--------|
| 9 | GitHub Personal Access Tokens | Revoke ALL fine-grained + classic PATs; reissue with least-privilege scope |
| 10 | GitHub OAuth tokens (CLI, IDE) | Revoke in user settings → Applications |
| 11 | GitHub SSH keys | Audit `~/.ssh/authorized_keys` on hosts you control; rotate `id_rsa` / `id_ed25519` |
| 12 | GitHub Actions secrets | Rotate every secret in every repo that the compromised user has access to |
| 13 | npm publish tokens | Revoke at `npmjs.com/settings/<user>/tokens`; reissue with `bypass_2fa: false` |
| 14 | PyPI / Cargo / RubyGems publish tokens | Same pattern as npm |

### 6.3 Container registries and infra

| Order | Provider | Action |
|-------|----------|--------|
| 15 | Docker Hub PAT | Revoke + reissue |
| 16 | ECR / GAR / ACR pull secrets | Rotate; redeploy services that consumed them |
| 17 | CI/CD platform tokens (CircleCI, BuildKite, etc.) | Revoke + reissue |

### 6.4 SaaS that the env had OAuth into

Audit `~/.config/<service>/`, IDE token caches, browser-stored OAuth refresh tokens. Rotate any that were file-readable.

### 6.5 Cryptocurrency wallets (last, but critical)

If wallet directories were file-readable by the malware (`~/.electrum/wallets`, `~/.ethereum/keystore`, `~/.monero`, Exodus, Ledger Live config), assume the wallet is compromised:

| Order | Action |
|-------|--------|
| 18 | Generate a new wallet on a clean device |
| 19 | Move funds from the compromised wallet to the new wallet immediately |
| 20 | Treat the compromised seed phrase as burned — never reuse |
| 21 | Audit hardware-wallet companion apps separately — the firmware is fine; the host-side config (paired addresses, derivation paths) is not |

For staking / locked positions, accept loss rather than reuse the seed.

### 6.6 Notify and post-rotate

- Notify your employer / org security if any work credentials were on the machine. The DPA / incident-report clock starts.
- Notify npm security (`security@npmjs.com`) if your maintainer token was used to publish.
- Notify GHASA if a CVE / GHSA is appropriate for the package you maintain.
- File a postmortem via `triage`'s `postmortem` recipe.

---

## Phase 7: Re-onboarding and monitoring

After rotation:

1. Re-onboard the dev machine: fresh OS install is the gold standard for `ACTIVELY_BLEEDING` grade. For `CONFIRMED` without active execution, a clean reinstall of affected toolchains (Node, package managers, IDE) and a fresh OS user account is acceptable.
2. Enable Dependency Cooldown (`min-release-age=7`) and `ignore-scripts=true` per the hardening checklist in `scan-procedures.md`.
3. Pin GitHub Actions to full commit SHA + OIDC.
4. Schedule a `cull scan --verify-clean` weekly via `tempo` for the next 90 days.
5. Subscribe to the relevant advisory feeds (StepSecurity, OpenSSF, the package's own postmortem mailing list).

---

## Rotation order: rationale

Why this exact order?

- **Cloud identity first** because downstream registry tokens are often issued from cloud-identity OIDC flows. Rotating npm before AWS only swaps an attacker-known npm token for one the attacker can re-issue via the still-compromised AWS account.
- **GitHub PAT before npm** because GitHub Actions can mint npm tokens via OIDC. The attacker keeping a valid PAT means they can keep minting fresh npm tokens.
- **Wallets last** because earlier steps may require signed transactions (e.g. notifying a smart contract of key rotation). A compromised wallet should not sign anything once persistence is eradicated; the rule is "move funds out, then the wallet is dead."
- **Inside each tier, identity > read > publish**: revoke read tokens (which only expose data) before publish tokens (which can poison ecosystems) only when the read tokens are themselves bootstrap credentials. Otherwise revoke publish first (higher blast radius).

---

## Common mistakes

| Mistake | Consequence | Avoid by |
|---------|-------------|----------|
| Revoke GitHub PAT before stopping `gh-token-monitor` | `rm -rf ~/` fires | Phase 1 is non-negotiable |
| Delete droplets before quarantine | No evidence chain; cannot file disclosure | Phase 0 + Phase 2 ordering |
| Curl the C2 to "see what it does" | Attacker observes live response; payloads escalate | Passive log inspection only |
| Reinstall packages without `--ignore-scripts` | Stage-1 launcher runs again during reinstall | Phase 3 mandates `--ignore-scripts` |
| Trust SLSA provenance alone | Attackers obtained valid Build Level 3 provenance via CI/CD compromise | Cross-check provenance + clean-version baseline |
| Rotate cloud after GitHub | Attacker re-mints GitHub PAT via still-compromised cloud OIDC | Cloud → GitHub → npm order |
| Skip wallet rotation because "no fund movement seen" | Some drainers wait for high balances before draining | If keystore was readable, rotate |
| Reuse wallet seed after "cleaning" the machine | Seed phrase is burned the moment it left the host | New wallet, always |
| Auto-rotate without human approval | A wrong-order automation script fires retaliation | Rotation is gated on `verify_clean_gate` human-confirmed |

When in doubt, escalate to `triage` and wait. A few hours of delay is cheaper than `rm -rf ~/`.
