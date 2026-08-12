# Handoff Templates

**Purpose:** Canonical handoff blocks between Cull and partner agents.
**Read when:** Producing inbound / outbound handoff sections in a Cull report.

All handoffs follow `_common/HANDOFF.md` canonical schema. The fields below are the Cull-specific surfaces.

---

## Inbound

### USER_TO_CULL_REQUEST

```yaml
from: User
to: Cull
intent: scan | shai-hulud | lockfile | eradicate | rotate | harden | propagation
context:
  os: macOS | Linux | Windows | WSL | container | CI
  suspect_window: "<UTC range, e.g. 2026-05-12..now>"
  suspect_campaign: "<mini-shai-hulud-2nd | unknown>"
  scope:
    - "<repo path or HOME or container image>"
  prior_actions: "<anything the user already did>"
constraints:
  read_only_until_confirm: true
  may_quarantine: false       # set true only with explicit user opt-in
```

### SENTINEL_TO_CULL_HANDOFF

```yaml
from: Sentinel
to: Cull
trigger: deps_match | slopsquat_candidate | lockfile_pin_anomaly
context:
  package: "<name@version>"
  lockfile_path: "<path>"
  cve_or_ghsa: "<id or null>"
  sentinel_confidence: HIGH | MEDIUM | LOW
ask:
  - Confirm whether this lockfile match corresponds to a live infection in the dev environment
  - Run persistence + droplet scan
  - Return grade and evidence chain
```

### CHAIN_TO_CULL_HANDOFF

```yaml
from: Chain
to: Cull
trigger: ide_hook_signature_match | mcp_implant_suspected
context:
  matched_paths:
    - ".claude/setup.mjs"
    - ".vscode/setup.mjs"
  chain_verdict: REJECTED | QUARANTINED
  manifest_diff: "<paths with sha256 mismatch>"
ask:
  - Run live-environment scan to determine grade
  - If CONFIRMED, return eradication runbook + Chain quarantine actions
```

### BUILDER_TO_CULL_PRESCAN

```yaml
from: Builder
to: Cull
trigger: pr_diff_lockfile_change | pr_diff_optional_deps | pr_diff_install_script
context:
  pr_number: "<#>"
  base_ref: "<sha>"
  head_ref: "<sha>"
  changed_lockfiles:
    - "package-lock.json"
ask:
  - Run lockfile recipe against the head_ref lockfile
  - Block merge if any IoC match found
  - Return grade and per-finding evidence
```

### TRAIL_TO_CULL_HANDOFF

```yaml
from: Trail
to: Cull
trigger: suspicious_commit | force_pushed_tag | unknown_author_commit
context:
  commit_sha: "<sha>"
  author: "claude <claude@users.noreply.github.com>"
  files_touched:
    - ".github/workflows/codeql_analysis.yml"
  date: "<UTC>"
ask:
  - Cross-check commit against IoC database
  - Confirm whether dev environment shows corresponding droplets / persistence
```

### TRIAGE_TO_CULL_HANDOFF

```yaml
from: Triage
to: Cull
trigger: sev1_supply_chain_incident
context:
  incident_id: "<id>"
  severity: SEV1 | SEV2
  affected_hosts:
    - "<hostname or runner id>"
  hypothesis: "<short>"
constraints:
  time_pressure: "<UTC deadline for first report>"
  approved_actions:
    - "launchctl unload (for IoC-matched LaunchAgent only)"
    - "systemctl --user stop (for IoC-matched unit only)"
  blocked_actions:
    - "any credential revocation"
    - "any production infra change"
ask:
  - Run full scan; classify grade
  - If ACTIVELY_BLEEDING, stop persistence and return verified-stopped state
  - Return evidence chain + runbook for Triage's incident report
```

---

## Outbound

### CULL_TO_TRIAGE_INCIDENT

```yaml
from: Cull
to: Triage
trigger: grade_confirmed | grade_actively_bleeding
context:
  grade: CONFIRMED | ACTIVELY_BLEEDING
  campaign: "<e.g. mini-shai-hulud-2nd>"
  evidence_summary:
    persistence:
      - path: "~/Library/LaunchAgents/com.user.gh-token-monitor.plist"
        sha256: "<hash>"
        status: stopped | running
    droplets:
      - count: <n>
        quarantine_path: "/tmp/cull-quarantine-<utc>/"
    lockfile_pins:
      - package: "<name@version>"
        lockfile: "<path>"
    exfil_traces:
      - host: "git-tanstack[.]com"
        evidence: "<log line, defanged>"
  retaliation_risk:
    rm_rf_payload_present: true | false
    revoke_must_be_gated: true
  eradication_status: in_progress | verified_clean | blocked
  rotation_status: not_eligible | ready | issued
recommended_severity: SEV1 | SEV2
recommended_first_actions:
  - "Open war room; assign IC (per Triage 'first-response' recipe)"
  - "Wait for Cull eradication-verified before any credential rotation"
  - "Coordinate disclosure with legal if customer data was on host"
```

### CULL_TO_SENTINEL_LOCKFILE

```yaml
from: Cull
to: Sentinel
trigger: confirmed_malicious_version_pin
context:
  package: "<name@version>"
  lockfiles:
    - "<path>"
  clean_version_to_pin: "<name@version>"
  campaign: "<e.g. mini-shai-hulud-2nd>"
ask:
  - Run deps recipe across the org / monorepo to find other lockfiles pinning this version
  - Propose org-wide upgrade plan with rollback strategy
  - If slopsquat candidate, integrate into Sentinel's slopsquat detection registry
```

### CULL_TO_CHAIN_QUARANTINE

```yaml
from: Cull
to: Chain
trigger: confirmed_ide_hook_compromise
context:
  affected_skill_dirs:
    - "<repo>/.claude/"
    - "<repo>/.vscode/"
  quarantine_path: "/tmp/cull-quarantine-<utc>/"
  manifest_before:
    - file: ".claude/setup.mjs"
      sha256: "<malicious hash>"
  manifest_after:
    - file: ".claude/settings.json"
      sha256: "<clean hash post-restoration>"
ask:
  - Run intake recipe on the cleaned .claude/ directory
  - Regenerate .chain-manifest.json
  - Pin known-clean MCP server tool descriptions
```

### CULL_TO_GEAR_HARDEN

```yaml
from: Cull
to: Gear
trigger: post_eradication_harden
context:
  grade: CONFIRMED | ACTIVELY_BLEEDING
  affected_surfaces:
    - npm_runtime
    - github_actions
    - container_base_image
    - renovate_config
  hardening_recipe:
    - "ignore-scripts=true in .npmrc"
    - "min-release-age=7"
    - "GitHub Actions full-SHA pinning"
    - "OIDC over long-lived tokens"
    - "Registry proxy (Verdaccio / Artifactory / Takumi)"
    - "Renovate minimumReleaseAge: 7 days"
ask:
  - Apply hardening recipe to repo / org config
  - Verify CI/CD pipeline rebuild from clean base
  - Confirm secret-scanning + push-protection enabled
```

### CULL_TO_VIGIL_RULE_REQUEST

```yaml
from: Cull
to: Vigil
trigger: new_ioc_signature_observed
context:
  campaign: "<name>"
  signatures:
    - type: filename | sha256 | process_cmdline | network_endpoint | git_log_pattern
      value: "<defanged>"
      source: "<advisory URL + date>"
  attack_chain:
    - tactic: "<MITRE ATT&CK tactic>"
      technique: "T<id>.<sub>"
      surface: "<endpoint | network | cloud | ci>"
ask:
  - Author Sigma rules per signature (Sigma v2.1+, attack.<tactic>.<sub> tagging)
  - Author YARA rules where file pattern matching applies (droplet sha256, distinctive strings)
  - Map to ATT&CK Detection Strategies (v18+)
  - Test with sample data; verify FP rate within Vigil thresholds
```

### CULL_TO_LORE_JOURNAL

```yaml
from: Cull
to: Lore
trigger: repeated_campaign_pattern | novel_persistence_surface | rotation_order_lesson
context:
  pattern_summary: "<short>"
  recurrence_count: <n>
  ecosystem_impact: "<which agents should change behavior>"
  proposed_metapattern:
    title: "<name>"
    description: "<why this matters across agents>"
    affected_agents: [Sentinel, Chain, Vigil, Cull]
ask:
  - Curate into METAPATTERNS.md
  - Propagate behavior change to listed agents
  - Schedule revisit when next campaign in family lands
```

---

## Handoff hygiene

- One handoff per outbound target. Do not stack `triage` + `sentinel` + `chain` into the same handoff block — emit three separate blocks.
- Every handoff references concrete artifacts (paths, sha256, log lines). No vague "investigate further" without an evidence anchor.
- Defang attacker URLs in handoffs (`https` → `hxxps`, `.com` → `[.]com`). Recipients will undefang as needed; the handoff file itself should not be a click-trap.
- Do not embed credential values in handoffs. Paths and existence flags only.
- When the partner agent does not exist in the current installation (e.g. `lore` not present), still emit the handoff block — it documents intent and the next maintainer can wire it.


---

## Collaboration Handoffs and Overlap Boundaries (SKILL.md excerpt)

Cull receives compromise reports from User, slopsquat/CVE escalations from Sentinel, skill-audit handoffs from Chain, PR pre-merge requests from Builder, git-history anomalies from Trail, and incident-IoC requests from Triage. Cull returns confirmed-incident handoffs to Triage, lockfile remediation to Sentinel, skill quarantine to Chain, CI/CD hardening to Gear, rule-authoring requests to Vigil, and campaign-pattern journals to Lore.

**Receives:** User (compromise reports), Sentinel (slopsquat escalations), Chain (skill-audit handoff), Builder (PR pre-merge scan), Trail (history anomaly), Triage (incident IoC sweep)
**Sends:** Triage (incident handoff), Sentinel (lockfile remediation), Chain (skill quarantine), Gear (CI/CD harden), Vigil (rule authoring), Lore (campaign journal)

| Direction | Handoff | Purpose |
|-----------|---------|---------|
| User → Cull | `USER_TO_CULL_REQUEST` | Live-environment scan, eradication, rotation, or hardening request |
| Sentinel → Cull | `SENTINEL_TO_CULL_HANDOFF` | Lockfile match needs live-environment IoC confirmation |
| Chain → Cull | `CHAIN_TO_CULL_HANDOFF` | Skill / MCP audit found IDE-hook implant signatures |
| Builder → Cull | `BUILDER_TO_CULL_PRESCAN` | PR diff includes suspicious lockfile / `optionalDependencies` / `prepare` script |
| Trail → Cull | `TRAIL_TO_CULL_HANDOFF` | Git history anomaly (unknown author, force-pushed tag) — cross-check with IoCs |
| Triage → Cull | `TRIAGE_TO_CULL_HANDOFF` | SEV1 incident requires IoC sweep of dev environment |
| Cull → Triage | `CULL_TO_TRIAGE_INCIDENT` | `CONFIRMED` / `ACTIVELY_BLEEDING` grade — incident escalation |
| Cull → Sentinel | `CULL_TO_SENTINEL_LOCKFILE` | Confirmed malicious version pin → ecosystem-wide upgrade plan |
| Cull → Chain | `CULL_TO_CHAIN_QUARANTINE` | Confirmed `.claude/` or `.vscode/` compromise → manifest regeneration |
| Cull → Gear | `CULL_TO_GEAR_HARDEN` | CI/CD runner rebuild, registry proxy, Renovate config harden |
| Cull → Vigil | `CULL_TO_VIGIL_RULE_REQUEST` | New IoC signature → Sigma/YARA rule authoring + ATT&CK mapping |
| Cull → Lore | `CULL_TO_LORE_JOURNAL` | Repeated campaign pattern → ecosystem knowledge |

### Overlap Boundaries

| Agent | Cull owns | They own |
|-------|-----------|----------|
| Sentinel | Live IoC match + eradication runbook | Static SAST, dependency CVE scan, slopsquat detection |
| Chain | Live-environment scan of `.claude/` / `.vscode/` artifacts | SKILL.md / MCP / plugin intake audit + `.chain-manifest.json` |
| Vigil | IoC database curation + ground-truth matching | Sigma/YARA rule authoring, MITRE ATT&CK mapping |
| Triage | Technical IoC sweep + eradication/rotation runbook | Incident command, SEV classification, stakeholder comms |
| Trail | IoC cross-check on suspicious commits | Git history archaeology, regression bisection |
| Mend | Eradication runbook authoring | Automated runbook execution for catalogued patterns |
| Gear | CI/CD harden recommendation (delivered as runbook) | CI/CD config implementation, container hardening |
