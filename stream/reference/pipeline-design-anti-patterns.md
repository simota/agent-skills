# Pipeline Design Anti-Patterns

Purpose: anti-pattern IDs `PD-01..07`, orchestration guardrails, and test strategy rules for pipeline architecture.

## Contents

1. Core anti-patterns
2. ETL vs ELT selection mistakes
3. DAG design traps
4. Scale stages
5. Test strategy

## Core Anti-Patterns

| ID | Anti-Pattern | Risk | Required Response |
|----|--------------|------|-------------------|
| `PD-01` | Append-Only Trap | duplicate data on re-run | partition overwrite, transactional `DELETE -> INSERT`, or `UPSERT` |
| `PD-02` | Silent Failure | pipeline succeeds but data is stale | freshness monitoring separate from task success |
| `PD-03` | `SELECT *` Fragility | schema changes break loads silently | explicit columns, casts, and missing-column failure |
| `PD-04` | Cron Job Orchestration | no dependency, retry, or observability control | use an orchestrator with DAG dependencies |
| `PD-05` | Hardcoded Time | backfill and testing become non-deterministic | parameterize execution date |
| `PD-06` | No Validation Gate | bad data reaches consumers | enforce source/transform/sink validation |
| `PD-07` | Full Reload Addiction | linear cost growth and SLA failure | incremental load or CDC |

## ETL vs ELT Selection Mistakes

| Situation | Wrong Choice | Better Choice |
|-----------|--------------|---------------|
| Cloud DWH with strong compute | ETL | ELT with dbt/warehouse SQL |
| Legacy DB with constrained compute | ELT | ETL with Airflow/Python/Spark |
| `< 1 minute` latency | batch | streaming |
| daily reporting | streaming | batch |

Reference thresholds:
- daily/weekly -> batch
- within `1 hour` -> micro-batch can fit
- within `1 minute` -> streaming
- sub-second -> streaming + CDC

## DAG Design Traps

- avoid one "god DAG" for unrelated domains
- avoid deep serial chains of `20+` steps
- avoid fat tasks that mix extract, transform, and load
- avoid no-retry or infinite-retry setups
- avoid dropping failed records without a DLQ

Healthy defaults:
- `1 DAG = 1 domain`
- single-responsibility tasks
- parameterized execution date
- idempotent reruns
- failure and SLA alerts

## Scale Stages

| Stage | Approximate Size | Primary Shift |
|-------|------------------|---------------|
| Stage 1 | `<10` pipelines | scripts can work, debt starts accumulating |
| Stage 2 | `10-50` pipelines | orchestrator becomes mandatory |
| Stage 3 | `50-200` pipelines | incremental load, CDC, and lineage become mandatory |
| Stage 4 | `200+` pipelines | domain ownership and governance become mandatory |

## Test Strategy

| Level | Scope |
|-------|-------|
| Unit | transform logic and edge cases |
| Integration | source-to-sink execution on test data |
| Contract | schema, nullability, and range agreements |
| Canary | production statistical checks and SLA validation |
