# DAST Anti-Patterns

Purpose: Use this file when scan noise is high, DAST coverage is weak, or you need a triage model for false positives and proof-based validation.

## Contents

- `DA-01..DA-08`
- False-positive causes
- Proof-Based Scanning
- `L1..L4` triage
- Quality gates

## DAST Anti-Patterns

| ID | Anti-pattern | Risk | Required correction |
| --- | --- | --- | --- |
| `DA-01` | Ignore false positives | Alert fatigue and trust collapse | Use proof-based scanning and explicit triage |
| `DA-02` | Run full scans on every commit | Pipeline slowdown and skipped scans | Use diff-based CI scans and nightly full scans |
| `DA-03` | Scan without auth context | Shallow or misleading coverage | Manage auth/session safely and test protected paths |
| `DA-04` | Trust tool defaults | Framework-safe behavior becomes noise | Tune rules per app and framework |
| `DA-05` | Rely on automation only | Business logic flaws stay invisible | Pair automated and manual testing |
| `DA-06` | Scan production directly | Service disruption and data risk | Use staging/pre-production; production passive only |
| `DA-07` | Ignore business context | Bad prioritization | Use CVSS + asset value + exploitability |
| `DA-08` | Provide no developer feedback loop | Repeat findings and slow remediation | Send actionable feedback and ticket linkage |

## Common False-Positive Causes

| Cause | Example |
| --- | --- |
| Pattern matching without context | Reflected input flagged as XSS despite framework escaping |
| Missing app context | WAF block or business rule interpreted as a vuln |
| Broken auth/session setup | Scanner misses protected flows and produces shallow results |
| Dynamic rendering gaps | SPA routes or async content appear as false issues |

## Proof-Based Scanning

Proof-Based Scanning means reporting only after safe exploitability evidence exists.

- SQLi: prefer timing or harmless markers
- XSS: use inert markers where possible
- Command injection: use harmless echo markers
- Path traversal: read-only known files only

If safe proof is impossible in the allowed environment, label the issue `Needs Review` instead of confirmed.

## Four-Stage Triage Model

| Level | Method | Use when |
| --- | --- | --- |
| `L1` | Automatic known-false-positive filtering | Repeated, proven noise patterns |
| `L2` | Cross-tool correlation | DAST should be compared with SAST/IAST or logs |
| `L3` | ML or historical classification | Mature pipeline with triage history |
| `L4` | Manual security review | High-risk or ambiguous cases |

## Quality Gates

| Condition | Required action |
| --- | --- |
| False positive rate `> 30%` | Tune rules before broad rollout |
| Full scan in CI `> 30 min` | Shift to diff or scheduled scan |
| Authless scan only | Warn and request authenticated coverage |
| Automated scan only | Require manual test coverage for business logic |
| Production active scan requested | Ask first; default to passive only |
