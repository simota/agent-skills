# URL Frontier Design

## Frontier Architecture

The URL frontier is the central data structure of a web crawler. It manages URL discovery, deduplication, prioritization, and scheduling.

```
  Discovered URLs
        │
        ▼
  ┌───────────┐     ┌──────────────┐
  │ URL Canon- │────▶│  Seen-Set    │──── Already seen? → Discard
  │ icalization│     │ (Dedup)      │
  └───────────┘     └──────┬───────┘
                           │ New URL
                           ▼
                    ┌──────────────┐
                    │  Priority    │
                    │  Scoring     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Domain      │
                    │  Queues      │──── One queue per domain
                    └──────┬───────┘     (politeness enforcement)
                           │
                           ▼
                    ┌──────────────┐
                    │  Worker      │
                    │  Assignment  │──── Consistent hash → worker
                    └──────────────┘
```

## Deduplication Strategies

### Bloom Filter

```
Parameters for 10 billion URLs, 1% FPR:
- Size: ~11.5 GB (1.2 bytes/element × 10^10)
- Hash functions: 7 (optimal k = ln(2) × m/n)
- Lookup: O(k) = O(7)
- Insert: O(k) = O(7)
- Deletion: Not supported

Partitioned Bloom filter (for distributed):
- Split by hash(URL) % partition_count
- Each partition: independent Bloom filter
- Merge: bitwise OR (grows FPR — avoid)
```

**Best for:** Large/Web-scale tiers, append-only dedup, memory-constrained environments.

### Cuckoo Filter

```
Parameters for 10 billion URLs, 1% FPR:
- Size: ~15 GB (1.5 bytes/element × 10^10)
- Bucket size: 4 entries
- Fingerprint size: 12 bits
- Max kicks: 500
- Deletion: Supported (with false-negative risk at high load)

Advantages over Bloom:
- Supports deletion (domain blocking, URL expiry)
- Better cache locality (single lookup location)
- Similar or better FPR per byte at moderate loads
```

**Best for:** Large tier with domain blocking, URL expiry, or dynamic scope changes.

### Redis Seen-Set

```
Implementation:
- SADD url_seen_set <canonical_url>
- SISMEMBER url_seen_set <canonical_url>

Memory (10M URLs, avg 80 bytes/URL):
- ~1.6 GB (with Redis overhead ~2x raw)

Scaling:
- Redis Cluster for >50M URLs
- Sharding by hash(domain) for locality
```

**Best for:** Small/Medium tiers, exact dedup, operational simplicity.

### RocksDB

```
Implementation:
- Key: canonical URL (byte string)
- Value: crawl metadata (last_crawl, status, content_hash)
- Lookup: point query O(log N) with bloom filter acceleration
- Storage: LSM tree, compaction amortizes write cost

Memory:
- Block cache: 256 MB-1 GB (configurable)
- Data on disk: ~100 bytes/URL including metadata
- 1 billion URLs ≈ 100 GB on disk

Advantages:
- Exact dedup with metadata
- Disk-backed (RAM-efficient)
- Supports range scans (domain prefix queries)
```

**Best for:** Medium/Large tiers, when metadata per URL is needed, disk is cheaper than RAM.

## Priority Queue Design

### Multi-Level Priority Queue

```
Level 1 — Seed URLs (manually curated, highest priority)
Level 2 — Sitemap URLs (sitemap.xml priority signal)
Level 3 — In-link count (more inbound links = higher priority)
Level 4 — Depth-based (BFS-first, deeper = lower priority)
Level 5 — Discovery order (FIFO within same priority)

Within each level: domain-level round-robin for politeness
```

### Domain-Level Politeness Queues

```
Structure:
  Global priority queue
    └── Domain queue: example.com (sorted by URL priority)
    └── Domain queue: other.com (sorted by URL priority)
    └── Domain queue: ...

Drain strategy:
  Round-robin across domain queues
  Per-domain rate: min(token_bucket_rate, 1/crawl_delay)
  Empty domain queues are removed after TTL (1 hour)
```

### Re-Crawl Scheduling Models

| Model | Logic | Best For |
|-------|-------|----------|
| Fixed TTL | Re-crawl every N days | Simple, predictable budget |
| Change-detection | ETag/Last-Modified comparison, skip if unchanged | Bandwidth-efficient |
| Exponential backoff | Double interval on each unchanged check (cap at 30 days) | Low-change content |
| Adaptive | Estimate change rate from history, schedule proportionally | High-value content |
| Freshness-weighted | Combine content value × change rate → priority score | Mixed-importance corpus |

## URL Canonicalization

### RFC 3986 Normalization Pipeline

```
Input: https://WWW.Example.COM:443/path/../page?b=2&a=1#fragment

Step 1 — Lowercase scheme and host:
  https://www.example.com:443/path/../page?b=2&a=1#fragment

Step 2 — Strip default port:
  https://www.example.com/path/../page?b=2&a=1#fragment

Step 3 — Resolve path (remove .., .):
  https://www.example.com/page?b=2&a=1#fragment

Step 4 — Sort query parameters:
  https://www.example.com/page?a=1&b=2#fragment

Step 5 — Drop fragment:
  https://www.example.com/page?a=1&b=2

Step 6 — Strip trailing slash (optional, domain-specific):
  https://www.example.com/page?a=1&b=2

Output: https://www.example.com/page?a=1&b=2
```

### Additional Normalization Rules

| Rule | Example | When to Apply |
|------|---------|---------------|
| Strip tracking params | Remove `utm_*`, `fbclid`, `gclid` | Always for dedup |
| Decode unreserved chars | `%7E` → `~` | Always |
| Strip session IDs | Remove `JSESSIONID`, `PHPSESSID` from URL | Always |
| WWW normalization | `www.example.com` = `example.com` | Per-domain config |
| Protocol normalization | `http://` → `https://` if site redirects | Per-domain config |

## Frontier Persistence

### Persistence Strategies by Scale

| Scale | Strategy | RPO | RTO |
|-------|----------|-----|-----|
| Small | Redis RDB snapshots (every 5 min) | 5 min | < 1 min |
| Medium | Redis AOF (every 1 sec) + RDB | 1 sec | < 1 min |
| Large | Kafka offsets + RocksDB WAL | 0 (committed) | < 5 min |
| Web-scale | HDFS checkpoint + HBase WAL | 0 (replicated) | < 10 min |

### Recovery Protocol

```
1. Detect failure (heartbeat timeout or process crash)
2. Load last frontier snapshot
3. Replay WAL/AOF entries since snapshot
4. Mark in-flight URLs as PENDING (not COMPLETE)
5. Reset domain rate limiters
6. Resume crawl from recovered state
```
