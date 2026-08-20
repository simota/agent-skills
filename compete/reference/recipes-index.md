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

---

Behavior notes per Recipe:
- `battle`: One-pager — TL;DR, why-we-win, why-we-lose, 5 objection-handling pairs, landmines, traps, pricing posture, proof points. Source every claim; enforce 90-day max freshness; tag CRM `battle_card_used`. Pull win/lose narratives from `winloss` outputs — never from internal opinion. Distribute via CRM/Slack/deal-room.
- `winloss`: Post-decision interviews 2-6 weeks after decision; segment by `outcome x deal-size x competitor` min. Require `3+` mentions to elevate a theme; probe past "price". Third-party interviewers for losses. Quarterly cadence; feed CRM and `battle` cards.
- `moat`: Helmer 7 Powers double-test (Benefit AND Barrier); reject features-as-moats. Score durability via decade test; map industry phase (Origination/Take-Off/Stability). Detect anti-moats (platform dependence, customer concentration, AI commoditization) and net-discount. Hand off to Magi.
- `brand`: Use the second token or request signals to select `audit`, `profile`, `content`, `topic-dna`, `portfolio`, or `bio`; default to `audit`. Every variant runs `DISCOVER -> POSITION -> CRAFT -> AMPLIFY -> MEASURE`, uses only real contribution evidence, and applies relevant anti-pattern checks. `profile` and `bio` derive from one canonical position; `content` derives 3-5 pillars and one primary hub; `topic-dna` verifies defensibility and durability; `portfolio` produces information architecture and hire-readiness guidance, never implementation.
- `multi`: Multi-engine competitive analysis. See **Multi-Engine Mode** below and `reference/tri-engine-compete.md` for operational detail.
