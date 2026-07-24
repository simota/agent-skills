# Seek — AUTORUN `_STEP_COMPLETE` Schema

When Seek receives `_AGENT_CONTEXT`, parse `task_type`, `description`, `data_profile`, `search_strategy`, `engine_preference`, and `Constraints`, choose the correct output route, run the PROFILE→SELECT→MAP→QUERY→RANK→EVALUATE workflow, produce the search design deliverable, and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Seek
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Index Mapping | Vector Index Spec | Hybrid Pipeline | RAG Retrieval Spec | Evaluation Spec | Scaling Plan | Engine Comparison]"
    parameters:
      engine: "[Elasticsearch | OpenSearch | Meilisearch | pgvector | Pinecone | Weaviate | Qdrant]"
      strategy: "[full-text | vector | hybrid]"
      embedding_model: "[model name]"
      relevance_target: "[metric: threshold]"
      latency_target_p95: "[ms]"
    reranking: "[cross-encoder | ColBERT | cohere-rerank | none — reason]"
    evaluation_plan: "[metric set and judgment methodology]"
  Next: Builder | Oracle | Stream | Schema | Beacon | Radar | DONE
  Reason: [Why this next step]
```
