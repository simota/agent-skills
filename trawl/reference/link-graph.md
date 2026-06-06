# Link Graph Design

## Overview

The link graph captures the hyperlink structure discovered during crawling. It drives seed prioritization, important page discovery, and scope bounding.

```
  Crawled Page A
    ├── Link → Page B (anchor: "pricing")
    ├── Link → Page C (anchor: "about us")
    └── Link → External D (anchor: "partner site")
         │
         ▼
  Link Graph Storage
    ├── Forward Index: A → [B, C, D]
    ├── Reverse Index: B → [A, E, F]
    └── Anchor Text Index: B → ["pricing", "plans", "cost"]
```

## Data Structures

### Adjacency Representations

| Structure | Memory/1B edges | Insert | Lookup | Best For |
|-----------|----------------|--------|--------|----------|
| Adjacency list (HashMap) | ~24 GB | O(1) amortized | O(degree) | Small/Medium, dynamic updates |
| Compressed Sparse Row (CSR) | ~8 GB | O(N) rebuild | O(1) offset | Large/Web-scale, static analysis |
| Edge list (sorted) | ~16 GB | O(1) append | O(log N) binary search | Streaming ingest, batch processing |
| Graph DB (Neo4j) | Disk-backed | O(1) | O(1) traversal | Complex queries, relationship analysis |

### Selection Guide

```
Need complex graph queries (shortest path, community detection)?
  → Graph DB (Neo4j / JanusGraph)

Need fast batch PageRank computation?
  → CSR in memory or on disk (RocksDB-backed)

Need real-time link insertion during crawl?
  → Adjacency list (HashMap) or Edge list (append-only)

Scale > 10B edges?
  → Distributed: HBase edge table or Spark GraphX
```

## Anchor Text Schema

```
Edge record:
{
  from_url:       string    # Canonical source URL
  to_url:         string    # Canonical target URL
  anchor_text:    string    # Link text content
  context_window: string    # ±50 chars around the anchor (for relevance scoring)
  link_type:      enum      # INTERNAL | EXTERNAL | NOFOLLOW | UGC | SPONSORED
  discovered_at:  timestamp # First discovery timestamp
  last_seen_at:   timestamp # Most recent crawl where this link was found
  position:       enum      # NAV | CONTENT | FOOTER | SIDEBAR
}

Storage estimate: ~200 bytes/edge average
1 billion edges ≈ 200 GB raw, ~80 GB compressed (Snappy/ZSTD)
```

### Link Type Classification

| Type | rel attribute | Follow | Index Priority Impact |
|------|-------------|--------|----------------------|
| INTERNAL | (none) | Yes | High — same-domain authority flow |
| EXTERNAL | (none) | Yes | Medium — cross-domain authority |
| NOFOLLOW | `rel="nofollow"` | No | Low — no authority transfer |
| UGC | `rel="ugc"` | No | Low — user-generated, unreliable |
| SPONSORED | `rel="sponsored"` | No | None — paid placement |

## PageRank-Variant Seed Prioritization

### Standard PageRank

```
Parameters:
  Damping factor (d): 0.85 (standard)
  Convergence threshold (ε): 10^-6
  Max iterations: 100

Formula:
  PR(A) = (1-d)/N + d × Σ(PR(T)/C(T)) for all T linking to A
  where:
    N = total pages
    T = pages linking to A
    C(T) = outbound link count of T

Convergence: typically 40-60 iterations for 1M+ page graphs
```

### Topic-Sensitive PageRank (for focused crawls)

```
Modification:
  Replace uniform teleportation (1-d)/N with biased teleportation:
  PR(A) = (1-d) × topic_weight(A) + d × Σ(PR(T)/C(T))

  topic_weight(A) = 1.0 if A matches target topic, 0.0 otherwise
  (normalized so Σ topic_weight = 1.0)

Use case: Domain-specific crawls where seed URLs define the topic.
Benefit: Pages relevant to the crawl topic get 3-5x higher priority.
```

### Simplified Seed Scoring (when full PageRank is too expensive)

```
seed_score(URL) = w1 × in_link_count
               + w2 × domain_authority
               + w3 × sitemap_priority
               + w4 × (1 / hop_depth)

Recommended weights:
  w1 = 0.3 (in-link count, log-normalized)
  w2 = 0.3 (domain-level authority estimate)
  w3 = 0.2 (sitemap <priority> value, 0.0-1.0)
  w4 = 0.2 (inverse depth: root=1.0, depth-1=0.5, depth-2=0.33)

Advantage: O(1) per URL, no graph traversal needed.
Trade-off: Less accurate than PageRank but sufficient for frontier prioritization.
```

## Scope Bounding

### Hop Depth × Domain Affinity

```
scope_score(URL) = domain_affinity(URL) × depth_factor(URL)

domain_affinity:
  Same domain as seed:      1.0
  Same registered domain:   0.8  (e.g., blog.example.com for seed example.com)
  Linked domain (1 hop):    0.3
  Linked domain (2+ hops):  0.1

depth_factor:
  depth_factor = max(0, 1.0 - (hop_depth / max_depth))
  where max_depth is configurable (default: 5)

Decision:
  scope_score ≥ 0.3 → include in frontier
  scope_score < 0.3 → discard (out of scope)
```

### Domain Scope Strategies

| Strategy | Rule | Best For |
|----------|------|----------|
| Same-domain only | Only URLs matching seed domain(s) | Focused site crawls |
| Same-registered-domain | Include all subdomains | Company-wide crawls |
| Follow-one-hop | Follow external links one hop out | Discovery crawls |
| Allowlist | Only domains in explicit allowlist | Compliance-restricted crawls |
| Denylist + open | Follow all except denied domains | Broad research crawls |

## Use Cases

### Important Page Discovery
- Run PageRank on the crawled link graph (Personalized PageRank for topic-focused crawls)
- Pages with PR > mean + 2σ are "important"
- Use as priority boost in re-crawl scheduling
- External authority signals: Common Crawl Webgraph (latest release `cc-main-2025-26-nov-dec-jan`, 250.8M host nodes / 10.9B edges; domain-level 121.3M / 6.2B); Open PageRank (free decile rank); Majestic Trust Flow (commercial). Use as seed-priority feature when the crawled subgraph is too sparse for in-house PageRank.

### Orphan Page Detection
- Pages with in_link_count = 0 (no internal links pointing to them)
- Common in large sites — pages exist but are unreachable from navigation
- Flag for site owner or exclude from index

### Domain Relationship Analysis
- Aggregate edges by domain → domain-level graph
- Identify link farms (domains with > 90% outbound links to a single target)
- Detect content syndication networks (bidirectional high-volume linking)

## Storage Backend Selection

| Backend | Edges | Query Types | Latency | Best For |
|---------|-------|-------------|---------|----------|
| RocksDB | < 1B | Point lookup, range scan | < 1ms | Medium tier, single-node |
| Neo4j | < 100M | Traversal, path queries | 1-10ms | Complex graph analysis |
| HBase | 1B+ | Point lookup, scan | 5-50ms | Web-scale, distributed |
| Spark GraphX | 1B+ | Batch PageRank, analytics | Minutes | Offline analysis |
| DuckDB | < 100M | SQL analytics on edges | < 1ms | Ad-hoc analysis, prototyping |
