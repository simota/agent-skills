# Tuner Boundaries — Rationale and Case Detail

Full rationale for each `Never` rule in `SKILL.md`. Kept out of the routing shell because the one-line rule is enough to enforce the boundary; the case detail exists for when a user or agent pushes back and needs the "why".

- **Run heavy exploratory queries on production without approval.** Uncontrolled scans compete with production workload for buffers and I/O.
- **Drop indexes without understanding usage.** A retail company dropped an "unused" index that was critical for a nightly batch job, causing 8-hour processing delays discovered only at month-end.
- **Recommend changes without execution-plan evidence.** Guesswork recommendations without `EXPLAIN` evidence are unverifiable and often wrong.
- **Ignore write overhead or lock risk.** Non-concurrent index creation on a 100M+ row table can lock writes for hours; always use `CREATE INDEX CONCURRENTLY` in PostgreSQL production.
- **Assume uniform data distribution.** Skewed data (e.g., 90% of orders in "completed" status) makes generic index advice dangerous; always check `pg_stats` column histograms.
- **Use `SELECT *` in performance-critical paths.** Transferring unnecessary columns wastes network bandwidth and prevents covering-index optimizations.
- **Wrap indexed columns in functions** (e.g., `WHERE YEAR(created_at) = 2026`). This prevents index usage and forces full table scans; rewrite as range conditions.
- **Use random UUIDv4 as primary key on high-write tables without considering fragmentation cost.** Random inserts scatter across B-tree pages, causing ~30× more buffer hits than time-ordered UUIDv7 or bigserial; on PostgreSQL 18+ recommend `uuidv7()` instead.
- **Use `OFFSET` pagination on tables exceeding a few thousand rows.** PostgreSQL reads, sorts, and discards all rows up to the offset, causing linear degradation (benchmarks show 17× slower at deep pages); recommend keyset/cursor pagination (`WHERE (sort_col, id) > (last_val, last_id) ORDER BY sort_col, id LIMIT N`) with a composite index instead.
- **Use `NOT IN (SELECT ...)` on subqueries returning many rows.** The plain subplan is **O(N²)** per outer row; small-scale tests look fine, then performance collapses by 5+ orders of magnitude once a size threshold is crossed. `NOT IN` also returns unexpected empty results when the subquery contains any NULL row. Rewrite as `NOT EXISTS (SELECT 1 ... WHERE ...)` or a LEFT JOIN / `IS NULL` anti-join.
