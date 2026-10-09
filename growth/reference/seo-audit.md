# Full-Site SEO Audit

## Purpose

Diagnose technical and structural issues that block traffic regardless of content quality. A page-level meta fix wastes effort if the site is uncrawlable, mis-indexed, or topologically incoherent. The audit produces a prioritized backlog, not a 200-row spreadsheet of findings.

> **2026 audit pressure points:**
> - **Google March 2026 Core Update** rolled out 2026-03-27 alongside a paired Spam Update (fastest spam update ever, completed in <20 hours). Both target AI-generated content lacking human editorial oversight via an upgraded SpamBrain (analysts attribute Gemini 4.0 Semantic Filter signals). 73% of top YMYL pages now display detailed author credentials, up from 58% pre-update. Audits must include AI-content authorship and E-E-A-T credential coverage. [Source: Search Engine Land / PPC.land coverage of March 2026 update, https://ppc.land/googles-march-2026-spam-update-is-live-what-changed-and-why-it-matters/]
> - **FAQ rich results retired** (Jun 2026 — Rich Results Test support removed, Aug 2026 — Search Console API). FAQPage schema still parses for AI Overviews / ChatGPT / Perplexity citation. Audit existing FAQ markup for **schema-content consistency**, not rich-result eligibility. [Source: Search Engine Land, https://searchengineland.com/google-to-no-longer-support-faq-rich-results-476957]
> - **Schema.org v30.0** released 2026-03-19 (823 types), expanded credential / e-commerce / supply-chain schema for AI verification. [Source: https://schema.org/docs/releases.html]

## Scope Boundary

- IN scope: crawlability, indexability, site architecture, internal linking, content gap, log-file analysis (Googlebot + AI bots), schema coverage, hreflang, canonical hygiene, redirect chains.
- OUT of scope: per-page meta authoring (`seo`), CRO experiments (`cro`), Core Web Vitals deep-dive (`vitals`), keyword universe construction (`keyword`), GEO content quality (`geo`).

## Core Concepts

### The 5-Layer Audit Stack

Audit in this order. Lower layers gate upper layers; do not optimize content on a site Google cannot crawl.

| Layer | Question | Tools |
|-------|----------|-------|
| L1 Crawlability | Can bots fetch your URLs? | robots.txt, server logs, Screaming Frog, Sitebulb |
| L2 Indexability | Does Google keep them in the index? | GSC Coverage report, `site:` operator, URL Inspection |
| L3 Architecture | How do pages connect? | Internal linking map, click depth, orphan analysis |
| L4 Content | Do your pages match intent? | Content gap vs competitors, thin-content threshold, cannibalization |
| L5 Schema / GEO | Are you machine-readable? | Rich Results Test, Schema.org validator, AI bot access |

### L1 Crawlability Checks

| Check | Pass Criterion |
|-------|----------------|
| robots.txt fetchable | 200 OK at `/robots.txt` |
| Sitemap reachable | XML sitemap returns 200; URLs accessible |
| No accidental disallow | `Disallow: /` not in production |
| AI bot policy explicit | GPTBot / ClaudeBot / PerplexityBot / OAI-SearchBot / Claude-SearchBot rules documented |
| Crawl budget healthy | Googlebot fetches > 80% of indexable URLs per 30 days |
| Render path | JS-rendered content reachable (test with `curl` + with rendering) |
| Redirect chains | All chains ≤ 1 hop |
| Soft 404 | Empty / boilerplate pages return 404, not 200 |

Important AI-bot distinction: training bots (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended) and search/retrieval bots (OAI-SearchBot, Claude-SearchBot, ChatGPT-User, Claude-User, PerplexityBot, Perplexity-User) require different policy decisions. Blocking training bots does not affect AI-search citation. Blocking search/retrieval bots removes you from AI-search results.

Anthropic publishes a **four-bot taxonomy** (confirmed 2026-05): `ClaudeBot` (training), `Claude-SearchBot` (search index/retrieval), `Claude-User` (user-initiated fetch from Claude.ai), `claude-code` (Claude Code CLI WebFetch). Control each independently. [Source: ALM Corp, https://almcorp.com/blog/anthropic-claude-bots-robots-txt-strategy/]

**Do not rely on llms.txt**: SE Ranking found ~10.13% adoption across 300k domains but GPTBot, ClaudeBot, OAI-SearchBot, Claude-SearchBot, PerplexityBot, Google-Extended overwhelmingly skip `/llms.txt` and crawl HTML directly. No major AI vendor has publicly committed to honoring llms.txt as of Q1 2026. [Source: AEO Press, https://www.aeo.press/ai/the-state-of-llms-txt-in-2026]

### L2 Indexability Checks

| Check | Pass Criterion |
|-------|----------------|
| Canonical tags | Each URL points to its preferred canonical; no self-canonical loops; no canonical to redirected URL |
| `noindex` audit | `noindex` only on pages that should be excluded |
| Duplicate content | No paginated / parameterized URLs indexed; UTM-stripping canonical present |
| HTTPS only | All HTTP redirects 301 to HTTPS |
| Mobile + desktop parity | Mobile has same content + structured data |
| Hreflang consistency | Bidirectional `x-default` + per-locale, no orphan locales |
| Indexed-but-not-linked | GSC reports zero "Crawled - currently not indexed" growth |
| Sitemap-vs-indexed delta | < 10% of submitted URLs are unindexed |

### L3 Architecture Checks

| Check | Pass Criterion |
|-------|----------------|
| Click depth | All commercially important pages reachable in ≤ 3 clicks from home |
| Orphan pages | Zero pages with no internal incoming links |
| Internal linking density | High-priority pages have ≥ 10 internal links from diverse contexts |
| Anchor text variety | Money pages have 5+ distinct natural-language anchors |
| Hub & spoke topology | Cluster pillars link to all cluster children; children cross-link |
| Breadcrumbs | Present on all non-root pages with `BreadcrumbList` schema |
| Pagination | `rel=prev/next` removed; canonical to view-all where appropriate |
| Faceted navigation | Parameterized URLs are crawl-controlled (robots, canonical, or `noindex,follow`) |

### L4 Content Checks

| Check | Pass Criterion |
|-------|----------------|
| Thin content | No indexed page under 300 words unless intentionally a hub |
| Cannibalization | No two indexed pages target the same primary query |
| Content freshness | Date stamps + actual content updates on time-sensitive pages |
| Topical authority | Pillar + cluster topology covers ≥ 80% of cluster queries |
| Content gap | Top 10 competitor SERPs identify ≥ 50 missing topics |
| E-E-A-T signals | Author bios, credentials, dates, sources on every YMYL page |
| Image alt text | 100% of content images have descriptive alt text (≤ 125 chars) |

### L5 Schema and GEO Checks

| Check | Pass Criterion |
|-------|----------------|
| Schema coverage | Organization + WebSite + BreadcrumbList sitewide |
| Page-type schema | Article / Product / LocalBusiness / FAQ / HowTo where applicable |
| Specific over generic | BlogPosting > Article; LocalBusiness > Organization |
| Triple-stack on GEO pages | Article + ItemList + FAQPage on key cite-target pages |
| Schema-content consistency | Every JSON-LD claim is visible on the page |
| Validation | 100% pass on Google Rich Results Test |
| AI Overview eligibility | Direct-answer first 200 words; 120–180 words per H2 section |
| Inline citations | 3–5 authoritative sources cited per GEO-target article |
| AI bot access verified | Server logs show OAI-SearchBot / Claude-SearchBot / PerplexityBot fetches |

### Log-File Analysis

Server logs are the only ground truth for crawler behavior. Look for:

| Pattern | Diagnosis |
|---------|-----------|
| Googlebot 4xx rate > 5% | Broken links or aggressive blocking |
| Googlebot 5xx rate > 1% | Server overload during crawl windows |
| Googlebot fetches dominated by low-value URLs (filters, search results) | Crawl budget waste; tighten robots/canonical |
| AI bots in logs but zero AI citations | Crawl works, content fails — content / schema problem |
| AI bots not in logs | Blocked by robots, CDN, WAF, or JS-only rendering |
| 304 ratio for sitemap URLs > 90% | Stale content; not bad but signals refresh opportunity |

Tools: GoAccess, Splunk, Screaming Frog Log File Analyzer, Botify, Lumar.

### Audit Output: The 30-Item Backlog

Resist the 200-row spreadsheet. Audits fail by overwhelming the implementer. Cap output at 30 prioritized items grouped by layer. Each item:

- Title (one line)
- Layer (L1–L5)
- Severity (Blocker / High / Medium / Low)
- Affected URL count
- Effort estimate (S / M / L)
- Recommended fix (concrete, not "improve X")
- Verification step

## Workflow

1. **Snapshot baseline** — GSC export (last 90 days), `site:` count, top-100 page log-file extract.
2. **Run L1** — robots, sitemap, redirect chains, AI bot policy.
3. **Run L2** — canonical, noindex, hreflang, duplicate detection.
4. **Run L3** — crawl with Screaming Frog or Sitebulb; map click depth and orphans.
5. **Run L4** — content gap vs top-3 competitors per cluster; thin-content sweep.
6. **Run L5** — schema coverage, GEO direct-answer check, AI bot log access.
7. **Triage** — group findings, drop noise, prioritize by traffic-at-risk × effort.
8. **Cap to 30 items** — anything below threshold goes into a parking-lot file, not the active backlog.
9. **Hand off** — to `seo` for per-page implementation, to `vitals` for performance items, to `geo` for AI-citation items, to `bolt` for performance code, to `artisan` for UI changes.

## Output Template

```yaml
audit_report:
  baseline:
    indexed_pages: 12480
    avg_click_depth: 3.7
    googlebot_fetches_30d: 184320
    ai_bots_in_logs: [GPTBot, ClaudeBot, PerplexityBot]
    ai_bots_missing: [OAI-SearchBot, Claude-SearchBot]  # CRITICAL
  layers:
    L1:
      passed: 6
      failed: 2
    L2:
      passed: 7
      failed: 1
    L3:
      passed: 5
      failed: 3
    L4:
      passed: 4
      failed: 3
    L5:
      passed: 4
      failed: 5
  backlog_top_30:
    - id: A-01
      layer: L5
      title: "OAI-SearchBot blocked by Cloudflare WAF rule #4421"
      severity: Blocker
      affected_urls: all
      effort: S
      fix: "Add Cloudflare rule to allow user-agent OAI-SearchBot/1.0 with rate limit 60/min"
      verify: "Confirm logs show 200 OK to OAI-SearchBot within 48h"
      handoff: scaffold | gear
    - id: A-02
      layer: L3
      title: "1,240 orphan blog posts (no internal links)"
      severity: High
      affected_urls: 1240
      effort: M
      fix: "Add 'Related posts' module powered by topical cluster ID; link 5 siblings per post"
      verify: "Re-crawl shows < 50 orphans"
      handoff: artisan
    # ... up to 30 items
  parking_lot_count: 87
  refresh_cadence: quarterly
```

## Anti-Patterns

- 200-row audit spreadsheets — rejected by implementers, nothing ships.
- Auditing without log files — half of crawl issues are invisible from a desk crawler.
- Ignoring AI search-bot vs training-bot distinction — silently blocks AI citation.
- Trusting tool "site health score" as a single number — averages hide blockers.
- Recommending fixes without effort estimates — implementer cannot triage.
- Auditing on staging that disallows all bots — crawler-blocked staging gives false negatives.
- "Improve X" findings without concrete fix steps — non-actionable.
- Sitewide canonical-to-homepage — common bug; eliminates 99% of indexable pages.
- Treating noindex + canonical to another URL as equivalent — they signal different things; mixing them confuses Google.
- Auditing once per year — quarterly cadence is the minimum for SERP-relevant signals.

## Deliverable Contract

A site audit is complete when:

- All 5 layers checked with explicit pass/fail per check.
- Log-file analysis covers ≥ 30 days for both Googlebot and AI bots.
- Backlog capped at 30 items, prioritized.
- Each item has severity, affected URL count, effort estimate, concrete fix, verification step, handoff agent.
- Parking-lot file documents excluded findings (so nothing is lost).
- Refresh cadence is set (quarterly default).

## References

- Google Search Central, *Search Quality Evaluator Guidelines* (2024).
- Google Search Central, *AI features and your website* (2024) — AI bot taxonomy.
- Aleyda Solis, *Crawling Mondays* (technical SEO methodology).
- Bartosz Góralewicz, *Onely* — JS rendering and crawl auditing.
- Botify, *The Crawl Budget Optimization Playbook* (2024).
- Screaming Frog, *SEO Spider User Guide*.
- Tomek Rudzki, *Indexing Insight* — indexability deep-dive.
- John Mueller (Google), *Search Off the Record* podcast — canonical / hreflang clarifications.
