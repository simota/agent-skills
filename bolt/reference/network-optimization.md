# Network Delivery Optimization Reference

Purpose: Design and tune the client/server delivery layer so bytes already on-disk arrive sooner, in fewer round trips, and with maximum cache reuse. The subcommand produces header policies, resource-hint placements, Service Worker strategies, and CDN cache-control rules — measured against TTFB, LCP, and CDN hit ratio.

## Scope Boundary

- **Bolt `network`** (this Recipe): the *policy and client/server signals* that govern delivery — HTTP/2 / HTTP/3 enablement on the origin, Early Hints (103), `Link:` preload headers, `<link rel="preload|prefetch|preconnect|dns-prefetch">`, Service Worker caching strategy, CDN `Cache-Control` / `s-maxage` / `stale-while-revalidate`, Brotli tuning.
- **Scaffold**: *provisions* the CDN, edge, and origin (Terraform/OpenTofu/CloudFormation/Pulumi). Creates the distribution, WAF, origin access.
- **Gear**: *operates* the CDN and build pipeline — dependency versions, invalidation jobs, CI wiring, health checks, runtime observability.
- **Bolt `bundle`**: changes the bytes themselves. `network` never changes what ships, only how it travels.
- **Bolt `cache`**: application-layer cache (Redis / LRU / HTTP response cache at origin). `network` is the edge-and-client half; `cache` is the origin half. They compose.

If the fix is "add a `preload` header" → `network`. If it's "migrate S3 behind a new CloudFront" → Scaffold. If it's "bump nginx to enable HTTP/3" → Gear.

## Workflow

```
PROFILE   →  run Lighthouse + WebPageTest with HAR export
          →  capture: TTFB, LCP, per-asset protocol (h1/h2/h3), Brotli vs gzip
          →  inspect response headers on critical resources
              (cache-control, vary, link, alt-svc, content-encoding)
          →  check CDN hit ratio and per-asset TTL

SELECT    →  pick ONE of: Early Hints · resource hints · SW cache · CDN policy · Brotli
          →  target the critical-request chain (LCP asset → first paint)
          →  reject hints that don't correspond to measured critical resources

OPTIMIZE  →  apply the single policy change
          →  emit headers from origin or edge, not <head> when both possible
              (earlier arrival + cacheable by intermediaries)
          →  for SW: never cache HTML as cache-first without a kill-switch

VERIFY    →  re-run WebPageTest; compare waterfall
          →  confirm: no double-download, no hint for unused asset
          →  check CDN hit ratio delta (should rise, not fall)
          →  LCP / TTFB delta recorded

PRESENT   →  Before/After: TTFB, LCP, hit ratio, bytes over wire
          →  risks: CORS / CORB / Vary fragmentation
          →  handoff to Gear if config change touches CDN runtime
```

## Protocol & Compression Quick Reference

| Layer | Default | When to change |
|-------|---------|----------------|
| HTTP/2 | On at modern edges | Verify; still not universal on origin |
| HTTP/3 / QUIC | Opt-in on most CDNs | Enable when mobile / lossy network is a large audience — measurable RTT win on 0-RTT resumption |
| Brotli | Level 4 dynamic / 11 static | Raise static level; never raise dynamic past 6 (CPU cost) |
| gzip | Fallback only | Keep for ancient clients |
| Early Hints (103) | Opt-in | Preload critical CSS/JS before origin finishes HTML |

## Resource Hint Placement

| Hint | Use for | Don't use for |
|------|---------|----------------|
| `preload` | LCP image, hero font, critical CSS (same-origin) | Anything not used in the first second |
| `prefetch` | Likely-next navigation JS chunk | Above-the-fold resources |
| `preconnect` | Cross-origin critical domains (≤4) | Every third-party |
| `dns-prefetch` | Many cross-origin domains | Same-origin resources |
| `modulepreload` | Static ESM chunks known at build | Dynamically-decided code paths |

Emit via `Link:` response header where possible — parseable before `<head>` is read and reusable across intermediaries.

## Service Worker Cache Strategy

| Asset class | Strategy | TTL | Rationale |
|-------------|----------|-----|-----------|
| Hashed JS/CSS | cache-first | 1y | Immutable URL |
| HTML shell | network-first w/ timeout → cache fallback | short | Avoid stuck-on-old-version |
| API GET | stale-while-revalidate | minutes | Instant paint, eventual consistency |
| Images | cache-first w/ LRU size cap | 30d | Bounded device storage |
| Auth-sensitive | network-only | — | Never cache |

Ship a kill-switch: SW reads a `version.json` on activate; if mismatched, wipes and reloads.

## CDN Cache-Control Patterns

- Immutable hashed assets: `public, max-age=31536000, immutable`
- HTML: `public, max-age=0, s-maxage=60, stale-while-revalidate=300` (edge holds briefly; origin drives truth)
- Authenticated JSON: `private, no-store` (never let edge cache)
- Shared catalog JSON: `public, max-age=0, s-maxage=300, stale-while-revalidate=3600`

Always pair with `Vary: Accept-Encoding` (and `Accept` for content-negotiated). Audit `Vary` values — each unique combination forks the cache key.

## Anti-Patterns

- `preload` every JS chunk — blows main-thread budget and hurts LCP.
- `preconnect` to 10+ third parties — each consumes a connection slot.
- SW caching HTML with cache-first and no version check — users stuck on stale app.
- Brotli level 11 on dynamic responses — origin CPU climbs faster than bytes saved.
- Setting `Cache-Control: no-cache` when you meant `no-store` (or vice versa).
- Serving identical resource under two URLs (e.g., with and without trailing slash) — doubles cache storage, halves hit ratio.

## Handoff

- **→ Scaffold**: new CDN/edge distribution, origin change, WAF rules.
- **→ Gear**: runtime operations — invalidation jobs, header rollout via infra config, observability on hit ratio.
- **→ Bolt `bundle`**: if the asset is simply too large for any hint to help.
- **→ Bolt `cache`**: origin response caching (Redis, in-memory) to shore up `s-maxage` misses.
- **→ Sentinel**: review of CSP / CORS / CORB implications of new cross-origin hints.
