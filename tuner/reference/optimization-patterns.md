# Query Optimization Patterns

Purpose: Use this file when recommending common query rewrites, index checks, or index recommendation structure.

Contents:
- rewrite patterns
- missing-index detection
- unused-index detection
- index recommendation template

## Common Rewrites

| Before | After | Use when |
|--------|-------|----------|
| N+1 query loop | `JOIN` or batched `IN` query | repeated per-row fetches |
| deep subquery | `CTE` or `JOIN` | planner struggles or readability is poor |
| `OFFSET` pagination | cursor pagination | large offsets |

### N+1 -> JOIN

```sql
SELECT o.*, u.name
FROM orders o
JOIN users u ON o.user_id = u.id;
```

### Subquery -> CTE

```sql
WITH active_users AS (SELECT id FROM users WHERE active)
SELECT o.*
FROM orders o
JOIN active_users au ON o.user_id = au.id;
```

### OFFSET -> Cursor

```sql
SELECT *
FROM items
WHERE id > last_seen_id
ORDER BY id
LIMIT 20;
```

## Missing Index Checks

### PostgreSQL

```sql
SELECT
    schemaname || '.' || relname AS table,
    seq_scan,
    seq_tup_read,
    idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > 100
  AND seq_tup_read / GREATEST(seq_scan, 1) > 1000
ORDER BY seq_tup_read DESC
LIMIT 20;
```

### MySQL

```sql
SELECT
    t.TABLE_SCHEMA,
    t.TABLE_NAME,
    t.TABLE_ROWS,
    IFNULL(i.index_count, 0) AS index_count
FROM information_schema.TABLES t
LEFT JOIN (
    SELECT TABLE_SCHEMA, TABLE_NAME, COUNT(*) AS index_count
    FROM information_schema.STATISTICS
    GROUP BY TABLE_SCHEMA, TABLE_NAME
) i
ON t.TABLE_SCHEMA = i.TABLE_SCHEMA AND t.TABLE_NAME = i.TABLE_NAME
WHERE t.TABLE_TYPE = 'BASE TABLE'
  AND t.TABLE_ROWS > 10000
  AND IFNULL(i.index_count, 0) < 2
ORDER BY t.TABLE_ROWS DESC;
```

## Unused Index Checks

### PostgreSQL

```sql
SELECT
    schemaname || '.' || relname AS table,
    indexrelname AS index,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;
```

### MySQL

```sql
SELECT
    object_schema,
    object_name AS table_name,
    index_name,
    count_read,
    count_write
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE index_name IS NOT NULL
  AND count_read = 0
  AND object_schema NOT IN ('mysql', 'performance_schema')
ORDER BY count_write DESC;
```

## Index Recommendation Template

```markdown
## Index Recommendation: [Table].[Column(s)]

### Problem
- Query: `SELECT ...`
- Current plan: [plan]
- Execution time: [time]

### Proposed Index
```sql
CREATE INDEX CONCURRENTLY idx_table_column ON table (column);
```

### Expected Improvement
- Plan change: [before -> after]
- Expected execution time: [time]

### Trade-offs
- Disk space: [estimate]
- Write overhead: [estimate]

### Validation
- Re-run `EXPLAIN ANALYZE`
```
