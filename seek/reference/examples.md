# Search Design Examples

**Purpose:** Concrete usage examples for common search design scenarios.
**Read when:** You need reference implementations or design templates.

---

## Example 1: E-Commerce Product Search

### Requirements
- 500K products, multilingual (EN/JA)
- Autocomplete, faceted search, relevance ranking
- P95 latency < 100ms

### Design

```yaml
SEARCH_PROFILE:
  engine: Elasticsearch 8.x
  strategy: Full-text with semantic boosting
  index:
    name: products
    shards: 2
    replicas: 1
  analyzers:
    - en_analyzer (standard + stemmer + synonym)
    - ja_analyzer (kuromoji + synonym)
    - autocomplete_analyzer (edge_ngram 2-15)
```

**Index Mapping:**
```json
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "analyzer": "en_analyzer",
        "fields": {
          "ja": { "type": "text", "analyzer": "ja_analyzer" },
          "autocomplete": { "type": "text", "analyzer": "autocomplete_analyzer" }
        }
      },
      "category": { "type": "keyword" },
      "price": { "type": "float" },
      "rating": { "type": "float" },
      "in_stock": { "type": "boolean" }
    }
  }
}
```

**Query Template:**
```json
{
  "query": {
    "bool": {
      "must": {
        "multi_match": {
          "query": "{{user_query}}",
          "fields": ["name^3", "name.ja^3", "description", "brand^2"],
          "type": "best_fields"
        }
      },
      "filter": [
        { "term": { "in_stock": true } },
        { "range": { "price": { "gte": "{{min_price}}", "lte": "{{max_price}}" } } }
      ],
      "should": [
        { "range": { "rating": { "gte": 4.0, "boost": 1.5 } } }
      ]
    }
  },
  "aggs": {
    "categories": { "terms": { "field": "category", "size": 20 } },
    "price_ranges": { "range": { "field": "price", "ranges": [
      { "to": 1000 }, { "from": 1000, "to": 5000 }, { "from": 5000 }
    ]}}
  }
}
```

**Evaluation:** NDCG@10 target 0.75, measured against 100 curated query-product pairs.

---

## Example 2: RAG Knowledge Base (Hybrid Search)

### Requirements
- 50K documents (technical docs, 2K avg tokens)
- Semantic understanding required
- Support for RAG pipeline with LLM

### Design

```yaml
SEARCH_PROFILE:
  engine: pgvector (within existing PostgreSQL)
  strategy: Hybrid (BM25 + vector with RRF)
  embedding_model: text-embedding-3-small (1536d)
  chunking:
    strategy: recursive
    chunk_size: 512 tokens
    overlap: 64 tokens
  retrieval:
    top_k_bm25: 50
    top_k_vector: 50
    rrf_k: 60
    final_top_k: 10
  reranker: cohere-rerank-v3.5
```

**Schema:**
```sql
CREATE TABLE document_chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES documents(id),
  chunk_index INT NOT NULL,
  content TEXT NOT NULL,
  embedding vector(1536),
  metadata JSONB DEFAULT '{}',
  tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_chunks_embedding ON document_chunks
  USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 200);
CREATE INDEX idx_chunks_tsv ON document_chunks USING gin(tsv);
```

**Retrieval Function:**
```python
async def hybrid_search(query: str, top_k: int = 10) -> list[ChunkResult]:
    query_embedding = await embed(query)

    bm25_results = await db.execute(
        "SELECT id, ts_rank(tsv, plainto_tsquery($1)) AS score "
        "FROM document_chunks WHERE tsv @@ plainto_tsquery($1) "
        "ORDER BY score DESC LIMIT 50",
        query
    )

    vector_results = await db.execute(
        "SELECT id, 1 - (embedding <=> $1::vector) AS score "
        "FROM document_chunks "
        "ORDER BY embedding <=> $1::vector LIMIT 50",
        query_embedding
    )

    fused = rrf_fusion(bm25_results, vector_results, k=60)
    reranked = await cohere_rerank(query, fused[:20], top_n=top_k)
    return reranked
```

---

## Example 3: Real-Time Log Search

### Requirements
- 100M+ log entries/day
- Full-text search + structured filters
- 7-day hot, 30-day warm, 90-day cold retention

### Design

```yaml
SEARCH_PROFILE:
  engine: OpenSearch 2.x
  strategy: Full-text with ILM
  index_pattern: logs-{YYYY.MM.dd}
  ilm_policy:
    hot: 7 days (SSD, 2 replicas)
    warm: 30 days (HDD, 1 replica, force-merge)
    cold: 90 days (S3, 0 replicas, searchable snapshot)
    delete: 90 days
```

---

## Example 4: Autocomplete / Search-As-You-Type

### Design

```json
{
  "settings": {
    "analysis": {
      "filter": {
        "autocomplete_filter": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 15
        }
      },
      "analyzer": {
        "autocomplete_index": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "autocomplete_filter"]
        },
        "autocomplete_search": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "suggest": {
        "type": "text",
        "analyzer": "autocomplete_index",
        "search_analyzer": "autocomplete_search"
      }
    }
  }
}
```

**Key principle:** Index-time ngram, search-time standard. Never use ngram at search time.
