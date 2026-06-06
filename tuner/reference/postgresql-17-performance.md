# PostgreSQL 17 Performance Features

Purpose: Use this file when tuning PostgreSQL 17 or evaluating whether PG17 planner changes affect a recommendation.

Contents:
- 2026-05 status (why this file still matters)
- optimizer improvements
- vacuum changes
- bulk-load changes
- recommended settings
- upgrade checks

---

## 2026-05 Status (Why This File Still Matters)

PG17 is **no longer the latest stable major** as of 2026-05 — PG18 GA shipped 2025-09-25 (`https://www.postgresql.org/about/news/postgresql-18-released-3142/`) and the current PG17 minor is **17.8** (released 2026-05-14 alongside 18.4; `https://www.postgresql.org/about/news/postgresql-184-178-1612-1516-and-1421-released-3235/`). Use this file when:

- The cluster is still on PG17 (Aurora PostgreSQL-compatible cluster, RDS, GCP Cloud SQL fleets often lag a major behind), and an upgrade to PG18 is not yet scheduled.
- You are planning a PG17 → PG18 migration and need to know which 17.x planner behaviors will change.
- A managed service is pinned to PG17 because PG18 is not yet offered (verify in the provider release calendar: `https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html`).

For new deployments in 2026-05, the production default is **PG18 (currently 18.4)** — read `postgresql-18-performance.md` first. PG17 EOL is scheduled for **2029-11-08** per the PostgreSQL versioning policy (`https://www.postgresql.org/support/versioning/`).

Key behavior that changes when moving PG17 → PG18 (full list in `postgresql-18-performance.md`):
- `EXPLAIN (ANALYZE)` includes `BUFFERS` automatically on PG18 (PG17 still requires the explicit option).
- Async I/O subsystem (PG17 stayed synchronous; PG18 default is `io_method = worker`).
- `pg_upgrade` preserves planner statistics from PG14+ source by default on PG18 (PG17 required a full post-upgrade `ANALYZE`).
- Multicolumn B-tree Skip Scan (PG17 falls back to Seq Scan when leading column is absent from `WHERE`).
- `uuidv7()` is built in on PG18; on PG17 you need an extension or app-side generation.

## Query Optimizer Improvements

| Improvement | Typical effect | Notes |
|------------|----------------|-------|
| Streaming I/O | `~27%` faster seq scans | multiple-buffer reads |
| B-tree `IN` optimization | `~10%` faster | fewer leaf-page scans |
| correlated subquery -> `JOIN` conversion | can be dramatic, even `14000x` in best cases | verify actual plan |
| `UNION` optimization | `~15%` faster | better merge behavior |
| CTE statistics propagation | around `2x` on affected queries | planner sees more accurate stats |
| `IS NULL` on `NOT NULL` columns | huge plan simplification | unnecessary check removed |

## Vacuum And Bulk Operations

- vacuum memory footprint can drop significantly in PG17
- autovacuum becomes easier to run under concurrency
- `COPY` and large-row bulk operations can improve, sometimes near `2x`

## Recommended Settings

| Parameter | Suggested range |
|-----------|-----------------|
| `shared_buffers` | `25%` of RAM |
| `effective_cache_size` | `75%` of RAM |
| `work_mem` | `64MB-256MB` |
| `maintenance_work_mem` | `256MB-1GB` |
| `random_page_cost` | `1.1` for SSD |
| `jit` | on for complex-query workloads |
| `max_parallel_workers_per_gather` | `2-4` |

## Upgrade Validation

1. compare top queries with `EXPLAIN ANALYZE` before and after upgrade
2. compare top workload from `pg_stat_statements`
3. check vacuum memory behavior
4. benchmark `COPY` throughput
5. run `ANALYZE` after upgrade to refresh statistics
