# Multi-Engine Demand Generation

> **Filename retained** as `tri-engine-demand.md` for backward compatibility. Covers both dual-engine baseline (Claude + Codex) and tri-engine optional (Claude + Codex + agy) modes.

Default flow for `/plea multi`. Run subagents in parallel — one per AVAILABLE engine — to generate synthetic user demands across the same persona set, integrate results across two axes (concurrence + divergence), and deliver a Demand Report that preserves both universal pain points AND engine-specific blind-spot fills.

**Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) only when AVAILABLE at PREFLIGHT. Dual-engine mode is NOT degraded — persona-voice divergence comes from independent channeling of the same persona by 2 engines with non-overlapping training-data priors (Claude's empathy-curated corpus + Codex's GitHub-issue-driven complaint patterns). See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Pattern**: D (Divergence-primary) per `_common/MULTI_ENGINE_RECIPE.md`. Divergent single-engine demands are NOT auto-low-value — they often surface the silent-majority insight that the other engines' persona-channeling priors smoothed over.

**Why three engines for synthetic demand (different from Judge):** Judge optimizes for *agreement on a single defect* — concurrence is the quality signal. Plea optimizes for *authentic user voice from diverse persona perspectives* — concurrence reveals universal unmet needs (high-confidence demands), but divergence reveals engine-specific persona-channeling angles. Each engine has different priors about how a "beginner" or "accessibility-dependent user" actually thinks; the breakthrough demand often comes from the engine that channels the persona most distinctively.

**Adapted from `judge/reference/tri-engine-review.md`. Re-uses PREFLIGHT and FAN-OUT mechanics; replaces SCORE/GROUND/FILTER with Concurrence-Divergence Scoring and Synthesis that preserves persona-voice fidelity.**

---

## Flow

```
SCOPE → CAST → PREFLIGHT → FAN-OUT (parallel subagents) → NORMALIZE → CLUSTER → SCORE (concurrence + divergence) → CALIBRATE → SYNTHESIZE → DELIVER
```

### 1. SCOPE

Define the demand-generation target once. All three subagents share the same scope:

- Product / feature surface
- Generation mode (EXPLORE / DEEP / CHALLENGE / COMPETE / EDGE) per `reference/mode-playbooks.md`
- Existing roadmap or assumptions to challenge (if any)
- Discovery evidence (Voice findings, Trace observations, Field data — if present, for calibration)

### 2. CAST — persona selection (shared across engines)

Select **at least 3 personas** spanning at least 2 axes of the Persona Diversity Matrix. **All three engines work with the same persona set** — the divergence comes from how each engine channels those personas, not from different persona pools.

- Prefer Cast registry at `.agents/personas/registry.yaml` if available.
- When Cast is absent, generate proto-personas internally under AI persona guardrails (`_common/AI_PERSONA_RISKS.md`) and cap their confidence at 0.50.
- Fill the `PERSONA_CHANNEL` template for each before FAN-OUT (per `reference/persona-embodiment.md`).

### 3. PREFLIGHT — engine availability detection (Plea main context, never delegated)

Detect engine availability **once in the main Plea context** before spawning subagents. Subagent PATH is narrower than the user's interactive shell; never delegate availability detection.

Use the combined preflight from `judge/reference/tri-engine-review.md §2`. The probe order is identical for `codex`, `agy`, `claude`.

Availability verdict and "never declare unavailable based on..." rules: identical to Judge tri-engine PREFLIGHT.

### 4. FAN-OUT — parallel subagents

Spawn **three Agent calls in a single message** so they run concurrently. Each subagent receives the **same persona set** but channels them independently. Each engine has different priors about how each persona expresses frustration — this is the source of valuable divergence.

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `demand-codex` | Codex CLI | `codex exec --full-auto "<prompt>"` |
| `demand-agy` | Antigravity CLI | `agy -p "<prompt>" --dangerously-skip-permissions --log-file <path>` (silent-failure detection mandatory — see `_common/MULTI_ENGINE_RECIPE.md §3.5 Engine Runtime Failure Detection`) |
| `demand-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

**Loose prompt rule (per `_common/SUBAGENT.md` MULTI_ENGINE)**: pass only Role + Persona-channel block + Target product + Output format. Do NOT pass the Plea "curse of knowledge" table, JTBD templates, or assumption-challenge taxonomies — those Plea-specific frames are applied at SYNTHESIZE. Each engine channels persona voice in its own way.

**Required JSON output schema:**

```json
{
  "engine": "codex|agy|claude",
  "demands": [
    {
      "persona_id": "Persona name or archetype (must match input)",
      "scene": "When, where, what they were doing when the need arose",
      "user_voice_verbatim": "First-person request in the persona's own words (preserve emotion, specificity, jargon-avoidance)",
      "why_this_matters": ["user-context reason 1", "user-context reason 2"],
      "acceptance_criteria": ["criterion 1 in user perspective", "criterion 2"],
      "current_emotion": "Frustration|Resignation|Tolerance|Unaware",
      "post_fulfillment_emotion": "Relief|Joy|Surprise|Obvious",
      "urgency": "Daily pain|Weekly inconvenience|Occasional thought",
      "competitor_anchor": "Optional: competitor experience this demand draws on (COMPETE mode)"
    }
  ],
  "blind_spots_surfaced": ["assumption the team likely holds that this demand counters", ...],
  "engine_notes": "Optional: which persona this engine felt strongest channeling and why"
}
```

If an engine is genuinely unavailable per PREFLIGHT criteria, record the failure and proceed with remaining engines. Below two engines, downgrade to single-engine output and flag reduced persona-voice diversity.

### 5. NORMALIZE

Parse the three JSON blobs into a unified demand list. Tag each demand with its source engine **and** its persona. Demand identity in Plea is `(persona, demand-essence)` — the same persona can have multiple demands, and the same demand-essence can surface across personas. If an engine returns free-form Markdown, ask its subagent to re-emit as JSON before integrating.

### 6. CLUSTER — dedup across engines

Group demands that describe the same unmet need. Two demands match when **all three** hold:

- same `persona_id` (or semantically equivalent persona — beginner-A and beginner-B count as same)
- same or overlapping `why_this_matters` (the underlying need, not the surface request — "want to bulk-edit tags" and "want to apply tags to many items at once" cluster together)
- same emotional valence (`current_emotion`) — a "Frustration" demand and a "Tolerance" demand about the same surface feature are different signal levels, not duplicates

**Critical rule:** Do NOT cluster across personas. Demand X from persona-A and demand X from persona-B are *separate* — the fact that two personas independently voice the same need is a cross-persona signal that SYNTHESIZE surfaces, not a deduplication target.

Record the set of engines that voiced each cluster (within the same persona).

### 7. SCORE — concurrence + divergence (the key difference from Judge)

Plea scores each cluster on **two axes within each persona**, plus a third axis across personas:

#### Per-cluster (within persona):

| Engines in cluster | Concurrence label | Divergence label | Interpretation |
|--------------------|-------------------|------------------|----------------|
| 3 / 3 | `UNIVERSAL-DEMAND` | none | All engines channeled this persona to the same unmet need — high-confidence synthetic demand. May still be synthetic-only; calibration against real Voice/Trace data is needed before treating as validated. |
| 2 / 3 | `LIKELY-DEMAND` | mild | Two engines concur; one missed it — note the missing engine's silence (it may have channeled the persona differently). |
| 1 / 3 | `CANDIDATE-DEMAND` | `DIVERGENT-VOICE` | Only one engine surfaced this for the persona. Either a unique angle from that engine's training data OR an artifact of weak persona channeling. Must pass calibration (step 8) to survive. |

#### Cross-persona signal (new in tri-engine Plea):

After per-cluster scoring, also identify demands that surfaced across multiple personas:

- `CROSS-PERSONA-UNIVERSAL`: ≥2 personas voiced this demand, AND it was `UNIVERSAL-DEMAND` or `LIKELY-DEMAND` in each of those persona clusters. Strongest signal — broadly felt unmet need.
- `PERSONA-SPECIFIC`: Demand surfaced for exactly one persona. Persona-specific insight; do not generalize.

**Critical rule for Plea (does NOT exist in Judge):** `DIVERGENT-VOICE` demands are not automatically lower-quality than `UNIVERSAL-DEMAND` demands. The "silent majority" demand or the unspoken assumption is often surfaced by exactly one engine, because the other two engines smoothed over the same persona's quirks. Preserve all `DIVERGENT-VOICE` clusters through SYNTHESIZE.

#### Negative concurrence (the multi-only subtraction signal):

Presence-concurrence (above) ranks demands that *appeared*. **Absence-concurrence** is a signal only multi can produce: when independent engines, channeling the same persona at the same feature surface, **all fail to surface a compelling demand**, that silence is evidence — not a gap to fill.

- `NO-DEMAND-CONSENSUS`: all AVAILABLE engines produced **zero** `Frustration`/`Resignation`-valence demands for a feature area the scope expected to be painful. Strong **don't-build / already-adequate / non-need** signal — the curb-cut equivalent of subtraction. Surface as a don't-build candidate, never silently drop.
- Caveat: absence can also mean all engines share the same blind spot (correlated WEIRD/mode-collapse bias). Distinguish "engines agree it's fine" from "engines all can't imagine this persona" — if the persona's `last_frustration`/`unspoken_assumption` was rich but no demand emerged, suspect shared bias and flag for Field, don't conclude non-need.

### 8. CALIBRATE — verify CANDIDATE/DIVERGENT demands (Plea main context, never delegated)

For every `CANDIDATE-DEMAND / DIVERGENT-VOICE` cluster, the Plea main context must:

1. **Persona-voice authenticity check** — does the `user_voice_verbatim` actually sound like the named persona? Or does it slip into developer/PM language? If inauthentic, mark `REJECTED-VOICE-MISMATCH`.
2. **Acceptance-criteria specificity check** — are the criteria in user perspective (not implementation perspective)? Vague criteria ("works well") fail; specific behaviors pass.
3. **Curse-of-knowledge check** — does this demand challenge a likely team assumption? If yes, flag for `Questions for the Team` section.
4. **Real-data calibration** — if Voice / Trace / Field data is available in the project (e.g., `.agents/voice.md`), cross-check whether the synthetic demand aligns with real signals. Apply the confidence tags from `reference/calibration.md`:
   - `[validated]` — synthetic demand matches real Voice/Trace/Field evidence
   - `[supported]` — partial evidence (one source agrees, others silent)
   - `[hypothesis]` — no real-data conflict, no real-data support
   - `[synthetic-only]` — no real-data sources available
5. **Feasibility-filter check** — confirm no demand was dropped because it "seemed hard to build." Users don't price implementation; feasibility-filtering is forbidden (count must be 0 in the rejection ledger). Aligns with the single-engine self-rejection gate (`reference/patterns.md`).
6. **Mark each as** `VERIFIED-DIVERGENT` (keep with confidence tag), `REJECTED-{reason}` (drop), or `NEEDS-INFO` (escalate — ask the user).

For `UNIVERSAL-DEMAND` and `LIKELY-DEMAND` clusters, apply only the persona-voice authenticity check and the real-data calibration tag. Three engines rarely channel the same persona inauthentically in the same way.

**Validate-first priority (riskiest-first family):** after calibration, name the **load-bearing demand** — the demand whose validation status, if flipped, most changes the roadmap (typically a high-urgency `CROSS-PERSONA-UNIVERSAL` still tagged `[hypothesis]`/`[synthetic-only]`). Field validates this first. Mirrors `jtbd` `riskiest_force` / `5whys` `weakest_link` / `opportunity` load-bearing opportunity.

### 9. SYNTHESIZE — Demand Report structure

Plea's multi-engine output keeps **persona as the primary axis** and **engine concurrence as the secondary axis**, the opposite of Judge's "by severity" structure. This is because Plea's value is in persona-voice diversity, not in defect ranking.

Synthesis steps:

1. **Per persona**: list demands ranked by concurrence × urgency × emotion. Within each persona, show `UNIVERSAL-DEMAND` first, then `LIKELY-DEMAND`, then `VERIFIED-DIVERGENT-VOICE`.
2. **Cross-persona analysis**: list `CROSS-PERSONA-UNIVERSAL` demands as the top-priority section. These are the strongest synthetic signals.
3. **Persona-specific demands**: list `PERSONA-SPECIFIC` demands grouped by persona, with a one-line note on why only that persona notices.
4. **Engine-channeling notes**: a brief section noting which engine channeled which persona most distinctively, surfaced from the engines' optional `engine_notes` field. Useful for next-session persona prep.
5. **Assumption challenges**: aggregate from all three engines' `blind_spots_surfaced` fields. Deduplicate; flag the strongest 3-5 as `Questions for the Team`.
6. **Don't-build candidates** (multi-only): list `NO-DEMAND-CONSENSUS` areas — feature surfaces where all engines were silent. Mark each as **don't-build / already-adequate** or **shared-bias-suspect** (per the negative-concurrence caveat). This is the subtraction signal single-engine cannot produce.
7. **Rejection ledger** (condensed): count and categories of rejected demands (voice-mismatch / criteria-vague / persona-fabricated / **feasibility-filtered — must be 0**) — preserves transparency without noise.

#### Engine-attribution rule

Every demand that ships must carry both an `engine_concurrence` tag AND a calibration confidence tag:

- `[codex+agy+claude] [validated]` — strongest signal: 3/3 concurrence + real-data validation
- `[codex+agy] [supported]` — 2/3 concurrence + partial real-data support
- `[claude-verified] [hypothesis]` — 1/3 verified divergent voice + no conflicting real data
- `[claude-verified] [synthetic-only]` — 1/3 verified divergent voice + no real-data available for calibration

### 10. DELIVER — output structure

Output structure follows the existing Plea Demand Report template (`plea/SKILL.md §Output Format`) with these tri-engine additions:

- **Header summary table** gains engine-status line and concurrence stats (`UNIVERSAL: N / LIKELY: N / VERIFIED-DIVERGENT: N / CROSS-PERSONA: N`)
- **Cross-Persona Analysis** section is mandatory in multi mode (single-engine mode treats it as optional)
- **Per-demand `LLM Instruction Prompt`** still applies — verb selection per `plea/SKILL.md §LLM Instruction Prompt Generation`. Each per-request prompt embeds the demand's engine_concurrence and calibration tags so downstream agents (Spark, Scribe, Builder) know whether they are acting on a 3/3-validated demand or a 1/3-divergent hypothesis.
- **Per-report `LLM Orchestration Prompt`** at the bottom — adapted to mention the tri-engine origin and the calibration distribution.

Do not include rejected demands in the main list. Do not surface engine-raw output. Synthetic-true tagging applies to every demand unless calibration upgraded it to `[validated]`.

---

## Parallel Subagent Invocation

Use the Agent tool three times **in the same message** for genuine parallel execution. Each subagent receives a self-contained prompt:

```
You are the {engine} demand subagent for Plea. You channel synthetic user voice — speak AS the persona, not ABOUT the persona.

# Role
For each persona below, generate {N=2-4} feature demands in first-person voice. You are one of three engines channeling the same personas independently. Express the persona as your training data suggests they would actually speak; do not smooth out their quirks.

# Personas
{PERSONA_CHANNEL blocks from CAST step — full template per persona including last_frustration, unspoken_assumption, daily_context, current_emotion}

# Target
- Product / feature surface: {scope}
- Mode bias: {EXPLORE | DEEP | CHALLENGE | COMPETE | EDGE — per `reference/mode-playbooks.md`}
- Roadmap / assumptions to challenge: {if CHALLENGE mode}
- Competitor anchor: {if COMPETE mode}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{JSON schema}

# Constraints
- Speak in FIRST PERSON as the persona ("I", "my", "me") — never developer/PM voice
- Preserve emotional specificity — frustration sounds different from resignation
- Include daily-context scenes (when/where/what they were doing) — not abstract requests
- Do not paraphrase out the user's emotion; quote the persona verbatim
- Avoid jargon the persona would not actually use
- Do not filter demands by technical feasibility — users do not know implementation cost
- Surface at least one assumption the team likely holds (in `blind_spots_surfaced`) per persona
```

The three subagents return JSON; Plea main context handles NORMALIZE through DELIVER.

---

## Degraded Modes

| Situation | Behavior |
|-----------|----------|
| 1 engine binary missing | Run the other two; note reduced persona-voice diversity; `CANDIDATE-DEMAND / DIVERGENT-VOICE` clusters from the single remaining engine require stricter calibration |
| 2 engines fail | Single-engine output; treat every demand as `CANDIDATE-DEMAND`; calibrate all before reporting; flag reduced confidence; loud `synthetic-only` tag |
| All 3 fail | Abort tri-engine flow; degrade to standard `request` Recipe with the Plea main context |
| User explicitly requests single engine | Skip fan-out; use standard `request` Recipe |
| Fewer than 3 personas available | Multi mode still runs but with the same persona pool — flag persona-representativeness as a risk per `reference/calibration.md` |

---

## Mode Modifier Interaction

The `multi` Recipe is **compatible with `COMPETE` and `EDGE` mode modifiers**:

- `multi --mode=COMPETE` — all three engines channel personas with competitor anchors. Strong for surfacing "App X already does this" demands with multi-engine cross-validation.
- `multi --mode=EDGE` — all three engines focus on minority/extreme personas (accessibility, regulated industries, fringe). Strong for surfacing demands that no single engine alone would prioritize.

When combining `multi` with `CHALLENGE` mode, the engines independently counter the same roadmap assumptions — divergence here is especially valuable because each engine attacks the assumptions from different angles.

---

## Why This Works for Synthetic Demand (different from Judge)

- **Persona-channeling priors differ across engines.** Codex, Antigravity, and Claude have different training-data exposure to how "beginners," "power users," or "accessibility-dependent users" actually speak. Three independent channelings of the same persona surface more authentic voice diversity than a single engine ever could.
- **Concurrence still filters obviously inauthentic voices.** When three engines independently channel the same persona to the same unmet need, that demand almost certainly reflects a real friction class — though synthetic-vs-validated calibration still applies.
- **Divergence preserves the "silent majority" insight.** The most valuable Plea demand is often the one no team member noticed — surfaced by exactly one engine, because the other two engines unconsciously smoothed over the persona's quirks. Tri-engine flow makes this divergence visible instead of averaging it out.
- **Cross-persona signals are stronger in tri-engine mode.** A demand that surfaces across 3 personas × 3 engines (9 independent voices) is one of the strongest synthetic signals Plea can produce — call it out as a `CROSS-PERSONA-UNIVERSAL`.
- **AI-persona bias risks (mode-collapse, WEIRD, over-sanitization per `_common/AI_PERSONA_RISKS.md`) are partially mitigated by tri-engine.** Different engines have different bias profiles; their disagreement reveals where any single engine is collapsing. Still tag synthetic-true unless calibrated against real data.

---

## Cross-References

- `_common/SUBAGENT.md §MULTI_ENGINE` — base protocol for engine dispatch and loose prompts
- `_common/AI_PERSONA_RISKS.md` — persona-bias guardrails (still apply in multi mode, per engine)
- `judge/reference/tri-engine-review.md` — sibling tri-engine flow (review domain); PREFLIGHT and FAN-OUT logic mirrored here
- `plea/reference/persona-embodiment.md` — PERSONA_CHANNEL template fed into FAN-OUT
- `plea/reference/calibration.md` — confidence tagging applied at CALIBRATE step
- `plea/reference/mode-playbooks.md` — Mode Modifier semantics (COMPETE / EDGE / CHALLENGE compatibility)
- `plea/SKILL.md §LLM Instruction Prompt Generation` — per-request and per-report prompt generation rules
