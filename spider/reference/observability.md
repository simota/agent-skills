# Crawl Observability Design

## Overview

Crawl observability ensures the system is operating correctly, efficiently, and within compliance bounds. It covers metrics collection, dashboards, alerting, cost modeling, and graceful shutdown monitoring.

## Prometheus Metrics

### Core Metrics

| Metric | Type | Labels | Unit | Description |
|--------|------|--------|------|-------------|
| `crawler_urls_fetched_total` | Counter | `domain`, `status_code`, `worker_id` | count | Total URLs fetched |
| `crawler_urls_discovered_total` | Counter | `source` (link/sitemap/seed) | count | Total URLs added to frontier |
| `crawler_frontier_depth` | Gauge | `priority_level` | count | Current pending URLs in frontier |
| `crawler_frontier_breadth` | Gauge | — | count | Number of distinct domains in frontier |
| `crawler_fetch_duration_seconds` | Histogram | `domain`, `content_type` | seconds | Fetch latency distribution |
| `crawler_fetch_bytes_total` | Counter | `domain`, `content_type` | bytes | Total bytes downloaded |
| `crawler_error_total` | Counter | `domain`, `error_category` | count | Fetch errors by category |
| `crawler_extraction_duration_seconds` | Histogram | `parser_type` | seconds | Extraction pipeline latency |
| `crawler_dedup_hit_total` | Counter | — | count | URLs rejected by dedup (seen-set hit) |
| `crawler_compliance_block_total` | Counter | `signal_type` (robots / x-robots-tag / tdmrep / ai.txt / c2pa / tos / pay-per-crawl-402) | count | URLs blocked by compliance |
| `crawler_pay_per_crawl_402_total` | Counter | `domain`, `outcome` (accepted/declined) | count | Cloudflare 402 Pay-Per-Crawl events |
| `crawler_pay_per_crawl_charged_cents` | Counter | `domain` | cents | Cumulative paid-crawl spend |
| `crawler_worker_active` | Gauge | `worker_id` | count | Currently active workers |
| `crawler_checkpoint_age_seconds` | Gauge | — | seconds | Time since last frontier checkpoint |

### Derived Metrics (Recording Rules)

```yaml
# Crawl throughput (URLs/sec, 5-minute average)
- record: crawler:throughput_5m
  expr: rate(crawler_urls_fetched_total[5m])

# Error rate by category (percentage)
- record: crawler:error_rate_4xx
  expr: rate(crawler_error_total{error_category="4xx"}[5m]) / rate(crawler_urls_fetched_total[5m])

- record: crawler:error_rate_5xx
  expr: rate(crawler_error_total{error_category="5xx"}[5m]) / rate(crawler_urls_fetched_total[5m])

# Cost per URL (derived from egress and compute)
- record: crawler:cost_per_url
  expr: (crawler_fetch_bytes_total * 0.00000001 + crawler_fetch_duration_seconds * 0.00005) / crawler_urls_fetched_total

# Frontier drain rate (URLs consumed per second)
- record: crawler:frontier_drain_rate
  expr: -deriv(crawler_frontier_depth[10m])
```

### Error Category Labels

| error_category | HTTP Status / Condition | Action |
|---------------|------------------------|--------|
| `4xx` | 400-499 (client error) | Skip URL, do not retry (except 429) |
| `429` | Too Many Requests | Back off, reduce domain rate |
| `5xx` | 500-599 (server error) | Retry up to 3x with exponential backoff |
| `network` | DNS failure, timeout, connection reset | Retry up to 3x, then mark domain degraded |
| `compliance` | robots.txt block, opt-out signal | Skip URL, log compliance decision |
| `redirect_loop` | > 5 redirects in chain | Skip URL, log redirect chain |
| `content_error` | Parse failure, encoding error | Log for manual review |

## Grafana Dashboard Design

### Dashboard Layout (4 rows)

```
Row 1: Overview
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ URLs/sec     │ Total Fetched│ Frontier     │ Active       │
│ (gauge)      │ (counter)    │ Depth (gauge)│ Workers      │
└──────────────┴──────────────┴──────────────┴──────────────┘

Row 2: Performance
┌──────────────────────────┬──────────────────────────────┐
│ Fetch Latency (p50/p95)  │ Throughput by Domain (top 10)│
│ (heatmap)                │ (time series)                │
└──────────────────────────┴──────────────────────────────┘

Row 3: Errors & Compliance
┌──────────────────────────┬──────────────────────────────┐
│ Error Rate by Category   │ Compliance Blocks            │
│ (stacked area)           │ (by signal type, pie)        │
└──────────────────────────┴──────────────────────────────┘

Row 4: Cost & Health
┌──────────────────────────┬──────────────────────────────┐
│ Cost per URL (time series)│ Checkpoint Age (gauge)      │
│ (line, with budget line) │ (single stat, red > 5 min)  │
└──────────────────────────┴──────────────────────────────┘
```

## Alert Thresholds

### Critical Alerts (Page Immediately)

| Alert | Condition | Duration | Action |
|-------|-----------|----------|--------|
| Frontier exhaustion | `crawler_frontier_depth < 100` | 5 min | Crawl is about to stop — investigate seed injection or scope limits |
| Checkpoint stale | `crawler_checkpoint_age_seconds > 600` | 1 min | Frontier state may be lost on crash — investigate persistence layer |
| All workers down | `crawler_worker_active == 0` | 2 min | Complete crawl failure — check coordinator and infrastructure |
| Error rate spike | `crawler:error_rate_5xx > 0.10` | 5 min | 10%+ of fetches failing — check target site health or rate limiting |

### Warning Alerts (Notify)

| Alert | Condition | Duration | Action |
|-------|-----------|----------|--------|
| Throughput drop | `crawler:throughput_5m < 0.5 * avg_over_time(crawler:throughput_5m[1h])` | 15 min | Throughput dropped 50%+ — check politeness limits or proxy health |
| Frontier backlog | `crawler_frontier_depth > 10000000` | 30 min | 10M+ pending URLs — may need more workers or scope tightening |
| High 4xx rate | `crawler:error_rate_4xx > 0.05` | 10 min | 5%+ client errors — check URL canonicalization or stale URLs |
| Cost overshoot | `crawler:cost_per_url > budget_per_url * 1.5` | 1 hour | Cost 50%+ over budget — review proxy costs or egress optimization |
| Rate limit hits | `rate(crawler_error_total{error_category="429"}[5m]) > 0.5` | 5 min | Being rate-limited — reduce per-domain crawl rate |

## Cost-per-URL Modeling

### Component Breakdown

| Component | Cost Model | Typical Range |
|-----------|-----------|---------------|
| **Compute** | vCPU-seconds × $/vCPU-second | $0.00001-0.0001 per URL |
| **Network egress** | bytes × $/GB (cloud egress pricing) | $0.00005-0.001 per URL |
| **Proxy** | requests × $/request (or GB × $/GB) | $0.0001-0.01 per URL |
| **Storage** | bytes × $/GB-month (output storage) | $0.000001-0.00001 per URL |
| **Queue/Redis** | operations × $/operation | $0.000001-0.0001 per URL |

### Estimation Formula

```
cost_per_url = compute_cost + egress_cost + proxy_cost + storage_cost + queue_cost

Where:
  compute_cost = avg_fetch_duration_sec × vcpu_cost_per_sec
  egress_cost  = avg_page_size_bytes × egress_cost_per_byte
  proxy_cost   = proxy_cost_per_request (if using proxy)
  storage_cost = avg_output_size_bytes × storage_cost_per_byte_month × retention_months
  queue_cost   = 3 × queue_operation_cost (enqueue + dequeue + dedup check)

Example (Medium tier, cloud-hosted, residential proxy):
  compute:  0.5s × $0.00004/vCPU-s  = $0.00002
  egress:   200KB × $0.09/GB         = $0.000018
  proxy:    $0.005/request            = $0.005
  storage:  50KB × $0.023/GB-mo × 3  = $0.0000035
  queue:    3 × $0.0000004            = $0.0000012
  ────────────────────────────────────────────
  Total:                              ≈ $0.0051/URL

Without proxy:                        ≈ $0.000042/URL
```

### Budget Planning Table

| Scale Tier | URLs/day | Cost/URL (no proxy) | Cost/URL (proxy) | Daily Cost Range |
|-----------|---------|---------------------|------------------|-----------------|
| Small | 10K | $0.00004 | $0.005 | $0.40 - $50 |
| Medium | 500K | $0.00003 | $0.003 | $15 - $1,500 |
| Large | 10M | $0.00002 | $0.002 | $200 - $20,000 |
| Web-scale | 100M | $0.00001 | N/A (own infra) | $1,000+ |

## Graceful Shutdown Observability

### Shutdown Metrics

```
Shutdown sequence monitoring:
1. SIGTERM received → log timestamp
2. crawler_shutdown_initiated (gauge = 1)
3. crawler_inflight_requests (gauge, draining toward 0)
4. crawler_frontier_flush_status (0=pending, 1=complete)
5. crawler_kafka_offsets_committed (0=pending, 1=complete)
6. crawler_shutdown_complete (gauge = 1)
7. Process exit

Monitor: time between step 1 and step 6 should be < 30 seconds.
Alert if: crawler_inflight_requests > 0 after 30 seconds of shutdown.
```

### Resume Verification

```
After restart, verify:
1. crawler_frontier_depth matches pre-shutdown value (±1%)
2. No duplicate fetches in first 5 minutes (check dedup hit rate)
3. Throughput reaches 80% of pre-shutdown level within 10 minutes
4. All workers reconnect within 2 minutes
```

## SLO/SLI Alignment with Beacon

Spider's observability design produces the inputs that Beacon uses for alerting. The mapping:

| Spider Metric | Beacon SLI | SLO Target |
|--------------|-----------|------------|
| `crawler:throughput_5m` | Crawl throughput | ≥ configured URLs/sec |
| `1 - crawler:error_rate_5xx` | Fetch success rate | ≥ 99% |
| `max(content_age)` | Content freshness | < freshness SLO |
| `crawler_frontier_depth` | Frontier health | 100 < depth < 10M |
| `crawler:cost_per_url` | Cost efficiency | < budget per URL |
| `crawler_compliance_block_total{signal_type="pay-per-crawl-402"}` | Pay-Per-Crawl budget guard | within monthly cap |
| `concurrent_per_target` (cross-IP) | DDoS-equivalent prevention | ≤ 10 (post-Trilegangers default) |

Instrument with OpenTelemetry SDK (Traces / Metrics / Logs all Stable in early 2026; Profiling signal at RC). Use OTLP exporter to Tempo/Jaeger (traces), Prometheus/Mimir (metrics), Loki/SigNoz (logs).
