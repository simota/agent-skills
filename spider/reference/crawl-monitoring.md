# Crawl Monitoring Reference

Purpose: Design observability for a distributed crawler fleet — fetch rate, frontier depth, error taxonomy, cost-per-URL, politeness adherence, and graceful shutdown/resume. Spider emits monitoring specs; Builder wires metrics; Beacon owns SLO/SLI enforcement.

## Scope Boundary

- **spider `monitoring`**: Crawler-specific observability (this document).
- **spider `frontier` / `politeness` / `extraction` (elsewhere)**: Components being monitored.
- **Beacon (elsewhere)**: General SLO/SLI framework. Spider hands off specific signals to Beacon.
- **Stream (elsewhere)**: Downstream data quality (Great Expectations). Crawl monitoring ends before ETL.
- **Triage (elsewhere)**: Incident response. Crawl monitoring feeds alerts.

## Signal Categories

| Category | Questions answered |
|----------|---------------------|
| Throughput | Am I crawling fast enough? |
| Saturation | Is the fleet at capacity? |
| Errors | What's failing and why? |
| Cost | What does each URL cost? |
| Compliance | Am I respecting robots.txt and rate limits? |
| Freshness | How stale is the corpus? |
| Progress | Is the frontier draining? |

## Core Metrics

### Throughput

| Metric | Target example | Why |
|--------|----------------|-----|
| `crawl_fetch_rate_per_sec` | sustained >N | Sanity check on worker pool |
| `crawl_fetch_rate_per_domain` | ≤ domain budget | Politeness compliance |
| `crawl_fetch_success_rate` | > 95% | Filter bad targets early |
| `crawl_urls_per_worker_sec` | ≥ saturation benchmark | Detect slow workers |
| `crawl_bytes_per_sec` | within bandwidth budget | Capacity planning |

### Saturation

| Metric | Alert |
|--------|-------|
| `worker_cpu_util` | >85% for 10 min |
| `worker_memory_util` | >90% |
| `frontier_queue_depth` | growing unbounded |
| `dns_resolver_latency_p99` | >200 ms |
| `proxy_pool_healthy_ratio` | <80% |

### Error taxonomy

Categorize every failure. Aggregate and dashboard.

| Class | Example status / signal | Action |
|-------|------------------------|--------|
| DNS failure | NXDOMAIN, timeout | Retry with different resolver; blacklist |
| TCP / TLS | connection refused, handshake failure | Retry with backoff; check TLS fingerprint |
| HTTP 4xx | 403/404/410 | Suppress re-crawl; remove from frontier |
| HTTP 429 | rate limit | Adaptive backoff; reduce domain concurrency |
| HTTP 5xx | server error | Exponential backoff; cap retries |
| Timeout | fetch > N s | Proxy rotation; different egress |
| Parse error | bad encoding, truncation | Quarantine for manual review |
| Render failure | headless crash | Fallback to static; alert on rate |
| Robots disallow | path excluded | Log + never retry |
| Size limit | body > N MB | Truncate or skip |
| Content-type mismatch | expected HTML, got binary | Skip or re-route to binary pipeline |

### Cost-per-URL

```
cost_per_url = (compute_cost + egress_cost + proxy_cost + storage_cost) / urls_fetched
```

Track monthly. Alert on 20%+ trend change.

Compute includes render layer (headless is 10-40x static). Egress includes response bytes + proxy middleman. Proxy cost varies by tier (datacenter / residential / mobile). Storage = compressed write + index.

### Compliance

| Signal | Why |
|--------|-----|
| `robots_txt_refresh_age_max` | Stale robots → illegal crawl |
| `domain_crawl_delay_violations` | Politeness breach — legal risk |
| `concurrent_connections_per_domain_violations` | Same |
| `ai_opt_out_signal_observed` (robots.txt / X-Robots-Tag / TDMRep / ai.txt / C2PA) | EU AI Act Art. 53 compliance; GPAI fines from 2026-08-02 |
| `tdm_reservation_respected_ratio` | Same |
| `pay_per_crawl_402_responses` | Cloudflare Pay-Per-Crawl economic budget tracking |
| `pay_per_crawl_charged_total_usd` | Cumulative paid-crawl spend |
| `fleet_wide_concurrent_per_target` | Prevents DDoS-equivalent traffic (Trilegangers / OpenAI 600-IP / 39K req/min incident pattern) |

### Freshness

For re-crawl pipelines:

| Metric | Purpose |
|--------|---------|
| `corpus_p50_age_days` | Median staleness |
| `corpus_p99_age_days` | Worst-case staleness |
| `recrawl_queue_depth` | Re-crawl lag |
| `change_detection_hit_rate` | Last-Modified / ETag signal coverage |

### Progress

| Metric | Use |
|--------|-----|
| `frontier_size_total` | Total pending |
| `frontier_size_per_domain_p99` | Tail domains |
| `frontier_drain_rate` | URLs fetched / URLs added |
| `frontier_depth_p99` | Graph BFS depth reached |
| `seed_completion_ratio` | % of seeds that have reached target depth |

If drain_rate < 1 sustained, the frontier grows unbounded → crawl will never finish.

## RED Method per Worker

Apply Google-SRE's RED (Rate, Errors, Duration) at the worker layer:

| Signal | Meaning for a crawler worker |
|--------|------------------------------|
| **Rate** | fetches per second |
| **Errors** | fetches returning non-2xx / timeout / crash |
| **Duration** | end-to-end fetch + render latency p50/p95/p99 |

## USE Method for Infrastructure

Apply USE (Utilization, Saturation, Errors) at infrastructure layer:

| Resource | U | S | E |
|----------|---|---|---|
| CPU | util % | run-queue depth | exceptions |
| Memory | used / total | swap rate | OOM kills |
| Network | Mbps / capacity | queue drops | iface errors |
| Disk | IOPS used / max | queue depth | I/O errors |
| DNS resolver | qps / capacity | timeout rate | NXDOMAIN rate |

## Graceful Shutdown & Resume

A crawler must be restartable without losing data.

### Shutdown protocol

1. Coordinator signals workers to drain.
2. Workers finish in-flight fetches; do not pick up new URLs.
3. Workers flush any buffered writes to durable storage.
4. Workers persist their checkpoint (which batch ID last completed).
5. Coordinator records shutdown timestamp + frontier snapshot.

### Resume protocol

1. On start, coordinator loads last frontier snapshot.
2. Replay WAL of any URLs dispatched but not confirmed.
3. Re-dispatch unconfirmed URLs (idempotent via content hash).
4. Workers resume with their saved checkpoint.
5. Re-hydrate dedup filters from disk snapshots.

### Checkpoint cadence

- Frontier snapshot: every N minutes (e.g., 5).
- Dedup filter snapshot: every M minutes (e.g., 15).
- Worker-level checkpoint: every K fetched URLs (e.g., 100).

## Dashboard Layout (Canvas handoff)

```
Row 1: SLO overview
  - fetch success SLO (rolling 30d)
  - p99 fetch latency SLO
  - cost-per-URL trend

Row 2: Throughput
  - fleet fetch rate (per second)
  - per-region fetch rate
  - fetch rate per worker (heatmap)

Row 3: Errors (stacked area)
  - 4xx / 5xx / timeout / DNS / TLS / render
  - top N domains by error count

Row 4: Frontier
  - total pending (line)
  - drain rate (ratio)
  - per-domain queue heatmap

Row 5: Compliance
  - crawl-delay violations
  - robots refresh freshness
  - opt-out signal respect ratio

Row 6: Cost
  - cost per URL (daily)
  - by render mode (static vs headless)
  - by region / proxy tier
```

## Alerting Tiers

| Severity | Condition | Response |
|----------|-----------|----------|
| P0 | fleet down, fetch rate = 0 for 5 min | page on-call |
| P1 | fetch success < 80% for 15 min | alert team channel |
| P1 | robots-violation rate > 0.1% | alert + pause affected domain |
| P2 | frontier unbounded growth 30 min | daytime investigation |
| P2 | cost-per-URL +20% DoD | budget owner review |
| P3 | freshness degradation | weekly report |

Follow Google SRE multi-burn-rate alerting for SLO-based alerts.

## Workflow

```
DEFINE     →  identify signals per layer (throughput / saturation / errors / cost / compliance)
           →  set SLO targets (success rate, latency, freshness)

INSTRUMENT →  design structured logs (OpenTelemetry Logs)
           →  design metrics (OpenTelemetry Metrics, Prometheus format)
           →  design traces (per-URL trace id, sample rate)

BUDGET     →  compute error budget from SLO
           →  design multi-burn-rate alerts (fast/slow)

DASHBOARD  →  lay out RED/USE + crawler-specific panels
           →  hand off to Canvas for visualization
           →  hand off to Beacon for SLO ownership

RUNBOOK    →  per-alert response runbook
           →  escalation tree
           →  hand off to Triage for incident response

SHUTDOWN   →  design graceful shutdown + resume protocol
           →  checkpoint cadences
```

## Output Template

```markdown
## Crawl Monitoring: [Fleet / Corpus]

### SLO Targets
| SLI | Target | Window |
|-----|--------|--------|
| fetch_success_rate | ≥ 95% | rolling 30d |
| fetch_latency_p95 | ≤ 3s | rolling 7d |
| robots_respect | = 100% | rolling 24h |
| cost_per_url | ≤ $[N] | rolling 30d |

### Metrics (OpenTelemetry)
- `crawl_fetch_rate_per_sec` (counter)
- `crawl_fetch_duration_seconds` (histogram)
- `crawl_error_count` (counter; labels: class, domain)
- `crawl_frontier_size` (gauge)
- `crawl_dedup_hit_rate` (gauge)
- `crawl_cost_per_url_cents` (gauge)
- `crawl_robots_age_seconds` (gauge)

### Error Taxonomy
[list all error classes with expected rates]

### Cost Model
- compute: $[N] per 1M URLs
- egress: $[N] per 1M URLs
- proxy: $[N] per 1M URLs
- storage: $[N] per 1M URLs
- **total**: $[N] per 1M URLs

### Alerts
| Severity | Condition | Runbook |
|----------|-----------|---------|
| P0 | ... | ... |
| P1 | ... | ... |
| ... | ... | ... |

### Graceful Shutdown
- Frontier snapshot: every [N] min
- Dedup snapshot: every [M] min
- Worker checkpoint: every [K] URLs
- Resume replay: WAL since last confirmed batch

### Handoffs
- Beacon: SLO ownership + error budget tracking
- Canvas: dashboard rendering
- Triage: per-alert runbooks
- Builder: implementation of instrumentation
- Ledger: cost dashboards and anomaly detection
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| One global success rate only | Per-domain and per-error-class; aggregate view hides hotspots |
| No graceful shutdown | Crash = data loss + long re-hydration |
| No frontier drain-rate metric | Unbounded growth goes unnoticed for days |
| No per-render-mode cost breakdown | Headless overuse can 10x costs invisibly |
| No compliance metric | Legal / regulatory blind spot |
| Alert on every 5xx | Pager fatigue; use SLO burn rate instead |
| Metrics without traces | Hard to debug specific URL failures |
| Logs only, no structured events | Can't aggregate or trend |
| Dashboard overload (50+ panels) | Design RED/USE per layer + crawler-specific panels |

## Deliverable Contract

When `monitoring` completes, emit:

- **SLO table** with SLI definitions and targets.
- **Metric catalog** (OpenTelemetry names, labels, type).
- **Error taxonomy** with expected rates.
- **Cost model** per URL.
- **Alert matrix** with runbook links.
- **Graceful shutdown / resume protocol** with checkpoint cadences.
- **Dashboard layout spec** for Canvas handoff.
- **Handoffs**: Beacon, Canvas, Triage, Builder, Ledger.

## References

- Google SRE Book — chapters on SLIs, SLOs, Error Budgets, Multi-Burn-Rate Alerting
- Google SRE Workbook — practical SLO patterns
- OpenTelemetry — spec for metrics, logs, traces (Traces/Metrics/Logs all Stable across major SDKs as of early 2026; Profiling signal RC Q1 2026, GA targeted Q3 2026)
- Prometheus — metric naming conventions and histogram guidance
- Brendan Gregg — USE Method for resource analysis
- Tom Wilkie — RED Method for service-level metrics
- Common Crawl operational blog — web-scale crawl observability learnings (latest dumps CC-MAIN-2026-04)
- Google's Webmaster logs — crawler-side signals from the inverse perspective
- Cloudflare AI Crawl Control docs — 402 Pay-Per-Crawl protocol, `crawler-price` / `crawler-exact-price` / `crawler-charged` headers
- Cloudflare radar 2026-01: Googlebot reaches 1.76x more unique URLs than GPTBot, 2.99x more than Meta-ExternalAgent, 3.26x more than Bingbot, 167x more than PerplexityBot, 714x more than CCBot
- Site Reliability Engineering Anti-patterns (O'Reilly, 2020)
