# Embedding Model Selection Guide

**Purpose:** Comprehensive comparison of embedding models for vector search.
**Read when:** Selecting an embedding model for vector or hybrid search.

---

## Model Comparison Matrix

### Commercial Models

| Model | Provider | Dimensions | Max Tokens | Multilingual | MTEB Score | Cost (per 1M tokens) | Matryoshka |
|-------|----------|-----------|------------|-------------|------------|----------------------|------------|
| text-embedding-3-large | OpenAI | 256-3072 | 8191 | Yes | ~64.6 | $0.13 | Yes |
| text-embedding-3-small | OpenAI | 256-1536 | 8191 | Yes | ~62.3 | $0.02 | Yes |
| voyage-3-large | Voyage AI | 1024 | 32000 | Yes | ~67.2 | $0.18 | No |
| voyage-3-lite | Voyage AI | 512 | 32000 | Yes | ~63.1 | $0.02 | No |
| embed-v4 | Cohere | 1024 | 512 | Yes (100+) | ~66.5 | $0.10 | Yes |

> **Note:** `embed-v3.0` (Cohere) has been superseded by `embed-v4` which adds Matryoshka dimension reduction and int8/binary quantization. Prefer `embed-v4` for new projects.

### Open-Source Models

| Model | Dimensions | Max Tokens | Multilingual | MTEB Score | License |
|-------|-----------|------------|-------------|------------|---------|
| multilingual-e5-large-instruct | 1024 | 512 | Yes (100+) | ~63.5 | MIT |
| bge-m3 | 1024 | 8192 | Yes (100+) | ~65.2 | MIT |
| all-MiniLM-L6-v2 | 384 | 256 | No | ~56.3 | Apache 2.0 |
| nomic-embed-text-v1.5 | 768 | 8192 | No | ~62.3 | Apache 2.0 |
| gte-Qwen2-7B-instruct | 3584 | 131072 | Yes | ~67.5 | Apache 2.0 |

**bge-m3 highlight:** Single model supports dense, sparse (SPLADE-style), and late-interaction (ColBERT) simultaneously — useful when a unified open-source embedding pipeline is preferred over separate models for retrieval stages.

---

## Selection Decision Tree

```
START
  │
  ├─ Budget constraint?
  │   ├─ Free/self-hosted required → Open-source models
  │   │   ├─ Multilingual? → bge-m3 or multilingual-e5-large-instruct
  │   │   ├─ English only? → nomic-embed-text-v1.5
  │   │   └─ Minimal resources? → all-MiniLM-L6-v2
  │   │
  │   └─ API budget available → Commercial models
  │       ├─ Best quality? → voyage-3-large or gte-Qwen2-7B
  │       ├─ Good quality + low cost? → text-embedding-3-small
  │       └─ Long documents (>8K tokens)? → voyage-3-large (32K context)
  │
  ├─ Matryoshka dimension reduction needed?
  │   ├─ Yes → OpenAI text-embedding-3-* or Cohere embed-v4
  │   └─ No → Any model
  │
  └─ Japanese text?
      ├─ Yes → multilingual models (OpenAI, Cohere, bge-m3)
      └─ No → Any model
```

---

## Distance Metrics

| Metric | Formula | Best For | Normalized |
|--------|---------|----------|-----------|
| Cosine | 1 - (a·b)/(|a||b|) | General text similarity | Yes (0-2) |
| L2 (Euclidean) | sqrt(Σ(a-b)²) | Dense clusters | No |
| Inner Product | -a·b | Pre-normalized vectors | Depends |

**Default recommendation:** Cosine distance for text embeddings. Most embedding models are trained with cosine similarity.

---

## Benchmarking Template

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def benchmark_model(model_name: str, queries: list[str], corpus: list[str], relevance: dict):
    """Benchmark an embedding model on your dataset."""
    model = SentenceTransformer(model_name)

    query_embeddings = model.encode(queries, normalize_embeddings=True)
    corpus_embeddings = model.encode(corpus, normalize_embeddings=True)

    # Cosine similarity (since normalized, dot product = cosine)
    scores = query_embeddings @ corpus_embeddings.T

    # Calculate NDCG@10
    ndcg_scores = []
    for i, query in enumerate(queries):
        ranked_indices = np.argsort(-scores[i])[:10]
        dcg = sum(relevance.get((query, corpus[j]), 0) / np.log2(rank + 2)
                  for rank, j in enumerate(ranked_indices))
        ideal = sorted([relevance.get((query, doc), 0) for doc in corpus], reverse=True)[:10]
        idcg = sum(rel / np.log2(rank + 2) for rank, rel in enumerate(ideal))
        ndcg_scores.append(dcg / idcg if idcg > 0 else 0)

    return {
        "model": model_name,
        "ndcg@10": np.mean(ndcg_scores),
        "embedding_dim": model.get_sentence_embedding_dimension(),
        "encode_speed": "measure separately"
    }
```

---

## Dimension Reduction Strategies

### Matryoshka (Recommended)

Models like OpenAI text-embedding-3-* support native dimension reduction:

```python
response = client.embeddings.create(
    model="text-embedding-3-large",
    input="text",
    dimensions=256  # Reduce from 3072 → 256
)
```

| Dimensions | Quality (relative) | Storage | Latency |
|-----------|-------------------|---------|---------|
| 3072 | 100% | Baseline | Baseline |
| 1536 | ~98% | 50% | ~50% |
| 512 | ~94% | 17% | ~17% |
| 256 | ~91% | 8% | ~8% |

### PCA (Post-hoc)

For models without Matryoshka support:

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=256)
reduced = pca.fit_transform(original_embeddings)
# Normalize after reduction
reduced = reduced / np.linalg.norm(reduced, axis=1, keepdims=True)
```

**Trade-off:** PCA typically loses 5-10% more quality than Matryoshka at the same dimension.
