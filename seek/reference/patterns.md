# Search Design Patterns

**Purpose:** Core design patterns for full-text, vector, and hybrid search systems.
**Read when:** Designing index mappings, query strategies, or ranking pipelines.

---

## Full-Text Search Patterns

### Pattern 1: Multi-Field Mapping

Use multi-fields for different analysis strategies on the same content.

```json
{
  "title": {
    "type": "text",
    "analyzer": "standard",
    "fields": {
      "exact": { "type": "keyword" },
      "autocomplete": { "type": "text", "analyzer": "edge_ngram_analyzer" },
      "search_as_you_type": { "type": "search_as_you_type" }
    }
  }
}
```

**When to use:** Content needs keyword search, autocomplete, and exact match simultaneously.

### Pattern 2: Japanese Full-Text Search

```json
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "kuromoji": {
          "type": "kuromoji_tokenizer",
          "mode": "search"
        }
      },
      "analyzer": {
        "ja_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji",
          "filter": [
            "kuromoji_baseform",
            "kuromoji_part_of_speech",
            "ja_stop",
            "kuromoji_stemmer",
            "lowercase"
          ]
        }
      }
    }
  }
}
```

**When to use:** Japanese text indexing. Always use `mode: search` for query-time segmentation.

### Pattern 3: Synonym-Aware Search

```json
{
  "filter": {
    "synonym_filter": {
      "type": "synonym_graph",
      "synonyms_path": "analysis/synonyms.txt",
      "updateable": true
    }
  }
}
```

**When to use:** Domain-specific terminology (e.g., "laptop" = "notebook computer").

---

## Vector Search Patterns

### Pattern 4: Matryoshka Embedding Reduction

```python
from openai import OpenAI

client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-3-large",
    input="search query",
    dimensions=256  # Reduce from 3072 to 256
)
# Trade-off: ~5% quality loss for 12x storage reduction
```

**When to use:** Storage/latency constraints outweigh marginal quality gains.

### Pattern 5: Two-Phase Vector Search

```sql
-- Phase 1: Approximate kNN with pre-filter
SELECT id, embedding <=> $1::vector AS distance
FROM documents
WHERE category = ANY($2)
ORDER BY embedding <=> $1::vector
LIMIT 100;

-- Phase 2: Rerank with cross-encoder score
-- (application layer)
```

**When to use:** Filtered vector search where filter selectivity varies widely.

### Pattern 6: Multi-Vector Retrieval

Store separate embeddings for title, content, and metadata. Query with field-weighted combination.

```python
# Weighted multi-field vector search
title_results = search(query_embedding, index="title_vectors", top_k=50)
content_results = search(query_embedding, index="content_vectors", top_k=50)
combined = rrf_fusion(title_results, content_results, k=60)
```

**When to use:** Documents with semantically distinct sections (e.g., title vs body).

---

## Hybrid Search Patterns

### Pattern 7: Elasticsearch Hybrid with RRF

```json
{
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": {
            "query": {
              "multi_match": {
                "query": "search terms",
                "fields": ["title^3", "content"]
              }
            }
          }
        },
        {
          "knn": {
            "field": "embedding",
            "query_vector_builder": {
              "text_embedding": {
                "model_id": "my-embedding-model",
                "model_text": "search terms"
              }
            },
            "k": 50,
            "num_candidates": 100
          }
        }
      ],
      "rank_constant": 60,
      "rank_window_size": 100
    }
  }
}
```

### Pattern 8: pgvector Hybrid Search

```sql
-- BM25 via pg_search + vector via pgvector
WITH bm25 AS (
  SELECT id, ts_rank(tsv, plainto_tsquery($1)) AS bm25_score
  FROM documents
  WHERE tsv @@ plainto_tsquery($1)
  ORDER BY bm25_score DESC
  LIMIT 100
),
vector AS (
  SELECT id, 1 - (embedding <=> $2::vector) AS vector_score
  FROM documents
  ORDER BY embedding <=> $2::vector
  LIMIT 100
),
fused AS (
  SELECT COALESCE(b.id, v.id) AS id,
    COALESCE(1.0 / (60 + b.rank), 0) + COALESCE(1.0 / (60 + v.rank), 0) AS rrf_score
  FROM (SELECT id, ROW_NUMBER() OVER (ORDER BY bm25_score DESC) AS rank FROM bm25) b
  FULL OUTER JOIN (SELECT id, ROW_NUMBER() OVER (ORDER BY vector_score DESC) AS rank FROM vector) v
  ON b.id = v.id
)
SELECT * FROM fused ORDER BY rrf_score DESC LIMIT 20;
```

---

## Scaling Patterns

### Pattern 9: Index Sharding Strategy

| Data Size | Shards | Replicas | Notes |
|-----------|--------|----------|-------|
| <10M docs | 1-2 | 1 | Single node sufficient |
| 10-100M docs | 3-5 | 1-2 | Distribute by time or category |
| 100M-1B docs | 5-20 | 2 | Consider ILM policies |
| >1B docs | 20+ | 2-3 | Shard by tenant or region |

### Pattern 10: Search Result Caching

```yaml
CACHE_STRATEGY:
  layer_1:
    type: "query result cache"
    ttl: "5m"
    invalidation: "on index update"
    scope: "exact query match"
  layer_2:
    type: "embedding cache"
    ttl: "24h"
    scope: "query text → vector"
  layer_3:
    type: "application cache (Redis)"
    ttl: "1-15m"
    scope: "user-facing search results"
```
