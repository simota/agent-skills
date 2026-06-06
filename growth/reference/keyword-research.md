# Keyword Research Methodology

## Purpose

Build the keyword universe that drives both traditional SEO ranking and GEO (AI-search) citation. Without intent classification and clustering, content competes on the wrong queries and scatters topical authority.

## Scope Boundary

- IN scope: seed expansion, search-intent classification, query clustering, SERP feature analysis, AI-prompt mining, prioritization scoring.
- OUT of scope: on-page meta implementation (`seo`), JSON-LD authoring (`geo`), conversion experiments (`cro`), competitor positioning (delegate to `compete`), KPI tracking dashboards (delegate to `pulse`).

## Core Concepts

### Four Search Intents (Google's Quality Rater Guidelines)

| Intent | Pattern | Example Query | Goal |
|--------|---------|---------------|------|
| Informational | "what / how / why" | "what is RAG" | Answer / explain |
| Navigational | brand or product name | "anthropic claude" | Find a specific destination |
| Commercial | "best / vs / review" | "best LLM API for production" | Evaluate alternatives |
| Transactional | "buy / pricing / signup" | "claude api pricing" | Take action |

Misclassification is the most common keyword-research failure: writing a buying-guide article for an informational query loses both rank and citation.

### Modifiers That Reveal Intent

| Modifier | Likely Intent |
|----------|---------------|
| how to, what, why, explain, tutorial, guide, definition | Informational |
| login, signin, dashboard, [brand] + [feature] | Navigational |
| best, top, vs, comparison, review, alternatives, "X or Y" | Commercial |
| buy, price, pricing, cheap, discount, signup, free trial | Transactional |
| near me, [city], [country] | Local / geographic |

### Long-Tail Distribution

Roughly 70% of all search queries are long-tail (3+ words, low individual volume). Long-tail traffic converts at 2.5–4× head-term rates and is significantly easier to rank for. A keyword universe weighted entirely toward head terms is a competition trap.

| Tier | Word Count | Volume | Competition | Conversion |
|------|-----------|--------|-------------|------------|
| Head | 1–2 | High | Very High | Low |
| Mid-tail | 2–4 | Medium | High | Medium |
| Long-tail | 4–8 | Low–Medium | Low–Medium | High |

### SERP Feature Signals

The SERP for a query tells you what content format the engine prefers:

| SERP Feature | Implication |
|--------------|-------------|
| Featured snippet | Direct-answer paragraph (40–60 words) wins |
| People Also Ask | FAQ schema + Q&A subheadings work |
| Video carousel | Embed video; pure text underranks |
| Image pack | Original images required |
| Product carousel | Product schema + price/rating |
| AI Overview | GEO optimization mandatory; structured data + first-200-word answer |
| Knowledge panel | Entity is well-defined; build around the canonical entity |
| Map pack | Local intent; LocalBusiness schema |

Always inspect the live SERP before committing — assumptions about format are wrong ~30% of the time.

### Keyword Difficulty Heuristics (Without Paid Tools)

Free signals you can read manually:

1. **Domain Rating of top 10** — if half are DR 80+, head-term ranking is a multi-quarter project.
2. **Forum / Reddit / community in top 10** — gap, easier to rank with a quality canonical answer.
3. **AI Overview present** — citation is the primary win, not rank #1.
4. **Search volume < 100/mo** — long-tail; rank fast but small individual yield.
5. **Wikipedia + .gov + .edu in top 10** — entity-level query, content needs deep authority.
6. **All top results > 2 years old** — refresh / update opportunity.

### Query Clustering

Group queries that share a SERP. Method (manual or automated):

1. Pull the top 10 results for each query.
2. If queries A and B share ≥ 4 of the top 10 URLs, they are the same SERP cluster.
3. One cluster = one canonical content asset; do not create cannibalizing pages.
4. Re-cluster every 90 days — Google reshuffles intent boundaries quarterly.

Tools that automate this: Keyword Insights, Surfer SEO, Ahrefs Parent Topic, Semrush Keyword Strategy Builder. Fully manual is feasible for clusters under 100 queries.

### AI-Prompt Mining (GEO)

Traditional keyword research targets typed search; GEO research targets the prompts that bring AI engines to your domain. Sources:

| Source | What to Extract |
|--------|-----------------|
| ChatGPT / Claude / Gemini / Perplexity prompt logs | Phrase patterns ("Compare X to Y for [persona]") |
| Reddit + Discord + Slack archives | Real natural-language formulations |
| Customer support chat / sales call transcripts | Buying-stage prompts |
| Google "People Also Ask" + autocomplete | Prompt seeds |
| Quora / Stack Overflow | Long-form question patterns |

AI prompts are typically 12–40 words, much longer than typed search. Capture the verbatim phrasing, not a normalized form.

### Prioritization Scoring (RICE-style)

| Factor | Weight | Notes |
|--------|--------|-------|
| Reach | volume × CTR-by-rank-target | **2026 reality (AIO-present queries):** Seer Sept 2025 measured organic CTR collapse from 1.76% to 0.61% (-61%) on AIO queries; rebounded to 2.4% by Feb 2026. For non-AIO queries use ~30% CTR for #1, 15% for #2, 10% for #3. For AIO queries, separately model **Citation Rate** because being cited drives +35% organic clicks. [Source: Search Engine Land, https://searchengineland.com/google-ai-overviews-ctr-recovery-study-475566] |
| Impact | $ value per visitor × intent multiplier | Transactional 5×, Commercial 3×, Informational 1× |
| Confidence | 0.4 / 0.7 / 0.9 by difficulty | DR mismatch reduces; topical authority match increases |
| Effort | content + linking + technical, in person-days | Conservative estimate |

Score = (Reach × Impact × Confidence) / Effort. Sort descending. Cap your roadmap at the top 30; below that the variance dominates the signal.

## Workflow

1. **Seed harvesting** — collect 20–50 seeds from product pages, sales transcripts, support tickets, competitors, autocomplete.
2. **Expansion** — for each seed, pull modifier expansions (how/best/vs/buy + question words).
3. **Volume + difficulty enrichment** — annotate each candidate with monthly volume and a difficulty proxy.
4. **Intent classification** — tag every candidate with one of the four intents.
5. **SERP inspection** — for the top 100 candidates, check the live SERP feature mix and snapshot it.
6. **Clustering** — group by SERP overlap (≥ 4 shared URLs in top 10).
7. **AI-prompt mining** — collect 20–50 verbatim AI prompts that map to the same clusters.
8. **Prioritization** — score with RICE; cut to a 30-item roadmap.
9. **Brief generation** — for each top cluster, write a content brief: target query, intent, SERP features to win, AI prompts to address, recommended schema, word count target.

## Output Template

```yaml
keyword_universe:
  seeds: [seed_1, seed_2, ...]
  candidates_total: 4327
  after_dedup: 1850
  classification:
    informational: 920
    commercial: 540
    transactional: 240
    navigational: 150
  clusters:
    - id: C-01
      canonical_query: "rag retrieval design patterns"
      sibling_queries: [...]
      intent: informational
      monthly_volume: 4200
      difficulty: medium
      serp_features: [featured_snippet, paa, ai_overview]
      ai_prompts:
        - "What are the key tradeoffs between dense and sparse retrieval for RAG?"
        - "Compare BM25 vs hybrid search for production RAG systems."
      rice_score: 184
      recommended_brief:
        format: long-form guide + FAQ
        word_count_target: 2200
        schema: [Article, FAQPage, BreadcrumbList]
        first_200_words_must_answer: "What are RAG retrieval design patterns?"
  roadmap_top_30: [C-01, C-04, C-07, ...]
```

## Anti-Patterns

- Targeting head terms with low domain authority — burning months on queries you cannot rank for.
- Skipping intent classification — content format mismatch is the #1 underperformance cause.
- One page per query instead of one page per cluster — cannibalization splits authority.
- Optimizing for volume alone, ignoring intent multiplier — high-traffic, low-revenue pages.
- Using keyword tools' static "difficulty" score without inspecting the live SERP — tool scores lag SERP changes by 30–60 days.
- Ignoring AI prompts — by 2026, AI search is 30%+ of all query traffic for many B2B verticals; prompts that don't appear in keyword tools never enter the roadmap.
- Refreshing the universe annually instead of quarterly — intent drift makes 6-month-old clusters unreliable.
- Treating navigational queries as content opportunities — you cannot win [Brand X] queries from outside Brand X's site.

## Deliverable Contract

A keyword research deliverable is complete when:

- ≥ 1,000 deduplicated candidates from seed expansion.
- 100% intent-classified.
- Top-100 candidates have live SERP snapshots within the last 30 days.
- Clusters use SERP-overlap method (≥ 4 shared URLs).
- AI prompts captured for each top cluster.
- RICE scoring applied; top-30 roadmap selected.
- Brief generated for each top-30 cluster (intent, format, schema, AI prompts, word target).
- Refresh cadence documented (90 days default).

## References

- Google Search Quality Rater Guidelines (2024 update) — official intent definitions.
- Andrei Broder, "A Taxonomy of Web Search" (2002) — original informational/navigational/transactional model.
- Ahrefs, *AI Overviews Reduce Clicks by 58%* (2025-12), https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/
- Aleyda Solis, *SEO Roadmap Methodology*.
- Aggarwal et al., *GEO: Generative Engine Optimization* (SIGKDD 2024 / arXiv:2311.09735) — citation patterns vs traditional queries.
- Seer Interactive AIO CTR studies (Sept 2025, Feb 2026 update) — post-AI-Overview CTR curves.
- Semrush AIO prevalence study 2025 — appears in ~13% of queries (Nov 2025: 15.69%).
- Tinuiti, *AI Citations Trends Q1 2026* — Reddit as growing AI-cited source post-Google×Reddit deal (2024-02).
