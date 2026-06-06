# dbt & Data Warehouse Anti-Patterns

Purpose: anti-pattern IDs `DW-01..07`, warehouse layer rules, materialization guidance, and semantic-layer thresholds.

## Contents

1. Core anti-patterns
2. Layer rules
3. Materialization strategy
4. Semantic-layer thresholds
5. Project checklist

## Core Anti-Patterns

| ID | Anti-Pattern | Risk | Required Response |
|----|--------------|------|-------------------|
| `DW-01` | Staging Skip | raw changes hit marts directly | always wrap sources with `stg_*` |
| `DW-02` | God Model | unreadable, untestable SQL | split into `int_*` models |
| `DW-03` | Hardcoded References | broken lineage and env portability | use `ref()` and `source()` |
| `DW-04` | Test Desert | quality regressions go undetected | require core dbt tests |
| `DW-05` | View Everything | slow queries and timeout risk | choose materialization by workload |
| `DW-06` | Metric Inconsistency | conflicting KPI definitions | centralize metrics in a semantic layer |
| `DW-07` | Documentation Void | low discoverability and trust | require model and column descriptions |

## Layer Rules

| Layer | Rule |
|-------|------|
| Source | declare every source and freshness check |
| `stg_*` | `1:1` with source, rename/cast/filter only |
| `int_*` | joins and business logic, small and reusable |
| `dim_*` / `fct_*` / `rpt_*` | business-facing outputs, performance-aware |

Dependency rule: `source -> stg -> int -> mart`, one direction only.

## Materialization Strategy

| Type | Best for |
|------|----------|
| `view` | lightweight staging |
| `table` | marts and heavily reused models |
| `incremental` | large append-heavy facts |
| `ephemeral` | helper transforms without standalone value |

Common default:
- `stg_ -> view`
- `int_ -> ephemeral` or `table`
- `dim_ -> table`
- `fct_ -> table` or `incremental`
- `rpt_ -> table`

## Semantic-Layer Thresholds

| Team Size | Guidance |
|-----------|----------|
| `1-3` | marts with clear docs may be enough |
| `4-10` | evaluate semantic-layer introduction |
| `10+` | semantic layer is strongly recommended |

Use it when multiple teams or BI tools define the same KPI differently.

## Project Checklist

- declare all sources and freshness checks
- ensure PKs have `unique` + `not_null`
- add `relationships` tests for FKs
- document all key models and columns
- avoid hardcoded table references
- review large `500+` line models for decomposition
- run `dbt build` in CI
