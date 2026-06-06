# Materialized Views & Table Partitioning

Purpose: Use this file when deciding whether to use materialized views, summary tables, or partitioning.

Contents:
- materialized-view decision rules
- PostgreSQL and MySQL patterns
- partitioning thresholds
- maintenance rules

## Materialized Views

### Decision Rules

| Scenario | Use MV? | Reason |
|----------|---------|--------|
| complex aggregation | Yes | avoids repeated computation |
| dashboard queries | Yes | predictable and cacheable |
| real-time data | No | staleness is unacceptable |
| infrequent queries | No | storage and refresh cost not justified |
| high-write tables | Depends | refresh cost may outweigh benefit |

### PostgreSQL

```sql
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT DATE(created_at) AS sale_date, product_id, SUM(amount) AS total_amount
FROM orders
GROUP BY DATE(created_at), product_id
WITH DATA;

CREATE INDEX idx_mv_daily_sales_date ON mv_daily_sales(sale_date);
CREATE UNIQUE INDEX idx_mv_daily_sales_pk ON mv_daily_sales(sale_date, product_id);
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales;
```

Rules:
- use `REFRESH CONCURRENTLY` for zero-downtime refresh
- `CONCURRENTLY` requires a unique index
- validate refresh cadence against staleness tolerance

### MySQL Alternative

MySQL has no native materialized views. Use a summary table plus scheduled refresh:
- table for precomputed aggregates
- refresh procedure or job
- event scheduler or external orchestrator

## Partitioning

### Decision Matrix

| Table Size | Query Pattern | Partition? | Strategy |
|------------|---------------|------------|----------|
| `< 10M rows` | any | No | index tuning first |
| `10M-100M` | time-based | Yes | range by date |
| `10M-100M` | category-based | Yes | list by category |
| `> 100M` | mixed patterns | Yes | composite strategy |
| any | full table scans only | No | partitioning will not rescue bad access patterns |

### PostgreSQL Pattern

```sql
CREATE TABLE orders (
    id BIGSERIAL,
    created_at TIMESTAMP NOT NULL
) PARTITION BY RANGE (created_at);
```

Maintenance rules:
- create future partitions before they are needed
- verify partition pruning in `EXPLAIN`
- archive or drop old partitions deliberately
- prefer `pg_partman` when partition maintenance is recurring

### MySQL Pattern

Use range partitions with the partition key included in the primary key and verify pruning with `EXPLAIN`.
