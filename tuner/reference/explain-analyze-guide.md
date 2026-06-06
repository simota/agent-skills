# EXPLAIN ANALYZE Guide

Purpose: Use this file when interpreting execution plans or selecting the right `EXPLAIN` command for PostgreSQL, MySQL, or SQLite.

Contents:
- DB-specific `EXPLAIN` commands
- node meanings
- threshold table
- red flags

## Core Metrics

- `Actual Time`: real execution time in ms
- `Rows`: actual vs estimated rows
- `Loops`: number of iterations
- `Buffers`: shared hit/read counts

## Commands by Database

### PostgreSQL

```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM users WHERE email = 'test@example.com';
EXPLAIN (COSTS, VERBOSE)
SELECT * FROM users WHERE email = 'test@example.com';
```

**PG18+ behavior change**: `EXPLAIN (ANALYZE)` includes `BUFFERS` by default and `EXPLAIN ANALYZE` itself reports **per-scan-node index lookup counts** — essential for diagnosing skip-scan efficiency on multicolumn B-tree indexes (see `postgresql-18-performance.md`). On PG17 and earlier, `BUFFERS` must still be requested explicitly.

### MySQL

```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
EXPLAIN FORMAT=JSON SELECT * FROM users WHERE email = 'test@example.com';
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
SHOW WARNINGS;
```

### SQLite

```sql
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'test@example.com';
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

## Common Node Types

| Node | Meaning | Concern |
|------|---------|---------|
| `Seq Scan` | full table scan | missing or unusable index |
| `Index Scan` | index lookup | usually good |
| `Index Only Scan` | covered by index | best case |
| `Nested Loop` | row-by-row join | bad when both sides are large |
| `Hash Join` | hash-based join | watch memory and spills |
| `Sort` | in-memory or disk sort | check `work_mem` and index support |

## Thresholds

| Signal | Good | Warning | Critical |
|--------|------|---------|----------|
| `Seq Scan` | small tables `< 1K rows` | medium tables | large tables |
| `Rows` estimate vs actual | close | `> 10x` | `100x+` |
| `Nested Loop` | small inner side | medium inner side | large tables on both sides |
| `Sort` | index-backed or memory sort | large memory sort | disk sort |

## Red Flags

- `Seq Scan` on table `> 100K rows`
- estimated vs actual rows off by `100x+`
- `Sort Method: external merge Disk`
- `Nested Loop` with large outer and inner sets
- filters removing `> 90%` of rows after scanning
- hash join spilling to disk
