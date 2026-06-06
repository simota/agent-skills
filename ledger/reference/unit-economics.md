# Unit Economics Reference

Purpose: Attribute cloud cost per unit — per customer, per tenant, per transaction, per feature, per user, per request. Unit economics transforms "we spend $X/month" into "we spend $Y per paying customer" — the basis for pricing, deal profitability, and product decisions.

## Scope Boundary

- **ledger `unit-economics`**: Per-unit cost attribution (this document).
- **ledger `tagging` (elsewhere)**: Tag taxonomy that enables unit economics.
- **ledger `estimate` (elsewhere)**: Pre-change cost diff.
- **ledger `finops-framework` (elsewhere)**: Parent capability domain.
- **Helm (elsewhere)**: Business-level forecasting.
- **Pulse (elsewhere)**: KPI definitions that unit economics ties to.

## Why Unit Economics

Total cloud spend tells leadership little. Unit cost answers decisions:

| Question | Needs |
|----------|-------|
| Can we offer a Starter plan at $29? | Cost per customer |
| Is the Enterprise tier profitable? | Cost per enterprise tenant |
| Should we build feature X? | Expected cost per user of X |
| Is this traffic spike unprofitable? | Cost per request × margin |
| Are our free users a loss? | Cost per free user × future conversion |

## Core Equations

```
Gross Margin = (Revenue − COGS) / Revenue
Contribution Margin = (Revenue − Variable Costs) / Revenue
LTV = ARPU × Gross Margin × (1 / Churn)
LTV / CAC = Lifetime Value / Customer Acquisition Cost
Payback Period = CAC / (ARPU × Gross Margin per month)
```

### Cost per unit

```
Cost per unit = Σ (attributable cloud cost) / (unit count in period)
```

Attribution is the hard part.

## COGS Decomposition for SaaS

| Category | Typical % of revenue | Notes |
|----------|----------------------|-------|
| Compute | 5-15% | EC2/Lambda/Kubernetes |
| Storage | 2-5% | S3/EBS/database storage |
| Data transfer | 2-8% | Egress; varies heavily by product |
| Databases | 3-8% | RDS/Aurora/managed DB |
| Third-party APIs | 1-10% | Stripe, Auth0, Twilio, OpenAI |
| Observability | 1-3% | Datadog, Sentry, logs |
| CDN | 1-3% | Cloudflare, Fastly, CloudFront |
| Support | 5-15% | Human cost bundled with COGS in SaaS |
| AI / ML inference | 0-30% | Highly variable; emerging category |
| **Total COGS** | **20-40%** | For healthy SaaS gross margin 60-80% |

## Attribution Techniques

### Direct attribution

Costs that belong to one unit:
- Dedicated instance per tenant.
- Per-tenant database cluster.
- Per-user AI API call cost.

Tag at source; read from Cost-and-Usage-Report.

### Proportional attribution

Costs shared across units; split by usage:
- Shared Kubernetes cluster → split by pod-hours per tenant.
- Shared database → split by row count or query count per tenant.
- Shared S3 bucket → split by bytes-read per tenant.

Requires usage metrics per tenant (Pulse).

### Unattributable (shared fixed)

Platform costs that don't split per unit:
- CI/CD infrastructure.
- Internal tools.
- Corporate IT.

Treat as overhead / fixed cost; don't force into unit economics.

### Kubernetes-specific

Tools: OpenCost (CNCF), Kubecost, StormForge. Attribution via:
- Pod-level resource requests × price.
- Workload labels → team / tenant.
- Namespace → team boundary.

## Unit Types

### Per-customer

Granularity: individual paying customer.
Use for: pricing decisions, deal-profitability analysis.

### Per-tenant (B2B SaaS)

Granularity: org account.
Use for: enterprise contract renegotiation, tenant migration decisions.

### Per-transaction

Granularity: payment / order / message / API call.
Use for: variable-cost pricing, margin per transaction.

### Per-feature

Granularity: feature use.
Use for: feature kill/keep decisions, AI feature profitability.

### Per-user

Granularity: active user (paid or free).
Use for: free-tier sustainability, freemium conversion economics.

## Fixed vs Variable Cost Classification

| Cost type | Grows with usage? | Examples |
|-----------|--------------------|----------|
| Variable | Yes | Serverless compute, per-request AI calls, data egress |
| Semi-variable | Stepwise | RI-covered compute (fixed within cap), managed DB with read replicas |
| Fixed | No | Control-plane, admin portal, internal tooling |

Contribution margin = (Revenue − Variable costs) / Revenue. Contribution margin > 0 is the minimum viability bar for a new tier or feature.

## Benchmark Ranges (SaaS, 2024)

| Metric | Healthy | Warning | Bad |
|--------|---------|---------|-----|
| Gross margin | 70-85% | 55-70% | < 55% |
| CAC payback | 6-12 mo | 12-24 mo | > 24 mo |
| LTV / CAC | ≥ 3 | 1.5-3 | < 1.5 |
| Magic number | ≥ 1 | 0.5-1 | < 0.5 |
| Net revenue retention | ≥ 110% | 90-110% | < 90% |

Unit-economics FinOps usually focuses on improving gross margin (reducing COGS) without harming the other metrics.

## Workflow

```
DEFINE      →  unit type (customer / tenant / transaction / feature / user)
            →  period (monthly / quarterly)

ATTRIBUTE   →  direct costs (tags required)
            →  proportional costs (usage-based split)
            →  unattributable fixed costs (overhead bucket)

COMPUTE     →  total attributed cost per unit
            →  revenue per unit (from finance / Pulse)
            →  gross margin per unit
            →  contribution margin per unit

SEGMENT     →  by plan tier (Free / Pro / Enterprise)
            →  by cohort (by signup quarter)
            →  by geography

IDENTIFY    →  unprofitable segments (contribution < 0)
            →  high-cost outliers (whale users)
            →  feature-level unprofitability

RECOMMEND   →  pricing adjustments
            →  optimization targets (where to reduce COGS)
            →  kill-candidates (features / tiers below contribution margin)

HANDOFF     →  Helm: business-level forecast
            →  Pulse: usage metrics required
            →  Launch: pricing changes
            →  Tagging: missing tags for better attribution
```

## Output Template

```markdown
## Unit Economics: [Product / Segment]

### Definition
- **Unit type**: [customer / tenant / transaction / feature / user]
- **Period**: [month / quarter]
- **Revenue source**: [finance / billing system]

### COGS Decomposition
| Category | $ per unit | % of cost | Trend |
|----------|-----------|-----------|-------|
| Compute | [...] | [...] | [...] |
| Storage | [...] | [...] | [...] |
| Data transfer | [...] | [...] | [...] |
| Databases | [...] | [...] | [...] |
| Third-party | [...] | [...] | [...] |
| Observability | [...] | [...] | [...] |
| CDN | [...] | [...] | [...] |
| Support | [...] | [...] | [...] |
| AI/ML | [...] | [...] | [...] |
| **Total** | [$N] | 100% | — |

### Margin
- **Revenue per unit**: [$N]
- **Gross margin**: [%]
- **Contribution margin**: [%]
- **Benchmark comparison**: [healthy / warning / bad]

### Segment Breakdown
| Segment | Unit cost | Revenue | Gross margin |
|---------|-----------|---------|--------------|
| Free | [...] | [0] | negative (expected) |
| Pro | [...] | [...] | [...] |
| Enterprise | [...] | [...] | [...] |

### Outliers
- **Top 5% costliest customers**: [what they cost, what they pay]
- **Unprofitable segment**: [segment, reason]
- **Feature-level unprofitability**: [feature, contribution]

### Recommendations
- Pricing: [adjustments]
- COGS reduction targets: [categories]
- Kill / unbundle: [features / tiers]

### Attribution Gaps
- Untagged cost: [%]
- Needed tags: [list → handoff to `tagging`]

### Handoffs
- Helm: business forecast update
- Pulse: usage metrics required
- Launch: pricing change rollout
- Tagging: coverage gaps
- Scribe: investor-deck-ready summary
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Average cost without segmentation | Whales + freeloaders average out; segment |
| Ignoring fixed costs entirely | Include overhead; report both gross and contribution |
| Shared-cost allocation by account count (not usage) | Use usage-based split |
| No AI cost category | AI is now often the largest COGS line; track it |
| Monthly unit cost without trend | Track trend; COGS drifts |
| Unit economics ignored during pricing | Pricing without unit cost = flying blind |
| Free tier economics ignored | Free can be >30% of total cost; must model conversion |
| Egress underestimated | Egress surprises; measure per-tenant explicitly |
| Support cost excluded | SaaS COGS includes human support; include it |
| Tagging coverage below 80%, report anyway | Refuse; unreliable |

## Deliverable Contract

When `unit-economics` completes, emit:

- **Unit type definition** + period.
- **COGS decomposition** (9 categories).
- **Margin metrics** (gross + contribution) vs benchmarks.
- **Segment breakdown** (plan tier, cohort, geo).
- **Outlier identification** (whales, unprofitable segments, features).
- **Recommendations** (pricing, reduction targets, kill-candidates).
- **Attribution gaps** report.
- **Handoffs**: Helm, Pulse, Launch, Tagging, Scribe.

## References

- FinOps Foundation — Unit Economics capability (2024 framework)
- *Cloud FinOps* (Storment & Fuller, 2nd ed, O'Reilly)
- SaaS CFO / Benchmarkit — SaaS benchmark reports
- KeyBanc Capital — *SaaS Survey* (annual)
- OpenCost — CNCF project for Kubernetes cost allocation
- Kubecost — commercial Kubernetes unit economics
- AWS Well-Architected Cost Pillar
- Azure Well-Architected Cost Optimization
- Google Cloud FinOps best practices
- David Skok — SaaS unit economics primer
- SaaStr — content library on unit-economics for SaaS leaders
