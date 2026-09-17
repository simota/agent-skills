# Tuner LLM Fix Prompt Generation

**Purpose:** Tuner-specific action verbs, suppression cases, template fields for the `## LLM Fix Prompt` block at the end of every Tuner performance report.
**Read when:** You are writing the `## LLM Fix Prompt` block for a Tuner report, choosing an action verb, or deciding whether to suppress.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Tuner-specific verbs, suppression cases, template fields.

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
