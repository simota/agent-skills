# Multi-Engine Competitive Analysis

> **Filename retained** as `tri-engine-compete.md` for backward compatibility. Covers both dual-engine baseline (Claude + Codex) and tri-engine optional (Claude + Codex + agy) modes.

Default flow for `/compete multi`. Run subagents in parallel — one per AVAILABLE engine — to surface competitive coverage across non-overlapping training-data priors, then integrate results into Battle Card / Feature Matrix / Positioning Map / SWOT artifacts with engine-concurrence attribution.

**Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT. For Compete the third engine's coverage uplift is **larger than for other Pattern D skills** because agy patches a blind-spot (large-cap APAC enterprise SaaS) that Claude and Codex share. When agy is UNAVAILABLE, surface the uncovered segment in the Uncommon-Competitors callout and recommend a manual WebSearch sweep. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Why multiple engines for competitive analysis (Pattern D — Divergence-primary):** Each engine's training data carries distinct enterprise/product exposure:

- **Codex** — GitHub-heavy corpus → strong on OSS, dev tools, infrastructure vendors, indie SaaS, GitHub-published changelogs
- **Antigravity** — Google-product-adjacent corpus → strong on Google Workspace / Cloud peers, enterprise SaaS, large-cap incumbents, ad/martech, regional Asia-Pacific players (optional axis when AVAILABLE)
- **Claude** — Anthropic-curated corpus → strong on diverse industries, B2C consumer brands, recent fundraising signal, AI-native competitors, regulated verticals

A single engine *will* systematically miss competitors in the segments it under-indexes. The most valuable output of multi-engine compete is a `VERIFIED-DIVERGENT` competitor — a real, ground-checked competitor that only one engine surfaced because the others' training data structurally blinded them to that segment. Dual-engine covers two of the three blind-spot axes (codex/claude); tri-engine adds the third (agy).

**Adapted from `_common/MULTI_ENGINE_RECIPE.md` and `spark/reference/tri-engine-proposal.md`. Re-uses PREFLIGHT, FAN-OUT, NORMALIZE, CLUSTER stages; specializes SCORE / GROUND / SYNTHESIZE for competitive coverage.**

---

## Flow

```
SCOPE → PREFLIGHT → FAN-OUT (parallel subagents) → NORMALIZE → CLUSTER → SCORE (coverage matrix) → GROUND → SYNTHESIZE → DELIVER
```

### 1. SCOPE

Define the competitive analysis target once. All three subagents share the same scope:

- Product / category boundary (what we sell, what category, what JTBD)
- Decision question (battle card? matrix? positioning? SWOT? — drives SYNTHESIZE format)
- Geographic / segment scope (global, US-only, JP-only, enterprise, SMB, etc.)
- Time horizon (current state, 12-month outlook, etc.)
- Known competitor seeds (if any — pass as "already known, surface additions")
- Pre-existing Voice / Pulse / Field signals (if any)

### 2. PREFLIGHT — engine availability detection (Compete main context, never delegated)

Run the combined preflight from `_common/MULTI_ENGINE_RECIPE.md §PREFLIGHT`. Probe `codex`, `agy`, `claude` binaries with version check and fallback path scan. Availability verdict rules identical to canonical protocol.

### 3. FAN-OUT — parallel subagents

Spawn **three Agent calls in a single message** for genuine parallel execution.

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `compete-codex` | Codex CLI | `codex exec --full-auto "<prompt>"` |
| `compete-agy` | Antigravity CLI | `agy -p "<prompt>" --dangerously-skip-permissions --log-file <path>` (silent-failure detection mandatory — see `_common/MULTI_ENGINE_RECIPE.md §3.5 Engine Runtime Failure Detection`) |
| `compete-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

**Loose prompt rule**: pass only Role + Target + Output format. Do NOT pass Compete's analysis templates, 7 Powers framework, SWOT taxonomies, or positioning-map axes — those apply in SYNTHESIZE. The whole point is to let each engine's training-data priors drive divergent competitor discovery.

**Required JSON output schema:**

```json
{
  "engine": "codex|agy|claude",
  "competitors": [
    {
      "name": "Canonical product/company name",
      "aliases": ["alternate names", "subsidiaries", "rebrand history"],
      "category": "direct | indirect | substitute | non-consumption",
      "positioning": "One-sentence value proposition as the competitor would phrase it",
      "primary_segment": "ICP / target customer (e.g., 'mid-market SaaS RevOps')",
      "geography": "global | US | EU | JP | APAC | regional-other",
      "features": ["feature 1", "feature 2", "..."],
      "strengths": ["what they win on"],
      "weaknesses": ["where they are exposed"],
      "pricing_posture": "freemium | usage-based | per-seat | enterprise-only | unknown",
      "evidence_sources": ["URL or attribution per claim"],
      "source_engine_bias_note": "Why this engine likely knows this competitor (optional self-aware tag)"
    }
  ],
  "engine_notes": "Optional: training-data domains this engine knows it over-indexes / under-indexes"
}
```

Ask each subagent to surface **5-10 competitors** spanning direct / indirect / substitute / non-consumption. Encourage breadth over depth — depth happens in SYNTHESIZE.

If an engine returns free-form Markdown, ask its subagent to re-emit as JSON before integrating.

### 4. NORMALIZE

Parse the three JSON blobs into a unified competitor list. Tag each entry with `source_engine`. Preserve per-engine wording — divergent phrasings on positioning / weaknesses often carry signal about which segment the engine is viewing the competitor from.

### 5. CLUSTER — dedup across engines (competitor identity normalization)

Group entries that describe the same competitor under different surface names. This is harder than for proposals because competitor naming is genuinely ambiguous (parent vs product, rebrands, regional names).

**Identity match rules** — two entries match when **at least two** of the following hold:

1. **Canonical name overlap** — same product name OR the alias of one matches the canonical of the other (e.g., "Google Docs" ≡ "Docs by Google" ≡ "Google Workspace Docs")
2. **Domain-of-record overlap** — same primary website / product URL
3. **Parent ↔ product collapse** — one entry names the parent company, another names the specific product (e.g., "Microsoft" + "Microsoft 365" — collapse to product-level unless the analysis is at vendor level)
4. **Category + segment + JTBD overlap** — same `category`, same `primary_segment`, and the `positioning` describes the same job-to-be-done

**Do NOT cluster when**:

- Same vendor, different products targeting different JTBDs (e.g., "Notion Docs" vs "Notion Calendar" — keep separate if the analysis is product-level)
- Same product name, different vendors (rare but happens — "Stream" by AWS vs "Stream" by another vendor)
- Acquired-but-still-distinct brands (e.g., "Figma" + "Adobe" pre-merger termination — keep distinct because positioning differs)

Record the set of engines that surfaced each cluster — this becomes the coverage tag at SCORE.

### 6. SCORE — competitive coverage matrix (Pattern D, divergence-primary)

Score each cluster on two axes:

| Engines in cluster | Coverage label | Interpretation |
|--------------------|----------------|----------------|
| 3 / 3 | `UNIVERSAL` | Mainstream competitor — every engine independently surfaced this. Safe to assume the customer's buying committee also knows them. Risk: may be too obvious; check whether the competitor is actually a current threat or just well-known. |
| 2 / 3 | `LIKELY` | Strong competitor with one blind-spot engine. The missing engine's absence is itself a signal — usually means the competitor lives in a segment the missing engine under-indexes. |
| 1 / 3 (pre-ground) | `CANDIDATE` | Surfaced by one engine only. Either (a) a genuine uncommon competitor the other two engines structurally missed, or (b) a hallucinated / wrong-category / defunct entity. MUST pass GROUND step to ship. |
| 1 / 3 (post-ground) | `VERIFIED-DIVERGENT` | A grounded uncommon competitor. **This is the highest-value output of Compete `multi`** — it surfaces a real competitor that single-engine analysis would have missed. Treat as a structural blind-spot patch, not a low-confidence add-on. |

**Critical rule for Compete (Pattern D, distinct from Judge):** A `VERIFIED-DIVERGENT` competitor is **not** automatically lower-value than a `UNIVERSAL` one. The strategic value of tri-engine Compete is precisely to surface competitors a single engine would miss. The most actionable Battle Card row is often a `VERIFIED-DIVERGENT` competitor that the sales team has been losing deals to without knowing why.

### 7. GROUND — verify CANDIDATE/DIVERGENT competitors (Compete main context, WebSearch mandatory)

For every `CANDIDATE` cluster, run a real-time grounding pass before promoting to `VERIFIED-DIVERGENT`. WebSearch is **mandatory** — never ship a single-engine competitor based on training knowledge alone.

| Check | Verify | Reject if |
|-------|--------|-----------|
| Existence | WebSearch returns the company's website, product page, or recent press | No corporate footprint found — `REJECTED-HALLUCINATION` |
| Operating status | Site is live, last update within 12 months, no acquisition-then-discontinuation | Defunct, acquired-and-shutdown, or zombie site — `REJECTED-DEFUNCT` |
| Category fit | Actually competes in the named category for the named JTBD | Wrong category (e.g., a vertical CRM tagged as horizontal CRM) — `REJECTED-CATEGORY-MISMATCH` |
| Segment fit | Targets a segment relevant to the user's scope | Out of geographic / size scope and not strategically threatening — `REJECTED-OUT-OF-SCOPE` |
| Distinctness | Not already covered by a UNIVERSAL/LIKELY cluster under a different alias | Alias of an existing cluster the CLUSTER step missed — fold into that cluster |

For `UNIVERSAL` and `LIKELY` clusters, run a lightweight freshness check (WebSearch for "{competitor} {category}" with date filter) — confirm the competitor is still active and the positioning still matches. Multi-engine concurrence rarely hallucinates, but it can lag behind acquisitions/pivots.

**Source attribution is mandatory** at this step — every grounded competitor must carry the verifying URL (with access date) into SYNTHESIZE. Per Compete's Core Contract, unsourced claims are forbidden.

### 8. SYNTHESIZE — produce the requested artifact (artifact-driven merge)

Unlike Spark's Compete/Portfolio split, Compete's merge strategy is artifact-driven. The user's request determines the output shape; the engine-concurrence data is woven into whichever artifact is produced.

| Requested artifact | Merge approach | Engine-concurrence integration |
|--------------------|----------------|-------------------------------|
| **Feature Matrix** | Row per competitor, column per feature. Universal/Likely/Verified-Divergent rows mixed; group by category (direct → indirect → substitute → non-consumption). | Append `engine_concurrence` column with tag (`[codex+agy+claude]` etc.). Add a "Coverage" annotation row at the bottom: total UNIVERSAL / LIKELY / VERIFIED-DIVERGENT counts. |
| **Battle Card** | One-pager per competitor (or per top 3 competitors). | Add `engine_concurrence:` line in front matter. For VERIFIED-DIVERGENT competitors, add a "Why we didn't see this coming" callout explaining which engine surfaced it and what segment the other engines structurally missed — this is sales-enablement gold. |
| **Positioning Map** | 2-axis chart with competitors plotted; differentiation white-space called out. | Tag each plotted competitor with its coverage label as a marker style (e.g., filled = UNIVERSAL, half-filled = LIKELY, hollow-with-star = VERIFIED-DIVERGENT). |
| **SWOT** | Standard 2x2 per competitor (or aggregate SWOT of the competitive set). | For each Strength/Weakness/Opportunity/Threat cell, prefix items with engine tags. Threats sourced from VERIFIED-DIVERGENT competitors get a "structural blind-spot threat" prefix. |
| **Win/Loss Analysis** | Pair tri-engine competitor list against actual win/loss records. | UNIVERSAL competitors expected in win/loss data; VERIFIED-DIVERGENT competitors absent from win/loss data are a research gap — recommend interviews. |
| **LLM Brand Visibility** | Compare tri-engine output itself as a brand-visibility signal. | Brands that 3/3 engines surface have high AI share of voice; 1/3 brands have low AIV. Map this against the actual AIV measurement from `reference/intelligence-gathering.md`. |
| **Landscape Map** | Categorized competitor list with tiering. | Append `engine_concurrence` column; group VERIFIED-DIVERGENT competitors under a "Uncommon competitors (single-engine surfaced, grounded)" subsection — make them visible, not buried. |

**Universal output requirements (all artifacts):**

- Header: engine status summary (which engines ran, which failed, PREFLIGHT verdicts)
- Coverage distribution: `UNIVERSAL: N, LIKELY: N, VERIFIED-DIVERGENT: N`
- Rejection ledger (condensed): count by category (hallucination / defunct / category-mismatch / out-of-scope / alias-fold)
- **Uncommon Competitors callout** — a dedicated section that lists every `VERIFIED-DIVERGENT` competitor with: name, engine that surfaced it, why the other engines likely missed it (training-data bias hypothesis), and the structural blind-spot it patches. **This callout is the single most valuable deliverable of `multi` and must never be omitted.**
- Sources section: numbered URL list with access dates, per Compete's standard output requirement

### 9. DELIVER

Final output structure:

```markdown
# Competitive Analysis ({artifact_type}) — Tri-Engine

**Engines:** codex [{status}], agy [{status}], claude [{status}]
**Coverage:** UNIVERSAL: N, LIKELY: N, VERIFIED-DIVERGENT: N
**Rejected:** {count} ({top categories})

## {Primary Artifact — Feature Matrix / Battle Card / Positioning Map / SWOT / ...}

{Artifact content with engine_concurrence tags woven in}

## Uncommon Competitors (Verified-Divergent)

For each VERIFIED-DIVERGENT competitor:
- **{Name}** [{engine}-verified]
- Why other engines missed it: {training-data bias hypothesis}
- Structural blind-spot patched: {segment/geography/JTBD}
- Evidence: {URL with access date}
- Recommended action: {monitor / add to battle card / pursue win-back research / etc.}

## Sources

[1] ... — accessed YYYY-MM-DD
```

---

## Parallel Subagent Prompt Skeleton

Use the Agent tool three times **in the same message**. Each subagent prompt:

```
You are the {engine} competitive-analysis subagent for Compete.

# Role
Surface 5-10 competitors for the target below, spanning direct / indirect / substitute / non-consumption.
You are one of three engines working independently — do not try to be exhaustive across all segments;
surface the competitors your training data knows most confidently. Other engines will cover what you miss.

# Target
- Product / category: {scope}
- Decision question: {battle card / matrix / SWOT / positioning / etc.}
- Geographic / segment scope: {global / US / JP / enterprise / SMB / etc.}
- Time horizon: {current / 12-month / etc.}
- Known competitor seeds (already on our list, prioritize SURFACING ADDITIONS): {list or "none"}
- Existing signals: {Voice / Pulse / Field findings if any}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{JSON schema from §3}

# Constraints
- Name each competitor by its CANONICAL product/company name; include aliases separately
- Categorize each as direct | indirect | substitute | non-consumption — do not lump all into "direct"
- Surface competitors in segments YOUR training data knows well; do not fabricate competitors in segments you do not know
- For each competitor, name at least one strength AND one weakness (avoid pure marketing copy)
- If you assert a feature or pricing posture, base it on something your training data actually contains — do not invent
- Open with the deliverable (no completion preamble)
```

The three subagents return JSON; Compete main context handles NORMALIZE through DELIVER. Source-grounding via WebSearch happens at step 7 (GROUND) and is mandatory for every CANDIDATE / DIVERGENT cluster.

---

## Degraded Modes

| Situation | Behavior |
|-----------|----------|
| 1 engine binary missing | Run the other two; note reduced coverage breadth in header; CANDIDATE clusters from the single remaining engine require stricter grounding |
| 2 engines fail | Single-engine output; treat every competitor as CANDIDATE; ground all via WebSearch before reporting; flag reduced coverage and disable the "Uncommon Competitors" callout (no concurrence signal available) |
| All 3 fail | Abort multi mode; degrade to standard `matrix` Recipe with the Compete main context |
| User explicitly requests single engine | Skip fan-out; use standard analysis Recipe |
| Scope obviously trivial (e.g., "is X a competitor of Y") | Optionally skip multi; recommend single-engine `matrix` |
| WebSearch unavailable during GROUND | Mark all CANDIDATE clusters as `NEEDS-INFO`; do not ship as VERIFIED-DIVERGENT without source attribution |

---

## Why This Works for Competitive Analysis (Pattern D rationale)

- **Each engine's training data has structural coverage gaps that are knowable but invisible to that engine.** Codex over-indexes OSS / GitHub-published / dev-tool vendors; Antigravity over-indexes Google ecosystem / large-cap SaaS; Claude over-indexes diverse industries and AI-native players. A `VERIFIED-DIVERGENT` competitor surfaced by one engine is a real competitor that the other two were structurally blind to — not a low-confidence guess.
- **Concurrence (3/3) still filters obvious hallucinations.** When all three engines independently name the same competitor with overlapping features and positioning, the competitor is almost certainly real and well-known.
- **The Uncommon-Competitor callout is the load-bearing deliverable.** Sales teams losing deals to a competitor they cannot name benefit far more from "here is the competitor your CI program structurally missed" than from "here is one more line on the matrix you already knew."
- **Compete's anti-patterns (no surface-level metrics, no reaction-to-every-move, ethical sources only, source-attribution mandatory) apply at SYNTHESIZE/GROUND, not at FAN-OUT.** Letting engines run loose maximizes coverage; rule enforcement happens centrally.

---

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — base protocol (Pattern D scoring, PREFLIGHT, FAN-OUT, attribution conventions)
- `_common/SUBAGENT.md §MULTI_ENGINE` — engine dispatch, loose prompts, fallback rules
- `spark/reference/tri-engine-proposal.md` — canonical Pattern D sibling (ideation domain)
- `plea/reference/tri-engine-demand.md` — canonical Pattern D with calibration tags (synthetic demand domain)
- `compete/reference/intelligence-gathering.md` — WebSearch / WebFetch sources used during GROUND
- `compete/reference/battle-card.md` — Battle Card output format that absorbs engine_concurrence tags
- `compete/reference/analysis-templates.md` — Feature Matrix / SWOT output formats
- `compete/reference/competitive-moats-category-design.md` — Positioning Map output format
