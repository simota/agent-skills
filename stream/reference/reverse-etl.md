# Reverse ETL Reference

Purpose: Design the activation pipeline that syncs warehouse-modeled data OUT to operational SaaS tools (Salesforce, HubSpot, Zendesk, Marketo, Intercom) so that sales, support, and marketing can act on warehouse-truth data without direct DWH access. The warehouse is the source of truth; the SaaS tool is the destination.

## Scope Boundary

- **Stream `reverse`**: DWH → SaaS activation. Source model selection, primary-key dedup, field mapping, sync cadence, destination rate limits, row-level failure handling.
- **Stream `etl` / `elt`**: source → DWH. Ingest, model, transform — data moving INTO the warehouse.

If the arrow points from source system → DWH, use `etl` or `elt`. If the arrow points from DWH → SaaS operational tool, use `reverse`. A "full round trip" needs both, but each direction is its own pipeline with its own contract.

## Tool Selection

| Tool | Pick when | Skip when |
|------|-----------|-----------|
| Census | SQL-first modeling, strong dbt integration, observability | Need deep workflow automation beyond sync |
| Hightouch | Audience / segmentation UX, AI decisioning, large destination catalog | Budget-constrained — enterprise pricing |
| Workato | Broader iPaaS — reverse ETL is one use case among many | Pure activation-only need (overkill) |
| RudderStack Reverse ETL | Already using RudderStack for CDP | Warehouse-first team without event pipeline |
| Hand-rolled (Airflow + destination SDK) | Unique destination, strict cost control | Team lacks ops bandwidth for rate-limit + retry logic |

Default: **Census or Hightouch** — the field has commoditized around these two for warehouse-native activation.

## Workflow

```
FRAME     →  declare source model (dbt mart), destination tool + object
             (Salesforce Contact / HubSpot Company / Zendesk User / Marketo Lead)
          →  declare primary-key column and destination match field
          →  target sync cadence (hourly / 15-min / near-real-time)
          →  identify PII + consent fields; check destination data-residency constraints

LAYOUT    →  pick tool; define warehouse connection (read-only role)
          →  define the "model" (SQL query or dbt model reference)
          →  field mapping: source column → destination field, with enum/picklist mapping
          →  sync mode: upsert (default) / insert / update / mirror
          →  identity resolution: which destination record matches which warehouse row

OPTIMIZE  →  dedup on warehouse side by primary key BEFORE sync
          →  diff-based sync (only changed rows) vs full mirror — prefer diff for cost + rate-limit reasons
          →  row-level reject handling (Salesforce field validation failures, HubSpot enum mismatches)
          →  destination rate-limit budget (Salesforce daily API limit, HubSpot per-10s limits)
          →  respect consent flags: suppress PII sync when consent revoked

WIRE      →  observability: rows synced / rejected / rate-limited per run
          →  alert on reject-rate > threshold (default 1%)
          →  rollback plan: destination-side delete is usually NOT safe — prefer soft-delete flag
          →  handoff to downstream: sales ops, CRM admin, lifecycle marketing
```

## Field Mapping Discipline

- **Primary key**: always a stable warehouse identifier (user_id, account_id) mapped to a destination external-ID field (Salesforce External ID, HubSpot custom unique property). Never map to the destination's native ID — that couples warehouse to destination internals.
- **Enum / picklist mapping**: destination picklists reject unknown values. Maintain an explicit mapping table in the warehouse (`dim_salesforce_stage_map`) so unmapped warehouse values are caught before sync.
- **Nullability**: destination fields often reject `NULL` as "clear value" by default. Decide per-field whether NULL means "skip" or "clear".
- **Computed fields**: compute in dbt, not in the reverse-ETL tool's SQL box. Keeps logic versioned and testable.

## Dedup by Primary Key

The warehouse model MUST deduplicate on the primary key before sync. Otherwise the destination receives N conflicting writes for the same record, rate-limit is consumed N times, and the "last write wins" race is non-deterministic.

```sql
-- dbt model: models/activation/crm_contact_activation.sql
select distinct on (user_id)
  user_id,                          -- primary key, maps to Salesforce External ID
  email,                            -- match / upsert key
  first_name,
  last_name,
  lifecycle_stage,                  -- enum mapped via dim_salesforce_stage_map
  last_seen_at,
  account_id                        -- relation to Salesforce Account
from {{ ref('fct_user_activity') }}
where email is not null             -- destination required-field guard
  and consent_marketing = true      -- consent gate
order by user_id, last_seen_at desc
```

## Sync Cadence

| Cadence | When | Cost / risk |
|---------|------|-------------|
| Daily | Low-urgency enrichment, compliance attributes | Safe, cheap |
| Hourly | Lifecycle stage updates, lead scoring | Default for most CRM sync |
| 15-min | Support context (Zendesk user updates) | Watch destination rate limits |
| Near-real-time (streaming / webhook) | Sales alerts on high-intent signals | Needs event trigger upstream — usually out of reverse-ETL scope, hand off to `stream` |

"Near-real-time" reverse ETL above ~5-minute cadence is usually a sign the wrong tool is being used — evaluate event streaming instead.

## Anti-Patterns

- Syncing an unmodeled raw source table directly to Salesforce — no dedup, no contract, no test.
- Using destination's native ID as the match key — brittle to destination record merges.
- Ignoring destination rate limits until hitting them in production — Salesforce daily API limits are per-org, shared across all integrations.
- Treating reverse ETL as bidirectional — writes from SaaS back to warehouse are an ingest concern (`etl` / `elt`), not reverse ETL.
- Syncing PII to marketing tools without a consent gate in the model — GDPR / CCPA violation.
- Skipping a field-mapping review when the destination adds a picklist value — sync silently rejects those rows.
- Running a full mirror sync on a multi-million-row table — burns rate limit and destination storage; use diff-based sync.

## Handoff

- To `Schema`: activation mart design, dedup-key constraints.
- To `Builder`: custom destination adapter when no off-the-shelf connector exists.
- To `Sentinel` / `Cloak`: PII sync review, consent-gate verification.
- To `Pulse`: activation KPIs (rows synced, reject rate, downstream lift).
- To `Beacon`: reject-rate SLI, sync-latency SLI, destination rate-limit budget SLI.
- To `Mend` / `Triage`: elevated reject rate or rate-limit exhaustion incident.
