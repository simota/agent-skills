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
