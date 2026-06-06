# Database-Specific Optimizations & Query Plan Visualization

Purpose: Use this file when you need DB-specific tuning baselines or want to visualize a query plan for `Canvas`.

Contents:
- PostgreSQL baseline settings
- MySQL baseline settings
- SQLite baseline settings
- Canvas query-plan visualization

## PostgreSQL Baseline

- `shared_buffers`: `25%` of RAM
- `work_mem`: `RAM / max_connections / 4`
- `effective_cache_size`: `75%` of RAM
- `random_page_cost`: `1.1` for SSD, `4.0` for HDD
- maintain with regular `VACUUM ANALYZE`
- consider partial, covering, BRIN, and expression indexes where appropriate

## MySQL Baseline (2026-05)

- `innodb_buffer_pool_size`: `70%` of RAM
- `innodb_log_file_size`: `256M-2G`
- `query_cache_size`: `0` (the query cache was removed in MySQL 8.0)
- `tmp_table_size` / `max_heap_table_size`: `64M-256M`
- maintain with `ANALYZE TABLE`, `OPTIMIZE TABLE`, and online schema tools when needed

### MySQL Version Posture

- **MySQL 8.4 LTS** is the current long-term support line. The current 2026-05 minor is **8.4.9 (2026-04-21)** (`https://dev.mysql.com/doc/relnotes/mysql/8.4/en/news-8-4-9.html`).
- **MySQL 9.x is the Innovation track** — 9.5.0 ships in HeatWave alongside 8.4.7 / 8.0.44 (`https://docs.oracle.com/en-us/iaas/releasenotes/mysql-database/TC-40295-heatwave-950-847-8044.htm`). Innovation releases add features (vector store, JS stored procedures on HeatWave) but only get bug fixes for one quarter — **do not use 9.x for production unless you can re-baseline every quarter**.
- **MySQL 8.0** approaches EOL: Oracle's HeatWave fleet will be auto-upgraded to 8.4 LTS in 2027 after the **April 2027 final security update for 8.0** (`https://blogs.oracle.com/mysql/extending-mysql-8-0-support-in-mysql-heatwave`). Plan the 8.0 → 8.4 LTS migration now.
- **HeatWave Vector Store** is paid-only — vector + JavaScript stored procedures are not in MySQL Community Edition (`https://dev.mysql.com/doc/heatwave/en/mys-hw-genai-vector-store-overview.html`). For OSS MySQL vector workloads, route to a sidecar vector DB or PlanetScale's native vector type instead.

## SQLite Baseline

- `PRAGMA journal_mode = WAL`
- `PRAGMA synchronous = NORMAL`
- `PRAGMA cache_size = -64000`
- `PRAGMA temp_store = MEMORY`
- run `ANALYZE` after bulk changes
- remember limited concurrent writes and no parallel query execution

## Canvas Query-Plan Visualization

Tuner can hand a query plan to `Canvas` as Mermaid input.

Example packet:

```markdown
/Canvas visualize query plan

Query: SELECT ...
Plan nodes:
1. Limit
2. Sort - 500ms
3. Hash Join - 200ms
4. Seq Scan users - 800ms <- bottleneck
5. Index Scan orders - 50ms
```

Use this when a diagram will help explain the bottleneck or compare before/after plans.
