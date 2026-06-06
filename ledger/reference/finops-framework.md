# FinOps Foundation Framework Reference

Purpose: Apply the FinOps Foundation's Framework (2024 edition) — the industry-standard maturity model for cloud financial management. Assess current state across capabilities, map personas to activities, and sequence phase-appropriate next moves (Crawl / Walk / Run).

## Scope Boundary

- **ledger `finops-framework`**: Maturity assessment + roadmap (this document).
- **ledger `estimate` / `rightsizing` / `anomaly` / `ri-sp` / `gpu-cost` / `tagging` (elsewhere)**: Individual capability execution.
- **ledger `unit-economics` (elsewhere)**: Per-unit cost attribution — a capability within Quantifying Business Value.
- **ledger `greenops` (elsewhere)**: Sustainability overlay to FinOps.
- **Comply (elsewhere)**: Compliance-focused cost audit.
- **Harvest (elsewhere)**: PR work reporting.

## Framework Structure

```
FinOps Framework
├── Domains (4)
│  ├── Understanding Usage & Cost
│  ├── Quantifying Business Value
│  ├── Optimizing Usage & Cost
│  └── Managing the FinOps Practice
├── Capabilities (22)
├── Maturity Phases (Crawl → Walk → Run)
├── Personas (Engineer / Finance / FinOps Practitioner / Procurement / Leadership / Product / ITAM / Sustainability)
└── Principles (6)
```

## 6 Principles

1. Teams need to collaborate.
2. Everyone takes ownership for their cloud usage.
3. A centralized team drives FinOps.
4. FinOps reports should be accessible and timely.
5. Decisions are driven by business value of cloud.
6. Take advantage of the variable cost model of the cloud.

## 4 Domains × 22 Capabilities

### Domain 1 — Understanding Usage & Cost

| Capability | Crawl | Walk | Run |
|-----------|-------|------|-----|
| Data Ingestion | CUR / Billing export basic | Normalized multi-cloud | FOCUS spec + governed pipeline |
| Allocation | Account-level | Cost-allocation tags enforced | Shared-cost split with algorithms |
| Reporting & Analytics | Basic dashboards | Self-service + forecast | Real-time + anomaly overlay |
| Anomaly Management | Ad-hoc | Rule-based alerts | ML-driven + auto-root-cause |
| Forecasting | Spreadsheet | Trend + seasonality | Probabilistic + scenario |

### Domain 2 — Quantifying Business Value

| Capability | Crawl | Walk | Run |
|-----------|-------|------|-----|
| Planning & Estimating | Pre-go-live IaC estimate | Pre-change impact standard | Integrated into CI/CD |
| Budgeting | Annual budget | Rolling forecast | Budget-as-code |
| Benchmarking | Internal trends | Industry peer | Anchor-to-business-metric |
| Unit Economics | Total cost / revenue | Per-tenant / per-txn | Per-feature / per-journey |
| FinOps for AI | Per-model token cost | Per-agent / per-task | Unit margin per AI feature |

### Domain 3 — Optimizing Usage & Cost

| Capability | Crawl | Walk | Run |
|-----------|-------|------|-----|
| Rate Optimization | Spot where obvious | Commitment strategy (RI/SP) | Automated commitment |
| Workload Optimization | Manual right-sizing | Scheduled + autoscale | Continuous + cross-service |
| Cloud Sustainability | Region choice | SCI tracking | Carbon-aware scheduling |
| Licensing & SaaS | Track licenses | Rationalize | Unified SaaS FinOps |

### Domain 4 — Managing the FinOps Practice

| Capability | Crawl | Walk | Run |
|-----------|-------|------|-----|
| FinOps Practice Operations | Part-time role | FinOps team | CoE + chapter |
| FinOps Assessment | Annual | Quarterly | Continuous |
| FinOps Education & Enablement | Wiki | Training program | FinOps certification path |
| Onboarding Workloads | Post-hoc | Template-driven | Policy-enforced |
| Chargeback & Invoicing | Showback by team | Chargeback with dispute | Chargeback + unit rates |
| Policy & Governance | Manual | Guardrail rules | Policy-as-code |
| Invoice Reconciliation | Manual | Automated | Continuous audit |
| Intersecting Frameworks | None | ITIL / ITFM aware | ITSM / SRE / Security integrated |

## Persona × Capability Map

| Persona | Primary capabilities |
|---------|---------------------|
| Engineer | Workload Optimization, Planning & Estimating, Anomaly Management |
| Finance | Budgeting, Chargeback, Invoice Reconciliation, Forecasting |
| FinOps Practitioner | All — owns orchestration |
| Procurement | Rate Optimization, Licensing |
| Leadership | Unit Economics, Benchmarking, Business Value |
| Product | Unit Economics, FinOps for AI, Planning |
| ITAM | Licensing & SaaS, Onboarding |
| Sustainability | Cloud Sustainability, overlap with Rate Optimization |

## Maturity Assessment Rubric

For each of the 22 capabilities, assign Crawl / Walk / Run:

- **Crawl**: ad-hoc, reactive, manual, low visibility.
- **Walk**: defined process, dashboards, periodic cadence.
- **Run**: automated, continuous, predictive, integrated into SDLC.

Average across capabilities gives organizational phase. Most orgs sit at Crawl-Walk blended; Running is rare and expensive.

## Sequencing Next Moves

Rule of thumb: advance your *weakest* capability within your *highest-leverage* domain — don't try to jump all at once.

| Phase | Typical first move |
|-------|-------------------|
| Crawl → Walk | Mandatory tagging + allocation to teams |
| Walk → Run | Anomaly ML + commitment automation |
| Any | Unit Economics (transforms cost conversation) |

## Workflow

```
ASSESS      →  score current state per capability (Crawl/Walk/Run)
            →  compute domain averages
            →  heat-map weakest vs highest-value

PERSONA     →  map active FinOps personas in org
            →  identify gaps (no FinOps Practitioner? Limit scope)

GAP         →  highest-value weak capabilities surface as priorities
            →  cross-check with business context (AI-heavy? → FinOps for AI)

ROADMAP     →  1-3 capabilities to advance per quarter
            →  Crawl → Walk per capability takes ~1-2 quarters
            →  Walk → Run takes ~2-4 quarters

HANDOFF     →  Scaffold: policy-as-code enforcement
            →  Beacon: FinOps dashboards
            →  Launch: integrate pre-change estimate
            →  Comply: chargeback governance
```

## Output Template

```markdown
## FinOps Maturity: [Org]

### Phase Summary
- **Overall**: Crawl / Walk / Run
- **Strongest domain**: [...]
- **Weakest domain**: [...]

### Capability Heat Map
| Domain | Capability | Current | Target | Gap |
|--------|-----------|---------|--------|-----|
| Understand | Data Ingestion | Crawl | Walk | +1 |
| ... | ... | ... | ... | ... |

### Persona Map
| Persona | Active? | Primary owner of... |
|---------|---------|---------------------|
| FinOps Practitioner | Yes/No | [capabilities] |
| ... | ... | ... |

### Roadmap (next 2 quarters)
| Capability | Current → Target | Primary owner | Dependencies |
|-----------|-----------------|---------------|--------------|
| ... | ... | ... | ... |

### Principles Scorecard
| Principle | Status |
|-----------|--------|
| Teams collaborate | ✓ / partial / ✗ |
| Everyone owns usage | ... |
| Centralized team | ... |
| Reports accessible | ... |
| Business-value decisions | ... |
| Variable cost model used | ... |

### Handoffs
- Scaffold: policy-as-code for next capability
- Beacon: FinOps dashboard design
- Launch: integrate estimate into release plan
- Comply: chargeback governance
- Architect: if org needs new FinOps role
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Trying to reach Run on everything at once | Pick 1-3 per quarter |
| FinOps Practitioner role not assigned | Crawl/Walk collapse without a named owner |
| No unit economics at Walk | Costs reported but never linked to business value |
| Showback without chargeback discipline | Teams ignore showback; no incentive |
| Running without Crawl prerequisites (e.g., auto-commitment without tagging) | Automation on bad data = bigger mistakes faster |
| Engineer-only focus | Missing Finance / Leadership alignment |
| Framework adopted as checklist, not practice | Capabilities must connect to real decisions |
| Ignoring SaaS FinOps | SaaS spend now rivals IaaS in many orgs |
| No sustainability capability | Regulatory + reputational risk |

## Deliverable Contract

When `finops-framework` completes, emit:

- **Phase summary** (overall + per domain).
- **Capability heat map** with current vs target.
- **Persona map** with owners assigned.
- **2-quarter roadmap** with 1-3 capability advances.
- **Principles scorecard**.
- **Handoffs**: Scaffold, Beacon, Launch, Comply, Architect.

## References

- FinOps Foundation — *FinOps Framework 2024* (finops.org/framework)
- FinOps Foundation — *State of FinOps* annual report
- FinOps Foundation — FOCUS (FinOps Open Cost and Usage Specification) v1.0
- O'Reilly — *Cloud FinOps* (Storment & Fuller, 2nd ed)
- FinOps X conference recordings
- CNCF — FinOps working group
- ITIL 4 — ITFM (IT Financial Management) crossover
- FinOps certified practitioner program
