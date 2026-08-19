# Tenant Migration Reference

Purpose: Cross-shard tenant rebalancing, isolation-level upgrades (row-level → schema → dedicated DB), and zero-downtime tenant moves. Defines safe cutover modes, verification queries, and rollback playbooks for stateful tenant data — tenant_id is the partition key, but every move involves rows, sequences, FK chains, and downstream caches.

## Scope Boundary

- **shard `migration`**: tenant-level data moves and isolation-level transitions inside an established multi-tenant model. Output is a migration plan with cutover mode, verification, and rollback.
- **shard `isolation` / `rls` / `routing` / `scale` (elsewhere)**: greenfield isolation strategy, RLS policy authoring, tenant resolution, and noisy-neighbor controls. Migration consumes those designs but does not redesign them.
- **schema (elsewhere)**: physical schema/DDL migrations and column-level changes. Tenant migration calls Schema for DDL but owns the tenant-row movement plan itself.
- **beacon (elsewhere)**: SLO budget burn during cutover. Migration emits cutover-window targets; Beacon owns the live SLO observation.
- **tempo (elsewhere)**: cron/business-calendar scheduling for cutover windows. Migration specifies the constraints; Tempo schedules the actual run.
- **ledger (elsewhere)**: cost delta of moving a tenant to a dedicated DB. Migration produces the unit-cost line items; Ledger reconciles to FinOps.

## Workflow

```
ASSESS    →  inventory source/target shards, FK chains, sequences, caches, queues
          →  classify tenant: hot (zero-downtime required) | warm | cold (offline OK)

DESIGN    →  pick mode: dual-write+cutover | offline-copy | logical-replica-promote
          →  define idempotency key, batch size, throttle, sequence reset plan

DRY-RUN   →  run on staging tenant clone; measure copy time, replay lag, FK fan-out
          →  rehearse cutover script and rollback in non-prod

EXECUTE   →  freeze writes (or enable dual-write), copy, verify, flip routing
          →  reset sequences, re-warm caches, re-subscribe queues

VERIFY    →  row-count parity, content hash per table, FK integrity, sequence sanity
          →  smoke tests under tenant identity; observe error rate vs baseline

ROLLBACK  →  revert routing, re-enable source writes, replay diff from sink
          →  declare success only after N stable cycles post-cutover
```

## Migration Mode Matrix

| Mode | Downtime | Data freshness at cutover | Complexity | When to use |
|------|----------|---------------------------|------------|-------------|
| **Offline copy** | Hours | Exact (writes frozen) | Low | Cold tenant, off-hours allowed, small data |
| **Dual-write + cutover** | Seconds | Both shards converge | High | Hot tenant, active 24/7, can tolerate brief read divergence |
| **Logical replica promote** | Sub-second | Replication lag bounded | Medium | DB engine supports logical replication (Postgres pglogical, MySQL GTID) |
| **Backfill + CDC tail** | Sub-second | CDC lag bounded | Medium-High | Existing CDC pipeline (Debezium/Kafka) |
| **Online with shadow read** | Zero | Eventually consistent | Very High | Migration must be invisible; accept extra read cost during overlap |

## Isolation-Level Upgrade Patterns

| From → To | Trigger | Strategy | Risk |
|-----------|---------|----------|------|
| Pooled RLS → Schema-per-tenant | Tenant exceeds noisy-neighbor budget or compliance ask | `CREATE SCHEMA tenant_X`, copy filtered rows, switch routing | FK to global tables, sequence collisions |
| Pooled RLS → Dedicated DB | Enterprise contract / HIPAA / data-residency | Logical dump filtered by tenant_id, restore to new DB | Cross-tenant FKs (must not exist) |
| Schema-per-tenant → Dedicated DB | Per-tenant scale or regulatory | pg_dump schema, restore as public, repoint connection string | Search-path assumptions in app |
| Dedicated DB → Pooled RLS | Tenant churn / cost compression | Reverse: insert rows with tenant_id column added | RLS policies must already cover this tenant_id |

## Verification Queries

Run all three after cutover; any mismatch blocks finalization.

```sql
-- 1. Row count parity per table
SELECT 'orders' AS t, count(*) FROM source.orders WHERE tenant_id = :t
UNION ALL
SELECT 'orders', count(*) FROM target.orders WHERE tenant_id = :t;

-- 2. Content hash (deterministic ordering required)
SELECT md5(string_agg(t::text, '' ORDER BY id))
FROM source.orders t WHERE tenant_id = :t;
-- Compare to same query on target.

-- 3. FK integrity — orphan check post-move
SELECT count(*) FROM target.order_items oi
LEFT JOIN target.orders o ON o.id = oi.order_id
WHERE oi.tenant_id = :t AND o.id IS NULL;
-- Must be 0.
```

## Sequence and Identity Reset

| Identity type | Reset action |
|---------------|--------------|
| Postgres serial / `bigserial` | `SELECT setval('orders_id_seq', (SELECT max(id) FROM target.orders WHERE tenant_id = :t))` |
| Postgres `IDENTITY` | `ALTER TABLE … ALTER COLUMN id RESTART WITH …` |
| UUIDv4 | No reset needed (random) |
| UUIDv7 / ULID | No reset, but verify monotonic ordering preserved |
| MySQL AUTO_INCREMENT | `ALTER TABLE … AUTO_INCREMENT = N` |
| Application-side counter (Redis INCR) | Read source value, set on target, double-check before flip |

Forgetting sequence reset causes the next insert to collide with copied rows — the most common post-migration outage.

## Rollback Playbook

| Stage | Rollback action | Time budget |
|-------|----------------|-------------|
| Pre-copy | Cancel job; nothing to undo | seconds |
| During copy | Drop target rows for tenant_id; release lock | minutes |
| Dual-write active | Disable target writes; verify source still authoritative | seconds |
| Post-cutover, pre-verify | Flip routing back to source; replay target diff to source | < 5 min |
| Post-verify, pre-source-decom | Re-enable source writes; CDC replay to source; flip back | minutes-hours |
| Source decommissioned | Restore from snapshot; full reverse migration | hours |

Define the abort-decision threshold *before* cutover: e.g. "if verify queries fail or error rate > 2× baseline at T+5min, roll back."

## Anti-Patterns

- **Forgetting sequence reset** — copying rows without `setval` collides on next insert. Causes duplicate-key errors within minutes of cutover.
- **Untested replay path** — dual-write systems where the "replay diff to source" branch was never exercised on staging fail when actually needed.
- **Inconsistent FK chain** — moving `orders` for a tenant but leaving `order_items` behind because they had no `tenant_id` column. Always inventory the full FK closure.
- **Cache not invalidated under tenant key** — old shard's cached query results survive cutover; users see stale data even after routing flip.
- **Queue/CDC subscriptions not rebuilt** — Kafka consumer groups still pointing at source partitions; downstream services see writes disappear.
- **Cutover during peak** — running zero-downtime migration during business hours doubles blast radius. Schedule via Tempo for low-traffic windows.
- **No abort threshold defined** — teams keep "trying to make it work" past the safe rollback boundary. Define and commit to the abort criteria before cutover.
- **Cross-tenant FK pretending to be tenant-scoped** — a `users.referrer_id → users.id` self-FK that points across tenants blocks dedicated-DB migration silently.
- **Skipping content hash, trusting only row counts** — counts can match while content drifts (replication lag, swallowed write). Hash or sample-compare.

## Handoff

- **To Schema**: DDL changes required for the target shard (new schema, indexes, RLS policies on tenant_id) — Schema authors the migration SQL.
- **To Tempo**: cutover window constraints (off-peak, business calendar, region timezone) — Tempo schedules the run.
- **To Beacon**: SLO budget for the cutover window, alert thresholds, and tenant-scoped dashboards to watch live.
- **To Ledger**: per-tenant unit-cost delta when moving to dedicated infra — feeds FinOps and pricing-tier handoff.
- **To Sentinel**: post-migration RLS policy validation on the new shard; cross-tenant leakage scan.
- **To Builder**: cutover script, rollback script, and runbook for the on-call engineer executing the migration.
