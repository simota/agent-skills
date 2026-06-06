# Core Web Vitals Deep Optimization

## Purpose

Diagnose and fix Core Web Vitals (CWV) failures at the 75th-percentile real-user level. Generic Lighthouse advice does not move RUM percentiles; targeted root-cause fixes do. This reference covers the diagnostic chain and the targeted fix pattern catalog.

## Scope Boundary

- IN scope: LCP / INP / CLS root cause analysis, RUM-vs-lab interpretation, targeted fix patterns, third-party impact, Soft Navigations, INP attribution, AI-bot rendering parity.
- OUT of scope: general bundle optimization (delegate to `bolt`), backend performance (`bolt` server side), schema / SEO meta (`seo`), site audit (`audit`), CRO (`cro`).

## Core Concepts

### The CWV Triad and 75th-Percentile Reality

Google measures CWV at p75 across real users (CrUX), not lab tools. Lighthouse passes mean nothing if RUM fails. Always treat CrUX / RUM as authoritative.

| Metric | Threshold (Good at p75) | Most Common Failure |
|--------|-------------------------|---------------------|
| LCP | ≤ 2.5 s | Slow LCP element discovery + render delay |
| INP | < 200 ms | Long tasks blocking main thread on interaction |
| CLS | < 0.1 | Late-loading layout shifts (ads, fonts, images) |
| (Optional) VSI | Lower is better | Session-long visual instability |

INP fails on ~43% of sites at p75 — by far the most common CWV blocker in 2026. Prioritize INP diagnosis first when triaging.

### LCP Sub-Phases (Web.dev framework)

LCP = TTFB + Resource Load Delay + Resource Load Duration + Render Delay.

| Sub-phase | Diagnosis | Fix Pattern |
|-----------|-----------|-------------|
| TTFB | Backend slow | Server-side rendering on edge, caching, CDN |
| Resource Load Delay | LCP image discovered late | `fetchpriority="high"`, preload, `<link rel="preconnect">` |
| Resource Load Duration | LCP image too large | AVIF / WebP, responsive `srcset`, properly sized |
| Render Delay | JS / CSS blocks render | Critical CSS inline, defer non-critical JS, reduce hydration |

Use `PerformanceObserver` + `largest-contentful-paint` entry's `loadTime`, `renderTime`, `startTime` to attribute each phase. Generic "make site faster" never beats targeted phase fixes.

### INP Attribution

INP = the slowest interaction's full latency: `processingStart - eventTime` + `processingEnd - processingStart` + `presentationTime - processingEnd`.

| Sub-phase | Diagnosis | Fix Pattern |
|-----------|-----------|-------------|
| Input Delay | Main thread blocked when input arrived | Yield to main thread (`scheduler.yield()`, `setTimeout(0)`); break long tasks |
| Processing Time | Event handler too slow | Move work off main thread (Web Workers); memoize; virtualize lists |
| Presentation Delay | Layout / paint after handler | Use `content-visibility: auto`; isolate paint with `contain` |

Tooling (2026-05): use **Long Animation Frames (LoAF) API** (stable since Chrome 123, 2024-03) as the primary INP root-cause tool — each LoAF entry exposes the offending `scripts[]` array with `sourceURL`, `sourceFunctionName`, `invokerType`, and `forcedStyleAndLayoutDuration`. Web Vitals JS **v5.x** (`web-vitals/attribution`) auto-attaches `attribution.longAnimationFrameEntries` to every INP report — this is the recommended production pathway. The older `longtask` entry type is now legacy for INP diagnosis. [Source: Chrome for Developers — Long Animation Frames API, https://developer.chrome.com/docs/web-platform/long-animation-frames]

### CLS Root Causes

| Source | Frequency | Fix |
|--------|-----------|-----|
| Images without dimensions | Very high | `width` + `height` attributes; CSS `aspect-ratio` |
| Web fonts FOIT/FOUT | High | `font-display: optional`, preload, system stack fallback with `size-adjust` |
| Late-injected ads / embeds | High | Reserve space with min-height; avoid above-the-fold injection |
| Dynamic content (banners, GDPR consent) | Medium | Reserve space; animate via `transform`, not layout |
| Single-page app navigation | Medium | Use Soft Navigations API; restore scroll predictably |
| Third-party widgets (chat, social) | Medium | Load below the fold; reserve container |

CLS is cumulative within a session, not just initial load. Late shifts on scroll count.

### Lab vs RUM Reality

| Tool | What It Measures | Trust For |
|------|------------------|-----------|
| Lighthouse | Single synthetic run | Repro / regression detection |
| PageSpeed Insights (Field Data) | CrUX 28-day p75 | Authoritative — this is what Google uses |
| Web Vitals JS library | Per-session real-user | Production attribution |
| Chrome DevTools Performance | Single trace | Root-cause analysis |
| WebPageTest | Multi-run synthetic | Geographic / network simulation |

Lighthouse passing + CrUX failing means: synthetic conditions don't match your users' devices, networks, or interaction patterns. The fix lives in the gap, not in the lighter score.

### Third-Party Impact

| Third Party | Typical Impact |
|-------------|----------------|
| GTM / GA4 / Adobe Analytics | INP +30–80 ms; LCP +0–200 ms via blocking |
| Customer chat widgets (Intercom, Drift) | INP +50–200 ms; CLS if late |
| Ad networks | LCP heavy; INP heavy; CLS heavy |
| Cookie banners | CLS heavy (above the fold); INP if blocking |
| Embedded video (YouTube iframe) | LCP heavy if above the fold |

Audit with `requestIdleCallback` deferral, async loading, facade pattern (load static placeholder, swap on interaction), and `<link rel="preconnect">` for unavoidable connections.

### Targeted Fix Patterns

#### LCP

- **Image-LCP**: `fetchpriority="high"` + `loading="eager"` + `<link rel="preload" as="image">` + AVIF / WebP + correct `srcset`/`sizes`. Match LCP element to one preloaded resource only.
- **Text-LCP**: critical CSS inline, font preload with `crossorigin`, `font-display: swap` plus a system fallback sized via `ascent-override` and `size-adjust`.
- **Server-side**: edge SSR (Cloudflare Workers, Vercel Edge), HTML streaming, smaller above-the-fold payload.
- **Render-blocking removal**: defer non-critical JS, async or defer external CSS via `media` attribute swap.

#### INP

- **Long tasks**: split tasks > 50 ms. Use `scheduler.yield()` (Chrome 129+ stable, Firefox since 2025-08; **Safari has not implemented** — polyfill with `setTimeout(0)`). Diagnose with LoAF API, not the legacy `longtask` entry type.
- **Hydration**: progressive / partial / island hydration (Astro, Qwik, Marko, modern Next.js). Avoid full-page hydration on content sites.
- **Re-render storms**: in React, memoize, split state, use `useDeferredValue` and `useTransition`.
- **Heavy main-thread work**: move to Web Workers (`postMessage` JSON or `Comlink`).
- **Event handler bloat**: throttle / debounce; defer analytics dispatch.

#### CLS

- **Images**: always set dimensions; `aspect-ratio` CSS for responsive.
- **Fonts**: pair font-face declaration with a metric-matched fallback using `size-adjust`, `ascent-override`, `descent-override`, `line-gap-override`.
- **Ads**: reserve max expected ad slot height; avoid above-the-fold ad load.
- **SPAs**: Soft Navigations API (`PerformanceObserver` `navigation` entries) + scroll restoration policy.

### AI-Bot Rendering Parity

GEO citation depends on AI bots rendering the same primary content as users. Pitfalls:

| Issue | Fix |
|-------|-----|
| JS-only content + AI bot doesn't execute JS | Server-side render or static-prerender LCP content |
| Lazy-loaded primary content blocked by IntersectionObserver | Render LCP eagerly; lazy-load below the fold |
| Cookie / consent gate on first paint | Render structured data + main content above the gate |
| User-agent based content swap | Avoid; or serve identical primary content to all UAs |

Verify with `curl` (no JS) and Chrome with JS disabled — if your LCP / answer paragraph isn't there, AI bots likely won't see it either.

## Workflow

1. **Pull RUM baseline** — CrUX p75 LCP / INP / CLS for the URL or origin (PageSpeed Insights API).
2. **Identify the failing metric** — pick the worst.
3. **Attribute** — Web Vitals attribution build to find the worst element / interaction / layout shift in production sessions.
4. **Reproduce** — Chrome DevTools Performance trace on a representative device class (Slow 4G, Moto G4 CPU 4× throttle).
5. **Diagnose sub-phase** — for LCP: which sub-phase dominates; for INP: input delay vs processing vs presentation; for CLS: which element shifts.
6. **Apply targeted fix pattern** — from the catalogs above.
7. **Verify in lab** — Lighthouse + DevTools shows the sub-phase reduced.
8. **Wait for RUM** — CrUX updates on a 28-day rolling window. Real validation takes 2–4 weeks after rollout.
9. **Confirm AI-bot parity** — `curl` and JS-disabled Chrome render the LCP element.
10. **Iterate** — when one metric clears, pick the next failing metric.

## Output Template

```yaml
cwv_diagnosis:
  url: "/blog/why-rag"
  baseline_p75:
    lcp_ms: 3850       # FAIL (>2500)
    inp_ms: 280        # FAIL (>200)
    cls: 0.04          # PASS
  failing_metric: INP  # worst margin → pick this first
  attribution:
    inp:
      worst_interaction: "click on .site-search-input"
      sub_phase_dominant: processing_time
      processing_ms: 240
      offending_function: "fuzzysearch.score()"
  fix_plan:
    - pattern: "Move fuzzysearch to Web Worker via Comlink"
      effort: M
      expected_inp_reduction_ms: 180
    - pattern: "Add scheduler.yield() between batches in result-list render"
      effort: S
      expected_inp_reduction_ms: 60
  ai_bot_parity:
    js_disabled_render_ok: yes
    curl_render_ok: yes
  validation:
    lab_after_fix:
      inp_ms_synthetic: 110
    rum_check_date: 2026-05-23  # 28 days post-rollout
```

## Anti-Patterns

- Optimizing Lighthouse score, ignoring CrUX p75 — Google ranks on CrUX.
- Generic "improve performance" backlog — no targeted fix lands.
- Fixing INP without attribution — randomly memoizing components rarely moves p75.
- Chasing INP on desktop while mobile p75 fails — segment by device class.
- Lazy-loading the LCP image — direct CWV regression.
- Adding `loading="lazy"` to all images blindly — LCP image must be eager.
- `font-display: block` combined with no fallback — guaranteed CLS or LCP miss.
- Trusting a single Lighthouse run — variance is 10–30% on under-throttled environments.
- Reserving zero space for ads / chat widgets — predictable CLS.
- Ignoring Soft Navigations on SPAs — SPA route changes count toward CWV in 2025+.
- Optimizing without checking AI-bot rendering — passing CWV but invisible to AI search.

## Deliverable Contract

A CWV optimization deliverable is complete when:

- RUM baseline at p75 captured (PageSpeed Insights or Web Vitals JS).
- Failing metric identified by largest threshold breach.
- Attribution traces the metric to a specific element / interaction / shift.
- Sub-phase diagnosis present (which part of LCP / INP).
- Targeted fix patterns chosen from the catalog with effort + expected delta.
- AI-bot rendering parity verified (no-JS render check).
- Lab validation post-fix.
- RUM validation date scheduled 28 days post-rollout.

## References

- Google Web.dev, *Core Web Vitals* (2024 update) — official thresholds.
- Annie Sullivan & Rick Viscomi, *Optimize INP* (web.dev, 2024).
- Philip Walton, *web-vitals* JS library (Google) — RUM measurement and attribution.
- Barry Pollard, *Optimizing INP* and *LCP Sub-parts* analyses.
- Patrick Meenan, *WebPageTest Cookbook* — synthetic measurement methodology.
- Addy Osmani, *Speed at Scale* (HTTP Archive).
- Google CrUX Dashboard — origin-level RUM data.
- W3C Web Performance Working Group — Soft Navigations API specification.
- Houssein Djirdeh, Aurora team — partial / island hydration strategies.
