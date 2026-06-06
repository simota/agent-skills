# Legal Compliance Architecture

## Compliance as Infrastructure

Legal compliance is not an afterthought — it is a structural subsystem designed alongside the crawler. Every crawl architecture must include these components.

## robots.txt Parser Service

### Architecture

```
┌──────────────┐     ┌───────────────────┐
│  Worker N     │────▶│  robots.txt Cache │
│  (fetch URL)  │     │  Service          │
└──────────────┘     └────────┬──────────┘
                              │ Cache miss
                              ▼
                       ┌──────────────┐
                       │  Fetch       │
                       │  robots.txt  │
                       └──────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │  Parse +     │
                       │  Store       │
                       └──────────────┘
```

### Design Specifications

| Component | Specification |
|-----------|---------------|
| Cache TTL | 24 hours (default), configurable per domain |
| Cache backend | Redis with domain key, serialized parsed rules |
| Fetch failure | Fall back to conservative policy (1 req/10s, allow only root) |
| Parser | RFC 9309 compliant (2022 standard), handle wildcards, Crawl-delay |
| Versioning | Store fetch timestamp + ETag for change detection |
| User-agent matching | Match specific UA first, then `*` wildcard |

### Crawl-Delay Enforcement

```
Decision flow:
1. Check robots.txt for Crawl-delay directive for our User-Agent
2. If specified: use as minimum inter-request interval for that domain
3. If not specified: use default (1 second)
4. Apply token bucket rate limiter: burst = 1, refill = 1/crawl_delay
5. Floor: never faster than 1 request per second per domain

Edge cases:
- Crawl-delay = 0: treat as 1 second (defensive)
- Crawl-delay > 60: flag for review (may indicate "don't crawl")
- Missing robots.txt (404): no restrictions, use default rate
- Fetch error (5xx): retry 3x with backoff, then conservative policy
```

## EU AI Act Compliance (GPAI obligations live since 2025-08-02; AI Office enforcement/fines from 2026-08-02)

GPAI Code of Practice (final 2025-07-10): 26 signatories including OpenAI, Anthropic, Google, Microsoft, Amazon, IBM, Cohere, Mistral, Aleph Alpha (xAI signed only Safety chapter). Copyright chapter Commitment 1 explicitly requires signatories to "only employ web crawlers that follow the Robot Exclusion Protocol (RFC 9309) as specified by IETF, and identify and comply with other appropriate machine-readable protocols to express opt-outs." The EU Commission opened a 2025-12 stakeholder consultation on TDM opt-out protocols (Article 53(1)(c)) and will publish a maintained list of agreed machine-readable opt-out solutions, reviewed every two years.

### Opt-Out Signal Taxonomy (per EU Commission TDM consultation 2025-12)

| Signal Type | Source | Detection Method | Action |
|-------------|--------|-----------------|--------|
| Machine-readable | `robots.txt` Disallow (RFC 9309) | robots.txt parser | Block URL/path |
| Machine-readable | `X-Robots-Tag: noai` / `noimageai` | HTTP header inspection | Skip content |
| Machine-readable | `<meta name="robots" content="noai">` | HTML meta parse | Skip content |
| Machine-readable | TDM Reservation Protocol (TDMRep, W3C CG) | `tdm-reservation.json` / HTTP header | Block for TDM use |
| Machine-readable | `ai.txt` (Spawning) | Dedicated parser | Follow directives |
| Machine-readable | C2PA TDM Assertions | Manifest inspection | Honor assertion |
| Machine-readable | Do Not Train registry (Spawning AI) | API lookup | Block domain/URL |
| Machine-readable | JPEG Trust core foundation v2 | Image metadata | Honor flag |
| Machine-readable | TDM.ai protocol (Liccium) | Dedicated parser | Honor directives |
| Editorial-curation | `llms.txt` (Answer.AI proposal) | Dedicated parser | Treat as content-guidance, NOT opt-out (10.13% adoption Q1 2026; no major AI vendor commits to it in production) |
| Plain-text | ToS "no scraping" clause | Manual review → domain blocklist | Block domain |
| Plain-text | ToS "no AI training" clause | Manual review → domain blocklist | Block domain (German courts: plain-text reservation valid under Copyright Directive 2019/790 Art 4) |

### Implementation Pattern

```
Opt-out check pipeline (per URL):
1. robots.txt check (cached) → blocked? → skip
2. HTTP response headers → X-Robots-Tag check → noai? → skip content, keep metadata
3. HTML <meta> tags → noai? → skip content, keep metadata
4. Domain blocklist check (manually curated from ToS review) → blocked? → skip
5. Pass → proceed with extraction

Log every opt-out decision for audit trail.
```

### Penalty Framework

| Violation | Penalty (EU AI Act) |
|-----------|---------------------|
| GPAI data obligations (Art. 53) | Up to €15M or 3% global revenue (Art. 101); AI Office enforcement powers active from 2026-08-02 |
| Copyright opt-out violation | National copyright law + EU AI Act overlay |
| Data minimization failure (GDPR) | Up to €20M or 4% global turnover (Art. 83) |

### Pay-Per-Crawl economic compliance layer (Cloudflare 2025-07 GA / 2025-08-28 AI Crawl Control)

For AI-training and inference crawlers targeting Cloudflare-fronted sites (~20% of public web), the architecture must include a payment-aware fetcher path:

1. On HTTP 402 Payment Required + `crawler-price` header → decide via budget policy.
2. To accept: retry with `crawler-exact-price` header matching the quote.
3. Success returns HTTP 200 + `crawler-charged` header (Cloudflare bills aggregately as Merchant of Record).
4. Verified-crawler registration with Cloudflare is required for the AI-bot category (`crawler-id` claim).
5. Alternative monetized brokers: TollBit, ProRata, Vellum, Bright Data licensed feeds, Diffbot Knowledge Graph.

## Jurisdiction Risk Table (2026-05)

| Jurisdiction | Key Law | Risk Level | Key Requirement |
|-------------|---------|------------|-----------------|
| EU | AI Act + GDPR + Copyright Directive 2019/790 Art 4 (TDM opt-out) | High | Respect all machine-readable opt-out signals (RFC 9309 robots.txt + TDMRep + others on EU Commission's list), data minimization, DPIA for PII; GPAI fines from 2026-08-02 (up to €15M or 3% revenue) |
| US | CFAA (post Van Buren / hiQ Ninth Circuit 2022) + state laws + Fair Use | Medium | hiQ v. LinkedIn settled 2024-12 with permanent injunction against hiQ + $500K damages — CFAA does NOT prohibit scraping public data, but ToS + state-law + copyright + trespass-to-chattels claims remain (Reddit v. Anthropic 2025, Reddit v. Perplexity 2025-10-22, NYT v. Perplexity 2025-12-05, Anthropic-Authors $1.5B settlement 2025-09). Architecture must avoid hard-block circumvention (NYT alleged Perplexity bypassed hard-block). |
| UK | UK GDPR + ICO guidance | Medium-High | Similar to EU, ICO enforcement actions |
| Japan | Copyright Act Art. 30-4 (informational analysis exception, 2018) | Low-Medium | Broad research/AI training exception, but commercial collection should respect opt-out signals; cultural agency 2024 guidance flagged "unjustly prejudice the interests" carve-out |
| China | Personal Information Protection Law (PIPL) + DSL | High | Strict consent requirements for PII; cross-border transfer restrictions |
| Australia | Privacy Act + Copyright Act | Medium | Fair dealing defense, privacy obligations |

## Sitemaps Integration

### Design Pattern

```
Sitemap as priority signal, NOT exhaustive URL source:
1. Fetch /sitemap.xml (or sitemap index)
2. Parse lastmod, changefreq, priority attributes
3. Inject URLs into frontier with priority boost
4. Do NOT rely solely on sitemap — many sites have incomplete sitemaps
5. Sitemap URLs get priority level 2 (below seeds, above discovered links)

Cache: Same TTL as robots.txt (24h)
Formats: XML sitemap, sitemap index, RSS/Atom feed
```

## Audit Trail Design

### What to Log

| Event | Fields | Retention |
|-------|--------|-----------|
| robots.txt fetch | domain, timestamp, status, rules_hash | 90 days |
| Opt-out detection | url, signal_type, action_taken | 1 year |
| Domain block | domain, reason, blocked_by, timestamp | Indefinite |
| Crawl-delay override | domain, requested_delay, applied_delay | 90 days |
| PII detection | url, pii_type, action_taken | 1 year (or per policy) |

### Storage

```
Audit log format: JSON-Lines, append-only
Storage: S3/GCS with lifecycle policy
Indexing: Date-partitioned for efficient querying
Access: Read-only for audit, write-only for crawler
```
