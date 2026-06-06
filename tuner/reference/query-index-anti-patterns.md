# Query & Index Anti-Patterns

Purpose: Use this file when screening query and index mistakes before proposing a tuning change.

Contents:
- `QA-01..06`
- `IA-01..06`
- detection rules
- optimization flow

## Query Anti-patterns

| ID | Anti-pattern | Risk | Preferred response |
|----|--------------|------|--------------------|
| `QA-01` | `SELECT *` | over-fetching and no covering benefit | select only required columns |
| `QA-02` | function-wrapped column | index becomes unusable | rewrite to range predicate or expression index |
| `QA-03` | implicit type conversion | index may be skipped | align types |
| `QA-04` | heavy `OR` conditions | planner may choose seq scan | split to `UNION ALL` or use better composite strategy |
| `QA-05` | leading `%` in `LIKE` | B-tree unusable | full-text, `pg_trgm`, or alternate strategy |
| `QA-06` | deeply nested subqueries | poor planner leverage | rewrite with `CTE` or `JOIN` |

## Index Anti-patterns

| ID | Anti-pattern | Risk | Preferred response |
|----|--------------|------|--------------------|
| `IA-01` | over-indexing | write slowdown and storage waste | keep only query-backed indexes |
| `IA-02` | redundant indexes | duplicate write cost | detect and report deletion candidates |
| `IA-03` | wrong column order in composite index | index not used as intended | match `WHERE` and `ORDER BY` access path |
| `IA-04` | B-tree on low-cardinality column | planner still picks seq scan | consider partial index |
| `IA-05` | unused indexes left behind | write overhead only | review `idx_scan = 0` regularly |
| `IA-06` | production `CREATE INDEX` without `CONCURRENTLY` | write blocking | use `CREATE INDEX CONCURRENTLY` |

## Detection Rules

- grep `pg_stat_statements` for `YEAR(...)`, `DATE(...)`, `LOWER(...)`, casts, or wrapped predicates
- inspect `EXPLAIN FORMAT=JSON` for type-conversion clues in MySQL
- use `pg_stat_user_indexes` to find `idx_scan = 0`
- compare `(a)` vs `(a, b)` to detect redundant prefixes

## Optimization Flow

1. Run `EXPLAIN ANALYZE`.
2. If `Seq Scan` is the issue:
   - no index -> consider a new index
   - index exists but is unused -> check `QA-02`, `QA-03`, `IA-04`, or small-table exception
   - stale stats -> refresh statistics
3. If `Nested Loop` is the issue:
   - add inner-side index or test alternative join strategy
4. If `Sort` is the issue:
   - check `work_mem`
   - consider sort-supporting index
5. If repeated row-by-row access appears, treat it as N+1.
