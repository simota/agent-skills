# Vector Search Query Optimization

Purpose: Use this file when optimizing pgvector queries, tuning HNSW/IVFFlat indexes, or diagnosing filtered vector search performance.

Contents:
- 2026-05 pgvector version posture
- pgvector 0.8.0 Iterative Scan
- HNSW vs IVFFlat comparison
- Index parameter tuning
- Filter optimization patterns
- EXPLAIN ANALYZE for vector queries
- Production recommended settings

---

## 2026-05 pgvector Version Posture

The supported pgvector lineage as of 2026-05:

| Version | Headline change | When to choose |
|---------|-----------------|----------------|
| `0.7.x` | `halfvec` (2-byte floats, up to 4000 dims), `sparsevec` (up to 1000 nonzero dims), `bit` binary vectors (up to 64000 dims); scalar quantization | Reduce storage/memory 50%+ for float32 embeddings via halfvec (`https://www.postgresql.org/about/news/pgvector-070-released-2852/`) |
| `0.8.x` | HNSW iterative scan (`hnsw.iterative_scan`), parallel HNSW build; up to 5.7× QPS improvement for filtered queries vs 0.7.4 | Production default if managed service supports it (Aurora `pgvector 0.8.0` available since 2025; `https://aws.amazon.com/blogs/database/supercharging-vector-search-performance-and-relevance-with-pgvector-0-8-0-on-amazon-aurora-postgresql/`) |
| `0.9.x` (early 2026) | IVFFlat improvements, sparse vector support, further speed boosts (`https://callsphere.ai/blog/vector-database-benchmarks-2026-pgvector-qdrant-weaviate-milvus-lancedb`) | When self-managing PG and the dataset has high filter selectivity, sparse-vector use cases, or large IVFFlat indexes |

Benchmarks (1M vectors, ann-benchmarks-style):
- pgvector **HNSW @ ef_search=100**: p50 ≈ 2.1ms, p99 ≈ 4.3ms, recall@10 ≈ 0.971.
- Qdrant default HNSW: p50 ≈ 1.8ms, p99 ≈ 3.6ms, recall@10 ≈ 0.978.
- HNSW parallel build (PG17+ background workers) cut build time **30–50% on multi-core hosts** for 1M-vector indexes (`https://callsphere.ai/blog/vector-database-benchmarks-2026-pgvector-qdrant-weaviate-milvus-lancedb`).

Trade-off rule: **stay on pgvector** when the workload is dominated by hybrid relational+vector queries inside one transaction. Move to a dedicated vector DB (Qdrant, Weaviate, Milvus, LanceDB) only when (a) raw QPS is the binding constraint, (b) the recall budget is tighter than what HNSW + iterative scan delivers, or (c) sparse + dense + lexical fusion is required.

For TimescaleDB-style time-series + vector hybrid workloads, **Timescale rebranded to Tiger Data in June 2025** (`https://www.tigerdata.com/blog/timescale-becomes-tigerdata`); the vector extension is now `pgvectorscale` (Streaming DiskANN) and ships alongside Hypercore (hybrid row/columnar engine) on Tiger Cloud.

---

## pgvector 0.8.0: Iterative Scan

pgvector 0.8.0 introduced Iterative Scan for HNSW indexes, enabling accurate filtered vector search by progressively expanding the search until enough results meeting the filter condition are found.

### New Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `hnsw.iterative_scan` | `off` | Enable iterative scan: `off`, `relaxed_order`, `strict_order` |
| `hnsw.max_scan_tuples` | `20000` | Maximum tuples to scan per query |
| `hnsw.scan_mem_multiplier` | `1.0` | Memory multiplier for scan buffer |

### Iterative Scan Modes

| Mode | Behavior | Use when |
|------|----------|----------|
| `off` | Standard HNSW scan (no iteration) | No WHERE filter on vector queries |
| `relaxed_order` | Results may not be strictly ordered by distance | Acceptable for approximate nearest-neighbor with filter |
| `strict_order` | Strict distance ordering preserved | Exact order required with filter |

```sql
-- Enable iterative scan for filtered vector search
SET hnsw.iterative_scan = 'relaxed_order';
SET hnsw.max_scan_tuples = 50000;

SELECT id, content, embedding <=> '[0.1, 0.2, ...]' AS distance
FROM documents
WHERE category = 'technical'
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 10;
```

---

## HNSW vs IVFFlat Comparison

| Metric | HNSW | IVFFlat |
|--------|------|---------|
| Query latency (1M rows) | ~1-5ms | ~5-20ms |
| Recall @ 10 (default params) | ~95-99% | ~85-95% |
| Memory usage | High (graph stored in RAM) | Low (only centroids in RAM) |
| Build time | Slow (O(n log n)) | Fast (O(n)) |
| Update performance | Good (incremental insert) | Poor (requires rebuild for accuracy) |
| Filter support (pre-0.8) | Poor without iterative scan | Moderate with probes tuning |
| Filter support (0.8+) | Good with iterative scan | Good with probes tuning |
| Best for | Online search, fresh data, high recall | Batch workloads, static data, memory-limited |

---

## Index Parameter Tuning

### HNSW Parameters

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `m` | 16 | 4–100 | Graph connectivity; higher = better recall, more memory |
| `ef_construction` | 64 | 4–1000 | Build quality; higher = better recall, slower build |
| `ef_search` | 40 | 1–1000 | Query quality; higher = better recall, slower query |

```sql
-- High-recall HNSW index
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 32, ef_construction = 128);

-- Query tuning
SET hnsw.ef_search = 100;
```

### IVFFlat Parameters

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `lists` | 100 | 1–10000 | Number of clusters; rule: `sqrt(row_count)` |
| `probes` | 1 | 1–lists | Clusters searched at query time; higher = better recall |

```sql
-- IVFFlat for 1M rows
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 1000);

-- Query tuning (balance recall vs speed)
SET ivfflat.probes = 10;
```

### Rule of Thumb

```text
HNSW:
  m = 16 (default)    → general purpose
  m = 32–64           → high recall requirement
  ef_construction = 64–128 → standard build
  ef_search = 40–200  → runtime tuning without rebuild

IVFFlat:
  lists = sqrt(row_count)    → starting point
  probes = lists * 0.05–0.1  → 5-10% of lists for good recall
```

---

## Filter Optimization Patterns

### Pre-filter vs Post-filter

| Strategy | How it works | When to use |
|----------|-------------|-------------|
| **Post-filter** | ANN search → filter results | Default; filter selectivity > 50% |
| **Pre-filter** | Filter rows → exact search on subset | Small filtered set (< 10K rows) |
| **Iterative scan** (pgvector 0.8+) | ANN search → expand until filter satisfied | Medium selectivity, HNSW index |
| **Composite index** | Separate btree index on filter column | High-cardinality filter, partition by filter value |

### Post-filter (default behavior)

```sql
-- pgvector defaults to ANN then filter
SELECT id, content
FROM documents
WHERE embedding <=> '[...]' < 0.5  -- distance threshold
  AND category = 'technical'
ORDER BY embedding <=> '[...]'
LIMIT 10;
```

### Pre-filter with Subquery

```sql
-- Effective when category has very few matching rows
SELECT id, content, embedding <=> '[...]' AS distance
FROM (
  SELECT * FROM documents WHERE category = 'technical' AND active = true
) filtered
ORDER BY embedding <=> '[...]'
LIMIT 10;
```

### Partition by Filter Value

```sql
-- Partition table by category for large datasets
CREATE TABLE documents_technical PARTITION OF documents
FOR VALUES IN ('technical');

-- Query hits only one partition
SELECT id, content, embedding <=> '[...]' AS distance
FROM documents
WHERE category = 'technical'
ORDER BY embedding <=> '[...]'
LIMIT 10;
```

---

## EXPLAIN ANALYZE for Vector Queries

```sql
-- Analyze vector search plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT id, content, embedding <=> '[0.1, 0.2, ...]' AS distance
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 10;
```

### Key Plan Nodes to Look For

| Node | Meaning | Action |
|------|---------|--------|
| `Index Scan using hnsw_idx` | HNSW index used | Check `ef_search` if recall is low |
| `Index Scan using ivfflat_idx` | IVFFlat index used | Increase `probes` if recall is low |
| `Seq Scan` | No index used | Check `enable_seqscan`, index existence |
| `rows=X (actual X)` | Estimate accuracy | Large mismatch → run `ANALYZE` |

### Diagnosing Low Recall

```sql
-- Check actual vs approximate results
WITH exact AS (
  SELECT id, embedding <-> '[...]' AS dist
  FROM documents ORDER BY dist LIMIT 10
),
approx AS (
  SELECT id, embedding <-> '[...]' AS dist
  FROM documents ORDER BY dist LIMIT 10
)
SELECT COUNT(*) AS overlap
FROM exact e JOIN approx a USING (id);
-- overlap < 8 → tune ef_search or probes
```

---

## Production Recommended Settings

```sql
-- postgresql.conf tuning for pgvector workloads
shared_buffers = '25% of RAM'          -- keep HNSW graph in buffer cache
work_mem = '256MB'                      -- for sort during IVFFlat build
maintenance_work_mem = '2GB'            -- for index build operations
max_parallel_workers_per_gather = 4     -- parallel index scans

-- Session-level for query tuning
SET hnsw.ef_search = 100;
SET hnsw.iterative_scan = 'relaxed_order';
SET hnsw.max_scan_tuples = 50000;
SET ivfflat.probes = 20;
```

### Index Creation Best Practices

```sql
-- Always use CONCURRENTLY in production
CREATE INDEX CONCURRENTLY ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Monitor build progress
SELECT phase, blocks_done, blocks_total,
       tuples_done, tuples_total
FROM pg_stat_progress_create_index
WHERE relid = 'documents'::regclass;
```

### Monitoring Vector Index Health

```sql
-- Index size
SELECT pg_size_pretty(pg_relation_size('hnsw_idx')) AS index_size;

-- Cache hit ratio for index
SELECT idx_blks_hit::float / NULLIF(idx_blks_hit + idx_blks_read, 0) AS hit_ratio
FROM pg_statio_user_indexes
WHERE indexrelname = 'hnsw_idx';

-- Slow vector queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE query LIKE '%<=>%' OR query LIKE '%<->%'
ORDER BY mean_exec_time DESC
LIMIT 10;
```
