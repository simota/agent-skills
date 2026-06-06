# Handoff Templates

**Purpose:** Canonical handoff blocks between Cull and partner agents.
**Read when:** Producing inbound / outbound handoff sections in a Cull report.

All handoffs follow `_common/HANDOFF.md` canonical schema. The fields below are the Cull-specific surfaces.

---

## Inbound

### USER_TO_HUSK_REQUEST

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

### SENTINEL_TO_HUSK_HANDOFF

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

### CHAIN_TO_HUSK_HANDOFF

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

### BUILDER_TO_HUSK_PRESCAN

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

### TRAIL_TO_HUSK_HANDOFF

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

### TRIAGE_TO_HUSK_HANDOFF

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

### HUSK_TO_TRIAGE_INCIDENT

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
        quarantine_path: "/tmp/husk-quarantine-<utc>/"
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

### HUSK_TO_SENTINEL_LOCKFILE

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

### HUSK_TO_CHAIN_QUARANTINE

```yaml
from: Cull
to: Chain
trigger: confirmed_ide_hook_compromise
context:
  affected_skill_dirs:
    - "<repo>/.claude/"
    - "<repo>/.vscode/"
  quarantine_path: "/tmp/husk-quarantine-<utc>/"
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

### HUSK_TO_GEAR_HARDEN

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

### HUSK_TO_VIGIL_RULE_REQUEST

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

### HUSK_TO_LORE_JOURNAL

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
