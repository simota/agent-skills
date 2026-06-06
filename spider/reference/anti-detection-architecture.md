# Anti-Detection Architecture

## Ethical Framework

**Anti-detection measures are infrastructure design decisions, not adversarial tools.** Before designing any anti-detection layer, document:

1. **Authorization:** Written permission, ToS compliance, or legal basis for crawling
2. **Purpose:** Legitimate use case (research, market analysis, compliance monitoring)
3. **Proportionality:** Measures are proportional to the access need
4. **Transparency:** User-Agent identifies the crawler and provides contact info

**When NOT to design anti-detection:**
- Public data with permissive robots.txt → standard crawling is sufficient
- Sitemap-only crawls → no detection risk
- API-based data collection → use the API
- No clear legal basis for access → do not proceed

## IP Rotation Strategies

### Proxy Pool Architecture

```
┌────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Worker     │────▶│  Proxy Gateway   │────▶│  Target     │
│  (Fetcher)  │     │  (IP Selection)  │     │  Website    │
└────────────┘     └──────┬───────────┘     └─────────────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
        ┌─────▼─────┐ ┌──▼──────┐ ┌──▼──────┐
        │Residential │ │Datacenter│ │Egress   │
        │Proxy Pool  │ │Proxy Pool│ │Gateway  │
        └───────────┘ └─────────┘ └─────────┘
```

### Proxy Type Comparison

| Type | Cost/GB | Block Rate | Speed | Best For |
|------|---------|------------|-------|----------|
| Datacenter | $0.5-2 | High (20-40%) | Fast | Low-protection targets, high volume |
| Residential | $5-15 | Low (2-5%) | Medium | High-protection targets, critical data |
| Mobile | $15-30 | Very low (< 1%) | Variable | Maximum stealth, limited volume |
| ISP (static residential) | $3-8 | Low (5-10%) | Fast | Session persistence needed |
| Egress gateway rotation | Infra cost | Medium | Fast | Own infrastructure, predictable cost |

### IP Rotation Strategies

| Strategy | Implementation | Suitable For |
|----------|---------------|-------------|
| Per-request rotation | New IP every request | High-volume, no session |
| Per-session rotation | New IP every N requests or T minutes | Session-based crawling |
| Per-domain rotation | Sticky IP per domain, rotate on block | Domain affinity crawling |
| Geo-targeted | Match proxy location to target locale | Region-specific content |
| Reputation-based | Track IP success rate, retire low performers | Long-running crawls |

## User-Agent Management

### Pool Design

```
Requirements:
- 50-200 realistic User-Agent strings
- Weighted by actual browser market share
- Updated quarterly (browser versions change)
- Rotation: per-session (not per-request — consistent UA within a session)

Example distribution (Q2 2026 approximation, StatCounter desktop share):
  Chrome 130-136 (Windows 10/11): 45%
  Chrome 130-136 (macOS): 15%
  Safari 18.x (macOS): 12%
  Firefox 130-136 (Windows/Linux): 9%
  Edge 130-136 (Windows): 8%
  Chrome Mobile (Android): 8%
  Safari Mobile (iOS): 3%

Anti-pattern: DO NOT use bot-like UAs (e.g., "Python-urllib/3.12")
Best practice: Include realistic Accept, Accept-Language, Accept-Encoding, Sec-CH-UA-* client-hint headers consistent with the chosen UA. Cloudflare Bot Management cross-checks UA vs JA4 vs client hints; mismatch is flagged.
```

## TLS Fingerprint Diversification

### JA3/JA4 Fingerprinting (2026 status)

```
What it detects:
  TLS Client Hello → cipher suites, extensions, supported groups, signature algorithms,
  ALPN, GREASE values, HTTP/2 SETTINGS frame ordering.
  As of 2026 JA4/JA4+ (FoxIO) is baked into every major bot-protection vendor
  (Cloudflare Bot Management, Akamai Bot Manager, DataDome, PerimeterX/HUMAN);
  JA3 is considered legacy because TLS 1.3 extension permutation made it unstable.
  JA4 sorts extensions alphabetically before hashing → resistant to randomization.

  Each TLS library has a distinctive fingerprint:
  - Python requests (urllib3): distinct JA4 hash
  - Go net/http: distinct JA4 hash
  - Chrome 130+ browser: distinct JA4 hash with GREASE
  - curl 8.x baseline: distinct JA4 hash (NOT a browser)

Mitigation strategies:
1. curl-impersonate / curl_cffi (Python binding): mimics Chrome/Firefox/Edge/Safari TLS+HTTP/2 fingerprints; default tool in 2026.
2. Playwright / Puppeteer / undetected-chromedriver: real browser TLS stack, also handles JS fingerprinting (canvas/WebGL).
3. utls (Go): ClientHelloID presets for Chrome/Firefox.
4. Custom cipher suite ordering: Match target browser profile.

Decision: If target uses JA4/JA4+ fingerprinting (Cloudflare, Akamai, DataDome),
use curl-impersonate/curl_cffi or browser-based fetching. Pure curl/requests/httpx
will be flagged. curl-impersonate does NOT handle JS-layer fingerprinting
(canvas, WebGL, font enumeration, navigator.webdriver) — that requires Playwright/stealth.
```

## Timing Models

### Inter-Request Delay Design

| Model | Formula | Realism | Complexity |
|-------|---------|---------|------------|
| Fixed delay | delay = constant | Poor (detectable) | Low |
| Uniform random | delay = uniform(min, max) | Fair | Low |
| Gaussian jitter | delay = max(floor, N(μ, σ)) where μ = crawl_delay, σ = 0.3μ | Good | Medium |
| Pareto distribution | delay = pareto(α=1.5, x_m=crawl_delay) | Excellent (human-like) | Medium |
| Session-aware | Short bursts (2-5 pages) + longer pauses (10-30s) | Excellent | High |

**Recommended default:** Gaussian jitter with μ = Crawl-Delay (or 1s), σ = 30% of μ, floor = 0.5s.

### Behavioral Pattern Avoidance

```
Anti-patterns (detectable by sophisticated systems):
✗ Alphabetical URL crawling within a domain
✗ Perfectly sequential page numbers
✗ Constant request interval
✗ No referrer headers
✗ Unrealistic session depth (1000 pages without pause)

Best practices:
✓ Randomize URL order within domain queue
✓ Vary session depth (5-50 pages per "session")
✓ Include realistic referrer chains
✓ Simulate "reading time" (longer delay for content pages)
✓ Occasionally re-visit previously seen pages (human browsing pattern)
```

## CAPTCHA Escalation Path

```
CAPTCHA encounter decision flow:

1. CAPTCHA detected?
   ├── No → Continue crawling
   └── Yes → Classify type
        ├── Simple (image text) → Flag for review, DO NOT auto-solve
        ├── reCAPTCHA v2/v3 → Pause domain, rotate proxy, retry after cooldown
        ├── hCaptcha → Pause domain, reduce crawl rate, retry in 1 hour
        └── Custom/unknown → Block domain, log, escalate to human

IMPORTANT: Never design automated CAPTCHA solving as a primary path.
Acceptable responses:
- Reduce crawl rate for that domain
- Rotate to different proxy
- Pause and retry after cooldown period
- Escalate to human operator for decision
- Accept data loss for that domain
```

## Cloudflare-Fronted Sites (2026 default block)

Since 2025-07-01 Cloudflare flips new sites to "Block AI crawlers by default" and offers Pay-Per-Crawl (HTTP 402 Payment Required with `crawler-price` / `crawler-exact-price` / `crawler-charged` headers). About 20% of the public web is fronted by Cloudflare. Architecture implications:

- Classify each target host's edge (Cloudflare / Akamai / Fastly / origin) at DISCOVER. Cloudflare-edged targets that have not opted into your crawler will return 403 even with perfect TLS impersonation.
- Cloudflare AI Labyrinth (2025-03) serves an infinite maze of AI-generated decoy pages to crawlers that ignore robots.txt. Detect via abnormally high in-link counts to never-before-seen URLs from a single domain → quarantine and exclude.
- Verified Bots program: register your crawler with Cloudflare (`bot-management/verified-bots`) for legitimate access; unverified bots that mimic Googlebot UA are blocked.
- For AI-training corpus crawls: classify target hosting and treat Cloudflare/AI-Audit fronted domains as a separate licensable tier (negotiate via Pay-Per-Crawl marketplace or skip).

## Detection Risk Assessment

| Indicator | Risk Level | Mitigation |
|-----------|-----------|------------|
| High request rate from single IP | High | IP rotation, rate limiting |
| Bot-like User-Agent | High | Realistic UA pool |
| Missing browser headers | Medium | Full header simulation |
| TLS fingerprint mismatch | Medium | curl-impersonate / browser |
| Sequential URL patterns | Medium | Randomized crawl order |
| No JavaScript execution | Low-Medium | Browser-based fetching for JS-heavy sites |
| Unusual access times | Low | Schedule during business hours |
| Missing cookie handling | Low | Session-aware cookie jar |
