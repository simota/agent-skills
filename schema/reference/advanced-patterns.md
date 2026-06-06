# Advanced Schema Patterns

Reference for event sourcing, CQRS projections, pgvector/AI schema, and bitemporal design.

---

## Event Sourcing Schema

### Core Tables

```sql
-- Append-only event store
CREATE TABLE event_store (
  event_id        UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  aggregate_id    UUID        NOT NULL,
  aggregate_type  TEXT        NOT NULL,
  event_type      TEXT        NOT NULL,
  event_version   INT         NOT NULL,
  payload         JSONB       NOT NULL,
  metadata        JSONB       NOT NULL DEFAULT '{}',
  occurred_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (aggregate_id, event_version)
);

CREATE INDEX idx_event_store_aggregate ON event_store(aggregate_id, event_version);
CREATE INDEX idx_event_store_type_time ON event_store(aggregate_type, occurred_at);

-- Snapshot table for aggregate state cache
CREATE TABLE aggregate_snapshots (
  aggregate_id    UUID        PRIMARY KEY,
  aggregate_type  TEXT        NOT NULL,
  snapshot_data   JSONB       NOT NULL,
  last_event_id   UUID        NOT NULL REFERENCES event_store(event_id),
  last_version    INT         NOT NULL,
  taken_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Design Rules

1. `event_store` is **append-only** — never UPDATE or DELETE rows.
2. Use `(aggregate_id, event_version)` unique constraint to detect optimistic concurrency conflicts.
3. Rebuild projections from `event_store` on demand; snapshots are a performance optimization, not the source of truth.
4. Partition `event_store` by `occurred_at` for long-running systems (> 1M events/month).

---

## CQRS Projection Tables

Projections are read-optimized materialized views of aggregate state, updated by event handlers.

```sql
-- Order summary projection (read model)
CREATE TABLE order_summary_projection (
  order_id        UUID        PRIMARY KEY,
  tenant_id       UUID        NOT NULL,
  customer_id     UUID        NOT NULL,
  status          TEXT        NOT NULL,
  total_amount    NUMERIC(12,2) NOT NULL,
  item_count      INT         NOT NULL DEFAULT 0,
  created_at      TIMESTAMPTZ NOT NULL,
  updated_at      TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_order_summary_tenant_status ON order_summary_projection(tenant_id, status, created_at DESC);

-- Projection checkpoint tracker
CREATE TABLE projection_checkpoints (
  projection_name TEXT        PRIMARY KEY,
  last_event_id   UUID,
  last_position   BIGINT      NOT NULL DEFAULT 0,
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

**Design rules:**
- Projections can be dropped and rebuilt from `event_store` at any time — they are dispensable.
- Use `projection_checkpoints` to track replay progress and support resumable rebuilds.
- Keep projections in a separate schema (`read_models`) to make the CQRS boundary explicit.

---

## pgvector / AI Schema Extensions

> **2026-05 baseline:** pgvector 0.8.0 (released October 2024) is the current widely-deployed line; available on Amazon Aurora PostgreSQL, Neon, Tiger Data, Nile, and self-hosted Postgres 18. Key new capability: iterative index scans for filtered queries.

### Document Embeddings Table

```sql
-- Requires: CREATE EXTENSION vector;
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
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- HNSW index (slower build, better recall, good for dynamic datasets)
-- CREATE INDEX idx_embeddings_hnsw
--   ON document_embeddings
--   USING hnsw (embedding vector_cosine_ops)
--   WITH (m = 16, ef_construction = 64);
```

### IVFFlat vs HNSW Comparison

| Dimension | IVFFlat | HNSW |
|-----------|---------|------|
| Build speed | Fast (minutes) | Slow (hours for large datasets) |
| Search recall | ~95% at nprobe=10 | ~99% at ef=64 |
| Memory usage | Low | High (graph stored in RAM) |
| Dynamic inserts | Requires periodic rebuild | Fully dynamic |
| Recommended for | Batch-loaded, static datasets | Live-updated, recall-critical datasets |
| Key parameter | `lists = sqrt(n_rows)` | `m = 16`, `ef_construction = 64` |

### Hybrid Search SQL

```sql
-- Combine semantic similarity with keyword filter
SELECT
  d.id,
  d.source_id,
  d.content,
  1 - (d.embedding <=> $1::vector) AS similarity
FROM document_embeddings d
WHERE
  d.source_type = 'article'
  AND d.metadata @> '{"language": "en"}'::jsonb
ORDER BY d.embedding <=> $1::vector
LIMIT 20;
```

### Design Rules

1. Store the `embedding_model` (provider + name + version) so embeddings can be invalidated and regenerated when the model changes — a model swap requires re-embedding all rows.
2. Use `chunk_index` to track position within a document when chunking long text; consider `document_id + chunk_index` UNIQUE for idempotent re-ingest.
3. Choose `vector_cosine_ops` for normalized embeddings (OpenAI text-embedding-3-*, Cohere, most sentence-transformers); use `vector_l2_ops` for unnormalized embeddings; `vector_ip_ops` (inner product) for some specialised models.
4. Add a GIN index on `metadata` if filtering by metadata fields is frequent.
5. **pgvector 0.8.0 iterative scans** (released Oct 2024): set `hnsw.iterative_scan = relaxed_order` (or `strict_order` when exact distance ordering matters) at the session/role level for WHERE-filtered KNN queries. Bound the work with `hnsw.max_scan_tuples` and tune `hnsw.scan_mem_multiplier` for highly-selective prefilters. Before 0.8, post-filter under-fetch was the #1 RAG quality bug.
6. **halfvec** halves storage (float16) with negligible recall loss for most workloads and lifts the HNSW 2 000-dimension ceiling for `vector` — required for embeddings > 2 000 dims (e.g., Cohere embed-v3 4 096).
7. Combine with structured prefilters (`tenant_id`, `language`, `source_type`) for order-of-magnitude latency gains over pure KNN; pgvector 0.8's improved planner statistics now make `WHERE tenant_id = $1 ORDER BY embedding <=> $2 LIMIT 20` plan correctly without query hints in most cases.

---

## Bitemporal Design

Bitemporal tables track two time axes independently:
- **Valid time** (`valid_from` / `valid_to`): when the fact was true in the real world.
- **Transaction time** (`recorded_at` / `invalidated_at`): when the database recorded the fact.

### Employee Contracts (Bitemporal) — PostgreSQL 18 idiom

```sql
-- PostgreSQL 18 ships SQL:2011 temporal PKs (WITHOUT OVERLAPS) and FKs (PERIOD).
-- The valid-time uniqueness no longer needs a hand-rolled GiST exclusion constraint.
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
  -- PG 18: temporal PK rejects overlapping valid-time ranges per employee.
  UNIQUE (employee_id, valid_period WITHOUT OVERLAPS)
);

CREATE INDEX idx_contracts_employee_valid
  ON employee_contracts (employee_id, valid_period)
  WHERE invalidated_at = 'infinity';
```

### Pre-PG-18 (PostgreSQL ≤ 17) fallback

If your cluster is still on PG 17 or earlier, keep the `EXCLUDE USING gist` form below — it remains the only in-database way to enforce non-overlap.

```sql
ALTER TABLE employee_contracts
  ADD CONSTRAINT no_valid_overlap EXCLUDE USING gist (
    employee_id WITH =,
    daterange(valid_from, valid_to, '[)') WITH &&
  ) WHERE (invalidated_at = 'infinity');
```

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
