# Slow Query Analysis & Benchmarks

Purpose: Use this file when enabling slow-query logging, collecting top offenders, or benchmarking improvements.

Contents:

- PostgreSQL slow-query setup
- MySQL slow-query setup
- benchmark commands
- reporting link

## PostgreSQL Slow Queries

```sql
ALTER SYSTEM SET log_min_duration_statement = '1000';
ALTER SYSTEM SET log_statement = 'none';
SELECT pg_reload_conf();

SELECT
    query,
    calls,
    round(total_exec_time::numeric, 2) AS total_ms,
    round(mean_exec_time::numeric, 2) AS mean_ms,
    round(stddev_exec_time::numeric, 2) AS stddev_ms,
    rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```

On **PostgreSQL 18+**, `pg_stat_statements` adds the `wal_buffers_full` column and normalises `IN (...)` lists more aggressively (`https://www.data-bene.io/en/blog/cumulative-statistics-in-postgresql-18/`). Add `wal_buffers_full` to ordering when WAL pressure is the suspected bottleneck:

```sql
-- PG18+: surface WAL-buffer-pressured statements
SELECT query, calls, wal_buffers_full,
       round(total_exec_time::numeric / NULLIF(calls,0), 2) AS mean_ms
FROM pg_stat_statements
WHERE wal_buffers_full > 0
ORDER BY wal_buffers_full DESC
LIMIT 20;
```

Combine with `auto_explain` for plan capture — Datadog DBM and pganalyze both consume `auto_explain` output for post-hoc bottleneck attribution (`https://www.datadoghq.com/blog/database-monitoring-explain-analyze/`).

## MySQL Slow Queries

```sql
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
SET GLOBAL log_queries_not_using_indexes = 'ON';

SELECT
    DIGEST_TEXT,
    COUNT_STAR,
    ROUND(SUM_TIMER_WAIT/1000000000000, 3) AS total_sec,
    ROUND(AVG_TIMER_WAIT/1000000000000, 3) AS avg_sec
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;
```

### pt-query-digest (Percona Toolkit 3.7.1, 2026-04-17)

`pt-query-digest` aggregates MySQL slow query logs by normalized fingerprint and reports P95/P99 latency, rows-examined, and query count. Latest version: **3.7.1** (released 2026-04-17) (`https://docs.percona.com/percona-toolkit/pt-query-digest.html`).

```bash
# Basic slow-log analysis
pt-query-digest /var/log/mysql/slow.log

# Review mode: save unique queries to DB, skip already-reviewed on re-run
pt-query-digest --review h=localhost,D=review_db,t=query_review /var/log/mysql/slow.log

# History mode: track per-fingerprint latency trends over time
pt-query-digest --history h=localhost,D=review_db,t=query_history /var/log/mysql/slow.log

# Top 10 by total time with explain
pt-query-digest --limit 10 --explain h=localhost,u=root,p=pass /var/log/mysql/slow.log
```

### MySQL 9.7 Hypergraph Optimizer Validation

MySQL 9.7+ ships a new Hypergraph join optimizer (GA in Community Edition, 2026-05). For multi-table join workloads, enable per session and validate with `EXPLAIN FORMAT=TREE` (`https://blogs.oracle.com/mysql/the-hypergraph-optimizer-is-now-available-in-mysql-9-7-community-edition`):

```sql
-- Enable Hypergraph optimizer for session
SET optimizer_switch = 'hypergraph_optimizer=on';

-- Validate: TREE format is the only output showing hash join nodes
EXPLAIN FORMAT=TREE
SELECT u.name, COUNT(o.id)
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.created_at > NOW() - INTERVAL 30 DAY
GROUP BY u.name;

-- Confirm hash join selected (look for "Hash join" in output)
-- Benchmark: sysbench read-only-distinct shows ~26% gain with hypergraph on 9.7.0
```

MySQL 8.4 LTS note: `innodb_adaptive_hash_index` defaults to **OFF** in 8.4 (was ON in 8.0). Benchmark with and without before enabling in production. Hash joins use `join_buffer_size` for in-memory budget; spill-to-disk degrades significantly on large joins.

## Benchmarks

### PostgreSQL (`pgbench`)

```bash
pgbench -i -s 10 mydb
pgbench -c 10 -j 2 -T 60 -S mydb
pgbench -c 10 -j 2 -t 1000 -f custom_query.sql mydb
```

### MySQL (`sysbench`)

```bash
sysbench oltp_read_write --mysql-host=localhost --mysql-db=mydb --mysql-user=root --tables=10 --table-size=100000 prepare
sysbench oltp_read_write --mysql-host=localhost --mysql-db=mydb --mysql-user=root --threads=4 --time=60 run
sysbench oltp_read_write cleanup
```

## Reporting

Use [performance-report-template.md](~/.claude/skills/tuner/reference/performance-report-template.md) for the canonical before/after report format.


---

# Critical Thresholds and Production-Safety Rules (full)

Canonical home for the threshold table and safety rules summarized in `SKILL.md`.

| Signal                                        | Threshold                                  | Meaning                               |
| --------------------------------------------- | ------------------------------------------ | ------------------------------------- |
| Seq Scan is acceptable                        | table `< 1K rows`                          | usually fine                          |
| Row estimate mismatch warning                 | `> 10x`                                    | planner statistics or predicate issue |
| Row estimate mismatch critical                | `100x+`                                    | plan reliability is poor              |
| Seq Scan critical                             | table `> 100K rows`                        | likely bottleneck unless justified    |
| Partitioning usually not needed               | table `< 10M rows`                         | index tuning first                    |
| Partitioning becomes likely                   | `10M-100M` rows with time/category filters | evaluate range or list                |
| Composite partitioning likely                 | `> 100M` rows with mixed filters           | evaluate carefully                    |
| Bulk operations should leave ORM comfort zone | `10,000+` rows                             | prefer raw SQL or bulk tools          |
| ORM overhead becomes critical                 | `1000+ RPS` API paths                      | measure hydration/serialization cost  |
| OFFSET pagination degradation                 | table `> 5K rows` with deep pages          | switch to keyset/cursor pagination    |
| P99 latency concern (user-facing)             | `> 200ms`                                  | investigate and optimize              |
| P99 latency concern (background)              | `> 500ms`                                  | investigate and optimize              |
| Connection pool exhaustion risk               | `> 80%` pool utilization sustained         | scale pool or optimize query duration — PgBouncer for <50 clients, PgCat for >50 clients or read/write splitting, Supavisor for serverless |
| Statistics staleness                          | `n_dead_tup > 10%` of `n_live_tup`        | run ANALYZE or check autovacuum       |
| Index bloat concern                           | index size `> 2×` expected for row count   | consider REINDEX CONCURRENTLY         |
| pgvector index selection                      | dataset `> 500K vectors`                   | HNSW as production default (~15× higher QPS than IVFFlat at 1M/50d benchmarks); fall back to IVFFlat only when build time or memory (HNSW ≈3× memory, ~30× build time) dominate |
| pgvector filtered search overfiltering risk   | any WHERE filter on vector query           | enable `hnsw.iterative_scan = 'relaxed_order'` (pgvector 0.8+); without it only ef_search candidates are evaluated before the filter, causing result starvation — up to 5.7× QPS improvement for selective filters (`https://www.postgresql.org/about/news/pgvector-080-released-2952/`) |
| pgvector halfvec storage reduction            | dataset with float4 embeddings             | halfvec (2-byte floats, pgvector 0.7+) cuts index storage ~60% with negligible recall loss on 1536-dim embeddings; up to 10M vectors fit on a mid-tier managed instance (`https://www.postgresql.org/about/news/pgvector-070-released-2852/`) |
| MySQL Hypergraph optimizer                    | MySQL 9.7+ with complex multi-table joins  | enable via `SET optimizer_switch='hypergraph_optimizer=on'`; GA in MySQL 9.7 Community Edition (2026-05); shows +26% read-only-distinct, +15% range gains in sysbench; use `EXPLAIN FORMAT=TREE` to verify hash-join selection (`https://blogs.oracle.com/mysql/the-hypergraph-optimizer-is-now-available-in-mysql-9-7-community-edition`) |

Production-safety rules:

- PostgreSQL production index creation should use `CREATE INDEX CONCURRENTLY`.
- Materialized views are good for repeated aggregates and dashboards, not for truly real-time data.
- PostgreSQL 18+: leverage AIO for up to 3× I/O throughput on sequential scans and bitmap heap scans; use skip scan for multicolumn B-tree indexes where the leading column has low cardinality (~40% speedup over seq scan); use parallel GIN index builds for full-text and JSONB indexes; prefer `uuidv7()` for primary keys (time-ordered writes eliminate B-tree fragmentation); leverage improved merge joins with incremental sort and faster hash joins; prefer virtual generated columns over stored for read-only derived values to reduce write overhead. Additional planner wins: Self-Join Elimination (drops redundant self-joins; `enable_self_join_elimination`), OR-clause to array transform for index-friendly OR predicates, `IN (VALUES ...)` → `= ANY (...)` for better selectivity estimates, expanded partitionwise joins with reduced memory, and `DISTINCT` key reordering to skip sorts.
- PostgreSQL 18+ `pg_upgrade` preserves planner statistics from PG14+ source clusters **by default**, eliminating the historical post-upgrade performance cliff. **Extended statistics created with `CREATE STATISTICS` are NOT preserved** — always rebuild them and run `vacuumdb --all --analyze-in-stages --missing-stats-only` followed by `vacuumdb --all --analyze-only` after the upgrade. Do not blame "missing stats" for post-upgrade regressions on PG18+ unless extended/multivariate stats are involved.
- On PostgreSQL 18+, `EXPLAIN ANALYZE` reports **index lookup counts per index scan node** — essential for diagnosing skip-scan efficiency and verifying that a multicolumn B-tree actually skips rather than degenerating into repeated scans.
- Always verify `@Transactional(readOnly = true)` on read-only queries in ORM frameworks — omitting it causes unnecessary write locks and reduces concurrent read throughput.
- Enable `auto_explain` module (`auto_explain.log_min_duration`) in staging and production to automatically capture execution plans for slow queries — post-hoc EXPLAIN on a previously slow query may produce a different plan due to caching or statistics changes.
- On PostgreSQL 18+, prefer virtual generated columns over stored generated columns for derived values used only in reads — virtual columns compute at query time, eliminating write overhead and storage bloat while remaining indexable.
- MySQL 8.4 LTS InnoDB tuning: `innodb_adaptive_hash_index` is **disabled by default** in 8.4 (enabled in 8.0/earlier); benchmark both states before enabling. For hash joins, `join_buffer_size` caps in-memory usage — spill-to-disk degrades significantly; tune based on workload. Use `EXPLAIN FORMAT=TREE` to confirm hash join selection (`https://dev.mysql.com/doc/refman/8.4/en/hash-joins.html`). MySQL parallel DDL (index creation uses parallel threads by default in 8.4+) makes large `ALTER TABLE` operations significantly faster — verify `innodb_ddl_threads` setting.
- MySQL 9.7+ Hypergraph optimizer: GA in MySQL 9.7 Community Edition (2026-05); enables better hash-join cost models vs the classic nested-loop-first optimizer. Enable per-session with `SET optimizer_switch='hypergraph_optimizer=on'`. The `EXPLAIN FORMAT=TREE` output is the only format showing hash-join node details (`https://blogs.oracle.com/mysql/the-hypergraph-optimizer-is-now-available-in-mysql-9-7-community-edition`).
- For MySQL slow-query analysis, use `pt-query-digest` (Percona Toolkit 3.7.1, released 2026-04-17) to aggregate slow logs by normalized fingerprint and surface P95/P99 latency and rows-examined distributions (`https://docs.percona.com/percona-toolkit/pt-query-digest.html`). For workload profiling and index advising, pair with `pg_qualstats` + `hypopg` on PostgreSQL: `pg_qualstats_index_advisor()` proposes candidates, hypopg validates each via `EXPLAIN` without building the real index, then promote with `CREATE INDEX CONCURRENTLY` (`https://www.percona.com/blog/automatic-index-recommendations-in-postgresql-using-pg_qualstats-and-hypopg/`).
- pgvector 0.8+ iterative scan: for filtered vector queries with a WHERE clause, set `hnsw.iterative_scan = 'relaxed_order'` (or `strict_order` when exact distance ordering is required) and tune `hnsw.max_scan_tuples`. Without this, `ef_search` candidates are evaluated before the filter, causing result starvation on selective filters. pgvector 0.7+ `halfvec` type halves storage with negligible recall loss — prefer for float32 embeddings when storage cost matters.
- PostgreSQL 19 (Beta 1 expected 2026-06-04, GA 2026-09): forward-plan only. Notable monitoring additions: `pg_stat_statements.last_exec_time`, per-process-type log verbosity, and enhanced autoanalyze statistics. Do not include PG19 features in production Fix Prompts until GA + first minor release (`https://versionlog.com/blog/postgresql-19-whats-coming-september-2026/`).

