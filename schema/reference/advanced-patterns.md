# Advanced Schema Patterns

Reference for event sourcing, CQRS projections, pgvector/AI schema, and bitemporal design.

---

## Event Sourcing Schema & CQRS Projections

Full event-store schema (events table, snapshots, projections, optimistic concurrency, aggregate boundaries, transactional outbox, schema evolution, anti-patterns) → `reference/event-sourcing-schema.md` (`event-sourcing` recipe). Not duplicated here.

---

## pgvector / AI Schema Extensions

> **2026-05 baseline:** pgvector 0.8.0 (released October 2024) is the current widely-deployed line; available on Amazon Aurora PostgreSQL, Neon, Tiger Data, Nile, and self-hosted Postgres 18. Key new capability: iterative index scans for filtered queries.

### Document Embeddings Table

```sql
CREATE EXTENSION IF NOT EXISTS vector;
-- On PostgreSQL 18 prefer uuidv7() for the row id when downstream consumers
-- want time-ordered insertion.
CREATE TABLE document_embeddings (
  id              UUID        PRIMARY KEY DEFAULT uuidv7(),
  source_id       UUID        NOT NULL,
  source_type     TEXT        NOT NULL,  -- 'article', 'product', 'support_ticket'
  chunk_index     INT         NOT NULL DEFAULT 0,
  content         TEXT        NOT NULL,
  embedding       halfvec(1536),         -- pgvector 0.8 halfvec — 50% the storage of vector
  embedding_model TEXT        NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  metadata        JSONB       NOT NULL DEFAULT '{}'
);

-- IVFFlat index (faster build, good for static datasets)
CREATE INDEX idx_embeddings_ivfflat
  ON document_embeddings
  USING ivfflat (embedding halfvec_cosine_ops)
  WITH (lists = 100);

-- HNSW index (slower build, better recall, good for dynamic datasets)
-- CREATE INDEX idx_embeddings_hnsw
--   ON document_embeddings
--   USING hnsw (embedding halfvec_cosine_ops)
--   WITH (m = 16, ef_construction = 64);
```

IVFFlat vs HNSW build speed / recall / memory / dynamic-insert trade-offs → `reference/index-strategies.md` § pgvector Index Selection. Not duplicated here.

### Hybrid Search SQL

```sql
-- Combine semantic similarity with keyword filter
SELECT
  d.id,
  d.source_id,
  d.content,
  1 - (d.embedding <=> $1::halfvec(1536)) AS similarity
FROM document_embeddings d
WHERE
  d.source_type = 'article'
  AND d.metadata @> '{"language": "en"}'::jsonb
ORDER BY d.embedding <=> $1::halfvec(1536)
LIMIT 20;
```

### Design Rules

1. Store the `embedding_model` (provider + name + version) so embeddings can be invalidated and regenerated when the model changes — a model swap requires re-embedding all rows.
2. Use `chunk_index` to track position within a document when chunking long text; consider `document_id + chunk_index` UNIQUE for idempotent re-ingest.
3. Match the operator class and query parameter type to the indexed column: `halfvec_cosine_ops` and `::halfvec(1536)` for this `halfvec` example; `vector_cosine_ops` and `::vector` for `vector` columns. Choose cosine, L2, or inner-product distance according to the embedding model's retrieval metric. Source: [pgvector operator-class definitions](https://github.com/pgvector/pgvector/blob/master/sql/vector.sql), verified 2026-09-13.
4. Add a GIN index on `metadata` if filtering by metadata fields is frequent.
5. **pgvector 0.8.0 iterative scans** (released Oct 2024): set `hnsw.iterative_scan = relaxed_order` (or `strict_order` when exact distance ordering matters) at the session/role level for WHERE-filtered KNN queries. Bound the work with `hnsw.max_scan_tuples` and tune `hnsw.scan_mem_multiplier` for highly-selective prefilters. Before 0.8, post-filter under-fetch was the #1 RAG quality bug.
6. **halfvec** reduces value storage to float16; measure recall for the workload. Its HNSW index supports up to 4 000 dimensions versus 2 000 for `vector`, so a 4 096-dimensional embedding still needs dimensionality reduction or another supported indexing strategy. Source: [pgvector supported types](https://github.com/pgvector/pgvector#supported-types), verified 2026-09-13.
7. Combine with structured prefilters (`tenant_id`, `language`, `source_type`) for order-of-magnitude latency gains over pure KNN; pgvector 0.8's improved planner statistics now make `WHERE tenant_id = $1 ORDER BY embedding <=> $2 LIMIT 20` plan correctly without query hints in most cases.

---

## Bitemporal Design

Bitemporal tables track two time axes independently:
- **Valid time** (`valid_from` / `valid_to`): when the fact was true in the real world.
- **Transaction time** (`recorded_at` / `invalidated_at`): when the database recorded the fact.

### Employee Contracts (Bitemporal) — PostgreSQL 18

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- Keep invalidated history; only current assertions must not overlap.
CREATE TABLE employee_contracts (
  id                UUID         PRIMARY KEY DEFAULT uuidv7(),
  employee_id       UUID         NOT NULL,
  role              TEXT         NOT NULL,
  salary            NUMERIC(10,2) NOT NULL,
  -- Valid time (business reality)
  valid_period      daterange    NOT NULL,
  -- Transaction time (audit trail)
  recorded_at       TIMESTAMPTZ  NOT NULL DEFAULT now(),
  invalidated_at    TIMESTAMPTZ  NOT NULL DEFAULT 'infinity',
  recorded_by       UUID         NOT NULL,
  CONSTRAINT no_current_valid_overlap EXCLUDE USING gist (
    employee_id WITH =,
    valid_period WITH &&
  ) WHERE (invalidated_at = 'infinity')
);

CREATE INDEX idx_contracts_employee_valid
  ON employee_contracts (employee_id, valid_period)
  WHERE invalidated_at = 'infinity';
```

### Pre-PG-18 (PostgreSQL ≤ 17) fallback

Use the same partial exclusion constraint on PostgreSQL 17; replace `uuidv7()` with `gen_random_uuid()`. A `WITHOUT OVERLAPS` key covers every row and cannot be restricted with a `WHERE` predicate, so it would reject a corrected row while the invalidated original remains. Use temporal keys for tables without retained overlapping versions; keep partial exclusion for this current-assertion pattern. Source: [PostgreSQL 18 CREATE TABLE](https://www.postgresql.org/docs/18/sql-createtable.html), verified 2026-09-13.

For a correction, use one transaction to invalidate the current row and insert its replacement. Require the invalidation to affect exactly one current row before inserting; serialize corrections for the employee or retry exclusion conflicts.

### Bitemporal vs SCD Type 2

| Dimension | Bitemporal | SCD Type 2 |
|-----------|-----------|------------|
| Time axes | Valid time + Transaction time | Valid time only |
| Retroactive corrections | Supported (invalidate old row, insert corrected row with original valid_from) | Not natively supported |
| Audit trail | Complete (who recorded what, when) | Partial (only current chain) |
| Query complexity | Higher | Lower |
| Use when | Compliance, audit, corrections to historical data | Analytics, slowly-changing dimensions |

### Design Gate

Apply bitemporal design when any of the following are true:
- The system must support **retroactive corrections** to historical records.
- Regulatory or audit requirements demand knowing what the database believed at a given time.
- Temporal queries like "what did the system show on 2023-06-01 for events in Q1 2023?" are required.


---

## pgvector Tuning and Replicated-Schema Maintenance

- For vector/AI workloads, prefer pgvector within PostgreSQL for ACID compliance and hybrid search (benchmarked at 50 M+ vectors with pgvectorscale). Use HNSW index (`m=16`, `ef_construction=64`; raise `ef_construction` to 256 for recall-critical workloads) for recall-performance balance; use IVFFlat only when index build time is the bottleneck. Use `halfvec` (float16) to halve memory with near-identical accuracy. Combine vector KNN with structured prefilters (e.g., `tenant_id`, `language`) for order-of-magnitude speedups over vector-only scans. On pgvector 0.8+, enable `SET hnsw.iterative_scan = relaxed_order` for filtered queries to prevent under-fetching when prefilters are selective — this iteratively widens the search until enough post-filter results are found. Tune `hnsw.scan_mem_multiplier` (multiple of `work_mem`) to improve recall on high-selectivity filtered queries by allowing larger in-memory candidate sets. Monitor P99 search latency; alert on > 2× baseline.

- PostgreSQL 18 logical replication does not propagate DDL. Coordinate schema migrations on every subscriber and the publisher; apply compatible additive changes to subscribers first. Details and official source: `reference/postgresql18-features.md`.
