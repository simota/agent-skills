# Extraction Pipeline Deep-Dive Reference

Purpose: Design the full extraction pipeline for a web-scale crawler — from the render layer (static HTML vs JavaScript-rendered) through parsing (DOM/XPath/CSS/LLM), structured-data harvesting (JSON-LD / microdata / OpenGraph), near-duplicate detection, and output schema. Spider emits the architecture; Builder implements; Stream consumes.

## Scope Boundary

- **spider `extraction`**: Pipeline-level architecture (this document).
- **spider `frontier` (elsewhere)**: Input side — URL management.
- **spider `dedup` (elsewhere)**: Deduplication (URL + content + near-dup).
- **Navigator (elsewhere)**: Single-session scraping execution.
- **Stream (elsewhere)**: Downstream ETL of extracted data.
- **Grok (elsewhere)**: Regex/parser grammar authoring details.

## Pipeline Stages

```
URL  →  RENDER  →  PARSE  →  STRUCTURE  →  NEAR-DUP  →  SCHEMA  →  WRITE
        layer     layer    harvest       detection   selection   to sink
```

Each stage is independently swappable. Design for a fleet: decisions apply across millions of URLs.

## Stage 1: Render Layer

| Mode | When | Cost multiplier (vs static) |
|------|------|------------------------------|
| Static HTTP fetch (curl_cffi / httpx) | Content in initial HTML | 1x |
| Light JS (prerender hints) | `<noscript>` fallback works | 1.2x |
| Headless browser (Playwright 1.49+ / Puppeteer 23+) | SPA, hydration required | 8-20x |
| Remote browser farm (Browserless v2, Scrapfly, Bright Data Scraping Browser) | Geo / CAPTCHA / detection concerns | 20-40x |
| Prerender.io / cached rendering service | Public SPAs with SEO prerender | 3-6x |
| LLM-friendly crawler (Crawl4AI 0.8+, Firecrawl) | LLM/RAG output needed as Markdown | 3-8x (includes content cleaning) |

### Selection rules

- Default to static HTTP. Confirm via sampled render diff.
- If > 40% of target data arrives only post-hydration → headless.
- If target domain uses Cloudflare/Akamai JA4 fingerprinting → curl_cffi (Python) or stealth browser (undetected-chromedriver, Playwright-stealth, patchright). Plain `requests`/`httpx`/`Scrapy` default TLS will be blocked.
- If target is on Cloudflare with AI default-block (post 2025-07): expect HTTP 403 or HTTP 402 Pay-Per-Crawl quote — route to compliance path, not anti-detect.
- If geo-walled → proxy-routed browser farm.

### Headless cost drivers

- Startup time (500-2000 ms per session).
- DOM memory (50-300 MB per tab).
- CPU (JS evaluation + layout).
- Network (full asset load vs request interception).

Request interception (blocking images, fonts, analytics) cuts cost 40-70%.

## Stage 2: Parse Layer

| Strategy | Strengths | Weaknesses | Use when |
|----------|-----------|-----------|----------|
| `lxml` + XPath | Fast, C-backed, precise | Brittle to layout changes | High-volume, stable layout |
| BeautifulSoup | Lenient, Pythonic | Slower, tree rebuild | Forgiving HTML, small scale |
| Scrapy selectors | Built-in, XPath+CSS | Scrapy-coupled | Inside Scrapy runtime |
| Parsel | Scrapy selector standalone | Same as selectors | Non-Scrapy Python |
| `cheerio` (Node) | jQuery-like | Memory per tree | Node/TS workflows |
| Playwright DOM queries | Post-render access | Headless-coupled | SPA-only data |
| Readability / trafilatura | Article body extraction | Article-oriented only | News/blog body capture |
| LLM extraction (Claude/GPT) | Schema-free, resilient | Cost, latency, hallucination | Long-tail unstructured |
| Hybrid (deterministic + LLM fallback) | Best of both | Routing complexity | Mixed-structure sources |

### Parser selection matrix

| Target shape | First choice | Fallback |
|--------------|--------------|----------|
| Product page (e-commerce) | XPath + JSON-LD | Readability |
| Article body | Trafilatura | Readability |
| Job listings | XPath | LLM extraction |
| Forum thread | CSS selectors | XPath |
| SPA dashboard | Playwright DOM | LLM extraction |
| PDF-embedded | PyMuPDF / Unstructured | OCR (Tesseract) |

## Stage 3: Structured-Data Harvest

Most modern sites embed machine-readable data. Harvest these first — they are schema-stable.

| Source | Priority | Notes |
|--------|----------|-------|
| JSON-LD (`<script type="application/ld+json">`) | Highest | Schema.org classes; preferred by Google |
| Microdata (`itemscope/itemprop`) | High | HTML5 inline |
| RDFa | Medium | Declining use |
| OpenGraph (`og:*` meta) | Medium | Social-card-friendly |
| Twitter Card (`twitter:*`) | Medium | Redundant with OG |
| Microformats (h-entry, h-card) | Low | IndieWeb niche |
| Sitemaps (xml) | High | URL discovery; change hints |
| hreflang/alternate | Medium | Multi-language graph |
| Pagination rels (`rel="next"`) | High | Follow for list pages |

### Schema.org classes worth knowing

`Product`, `Offer`, `Article`, `NewsArticle`, `BlogPosting`, `Recipe`, `JobPosting`, `Event`, `Organization`, `Person`, `Place`, `Review`, `AggregateRating`, `BreadcrumbList`, `FAQPage`, `HowTo`, `Movie`, `Book`.

## Stage 4: Near-Duplicate Detection

Full pipeline dedup happens later; at extraction time, detect near-duplicates to drop before downstream storage.

| Technique | Signature size | Best for |
|-----------|----------------|----------|
| SimHash (64-bit) | 64 bits | Web-scale page-level dedup |
| MinHash + LSH | 128-256 hashes | Shingled document dedup |
| SSDEEP (CTPH) | ~80 chars | Malware / binary near-dup |
| Shingling (w=5 word n-grams) | Set of hashes | Jaccard similarity base |
| Simhash Hamming distance | ≤3 = near-dup | Google-style web dedup |

### SimHash pipeline

1. Extract visible text (strip nav, footer, ads).
2. Tokenize → weights (TF or TF-IDF).
3. 64-bit feature hashes → sum weighted bit vector.
4. Take sign per bit → 64-bit signature.
5. Hamming distance ≤3 → near-duplicate.

Store signatures in a 64-bit index for O(1) lookup. Use permutation tables for sub-Hamming-distance clustering at scale.

### MinHash + LSH

1. Shingle document (word 5-grams).
2. Hash shingles with k MinHash functions.
3. LSH banding (b bands × r rows) → bucket similar docs.
4. Jaccard threshold typically 0.7-0.8 for near-dup.

Use `datasketch` (Python) or `simhash-py` for reference implementations.

## Stage 5: Output Schema

| Format | When | Notes |
|--------|------|-------|
| WARC (Web ARChive) | Full fidelity corpus (Common Crawl compatible) | Archive-grade; large |
| JSON Lines (JSONL) | Standard pipeline ingestion | Stream-friendly, tool-universal |
| Parquet (columnar) | Analytics workloads | Compressed, column-pruning |
| Avro | Schema-evolution critical | Kafka-native |
| Protobuf / msgpack | Tight binary with schema | Low-latency pipelines |
| HTML + metadata sidecar | Rerun-ability preserved | Reprocessable |

### Minimum record fields

```json
{
  "url": "...",
  "url_canonical": "...",
  "fetched_at": "ISO8601",
  "status": 200,
  "content_type": "text/html; charset=utf-8",
  "content_sha256": "...",
  "simhash": "...",
  "render_mode": "static | headless",
  "final_url": "...",
  "response_headers": {...},
  "extracted": { "schema.org/Product": {...} },
  "text": "...",
  "html_compressed": "base64/gz(...)",
  "crawl_source": "frontier_id"
}
```

## Workflow

```
CLASSIFY    →  per-domain, decide render mode (static vs headless)
            →  per-page-type, decide parser strategy

HARVEST     →  JSON-LD / microdata first (schema.org)
            →  then XPath/CSS for site-specific data
            →  LLM fallback for unstructured long-tail

NEAR-DUP    →  SimHash or MinHash on visible text
            →  drop at Hamming ≤3 or Jaccard ≥0.85
            →  log dropped counts for observability

NORMALIZE   →  common entity schema (Product / Article / Job / ...)
            →  currency / timezone / language tags

WRITE       →  choose WARC / JSONL / Parquet
            →  include fetch metadata + content hash + simhash

HANDOFF     →  Stream: ETL spec + schema contract
            →  Seek: index ingestion format
            →  Cloak: PII surface area from extracted fields
```

## Output Template

```markdown
## Extraction Pipeline: [Corpus / Target]

### Scale
- URLs/day: [N]
- Domains: [N]
- Render mode mix: static [%] / headless [%]

### Render Layer
- **Default**: [static HTTP / headless]
- **Headless trigger**: [domains / page patterns]
- **Cost model**: [$ per 1M pages]

### Parse Strategy
| Target shape | Parser | Fallback |
|--------------|--------|----------|
| ... | ... | ... |

### Structured Harvest
- [ ] JSON-LD (schema.org classes: [list])
- [ ] Microdata
- [ ] OpenGraph
- [ ] Sitemaps

### Near-Dup
- **Technique**: [SimHash / MinHash]
- **Threshold**: [Hamming ≤3 / Jaccard ≥0.85]
- **Expected dedup rate**: [%]

### Output Schema
- **Format**: [WARC / JSONL / Parquet]
- **Required fields**: [list]
- **Partitioning**: [by date / domain / hash-prefix]

### Observability hooks
- [ ] Extraction success rate
- [ ] Schema-coverage rate
- [ ] Dedup drop rate
- [ ] LLM-fallback invocation rate (cost)

### Handoffs
- Stream: pipeline contract
- Seek: search-index contract
- Cloak: PII surface analysis
- Beacon: extraction-layer SLOs
- Builder: implementation spec
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Headless everywhere | Default static; escalate based on render-diff sampling |
| Loading images/fonts in headless | Request interception — block by default |
| Ignoring JSON-LD, parsing HTML manually | Always try structured-data first |
| LLM for every page | LLM is fallback, not default — cost explodes |
| No near-dup at extraction time | Dedup downstream is more expensive |
| WARC for operational pipelines | WARC = archival; use JSONL/Parquet for ops |
| No content hash stored | Can't verify or dedup cross-run |
| Parser per site with no shared abstraction | Shared entity schema + per-site adapters |

## Deliverable Contract

When `extraction` completes, emit:

- **Render-layer decision** with cost estimate.
- **Parser strategy** per page-type.
- **Structured-data harvesting** plan.
- **Near-duplicate technique** + threshold.
- **Output schema** + format + partitioning.
- **Observability hooks** for each stage.
- **Handoffs**: Stream, Seek, Cloak, Beacon, Builder.

## References

- Google — *Web Crawling* (Brin & Page 1998; Najork 2009 survey)
- Common Crawl — WARC format and pipeline; CC-MAIN-2026-04 latest crawl + webgraph cc-main-2025-26-nov-dec-jan (250.8M host nodes / 10.9B edges)
- `datasketch` — MinHash / LSH / HyperLogLog Python library
- `simhash-py`, `simhash-java` — SimHash reference implementations
- Manku, Jain, Das Sarma — "Detecting Near-Duplicates for Web Crawling" (Google 2007)
- Scrapy 2.13 — documentation on selectors, middleware, and pipelines
- Playwright 1.49+ / Puppeteer 23+ — docs on request interception and resource blocking
- Trafilatura — article body extraction library + benchmarks
- Crawl4AI 0.8+ — LLM-friendly crawler, async, Markdown output for RAG (PyPI 2026-03)
- Firecrawl — LLM-ready scraping API
- Unstructured.io — multi-format extraction toolkit
- `extruct` — structured-data harvester (JSON-LD/microdata/RDFa/OpenGraph)
- curl-impersonate / curl_cffi — JA4-resistant TLS impersonation library
