# Extraction Pipeline Design

## Pipeline Architecture

```
  Fetched Document
        │
        ▼
  ┌───────────┐
  │  Content   │──── Content-Type routing
  │  Router    │
  └─────┬─────┘
        │
   ┌────┼────┬────────┐
   ▼    ▼    ▼        ▼
  HTML  JSON  PDF    Other
   │    │     │       │
   ▼    ▼     ▼       ▼
  ┌───────────────────────┐
  │  Structured Extraction│──── CSS/XPath/JSON-LD mapping
  └───────────┬───────────┘
              │
              ▼
  ┌───────────────────────┐
  │  Content Dedup        │──── SimHash/MinHash
  └───────────┬───────────┘
              │
              ▼
  ┌───────────────────────┐
  │  Canonical Resolution │──── URL normalization + redirect
  └───────────┬───────────┘
              │
              ▼
  ┌───────────────────────┐
  │  Output Serialization │──── WARC/JSON-Lines/Parquet
  └───────────────────────┘
```

## HTML Parser Selection

| Parser | Speed | Tolerance | Memory | Best For |
|--------|-------|-----------|--------|----------|
| lxml | Fast (C-based) | Moderate | Low | Large-scale, well-formed HTML |
| BeautifulSoup 4.13 + html5lib | Slow | High | High | Broken/malformed HTML |
| BeautifulSoup 4.13 + lxml | Fast | Moderate | Low | General purpose (recommended default) |
| Streaming SAX | Fastest | Low | Minimal | Very large documents (>10 MB) |
| Selectolax (modest fork 2026) | Very fast | Moderate | Low | High-throughput extraction |
| Trafilatura 1.x | Fast | High | Low | Article body extraction (news/blog), beats Readability in benchmarks |

### Decision Flow

```
Document size > 10 MB? → Streaming SAX
Malformed HTML likely? → BeautifulSoup + html5lib
High throughput required? → lxml or Selectolax
General purpose? → BeautifulSoup + lxml (default)
```

## Structured Data Extraction

### Schema.org / JSON-LD Extraction

```
Strategy:
1. Find all <script type="application/ld+json"> tags
2. Parse JSON, validate against schema.org types
3. Extract relevant fields to unified schema
4. Fall back to Microdata/RDFa if JSON-LD absent

Common types:
- Product: name, price, availability, reviews
- Article: headline, datePublished, author, body
- Organization: name, url, logo, contact
- Event: name, startDate, location, offers
- BreadcrumbList: navigation structure
```

### CSS/XPath Selector Extraction

```
Design pattern — extraction schema per page type:

{
  "page_type": "product_listing",
  "selectors": {
    "title": "h1.product-title",
    "price": "span.price-current",
    "description": "div.product-description",
    "images": "img.product-image::attr(src)",
    "reviews": {
      "container": "div.review-item",
      "author": "span.reviewer-name",
      "rating": "span.star-rating::attr(data-rating)",
      "text": "p.review-text"
    }
  },
  "pagination": {
    "next": "a.next-page::attr(href)",
    "strategy": "follow_next"
  }
}
```

## Near-Duplicate Detection

### SimHash

```
Algorithm:
1. Tokenize document (shingles of width 3-5 words)
2. Hash each shingle (64-bit hash)
3. Weight and accumulate bit vectors
4. Threshold: output 64-bit fingerprint

Comparison:
- Hamming distance ≤ 3 = near-duplicate (for 64-bit hash)
- Hamming distance 4-6 = possibly related
- Hamming distance > 6 = distinct

Storage: 8 bytes per document → 80 GB for 10 billion documents
Lookup: Bit permutation indexing for sub-linear search
```

### MinHash (with LSH)

```
Algorithm:
1. Tokenize document (character n-grams or word shingles)
2. Apply k independent hash functions (k = 128 typical)
3. Keep minimum hash value for each function → signature

Comparison:
- Jaccard similarity ≈ fraction of matching minhash values
- Jaccard ≥ 0.8 = near-duplicate
- Jaccard ≥ 0.5 = substantially similar

LSH for efficient lookup:
- Divide signature into b bands of r rows
- Hash each band → bucket
- Candidate pairs: any shared bucket
- Typical: b=20, r=5 → catches pairs with Jaccard ≥ 0.5
```

### Selection Guide

| Factor | SimHash | MinHash + LSH |
|--------|---------|---------------|
| Speed | Faster (single fingerprint) | Slower (k hashes) |
| Storage | 8 bytes/doc | 128-512 bytes/doc |
| Accuracy | Good for near-exact dupes | Better for partial overlap |
| Scalability | Better (smaller signatures) | Requires LSH infrastructure |
| Use case | Web page dedup (boilerplate detection) | Document clustering, content similarity |

**Recommendation:** SimHash for web-scale dedup (memory efficient), MinHash+LSH for content similarity analysis.

## Output Format Comparison

| Format | Size | Query | Streaming | Archival | Best For |
|--------|------|-------|-----------|----------|----------|
| WARC | Large | Poor | Good | Excellent | Web archiving, legal preservation |
| JSON-Lines | Medium | Moderate | Excellent | Good | Streaming pipelines, real-time |
| Parquet | Small (compressed) | Excellent | Poor | Good | Analytics, batch processing |
| CSV | Small | Poor | Good | Poor | Simple exports, small datasets |

### WARC (Web ARChive)

```
ISO 28500 standard format
- Preserves: HTTP headers, response body, metadata, timestamps
- Tools: warcio (Python), WARC module
- Use when: Legal preservation, full fidelity needed, Internet Archive compatibility
- Typical size: 2-3x raw content (headers + metadata overhead)
```

### JSON-Lines

```
One JSON object per line
- Fields: url, timestamp, content, metadata, headers, status_code
- Tools: standard JSON parsers
- Use when: Streaming to Kafka/pipeline, real-time processing
- Compression: gzip reduces ~80%
```

### Parquet

```
Columnar storage format
- Schema: url (string), content (string/binary), metadata (struct), timestamp (int64)
- Compression: Snappy/ZSTD (70-90% reduction)
- Tools: PyArrow, Spark, DuckDB
- Use when: Downstream analytics, SQL queries, batch processing
- Partitioning: By crawl_date, domain, or content_type
```

## Redirect Chain Handling

```
Configuration:
- Max hops: 5 (default)
- Loop detection: track visited URLs in chain
- Final URL: use for dedup and canonical resolution
- Preserve chain: log full redirect chain for audit

Decision table:
  301 (Permanent) → Follow, update canonical to final URL
  302 (Temporary) → Follow, keep original as canonical
  303 (See Other) → Follow, log as reference
  307 (Temporary) → Follow, keep original as canonical
  308 (Permanent) → Follow, update canonical to final URL
  Meta refresh → Follow if < 5 seconds delay
  JavaScript redirect → Flag for Navigator handoff (requires browser)
```
