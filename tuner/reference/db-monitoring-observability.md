# Database Monitoring & Observability

Purpose: Use this file when the task is ongoing DB monitoring, alert design, or observability-driven tuning.

Contents:
- five monitoring pillars
- `pg_stat_statements` vs `pg_stat_monitor`
- alert thresholds
- dashboard guidance

## Five Monitoring Pillars

| ID | Pillar | Key metrics |
|----|--------|-------------|
| `MO-01` | query performance | p50/p95/p99 latency, slow-query count, executions |
| `MO-02` | resource usage | CPU, memory, disk I/O |
| `MO-03` | connection management | active/idle connections, pool usage, waiters |
| `MO-04` | locks and contention | lock wait time, deadlocks, contention rate |
| `MO-05` | maintenance health | autovacuum, table bloat, index bloat |

## `pg_stat_statements` vs `pg_stat_monitor`

| Tool | Best use |
|------|----------|
| `pg_stat_statements` | long-term trend analysis |
| `pg_stat_monitor` | deeper real-time debugging and richer dimensions |

Recommended `pg_stat_statements` posture:
- enable via `shared_preload_libraries`
- keep `track = 'top'` unless deeper nesting is necessary
- size `pg_stat_statements.max` to fit memory budget
- on **PG18+**, `pg_stat_statements` exposes ≥ 45 columns including a new `wal_buffers_full` column, and `IN (...)` lists are normalised more aggressively — refresh dashboards that bucketed on `query` text (`https://www.data-bene.io/en/blog/cumulative-statistics-in-postgresql-18/`)

## AI-Assisted SQL Tuning Platforms (2026-05)

These platforms layer rule + ML-driven tuning on top of `pg_stat_statements` / auto_explain output. Use as recommendation engines feeding Tuner — never as a substitute for plan-evidence review.

| Platform | Specialisation | 2026 capability surface |
|----------|----------------|-------------------------|
| **pganalyze** | PostgreSQL-only; deep root-cause analysis | Query / Index / VACUUM Advisor, auto_explain integration with per-query trace correlation; supports PG18 `wal_buffers_full` column and new `pg_stat_io` byte metrics (`https://pganalyze.com/comparison/pganalyze-vs-datadog`, `https://pganalyze.com/blog/postgres-18-async-io`) |
| **Datadog DBM** | Multi-engine; APM correlation | Auto-collects `EXPLAIN ANALYZE` for PostgreSQL, ingests auto_explain output, DBM Recommendations surface prioritised bottlenecks; EverSQL integration enables one-click SQL rewrite directly inside DBM (`https://www.datadoghq.com/blog/database-monitoring-explain-analyze/`, `https://docs.datadoghq.com/integrations/eversql/`) |
| **AWS DevOps Guru for RDS** | Aurora/RDS host-level ML | Anomaly detection on host metrics + slow query log; routes to Performance Insights |
| **Percona pg_stat_monitor** | PostgreSQL workload profiling | Bucket-based time-window aggregation, query plan capture per bucket, histogram view; compatible with PG13–18; more granular than `pg_stat_statements` for per-bucket P95/P99 (`https://docs.percona.com/pg-stat-monitor/`) |
| **pt-query-digest (Percona Toolkit 3.7.1)** | MySQL slow-log aggregation | Normalises queries to fingerprints; reports P95/P99 latency, rows-examined; supports `--review` for ongoing review workflow and `--history` for trend analysis; latest release 2026-04-17 (`https://docs.percona.com/percona-toolkit/pt-query-digest.html`) |
| **pg_qualstats + hypopg pipeline** | PostgreSQL index advising without builds | `pg_qualstats` tracks predicate access patterns; `pg_qualstats_index_advisor()` proposes candidates; hypopg validates each via `EXPLAIN` without building the real index; promote winners with `CREATE INDEX CONCURRENTLY` (`https://www.percona.com/blog/automatic-index-recommendations-in-postgresql-using-pg_qualstats-and-hypopg/`) |

Tuner contract: AI advisors generate **candidates**, not commitments. Always re-EXPLAIN against the actual workload, quantify the write overhead, and check adjacent queries for regression before accepting an AI-recommended index DDL.

### PostgreSQL 19 Forward-Look (monitoring, 2026-09 GA target)

`pg_stat_statements` will gain a `last_exec_time` column for last-execution tracking, per-process-type log verbosity (reducing debug-log volume explosions), and enhanced autoanalyze statistics. Do not rely on these in production Fix Prompts until PG19 GA + 19.1 minor (`https://versionlog.com/blog/postgresql-19-whats-coming-september-2026/`).

## Alert Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| query latency p95 | `> 500ms` | `> 2000ms` | investigate slow queries |
| connection usage | `> 80%` | `> 95%` | expand pool or find leaks |
| CPU usage | `> 75%` | `> 90%` | optimize workload or scale |
| memory usage | `> 80%` | `> 95%` | revisit memory settings |
| disk I/O latency | `> 10ms` | `> 50ms` | check indexes or storage |
| deadlocks | `> 0/hr` | `> 5/hr` | review transaction design |
| replication lag | `> 1s` | `> 10s` | inspect replica and network |
| table bloat | `> 20%` | `> 50%` | tune vacuum or reclaim space |
| autovacuum delay | `> 1hr` | `> 24hr` | tune autovacuum |
| unused index count | `> 5` | `> 20` | review removal candidates |

Operational quality gates:
- cache hit ratio `< 95%` -> revisit `shared_buffers` or indexing
- dead tuple ratio `> 20%` -> tune autovacuum

## Dashboard Guidance

Recommended panels:
- QPS and active connections
- p50/p95/p99 latency
- top slow queries
- cache hit ratio and disk I/O
- bloat and autovacuum status
- long transactions and deadlocks
