# Data Quality Reference

Purpose: Design the runtime data-correctness layer of a pipeline — the data contract, the checks that enforce it, the lineage that explains it, and the alerting that hands off contract violations to incident response. Scope is the contract and the check, not application code and not load testing.

## Scope Boundary

- **Stream `quality`**: runtime data-correctness in pipelines — freshness, completeness, uniqueness, validity, distribution, and the contract + alert that surface violations.
- **Radar (elsewhere)**: application code tests (unit / integration / regression) — testing logic, not data in flight.
- **Siege (elsewhere)**: system-under-load testing — throughput, latency, resilience, not row-level correctness.
- **Mend / Triage (elsewhere)**: remediation of a quality incident AFTER a check fires. `quality` designs the check; Mend / Triage executes the runbook.

If the question is "is the code correct?" → `Radar`. If the question is "does it survive 10× load?" → `Siege`. If the question is "is yesterday's row count 30% below baseline and why?" → `quality`. If the question is "the check just fired, what do we do?" → `Mend` / `Triage`.

## Tool Selection

| Tool | Pick when | Skip when |
|------|-----------|-----------|
| Great Expectations (GX) | Python-native pipelines, rich expectation catalog, doc generation | Pure dbt shop — GX overlaps with dbt tests |
| Soda (Soda Core / Soda Cloud) | SodaCL YAML-first checks, broad warehouse coverage, incident workflow | Team prefers Python-as-config |
| Elementary | dbt-native, installs as dbt package, anomaly detection on existing dbt models | Non-dbt pipelines |
| dbt tests (built-in + `dbt-expectations`) | Already using dbt, checks close to the model | Freshness on non-dbt assets, cross-system checks |
| Monte Carlo / Bigeye / Anomalo | ML-driven anomaly detection at scale, enterprise observability | Early-stage team without ops bandwidth |

Default in a dbt stack: **Elementary + `dbt-expectations`** for model-level checks, **Soda** for freshness and cross-asset contracts.

## The Five Check Families

Every pipeline quality design MUST cover all five families for critical (Tier 1) assets. Tier 2/3 can scope down.

| Family | Question | Example check |
|--------|----------|---------------|
| Freshness | Did the pipeline land on time? | `max(updated_at)` within 1 hour of SLA |
| Completeness | Did all expected rows arrive? | Row count within ±10% of 7-day rolling median |
| Uniqueness | Are primary keys actually unique? | `count(distinct pk) = count(pk)` |
| Validity | Do values match the contract? | `email` matches regex, `status` ∈ enum, `amount ≥ 0` |
| Distribution | Is the shape of the data normal? | `null_rate(column)` within baseline, `avg(amount)` within 3σ |

## Workflow

```
FRAME     →  declare asset in scope (source / Bronze / Silver / Gold / mart)
          →  identify criticality tier (Tier 1 / 2 / 3 per Stream SLA contract)
          →  list consumers of the asset — each consumer implies contract expectations
          →  confirm freshness SLA + baseline volume

LAYOUT    →  write the data contract: schema, PKs, required fields, enum domains, nullability
          →  map each contract clause to one or more checks across the five families
          →  pick tool per asset class (GX / Soda / Elementary / dbt test)
          →  decide severity: warn (log) vs error (block downstream) vs page (alert on-call)

OPTIMIZE  →  baseline thresholds from historical data, not guesses — avoid check-fatigue
          →  attach OpenLineage events to the pipeline so the check result flows into lineage
          →  deduplicate checks — a dbt test + GX expectation + Soda check on the same column
             = noise, not coverage
          →  circuit-breaker: blocking errors on Tier 1 freshness; warn-only on distribution drift

WIRE      →  alert routing: Slack / PagerDuty / Opsgenie by severity
          →  runbook link on every alert — hands off to Mend / Triage
          →  dashboard: per-asset check-pass rate, MTTR of fired checks
          →  scheduled check cadence ≥ 2× the freshness SLA of the asset being checked
```

## Data Contract Example

```yaml
# contracts/gold_orders.yaml
asset: gold.fct_orders
owner: data-platform
tier: 1
freshness:
  sla: 1h
  check_cadence: 15m
schema:
  - name: order_id
    type: string
    required: true
    unique: true            # uniqueness family
  - name: user_id
    type: string
    required: true          # completeness family
  - name: order_status
    type: string
    enum: [pending, paid, shipped, canceled, refunded]  # validity family
  - name: amount_cents
    type: int
    min: 0                  # validity family
distribution:
  - column: amount_cents
    check: null_rate < 0.01
  - column: amount_cents
    check: avg within 3_sigma_of_30d_baseline    # distribution family
alert:
  tier_1_breach: pagerduty:data-oncall
  tier_2_breach: slack:#data-alerts
  runbook: https://runbooks/gold_orders.md
```

## OpenLineage Integration

Every check event should emit an OpenLineage `RunEvent` (or `DatasetEvent`) so that lineage graphs show not only "table A depends on table B" but "check X on table A was passing / failing at run Y". This turns lineage into an incident-debugging tool: when a Gold asset goes bad, you traverse upstream to the first failing check.

OpenLineage is now at **1.40.x** (2025-2026). Notable additions: static ("design-time") lineage, batch API endpoint for multi-event ingestion, `JobDependenciesRunFacet` for job-to-job dependency tracking, and ordinal position in `SchemaDatasetFacet`. Source: [openlineage.io/docs](https://openlineage.io/docs/)

- Airflow: `openlineage-airflow` provider — automatic lineage for most operators.
- dbt: `openlineage-dbt` wrapper / Elementary's OpenLineage adapter.
- Flink / Spark: `openlineage-flink` / `openlineage-spark` listeners.
- Custom Python: emit events manually via `openlineage-python` client at check boundaries.

## Data Contract Standard (2025-2026)

The industry is converging on the **Open Data Contract Standard (ODCS) v3.1** as the primary format. The original `datacontract-specification` (datacontract-specification.com) is being deprecated in favor of ODCS; support in `datacontract-cli` and tooling continues through end-of-2026. If starting a new data contract initiative, use ODCS v3 — it covers infrastructure, schemas, quality rules, SLA agreements, team ownership, and access control in one document. Source: [datacontract-specification.com](https://datacontract-specification.com/) and [datacontract.com](https://datacontract.com/)

## Anti-Patterns

- Defining 50+ checks on a single model — check-fatigue makes alerts ignored. Prefer ~5-10 per Tier 1 asset, focused on contract boundaries.
- Hard-coded thresholds that drift from reality — use rolling baselines, not constants.
- Severity-all-page — everything that fires wakes on-call, real incidents get buried. Reserve page severity for Tier 1 freshness / completeness / uniqueness breaks.
- Running quality checks inside the same transaction as the transformation — check failure rolls back good data. Checks belong on the written asset.
- Quality checks without a runbook link — alert → silence, because no one knows what to do.
- Duplicating the same check across GX + Soda + dbt test — pick one owner per check, not three.
- Treating `null_rate` drift as always-critical — many assets legitimately have sparse columns. Baseline first.
- Skipping distribution checks because "they're noisy" — distribution drift is the early-warning signal for upstream schema drift, which Stream's core contract requires detecting.

## Handoff

- To `Schema`: contract violations that require source-side constraint changes (add PK, add NOT NULL).
- To `Builder`: check implementation in pipeline code where no off-the-shelf test exists.
- To `Beacon`: SLI definitions for check-pass rate, freshness SLA burn.
- To `Mend` / `Triage`: quality-check firing is an incident — hand off with runbook, affected asset, baseline-vs-current metric snapshot.
- To `Cloak`: validity checks on PII (email format, consent flag presence).
- To `Pulse`: trust-metric dashboards for data consumers.
