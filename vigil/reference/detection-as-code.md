# Detection-as-Code Reference

**Purpose:** CI/CD pipeline design for detection rule lifecycle management.
**Read when:** Designing automated detection rule testing, linting, and deployment.

---

## Detection-as-Code Principles

1. **Version control** — All detection rules live in Git, not in SIEM UI
2. **Code review** — Detection rule changes go through PR review
3. **Automated testing** — Syntax, true positive, and false positive tests run on every PR
4. **Staged deployment** — Rules deploy to staging before production
5. **Observability** — Track rule performance (fire rate, FP rate, MTTD)
6. **Supply-chain hardening** — Treat the DaC pipeline as production infrastructure. A compromised pipeline can push attacker-controlled rules that silently blind the SOC.
7. **Adversary-emulation tests are non-negotiable** — Every Sigma / YARA rule pairs with an **Atomic Red Team** (or equivalent) procedure that maps to the same ATT&CK technique. A rule with no emulation test is a hypothesis, not a detection.

## Engine Snapshot (2026-05)

| Engine | Status | Use it when |
|--------|--------|-------------|
| **YARA-X** (Rust rewrite, VirusTotal) | `1.0.0` stable since 2025-06; powers VirusTotal Livehunt / Retrohunt at billions-of-files scale; ~`99%` rule compatibility with classic YARA; heavy rules (large regex, deep loops) run seconds faster | New rule authoring, threat hunting pipelines, any project that can afford a one-time migration |
| **YARA 4.x** (classic, C) | Maintenance mode — only bug fixes land here; new features go exclusively to YARA-X | Legacy pipelines that have not yet migrated; budget the YARA-X migration |
| **Sigma** (SigmaHQ) | Active; the de-facto vendor-agnostic log-detection format. Compile to Splunk SPL / Elastic ES|QL / Sentinel KQL / Sumo / etc. via `sigma-cli` | First-class authoring for log-based detections; all rules in this repo start as Sigma |
| **Snort 3 / Suricata 7** | Active; network-traffic detection. See `snort-network-detection.md` | Packet-level signatures, IDS / IPS rules |

### Pipeline Supply-Chain Controls (GitHub Actions 2026 baseline)

| Control | Rule | Why |
|---------|------|-----|
| Action pinning | Pin every third-party action to a **full commit SHA**, not a branch or mutable tag | Tag/branch refs can be retargeted by the action owner or an attacker with repo write; SHA is immutable |
| Cloud auth | Use **OIDC** (`permissions: id-token: write`) to exchange a short-lived token for cloud credentials; never store long-lived secrets | Leaked OIDC tokens expire in minutes; leaked static secrets live until rotated |
| Least privilege | Set `permissions:` at the **job level** (default `contents: read`); grant extra scopes only to the job that needs them | Limits blast radius of a compromised step |
| Untrusted code | Never combine `pull_request_target` with `actions/checkout` of the PR ref | That pattern executes attacker-controlled code with repo-write privileges |
| Secret protection | Enable push protection + secret scanning on the detection-rules repo | Blocks accidental secret commits before they land |
| Artifact integrity | Sign converted SIEM rule bundles with Sigstore/Cosign; verify signatures at deploy time | Ensures rules deployed to production match what was PR-reviewed |

---

## Repository Structure

```
detection-rules/
├── sigma/
│   ├── endpoint/
│   │   ├── process_creation/
│   │   │   ├── det-001-powershell-encoded.yml
│   │   │   └── det-002-webshell-spawn.yml
│   │   └── file_event/
│   │       └── det-003-suspicious-dll.yml
│   ├── network/
│   │   └── det-010-dns-tunneling.yml
│   └── cloud/
│       └── det-020-iam-escalation.yml
├── yara/
│   └── malware/
│       └── det-100-cobalt-strike.yar
├── tests/
│   ├── true_positive/
│   │   ├── det-001-tp.json    # Known-bad log samples
│   │   └── det-002-tp.json
│   ├── false_positive/
│   │   ├── det-001-fp.json    # Known-benign log samples
│   │   └── det-002-fp.json
│   └── config.yml
├── coverage/
│   └── attack-coverage.md     # ATT&CK coverage map
├── .github/
│   └── workflows/
│       └── detection-ci.yml
└── README.md
```

---

## CI/CD Pipeline Template (GitHub Actions)

```yaml
name: Detection Rule CI/CD

on:
  pull_request:
    paths: ['sigma/**', 'yara/**']
  push:
    branches: [main]
    paths: ['sigma/**', 'yara/**']

permissions:
  contents: read   # default least-privilege for every job

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1 — pin to SHA, never @v4
      - name: Install sigma-cli
        run: pip install sigma-cli
      - name: Lint Sigma rules
        run: sigma check sigma/

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
      - name: True positive tests
        run: |
          for rule in sigma/**/*.yml; do
            sigma_id=$(basename "$rule" .yml)
            if [ -f "tests/true_positive/${sigma_id}-tp.json" ]; then
              sigma test "$rule" --input "tests/true_positive/${sigma_id}-tp.json"
            fi
          done
      - name: False positive tests
        run: |
          for rule in sigma/**/*.yml; do
            sigma_id=$(basename "$rule" .yml)
            if [ -f "tests/false_positive/${sigma_id}-fp.json" ]; then
              sigma test "$rule" --input "tests/false_positive/${sigma_id}-fp.json" --expect-no-match
            fi
          done

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      id-token: write   # OIDC: exchange for short-lived cloud creds
      contents: read
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
      - name: Convert to SIEM format
        run: sigma convert --target splunk sigma/ -o output/
      - name: Assume cloud role via OIDC
        uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502  # v4.0.2 — SHA-pinned
        with:
          role-to-assume: arn:aws:iam::123456789012:role/siem-deployer-staging
          aws-region: us-east-1
      - name: Deploy to staging SIEM
        run: echo "Deploy converted rules to staging"

  deploy-production:
    needs: deploy-staging
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment: production   # gated environment with required reviewers
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
      - name: Deploy to production SIEM
        run: echo "Deploy to production"
```

---

## Testing Strategy

### Test Data Format

```json
{
  "test_cases": [
    {
      "name": "True positive: PowerShell encoded command",
      "expected": "match",
      "log": {
        "EventID": 1,
        "Image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "CommandLine": "powershell.exe -enc SQBFAFgAIAAoA..."
      }
    }
  ]
}
```

### Test Types

| Type | When | Tool | Pass Criteria |
|------|------|------|---------------|
| Syntax lint | Every PR | sigma-cli check / `yara-x check` | No syntax errors |
| True positive | Every PR | sigma-cli test / `yara-x scan` | Rule matches known-bad data |
| False positive | Every PR | sigma-cli test / `yara-x scan` (negative) | Rule does NOT match known-benign data |
| Adversary emulation | Every PR | Atomic Red Team (`Invoke-AtomicTest`) on a sandbox host | Rule fires on the technique's simulated execution |
| Performance | Weekly | SIEM benchmark / `yara-x` regex-cost report | Rule executes within time budget |
| Coverage | Monthly | Custom script + MITRE Navigator | ATT&CK coverage meets target |

---

## Rule Lifecycle

```
DRAFT → REVIEW → TEST → STAGE → PRODUCTION → TUNE → RETIRE
```

| Phase | Owner | Criteria | Action |
|-------|-------|----------|--------|
| DRAFT | Detection engineer | Hypothesis or attack finding exists | Write rule + tests |
| REVIEW | Peer | PR approved, tests pass | Merge to main |
| TEST | CI/CD | All automated tests pass | Auto-deploy to staging |
| STAGE | SOC team | 7-day staging observation | Monitor FP rate |
| PRODUCTION | Release manager | FP rate < threshold | Tag release |
| TUNE | Detection engineer | FP rate exceeds threshold | Adjust conditions |
| RETIRE | Detection engineer | Rule is obsolete or superseded | Archive with reason |

---

## Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Detection coverage | >60% of applicable ATT&CK techniques | Automated coverage map |
| False positive rate | <5% per rule | FP / (TP + FP) |
| Mean time to detect (MTTD) | <1 hour for critical | Time from attack to alert |
| Rule deployment time | <24 hours from merge | Git to SIEM lag |
| Rule test coverage | 100% of production rules | Rules with TP/FP tests |
