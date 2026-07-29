# Core Web Vitals — SEO/Ranking Context

For remediation techniques and code (LCP hero image/font fixes, INP long-task breakup, LoAF diagnostics, CLS layout-shift fixes, RUM setup), see **`bolt/reference/core-web-vitals.md`** — Bolt owns the technical fix library. This file covers only what's specific to search ranking and SEO measurement.

## Why Growth cares

Core Web Vitals are a confirmed Google ranking signal (part of the Page Experience system) and — separately — a direct UX/conversion lever: slow, jumpy pages lose organic sessions before ranking is even a factor. Growth's job is to catch CWV failures that are invisible to SEO tooling and translate a fix into ranking/traffic impact, not to re-derive the remediation itself.

> **2026 baseline (CrUX):** Only ~48% of mobile origins pass all three Core Web Vitals; ~43% of sites still fail the INP < 200ms threshold at p75, making INP the most commonly failed CWV. LCP mobile pass rate sits around 52–62%; CLS has the highest pass rate. INP replaced FID as a Core Web Vital on 2024-03-12. [Source: corewebvitals.io 2026 guide, https://www.corewebvitals.io/core-web-vitals; web.dev/articles/inp]

## Thresholds (ranking-relevant, p75)

| Metric | Good | Needs Improvement | Poor |
|--------|------|--------------------|------|
| LCP | ≤ 2.5s | 2.5–4.0s | > 4.0s |
| INP | ≤ 200ms | 200–500ms | > 500ms |
| CLS | ≤ 0.1 | 0.1–0.25 | > 0.25 |

Google evaluates these at the **75th percentile of real-user visits (CrUX)**, not lab scores — a page that passes Lighthouse locally can still fail the ranking signal if p75 real-user traffic (older devices, poor networks, cold cache) is worse than what you tested on.

## The Growth-specific measurement gap

**Lighthouse-passing + CrUX-failing is the most common Growth blind spot.** Lighthouse runs a single synthetic trace on a fast machine; CrUX aggregates real Chrome user data at p75. A page can look fine in a local audit while still failing the ranking threshold for the segment of visitors Google actually scores. Always cross-check:

1. **PageSpeed Insights** — shows both the Lighthouse lab score and the CrUX field data side by side; treat the CrUX numbers as the one that affects ranking.
2. **Google Search Console → Core Web Vitals report** — shows URL groups failing at p75 across real traffic, segmented by device.
3. **`web-vitals` RUM in production** (see `bolt/reference/core-web-vitals.md` § Web Vitals Monitoring) — closes the loop between what you shipped and what real users experienced, before waiting weeks for CrUX to update.

## Verification checklist (VERIFY step)

- [ ] PageSpeed Insights: CrUX field data passes all three metrics at p75 (not just the lab score)
- [ ] Search Console Core Web Vitals report shows no "Poor" URL groups for the affected templates
- [ ] Mobile checked separately from desktop — CrUX and ranking weight mobile more heavily
- [ ] If a fix was shipped, confirm via RUM within days rather than waiting on the ~28-day CrUX rolling window
