# Data Inputs Reference — Helm

Purpose: Normalize raw business inputs, define minimum viable data, and handle missing information without hiding uncertainty.

## Contents

- Input tiers
- Minimum input schema
- Recommended and optional inputs
- Industry defaults
- Gap handling
- Handoff-ready input packaging

## Input Tiers

| Tier | Meaning | Accuracy impact |
|------|---------|-----------------|
| `Tier 1` | mandatory minimum | simulation cannot proceed without it |
| `Tier 2` | strongly recommended | materially improves accuracy |
| `Tier 3` | optional domain-specific input | improves targeted analyses |
| `Tier 4` | external defaults | usable with disclosure |

## Tier 1: Minimum Input Set

```yaml
financial_overview:
  current_mrr: "¥Xm"
  revenue_type: "SaaS|Product|Service|Mixed"
  growth_rate_ytd: "X%"
  gross_margin: "X%"
  operating_profit: "¥Xm or X%"
  cash_position: "¥Xm"
  monthly_burn: "¥Xm"
  primary_model: "SaaS|Transaction|Project|Product|Hybrid"
  customer_type: "B2B|B2C|Both"
  avg_contract_value: "¥X"

market_context:
  industry: "SaaS/HR|EC|FinTech|Healthcare|Manufacturing|..."
  target_market: "SMB|Mid-market|Enterprise|Consumer"
  geographic_scope: "Japan|APAC|Global"
  tam: "¥Xbn"
  market_growth_rate: "X%/year"
  competitive_position: "Leader|Challenger|Niche|Follower"

simulation_config:
  horizon: "SHORT|MID|LONG|ALL"
  priority_question: "string"
```

If the user gives a short verbal description, normalize it into this schema before modeling.

## Tier 2: Recommended Inputs

### KPI Data

```yaml
kpi_data:
  total_customers: X
  new_customers_per_month: X
  churn_rate_mrr: "X%"
  churn_rate_logo: "X%"
  nps: XX
  cac: "¥X"
  ltv: "¥X"
  ltv_cac_ratio: "X.X"
  payback_period: "X months"
  magic_number: "X.X"
  arpu: "¥X"
  expansion_revenue_rate: "X%"
```

### Competitive Intelligence

```yaml
competitive_intel:
  direct_competitors:
    - name: "Competitor A"
      estimated_revenue: "¥Xm"
      market_share: "X%"
      key_differentiators: ["...", "..."]
      recent_moves: "..."
  our_differentiation: "string"
  win_rate: "X%"
```

### Organization Data

```yaml
organization:
  headcount_total: X
  headcount_by_function:
    engineering: X
    sales: X
    marketing: X
    cs: X
    ga: X
  personnel_cost: "¥Xm/month"
  personnel_ratio: "X%"
  planned_hires_next_12m: X
  key_roles: ["...", "..."]
```

## Tier 3: Optional Inputs

- `ESG data` for long-horizon simulations
- `product_portfolio` for BCG and product allocation work
- `ma_exit_context` for M&A or exit analysis

## Tier 4: Default External Benchmarks

Use only when the user does not provide data, and always disclose the substitution.

| Input | Default (2026) | Source |
|------|---------|------|
| SaaS churn (classical B2B) | `1-2%/month` | Standard benchmark |
| SaaS churn (AI-native, <$250/mo ACV) | `3-7%/month` | m3ter / SaaS Mag 2026 — disclose AI-native flag |
| SaaS gross margin (classical) | `70-80%` | Standard benchmark |
| SaaS gross margin (AI-native) | `60-70%` | SFAI Labs 2026 disclosure tracker; Bessemer Shooting Stars ~60% |
| Japan IT market growth | `3-5%/year` | Standard benchmark |
| CAC payback (B2B SaaS) | `12-18 months` | Standard benchmark |
| LTV:CAC target | `3:1+` | Standard benchmark |
| SaaS Magic Number healthy line | `0.75+` | Standard benchmark |
| SaaS M&A revenue multiple | `5-8× ARR` (AI premium tier `1-3× higher` per Livmo 2026) | Standard benchmark + AI premium |
| Startup personnel-cost ratio | `60-70%` | Standard benchmark |
| Rule of 40 (public SaaS median) | `28%` (Q4 2025), only `~20%` clear 40 | Aventis Advisors 2026 |
| Seed median post-money | `$24M` (Q4 2025); AI seed `+42%` vs non-AI | Carta State of Pre-Seed Q1 2026 |

## Gap Handling

### Gap Severity

`CRITICAL`:
- revenue scale unknown
- industry or market unknown
- horizon not specified

`SIGNIFICANT`:
- churn unknown
- competition unknown
- cost structure unknown

`MINOR`:
- ESG missing
- M&A details missing
- product portfolio missing

### Action Rules

- `CRITICAL` -> trigger `ON_DATA_INSUFFICIENT` and ask first
- `SIGNIFICANT` -> proceed with industry defaults and disclose assumptions
- `MINOR` -> narrow scope and list the limitation in the output

### Disclosure Table

| Field | Assumed value | Reason | Replace later |
|------|----------------|--------|---------------|
| churn | `1.5%/month` | B2B SaaS median | `yes` |
| gross margin | `75%` | SaaS benchmark | `yes` |
| market growth | `8%/year` | market benchmark | `yes` |

## Handoff-Ready Packaging

Use the same normalized schema when ingesting `COMPETE_TO_HELM` or `PULSE_TO_HELM`. Convert unstructured inputs into Tier-based fields before simulation.
