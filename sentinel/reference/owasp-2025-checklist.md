# OWASP Top 10 (2025) Checklist & Audit Templates

Purpose: Map Sentinel findings to OWASP Top 10 (2025), run checklist-driven audits, and produce consistent security reports.

---

## OWASP Top 10 (2025) Overview

| Rank | Category | Change from 2021 | CWEs |
|------|----------|------------------|------|
| `A01` | Broken Access Control | Kept #1; SSRF folded in | 37 |
| `A02` | Security Misconfiguration | Moved up from #5 | 11 |
| `A03` | Software Supply Chain Failures | **New** (expands A06:2021 Vulnerable Components) | 5 |
| `A04` | Cryptographic Failures | Moved down from #2 | 11 |
| `A05` | Injection | Moved down from #3; Prompt Injection added | 7 |
| `A06` | Insecure Design | Moved down from #4 | 14 |
| `A07` | Authentication Failures | Kept #7 | 10 |
| `A08` | Software or Data Integrity Failures | Kept #8 | 6 |
| `A09` | Logging & Alerting Failures | Renamed from Monitoring | 4 |
| `A10` | Mishandling of Exceptional Conditions | **New** (24 CWEs) | 24 |

Key methodology change: 589 CWEs analyzed (up from ~400 in 2021). Focus on root causes over symptoms.

---

## Category Checklist

| Category | What to check |
|----------|---------------|
| `A01 Broken Access Control` | Deny-by-default authz, ownership checks (BOLA), IDOR, SSRF allowlists, internal IP blocking, CORS policy |
| `A02 Security Misconfiguration` | Security headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options), no stack traces, debug disabled, cloud hardening, default credentials |
| `A03 Supply Chain Failures` | SBOM (SPDX/CycloneDX), transitive CVEs, unused packages, CI/CD security (SHA-pinned actions), artifact signatures, lockfile integrity, slopsquatting |
| `A04 Cryptographic Failures` | Encryption at rest/in transit, TLS 1.2+, strong password hashing (bcrypt/argon2), no MD5/SHA1, safe key management |
| `A05 Injection` | Parameterized SQL, output encoding, command/LDAP/NoSQL/XSS protection, prompt injection review for AI features |
| `A06 Insecure Design` | Threat modeling, secure design patterns, resource-abuse prevention, rate limits on expensive operations |
| `A07 Authentication Failures` | MFA support, brute-force protection, secure recovery, safe session management, credential stuffing defense |
| `A08 Software or Data Integrity Failures` | CI/CD protection, code signing, dependency integrity, deserialization validation |
| `A09 Logging & Alerting Failures` | Auth failure logging, tamper resistance, alerting on suspicious activity, no secrets in logs |
| `A10 Exceptional Conditions` | Empty catch blocks, sensitive error leaks (CWE-209), fail-open (CWE-636), unhandled rejections, unsafe null access, resource leaks |

---

## Security Audit Report Template

### Executive Summary

| Metric | Value |
|--------|-------|
| Scan Date | `YYYY-MM-DD` |
| Files Scanned | `X` |
| Critical / High / Medium / Low | `X / X / X / X` |
| OWASP 2025 Coverage | `X/10` |

### Finding Template

```markdown
#### [SEVERITY-NNN] Finding Title
- **File**: `src/path/file.js:42`
- **OWASP 2025**: A0X - Category Name
- **Risk**: Impact if exploited
- **Evidence**: `code snippet showing the issue`
- **Remediation**: Exact fix or mitigation
- **Status**: Open / In Progress / Fixed
```

### Recommendation Cadence

1. `Immediate`: fix all CRITICAL and HIGH
2. `Short-term`: update vulnerable dependencies and harden configs
3. `Long-term`: integrate security checks into CI/CD

---

## 2021 → 2025 Migration

| 2021 | 2025 | Note |
|------|------|------|
| A01 Broken Access Control | A01 | SSRF integrated |
| A02 Cryptographic Failures | A04 | Lower rank |
| A03 Injection | A05 | Prompt Injection added |
| A04 Insecure Design | A06 | Lower rank |
| A05 Security Misconfiguration | A02 | Cloud misconfigs emphasized; highest frequency |
| A06 Vulnerable Components | A03 | Expanded to full supply chain |
| A09 Logging & Monitoring | A09 | Renamed to Logging & Alerting |
| A10 SSRF | folded into A01 | No longer standalone |
| (none) | A10 Exceptional Conditions | New: 24 CWEs covering error handling and resilience |

---

## Sentinel Scan Mapping

| Sentinel scan area | OWASP 2025 | Notes |
|--------------------|------------|-------|
| Secret detection | A07 | Credential and auth failure surface |
| SQLi / XSS / command injection | A05 | Includes prompt injection for AI systems |
| Input validation | A05 + A10 | Injection plus exceptional-condition safety |
| Security headers | A02 | Includes CSP, HSTS |
| Dependency CVEs and SBOM | A03 | Full supply-chain scope including CI/CD |
| Error handling and resource leaks | A10 | Newly emphasized in 2025 |
| Access control / BOLA | A01 | Ownership checks, SSRF |
| Cryptographic weakness | A04 | Hashing, TLS, key management |

**Source:** [OWASP Top 10:2025](https://owasp.org/Top10/2025/) · [OWASP A01:2025 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) · [OWASP A03:2025 Supply Chain](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/) · [OWASP A10:2025 Exceptional Conditions](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/) · [Fastly: OWASP 2025 Changes](https://www.fastly.com/blog/new-2025-owasp-top-10-list-what-changed-what-you-need-to-know) · [GitLab: OWASP 2025 Analysis](https://about.gitlab.com/blog/2025-owasp-top-10-whats-changed-and-why-it-matters/)
