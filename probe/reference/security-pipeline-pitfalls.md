# Security Pipeline Pitfalls

Purpose: Use this file when designing CI/CD security gates, staging scan placement, SARIF workflows, or DAST rollouts that developers will actually use.

## Contents

- `SP-01..SP-08`
- Stage placement
- Risk-based gating
- Pipeline KPIs
- Probe quality gates

## Security Pipeline Anti-Patterns

| ID | Anti-pattern | Risk | Correction |
| --- | --- | --- | --- |
| `SP-01` | Security theater | Nobody acts on results | Alert only on actionable findings with clear owners |
| `SP-02` | Pipeline blocker scans | Developers skip or disable checks | Keep PR gates lightweight, move full scans to schedule |
| `SP-03` | Alert flood | Alert fatigue and ignored risk | Severity-aware gates and false-positive tuning |
| `SP-04` | Security silo | Findings never reach developers | Integrate with PR comments, tickets, and team workflows |
| `SP-05` | Too many tools everywhere | Duplicate or conflicting results | Select tools by stage and correlate outputs |
| `SP-06` | Production-only testing | Fixes become expensive and risky | Shift left to staging, keep production passive |
| `SP-07` | Static gate rules | Context-free blocking | Use risk-based gating |
| `SP-08` | No pipeline health monitoring | Broken scans go unnoticed | Track completion, time, MTTR, and false positives |

## Recommended Stage Placement

| Stage | Tests | Time budget | Blocking rule |
| --- | --- | --- | --- |
| `PR/Commit` | SAST, secret scan, lint | `< 5 min` | Critical SAST only |
| `Build` | SCA, container scan | `< 10 min` | Known critical CVE |
| `Deploy to Staging` | Lightweight DAST, API tests | `< 15 min` | Confirmed `Critical` / `High` |
| `Scheduled staging` | Full DAST, auth tests | `60 min+` | Notify, do not auto-block |
| `Production` | Passive monitoring | Continuous | Alert only |

## Risk-Based Gating

Use context-aware blocking instead of severity-only blocking.

```text
risk_score = CVSS
           * exploitability_factor
           * asset_value_factor
```

Suggested factors:

- Proof-Based Confirmed: `1.5x`
- DAST + SAST confirmed: `1.3x`
- DAST only: `1.0x`
- SAST only: `0.7x`
- Payment/Auth asset: `1.5x`
- User data: `1.3x`
- Public content: `0.8x`

Suggested decisions:

- `> 12` -> `BLOCK`
- `8-12` -> `WARN`
- `< 8` -> `INFO`

## Pipeline KPIs

| KPI | Target |
| --- | --- |
| Scan completion rate | `> 95%` |
| False positive rate | `< 20%` |
| MTTR | `Critical < 24h`, `High < 7d` |
| PR scan time | `< 15 min` |
| Full scan time | `< 60 min` |
| Vulnerability recurrence | `< 10%` |

## Probe Quality Gates

| Condition | Required action |
| --- | --- |
| False positive rate `> 30%` | Tune rules before expanding rollout |
| PR-stage DAST `> 30 min` | Reduce scope or move to schedule |
| Scan completion rate `< 90%` | Fix pipeline health before trusting results |
| Results not delivered to developers | Add PR/ticket integration |
