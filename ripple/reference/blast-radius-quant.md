# Blast Radius Quantification Reference

Purpose: Quantify the *production* blast radius of a proposed change — customer count, SLO error-budget burn, revenue at risk, region/AZ scope, tenant fan-out, and data classification. Produces an evidence-grounded SEV-tier mapping that translates code-level change impact into incident-severity language operators and leadership understand.

## Scope Boundary

- **ripple `blast-radius`**: Production-quantified impact — customers, revenue, SLO burn, scope, data class, SEV tier (this document).
- **ripple `impact` / `vertical` / `horizontal` (elsewhere)**: Code-level dependency tracing. Feed dependency counts into blast-radius quantification.
- **ripple `rollback-plan` (elsewhere)**: Reversibility contract. Blast radius informs rollback urgency (ToR target).
- **Beacon (elsewhere)**: SLO/SLI design and error-budget policy. Blast-radius quantification *consumes* the SLO/error-budget from Beacon.
- **Triage (elsewhere)**: Live incident scoping. Blast-radius here is *pre-change estimation*; Triage is *in-incident actual*.
- **Sentinel (elsewhere)**: Security blast radius (exploit reach). Coordinate when change touches auth/PII/payment paths.

## Workflow

```
SCOPE      →  confirm change target + dependency count (from `impact`)
           →  identify surfaces: API, worker, DB, cache, queue, UI

CUSTOMERS  →  count active customers / users through affected surface
           →  segment by plan tier (enterprise / paid / free)
           →  flag if any one tenant > 5% of traffic (Noisy Neighbor risk)

REVENUE    →  compute revenue-at-risk (MRR through surface × downtime window)
           →  pair with SLA contract obligations (% uptime commitments)

SLO BURN   →  map to error-budget burn rate
           →  e.g., 1% of month's budget = SEV3 threshold

REGION/AZ  →  single-AZ / multi-AZ / multi-region
           →  mark blast floor (minimum recoverable scope)

TENANT     →  multi-tenant fan-out factor
           →  RLS/isolation verification (defers to shard)

DATA CLASS →  PII / PHI / financial / IP / internal
           →  activate compliance blast overlay (GDPR/HIPAA/PCI)

SEV MAP    →  combine dimensions → SEV1/SEV2/SEV3/SEV4
           →  emit escalation triggers
```

## Blast Dimensions

| Dimension | Measure | Data Source |
|-----------|---------|-------------|
| Customer count | # active accounts through the affected surface in last 28 days | analytics warehouse / billing DB |
| User count | # DAU / MAU reaching the affected code path | product analytics |
| Revenue at risk | MRR × (expected downtime minutes / month minutes) | billing DB × on-call history |
| SLA commitment | contractual uptime % (99.9 / 99.95 / 99.99) | sales / legal |
| Error budget | remaining minutes in current window | Beacon SLO dashboard |
| Region scope | single-AZ / multi-AZ / multi-region | infra registry |
| Tenant fan-out | % of tenants touched + largest-tenant share | tenant routing table |
| Data classification | PII / PHI / Financial / IP / Internal | data catalog |
| Dependent services | # downstream services consuming the surface | service catalog / Atlas output |
| AI-assisted | yes/no (elevated scrutiny per Amazon 2026) | PR metadata |

## Customer and Revenue Formula

```
Customers Affected       = distinct_accounts(events ∋ affected_endpoint, last 28d)
Revenue at Risk (monthly)= Σ MRR(customer) for customers_affected
Expected Impact ($)      = Revenue_at_Risk × (expected_downtime_min / 43200)
                           (43200 = minutes/month)
SLA Breach Risk          = YES if expected_downtime_min > monthly_budget
                           e.g., 99.9% budget = 43.2 min/month
```

## SEV Tier Mapping

| SEV | Condition | On-call Response | Examples |
|-----|-----------|------------------|----------|
| SEV1 | Customer-visible outage + >50% MAU or >25% revenue affected OR PII/PHI/Financial data at risk | Immediate page, exec notification, customer comms within 30 min | Payment processor down, auth system unavailable, PII leak |
| SEV2 | Major degradation + 10-50% MAU or top-tier enterprise tenant affected OR SLO burn > 2x budget | Page within 15 min, status page update | One region down, feature broken for paid tier |
| SEV3 | Partial degradation + < 10% MAU, no enterprise tenant, SLO burn within budget | Page during business hours, team-level comms | Secondary feature degraded, one AZ impaired |
| SEV4 | Minor issue, internal impact only, no customer-visible symptom | Ticket, no page | Internal dashboard broken, dev-only surface |

## Compliance Blast Overlay

When the change touches a classified data path, add compliance blast estimates:

| Classification | Regulation | Added Blast |
|---------------|-----------|-------------|
| PII (EU residents) | GDPR | Data breach notification obligation (72h), fine up to 4% global revenue or €20M |
| PII (CA residents) | CCPA/CPRA | Consumer notification, statutory damages $100-$750 per consumer |
| PII (JP residents) | APPI | PPC notification, 三層分類 handling |
| PHI | HIPAA | HHS breach notification, per-record penalties |
| Financial (PAN) | PCI-DSS | Card brand notification, forensic audit |
| Financial (SOX scope) | SOX | 10-K/10-Q disclosure impact |

Route compliance-impacting changes to Cloak and Comply for parallel review.

## Output Template

```markdown
## Blast Radius Report

### Change Summary
- **Target**: [file paths / API surface]
- **Type**: [schema / API / worker / UI / infra]
- **Deploy surface**: [production / staging / preview]

### Quantified Blast

| Dimension | Value | Source |
|-----------|-------|--------|
| Customers affected | [N] | [source] |
| % of MAU | [X%] | product analytics |
| Revenue at risk (mo) | $[X] | billing |
| Top-tier tenants affected | [list] | CRM |
| Region scope | [AZ/region list] | infra registry |
| Tenant fan-out | [X% of tenants, largest X%] | tenant routing |
| Data classification | [PII/PHI/Financial/IP/Internal] | data catalog |
| Dependent services | [list] | service catalog |

### SLO Impact
- **Affected SLO**: [name, target %]
- **Remaining error budget**: [minutes / %]
- **Expected burn from this change**: [minutes / %]
- **Burn classification**: within / 2x / exhausted

### SEV Tier (Pre-Change Estimate)
- **Tier**: [SEV1 / SEV2 / SEV3 / SEV4]
- **Rationale**: [which dimensions drove the classification]
- **Escalation triggers**: [conditions under which tier escalates during rollout]

### Compliance Overlay
- **Regulations in scope**: [GDPR / CCPA / HIPAA / PCI-DSS / SOX / none]
- **Notification obligations**: [if incident]
- **Handoffs**: Cloak ([reason]), Comply ([reason])

### Recommended Mitigations
- [ ] Canary scope: [% traffic, tenant allowlist]
- [ ] Feature flag kill-switch: [flag name]
- [ ] Pre-deploy verification: [test matrix]
- [ ] Rollback plan: [see rollback-plan output]
- [ ] On-call pre-notification: [team, channel]
- [ ] Status page pre-draft: [yes / no]

### Handoff
- [ ] Builder / Guardian (implementation + PR strategy)
- [ ] Beacon (SLO guard / alert prepare)
- [ ] Triage (on-call brief for SEV1/2)
- [ ] Sentinel (security blast verify)
- [ ] Cloak / Comply (compliance overlay)
- [ ] Launch (rollout gating)
```

## Alert Integration

For changes classified SEV1/SEV2, set pre-deploy alerts in Beacon:

- **Latency SLO**: P95 > target × 1.5 → auto-rollback candidate
- **Error rate SLO**: 5xx > 1% over 5 min → auto-rollback candidate
- **Business KPI**: conversion drop ≥20% over 15 min → pause + investigate

## Deliverable Contract

When `blast-radius` completes, emit:

- **Quantified blast table** (all 10 dimensions populated or marked N/A with rationale).
- **SEV tier** with explicit dimensional rationale.
- **SLO error-budget burn estimate** (minutes, % of monthly).
- **Compliance overlay** (regulations, notification obligations, handoffs).
- **Recommended mitigations** (canary, feature flag, kill-switch, pre-deploy alerts).
- **Escalation triggers** (conditions that would bump tier during rollout).
- **Handoff targets**: Beacon (SLO), Triage (SEV1/2 brief), Sentinel (security), Cloak/Comply (data class), Launch (rollout gating).

## References

- Google SRE — Embracing Risk & Error Budgets
- Amazon 2026 — Mandatory engineering meeting on high-blast-radius AI-assisted changes
- OWASP 2026 — Top 10 for Agentic Applications (blast radius for agentic systems)
- Site Reliability Workbook — Incident severity tiers
- PagerDuty Incident Severity Levels Handbook
- GDPR Art. 33/34 — Data breach notification
- HIPAA Breach Notification Rule (45 CFR §§ 164.400-414)
