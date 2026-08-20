# Compete Recipe Registry

The full Recipe table for `compete`. `compete/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Competitor Matrix | `matrix` | ✓ | Competitor map, feature comparison matrix, tiering | — |
| SWOT Analysis | `swot` | | SWOT, positioning, differentiation strategy | `reference/competitive-moats-category-design.md` |
| Positioning Map | `positioning` | | Positioning map, category design, moat evaluation | `reference/competitive-moats-category-design.md` |
| LLM Visibility | `llm-visibility` | | LLM brand presence, AI share of voice measurement | `reference/intelligence-gathering.md` |
| Battle Card | `battle` | | One-pager sales enablement, objection-handling pairs, freshness governance, GTM distribution | `reference/battle-card.md` |
| Win/Loss Analysis | `winloss` | | Post-decision interviews, segmentation, theme extraction, cadence design, CRM integration | `reference/winloss-analysis.md` |
| Moat (7 Powers) | `moat` | | Helmer 7 Powers assessment, durability scoring, anti-moat detection | `reference/moat-7-powers.md` |
| Professional Brand | `brand` | | Engineer-brand family: audit, profile, content, topic-dna, portfolio, or bio variant | `reference/positioning-frameworks.md`, `reference/metrics-guide.md` |
| Multi-Engine | `multi` | | Tri-engine coverage (Codex + agy + Claude parallel) leveraging non-overlapping priors. Artifact-driven merge with `engine_concurrence` tags + mandatory "Uncommon Competitors (Verified-Divergent)" callout patching single-engine blind-spots. | `reference/tri-engine-compete.md` |
