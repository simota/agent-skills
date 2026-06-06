# GEO (Generative Engine Optimization) — 2026 Field Guide

## What changed in 2025–2026

- **AI Overviews scaled globally.** As of May 2025, AI Overviews are available in 200+ countries and 40+ languages [Source: Google, *AI Overviews expansion* (2025-05), https://blog.google/products/search/ai-overview-expansion-may-2025-update/]. AI Overviews appear on ~13% of all Google queries (Semrush AIO prevalence study peaked at ~25% in mid-2025, settled around 15.69% Nov 2025) [Source: Search Engine Land, https://searchengineland.com/google-ai-overviews-ctr-recovery-study-475566].
- **AI Mode is the new conversational layer.** Google AI Mode (launched at I/O 2025) reached US, India, Japan, South Korea, Indonesia, Brazil in 2025 and went near-global (~200 countries, 98 languages) at I/O 2026 (2026-05) with **Gemini 3.5 Flash** as the default model [Source: Google blog — *AI Mode expands languages and locations* (2026-05), https://blog.google/products-and-platforms/products/search/ai-mode-expands-languages-locations/]. The classic SERP and AI Mode are merging into one continuous experience.
- **CTR impact is severe but cited pages benefit.** Seer Interactive (Sept 2025): organic CTR on AIO-present queries dropped **61% (1.76% → 0.61%)**, paid CTR dropped 68%; but **cited pages earn 35% more organic clicks (91% more paid)** than uncited pages on the same SERP [Source: Search Engine Land, https://searchengineland.com/google-ai-overviews-hurt-click-through-rates-454428]. CTR is also recovering: from 1.3% (Dec 2025) to 2.4% (Feb 2026), an 85% rebound [Source: https://searchengineland.com/google-ai-overviews-ctr-recovery-study-475566].
- **Citation decoupled from rank.** In mid-2025 ~76% of AI Overview citations came from the organic top-10; by early 2026 that share collapsed to 38% (some reports as low as 16%) — being ranked #1 no longer guarantees AI citation [Source: Edward Rippen — *AI Overviews citation strategy 2026*, https://edwardrippen.com/ai-overviews-citation-strategy-2026/]. Reddit and other community sources are increasingly cited (Tinuiti AI Citations Trends Q1 2026: social media share of AI citations >9%, Reddit dominant) [Source: CMSWire, https://www.cmswire.com/digital-marketing/reddits-rise-in-ai-citations-what-marketers-must-know-about-aeo-strategy/].

## The Princeton GEO framework

The term GEO and the original methodology come from Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan, Deshpande, *GEO: Generative Engine Optimization* (Princeton / GA Tech / AI2 / IIT Delhi), ACM SIGKDD 2024 (preprint Nov 2023, arXiv:2311.09735). The paper tested nine optimization strategies across 10,000 queries and multiple generative engines; the winning combination — **adding statistics, citing sources, adding quotations, mentioning authorities** — raised visibility by **up to 40%** in AI-generated responses [Source: Princeton — *GEO: Generative Engine Optimization*, https://collaborate.princeton.edu/en/publications/geo-generative-engine-optimization/].

## Four-signal framework

| Signal | Question | Tactics |
|--------|----------|---------|
| Retrievability | Can AI bots fetch the page? | robots.txt allows search/retrieval bots; SSR or static prerender of primary content; no JS-only gating |
| Extractability | Can AI parse a structured answer? | Direct-answer first 200 words; 120–180 words per H2; FAQ + HowTo + Article + ItemList stacked schema |
| Credibility | Are claims defensible? | 3–5 inline citations from authoritative sources per page; original data / statistics; author bio with credentials |
| Entity clarity | Are entities disambiguated? | Schema.org `@id` cross-references; consistent canonical naming; Organization + WebSite + sameAs links |

## AI crawler taxonomy (2026-05)

> **Training-bot blocks do not affect AI search citation. Search/retrieval-bot blocks remove you from AI search entirely.** Audit both before changing robots.txt.

| Vendor | Training crawler (safe to block) | Search/retrieval bot (KEEP ALLOWED for citation) | User-initiated fetch |
|--------|----------------------------------|--------------------------------------------------|----------------------|
| OpenAI | `GPTBot` | `OAI-SearchBot` | `ChatGPT-User` |
| Anthropic | `ClaudeBot` | `Claude-SearchBot` | `Claude-User` (+ `claude-code` for CLI) |
| Google | `Google-Extended` | (Googlebot covers AIO/AI Mode) | `Google-NotebookLM`, `Google-Read-Aloud` |
| Perplexity | (none separate) | `PerplexityBot` | `Perplexity-User` |
| Apple | `Applebot-Extended` | `Applebot` | — |
| Meta | — | `meta-externalagent` | — |

Anthropic confirmed the 4-bot split (`ClaudeBot` / `Claude-SearchBot` / `Claude-User` / `claude-code`) in its public bot directory; SE Ranking observed that 73% of sites have unintentional barriers (broad robots.txt, CDN/WAF rules, JS-only rendering) blocking AI retrieval bots [Source: ALM Corp — *Anthropic's three-bot framework*, https://almcorp.com/blog/anthropic-claude-bots-robots-txt-strategy/].

### llms.txt status (2026-05): **do not rely on it**

SE Ranking study of 300,000 domains: **~10.13% adoption**, but **GPTBot, ClaudeBot, OAI-SearchBot, Claude-SearchBot, PerplexityBot, Google-Extended overwhelmingly do not fetch `/llms.txt`** and crawl HTML directly. As of Q1 2026, no major AI vendor has publicly committed to honoring llms.txt in production [Source: AEO Press — *State of llms.txt 2026*, https://www.aeo.press/ai/the-state-of-llms-txt-in-2026]. Use robots.txt + structured data + canonical content — not llms.txt — as the primary GEO control surface.

## GEO KPIs (replace traditional rank tracking)

| KPI | Definition | Benchmark |
|-----|------------|-----------|
| Mention Rate | % of AI answers in a tracked prompt set that name your brand | <5% invisible, 5–15% emerging, 15–30% strong, >30% category leader |
| Citation Rate | % of those answers that include a clickable link to your domain | Perplexity highest citation/mention ratio; Google AI Mode lowest |
| Share of Voice | Brand mentions vs each tracked competitor across the prompt set | Track per-prompt-cluster to detect topical weakness |

Tools: ConvertMate, Profound, Otterly, AthenaHQ, Goodie, Peec.

## Anti-patterns

- Treating GEO as a single-platform game (ChatGPT-only) — each engine has different source sets and retrieval mechanics.
- Blocking `OAI-SearchBot` / `Claude-SearchBot` / `PerplexityBot` while keeping `Googlebot` allowed — you remain visible on Google AIO but invisible on ChatGPT, Claude, Perplexity citations.
- Publishing schema that contradicts visible page content — AI engines verify and penalize mismatches.
- Optimizing only for citation count, ignoring Share of Voice — high mentions with low citation links yield low downstream traffic.
- Ignoring Reddit and community surfaces — by 2026, community-sourced AI citations exceed 9% and are growing.

## References

- Aggarwal et al., *GEO: Generative Engine Optimization* (SIGKDD 2024 / arXiv:2311.09735).
- Google, *AI Mode expands languages and locations* (2026-05), https://blog.google/products-and-platforms/products/search/ai-mode-expands-languages-locations/
- Seer Interactive AI Overviews CTR studies (Sept 2025 + Feb 2026).
- Ahrefs, *Update: AI Overviews Reduce Clicks by 58%* (Dec 2025), https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/
- AEO Press, *State of llms.txt 2026*, https://www.aeo.press/ai/the-state-of-llms-txt-in-2026
- Tinuiti, *AI Citations Trends Report Q1 2026* (via CMSWire).
- ALM Corp, *Anthropic's Three-Bot Framework* (2026), https://almcorp.com/blog/anthropic-claude-bots-robots-txt-strategy/
- Schema.org v30.0 release (2026-03-19), https://schema.org/docs/releases.html
