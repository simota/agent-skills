# Index Performance Anti-Patterns

Purpose: Use this file when reviewing composite indexes, FK coverage, bloat, or index-health tradeoffs.

Contents:
1. Core anti-patterns
2. Composite ordering rules
3. Index-type guide
4. Health monitoring
5. Design gates

## Core Anti-Patterns

| ID | Anti-pattern | Signal | Safer pattern |
|----|--------------|--------|---------------|
| `IP-01` | Over-Indexing | `10+` indexes on one table or `20+` in extreme cases, writes slow down | Keep only indexes that serve real predicates or uniqueness |
| `IP-02` | Composite Order Mistake | Index exists but planner still uses sequential scan | Align order with `Equality -> Range -> Sort` |
| `IP-03` | Low Cardinality Index | Boolean / low-cardinality column uses a plain B-tree with little benefit | Use partial index, BRIN, or no index |
| `IP-04` | Missing FK Index | JOINs and cascades scan full tables | Add indexes on FK columns explicitly |
| `IP-05` | Index Bloat | Index size rivals or exceeds table size, dead tuples grow | Reindex, tune vacuum, review churn |
| `IP-06` | Expression Index Neglect | Queries use `LOWER(email)` or similar functions and miss indexes | Add expression index |
| `IP-07` | Covering Index Miss | Index scan still performs many heap fetches | Use `INCLUDE` or covering pattern |

## Composite Ordering Rules

- Respect the leftmost-prefix rule.
- Put equality predicates first.
- Put range predicates after equality predicates.
- Add sort columns last when the query benefits from index-order traversal.

Example:

```sql
WHERE status = 'active'
  AND customer_id = $1
  AND created_at > NOW() - INTERVAL '30 days'
ORDER BY created_at DESC
```

Preferred order:

```sql
(status, customer_id, created_at DESC)
```

## Index-Type Guide

| Need | Prefer |
|------|--------|
| Equality / range / sort | `B-tree` |
| JSONB / array contains / full-text tokens | `GIN` |
| Geospatial / nearest-neighbor / range types | `GiST` |
| Huge append-only time-series | `BRIN` |
| Expression lookup | Expression index |
| Partial subset | Partial index |

## Health Monitoring

Use monitoring queries for:
- unused indexes (`idx_scan < 50` is a strong candidate to review)
- duplicate or overlapping indexes
- index bloat and table-to-index size drift
- missing index pressure from heavy sequential scans

## Design Gates

- Table has `10+` indexes -> review for overlap or write cost
- FK without index -> add one unless a better covering/composite index already exists
- Boolean/ENUM B-tree index -> review for partial-index alternative
- `LOWER(...)` / `UPPER(...)` in predicates -> consider expression index
- Index storage exceeds table storage -> inspect for bloat or redundancy
- Frequent heap fetch after index scan -> consider covering index
