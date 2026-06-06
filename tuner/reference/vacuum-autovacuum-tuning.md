# VACUUM & Autovacuum Tuning Reference

Purpose: Use this file when the bottleneck is table/index bloat, stale planner statistics, transaction-ID wraparound risk, or autovacuum is visibly falling behind. Covers VACUUM/ANALYZE/autovacuum knobs, bloat detection queries, `fillfactor`, freeze horizon, and `default_statistics_target` tuning. PostgreSQL-specific.

## Scope Boundary

- **Tuner `vacuum`**: runtime maintenance — autovacuum thresholds, statistics-target tuning, bloat remediation, freeze horizon management, REINDEX/VACUUM FULL timing.
- **Schema (elsewhere)**: design-time decisions that influence vacuum behavior — `fillfactor` set at `CREATE TABLE`, partitioning strategy to shrink vacuum windows, HOT-update-friendly column layout. Schema owns the DDL, Tuner owns the runtime parameter.
- **Gateway (elsewhere)**: unrelated — API-layer concern, called out only to disambiguate.
- **Forge (elsewhere)**: prototype databases don't need vacuum tuning; real tuning is Tuner's.
- **Beacon (downstream)**: dashboards and alerts for bloat/wraparound — Tuner designs the queries, Beacon operationalizes them.

If the question is "autovacuum is too slow / too aggressive / skipping this table" → `vacuum`. If it's "our update pattern creates bloat, redesign the column" → Schema.

## Key Thresholds

| Signal | Threshold | Meaning |
|--------|-----------|---------|
| Dead tuple ratio | `n_dead_tup / n_live_tup > 10%` | ANALYZE lag or autovacuum falling behind |
| Dead tuple ratio (critical) | `> 20%` | Index scans degrade, bloat compounds |
| Last autovacuum | `> 24h on busy table` | Autovacuum starving, check cost limits |
| Last autoanalyze | `> 24h` | Planner stats stale, bad plans likely |
| Wraparound risk | `age(relfrozenxid) > 200M` | Aggressive antiwraparound vacuum imminent |
| Wraparound emergency | `> 1.5B` | Shutdown risk; single-user mode may be required |
| Table bloat | `> 2× expected size` | Consider VACUUM FULL / pg_repack |
| Index bloat | `> 2× expected` | REINDEX CONCURRENTLY |

## Detection Queries

Dead tuple ratio per table:

```sql
SELECT schemaname, relname,
       n_live_tup, n_dead_tup,
       round(n_dead_tup * 100.0 / nullif(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
       last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY dead_pct DESC NULLS LAST
LIMIT 20;
```

Wraparound horizon:

```sql
SELECT c.relname,
       age(c.relfrozenxid) AS xid_age,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS size
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind IN ('r','m','t') AND n.nspname NOT IN ('pg_catalog','information_schema')
ORDER BY age(c.relfrozenxid) DESC
LIMIT 20;
```

Index bloat estimate (approximate; use `pgstattuple` extension for accuracy):

```sql
SELECT schemaname, indexrelname, pg_size_pretty(pg_relation_size(indexrelid)) AS size,
       idx_scan
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 20;
```

## Autovacuum Tuning

Default autovacuum is conservative and scales poorly on large tables. Per-table overrides are the correct granularity:

```sql
-- Aggressive autovacuum for a high-churn table
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.02,      -- default 0.20 → trigger at 2% dead
  autovacuum_analyze_scale_factor = 0.01,     -- default 0.10
  autovacuum_vacuum_cost_limit = 2000,        -- default 200; higher = more work per cycle
  autovacuum_vacuum_cost_delay = 2            -- ms; default 2ms in PG12+
);
```

Global knobs worth revisiting on fast storage:

```ini
# postgresql.conf
autovacuum_max_workers = 6          # default 3; scale with cores
autovacuum_naptime = 30s            # default 1min; tighter on busy OLTP
maintenance_work_mem = 1GB          # default 64MB; VACUUM and CREATE INDEX benefit
vacuum_cost_limit = 2000            # default 200; NVMe can handle 10×
autovacuum_work_mem = -1            # inherit maintenance_work_mem
```

Rule: `autovacuum_vacuum_scale_factor` should decrease as the table grows — a 1B-row table at 20% scale factor means 200M dead tuples before autovacuum triggers.

## Fillfactor & HOT Updates

`fillfactor` reserves free space on each page for in-page (HOT) updates, which avoid index bumps and vacuum pressure:

| Table profile | Recommended fillfactor |
|---------------|-----------------------|
| Append-only (events, logs) | 100 (default) |
| Mixed read/write | 90 |
| Heavy UPDATE on non-indexed columns | 70-80 |
| Very heavy UPDATE hot rows | 60-70 |

```sql
ALTER TABLE user_sessions SET (fillfactor = 80);
-- New pages use 80%. Existing pages rebuild on VACUUM FULL or CLUSTER.
```

HOT update requirements: the updated column is not indexed, and the new row fits on the same page. If either fails, the update is not HOT, a new index entry is written, and the old tuple becomes dead → more vacuum work.

## Statistics Target

`default_statistics_target` controls histogram resolution. Default 100 is fine for most columns; raise for skewed or high-cardinality columns that drive selectivity estimates:

```sql
-- Per-column; preferred over raising the global default
ALTER TABLE orders ALTER COLUMN customer_id SET STATISTICS 500;
ANALYZE orders;
```

Signals for raising statistics target:
- Planner estimate vs. actual ratio > 10× on queries filtering this column.
- Column has long-tail distribution (e.g., 1% of customers drive 90% of orders).
- `pg_stats.n_distinct` reported value looks wrong.

Cost: larger `pg_statistic`, slower ANALYZE. Raising globally is a blunt instrument; prefer per-column.

## Freeze Horizon

`vacuum_freeze_min_age` and `autovacuum_freeze_max_age` govern when tuples are frozen to avoid wraparound:

```ini
autovacuum_freeze_max_age = 200000000   # default; antiwraparound vacuum triggers here
vacuum_freeze_min_age = 50000000        # default; tuples older than this get frozen
vacuum_freeze_table_age = 150000000     # aggressive scan threshold
```

On very large tables, antiwraparound vacuum is expensive because it must scan every page not marked all-frozen. Mitigation:

- Lower `autovacuum_freeze_max_age` on large tables so freeze work is spread out.
- Ensure the visibility map is current — recent VACUUMs mark pages all-visible/all-frozen so future vacuums can skip them.
- On PG 13+, parallel index vacuuming (`max_parallel_maintenance_workers`) speeds large-table vacuum.

## VACUUM FULL vs pg_repack

| Tool | Locks | Downtime | When |
|------|-------|---------|------|
| VACUUM FULL | ACCESS EXCLUSIVE | Full table unavailable | Small tables, scheduled maintenance |
| CLUSTER | ACCESS EXCLUSIVE | Full table unavailable | Rewrite by index, small/medium tables |
| pg_repack | Brief locks at start/end | Online | Large production tables |
| REINDEX CONCURRENTLY | No blocking | Online | Index bloat only |

Default to `pg_repack` for bloated large tables in production; `VACUUM FULL` only during approved maintenance windows.

## Anti-Patterns

- Running `VACUUM FULL` on a 100GB+ table during business hours — ACCESS EXCLUSIVE lock stalls all reads/writes for the duration.
- Raising `default_statistics_target` globally to 1000 because one column needs it — slows every ANALYZE and bloats `pg_statistic` for no gain.
- Ignoring `last_autovacuum = NULL` on large busy tables — autovacuum is being starved by cost limits, not turned off.
- Disabling autovacuum on a table to "improve write performance" — dead tuples accumulate, index scans degrade, and eventually an emergency antiwraparound vacuum runs anyway at the worst possible time.
- Setting `fillfactor = 50` reflexively on every table — wastes 50% of disk and memory on tables that never UPDATE.
- Treating bloat as a vacuum problem when the root cause is long-running transactions blocking tuple removal — check `pg_stat_activity` for old `xact_start` before tuning vacuum knobs.
- Running REINDEX without CONCURRENTLY on production indexes — blocks writes for the duration.
- Forgetting that replication slots hold back vacuum — an abandoned logical replication slot prevents dead tuple removal across the entire cluster.

## Handoff / Next Steps

After a `vacuum` recommendation:

- **To Schema** (via `TUNER_TO_SCHEMA`): when the real fix is `fillfactor` at table creation, partitioning to shrink the vacuum window, or removing an index that blocks HOT updates — Schema owns DDL.
- **To Builder** (via `TUNER_TO_BUILDER`): fix application patterns that create bloat — batch updates over many small transactions, long-held transactions in web handlers, unused replication slots from dev tooling.
- **To Beacon** (via `TUNER_TO_BEACON`): dashboards for dead-tuple ratio, last_autovacuum age, wraparound horizon, replication slot lag; alert on `age(relfrozenxid) > 500M` or `dead_pct > 20% on > 1M-row table`.
- **To Bolt** (via `TUNER_TO_BOLT`): when vacuum cost is IO-bound on shared storage, revisit storage tier or isolation before further tuning.

Deliverable artifacts: per-table autovacuum overrides, bloat-detection query set, freeze-horizon monitoring query, fillfactor recommendation matrix, pg_repack / REINDEX CONCURRENTLY schedule.
