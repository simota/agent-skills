# IoC Database

**Purpose:** Curated, source-cited IoC tables per public supply-chain worm campaign.
**Read when:** Scanning, classifying grade, or proposing IoC database PRs.

Each section is dated. When a new wave is published, add an entry with `Source: <URL>` and `Reported: YYYY-MM-DD`. Never invent IoCs.

---

## Contents

- Mini Shai-Hulud 1st wave (2026-04)
- Mini Shai-Hulud 2nd wave (2026-05) — TanStack Router compromise
- S1ngularity (2024-08)
- lottie-player (2024-10)
- General npm Stage-1 launcher signatures
- General npm Stage-2 payload signatures
- General persistence signatures (cross-campaign)
- C2 / exfil channel signatures
- GitHub anomaly signatures
- Update checklist for new campaigns

---

## Mini Shai-Hulud 2nd wave (2026-05) — TanStack Router compromise

**Reported:** 2026-05-12
**Source:** https://blog.flatt.tech/entry/mini_shai_hulud_2nd
**Cross-reference:** StepSecurity advisory, TanStack postmortem (https://tanstack.com/blog/npm-supply-chain-compromise-postmortem), GHSA-g7cv-rxg3-hmpx
**Scale:** 200+ npm packages compromised. UiPath, Mistral AI SDK, DraftLab among victims. CI/CD pipeline compromise as primary initial-access vector.

### Stage-1 launcher (optionalDependencies pattern)

```json
"optionalDependencies": {
  "@tanstack/setup": "github:tanstack/router#79ac49eedf..."
}
```

| Signal | Value |
|--------|-------|
| Attacker GitHub fork account ID | `269549300` |
| Lifecycle script | `prepare` (executes during install) |
| Runtime | Bun (called by `tanstack_runner.js`) |
| Failure tactic | Trailing `exit 1` to disguise execution as graceful failure |

### Stage-1 droplet files

| File | sha256 |
|------|--------|
| `router_init.js` | `ab4fcadaec49c03278063dd269ea5eef82d24f2124a8e15d7b90f2fa8601266c` |
| `tanstack_runner.js` | `2ec78d556d696e208927cc503d48e4b5eb56b31abc2870c2ed2e98d6be27fc96` |

### Stage-2 payload (`router_init.js` embedded in `@tanstack/react-router`)

| Property | Value |
|----------|-------|
| Size | ~2.3 MB (single-line obfuscated) |
| Bundled into | `@tanstack/react-router` |
| Clean baseline | ~190 KB → malicious ~905 KB (4.7× inflation) |
| Obfuscation | PBKDF2 200,000 iterations + multi-layer AES-GCM |

### Stage-3 credential targets (file-based)

```
~/.aws/credentials
~/.aws/config
~/.config/gcloud/application_default_credentials.json
~/.azure/accessTokens.json
~/.kube/config
~/.vault-token
~/.ssh/id_rsa
~/.ssh/id_ed25519
~/.npmrc
~/.electrum/wallets
~/.ethereum/keystore
~/.monero
~/.config/Exodus
~/Library/Application Support/Ledger Live
```

### Stage-3 cloud API probing (2nd-wave-specific)

| Target | Endpoint / pattern |
|--------|--------------------|
| AWS STS | `sts.us-east-1.amazonaws.com` (credential validity check) |
| AWS SSM Parameter Store | All 17 regions scanned |
| AWS Secrets Manager | All 17 regions scanned |
| HashiCorp Vault | `127.0.0.1:8200` local probe |
| EC2 / ECS metadata | `169.254.169.254`, `169.254.170.2` |
| GitHub CLI | `gh auth token` invocation |

### Stage-4 exfiltration channels (3 parallel)

**A. Primary C2**
- `hxxps://git-tanstack[.]com:443/router` (POST)
- `api[.]masscan[.]cloud/v2/upload` (confirmed alternate)

**B. Session Protocol (always-on parallel)**
- Endpoint: `hxxp://filev2.getsession[.]org/file/{id}`
- Encryption: RSA-4096-OAEP + AES-256-GCM hybrid
- Seed nodes: `seed1.getsession[.]org`, `seed2.getsession[.]org`, `seed3.getsession[.]org`
- Recipient Session ID: `05f9e609d79eed391015e11380dee4b5c9ead0b6e2e7f...`
- TLS pin: CN=`seed1.getsession[.]org`, issuer `Oxen Privacy Tech Foundation`

**C. GitHub fallback (only on C2 failure)**
- Repo naming pattern: `{dune_word}-{dune_word}-{3-digit}` (e.g. `arrakis-fremen-042`)
- Commit method: `createCommitOnBranch` GraphQL mutation (aliases `b0`, `b1`, ...)
- Commit message: `"chore: update dependencies"`
- Chunk size: 30 MB, base64-encoded

### Stage-5 persistence

**macOS**
```
~/Library/LaunchAgents/com.user.gh-token-monitor.plist
```

**Linux**
```
~/.config/systemd/user/gh-token-monitor.service
~/.config/gh-token-monitor/
~/.local/bin/gh-token-monitor.sh
```

**Cross-platform IDE hooks**
```
.claude/settings.json
.claude/setup.mjs
.claude/router_runtime.js
.vscode/tasks.json
.vscode/setup.mjs
.github/workflows/codeql_analysis.yml   # attacker-added, masquerades as legitimate
```

### Retaliation payload (critical)

`gh-token-monitor` polls every 60 seconds:

```bash
gh auth status  # or equivalent token-validity check
# On HTTP 40x response:
rm -rf ~/
```

**npm token description hook:**
```
IfYouRevokeThisTokenItWillWipeTheComputerOfTheOwner
```

→ **Rotation must be gated on persistence eradication.** This is the load-bearing rule for the whole skill.

### Stage-6 worm propagation (maintainer-side)

1. Select npm tokens with `bypass_2fa: true`
2. Enumerate packages: `https://registry.npmjs.org/-/v1/search?text=maintainer:{username}&size=250`
3. Inject `router_init.js` + tampered `package.json` into target tarballs
4. CI/CD: obtain npm publish token via GitHub OIDC token exchange
5. `PUT` tampered tarball with valid SLSA Provenance (Build Level 3) attached

### Runtime indicators

| Surface | Pattern |
|---------|---------|
| Lockfile | `/tmp/tmp.ts018051808.lock` |
| Processes | `tanstack_runner`, `router_runtime`, `gh-token-monitor`, anomalous `bun` |
| Git anomaly | Commits authored by `claude <claude@users.noreply.github.com>` |

---

## Mini Shai-Hulud 1st wave (2026-04)

**Reported:** 2026-04-29
**Source:** https://blog.flatt.tech/entry/mini_shai_hulud (companion article)
**Scale:** 6 packages compromised.
**Initial access:** Stolen npm publish tokens (not yet CI/CD).
**Persistence:** IDE hooks only (no LaunchAgent / systemd).
**Exfil:** GitHub only (no C2 / no Session Protocol).

**Cross-wave indicators (also present in 2nd wave):**
- IDE-hook implant paths (`.claude/`, `.vscode/`)
- GitHub repo creation with `{dune_word}` patterns
- Commits authored by `claude <claude@users.noreply.github.com>`

When scanning a system that may have been hit by 1st wave, the absence of OS-level persistence **does not** imply absence of compromise — check IDE hooks and GitHub history independently.

---

## S1ngularity (2024-08)

**Reported:** 2024-08-26
**Targets:** Nx-related packages.
**Cross-wave indicators:**
- AI-CLI invocation harvesting (`claude`, `agy`, `q` CLI used to enumerate repos / credentials)
- GitHub repo `s1ngularity-repository-*` pattern
- Cryptocurrency wallet exfil (Electrum, Ethereum keystore)

Husk's `propagation` recipe specifically targets this maintainer-side pattern.

---

## lottie-player (2024-10)

**Reported:** 2024-10-31
**Targets:** `@lottiefiles/lottie-player` npm package.
**Surface:** Browser-side cryptocurrency wallet drainer (no OS persistence).

When matched: scope is browser tabs that loaded the package; OS-side IoCs are absent. Still escalate to `triage` because user wallets may already be drained.

---

## General npm Stage-1 launcher signatures

These cross campaigns and should be flagged regardless of named family:

| Pattern | Risk |
|---------|------|
| `optionalDependencies` referencing `github:<owner>/<repo>#<sha>` orphan commit | Stage-1 launcher |
| `prepare`, `postinstall`, `preinstall` script that fetches and executes remote code | Stage-1 launcher |
| `postinstall` invoking `node -e "$(curl ...)"` or `node -e "$(wget ...)"` | Direct RCE |
| `dependencies` self-referencing a fork with non-semver tag | Stage-1 launcher |
| Package source size > 2× clean baseline | Stage-2 payload candidate (cross-reference clean version sha256) |
| Single-line minified JS in source files (not just dist) | Obfuscated payload |
| Bun / Deno invocation in a package that does not declare these as engines | Sandbox-escape candidate |

---

## General npm Stage-2 payload signatures

| Pattern | Risk |
|---------|------|
| PBKDF2 with >100,000 iterations + AES-GCM in source | Multi-layer obfuscation |
| Hardcoded curve25519 / ed25519 public keys (recipient pinning) | C2 receiver identity |
| Embedded base64 blob > 100 KB | Encrypted payload |
| `process.env.AWS_*`, `GCP_*`, `AZURE_*` enumeration | Credential harvest |
| Recursive walk of `~/.config`, `~/Library/Application Support`, `%APPDATA%` | Filesystem credential sweep |

---

## General persistence signatures (cross-campaign)

| Surface | Pattern |
|---------|---------|
| macOS LaunchAgent | `~/Library/LaunchAgents/*.plist` with `ProgramArguments` referencing unfamiliar interpreter (`bun`, `deno`, hidden node path) |
| macOS LaunchDaemon (rare for user-level malware) | `/Library/LaunchDaemons/*.plist` — flag any unauthored entry |
| Linux systemd user | `~/.config/systemd/user/*.service` with `ExecStart` referencing `~/.local/bin/*.sh` of unknown origin |
| Linux cron | `crontab -l` entries referencing `~/.config/`, `/tmp/`, or `~/.local/bin/` |
| Windows Scheduled Task | `schtasks /query` entries with unknown `Author` and command lines invoking PowerShell with `-EncodedCommand` |
| Windows Run keys | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` entries added recently |
| Cross-platform shell rc | `~/.bashrc`, `~/.zshrc`, `~/.profile` containing `source ~/.config/<unknown>` |
| Editor extensions | `~/.vscode/extensions/`, `~/.cursor/extensions/`, `~/.continue/extensions/` with packages installed outside marketplace |

---

## C2 / exfil channel signatures

| Channel | Known endpoints |
|---------|----------------|
| HTTP C2 (Mini Shai-Hulud 2nd) | `git-tanstack[.]com`, `api[.]masscan[.]cloud` |
| Session Protocol seed nodes | `seed1.getsession[.]org`, `seed2.getsession[.]org`, `seed3.getsession[.]org` |
| Session Protocol file relay | `filev2.getsession[.]org`, `filev2-<n>.getsession[.]org` |
| GitHub fallback | `api.github.com/repos/.../createCommitOnBranch` with `b\d+` aliases |
| DNS exfil (occasional) | TXT queries to subdomain-encoded base32 payloads |
| Discord webhook (older campaigns) | `discord[.]com/api/webhooks/...` POSTed from package code |
| Pastebin / GitHub gist | unauthenticated POST from package install context |

**Passive log inspection only.** Never `curl`, `dig`, or `nslookup` these from the suspect environment — that confirms infection to the attacker and may activate further payloads.

---

## GitHub anomaly signatures

| Pattern | Risk |
|---------|------|
| New repos matching `{dune_word}-{dune_word}-\d{3}` (Arrakis lore: `fremen`, `harkonnen`, `arrakis`, `caladan`, `sietch`, `shai`, `hulud`, `gom`, `jabbar`, ...) | Mini Shai-Hulud exfil |
| New repos matching `s1ngularity-repository-*` | S1ngularity exfil |
| Commits with message exactly `chore: update dependencies` from unknown author within last 7 days | Generic exfil pattern |
| Commits authored by `claude <claude@users.noreply.github.com>` | Mini Shai-Hulud attribution masquerade |
| `createCommitOnBranch` mutations with `b\d+` aliases in audit log | GraphQL-API exfil pattern |
| Force-push to release tag within hours of release publish | Tarball substitution attempt |
| New `.github/workflows/codeql_analysis.yml` not authored by the team | CI implant |
| `SECRETS.*` access from unfamiliar workflow within last 14 days | Credential harvest via Actions |

---

## Update checklist for new campaigns

When adding a new campaign section:

1. Header: campaign name + first-reported date + cross-reference URL.
2. Initial-access vector (stolen-token / CI-pipeline / typosquatting / dependency-confusion / vibe-coding-supply-chain).
3. Stage table: launcher → payload → credential targets → exfil → persistence → propagation.
4. Per file: sha256 + canonical path + size.
5. Per network endpoint: host + port + URL pattern (defang with `[.]`).
6. Retaliation payloads: if revoke-on-detect or `rm -rf`-class, flag prominently — rotation runbook must be gated on persistence eradication.
7. Source citations: at least two independent sources for `CONFIRMED` IoCs (vendor advisory + maintainer postmortem ideally).
8. Update the `Critical Patterns (Quick Reference)` table in `husk/SKILL.md` if the family introduces a new persistence surface or retaliation hook.
9. Bump the `ioc_database_version` value emitted in `_STEP_COMPLETE` to the new commit date.

**Never copy raw exfil URLs without defanging.** Defang scheme (`https` → `hxxps`) and TLDs (`com` → `[.]com`) so the reference file is not itself a click-trap.
