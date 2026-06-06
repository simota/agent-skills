# Search Engine Comparison Guide

**Purpose:** Decision framework for search engine and vector DB selection.
**Read when:** Choosing between search engines or vector databases for a project.

---

## Full-Text Search Engines

| Feature | Elasticsearch | OpenSearch | Meilisearch | Typesense |
|---------|--------------|-----------|-------------|-----------|
| **License** | Elastic License 2.0 | Apache 2.0 | MIT | GPL-3.0 |
| **Vector Search** | Yes (8.x+) | Yes (2.x+) | Yes (1.3+) | Yes (0.25+) |
| **Japanese** | kuromoji plugin | kuromoji plugin | Limited | Limited |
| **Aggregations** | Advanced | Advanced | Basic | Basic |
| **Learning Curve** | High | High | Low | Low |
| **Managed Services** | Elastic Cloud | AWS OpenSearch | Meilisearch Cloud | Typesense Cloud |
| **Best For** | Enterprise, complex search | AWS-native, fork of ES | Dev-friendly, small-medium | Simple, typo-tolerant |
| **Max Scale** | PB-scale | PB-scale | ~10M docs | ~100M docs |

### Selection Guide

```
Is your data > 100M documents?
  ├─ Yes → Elasticsearch or OpenSearch
  │   ├─ AWS-native? → OpenSearch
  │   └─ Multi-cloud / on-prem? → Elasticsearch
  └─ No
      ├─ Need Japanese support? → Elasticsearch/OpenSearch
      ├─ Developer experience priority? → Meilisearch
      ├─ Typo tolerance critical? → Typesense
      └─ Already have ES expertise? → Elasticsearch
```

---

## Vector Databases

| Feature | pgvector | Pinecone | Weaviate | Qdrant | Milvus | ChromaDB |
|---------|---------|---------|---------|-------|-------|---------|
| **Type** | Extension | Managed SaaS | Self-hosted/Cloud | Self-hosted/Cloud | Self-hosted/Cloud | Embedded/Server |
| **License** | PostgreSQL | Proprietary | BSD-3 | Apache 2.0 | Apache 2.0 | Apache 2.0 |
| **Index Types** | HNSW, IVFFlat | Proprietary | HNSW | HNSW, ACORN | HNSW, IVF, DiskANN | HNSW |
| **Filtering** | SQL WHERE | Metadata | GraphQL + filters | Payload filters (ACORN) | Metadata | Metadata |
| **Hybrid Search** | tsvector + vector | Sparse + dense | BM25 + vector | Sparse + dense | BM25 + vector (v2.5+) | Limited |
| **Max Scale** | ~50M vectors (pgvectorscale) | Billions | 100M+ | 100M+ | Billions | ~1M |
| **Ops Complexity** | Low (part of PG) | Zero (managed) | Medium | Medium | Medium-High | Low |
| **Best For** | Existing PG, hybrid | Managed serverless | Multi-modal, RBAC | Filtering + vector | Large-scale open source | Prototyping, small |
| **Cost** | Free (PG cost) | Pay-per-use (serverless) | Free self-host | Free self-host | Free self-host | Free |

**Notable recent changes (2024-2026):**
- **pgvector 0.8.x**: Iterative index scans for HNSW/IVFFlat (auto-expand when needed), sparse vector (`sparsevec`) support, improved cost estimation — [github.com/pgvector/pgvector/releases](https://github.com/pgvector/pgvector/releases)
- **Pinecone serverless**: Dedicated read nodes (early access), BYOC (AWS/GCP), index backup/restore GA, namespace-level metadata schema — [docs.pinecone.io/release-notes/2025](https://docs.pinecone.io/release-notes/2025)
- **Weaviate 1.28**: BlockMax WAND for faster BM25/hybrid search (experimental), RBAC (technical preview), native Japanese `kagome_ja` tokenizer — [weaviate.io/blog/weaviate-1-28-release](https://weaviate.io/blog/weaviate-1-28-release)
- **Qdrant 1.16**: Tiered Multitenancy (dedicated shards for large tenants + shared shard for small), ACORN filtered vector search algorithm, Inline Storage for disk-efficient HNSW — [qdrant.tech/blog/qdrant-1.16.x](https://qdrant.tech/blog/qdrant-1.16.x/)
- **Milvus 2.5**: Full-text search (BM25 on sparse vectors, no client-side preprocessing) — [milvus.io/blog/introduce-milvus-2-5](https://milvus.io/blog/introduce-milvus-2-5-full-text-search-powerful-metadata-filtering-and-more.md)
- **Milvus 2.6**: RaBitQ 1-bit quantization (~28% memory, 4× QPS), hot-cold tiered storage (80% cost reduction), Woodpecker cloud-native WAL — [milvus.io/blog/introduce-milvus-2-6](https://milvus.io/blog/introduce-milvus-2-6-built-for-scale-designed-to-reduce-costs.md)

### Selection Guide

```
Already using PostgreSQL?
  ├─ Yes, < 5M vectors → pgvector HNSW (no new infra)
  ├─ Yes, 5-50M vectors → pgvector + pgvectorscale (StreamingDiskANN)
  └─ No or > 50M vectors
      ├─ Want zero ops? → Pinecone serverless
      ├─ Heavy filtering + vector? → Qdrant (ACORN algorithm)
      ├─ Multi-modal / enterprise RBAC? → Weaviate
      ├─ Billion-scale open source? → Milvus 2.6
      ├─ Rapid prototyping? → ChromaDB
      └─ Large scale + cost-sensitive? → Milvus self-hosted or Qdrant self-hosted
```

---

## Hybrid Search Capability Comparison

| Capability | ES/OS 8.x | pgvector + pg | Weaviate 1.28+ | Qdrant 1.16+ | Milvus 2.5+ |
|-----------|-----------|---------------|---------|--------|--------|
| Native RRF | Yes | Manual (SQL) | Yes | Manual | Yes |
| BM25 + kNN | Yes (ELSER sparse) | tsvector + vector | Yes (BlockMax WAND) | sparse + dense | Yes (native BM25) |
| Neural Sparse | ELSER v2 (Elastic) / Neural Sparse (OpenSearch) | — | — | — | sparsevec field |
| Cross-encoder rerank | Plugin/app layer | App layer | Module | App layer | App layer |
| Filtered vector search | Pre/post filter | SQL WHERE | GraphQL filter | Payload filter (ACORN) | Metadata filter |
| Multi-field boosting | Yes | Manual scoring | Yes | Manual | Manual |

**Key sparse/hybrid notes:**
- Elasticsearch ELSER v2 (2025): available via Elastic Inference Service (EIS), first model in technical preview — [elastic.co/search-labs/blog/sparse-vector-embedding](https://www.elastic.co/search-labs/blog/sparse-vector-embedding)
- OpenSearch neural sparse v2 (2024): distill model cuts parameters 50%, improves ingestion 1.74× on CPU — [opensearch.org/blog/neural-sparse-v2-models](https://opensearch.org/blog/neural-sparse-v2-models/)

---

## Cost Comparison (Approximate Monthly)

| Tier | Elasticsearch Cloud | AWS OpenSearch | Pinecone | Qdrant Cloud |
|------|-------------------|---------------|---------|-------------|
| Dev/Test | $95 (2GB RAM) | $30 (t3.small) | $0 (starter) | $0 (free tier) |
| Small Prod | $250 (4GB, HA) | $150 (m5.large) | $70 (s1.x1) | $25 (1GB) |
| Medium Prod | $800 (16GB, HA) | $500 (r5.xlarge) | $250 (s1.x4) | $100 (4GB) |
| Large Prod | $2500+ (64GB+) | $1500+ (custom) | Custom | $350+ (16GB) |

*Prices are approximate and vary by region and configuration.*

---

## Migration Paths

### Elasticsearch → OpenSearch

- API-compatible (mostly drop-in)
- Main differences: licensing, some plugins, version numbering
- Use snapshot/restore for data migration

### Single DB → Dedicated Search

```
Phase 1: Add search engine alongside DB (dual-write or CDC)
Phase 2: Migrate read queries to search engine
Phase 3: Remove search-related indexes from primary DB
Phase 4: Optimize search engine configuration
```

### pgvector → Dedicated Vector DB

```
Phase 1: Export embeddings to vector DB
Phase 2: Dual-read (query both, compare results)
Phase 3: Switch primary retrieval to vector DB
Phase 4: Keep pgvector as fallback / for joined queries
```
