# Data Observability Anti-Patterns

Purpose: anti-pattern IDs `DO-01..07`, observability maturity thresholds, five-pillar implementation rules, and data-contract guidance.

## Contents

1. Core anti-patterns
2. Maturity levels
3. Five pillars
4. Data contracts
5. Observability checklist

## Core Anti-Patterns

| ID | Anti-Pattern | Risk | Required Response |
|----|--------------|------|-------------------|
| `DO-01` | Test-Only Quality | only known issues are caught | combine tests with anomaly detection |
| `DO-02` | Alert Fatigue | real issues are ignored | use dynamic thresholds and severity |
| `DO-03` | Freshness Blindness | success masks stale data | monitor freshness separately from task success |
| `DO-04` | Schema Drift Ignorance | silent breakage or data loss | auto-detect schema changes and contracts |
| `DO-05` | Volume Anomaly Gap | large drops or spikes go unnoticed | monitor row-count anomalies statistically |
| `DO-06` | No Lineage | impact and root cause are slow to find | require lineage and dependency visibility |
| `DO-07` | Siloed Observability | no end-to-end trust signal | unify pipeline, warehouse, and consumption monitoring |

## Maturity Levels

| Level | Use when | Main capability |
|-------|----------|-----------------|
| Level 1: Testing | all teams | explicit business and schema tests |
| Level 2: Monitoring | `10+` pipelines | threshold or anomaly-based monitoring |
| Level 3: Observability | `50+` pipelines or `5+` team members | integrated RCA, lineage, and impact analysis |

## Five Pillars

| Pillar | What to monitor | Rule of thumb |
|--------|-----------------|---------------|
| Freshness | latest event/load timestamp | alert at `2-3x` expected update interval |
| Volume | row count, bytes | alert on strong deviation from recent baseline |
| Distribution | null rate, value distribution | track baseline drift |
| Schema | names, types, counts | detect additions, removals, and type changes |
| Lineage | upstream/downstream dependencies | use lineage for impact analysis and RCA |

Example thresholds:
- daily pipeline freshness alert after about `36h`
- row-count anomaly based on rolling baseline rather than fixed numbers

## Data Contracts

A data contract should define:
- schema and nullability
- freshness and volume expectations
- semantic meaning of important fields
- producer and consumer ownership
- change-management and compatibility rules

Preferred pattern by context:
- streaming -> schema registry
- dbt warehouse -> dbt contracts
- API ingestion -> OpenAPI or JSON Schema

## Observability Checklist

Minimum for every pipeline:
- success/failure alert
- runtime trend
- freshness check
- day-over-day or baseline row-count check
- PK `unique` and `not_null` tests

Add advanced layers when scale and blast radius increase.
