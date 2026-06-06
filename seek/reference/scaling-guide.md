# Search Scaling Guide

**Purpose:** Scaling strategies for search infrastructure.
**Read when:** Planning capacity, sharding, replication, or caching for search systems.

---

## Elasticsearch/OpenSearch Scaling

### Shard Sizing Guidelines

| Shard Size | Status | Notes |
|-----------|--------|-------|
| < 1 GB | Too small | Merge shards or reduce shard count |
| 10-50 GB | Ideal | Best balance of performance and management |
| > 50 GB | Too large | Split index, add time-based partitioning |

### Capacity Planning Formula

```
Total storage = (source data × (1 + indexing overhead)) × (1 + replicas)
Indexing overhead ≈ 1.1-1.5x for text, 2-3x for vectors
Replicas = 1 (default) to N (for read scaling)
```

### Index Lifecycle Management (ILM)

```json
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": { "max_size": "50gb", "max_age": "7d" },
          "set_priority": { "priority": 100 }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "forcemerge": { "max_num_segments": 1 },
          "shrink": { "number_of_shards": 1 },
          "set_priority": { "priority": 50 }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "searchable_snapshot": { "snapshot_repository": "s3_repo" },
          "set_priority": { "priority": 0 }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": { "delete": {} }
      }
    }
  }
}
```

---

## Vector DB Scaling

### pgvector Scaling Thresholds

| Vector Count | Index Type | RAM Needed | Notes |
|-------------|-----------|-----------|-------|
| < 100K | IVFFlat | ~1 GB (1536d) | Simple, fast build |
| 100K-1M | HNSW | 2-8 GB (1536d) | Best recall, more RAM |
| 1M-10M | HNSW + partitioning | 8-80 GB | Partition by tenant/category |
| > 10M | Dedicated vector DB | Varies | Consider Qdrant/Pinecone |

### HNSW Tuning Parameters

| Parameter | Default | Effect | Trade-off |
|-----------|---------|--------|-----------|
| `m` | 16 | Connections per node | Higher = better recall, more RAM |
| `ef_construction` | 64 | Build-time candidates | Higher = better index, slower build |
| `ef_search` | 40 | Search-time candidates | Higher = better recall, slower search |

**Recommended starting values:**
```sql
-- High recall (RAG, research)
CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops)
  WITH (m = 24, ef_construction = 256);
SET hnsw.ef_search = 100;

-- Balanced (general search)
CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 200);
SET hnsw.ef_search = 40;

-- Low latency (autocomplete, suggestions)
CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops)
  WITH (m = 12, ef_construction = 128);
SET hnsv.ef_search = 20;
```

---

## Caching Strategy

### Multi-Layer Cache

```
┌─────────────────────────────────────────┐
│ Layer 1: CDN / Edge Cache               │
│ - Static search results (trending)      │
│ - TTL: 1-5 minutes                      │
├─────────────────────────────────────────┤
│ Layer 2: Application Cache (Redis)      │
│ - Query result cache (exact match)      │
│ - Embedding cache (query → vector)      │
│ - TTL: 5-15 minutes                     │
├─────────────────────────────────────────┤
│ Layer 3: Search Engine Cache            │
│ - Request cache (Elasticsearch)         │
│ - Field data cache                      │
│ - Node query cache                      │
├─────────────────────────────────────────┤
│ Layer 4: OS Page Cache                  │
│ - Warm data in memory                   │
│ - Managed by OS, no explicit TTL        │
└─────────────────────────────────────────┘
```

### Cache Invalidation Strategies

| Strategy | When | Implementation |
|----------|------|----------------|
| TTL-based | Default for most search | Set TTL based on data freshness requirements |
| Event-based | Real-time inventory/pricing | Invalidate on index update event |
| Version-based | Index mapping changes | Cache key includes mapping version |
| Hybrid | E-commerce (price + content) | TTL for content, event for price/stock |

---

## Monitoring Checklist

```yaml
SEARCH_MONITORING:
  latency:
    - P50, P95, P99 search response time
    - Embedding generation latency
    - Reranking latency
  throughput:
    - Queries per second (QPS)
    - Indexing rate (docs/sec)
    - Bulk indexing throughput
  quality:
    - Zero-result rate
    - Click-through rate (CTR)
    - Result diversity score
  infrastructure:
    - Cluster health (green/yellow/red)
    - Disk usage per node
    - JVM heap usage
    - Circuit breaker trips
    - Merge queue depth
  vector_specific:
    - Vector index build time
    - Recall@k (periodic offline eval)
    - Embedding cache hit rate
```
