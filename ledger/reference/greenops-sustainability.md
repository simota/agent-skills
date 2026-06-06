# GreenOps / Cloud Sustainability Reference

Purpose: Overlay carbon-awareness onto FinOps. Design architectures that account for embodied + operational CO2e, compute Software Carbon Intensity (SCI) per ISO/IEC 21031, choose low-carbon regions, schedule carbon-aware workloads, and navigate the FinOps × GreenOps trade-off.

## Scope Boundary

- **ledger `greenops`**: Sustainability capability (this document).
- **ledger `finops-framework` (elsewhere)**: Parent maturity framework — sustainability is one of 22 capabilities.
- **ledger `ri-sp` / `rightsizing` (elsewhere)**: Individual optimizations that overlap with GreenOps.
- **Scaffold (elsewhere)**: IaC execution of region choices.
- **Beacon (elsewhere)**: SCI dashboards and SLO-equivalents.
- **Comply (elsewhere)**: CSRD / SEC climate-disclosure reporting.

## Why GreenOps Now

- EU CSRD (effective 2024 onward) mandates Scope 1-3 carbon disclosure for large companies.
- SEC climate disclosure rules (US).
- Customer RFPs increasingly include sustainability criteria.
- Hyperscalers (AWS, Azure, GCP) publish customer-specific carbon dashboards.
- ISO/IEC 21031 — Software Carbon Intensity (SCI) published 2023.

FinOps teams are inheriting sustainability responsibility because the data flow is similar: billing → usage → attribution.

## Core Metric: SCI (ISO/IEC 21031)

```
SCI = ((E × I) + M) / R

E = Energy consumed (kWh)
I = Location-based carbon intensity (gCO2e/kWh)
M = Embodied emissions (gCO2e, amortized)
R = Functional unit (per request / per user / per transaction)
```

Key insight: SCI is normalized per functional unit, so it scales with your product model, not total cost. A 2x traffic spike at steady SCI means carbon grew linearly (not efficiency drop).

### Components

| Component | How to measure |
|-----------|----------------|
| E (energy) | Cloud provider tools — AWS CCFT, Azure Emissions Impact Dashboard, GCP Carbon Footprint |
| I (carbon intensity) | Region-specific grid carbon data — WattTime, Electricity Maps |
| M (embodied) | Hardware lifecycle CO2e amortized over use; provider-disclosed |
| R (functional unit) | Per request / DAU / transaction — from Pulse |

## Region Carbon Intensity (illustrative ranges, 2024)

| Region | Avg gCO2e/kWh | Notes |
|--------|----------------|-------|
| eu-north-1 (Stockholm) | ~10-30 | Mostly hydro + nuclear |
| ca-central-1 (Montreal) | ~30 | Mostly hydro |
| eu-west-1 (Ireland) | ~300-400 | Mixed gas |
| us-west-2 (Oregon) | ~300-400 | Mixed hydro + gas |
| ap-northeast-1 (Tokyo) | ~450-550 | Gas + coal |
| ap-southeast-1 (Singapore) | ~450 | Gas + LNG |
| us-east-1 (N. Virginia) | ~400-500 | Gas + nuclear + coal |
| ap-south-1 (Mumbai) | ~700-900 | Coal-heavy |

Numbers shift by year and provider investment. Always pull live data from provider dashboards.

## Five Sustainability Levers

### 1. Region selection (biggest single lever)

Move workloads to low-carbon regions. Caveats:
- Latency impact on users.
- Data sovereignty (GDPR / APPI).
- Cost differences (cheap regions aren't always green).
- Provider-specific constraints.

Typical win: 40-70% emissions reduction moving US-East-1 → EU-North-1 or CA-Central-1.

### 2. Carbon-aware scheduling

Run non-urgent workloads when/where grid is clean.

| Pattern | Mechanism |
|---------|-----------|
| Temporal shift | Delay batch jobs by 1-6 hours for cleaner grid window |
| Spatial shift | Route workload to region with cleaner grid now |
| Demand response | Scale down in peak-carbon hours |
| CI cadence | Schedule CI runs during off-peak carbon hours |

Tools: Google Carbon-Aware Compute, AWS scheduled actions, WattTime API, Carbon Aware SDK (Green Software Foundation).

### 3. Right-sizing + efficiency

Fewer idle resources = less embodied + operational. Overlaps with `rightsizing`.
- Serverless > always-on VMs for bursty workloads.
- Efficient languages / runtimes (Rust / Go > Python / Ruby in hot path).
- Smaller container images = faster cold starts, less storage.

### 4. Hardware efficiency

- ARM (Graviton / Cobalt / Axion) → 30-60% better perf/watt than x86.
- Latest-gen instances are usually more efficient (m7g > m6g > m5).
- GPU right-sizing for AI workloads (use L40S instead of H100 for inference).

### 5. Storage class tiering

- Cold data → Glacier / Archive (lower embodied cost).
- Lifecycle policies to auto-tier.
- Dedup (see spider `dedup`) reduces storage footprint.

## FinOps × GreenOps Trade-off Matrix

Usually aligned (right-sizing saves $ and CO2e). Sometimes conflict.

| Scenario | FinOps says | GreenOps says | Resolution |
|----------|-------------|---------------|------------|
| Spot + interrupt-tolerant | Use spot for 60-80% discount | Spot is often clean-grid | Aligned |
| Temporal shift to off-peak | Can cost more (weekend rates) | Grid often cleaner off-peak | Modest conflict |
| Move to low-carbon region | May cost more | Large win | Depends on product |
| ARM migration | 20-40% cheaper | 30-60% less CO2e | Aligned |
| Serverless over always-on | Usually cheaper | Usually cleaner | Aligned |
| Buying RIs in dirty region | Saves $ | Doesn't move the needle | Trade-off vs moving region |
| GPU underutilization | Expensive | Wasted embodied carbon | Aligned |

Report both dimensions; escalate conflicts to Magi for arbitration.

## Workflow

```
MEASURE     →  pull current carbon data (provider dashboards + WattTime)
            →  compute SCI per functional unit (per request / per DAU)

ATTRIBUTE   →  emissions per team / tenant / feature (same as FinOps)
            →  Scope 1 / 2 / 3 split (Scope 2 = electricity; GHG Protocol)

TARGETS     →  align with company SBTi commitment if any
            →  set per-unit SCI targets (reductions over time)

LEVERS      →  assess region migration candidates
            →  identify carbon-aware scheduling opportunities
            →  ARM migration candidates
            →  GPU rightsizing for AI workloads

TRADEOFF    →  for each proposed change, score FinOps Δ + GreenOps Δ
            →  flag conflicts for Magi

REPORT      →  SCI trend, emissions by team/service/region
            →  CSRD / SEC compliance data (Comply handoff)

HANDOFF     →  Scaffold: region migration, carbon-aware scheduling
            →  Beacon: SCI dashboard
            →  Comply: regulatory disclosure
            →  Magi: FinOps×GreenOps conflict arbitration
            →  Launch: integrate carbon in release plan
```

## Output Template

```markdown
## GreenOps Analysis: [Workload / Org]

### Current State
- **Total CO2e (Scope 2)**: [tCO2e/month]
- **SCI (per request)**: [gCO2e/request]
- **SCI (per DAU)**: [gCO2e/user/day]
- **Region mix**: [% by region × carbon intensity]

### Emissions Breakdown
| Component | E (kWh) | I (gCO2e/kWh) | M (gCO2e) | % of total |
|-----------|---------|---------------|-----------|------------|
| Compute | [...] | [...] | [...] | [...] |
| Storage | [...] | [...] | [...] | [...] |
| Data transfer | [...] | [...] | [...] | [...] |
| AI/GPU | [...] | [...] | [...] | [...] |

### By Team / Service
| Team / Service | CO2e | $ Cost | SCI |
|----------------|------|--------|-----|
| [...] | [...] | [...] | [...] |

### Levers Assessment
| Lever | Potential CO2e Δ | $ Δ | Feasibility |
|-------|-------------------|-----|-------------|
| Region migration (us-east-1 → eu-north-1) | −60% | +5% | Medium — latency impact |
| ARM migration | −40% | −20% | High — aligned |
| Carbon-aware batch scheduling | −15% | +2% | Medium — requires scheduler update |
| GPU rightsizing | −25% | −30% | High — aligned |
| Storage lifecycle tiering | −10% | −15% | High — aligned |

### Trade-off Flags
- [Scenario]: FinOps says X, GreenOps says Y → [resolution or Magi escalation]

### Targets
- Current SCI: [...]
- Target SCI (Q4): [...] (−[%])
- SBTi alignment: [yes/no, target year]

### Compliance
- [ ] CSRD Scope 2 electricity data
- [ ] SEC climate disclosure package
- [ ] Provider carbon dashboard integrated

### Handoffs
- Scaffold: region migration IaC, carbon-aware scheduler wiring
- Beacon: SCI dashboard
- Comply: CSRD / SEC filing data
- Magi: FinOps × GreenOps conflict arbitration
- Launch: carbon in release plan
- Scribe: sustainability report for leadership / investor relations
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Treating GreenOps as marketing only | Tie to real decisions (region choice, ARM migration) |
| Reporting Scope 2 without Scope 3 for hardware | Embodied carbon matters; include M |
| Assuming "cheapest = greenest" | Not always; ap-south-1 is cheap + dirty |
| Ignoring SCI functional-unit normalization | Total CO2e can grow with usage while SCI improves |
| One-time audit, no continuous tracking | GreenOps needs ongoing measurement like FinOps |
| No FinOps × GreenOps trade-off analysis | Tension ignored = bad decisions |
| AI/GPU workloads excluded from GreenOps | AI is now often the largest emissions line |
| Using outdated grid intensity data | Refresh at least quarterly; live if possible |
| Conflating "carbon-neutral" marketing with actual reduction | Offsets are not reductions; prefer reduction first |

## Deliverable Contract

When `greenops` completes, emit:

- **Current state** (total CO2e, SCI, region mix).
- **Emissions breakdown** by component.
- **Team / service attribution**.
- **Levers assessment** with CO2e + $ delta estimates.
- **Trade-off flags** (FinOps × GreenOps conflicts).
- **Targets** aligned to SBTi / internal.
- **Compliance readiness** (CSRD / SEC).
- **Handoffs**: Scaffold, Beacon, Comply, Magi, Launch, Scribe.

## References

- ISO/IEC 21031:2024 — Software Carbon Intensity (SCI)
- GHG Protocol — Corporate Standard, Scope 1/2/3 definitions
- Green Software Foundation — Principles of Green Software Engineering
- Green Software Foundation — Carbon Aware SDK
- AWS — Customer Carbon Footprint Tool (CCFT)
- Azure — Emissions Impact Dashboard
- Google Cloud — Carbon Footprint tool
- WattTime — real-time grid carbon intensity API
- Electricity Maps — live carbon intensity map + API
- Principles of Green Software (training on Linux Foundation / edX)
- SBTi — Science Based Targets initiative criteria
- CSRD — EU Corporate Sustainability Reporting Directive
- SEC — Climate-Related Disclosures rule
- O'Reilly — *Building Green Software* (Anne Currie et al., 2024)
- FinOps Foundation — Cloud Sustainability capability (FinOps Framework 2024)
