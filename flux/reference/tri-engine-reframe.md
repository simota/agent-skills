# Multi-Engine Reframe Generation

Shared engine selection, capability/authorization gates, dispatch, capture, attribution and degraded-mode policy: `_common/MULTI_ENGINE_RECIPE.md` and `_common/CLI_COMPATIBILITY.md`. This reference defines only the domain payload and integration rules.

Default flow for `/flux multi`. Run subagents in parallel — one per AVAILABLE engine — to produce **assumption inversions and cross-domain reframes**, then synthesize a *Portfolio of divergent perspective shifts*.

**Consequence**: In Flux's `multi` Recipe, `VERIFIED-DIVERGENT` reframes (surfaced by exactly one engine) are the **most valuable** outputs — they represent perspective shifts structurally unreachable by the other two engines. This inverts Judge's scoring polarity. Flux ships divergence first, concurrence second.

---

## Flow

```
SCOPE → PREFLIGHT → FAN-OUT (parallel subagents) → NORMALIZE → CLUSTER → SCORE (novelty × concurrence) → GROUND → SYNTHESIZE (portfolio) → PRESENT
```

PREFLIGHT, FAN-OUT, NORMALIZE follow the canonical Pattern D protocol in `_common/MULTI_ENGINE_RECIPE.md`. The Flux-specific differences are in **CLUSTER, SCORE, GROUND, SYNTHESIZE** below.

### 1. SCOPE

Define the reframe target once. All selected subagents share the same scope:

- **Stuck problem statement** (verbatim user framing — the thing being reframed)
- **Evidence of stuck-ness** (what was tried, why it didn't work, where thinking loops)
- **Visible constraints** (real boundaries) vs. **assumed constraints** (boundaries to challenge)
- **Cynefin domain** if already classified (Clear / Complicated / Complex / Chaotic / Disorder)
- **Reframe axis preference** if user specified one (assumption-inversion / cross-domain / perspective-rotation / all)

Do NOT pass framework names (Bisociation, SCAMPER, TRIZ, Oblique Strategies) to subagents — those are tools Flux main context uses at SYNTHESIZE. The point of `multi` is to let each engine's training-data priors produce *its own* reframes, not to make three engines run the same framework.

### 2. PREFLIGHT

Identical to `_common/MULTI_ENGINE_RECIPE.md §2`. Run engine availability detection in Flux main context. Never delegate to subagents.

### 3. FAN-OUT — parallel subagents

Dispatch one independent task per selected, authorized engine using the shared CLI adapter; join the actual results before synthesis.

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `reframe-codex` | Codex CLI | Authorized invocation via `_common/CLI_COMPATIBILITY.md` |
| `reframe-agy` | Antigravity CLI | Authorized headless/native dispatch → `_common/CLI_COMPATIBILITY.md` §9; validate outputs under `_common/MULTI_ENGINE_RECIPE.md` §3.5 |
| `reframe-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

**Loose prompt rule**: pass only Role + Target + Output format. Do NOT pass Cynefin classification rules, framework taxonomies, or ASN-test criteria — those apply at SYNTHESIZE. Each engine should freely produce reframes from its own implicit priors.

**Required JSON output schema** (Flux-specific):

```json
{
  "engine": "codex|agy|claude",
  "reframes": [
    {
      "original_assumption": "The hidden premise being challenged (verbatim or paraphrased from the stuck problem)",
      "inverted_form": "The assumption reversed, negated, or restructured (the actual reframe)",
      "cross_domain_source": "Domain/discipline the inversion borrows from (e.g., 'epidemiology', 'theatre direction', 'cooking') — null if pure first-principles inversion",
      "perspective_shift": "What changes about the observer's vantage point (e.g., 'from operator to user', 'from cost to constraint', 'from solved to dissolved')",
      "applicability": "One concrete next-step action this reframe makes available that was NOT available under the original framing",
      "novelty_self_score": 1-5,
      "discomfort_self_score": 1-5,
      "reframe_class": "ASSUMPTION-INVERSION | CROSS-DOMAIN-BISOCIATION | PERSPECTIVE-ROTATION | CONTRADICTION-RESOLUTION | TIME-FRAME-SHIFT | SCALE-SHIFT"
    }
  ],
  "engine_notes": "Optional: what bias/strength this engine knows it brings — useful for downstream interpretation"
}
```

Target 4-6 reframes per engine. Quality over quantity — engines should err toward fewer-but-bolder rather than padding.

### 4. NORMALIZE

Parse the usable JSON outputs into a unified reframe list. Tag each reframe with its source engine. **Preserve per-engine wording verbatim** — in Flux, the *phrasing* of a reframe is part of its perspective-shift value (Oblique Strategies-style provocation is wording-sensitive).

### 5. CLUSTER — Flux-specific identity rules

This is where Flux diverges most from Spark/Judge. Standard CLUSTER deduplicates outputs that "say the same thing." For Flux, **two reframes targeting the same `original_assumption` but with different `inverted_form` are kept as SEPARATE clusters**, not merged.

**Rationale**: A single assumption can be inverted along multiple axes (negation, scale-shift, time-shift, observer-shift). When two engines invert the same assumption *differently*, both inversions are valuable divergent perspectives — merging them collapses the divergence Flux is paid to surface.

**Identity rules (refined for reframes)**:

Two reframes are the same cluster only when **all three** hold:

1. Same `original_assumption` (semantically — paraphrase tolerant)
2. **Same `inverted_form` direction** (e.g., both negate the same premise to the same polarity, not just both touch the same premise)
3. Same `applicability` class (same next-step action shape)

If two engines independently produce *the same inversion direction* on *the same assumption* with *the same downstream action*, that's a true cluster — and surprisingly strong, because two independent training-data corpora converged on it.

If two engines invert the same assumption *differently* (e.g., one negates, one scale-shifts, one time-shifts), keep all of them as **separate clusters tagged with a shared `assumption_root`**. The Portfolio output groups them under one assumption heading but lists each inversion separately.

Record the set of engines that produced each cluster. Preserve per-engine wording variations within a cluster as alternative phrasings (useful for Serendipity Injection-style provocations).

### 6. SCORE — novelty × concurrence (the key Flux difference)

Flux scores each cluster on **two independent axes**:

#### Axis A: Concurrence (how many engines reached this reframe)

| Engines | Concurrence label | Default interpretation |
|---------|-------------------|-------------------------|
| 3 / 3 | `UNIVERSAL` | Three independent priors converged. Strong inversion, but watch for "training-data common ground" — could be the *obvious* reframe everyone has already considered |
| 2 / 3 | `LIKELY` | Two engines concur, one missed it — check whether the missing engine surfaced an alternative inversion of the same assumption |
| 1 / 3 | `CANDIDATE` (provisional, awaits GROUND) | Single-engine reframe. Either a structurally unreachable insight from that engine's training data OR a low-quality random output |

#### Axis B: Novelty (how far the reframe is from the original framing)

Compute from `novelty_self_score`, `discomfort_self_score`, and the reviewer's own assessment of *how much new action surface* the `applicability` field opens:

| Novelty tier | Marker | Criteria |
|--------------|--------|----------|
| `HIGH` | breakthrough candidate | Opens ≥2 concrete actions unavailable under original framing; crosses ≥1 domain boundary; passes ASN test on Actionability+Specificity+Novelty all strongly |
| `MEDIUM` | useful pivot | Opens 1 new action; passes ASN test |
| `LOW` | restatement | Reframes wording without changing action surface — **drop at GROUND** (fails ASN-Novelty) |

#### Combined verdict (the Flux scoring rule)

| Concurrence × Novelty | Verdict | Priority in Portfolio |
|-----------------------|---------|----------------------|
| `UNIVERSAL × HIGH` | strong inversion | High — but check for "already considered" |
| `UNIVERSAL × MEDIUM` | safe restatement | Medium — include if it consolidates the obvious |
| `UNIVERSAL × LOW` | drop | — (synonym-substitution) |
| `LIKELY × HIGH` | strong with one dissenter | High — note what the missing engine surfaced instead |
| `LIKELY × MEDIUM` | useful | Medium |
| `LIKELY × LOW` | drop | — |
| `VERIFIED-DIVERGENT × HIGH` | **breakthrough — top-billing** | **Highest — these are reframes structurally unreachable by 2/3 of the engines** |
| `VERIFIED-DIVERGENT × MEDIUM` | unique angle | High — worth surfacing even at medium novelty because the engine reached it alone |
| `VERIFIED-DIVERGENT × LOW` | drop | — (single-engine restatement is just a random guess) |

**Critical Flux rule (does NOT exist in Judge, stronger than Spark)**: `VERIFIED-DIVERGENT × HIGH` reframes occupy the **top section** of the Portfolio output, ahead of `UNIVERSAL` reframes. Flux's entire premise is that breakthrough perspective shifts come from outside the consensus prior; the multi-engine recipe makes that operational by treating single-engine divergence as a feature, not a defect.

### 7. GROUND — verify CANDIDATE / VERIFIED-DIVERGENT reframes (Flux main context, never delegated)

For every `CANDIDATE` cluster, Flux main context must run the **ASN test** (Actionability / Specificity / Novelty) plus three Flux-specific checks:

1. **ASN gate** — does the reframe pass A (suggests concrete next step), S (applies to THIS problem not any problem), N (not a synonym of the original framing)? Fail any one → `REJECTED-ASN`.
2. **Hallucinated-domain check** — if `cross_domain_source` is cited (e.g., "in epidemiology, X"), verify the cited domain fact is plausibly real. AI engines can hallucinate cross-domain analogies. If the cited mechanism doesn't exist in the cited domain, the reframe is built on sand → `REJECTED-HALLUCINATION`. Note: Flux does not require deep verification — plausible-to-an-expert is enough; the reframe's value is the *perspective shift*, not the literal analogy.
3. **Synonym-substitution check** — does the reframe just rewrite the original framing in different words without changing the action surface? "Reduce costs" → "minimize expenses" fails this. → `REJECTED-SYNONYM` (a subclass of `REJECTED-ASN`).
4. **Bias-blind-spot check** — does this reframe inherit the *same* bias as the original framing? (E.g., if the original framing assumes "users are rational actors" and the reframe also assumes rational actors, the reframe didn't actually challenge the underlying premise.) → `REJECTED-BIAS-INHERITED`.
5. **Mark each as** `VERIFIED-DIVERGENT` (keep — promote to top-billing if novelty is HIGH), `REJECTED-{reason}` (drop), or `NEEDS-INFO` (escalate to user).

For `UNIVERSAL` and `LIKELY` clusters, run ASN + bias-blind-spot only — hallucinated-domain is unlikely when three engines independently converge.

### 8. SYNTHESIZE — Portfolio-only by default (Compete merge is anti-pattern for Flux)

Flux's `multi` Recipe defaults to **Portfolio merge with no Compete option**. The whole purpose of multi-engine reframing is to preserve divergence; collapsing three engines' perspectives into "one best reframe" reintroduces the consensus prior that Flux exists to break.

**Compete merge is offered only on explicit user request** (e.g., `multi --compete`) and even then Flux preserves the alternative reframes in an appendix, because in reframing work the "second-best" perspective often becomes the breakthrough once the user encounters the problem in a new context.

#### Portfolio Output Structure

Single document at `docs/reframes/PORTFOLIO-[topic]-[date].md` (or inline if user did not request a file):

1. **Header**: stuck problem statement (verbatim), Cynefin classification, engines that ran successfully, concurrence distribution (`UNIVERSAL: N, LIKELY: N, VERIFIED-DIVERGENT: N`)
2. **Top-billing section — `VERIFIED-DIVERGENT × HIGH`**: each reframe with full schema fields, the engine that produced it tagged as `[<engine>-verified]`, and an explicit "Why this perspective is structurally unreachable by the other engines" line
3. **High-confidence section — `UNIVERSAL × HIGH` and `LIKELY × HIGH`**: each reframe with engine-concurrence tag `[codex+agy+claude]` / `[codex+agy]` etc.
4. **Supporting section — MEDIUM novelty across all concurrence tiers**: useful pivots that don't break new ground but consolidate the reframe space
5. **Assumption Map**: cross-engine view organized by `assumption_root` — for each root assumption, list all inversions found, grouped under that root (this is where the "same assumption inverted differently" structure becomes visible)
6. **Blind Spot Report**: detected biases in the original framing + the bias-blind-spot audit of Flux's own output (per Flux Core Contract)
7. **Rejection ledger**: count by category (ASN-fail / hallucinated-domain / synonym-substitution / bias-inherited) — preserves transparency
8. **Recommended next step**: which 1-2 reframes Flux suggests pursuing first, and why (engine reasoning + concurrence reasoning + novelty reasoning). If user follow-up is `Magi`, Flux flags the top reframes as decision inputs. If follow-up is `Spark` or `Atlas`, Flux flags reframes most likely to seed downstream ideation/architecture.

#### Engine-attribution tag (mandatory on every shipped reframe)

- `[codex+agy+claude]` — 3/3 UNIVERSAL
- `[codex+agy]` (or any 2-engine combo) — 2/3 LIKELY
- `[codex-verified]` / `[agy-verified]` / `[claude-verified]` — 1/3 VERIFIED-DIVERGENT after grounding

For DIVERGENT reframes, append a second tag explaining *why divergence is informative here*: `[divergent: cross-domain-prior]`, `[divergent: scale-shift-prior]`, `[divergent: contrarian-prior]`, etc. This makes the Portfolio teach the user something about engine-prior structure, not just list reframes.

### 9. PRESENT

Default = inline Portfolio in the chat, with the document also written to `docs/reframes/PORTFOLIO-[topic]-[date].md` if the user requested a file. Do not surface engine-raw JSON. Do not include rejected reframes in the main list (they go in the rejection ledger as counts only).

---

## Parallel Subagent Prompt Skeleton

Use the canonical spawn/capture template in `_common/CLI_COMPATIBILITY.md` with the JSON schema in this reference. Spawn once per selected available engine, not a fixed three. Add these domain fields; the main context owns normalization, grounding and synthesis.

**Role:**
Generate {N=4-6} reframings of the stuck problem below. You are one of the selected engines working independently — do not try to be exhaustive or balanced; surface the inversions and perspective shifts that YOUR training-data priors find most provocative. Divergence from the other two engines is valuable, not a defect.

**Target:**
- Stuck problem statement: {scope}
- Evidence of stuck-ness: {what was tried, why it didn't work}
- Visible constraints (real): {list}
- Assumed constraints (to challenge): {list}
- Cynefin domain (if classified): {domain or "unknown"}
- Reframe axis preference: {assumption-inversion / cross-domain / perspective-rotation / all}

**Constraints:**
- Each reframe must name the ORIGINAL ASSUMPTION being challenged, not just the new framing
- Each reframe must specify the INVERTED FORM (what the new assumption is, not just that something is reversed)
- Each reframe must list ONE concrete next-step action made available by the reframe that was NOT available under the original framing
- Prefer bold inversions over safe restatements — a reframe that fails to change the action surface is not a reframe
- If you cite a cross-domain source, the mechanism must plausibly exist in that domain
- Do not paraphrase the original framing in different words and call it a reframe — synonym-substitution fails the Novelty test

## Degraded Modes

Use `_common/MULTI_ENGINE_RECIPE.md` § Engine Availability Modes and its actual-engine denominator. A healthy Claude+Codex pair is the normal dual-engine baseline, not a 2/3 degraded result.

With one usable engine, keep candidate reframes and the Blind Spot Report with an explicit single-engine label; do not invent independent engine voices. With zero, use `reframe`. Do not compensate for a missing engine by injecting framework-specific branches that violate the loose-prompt contract.

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — Pattern D (Divergence-Primary) base protocol
- `_common/SUBAGENT.md §MULTI_ENGINE` — base protocol for engine dispatch and loose prompts
- `spark/reference/tri-engine-proposal.md` — canonical Pattern D implementation (proposals); CLUSTER/SCORE/SYNTHESIZE differences noted above
- `echo/reference/tri-engine-demand.md` — Pattern D with calibration tags (Flux does not calibrate against ground-truth; we calibrate against ASN test)
- `flux/reference/output-formats.md` — Portfolio document template (Assumption Map, Insight Matrix, Blind Spot Report)
- `_common/OPUS_5_AUTHORING.md` — subagent prompt sizing, thinking-depth nudges at SCORE/GROUND
