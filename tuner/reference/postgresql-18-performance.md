# PostgreSQL 18 Performance Features

Purpose: Use this file when working with PostgreSQL 18 features, planning upgrades, or leveraging new performance capabilities.

Contents:
- 2026-05 release status
- AIO subsystem
- pg_stat_io enhancements
- pg_stat_statements 2026 metrics
- WAL I/O tracking
- per-backend I/O functions
- Merge Join improvements
- Multicolumn B-tree Skip Scan
- Planner optimizations (Self-Join Elimination, OR-to-ANY, partitionwise, DISTINCT reorder)
- pg_upgrade planner statistics preservation
- EXPLAIN ANALYZE index lookup counts
- Migration checklist

---

## 2026-05 Release Status

PostgreSQL 18 GA was **2025-09-25** (`https://www.postgresql.org/about/news/postgresql-18-released-3142/`). As of 2026-05 the supported minor stream is:

| Minor | Release date | Notes |
|-------|--------------|-------|
| `18.0` | 2025-09-25 | GA |
| `18.1` | 2025-11-13 | First scheduled minor |
| `18.2` | 2026-02-12 | Quarterly Feb minor |
| `18.3` | 2026-02-26 | Out-of-cycle security release (`https://www.postgresql.org/about/news/out-of-cycle-release-scheduled-for-february-26-2026-3241/`) |
| `18.4` | 2026-05-14 | Current as of 2026-05-22 (`https://www.postgresql.org/about/news/postgresql-184-178-1612-1516-and-1421-released-3235/`) |

The PostgreSQL project ships at least one minor release per quarter on the **2nd Thursday of Feb / May / Aug / Nov** (`https://www.postgresql.org/support/versioning/`). Always pin to the latest 18.x minor (currently 18.4) in production unless a regression is documented in the release notes.

PostgreSQL 19 entered **feature freeze on 2026-04-08** and **Beta 1 is scheduled for 2026-06-04** with GA targeted at **2026-09** (`https://pgpedia.info/postgresql-versions/postgresql-19.html`, `https://www.postgresql.org/message-id/3a3283b1-5f4b-4f11-bae8-56f998454a01@postgresql.org`). PG18 is the production target for new deployments in 2026-05; do **not** plan production cutovers to PG19 before its GA.

---

## AIO Subsystem

PostgreSQL 18 introduces a native Asynchronous I/O subsystem that replaces the previous synchronous pread/pwrite calls.

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `io_method` | `worker` | I/O method: `sync`, `worker`, or `io_uring` (Linux only) |
| `io_combine_limit` | `128kB` | Maximum bytes combined into a single I/O operation |

### Recommended Settings

```sql
-- For NVMe storage (Linux)
io_method = 'io_uring'
io_combine_limit = '256kB'

-- For general use
io_method = 'worker'
io_combine_limit = '128kB'
```

### Expected Impact

- Sequential scan throughput: 20-40% improvement on NVMe with `io_uring`; the project measured **up to 3× on cold-cache reads** (`https://www.postgresql.org/about/news/postgresql-18-released-3142/`).
- Checkpoint I/O: reduced stall during heavy write workloads
- Parallel query I/O: improved utilization of parallel workers

### 2026 Production Posture for `io_method`

| Method | When to use | Notes |
|--------|-------------|-------|
| `worker` (default) | Any OS, conservative deployments, the safe baseline | No kernel dependency; uses background I/O worker processes |
| `io_uring` | Linux kernel ≥ 5.1 with NVMe and `--with-liburing` build | Best measured throughput; **lower syscall overhead and elimination of I/O worker processes are the recommended setting for maximizing performance on PG18** (`https://aiven.io/blog/exploring-why-postgresql-18-put-asynchronous-io-in-your-database`, `https://pganalyze.com/blog/postgres-18-async-io`). Verify the build flag: `pg_config --configure | grep liburing`. |
| `sync` | Troubleshooting, A/B comparison vs PG17 | Disables AIO; do not use as a steady-state production setting on PG18+ |

Verify the binary was actually compiled with `liburing` before recommending `io_uring`; managed services often ship without it (Aurora 16/17 compatibility mode notably does not yet expose PG18's AIO knobs). Inspect `pg_aios` to confirm dispatch is async, not silently downgraded to worker/sync.

---

## pg_stat_io Enhancements

PostgreSQL 18 adds byte-level statistics to `pg_stat_io`, enabling precise I/O accounting.

### New Columns

| Column | Type | Description |
|--------|------|-------------|
| `read_bytes` | bigint | Total bytes read |
| `write_bytes` | bigint | Total bytes written |
| `extend_bytes` | bigint | Total bytes written to extend relations |

### Useful Queries

```sql
-- I/O breakdown by backend type
SELECT backend_type, context,
       read_bytes / 1024 / 1024 AS read_mb,
       write_bytes / 1024 / 1024 AS write_mb,
       hits, reads, writes
FROM pg_stat_io
ORDER BY read_bytes + write_bytes DESC;

-- Compare cache hit ratio with byte volume
SELECT backend_type,
       hits::float / NULLIF(hits + reads, 0) AS hit_ratio,
       read_bytes / 1024 AS read_kb
FROM pg_stat_io
WHERE context = 'normal';
```

---

## pg_stat_statements (PG18 2026 Posture)

PG18 reworks `pg_stat_statements` and surrounding cumulative-statistics infrastructure (`https://www.data-bene.io/en/blog/cumulative-statistics-in-postgresql-18/`, `https://postgrespro.com/blog/pgsql/5972351`):

- **Query grouping is more aggressive** — long `IN (1, 2, 3, ...)` lists collapse to a single normalised entry (only first and last literals are retained). Existing dashboards that bucketed on `query` text may show fewer, denser rows.
- **`wal_buffers_full`** column added — directly maps `wal_buffers` pressure to specific statements, removing a long-standing tuning blind spot.
- The view now exposes **≥ 45 columns** (`https://medium.com/@amareswer/postgresql-performance-tuning-with-pg-stat-statements-5f849c3d49ab`). Reuse-aware extensions (`pg_stat_monitor`, pganalyze, Datadog DBM, Aurora `aurora_stat_plans`) inherit the new columns automatically.
- **WAL statistics moved into `pg_stat_io`** (and `pg_stat_wal` correspondingly slimmed). Update any monitoring queries that JOIN both views.

```sql
-- Top wal_buffers_full offenders (PG18+)
SELECT query, calls,
       wal_buffers_full,
       round(total_exec_time::numeric / NULLIF(calls,0), 2) AS mean_ms
FROM pg_stat_statements
WHERE wal_buffers_full > 0
ORDER BY wal_buffers_full DESC
LIMIT 20;
```

---

## WAL I/O Tracking

`pg_stat_io` now tracks WAL write activity separately, enabling WAL tuning based on measured throughput.

```sql
-- WAL I/O statistics
SELECT backend_type, context,
       write_bytes / 1024 / 1024 AS wal_write_mb,
       writes AS wal_writes
FROM pg_stat_io
WHERE object = 'wal';
```

---

## Per-Backend I/O Function

```sql
-- pg_stat_get_backend_io(pid) — new in PostgreSQL 18
SELECT * FROM pg_stat_get_backend_io(pg_backend_pid());

-- Check I/O for a specific backend
SELECT pid, read_bytes, write_bytes
FROM pg_stat_activity
CROSS JOIN LATERAL pg_stat_get_backend_io(pid)
WHERE state = 'active';
```

Use this for live debugging of slow queries on specific connections.

---

## Merge Join: Incremental Sort Support

PostgreSQL 18 allows Merge Join to leverage Incremental Sort, removing the requirement for full pre-sort.

### Impact

- Queries with partial sort keys: 30-50% improvement in elapsed time
- Reduces sort spill-to-disk risk on large joins

### Verification

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT a.id, b.value
FROM table_a a
JOIN table_b b ON a.id = b.a_id
ORDER BY a.category, a.id;
-- Look for "Incremental Sort" above "Merge Join" in the plan
```

---

## Multicolumn B-tree Skip Scan

PostgreSQL 18 introduces Skip Scan for B-tree indexes, enabling index usage even when the leading column is not in the WHERE clause.

### Before (PostgreSQL 17 and earlier)

```sql
-- Index: (status, created_at)
-- Query: WHERE created_at > '2025-01-01'
-- Result: Sequential Scan (leading column 'status' not present)
```

### After (PostgreSQL 18)

```sql
-- Same index, same query
-- Result: Index Scan with Skip Scan on 'status' values
-- Effective when 'status' has low cardinality (< ~100 distinct values)
```

### When Skip Scan Helps

| Leading column cardinality | Skip Scan benefit |
|---------------------------|-------------------|
| < 10 distinct values | High — strongly recommended |
| 10–100 distinct values | Moderate |
| > 100 distinct values | Low — consider redesigning index |

### Verification

```sql
SET enable_skipscan = on; -- default in PG18
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE created_at > now() - interval '7 days';
-- Look for "Skip Scan" in Index Scan node
```

---

## Planner Optimizations

PostgreSQL 18 adds several optimizer transformations. Each is enabled by default; use the GUC to disable during regression triage.

| Transformation | What changes | GUC to disable |
|----------------|--------------|----------------|
| Self-Join Elimination (SJE) | Removes inner self-joins on a plain table when provably redundant (very common for ORM-generated SQL and range-table-heavy views) | `enable_self_join_elimination = off` |
| OR-clause to array | `col = 1 OR col = 2 OR col = 3` internally becomes `col = ANY('{1,2,3}')`, enabling index scans where the OR form would have forced seq scan | (transformation, no direct GUC) |
| `IN (VALUES ...)` → `= ANY (...)` | Better selectivity estimates for literal IN lists; the `ANY` form receives proper array statistics treatment | (transformation, no direct GUC) |
| DISTINCT key reordering | Planner reorders `SELECT DISTINCT` keys to match available sort orders and skip an extra sort | `enable_distinct_reordering = off` |
| Right Semi Join for semi-joins | Planner can pick Right Semi Join for `EXISTS`/`IN` semi-joins | (planner choice) |
| Partitionwise joins expansion | Applies in more cases with reduced memory usage; improved cost estimates for partition queries | `enable_partitionwise_join = off` |

### Diagnostic Tip

If a query regressed after upgrading to PG18, bisect with these GUCs at session scope before assuming a data or stats issue:

```sql
SET enable_self_join_elimination = off;
SET enable_distinct_reordering = off;
SET enable_partitionwise_join = off;
EXPLAIN (ANALYZE, BUFFERS) <query>;
```

---

## pg_upgrade Planner Statistics Preservation

PostgreSQL 18 `pg_upgrade` preserves optimizer statistics by default when upgrading from PG14, PG15, PG16, or PG17.

### What is preserved

- `pg_statistic` contents: `n_distinct`, null fractions, average widths, most common values (MCV lists), histograms

### What is NOT preserved

- **Extended statistics** created with `CREATE STATISTICS` (multivariate n_distinct, functional dependencies, multivariate MCV lists) — these must be rebuilt manually.

### Post-Upgrade Sequence

```bash
# 1. Fill any gaps (including extended statistics)
vacuumdb --all --analyze-in-stages --missing-stats-only
# 2. Finalize full statistics
vacuumdb --all --analyze-only
```

### Disabling (if needed)

`pg_upgrade --no-statistics` — typically only for testing or when source stats are known-bad.

### Diagnostic Implication

Post-upgrade regression on PG18+ should **not** be attributed to "missing planner stats" as a first guess; investigate plan shape changes, GUC defaults, and extended statistics loss instead.

---

## EXPLAIN ANALYZE Index Lookup Counts

PostgreSQL 18 adds per-index-scan-node **index lookup counts** to `EXPLAIN ANALYZE` output. This is essential for:

- Verifying Skip Scan actually skips (low lookup count) vs degenerates (lookup count ≈ row count)
- Diagnosing nested-loop inner-side work on composite indexes
- Spotting index scans that should have been bitmap scans

---

## pg_aios System View

`pg_aios` exposes the file handles used by the AIO subsystem — use it to confirm `io_method = io_uring` is actually dispatching async I/O (vs silently falling back to worker or sync).

```sql
SELECT * FROM pg_aios;
```

---

## Migration Checklist

When upgrading from PostgreSQL 17 to 18:

### Pre-Upgrade

- [ ] Run `pg_upgrade --check` to identify incompatibilities
- [ ] Review indexes on columns with low-cardinality leading keys — Skip Scan may change plan choices
- [ ] Audit `io_method` setting for your OS/storage type
- [ ] Benchmark `pg_stat_io` baseline on PG17 for comparison
- [ ] Inventory extended statistics (`\dX` in psql) — these will require rebuilding post-upgrade
- [ ] Capture baseline `EXPLAIN (ANALYZE, BUFFERS)` for top slow queries to compare with PG18 plans

### Post-Upgrade

- [ ] Enable `io_uring` if running on Linux with kernel ≥ 5.19 and NVMe storage
- [ ] Run `vacuumdb --all --analyze-in-stages --missing-stats-only` then `vacuumdb --all --analyze-only`
- [ ] Rebuild extended statistics (`CREATE STATISTICS` objects are not preserved by pg_upgrade)
- [ ] Monitor `pg_stat_io.read_bytes` to confirm I/O improvement
- [ ] Check Merge Join plans for Incremental Sort adoption
- [ ] Validate Skip Scan behavior for multicolumn indexes with low-cardinality leading columns
- [ ] Validate new planner transforms (SJE, DISTINCT reordering, partitionwise joins) against regression list
- [ ] Update monitoring dashboards to include `read_bytes`, `write_bytes` columns

### Incompatibilities to Watch

- `io_uring` requires Linux kernel ≥ 5.19; fall back to `worker` on older kernels
- Skip Scan may change query plans — verify regressions with `EXPLAIN (ANALYZE, BUFFERS)`
- `pg_stat_io` schema changes require monitoring query updates
- Self-Join Elimination can surface latent bugs in queries that depended on the extra self-join for row multiplication — audit `GROUP BY` / aggregation counts in regression tests
