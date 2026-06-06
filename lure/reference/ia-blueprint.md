# IA Blueprint — Information Architecture, SEO & GEO

Information Architecture, technical SEO, content SEO, and AI-search GEO are interleaved disciplines. `lure` treats them as one continuous axis: structure → readability → discoverability → citation-readiness.

> The best LP is one a human scans in 5 seconds, Google parses in 50ms, and an LLM cites verbatim. Same structure does all three.

---

## Section 1 — Information Architecture

### 1.1 Content Inventory & Hierarchy

Before wireframing, build a content inventory.

```yaml
CONTENT_INVENTORY:
  Promise: "<one sentence — locked at Strategy>"
  Pillars:
    - id: P1
      claim: "<top benefit>"
      proof: ["<proof point>", "<proof point>"]
      objection: "<the doubt this raises>"
      counter: "<how we address it>"
    - id: P2
      claim: "..."
  Authority_Anchors:
    - type: numeric | named-customer | award | open-source | press | founder
      value: "<concrete>"
  Decision_Triggers:
    - type: risk-reversal | urgency | clarity | social
      value: "<concrete>"
  CTAs:
    Primary: { verb: "...", outcome: "..." }
    Secondary: { verb: "...", outcome: "..." }
```

Inventory drives section count: 1 hero + (1 section per pillar) + proof + objection + final CTA + FAQ.

### 1.2 Visual Hierarchy Patterns

| Pattern | Use | Layout heuristic |
|---------|-----|------------------|
| **F-pattern** | Text-heavy, B2B, info-dense, blog-style | Strong left edge, headline + sub on left, supporting media right; eyes drop down left edge |
| **Z-pattern** | Above-fold hero with CTA | Top-left logo → top-right utility/login → diagonal sweep to hero copy → CTA at bottom-right Z-tail |
| **Layer-cake** | Product LPs, e-com, mobile-first | Full-width alternating sections, single column on mobile, hero image alternates left/right on desktop |
| **Centered axis** | Calm UI, premium, focus-first | Single column, generous whitespace, centered hero, mobile-identical |
| **Card grid** | Comparison, plan tiers, feature matrices | 2–4 column grid with consistent card anatomy |

Choose ONE primary pattern per page. Don't mix Z and centered-axis in one LP.

### 1.3 Scroll Narrative

The page tells a story top-to-bottom. Default arc:

1. **Promise** (hero) — what + for whom + why now
2. **Trust prime** (logo strip / numbers) — borrow credibility before asking for it
3. **Pillar 1** — top benefit framed as outcome
4. **Pillar 2** — second benefit, often "how it works"
5. **Proof** — specific outcome from named customer
6. **Pillar 3** — third benefit, often differentiation
7. **Objection** — FAQ-style or comparison table
8. **Final push** — risk-reversal + final CTA
9. **FAQ** — scannable, 3–5 Q/A
10. **Footer** — trust signals, legal, contact

Adjust order by Recipe (e-com pulls reviews higher; B2B pulls case study higher; lead-magnet collapses to 4–5 sections).

### 1.4 Content Chunking & Progressive Disclosure

- **One idea per section.** If a section needs two H2s, split.
- **Scan-readable.** Every section answers in 5 seconds: what it claims + what proves it.
- **Progressive disclosure**: long copy → expandable cards. Form fields > 3 → multi-step. Detail dumps → tabs or accordions.
- **Cognitive load budget**: max 7±2 distinct elements above fold. Reduce to 5 on mobile.

### 1.5 Heading Hierarchy

Hierarchy serves IA + SEO + GEO + a11y simultaneously.

| Level | Use | Count per page |
|-------|-----|----------------|
| **H1** | Page promise. One per page. | Exactly 1 |
| **H2** | Pillar / section claim | 4–8 |
| **H3** | Sub-claim within a section | 0–3 per H2 |
| **H4** | Rarely needed; FAQ questions if used | Optional |

Anti-patterns: skipping levels (H1 → H3), multiple H1s, H1 hidden visually for "SEO". Each heading must read as a meaningful claim, not a label.

### 1.6 Navigation Patterns

| Pattern | When |
|---------|------|
| **No nav** | Single-purpose LPs, lead-magnets, event registration |
| **Skinny utility bar** | Logo + sign-in + secondary action only |
| **Sticky CTA** | Long LPs (> 2000 words), high-friction CTA |
| **Anchor TOC** | Long LPs (> 5 sections), B2B comparison pages |
| **Mobile bottom CTA bar** | E-com, lead-gen on mobile |
| **Exit-intent overlay** | Lead-magnet downgrade, never on first-impression LPs |

Anti-pattern: full site nav on LPs. Every link is a leak.

### 1.7 IA Quality Rubric

Ship target: ≥ 15/20.

| Criterion | 4 — Excellent | 3 — Good | 2 — Weak | 1 — Broken |
|-----------|---------------|----------|----------|------------|
| **Single promise** | One promise, one path | Mostly | Two promises | Three+ promises |
| **5-second scan** | Promise + proof + next step visible in 5s | Mostly | Some friction | Cannot scan |
| **Scroll arc** | Coherent story top-to-bottom | Mostly | Disjointed | Random order |
| **Chunking** | One idea per section, < 7 above-fold | Mostly | Crowded | Wall of content |
| **Heading hierarchy** | H1 + clean H2/H3 tree | Mostly | Some skips | Broken tree |

---

## Section 2 — Technical SEO

### 2.1 Core Indexability

- **`<title>`**: 50–60 characters. Brand + benefit + keyword. Unique per page.
- **Meta description**: 140–160 characters. Compelling, includes primary keyword, ends with action verb.
- **Canonical URL**: explicit `<link rel="canonical">` on every page, including the page itself.
- **Robots**: `noindex, follow` for staging / A/B variants; `index, follow` for production.
- **XML sitemap**: page included; updated `<lastmod>`.
- **`robots.txt`**: doesn't block the LP path; allows crawler access to JS/CSS.
- **hreflang**: when multi-locale, every locale variant cross-references all others including itself; `x-default` set.

### 2.2 Structured Data (Schema.org / JSON-LD)

Choose the schema that matches the LP type. Validate with Rich Results Test before launch.

| LP Type | Primary schema | Optional add-ons |
|---------|----------------|------------------|
| SaaS / SaaS Trial | `SoftwareApplication` or `Product` | `Offer`, `AggregateRating` (if reviews), `Organization`, `FAQPage` |
| E-com Product | `Product` + `Offer` | `AggregateRating`, `Review`, `BreadcrumbList`, `Brand` |
| Event / Webinar | `Event` | `Offer` (free/paid), `Place` (virtual: `VirtualLocation`) |
| Lead Magnet (book/template) | `Book` / `CreativeWork` | `Person` (author), `Offer` (free download) |
| Course | `Course` | `Offer`, `Instructor`, `Provider` |
| Service / Consulting | `Service` | `Offer`, `Organization`, `Review` |
| Newsletter | `Organization` + `WebSite` | `SearchAction` |

Always include: `Organization`, `WebSite`, `WebPage`, `BreadcrumbList`, `FAQPage` (when FAQs exist), `Person` (when author authority matters).

### 2.3 Core Web Vitals (2026 thresholds)

| Metric | Good | Needs improvement | Poor |
|--------|------|--------------------|------|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | 2.5–4s | > 4s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | 200–500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | 0.1–0.25 | > 0.25 |

Ship target: all three Good. Bolt owns this gate.

### 2.4 Open Graph / Twitter Cards

- `og:title`, `og:description`, `og:image` (1200×630), `og:url`, `og:type`.
- `twitter:card` = `summary_large_image`; `twitter:title`, `twitter:description`, `twitter:image`.
- Per-locale variants when hreflang is in scope.

### 2.5 AI Crawler / Bot Policy (2026)

Robots policy must distinguish **Training** bots from **Search/Retrieval** bots. Blocking one does not block the other; conflating them costs AI-search visibility.

| Bot | Purpose | Recommended action |
|-----|---------|---------------------|
| `GPTBot` | OpenAI training | Allow if licensing model includes training data; otherwise deny |
| `OAI-SearchBot` | ChatGPT Search retrieval | **Allow** (denying disables ChatGPT Search citations) |
| `ChatGPT-User` | User-initiated browsing | Allow |
| `ClaudeBot` | Anthropic training | Allow or deny per training policy |
| `Claude-SearchBot` | Claude Search retrieval | **Allow** |
| `Claude-User` | User-initiated browsing | Allow |
| `PerplexityBot` | Perplexity retrieval | **Allow** |
| `Google-Extended` | Bard/Gemini training | Allow or deny per training policy |
| `Googlebot` / `Googlebot-Image` | Google Search + AI Overviews | **Allow** |

**Anti-pattern**: blanket `Disallow: /` for `User-agent: *` then forgetting AI search bots. Estimated 73% of sites unintentionally block Search-class bots this way.

Verify crawl access in production via server log inspection (presence of expected User-Agent hits within 7 days of launch). `llms.txt` is NOT honored by major AI crawlers as of 2026; do not rely on it.

### 2.6 Image & Video SEO

Images:
- AVIF/WebP with JPEG fallback; lossy at quality 75–85
- Explicit `width` and `height` attributes (prevents CLS)
- `loading="lazy"` below fold; `fetchpriority="high"` on LCP image (never both)
- `srcset` for responsive variants; `sizes` attribute set
- Descriptive alt text matching surrounding context (NOT keyword-stuffed); decorative images use `alt=""`
- `ImageObject` JSON-LD for hero / product images with `caption`, `creditText`, `creator`
- Filename: kebab-case descriptive (`product-name-feature-view.avif`), not `IMG_4823.jpg`

Videos:
- `VideoObject` JSON-LD with `name`, `description`, `thumbnailUrl`, `uploadDate`, `duration`, `contentUrl`
- Transcript visible or via `transcript` field (also feeds GEO)
- `poster` set; `preload="metadata"` default
- Chapter markers via WebVTT for long-form (also surfaces in AI Overviews)

### 2.7 Resource Hints & Indexability

- `<link rel="preconnect">` for known third-party origins (fonts, analytics, CDN)
- `<link rel="dns-prefetch">` for opportunistic origins
- `<link rel="preload">` for LCP-critical font/image
- **IndexNow** ping (Bing/Yandex; Cloudflare default in 2026) for instant indexing — supplements sitemap.xml, not replaces

### 2.8 Technical SEO Audit Checklist

Run at Optimize gate:

```
[ ] <title> unique, 50–60 chars (70 chars OK if question-form for AI Overview eligibility)
[ ] <meta description> 140–160 chars
[ ] Canonical tag present and correct
[ ] Robots directive correct (index/noindex per env)
[ ] AI bot policy explicit (Training vs Search differentiated per §2.5)
[ ] hreflang tags (if multi-locale); x-default set
[ ] XML sitemap entry present; IndexNow ping configured
[ ] JSON-LD primary schema valid (Rich Results Test)
[ ] Schema-content consistency (price/availability/rating match visible content)
[ ] Open Graph + Twitter Card complete; per-locale variants if multi-locale
[ ] All images optimized per §2.6 (AVIF/WebP, dimensions, alt, ImageObject for hero/product)
[ ] All videos schema'd per §2.6 (VideoObject, transcript)
[ ] H1 unique on page; H tree well-formed (no skipped levels)
[ ] Internal links use semantic anchors (not "click here")
[ ] No broken links (200 OK on all internal links); redirect chain ≤ 2 hops
[ ] HTTPS, valid cert, HSTS / CSP / X-Content-Type-Options / Referrer-Policy headers set
[ ] viewport meta present; tap targets ≥ 48×48 CSS px
[ ] Resource hints in place per §2.7
[ ] Mobile-friendly (Lighthouse Mobile: Perf ≥ 90, Acc ≥ 95, BP ≥ 95, SEO ≥ 95)
[ ] Core Web Vitals: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1, TTFB ≤ 800ms (p75), FCP ≤ 1.8s
```

---

## Section 3 — Content SEO

### 3.1 Search Intent Alignment

Classify the target query:

| Intent | LP shape | CTA |
|--------|----------|-----|
| **Informational** | Education-led, deep content, examples, comparison | Soft CTA — newsletter / related resource |
| **Navigational** | Brand-led, clear "is this the right page" cues | Direct CTA — sign in / contact |
| **Commercial investigation** | Comparison, social proof, calculator, demo | Mid-friction CTA — demo / trial |
| **Transactional** | Conversion-optimized hero, scarcity, trust, fast checkout | High-intent CTA — buy / start free trial |
| **Answer-Engine (2026)** | TL;DR above fold + question-as-heading + stat-with-source + author byline | Page is the answer; secondary CTA = learn-more / brand-context |

Mismatched intent = high bounce + zero CVR. Researcher + Growth align this at Discover / Strategy.

### 3.2 Keyword Strategy

- **One primary keyword** per page; align with H1 + title + first paragraph.
- **3–5 secondary keywords / semantic variants** woven naturally through H2s and body.
- **Avoid stuffing**: density check via Growth; if natural reading drops, rewrite.
- **Long-tail focus**: target specific phrases (`best invoicing tool for freelancers`) over head terms (`invoice`).
- **Featured snippet eligibility**: structured Q&A, definition paragraphs, lists, comparison tables.

### 3.3 E-E-A-T Signals + Author Entity

For high-trust categories (YMYL: health, finance, legal, news) and AI-search:

| Signal | How to surface on LP |
|--------|----------------------|
| **Experience** | Founder story, case studies, named customer testimonials, hands-on demos |
| **Expertise** | Author credentials, published research, awards, certifications, technical depth in content |
| **Authoritativeness** | Press mentions, industry recognition, citations from authoritative sites, expert endorsements |
| **Trustworthiness** | Privacy / terms / security badges, transparent pricing, contact info, guarantee, real reviews |

**Author Entity** is the structured implementation of E-E-A-T (also feeds GEO §4 citability):

```json
{
  "@type": "Person",
  "name": "Author Name",
  "jobTitle": "Title / role",
  "worksFor": { "@type": "Organization", "name": "Brand" },
  "url": "https://brand.example/team/author",
  "sameAs": [
    "https://www.linkedin.com/in/author-handle",
    "https://orcid.org/0000-0000-0000-0000",
    "https://www.wikidata.org/wiki/Q...",
    "https://github.com/author-handle"
  ]
}
```

Wire `Person` into `WebPage.author` or `Article.author`. Visible byline + credentials line on the page itself. `sameAs` should reach at least one platform LLMs grade as authoritative (Wikidata, ORCID, Wikipedia, Crunchbase, major academic press).

### 3.4 Topical Authority

If the LP sits within a topical cluster:
- Internal link to 3–5 pillar / supporting pages.
- Mention the broader topic in the introduction.
- Schema-graph the relationship via `BreadcrumbList` and `WebPage.isPartOf`.

---

## Section 4 — GEO (Generative Engine Optimization)

LLM-driven search (Perplexity, ChatGPT search, Gemini, Claude search, AI Overviews) reads pages differently from traditional crawlers. They prefer pages that are:

- **Citable** — facts attributable to a source
- **Structured** — clear question-answer pairs
- **Concise** — TL;DR, key takeaways, summary tables
- **Authoritative** — author bylines, original data, named expertise

### 4.1 GEO Structural Patterns

| Pattern | What it does |
|---------|--------------|
| **TL;DR block above fold** | LLMs lift this verbatim for citations. **First 30% of page text accounts for ~44% of citations.** **Authorship rule: Prose writes the TL;DR under Growth's structural brief — never Growth directly, to preserve brand voice.** |
| **Question-as-heading** | Increases chance of citation in conversational search; 120–180 words between headings yields ~70% more citations |
| **Definition-first paragraphs** | "X is Y because Z" pattern matches LLM training |
| **Comparison tables with rows = features, columns = options** | Cited in "X vs Y" queries |
| **Stat blocks with sources** | "$1B processed (Stripe, 2025)" — cited with attribution |
| **FAQ with structured Q/A** | Direct lift into AI Overview |
| **Stacked Schema** (Article + ItemList + FAQPage triple) | Up to 1.8× more AI citations vs single-schema pages (Princeton GEO research) |
| **Author byline + credentials** | E-E-A-T signal for LLM trust; couples to §3.3 Author Entity |
| **Last-updated date visible** | Freshness signal — LLMs prefer fresh sources |

### 4.1.1 Per-Platform Tactics (2026)

Different AI search engines weight different signals. Tune for the platforms your audience actually uses.

| Platform | Crawler | Primary citation drivers | Tactic |
|---|---|---|---|
| **Perplexity** | `PerplexityBot` | Recency + stat-with-source + URL-rich text | Date-stamp content; embed primary-source stats; explicit author byline |
| **ChatGPT Search** | `OAI-SearchBot` + `ChatGPT-User` | Structured Q&A; clear definitions | FAQPage schema; question-as-H2; 40–60 word direct answers |
| **Claude Search** | `Claude-SearchBot` + `Claude-User` | Authoritative sources (Wikipedia / Reuters / academic) | Wikidata `sameAs`; press-link pyramid; cite primary sources |
| **Google AI Overviews / AI Mode** | `Googlebot` | Existing search rank × structured data | Strong technical SEO + FAQPage + HowTo + Speakable |
| **Gemini** | `Google-Extended` + `Googlebot` | Same as AI Overviews + multimodal context | Add structured image/video schema + transcripts |

### 4.2 GEO Content Patterns

- Write **answers first**, context after. Inverted pyramid.
- Include **named entities** (people, products, places, dates) — LLMs index entities.
- Quote yourself in **citable units** — 1-sentence summaries that can stand alone.
- Provide **original data** when possible — LLMs prefer primary sources over aggregators.
- Avoid clickbait — LLMs deprioritize sources with weak factual grounding.

### 4.3 GEO Technical Patterns

- `Author` and `Organization` schema with `sameAs` links to authoritative profiles (LinkedIn, Wikipedia, Wikidata, ORCID, Crunchbase, GitHub).
- `dateModified` and `dateCreated` exposed in schema and visible UI.
- `mainEntityOfPage` set on the primary content; `@graph` + `@id` cross-references for entity disambiguation.
- `citation` field in schema for original research.
- `speakable` schema for voice-AI answer eligibility.
- `HowTo` schema for procedural content (high citation pickup in step-by-step queries).
- `QAPage` (distinct from `FAQPage`) when the page itself answers one primary question.
- AI-crawler access verified via server log within 7 days of launch (PerplexityBot / OAI-SearchBot / Claude-User hits present).

### 4.3.1 GEO KPIs (measurement, not just structure)

Pulse + Growth + Beacon coordinate measurement:

| KPI | Definition | Target |
|---|---|---|
| **Mention Rate** | % of brand-relevant AI-search queries that mention the brand | ≥ 15% |
| **Citation Rate** | % of mentions that include a clickable URL citation | Baseline + 30% within 90 days of launch |
| **Share of Voice** | Mentions of brand vs top 3 competitors across a fixed query set | Tracked; trend > 0 |

### 4.4 GEO Quality Rubric

Ship target: ≥ 15/20.

| Criterion | 4 — Excellent | 3 — Good | 2 — Weak | 1 — Broken |
|-----------|---------------|----------|----------|------------|
| **TL;DR present** | Above fold, lift-ready | Present but buried | Implicit only | Absent |
| **Question structure** | Question-as-heading throughout | Some questions | Mostly statements | No questions |
| **Citable facts** | Stat-with-source frequent | Some stats sourced | Stats without source | Vague claims |
| **Author authority** | Named author + credentials + sameAs | Named author only | Implicit | Anonymous |
| **Freshness** | Last-updated visible + recent | Recent but hidden | Stale | No date |

---

## Section 5 — Coordination With Other Disciplines

These rules keep IA + SEO + GEO aligned with Brand, Design, and Marketing:

1. **Heading text is brand voice.** SEO requires keywords; brand requires voice. Solution: lead with brand voice, weave keyword naturally. Never sacrifice voice for keyword density.
2. **Schema must reference the brand system.** `Organization.name`, `Person.name`, `Product.name` use the brand's canonical spelling.
3. **Trust signals serve all four** — IA (above fold), SEO (E-E-A-T), GEO (authority), Brand (positioning). Place them once, well.
4. **Performance is an IA decision.** Hero video weight, font weight, third-party scripts — all are IA trade-offs because they delay LCP and reduce scan-readiness.
5. **FAQ does triple duty.** Objection handling (IA), `FAQPage` schema (SEO), AI Overview eligibility (GEO). Write FAQ once, deploy across all three.
6. **Internationalization is an IA + SEO + Brand decision.** Polyglot extraction must preserve heading hierarchy, schema validity, and brand voice across locales.

---

## Section 6 — IA / SEO / GEO Gate (Optimize stage)

Composite gate enforced by `lure` at Optimize stage exit:

| Sub-gate | Threshold | Owner |
|---------|-----------|-------|
| IA rubric | ≥ 15/20 | `lure` + Funnel |
| Technical SEO checklist | All boxes ticked | Growth |
| Schema validity | Rich Results Test green | Growth |
| CWV | All Green | Bolt |
| Content SEO | Primary keyword aligned (title/H1/first para); intent matched | Growth |
| GEO rubric | ≥ 15/20 | Growth |

Fail → repair pass. Twice fail → escalate to user.
