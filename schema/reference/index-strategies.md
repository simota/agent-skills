# Index Strategy Guide

Purpose: Use this file when selecting index type, composite order, or monitoring strategy.

Contents:
1. Index type selection
2. Composite index rules
3. Partial and covering indexes
4. Monitoring queries

## Index Type Selection

| Query pattern | PostgreSQL | MySQL |
|--------------|------------|-------|
| Exact match (`=`) | `B-tree` | `B-tree` |
| Range (`>`, `<`, `BETWEEN`) | `B-tree` | `B-tree` |
| Full-text search | `GIN (tsvector)` | `FULLTEXT` |
| JSON field lookup | `GIN (jsonb)` | Virtual column + `B-tree` |
| Array membership | `GIN` | N/A |
| Geospatial | `GiST` | `SPATIAL` |

## Composite Index Rules

- Order columns as `Equality -> Range -> Sort`.
- Respect the leftmost-prefix rule.
- Prefer the actual predicate order over abstract “important columns”.

Example:

```sql
WHERE status = 'active' AND created_at > '2024-01-01' ORDER BY name
```

Preferred index:

```sql
(status, created_at, name)
```

## Partial And Covering Indexes

| Pattern | Use when | Example |
|--------|----------|---------|
| Partial index | Query targets a stable subset | `WHERE deleted_at IS NULL` |
| Covering index | Heap fetch cost dominates | `INCLUDE (name, email)` |

```sql
CREATE INDEX idx_active_users
  ON users(email)
  WHERE deleted_at IS NULL;

CREATE INDEX idx_covering_users
  ON users(status)
  INCLUDE (name, email);
```

## Monitoring Queries

```sql
-- Unused indexes (PostgreSQL)
SELECT indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE NOT indisunique AND idx_scan < 50;

-- Missing-index hints
SELECT relname, seq_scan - idx_scan AS too_much_seq
FROM pg_stat_user_tables
WHERE seq_scan - idx_scan > 100;
```

---

## pgvector Index Selection

Use this table when adding a vector similarity index to a table with `vector` columns.

| Dimension | IVFFlat | HNSW |
|-----------|---------|------|
| Build speed | Fast (minutes for 1M rows) | Slow (hours for 1M rows) |
| Search recall | ~95% at `nprobe=10` | ~99% at `ef_search=64` |
| Memory usage | Low (inverted file on disk) | High (full graph in RAM) |
| Dynamic inserts | Degrades; needs periodic `REINDEX` | Fully dynamic, no rebuild needed |
| Recommended params | `lists = sqrt(n_rows)` | `m = 16`, `ef_construction = 64` |
| Best for | Batch-loaded static datasets | Live-updated, recall-critical datasets |

```sql
-- IVFFlat: choose lists = sqrt(row_count), e.g. 100 for 10k rows
CREATE INDEX idx_embeddings_ivfflat
  ON document_embeddings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- HNSW: better recall, higher memory cost
CREATE INDEX idx_embeddings_hnsw
  ON document_embeddings
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
```

**Operator class selection:**
- `vector_cosine_ops` — normalized embeddings (OpenAI, Cohere, most transformers)
- `vector_l2_ops` — unnormalized embeddings, Euclidean distance
- `vector_ip_ops` — inner product (dot product similarity)
