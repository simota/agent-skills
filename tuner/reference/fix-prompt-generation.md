# Tuner LLM Fix Prompt Generation

**Purpose:** Tuner-specific action verbs, suppression cases, template fields, and worked example for the `## LLM Fix Prompt` block at the end of every Tuner performance report.
**Read when:** You are writing the `## LLM Fix Prompt` block for a Tuner report, choosing an action verb, or deciding whether to suppress.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Tuner-specific verbs, suppression cases, template fields, and an example.

## Contents

- Tuner action verbs
- Verb selection heuristic
- Tuner-specific suppression cases
- Per-finding fix prompt template (Tuner-specific fields)
- Worked example

---

## Tuner Action Verbs

Each fix prompt declares one verb at the top of `# Your task`.

| Verb | When to use | Receiving agent |
|------|-------------|----------------|
| `OPTIMIZE-QUERY` | Query plan fix (rewrite, hint, parameterization, JOIN order, predicate pushdown) | Builder |
| `ADD-INDEX` | Schema-level index addition (single/composite/partial/covering); coordinate with Schema for migration | Schema → Builder |
| `BREAKING-OPTIMIZE` | Query/schema change with API or contract impact (response shape, pagination semantics) | Builder + Guardian + Launch |
| `MIGRATE-WORKLOAD` | Structural — different query pattern needed (batched fetch, materialized view, denormalization) | Atlas + Builder + Schema |
| `INVESTIGATE-FURTHER` | EXPLAIN ANALYZE inconclusive; need production trace (pg_stat_statements, slow log) before deciding | Beacon (data collection) or Tuner re-entry |
| `MITIGATE` | Cache layer / materialized view / read replica routing while query is fixed | Builder + Bolt |

---

## Verb Selection Heuristic

```
Plan evidence == HIGH confidence ─┬─ scoped query rewrite ─────────────→ OPTIMIZE-QUERY
                                   ├─ index gap, no API change ─────────→ ADD-INDEX
                                   ├─ API contract must change ─────────→ BREAKING-OPTIMIZE
                                   └─ structural redesign required ──────→ MIGRATE-WORKLOAD

Plan evidence == MEDIUM (single EXPLAIN sample, no workload trace) ──→ INVESTIGATE-FURTHER

Underlying fix blocked / coordinator unavailable ──→ MITIGATE (cache/MV/read replica)
```

Tiebreakers:
- Always quantify write overhead for `ADD-INDEX` — if the table has high write traffic and the read gain is marginal, downgrade to `INVESTIGATE-FURTHER` and request workload data.
- For 100M+ row tables, `ADD-INDEX` MUST cite `CREATE INDEX CONCURRENTLY` (PostgreSQL) and the concurrent-build verification step.
- If the query owner is a 3rd-party ORM/library where Tuner cannot rewrite, suppress the prompt and document the upstream coordination instead.
- For pgvector / vector search bottlenecks, route via `MIGRATE-WORKLOAD` (HNSW vs IVFFlat + filter strategy is a structural change), not `OPTIMIZE-QUERY`.

---

## Tuner-Specific Suppression Cases

Universal cases live in `_common/LLM_PROMPT_GENERATION.md`. Tuner adds:

| Case | Reason | Note in report |
|------|--------|----------------|
| Tuner hands off to Schema for migration ownership (Schema owns the migration prompt) | Schema owns DDL migration coordination | "Fix prompt suppressed — Schema owns migration prompt; this report covers query plan analysis only." |
| Tuner hands off to Bolt for app-level caching (caching is the better fix) | Bolt owns application-level caching | "Fix prompt suppressed — Bolt owns caching remediation prompt." |
| Analysis-only mode (slow query inventory without remediation scope) | Out of scope for this engagement | "Fix prompt withheld per scope: analysis only." |
| Query is owned by 3rd-party ORM/library where Tuner cannot rewrite | Coordination is upstream, not in-repo | "Fix prompt withheld — query owned by [library]; coordinate upstream." |

---

## Per-Finding Fix Prompt Template (Tuner Fields)

Tuner adds these Tuner-specific blocks on top of the universal skeleton:

- `Slow query`: verbatim query text (parameterize secrets if any)
- `Current plan`: EXPLAIN ANALYZE output snippet showing the bottleneck (Seq Scan, Nested Loop, Sort, etc.)
- `Plan after fix (estimated)`: predicted EXPLAIN snippet showing the improvement (Index Scan, Hash Join, etc.)
- `Workload context`: rows scanned / rows returned / cost / actual time / index usage
- `Bottleneck classification`: missing index | suboptimal join order | missing predicate pushdown | N+1 | over-fetching | type mismatch | row-estimate skew | etc.
- `Database system`: PostgreSQL / MySQL / SQL Server / Oracle / etc. + version (planner behavior differs across versions)

````markdown
## LLM Fix Prompt

```text
# Your task
<VERB> the database performance finding described below.

# Finding context
- Title: [brief description]
- Severity: [Critical | High | Medium | Low] (relative to user-facing latency target)
- Confidence: [HIGH | MEDIUM | LOW] (Tuner's plan-evidence confidence)
- Database system: [PostgreSQL 18 | MySQL 8.4 | etc.]
- Bottleneck classification: [missing index | suboptimal join order | N+1 | etc.]

# Slow query
```sql
[verbatim query text — parameterize secrets]
```

Location: [file:line where the query is constructed, e.g., `src/server/orders/handler.ts:88` in `loadOrders()`]

# Current plan (EXPLAIN ANALYZE BUFFERS)
```
[snippet of plan output — focus on the bottleneck node]
Planning Time: [N] ms
Execution Time: [N] ms
```

# Workload context
- Table size: [row count]
- Rows scanned vs returned: [N scanned / M returned] (selectivity = M/N)
- Buffer hits / reads: [shared hit=N read=M]
- Row-estimate ratio: [estimate vs actual] ([Nx ratio — flag >10x stale, >100x unreliable])
- Frequency: [QPS or daily count from pg_stat_statements / slow log]
- P99 latency: [ms] (target: ≤200ms user-facing, ≤500ms background)

# Plan after fix (estimated)
```
[predicted plan after the change — Index Scan, Hash Join, etc.]
Estimated Execution Time: [N] ms (vs current [M] ms — Nx improvement)
```

# Recommended action
Approach: [strategy — query rewrite / index DDL / batched fetch / etc.]
Files / DDL to modify:
- [file or migration with expected change]

[For ADD-INDEX, include the DDL:]
```sql
-- PostgreSQL production-safe form
CREATE INDEX CONCURRENTLY idx_<table>_<cols> ON <table> (<cols>) [INCLUDE (<covering>)] [WHERE <predicate>];
```

Constraints:
- Write overhead estimate: [INSERT/UPDATE/DELETE cost increase, e.g., "+5% on hot writes"]
- Lock risk: [acquired locks, expected duration; CONCURRENTLY required for >1M row tables]
- Backward-compat: [response shape preserved | breaking — see Rollback]

# [BREAKING-OPTIMIZE / MIGRATE-WORKLOAD only — User-facing impact]
- API shape change: [yes/no — describe]
- Pagination semantics: [unchanged / cursor-based / etc.]
- Migration strategy for clients: [list]

# [BREAKING-OPTIMIZE only — Rollback plan]
- How to revert: [drop index, restore query, feature flag, etc.]
- Pre-deploy verification: [staging benchmark, canary rollout]

# Acceptance criteria
- [ ] EXPLAIN ANALYZE BUFFERS on the fixed query confirms the predicted plan (no Seq Scan / Sort / N+1)
- [ ] P99 latency improvement matches estimate (within ±20%)
- [ ] Row-estimate ratio < 10× (re-run ANALYZE if stale stats are involved)
- [ ] Write overhead measured and within constraint budget (for ADD-INDEX)
- [ ] No regression in adjacent query plans (run benchmark suite)
- [ ] [PostgreSQL 18+] Index lookup count matches expected scan pattern (especially for skip-scan)

# Ruled-out alternatives (do not revisit)
- [alternative 1] — eliminated because [evidence: e.g., another query depends on existing index]
- [alternative 2] — eliminated because [evidence: e.g., MV maintenance cost exceeds query gain]

# What NOT to do
- Do not silence the symptom by raising P99 thresholds or adding generic timeout retries
- Do not `CREATE INDEX` without `CONCURRENTLY` on production tables exceeding 1M rows
- Do not drop existing indexes without confirming usage via `pg_stat_user_indexes` / `sys.dm_db_index_usage_stats` over a full workload cycle
- Do not wrap indexed columns in functions (`WHERE YEAR(created_at) = 2026`) — rewrite as range conditions
- Do not use `SELECT *` in performance-critical paths — list columns to enable covering-index optimization
- Do not bundle unrelated query optimizations into the same migration
```
````

For `INVESTIGATE-FURTHER`, replace "Recommended action" with "Verification plan" (pg_stat_statements query, auto_explain config, or production trace request). For `MITIGATE`, add a "Cache strategy" block (TTL, invalidation, stampede guard).

---

## Worked Example (ADD-INDEX)

**Scenario:** Order history endpoint runs a Seq Scan on a 12M-row table because the composite filter+sort pattern lacks a matching composite index.

````markdown
## LLM Fix Prompt

```text
# Your task
ADD-INDEX the database performance finding described below.

# Finding context
- Title: Seq Scan on orders during /api/orders/history (user_id + created_at range + ORDER BY created_at)
- Severity: High (P99 = 2400ms vs 200ms target on user-facing endpoint)
- Confidence: HIGH (EXPLAIN ANALYZE BUFFERS + pg_stat_statements top-10 + reproduced in staging)
- Database system: PostgreSQL 18.1
- Bottleneck classification: missing composite index + redundant sort

# Slow query
```sql
SELECT id, user_id, total_amount, status, created_at
FROM orders
WHERE user_id = $1
  AND created_at >= $2
  AND created_at < $3
ORDER BY created_at DESC
LIMIT 50;
```

Location: `src/server/orders/handler.ts:88` in `loadHistory()`

# Current plan (EXPLAIN ANALYZE BUFFERS)
```
Limit  (cost=423012.10..423012.22 rows=50 width=72) (actual time=2387.4..2387.5 rows=50 loops=1)
  Buffers: shared hit=8124 read=412318
  ->  Sort  (cost=423012.10..423485.22 rows=189249 width=72)
        Sort Key: created_at DESC
        Sort Method: top-N heapsort  Memory: 38kB
        ->  Seq Scan on orders  (cost=0.00..416712.50 rows=189249 width=72)
              Filter: ((user_id = $1) AND (created_at >= $2) AND (created_at < $3))
              Rows Removed by Filter: 11814751
              Buffers: shared hit=8124 read=412318
Planning Time: 0.34 ms
Execution Time: 2387.61 ms
```

# Workload context
- Table size: 12,004,000 rows
- Rows scanned vs returned: 12,004,000 scanned / 50 returned (selectivity = 4.2e-6)
- Buffer hits / reads: shared hit=8124 read=412318 (99.4% disk reads — confirms no cache benefit)
- Row-estimate ratio: estimate 189,249 vs actual ~50 after sort+limit (~3800× over-estimate; not blocking but flag for autovacuum/ANALYZE)
- Frequency: 4,200 calls/min per pg_stat_statements (top-3 in workload)
- P99 latency: 2400ms (target: ≤200ms)

# Plan after fix (estimated)
```
Limit  (cost=0.43..52.18 rows=50 width=72) (actual time=0.18..1.42 rows=50)
  Buffers: shared hit=58
  ->  Index Scan Backward using idx_orders_user_created on orders
        Index Cond: ((user_id = $1) AND (created_at >= $2) AND (created_at < $3))
Estimated Execution Time: ~3 ms (vs current 2387 ms — ~800× improvement)
```

# Recommended action
Approach: Add a composite descending index on `(user_id, created_at DESC)` with an `INCLUDE` clause covering the SELECT columns, eliminating both the Seq Scan and the explicit Sort. The index serves the equality on user_id, the range on created_at, and the ORDER BY in a single backward index scan.

Files / DDL to modify:
- New migration: `migrations/20260501_orders_user_created_idx.sql`

```sql
-- PostgreSQL production-safe form
CREATE INDEX CONCURRENTLY idx_orders_user_created
  ON orders (user_id, created_at DESC)
  INCLUDE (id, total_amount, status);
```

Constraints:
- Write overhead estimate: +6% on INSERT (measured on staging copy via `pgbench -f insert.sql`); orders table has 1.2M inserts/day, so cost is acceptable
- Lock risk: `CREATE INDEX CONCURRENTLY` is required (12M rows, online traffic); estimated build duration ~28 min in staging, monitor for 60 min on production with `pg_stat_progress_create_index`
- Backward-compat: response shape unchanged; no API impact

# Acceptance criteria
- [ ] EXPLAIN ANALYZE BUFFERS on the production query shows `Index Scan Backward using idx_orders_user_created` (no Seq Scan, no explicit Sort)
- [ ] P99 latency for /api/orders/history drops below 200ms (current: 2400ms)
- [ ] Row-estimate ratio re-checked: planner estimate within 10× of actual after VACUUM ANALYZE
- [ ] Write overhead on INSERT measured at ≤10% (current baseline: 1.4ms/row → max 1.55ms/row)
- [ ] Index build completes via `CREATE INDEX CONCURRENTLY` (no exclusive lock on orders)
- [ ] No regression on `/api/orders/recent` and `/api/admin/orders` benchmark queries
- [ ] PostgreSQL 18 index lookup count per scan stays at 1 (no skip-scan degeneration into repeated scans)

# Ruled-out alternatives (do not revisit)
- Single-column index on `created_at` only — eliminated: leaves Seq Scan on filter, only helps the sort
- Single-column index on `user_id` only — eliminated: eliminates Seq Scan but explicit Sort remains; staging benchmark showed P99 = 480ms (still >target)
- Materialized view per-user — eliminated: 4M+ active users would explode the MV; MV refresh cost dominates
- Partitioning by `created_at` (monthly) — eliminated: pre-mature for 12M rows (Tuner threshold: 100M+); revisit if growth exceeds 30M rows
- Drop `orders.status` from response to enable a leaner covering index — eliminated: API contract requires status

# What NOT to do
- Do not `CREATE INDEX` without `CONCURRENTLY` — exclusive lock on a 12M-row table will block writes for 25+ minutes
- Do not silence the symptom by raising the P99 SLO target above 200ms — the latency is user-felt
- Do not drop the existing `idx_orders_user_id` index in the same migration — verify zero usage via `pg_stat_user_indexes` over a full week first; that is a separate cleanup PR
- Do not add additional indexes "while we're at it" — measure the write overhead budget impact one index at a time
- Do not skip the row-estimate sanity check — the 3800× over-estimate suggests stale statistics that may also affect adjacent queries
- Do not wrap `created_at` in functions (e.g., `WHERE DATE(created_at) = $1`) — that would defeat the new index
```
````

This prompt is self-contained: a coding LLM (or Schema for migration coordination) can act on it without seeing the rest of the Tuner report.
