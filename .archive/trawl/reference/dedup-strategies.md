# Deduplication Strategies Reference

Purpose: Design a multi-layer deduplication system for a web-scale crawler — URL canonicalization, exact-URL dedup (probabilistic or exact), content-hash dedup, and near-duplicate clustering. Trawl emits the strategy; Builder implements; Stream consumes clean records.

## Scope Boundary

- **trawl `dedup`**: Dedup architecture (this document).
- **trawl `frontier` (elsewhere)**: URL frontier (uses this dedup data).
- **trawl `extraction` (elsewhere)**: Extraction-time near-dup detection.
- **Schema (elsewhere)**: Database uniqueness constraints.
- **Seek (elsewhere)**: Index-time dedup.

## Dedup Layers

```
URL seen?         ←  Layer 1: URL canonicalization + exact-URL dedup
  │ no
  ▼
Content fetched
  │
  ▼
Content hash seen? ←  Layer 2: exact-content dedup (SHA-256)
  │ no
  ▼
Near-duplicate?    ←  Layer 3: near-dup clustering (SimHash / MinHash)
  │ no
  ▼
Write to corpus
```

Each layer answers a different question and has different storage/lookup cost.

## Layer 1: URL Canonicalization

Canonicalize before comparing. Without this, dedup misses obvious duplicates.

### Canonicalization rules (RFC 3986 + practical web)

1. Lowercase scheme + host.
2. Default port removal (`:80` for http, `:443` for https).
3. Path normalization (remove `.`, `..`, trailing slash policy).
4. Percent-encoding normalization (decode unreserved, uppercase hex).
5. Query parameter sorting + filtering (drop `utm_*`, `fbclid`, `gclid`, `ref`).
6. Fragment removal (for HTTP GET crawling).
7. IDN host normalization (Punycode).
8. Follow redirects → store canonical final URL.
9. `rel="canonical"` link tag: prefer the target.

### Example

| Before | After |
|--------|-------|
| `HTTP://Example.COM:80/Path/./?b=2&utm_source=x&a=1#frag` | `http://example.com/Path/?a=1&b=2` |
| `https://ja.wikipedia.org/wiki/東京` | `https://ja.wikipedia.org/wiki/%E6%9D%B1%E4%BA%AC` |

### Store the canonical URL, not raw. Index by URL hash (SHA-1 or xxhash).

## Layer 1b: Exact-URL Dedup

Binary question: "have I seen this canonical URL before?"

| Technique | Space (per URL) | False positive | Delete support |
|-----------|-----------------|----------------|----------------|
| Exact hash set (RocksDB / Redis) | ~40 B | 0 | Yes |
| Bloom filter | ~10 bits | ~1% @ 10 bits/item | No |
| Cuckoo filter | ~12 bits | <0.1% | Yes (delete support) |
| HyperLogLog | ~1 KB fixed | cardinality estimate | Estimate only |

### Selection matrix

| Crawl scale | Choice |
|-------------|--------|
| < 10M URLs | RocksDB / SQLite set |
| 10M–1B | Redis (hash or set) with sharding |
| 1B–100B | Cuckoo filter or sharded Bloom; RocksDB for authoritative |
| > 100B | Tiered: Bloom (RAM) → Cuckoo (RAM) → RocksDB (disk) |

### Two-level cascade

Google-scale crawlers use a tiered approach:
1. In-memory Bloom filter (false positive ~1%) — fastest rejection.
2. On-disk RocksDB authoritative set — consulted on Bloom hit.

This is the default pattern for > 1B URL crawlers.

## Layer 2: Content-Hash Dedup

After fetch, hash the normalized content.

### Normalization before hashing

- Strip DOCTYPE, comments, script/style blocks.
- Normalize whitespace (collapse runs to one space).
- Remove boilerplate (nav, footer, ad containers) — optional, improves signal.
- Canonicalize character encoding (UTF-8 NFC).
- For JSON responses, key-sort and re-serialize.

### Hash function

SHA-256 or Blake3. Both are collision-safe for corpus dedup. Blake3 is faster for large bodies.

Store the hash in the record. Duplicate-content URLs point to the same canonical content row.

## Layer 3: Near-Duplicate Clustering

Exact-hash dedup misses duplicates with minor differences (timestamps, session IDs, personalization). Near-dup captures these.

### SimHash (recommended for web)

64-bit locality-sensitive hash. Documents with Hamming distance ≤3 are near-duplicates (Google 2007 result).

```
1. Extract feature tokens (words / shingles) with weights (TF or TF-IDF).
2. For each feature: compute 64-bit hash.
3. Build a 64-length weight vector: for each bit in hash, add +weight if 1 else -weight.
4. Sign per bit → 64-bit SimHash.
5. Compare: Hamming distance.
```

**Scaling lookups**: permutation tables. Pre-compute rotations, index prefixes — sub-linear retrieval.

### MinHash + LSH (alternative, better for set similarity)

- Shingle document (5-word n-grams).
- Apply k MinHash functions → signature of length k (e.g. 128).
- LSH: split signature into b bands × r rows. Hash each band. Same-bucket = candidate pair.
- Jaccard similarity threshold: typical 0.7-0.9 for near-dup.

Use `datasketch` for reference.

### SSDEEP (Context-Triggered Piecewise Hashing)

- Tailored for binary / non-tokenizable data.
- Variable-length fuzzy hash with trigger-based block boundaries.
- Useful for malware corpora, binary file dedup.
- Not recommended for HTML-heavy web corpus.

### When to use which

| Content | Technique |
|---------|-----------|
| HTML pages | SimHash |
| Long text (articles, docs) | MinHash + LSH |
| Product listings | SimHash + structured-field dedup |
| Binary / files | SSDEEP or content-hash sharding |
| Short text (tweets, titles) | Exact + edit-distance (Levenshtein) |

## Bloom Filter Sizing

```
m = -n * ln(p) / (ln(2))²
k = (m/n) * ln(2)
```

Where:
- m = bits in filter
- n = expected items
- p = false positive rate
- k = number of hash functions

Example: 1B URLs @ 1% FP → ~10 bits/item → 1.25 GB RAM. Use double Bloom for rotation/aging.

## Cross-Session Persistence

Dedup state must survive crashes.

| Component | Storage |
|-----------|---------|
| URL canonical → URL id | RocksDB / Redis Cluster |
| URL-seen Bloom | periodic snapshot to disk; reload on boot |
| Content hash → canonical record | RocksDB / DynamoDB |
| SimHash signatures | RocksDB with permutation index; FAISS for large-scale |
| MinHash LSH buckets | Redis or dedicated LSH server |

### Checkpoint protocol

1. Periodic snapshot of filter state (every N minutes).
2. Journal-based write-ahead log for authoritative sets.
3. On restart: reload last snapshot + replay WAL.
4. Multi-region replication if geo-distributed.

## Workflow

```
ASSESS      →  scale: URLs/day, total corpus, retention window
            →  content diversity: HTML vs JSON vs binary mix

CANONICAL   →  design URL canonicalization rules
            →  define canonical fields (scheme/host/path/query/fragment)

LAYER-1     →  choose exact-URL dedup: in-RAM Bloom + on-disk RocksDB
            →  size Bloom filter (capacity × target FP rate)

LAYER-2     →  choose content-hash: SHA-256 or Blake3
            →  define normalization (whitespace, boilerplate)

LAYER-3     →  choose near-dup: SimHash (HTML) or MinHash (long-text)
            →  set Hamming / Jaccard threshold
            →  design permutation or LSH index

PERSIST     →  checkpoint protocol + WAL
            →  geo-replication if multi-region

MEASURE     →  dedup-rate metric per layer
            →  false-positive monitoring (sampled audit)
            →  size pressure alerting

HANDOFF     →  Builder: implementation spec per layer
            →  Schema: constraint design for canonical store
            →  Beacon: observability SLOs
```

## Output Template

```markdown
## Dedup Architecture: [Corpus]

### Scale
- URLs/day: [N]
- Total corpus: [N]
- Retention: [months]

### Layer 1: URL Dedup
- **Canonicalization rules**: [list]
- **Technique**: [Bloom + RocksDB / Cuckoo / exact]
- **Filter sizing**: [N bits, k hashes, p=N%]
- **Expected dedup rate**: [%]

### Layer 2: Content-Hash Dedup
- **Hash function**: [SHA-256 / Blake3]
- **Normalization**: [whitespace, boilerplate, encoding]
- **Store**: [RocksDB / DynamoDB]
- **Expected dedup rate**: [%]

### Layer 3: Near-Duplicate Clustering
- **Technique**: [SimHash / MinHash]
- **Threshold**: [Hamming ≤3 / Jaccard ≥0.85]
- **Index**: [permutation / LSH]
- **Expected near-dup rate**: [%]

### Persistence & Recovery
- **Checkpoint interval**: [minutes]
- **WAL path**: [...]
- **Replication**: [single / multi-region]
- **Reload protocol**: [snapshot + replay]

### Observability
- [ ] dedup_rate per layer
- [ ] false_positive_rate sampled audit
- [ ] filter_occupancy alerts
- [ ] bloom_rotation_age

### Handoffs
- Builder: per-layer implementation spec
- Schema: canonical store design
- Seek: index-time dedup alignment
- Beacon: SLO definitions
- Stream: downstream dedup contract
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| No URL canonicalization before dedup | Canonicalize first; dedup gain is often 20-40% on its own |
| Query parameters ignored entirely (over-dedup) | Drop tracking params only (utm_*, fbclid); keep semantic params |
| Single Bloom filter with no rotation | Double-buffered Bloom; rotate on capacity threshold |
| Content dedup without normalization | Whitespace/boilerplate varies; hashes miss dupes |
| SimHash without permutation index | Full-scan Hamming is O(N); use permutation for O(log N) |
| Near-dup threshold too loose (false positives) | Start strict (Hamming ≤3), loosen only with sampling audit |
| No cross-session persistence | Crash loses all dedup state; start from scratch |
| Dedup state not replicated | Single-node failure = full re-crawl risk |

## Deliverable Contract

When `dedup` completes, emit:

- **Canonicalization rules** (explicit list).
- **Three-layer dedup design** (URL / content-hash / near-dup).
- **Sizing calculations** (filter capacity, storage, lookup latency).
- **Persistence + recovery protocol**.
- **Observability hooks** per layer.
- **Handoffs**: Builder, Schema, Seek, Beacon, Stream.

## References

- Bloom — "Space/time trade-offs in hash coding with allowable errors" (1970)
- Manku, Jain, Das Sarma — "Detecting Near-Duplicates for Web Crawling" (Google 2007, SimHash permutation)
- Charikar — "Similarity estimation techniques from rounding algorithms" (SimHash origin, 2002)
- Broder — "On the resemblance and containment of documents" (MinHash, 1997)
- Indyk, Motwani — "Approximate nearest neighbors: towards removing the curse of dimensionality" (LSH, 1998)
- Fan et al. — "Cuckoo Filter: Practically Better Than Bloom" (2014)
- Roaring Bitmap — RoaringBitmap project (Lemire et al.) — preferred over bare Bitmap/Bloom for dense URL-ID sets, used by Lucene, Druid, ClickHouse
- `datasketch` Python — MinHash, LSH, HyperLogLog
- RocksDB 9.x — LSM-tree embedded KV store
- Common Crawl — operational dedup at web scale; latest dump CC-MAIN-2026-04
- Google Webmaster — URL canonicalization guidelines
