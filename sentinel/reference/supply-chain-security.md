# Supply Chain Security & SCA

Purpose: Use this reference when scanning dependencies, lockfiles, SBOMs, CI/CD pipelines, or AI-recommended packages.

---

## 1. Threat Landscape (2025-2026)

- 70-90% of modern applications are composed of OSS components
- OWASP Top 10 (2025) elevates supply-chain risk to A03
- 512,847 malicious packages detected in 2024 (+156% YoY); 845,204 cumulative by Q2 2025
- Verizon DBIR 2025: 30% of breaches involved third-party components (2x increase)
- AI-recommended dependencies: 44-49% may have known CVEs
- 2026 expands beyond npm: **first organised cargo campaign** (5 malicious Rust crates, Feb 2026), Ruby+Go **sleeper attacks** (May 2026), and PyPI **`.pth` persistence** (LiteLLM, Mar 2026)

### Attack Vectors

| Vector | Method | Example |
|--------|--------|---------|
| Typosquatting | Similar package name | `lodash` → `lodahs` |
| Dependency Confusion | Public package matching internal name | 2021 Alex Birsan |
| **Slopsquatting** | Register AI-hallucinated package name | 19.7% of AI-suggested packages don't exist |
| Compromised Maintainer | Take over maintainer account | `event-stream` (2018), XZ Utils (2024) |
| Build System Attack | Inject into CI/CD | `tj-actions/changed-files` (2025) |
| Malicious Update | Hostile update from legitimate package | `ua-parser-js` |
| **Remote Dynamic Dependencies (RDD)** | `package.json` dependency declared as off-registry HTTP URL, fetched + executed at install | PhantomRaven 2nd–4th wave (2026) |
| **Sleeper packages** | Clean v1 publication, malicious successor version | BufferZoneCorp Ruby+Go (May 2026) |
| **`.pth` persistence (PyPI)** | Drop a `.pth` file into `site-packages/` that auto-runs on every Python process start | LiteLLM 1.82.8 (Mar 2026) |
| **`extconf.rb` exploitation (Ruby)** | Native-extension hook auto-runs at `gem install` | BufferZoneCorp gems (May 2026) |
| **CI-token + OIDC chain** | Steal CI token → extract GHA OIDC → propagate via new workflow files | Mini Shai-Hulud / SAP CAP (Apr 2026) |
| **Self-replicating worms** | Stolen maintainer token reused to publish from every dependency | Shai-Hulud v1/v2/3.0 |

### Key Incidents

**XZ Utils Backdoor (CVE-2024-3094):** Attacker ("Jia Tan") spent 3 years building trust as maintainer, embedded backdoor enabling RCE via OpenSSH. CVSS 10.0. Discovered by accident.

**tj-actions/changed-files (CVE-2025-30066):** Attacker compromised GitHub Action used by 23,000+ repos. Secrets (PATs, npm tokens, RSA keys) leaked to CI logs. Triggered via compromised `reviewdog/action-setup@v1`. CISA emergency alert issued.

**Shai-Hulud v1.0 (2025-09) / v2.0 (2025-11) / 3.0 "Golden Path" (late 2025–2026):** first self-replicating npm worm. v1 propagated through preinstall scripts in 500+ packages by stealing maintainer npm tokens; v2 escalated to 796 packages / 132M monthly downloads with destructive payloads; 3.0 removed the dead-man switch, strengthened obfuscation, and now invokes Bun runtime via `bun_installer.js` — treat any unexpected `bun` invocation during npm install as a high-signal IOC. [Source: stepsecurity.io; kodemsecurity.com — Golden Path]

**Mini Shai-Hulud / SAP CAP (2026-04-29, ~2h19m window):** 4 packages (`@cap-js/sqlite@2.2.2`, `@cap-js/postgres@2.2.2`, `@cap-js/db-service@2.10.1`, `mbt@1.2.48`) published via a `cloudmtabot` token stolen from CircleCI plus GitHub Actions OIDC token extraction; preinstall bootstrapped Bun → `setup.mjs` → `execution.js` exfiltrated to a public GitHub repo. IOCs: `.github/workflows/discussion.yaml`, self-hosted runner `SHA1HULUD`, commit message prefix `OhNoWhatsGoingOnWithGitHub:[Base64]`. [Source: stepsecurity.io — Mini Shai-Hulud]

**PhantomRaven 2nd-4th wave (2025-11 → 2026-02, disclosed 2026-03):** introduced **Remote Dynamic Dependencies** — `package.json` declares an HTTP URL outside the registry as a dependency, fetched and executed at install time. 88 packages confirmed, two C2 servers active during research; cumulative campaigns total 200+ packages. Block by rejecting non-registry HTTP URLs in any dependency field at install. [Source: endorlabs.com — Return of PhantomRaven; bleepingcomputer.com]

**LiteLLM PyPI 1.82.7-1.82.8 (2026-03-24, ~40 min before PyPI quarantine):** 1.82.8 shipped `litellm_init.pth` into `site-packages/`, auto-executing on every Python process start. Exfiltrated credentials with AES-256 + RSA-4096 to `models.litellm.cloud`. Stage 3 of the TeamPCP campaign chain (Trivy → Checkmarx → LiteLLM). Monthly downloads ≈ 95M. Audit `site-packages/*.pth` for unsigned auto-execution. [Source: securitylabs.datadoghq.com — LiteLLM TeamPCP]

**Malicious Rust crates (2026-02):** 5 typosquatted "time utility" crates (`chrono_anchor`, `dnp3times`, `time_calibrator`, `time_calibrators`, `time-sync`) — **first organised cargo campaign**. Both `build.rs` and runtime hooks scan `.env` and POST to C2. Mitigate with `cargo vet`, `cargo-deny`'s ban list, and sandboxed build.rs. [Source: socket.dev — 5 Malicious Rust Crates]

**CVE-2026-33056 cargo tar (2026-03):** malicious crates can rewrite permissions on arbitrary directories during extraction. Affects all Rust ≤ 1.94.0; patched in 1.94.1. crates.io added upload-side detection 2026-03-13. [Source: blog.rust-lang.org]

**PyTorch Lightning PyPI (2026-04-30):** `lightning` 2.6.2/2.6.3 (sonatype-2026-002817) modified `__init__.py` to spawn a background credential-collection process on import. Attacker re-published 2.6.3 minutes after the 2.6.2 flag, attempting to evade quarantine. Pin Python deps by hash and monitor `importlib` hooks. [Source: sonatype.com]

**BufferZoneCorp sleeper (Ruby + Go, 2026-05):** clean v1 publications flipped into malicious successors. Ruby side abuses `extconf.rb` (auto-run at `gem install`) to exfiltrate `~/.ssh/`, `~/.aws/credentials`, `~/.config/gh/hosts.yml`. Go side mutates `GITHUB_ENV` / `GOPROXY` / `go.sum`. Affected gems include `activesupport-logger`, `devise-jwt`; Go modules include `go-retryablehttp`, `grpc-client`, `config-loader`. Defenses: `bundle config disable_install_extensions`, `GOFLAGS=-mod=readonly`, registry-side sleeper-pattern detection. [Source: socket.dev — Malicious Ruby Gems and Go Modules; thehackernews.com]

**Trivy Docker Hub / GHCR campaign extension (2026-03):** TeamPCP attack chain extended across every distribution channel (Docker Hub `latest`, GHCR, ECR Public, deb/rpm, `get.trivy.dev`). C2 domain `scan.aquasecurtiy.org` (typosquat); activation gated on 27+ CI/CD env vars. Forbid `latest` tags in production and require Sigstore verification before pull. [Source: docker.com; microsoft.com]

**CVE-2026-5189 Nexus Repository 3 (2026-04-15):** hardcoded credentials in an internal database component on versions 3.0.0–3.70.5 — relevant when running internal registries. Patch to 3.70.6+ and enforce mTLS on internal registries. [Source: support.sonatype.com]

---

## 2. Slopsquatting (AI Package Hallucination)

Research (576,000 samples, 16 models):

| Metric | Value |
|--------|-------|
| Hallucination rate (all models) | 19.7% |
| Open-source models | 21.7% |
| Proprietary models | 5.2% |
| Unique hallucinated package names | 205,474 |
| Repeat across queries | 43% appear every time |

Defense: verify package existence before install, use lockfiles, run AI-suggested installs in isolated containers, integrate SCA into CI/CD.

---

## 3. SCA Tools

| Tool | Strength |
|------|----------|
| `Snyk` | Developer-friendly, auto-fix PRs |
| `Dependabot` | GitHub-native, low setup |
| `Socket` | Behavior analysis, zero-day detection (pre-CVE) |
| `Endor Labs` | Function-level reachability analysis, noise reduction |
| `OWASP Dependency-Check` | Language-agnostic NVD matching |
| `Trivy` | Filesystem, container, and IaC scanning |

Prioritization factors: CVSS + EPSS + runtime reachability + exploit maturity + network exposure.

---

## 4. SBOM Requirements

### Accepted Formats

- SPDX, CycloneDX, SWID

### CISA 2025 Minimum Elements (Updated)

- Software Producer, Component Name, Version
- Unique Identifiers (CPE, PURL, SWID)
- Dependency Relationship
- **Component Hash** (new requirement)
- **License Information** (new requirement)
- Tool Name, Generation Timestamp
- Known unknowns disclosure

### EU Cyber Resilience Act (CRA) — two-stage timeline

- **2026-09-11**: vulnerability reporting and incident notification obligations take effect. 24h Early warning + 72h Full notification via the ENISA Single Reporting Platform. SBOM and a vulnerability-management process must already be operational by this date to meet the reporting cadence, even though SBOM is not yet a free-standing legal requirement.
- **2027-12-11**: main obligations apply — machine-readable SBOM (CycloneDX or SPDX), lifecycle security, technical documentation, and CE marking.
- Coverage: at minimum top-level dependencies, with transitive depth recommended.
- Must be available for authority submission on request.
- [Source: digital-strategy.ec.europa.eu — CRA Reporting obligations](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting), [keysight.com — One-Year Countdown](https://www.keysight.com/blogs/en/tech/nwvs/2025/09/11/one-year-countdown-to-eu-cra-compliance-september-11-2026-changes-everything)

### Generation Commands

```bash
npx @cyclonedx/cyclonedx-npm > sbom.json    # CycloneDX (npm)
syft dir:. -o cyclonedx-json > sbom.json                          # Syft
trivy fs . --format cyclonedx --output sbom.json                  # Trivy
```

---

## 5. Package Provenance & Signing

### Sigstore Adoption (2024-2026)

| Ecosystem | Status |
|-----------|--------|
| npm | GA since 2023; `npm publish --provenance`. **Trusted Publishing GA 2025-07** (auto-provenance when used). |
| PyPI | Sigstore signing since 2024. Trusted Publishers: 13,000+ projects adopted (2025). |
| Homebrew | Sigstore since 2024 |
| Maven Central | Sigstore since 2025 |
| GitLab CI/CD (npm Trusted Publishing) | **GA 2026-01** |

**Cosign v3** is current: mandates TSA-signed timestamps, emits OCI 1.1 referrers bundle format, integrates with **Rekor v2 GA** (Trillian-Tessera tile-based log + Witness append-only guarantees). [Source: blog.sigstore.dev — Cosign v3, Rekor v2 GA]

### SLSA Framework v1.2

| Level | Guarantee |
|-------|-----------|
| L0 | No requirements |
| L1 | Provenance exists |
| L2 | Signed provenance from build service |
| L3 | Verified and hardened build platform |

**v1.2 (RC2)** is the current public spec target — restructured the Source Track L2/L3 and clarified Build isolation requirements (v1.0 and v1.1 are superseded). [Source: slsa.dev/spec/v1.2/whats-new]

**provenance-attestation gap (2026)**: sigstore-js → npm dependency coverage shows ~7.2% provenance attachment; poetry → PyPI shows ~32.7%. PyPI leads npm in attestation density — factor this into trust-model assumptions per ecosystem.

---

## 6. CI/CD Hardening

### Critical Rules (Post tj-actions Incident)

1. **SHA-pin all third-party actions** — tags are mutable and can be rewritten
   ```yaml
   uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29  # v4.2.2
   ```
2. **Use OIDC tokens** instead of static secrets for cloud auth
3. **Set `GITHUB_TOKEN` to `read-only`** default; grant write per-job
4. **Isolate untrusted code** (external PRs) in restricted environments

### CI Pipeline Template

```yaml
name: Supply Chain Security
on: [push, pull_request]

jobs:
  sca-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29
      - run: npm audit --audit-level=high
      - run: npx @cyclonedx/cyclonedx-npm > sbom.json
      - run: npm ci --ignore-scripts
      - run: npx license-checker --failOn "GPL-3.0;AGPL-3.0"
```

### Dependency Workflow

Required: commit lockfile, use `npm ci` in CI, review lockfile diffs.
Forbidden: ignoring lockfiles in git, non-deterministic installs in CI.

### Sentinel Checklist

- [ ] Run `npm audit` / `yarn audit` / `pnpm audit` / `pip-audit` / `cargo audit` / `bundle audit` / `govulncheck`
- [ ] Detect known CVEs with reachability context
- [ ] Flag unused packages
- [ ] Check lockfile existence and integrity
- [ ] Check private package names against public registries
- [ ] Inspect `postinstall` / `preinstall` scripts and `extconf.rb` (Ruby) and `build.rs` (Rust)
- [ ] Audit `site-packages/*.pth` for unsigned auto-execution (Python — LiteLLM .pth class)
- [ ] Reject non-registry HTTP URLs in any `dependencies` field (PhantomRaven RDD)
- [ ] Watch for unexpected `bun` invocation during `npm install` (Shai-Hulud 3.0 IOC)
- [ ] For sleeper-pattern detection, treat a "first malicious version after a clean v1" as a high-signal anomaly (BufferZoneCorp)
- [ ] Forbid `latest` container tags in production; require Sigstore verification before pull
- [ ] Review license compatibility
- [ ] Verify GitHub Actions are SHA-pinned

### Adjacent OWASP frameworks (load when relevant)

- **OWASP MCP Top 10 (2025)** — MCP04 Software Supply Chain Attacks & Dependency Tampering is the MCP-specific framework when auditing MCP servers / tool definitions. [Source: owasp.org/www-project-mcp-top-10]
- **OWASP Agentic Skills Top 10** — SKILL.md distribution channel threats; complements the `chain` agent in this repo. [Source: owasp.org/www-project-agentic-skills-top-10]
- **OWASP Top 10 for Agentic Applications (2026)** — ASI04 Agentic Supply Chain Vulnerabilities provides the application-side framework for agent dep / MCP / weight registry attacks. [Source: genai.owasp.org]

**Source:** [OWASP A03:2025 Supply Chain](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/) · [CISA 2025 SBOM Requirements](https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom) · [CISA tj-actions Alert](https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction) · [Socket Slopsquatting](https://socket.dev/blog/slopsquatting-how-ai-hallucinations-are-fueling-a-new-class-of-supply-chain-attacks) · [Sonatype Q2 2025 Malware Index](https://www.sonatype.com/press-releases/q2-2025-open-source-malware-index) · [SLSA v1.2 What's New](https://slsa.dev/spec/v1.2/whats-new) · [EU CRA Reporting](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting) · [Rekor v2 GA](https://blog.sigstore.dev/rekor-v2-ga/) · [Cosign v3](https://blog.sigstore.dev/cosign-3-0-available/) · [PhantomRaven](https://www.endorlabs.com/learn/return-of-phantomraven) · [Mini Shai-Hulud](https://www.stepsecurity.io/blog/a-mini-shai-hulud-has-appeared) · [Shai-Hulud 3.0 Golden Path](https://www.kodemsecurity.com/resources/guess-whos-back-shai-hulud-3-0-the-golden-path) · [LiteLLM TeamPCP](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/) · [Malicious Rust Crates](https://socket.dev/blog/5-malicious-rust-crates-posed-as-time-utilities-to-exfiltrate-env-files) · [BufferZoneCorp Ruby/Go](https://socket.dev/blog/malicious-ruby-gems-and-go-modules-steal-secrets-poison-ci) · [CVE-2026-33056 cargo tar](https://blog.rust-lang.org/2026/03/21/cve-2026-33056/) · [Trivy DH/GHCR](https://www.docker.com/blog/trivy-kics-and-the-shape-of-supply-chain-attacks-so-far-in-2026/) · [CVE-2026-5189 Nexus](https://support.sonatype.com/hc/en-us/articles/50817138825491-CVE-2026-5189-Nexus-Repository-3-Hardcoded-Credential-in-Internal-Database-Component-2026-04-15)
