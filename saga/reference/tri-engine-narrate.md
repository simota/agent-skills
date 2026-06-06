# Multi-Engine Narrative Generation

> **Filename retained** as `tri-engine-narrate.md` for backward compatibility. Covers both dual-engine baseline (Claude + Codex) and tri-engine optional (Claude + Codex + agy) modes.

Saga-specific delta for the `multi` Recipe. Run subagents in parallel — one per AVAILABLE engine — to generate independent narrative arcs (2 for dual-engine baseline, 3 for tri-engine) for the same customer + same feature, integrate across two axes (concurrence + divergence), and deliver either a Portfolio of complementary arcs (default) or a single Compete-merged narrative.

**Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT. dual-engine mode is NOT degraded. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Base protocol**: `_common/MULTI_ENGINE_RECIPE.md` (Pattern D — Divergence-Primary). This document only specifies what differs for Saga.

**Why three engines for narratives:** Each engine carries a different mix of narrative-archetype priors from its training data. Codex's GitHub-heavy corpus leans toward technical case-study/JTBD arcs; Antigravity's Google-product corpus leans toward Hero's Journey and Before→After product stories; Claude's Anthropic-curated corpus leans toward Promised Land and emotionally calibrated transformation arcs. Asking the same customer-feature pair across all three surfaces complementary archetypes — and the single-engine archetype the other two missed is often the most resonant narrative for a specific audience or channel.

---

## Pattern Type: D (Divergence-Primary)

- `UNIVERSAL` (3/3) = universally resonant story beat — safe, broadly empathetic, may be obvious
- `LIKELY` (2/3) = strong narrative with one dissenting archetype angle
- `VERIFIED-DIVERGENT` (1/3 grounded) = single-engine archetype that the other engines did not surface — often the most channel-fit narrative (e.g., only Antigravity surfaced a Failure-Redemption arc that fits a B2B case study)

**Merge default**: Portfolio (3 complementary arcs preserved). Compete-merge only on explicit user request — Saga's value is in offering multiple A/B/C-testable narratives, not in collapsing them into a single "winner".

---

## Flow

```
SCOPE → PREFLIGHT → FAN-OUT → NORMALIZE → CLUSTER → SCORE → GROUND → SYNTHESIZE → DELIVER
```

PREFLIGHT / FAN-OUT mechanics: identical to `_common/MULTI_ENGINE_RECIPE.md §3` (engine availability probe, three Agent calls in one message, loose prompts).

### 1. SCOPE

Single shared scope across all engines:

- **Customer / persona** (from Cast registry at `.agents/personas/registry.yaml` if available; otherwise concrete persona description — never "the user")
- **Feature or product** (the subject of the narrative — what the customer interacts with)
- **Target audience** (dev team / stakeholders / end users / cross-team — from AUDIENCE_UNCLEAR resolution)
- **Channel** (LP / pitch / case study / onboarding / social / investor memo — drives length and tone)
- **Controlling Idea** if known (StoryBrand 2.0 promised transformation) — pass through to engines so they don't drift off-brand
- **Materials** available (Voice quotes, Field journey maps, Compete differentiators, Trace session insights — if any)

Do **not** pass framework choice (SB7 / Pixar / Hero's Journey / JTBD / Promised Land / BAB) to subagents. Let each engine select the archetype its training data finds most fitting. Framework rules are applied at SYNTHESIZE.

### 2. PREFLIGHT

Per `_common/MULTI_ENGINE_RECIPE.md §2`. Probe `codex`, `agy`, `claude` in Saga main context only.

### 3. FAN-OUT

Three Agent calls in one message:

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `narrate-codex` | Codex CLI | `codex exec --full-auto "<prompt>"` |
| `narrate-agy` | Antigravity CLI | `agy -p "<prompt>" --dangerously-skip-permissions --log-file <path>` (silent-failure detection mandatory — see `_common/MULTI_ENGINE_RECIPE.md §3.5 Engine Runtime Failure Detection`) |
| `narrate-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

**Loose prompt rule**: pass only Role + Customer + Feature + Channel + Output format. Do **NOT** pass:
- the AP-1 through AP-9 anti-pattern checklist (Saga applies it at SYNTHESIZE)
- framework selection (let each engine choose its own archetype)
- length targets (let each engine self-size; Saga normalizes at SYNTHESIZE)

#### Required JSON output schema

```json
{
  "engine": "codex|agy|claude",
  "narratives": [
    {
      "arc_type": "Hero's Journey | JTBD | Before-After-Bridge | Failure-Redemption | Pixar Story Spine | Promised Land | StoryBrand SB7 | CAR | ABT | Quest | Rebirth",
      "protagonist": "Concrete named character (e.g., 'Mei, a 32yo solo accountant') — never 'the user'",
      "inciting_incident": "The specific moment/event that triggers the story (concrete scene with sensory detail)",
      "external_problem": "The tangible obstacle (what the customer cannot do today)",
      "internal_problem": "The emotional frustration (how it makes them feel)",
      "philosophical_problem": "Why it matters universally (the principle being violated)",
      "journey_beats": [
        "Beat 1: Ordinary world / context",
        "Beat 2: Stakes / tension introduced",
        "Beat 3: Discovery / mentor (the product as guide, not hero)",
        "Beat 4: Trial / first attempt",
        "Beat 5: Transformation / payoff"
      ],
      "resolution": "The Before→After transformation — concrete, observable, ideally measurable",
      "emotional_payoff": "Relief | Pride | Confidence | Belonging | Mastery | Vindication",
      "applicable_channel": ["LP", "case-study", "pitch", "onboarding", "social", "investor-memo"],
      "controlling_idea_alignment": "Free-text: how this narrative connects to the brand's promised transformation (if Controlling Idea was provided)",
      "narrative_body": "The actual narrative as deliverable prose, length appropriate to channel (200-2000 chars)"
    }
  ],
  "engine_notes": "Optional: which archetype this engine felt strongest authoring and why"
}
```

Each engine should produce **2-3 narratives** (different arc_types) per call — Saga's target is 6-9 raw narratives total before clustering.

If an engine returns free-form Markdown, ask its subagent to re-emit as JSON before integrating.

### 4. NORMALIZE

Parse three JSON blobs into a unified narrative list. Tag each with source engine. Preserve verbatim narrative_body wording per engine — divergent phrasing carries archetype signal.

### 5. CLUSTER — Saga-specific identity rules

Two narratives belong to the same cluster when **all three** hold:

- **same `protagonist`** (same persona name OR semantically equivalent persona description — "solo accountant Mei" and "freelance bookkeeper character" cluster only if they share the same job + same struggle context)
- **same `arc_type`** (Hero's Journey ≠ JTBD ≠ BAB; each archetype is its own cluster axis)
- **same emotional payoff class** (`Relief` and `Pride` are different payoffs; clustering across payoffs would erase the divergence signal)

**Critical Saga rule** (different from Spark/Plea): **Different `arc_type`s for the same protagonist are NOT clustered together — they are preserved as separate clusters.** Saga's whole value proposition is that three engines may apply three different archetypes (e.g., Codex → JTBD, Antigravity → Hero's Journey, Claude → Promised Land) to the same customer-feature pair. Collapsing across archetypes would destroy the Portfolio output.

Record the set of engines that produced each cluster.

### 6. SCORE — concurrence + archetype coverage

Per cluster:

| Engines in cluster | Concurrence label | Interpretation |
|--------------------|-------------------|----------------|
| 3 / 3 | `UNIVERSAL` | All three engines independently selected the same archetype for the same protagonist with the same emotional payoff. Strong universality — the most empathetic baseline narrative. Watch: may be the most obvious / least differentiated. |
| 2 / 3 | `LIKELY` | Two engines concur; one chose a different archetype. Note the dissenting archetype — it may be the more channel-fit alternative. |
| 1 / 3 | `CANDIDATE` (becomes `VERIFIED-DIVERGENT` after grounding) | Only one engine surfaced this archetype-protagonist combination. Either a high-resonance breakthrough or a weak/inauthentic arc. Must pass grounding. |

**Cross-cluster archetype coverage check** (Saga-specific addition): after per-cluster scoring, audit the surviving narratives for archetype diversity. Saga's Portfolio output should ideally cover **at least 3 distinct archetypes** across the chosen channels (e.g., one Hero's Journey for case study, one JTBD for dev team, one BAB for LP). If all 3 surviving clusters are the same arc_type, flag this — the Portfolio loses its core value (multiple A/B-testable arcs).

### 7. GROUND — verify CANDIDATE narratives (Saga main context, never delegated)

For each `CANDIDATE` narrative, the Saga main context must run the full **AP-1 through AP-9 anti-pattern audit** with rejection-code classification — both the check criteria and the `REJECTED-*` / `NEEDS-INFO` codes live in `reference/anti-patterns.md` (§"Rejection Categories"). Do not re-implement; use that table.

Also verify:
- **Persona existence**: if `protagonist` cites a Cast registry persona, confirm the persona exists. If fabricated, downgrade or mark `REJECTED-PERSONA-FABRICATED`.
- **Material grounding**: if the narrative references Voice quotes, Field findings, or Compete differentiators, verify the source. Hallucinated quotes → `REJECTED-FABRICATED-EVIDENCE`.

Surviving narratives become `VERIFIED-DIVERGENT` and are eligible for the Portfolio.

For `UNIVERSAL` and `LIKELY` clusters, run a lightweight AP-2 (Hero Product) and AP-9 (Ad Copy) spot-check only — three engines rarely produce the same persona-hero violation independently.

### 8. SYNTHESIZE — Portfolio (default) vs Compete

**Portfolio Merge (default)** — multiple complementary arcs preserved:

1. Keep all surviving `UNIVERSAL`, `LIKELY`, and `VERIFIED-DIVERGENT` clusters.
2. Target **3 narratives** for the deliverable (one per archetype if possible — e.g., one Hero's Journey, one JTBD, one BAB). Up to 5 if the user explicitly wants more A/B variants.
3. Order: `UNIVERSAL` first (the empathetic baseline), then `LIKELY` (strong with archetype variation), then `VERIFIED-DIVERGENT` (the channel-fit breakthrough).
4. Each narrative ships with: arc_type, protagonist, emotional_payoff, applicable_channel, full narrative_body, AP-1~AP-9 check results, engine-attribution tag.
5. Add a **Portfolio Rationale** section explaining which narrative fits which channel (e.g., "Use the Hero's Journey version for the customer case study LP; use the BAB version for the homepage hero; use the JTBD version for the dev-team feature page").
6. Output path: `docs/narratives/PORTFOLIO-[topic]-[date].md` (or inline if the user prefers no file).

**Compete Merge** (`multi --compete`, explicit only) — single best arc:

1. Rank surviving clusters by: `UNIVERSAL > LIKELY > VERIFIED-DIVERGENT`.
2. Within tier, rank by AP-checklist pass-rate (8/9 > 7/9), emotional payoff strength, and channel fit.
3. Select the top cluster.
4. **Re-mix the narrative_body** — take the best per-beat wording across the engines that contributed to this cluster (e.g., Codex's inciting incident phrasing + Antigravity's resolution arc + Claude's emotional payoff line).
5. Emit at `docs/narratives/NARRATIVE-[name].md` with `engine_concurrence` front matter.

**Engine-attribution tag (mandatory on every shipped narrative)**:

- `[codex+agy+claude]` — 3/3 UNIVERSAL
- `[codex+agy]` / `[codex+claude]` / `[agy+claude]` — 2/3 LIKELY
- `[codex-verified]` / `[agy-verified]` / `[claude-verified]` — 1/3 VERIFIED-DIVERGENT after grounding

### 9. DELIVER

Output structure follows `saga/SKILL.md §Output Requirements` (named framework, story elements, audience, AP check results, assumptions, framework citation, Before→After arc, success metrics, recommended next agent, handoff content) with these tri-engine additions:

- **Engine status line** in the header: which engines ran, which failed/unavailable
- **Concurrence distribution**: `UNIVERSAL: N, LIKELY: N, VERIFIED-DIVERGENT: N`
- **Archetype coverage line**: which arc_types are represented in the Portfolio (e.g., `Hero's Journey + JTBD + BAB`)
- **Rejection ledger** (condensed): count by category (no-arc / hero-product / no-tension / generic-persona / jargon / ad-copy / fabricated-evidence)
- **Per-narrative engine-attribution tag**
- **Portfolio rationale** (Portfolio merge only) — channel-fit mapping

Do not include rejected narratives in the main list. Do not surface engine-raw output.

---

## Parallel Subagent Invocation

Use the Agent tool three times **in the same message**. Each subagent receives a self-contained prompt:

```
You are the {engine} narrative subagent for Saga. You are one of three engines authoring narratives independently for the same customer-feature pair — surface what your training data suggests is the most resonant story arc.

# Role
Generate {N=2-3} narratives for the target customer and feature below. Each narrative must use a DIFFERENT arc_type (e.g., don't author three Hero's Journeys — pick three different archetypes your training data finds most fitting).

# Target
- Customer / persona: {persona description from Cast or inline}
- Feature / product: {what the customer interacts with}
- Target audience: {dev team | stakeholders | end users | cross-team}
- Channel: {LP | pitch | case study | onboarding | social | investor memo}
- Controlling Idea (if known): {brand's promised transformation}
- Available materials: {Voice quotes / Field findings / Compete differentiators / Trace insights — list, or "none"}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{JSON schema from §3 above}

# Constraints
- Customer is the hero; product is the guide (never the protagonist)
- Each narrative names a CONCRETE protagonist with context — never "the user"
- Include three problem levels: external (tangible), internal (emotional), philosophical (universal)
- Include a Before→After transformation with observable change
- Embed tension — no happy-path-only stories
- Do not write promotional copy — narrative voice, not ad voice
- Do not fabricate Voice quotes, customer names, or evidence; if you cite materials, they must come from the input
- Open with the deliverable (no completion preamble)
```

The three subagents return JSON; Saga main context handles NORMALIZE through DELIVER.

---

## Degraded Modes

Per `_common/MULTI_ENGINE_RECIPE.md §Degraded Modes`. Saga-specific notes:

- **1 engine down**: continue with 2; archetype coverage may drop to 2 distinct arc_types — flag in the rationale.
- **2 engines down**: single-engine output; Portfolio collapses to a single narrative; treat as `CANDIDATE` and run full AP-1~AP-9 grounding before shipping.
- **All 3 down**: degrade to standard `story` Recipe with Saga main context.
- **Trivial scope** (e.g., single-line social post): recommend `bab` or `story` Recipe instead — multi mode adds overhead without proportional value.

---

## Why This Works for Narratives (Pattern D Application)

- **Archetype priors differ across engines.** Codex (GitHub) leans technical-case-study/JTBD; Antigravity (Google) leans product-success Hero's Journey and BAB; Claude (Anthropic) leans Promised Land and emotionally calibrated transformations. Asking the same customer-feature pair across all three surfaces archetypes a single engine would not have chosen alone.
- **Concurrence reveals universal resonance.** When three engines independently land on the same arc_type for the same protagonist, that archetype is almost certainly the most empathetic baseline — but it may also be the most obvious. The Portfolio surfaces both the safe bet AND the channel-fit alternatives.
- **Divergence is the Portfolio's whole point.** Saga's deliverable is not a single best story — it is a set of A/B/C-testable arcs aligned to different channels. The single-engine archetype (e.g., only Antigravity surfaced a Failure-Redemption arc) is often the most resonant for a specific case study; Portfolio merge preserves it.
- **AP-1~AP-9 enforcement happens centrally.** Letting engines run loose maximizes archetype diversity; the anti-pattern audit at SYNTHESIZE filters out feature dumps, hero-product violations, jargon walls, and ad-copy disguises.

---

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — base protocol (canonical flow, PREFLIGHT, FAN-OUT, scoring axes, attribution rules)
- `_common/SUBAGENT.md §MULTI_ENGINE` — engine dispatch, loose-prompt rules
- `saga/reference/frameworks.md` — archetype definitions (SB7, Pixar, Hero's Journey, JTBD, Promised Land, CAR, BAB, ABT) applied at SYNTHESIZE
- `saga/reference/templates.md` — per-channel narrative templates used when normalizing length
- `saga/reference/examples.md` — example narratives for AP-1~AP-9 calibration during GROUND
- `spark/reference/tri-engine-proposal.md` — sibling Pattern D implementation (Portfolio/Compete merge precedent)
- `plea/reference/tri-engine-demand.md` — sibling Pattern D with persona-channel diversity (closest analog to Saga's archetype diversity)
