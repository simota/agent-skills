# EXPLAIN ANALYZE Delta

Purpose: Tuner command selection and evidence contract. Plan-node definitions are model-known; interpretation must use the actual engine/version and runtime evidence.

## Safe Command Selection

```sql
-- PostgreSQL
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT ...;

-- MySQL
EXPLAIN ANALYZE SELECT ...;
EXPLAIN FORMAT=JSON SELECT ...;

-- SQLite
EXPLAIN QUERY PLAN SELECT ...;
```

`ANALYZE` executes the statement. Do not use it on mutating or expensive production queries without a safe transaction, representative replica, or explicit authorization. Redact sensitive literals from shared plans.

## Version Delta

PostgreSQL 18 reports buffer information by default for `EXPLAIN ANALYZE` and adds per-scan-node index lookup counts. Confirm the server version before relying on these fields; request `BUFFERS` explicitly for portable scripts.

## Interpretation Contract

- Compare estimated vs actual rows, loops, time, buffer hits/reads, temporary I/O, filters, and spill behavior.
- A sequential scan or nested loop is not inherently bad; judge it against relation size, selectivity, cache state, and total work.
- Treat the Critical Thresholds in `tuner/SKILL.md` as investigation triggers, not query-plan verdicts.
- Run comparable warm/cold and parameter cases where parameter sensitivity matters.
- State schema, statistics freshness, parameters, hardware/environment, and query timing.
- Recommend an index or rewrite only after explaining write/storage cost and validating with a before/after plan.
