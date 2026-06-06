# Handoff Templates

**Purpose:** Standardized handoff formats between Seek and partner agents.
**Read when:** Receiving input from or sending output to collaborating agents.

---

## Inbound Handoffs

### From Oracle (RAG Retrieval Design)

```yaml
ORACLE_TO_SEEK_HANDOFF:
  context:
    use_case: "[QA / summarization / agent tool / chatbot]"
    corpus:
      description: "[what data is being searched]"
      size: "[document count]"
      avg_document_length: "[tokens]"
      languages: "[en / ja / multilingual]"
      update_frequency: "[real-time / daily / weekly]"
  requirements:
    quality_targets:
      primary_metric: "[MRR / NDCG@k / Recall@k]"
      target_value: "[0.0-1.0]"
    latency_budget_ms: "[ms allocated to retrieval step]"
    context_window_budget: "[tokens allocated for retrieved context]"
  constraints:
    infrastructure: "[existing stack or new]"
    embedding_model: "[recommended or TBD]"
    chunking_strategy: "[recommended or TBD]"
  expected_output:
    - Retrieval layer design (engine, index, query templates)
    - Embedding model recommendation with benchmarks
    - Reranking strategy
    - Evaluation methodology
```

### From Builder (Search Feature Request)

```yaml
BUILDER_TO_SEEK_HANDOFF:
  feature:
    description: "[search feature description]"
    user_stories: "[relevant user stories]"
  data:
    source_tables: "[table names and schemas]"
    volume: "[row count]"
    update_pattern: "[real-time / batch / CDC]"
  requirements:
    query_types: "[keyword / autocomplete / faceted / semantic]"
    latency_target_ms: "[P95 target]"
    result_format: "[list / paginated / infinite scroll]"
  constraints:
    existing_stack: "[current DB, search engine if any]"
    budget: "[managed service tier or compute budget]"
```

### From Schema (Data Model for Indexing)

```yaml
SCHEMA_TO_SEEK_HANDOFF:
  models:
    - table: "[table name]"
      columns:
        - name: "[column name]"
          type: "[data type]"
          searchable: true/false
          filterable: true/false
      relationships:
        - type: "[has_many / belongs_to]"
          target: "[related table]"
  notes:
    - "[any relevant schema constraints or patterns]"
```

### From Stream (Ingestion Pipeline Specs)

```yaml
STREAM_TO_SEEK_HANDOFF:
  pipeline:
    source: "[data source]"
    frequency: "[real-time CDC / batch interval]"
    format: "[JSON / Avro / Parquet]"
    volume: "[events per second or batch size]"
  requirements:
    index_freshness: "[max staleness tolerated]"
    schema_evolution: "[how schema changes are handled]"
```

---

## Outbound Handoffs

### To Builder (Search API Implementation)

```yaml
SEEK_TO_BUILDER_HANDOFF:
  design:
    engine: "[Elasticsearch / OpenSearch / pgvector / Pinecone]"
    version: "[engine version]"
    strategy: "[full-text / vector / hybrid]"
  index:
    name: "[index name]"
    mapping: "[full mapping definition or reference to file]"
    analyzers: "[analyzer configurations]"
    settings:
      shards: "[count]"
      replicas: "[count]"
  queries:
    templates:
      - name: "[query template name]"
        type: "[search / autocomplete / faceted / similar]"
        template: "[query DSL or SQL]"
        parameters: "[list of dynamic parameters]"
  ranking:
    strategy: "[BM25 / vector / hybrid RRF / custom]"
    boosting: "[field boost configuration]"
    reranker: "[cross-encoder model or API]"
  implementation_notes:
    sdk: "[elasticsearch-py / pgvector / pinecone-client]"
    connection: "[connection pool settings]"
    error_handling: "[retry / fallback / circuit breaker]"
    caching: "[query result cache / embedding cache]"
  evaluation:
    metrics: "[NDCG@10, MRR, Recall@20]"
    baseline: "[current system measurements]"
    target: "[improvement targets]"
```

### To Oracle (Retrieval Quality Report)

```yaml
SEEK_TO_ORACLE_HANDOFF:
  retrieval_design:
    engine: "[engine used]"
    strategy: "[retrieval strategy]"
    embedding_model: "[selected model]"
    chunking:
      strategy: "[chunking approach]"
      chunk_size: "[tokens]"
      overlap: "[tokens]"
    reranking: "[reranker used]"
  quality_metrics:
    ndcg_at_10: "[measured value]"
    mrr: "[measured value]"
    recall_at_20: "[measured value]"
    latency_p95_ms: "[measured value]"
  recommendations:
    - "[recommendation 1]"
    - "[recommendation 2]"
  integration_notes:
    context_assembly: "[how to format retrieved chunks for LLM]"
    max_context_tokens: "[token budget]"
```

### To Stream (Index Ingestion Requirements)

```yaml
SEEK_TO_STREAM_HANDOFF:
  index_target:
    engine: "[search engine]"
    index_name: "[target index]"
    endpoint: "[connection details]"
  ingestion:
    source_tables: "[tables to index]"
    fields: "[fields to extract and transform]"
    embedding_fields: "[fields requiring vector embedding]"
    embedding_model: "[model for embedding generation]"
  requirements:
    freshness: "[max acceptable lag]"
    consistency: "[eventual / strong]"
    error_handling: "[DLQ / retry / alert]"
  transforms:
    - field: "[field name]"
      transform: "[transformation description]"
```

### To Beacon (Search SLO/SLI)

```yaml
SEEK_TO_BEACON_HANDOFF:
  slos:
    - name: "Search Latency"
      sli: "P95 search response time"
      target: "< 200ms"
      window: "30d rolling"
    - name: "Search Availability"
      sli: "Successful search responses / total requests"
      target: "99.9%"
      window: "30d rolling"
    - name: "Index Freshness"
      sli: "Time from data change to searchable"
      target: "< 60s"
      window: "continuous"
  dashboards:
    - "Search latency distribution (P50/P95/P99)"
    - "Query rate and error rate"
    - "Index lag and document count"
  alerts:
    - condition: "P95 > 500ms for 5 minutes"
      severity: "warning"
    - condition: "Error rate > 5% for 2 minutes"
      severity: "critical"
```

### To Radar (Search Quality Tests)

```yaml
SEEK_TO_RADAR_HANDOFF:
  test_suites:
    relevance_regression:
      description: "Ensure search quality does not degrade"
      judgment_set: "[path to query-relevance pairs]"
      metrics:
        - "NDCG@10 >= 0.72"
        - "MRR >= 0.65"
      frequency: "on every index mapping change"
    functional:
      - "Empty query returns no error"
      - "Special characters are handled gracefully"
      - "Filter-only queries work without text"
      - "Pagination returns consistent results"
    performance:
      - "P95 < 200ms for standard queries"
      - "P95 < 50ms for autocomplete"
      - "Concurrent 100 QPS maintains P99 < 500ms"
```
