# Multi-Engine Cognitive Walkthrough

> **Filename retained** as `tri-engine-walkthrough.md` for backward compatibility. Covers both dual-engine baseline (Claude + Codex) and tri-engine optional (Claude + Codex + agy) modes.

Default flow for `/echo multi`. Run subagents in parallel — one per AVAILABLE engine — to perform cognitive walkthroughs of the **same UI flow** across the **same persona set**, then integrate the results across three axes — per-persona concurrence, cross-persona universality, and engine-specific blind-spot fills.

**Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT. dual-engine mode is NOT degraded — Claude (empathy-curated persona channeling) + Codex (GitHub-issue user-pain patterns) cover two distinct UX-judgment priors. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Why multiple engines for cognitive walkthrough (different from Judge / Spark):** Judge optimizes for *agreement on a single defect* — concurrence is the quality signal. Spark optimizes for *breadth of ideation*. Echo lives in between: a friction confirmed by all AVAILABLE engines × N personas is one of the strongest synthetic UX signals available, but the *novel* friction noticed by only one engine inside one persona's voice is often the breakthrough finding the team had unconsciously normalized. Each engine has different priors about how a "beginner," "senior," or "mobile user" actually moves through a UI; multi-engine flow surfaces both convergent confidence and divergent angle in a single matrix.

**Adapted from `_common/MULTI_ENGINE_RECIPE.md` (Pattern H) and `plea/reference/tri-engine-demand.md`.** Re-uses PREFLIGHT and FAN-OUT mechanics; only the parts that differ for the walkthrough domain are documented below.

---

## Flow

```
SCOPE → CAST → PREFLIGHT → FAN-OUT (parallel subagents) → NORMALIZE → CLUSTER → SCORE (per-persona + cross-persona + per-engine) → GROUND → SYNTHESIZE → DELIVER
```

The flow mirrors Plea's tri-engine demand generation but the unit of work is a **step-level walkthrough trace**, not a feature demand.

### 1. SCOPE

Define the walkthrough target once. All three subagents share:

- **UI flow under evaluation** — name, entry condition, success condition (and failure conditions if any).
- **Step list** — ordered atomic steps the persona is expected to traverse (e.g., `S1 land → S2 sign up CTA → S3 form → S4 verify email → S5 dashboard`). Each step is the unit subagents must score.
- **Artifact references** — screenshot paths, copy excerpts, route names, or live URL. Subagents that can read images should be told so explicitly; subagents that cannot should be given verbal descriptions of the screen plus key copy.
- **Mode** — `walkthrough` (default), `confusion` (focus on cognitive load), `emotion` (focus on emotion scoring), `dark-pattern` (focus on bias/deception), `a11y` (accessibility persona only).
- **Constraints** — task limit (1-4 tasks per persona per session) and walkthrough depth.

### 2. CAST — persona selection (shared across engines)

Select **at least 3 personas** spanning at least 2 axes of the Persona Diversity Matrix. **All three engines walk the same persona set through the same UI flow** — divergence comes from how each engine channels the persona, not from different persona pools.

- Prefer Cast registry at `.agents/personas/registry.yaml` if available.
- When Cast is absent, generate proto-personas internally under AI persona guardrails (`_common/AI_PERSONA_RISKS.md`) and cap their confidence at 0.50.
- For each persona include in the FAN-OUT prompt: `persona_id`, archetype, environmental context (device, connectivity, attention level, time pressure), known mental model gaps, prior tool exposure, and last frustration. This is the same `PERSONA_CHANNEL` block Plea uses.

### 3. PREFLIGHT — engine availability detection (Echo main context, never delegated)

Identical to `_common/MULTI_ENGINE_RECIPE.md §2`. Probe `codex`, `agy`, `claude` from Echo main context with the canonical probe; subagent PATH is narrower and would produce false-negative verdicts.

### 4. FAN-OUT — parallel subagents

Spawn **three Agent calls in a single message** so they run concurrently. Each subagent receives the **same persona set + same step list + same artifacts** and is asked to walk every persona through every step independently. The matrix unit is one `(persona, step)` cell per engine — so 3 personas × 5 steps × 3 engines = 45 cells per session.

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `walkthrough-codex` | Codex CLI | `codex exec --full-auto "<prompt>"` |
| `walkthrough-agy` | Antigravity CLI | `agy -p "<prompt>" --dangerously-skip-permissions --log-file <path>` (silent-failure detection mandatory — see `_common/MULTI_ENGINE_RECIPE.md §3.5 Engine Runtime Failure Detection`) |
| `walkthrough-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

**Loose prompt rule:** pass only Role + Personas + UI flow + Step list + Artifacts + Output schema. Do NOT pass Echo's Nielsen heuristics, NASA-TLX rubric, dark-pattern taxonomy, or Peak-End synthesis rules — those frames apply at SYNTHESIZE. Each engine should channel the persona through the steps in its own way.

**Required JSON output schema:**

```json
{
  "engine": "codex|agy|claude",
  "walkthroughs": [
    {
      "persona_id": "Persona name or archetype (must match input)",
      "environmental_context": "Device, connectivity, attention, time pressure",
      "steps": [
        {
          "step_id": "S1 | S2 | ...",
          "step_label": "Short description of what the persona is trying to do",
          "expected_behavior": "What a successful persona would do",
          "predicted_behavior": "What the channeled persona actually does (in first-person voice if natural)",
          "friction_points": [
            {
              "friction_id": "engine-local id, e.g. codex-F1",
              "friction_class": "copy-ambiguity | trust-signal-missing | navigation-loss | cognitive-overload | form-friction | feedback-absence | dark-pattern | a11y-block | mental-model-gap | other",
              "description": "What the persona experiences — first-person where natural",
              "severity": "0 (none) | 1 (cosmetic) | 2 (minor) | 3 (major) | 4 (blocker)",
              "evidence_locator": "Copy text / element / route / screenshot region the friction attaches to"
            }
          ],
          "cognitive_load": "1 (very low) | 2 | 3 | 4 (very high) — SEQ-style single-item rating",
          "emotional_score": -3,
          "emotional_dimension": "Valence (-3 to +3) — required; Arousal / Dominance optional",
          "confusion_moments": ["Concrete moment of confusion in persona voice"],
          "mental_model_gap": "Optional: what the persona expected vs what happened",
          "suggested_fix": "Optional: one-line fix from persona perspective (NOT implementation jargon)"
        }
      ],
      "journey_summary": {
        "overall_emotion": "-3 to +3 average / Peak-End estimate",
        "completion_likelihood": "0.0-1.0",
        "task_success": "true | false | partial"
      }
    }
  ],
  "engine_notes": "Optional: which persona this engine felt strongest channeling, and any persona × step it explicitly skipped or struggled with"
}
```

If an engine returns free-form Markdown, ask its subagent to re-emit as JSON before integrating.

### 5. NORMALIZE

Parse the three JSON blobs into a unified walkthrough cell list. Tag each cell with `(engine, persona_id, step_id)`. Preserve per-engine wording — divergent persona voice is signal.

### 6. CLUSTER — dedup within the same (persona, step)

Group **friction points** that describe the same UX issue inside the same `(persona_id, step_id)` cell. Two friction points match when **all three** hold:

- **same `persona_id`** — never cluster across personas (see cross-persona signal below)
- **same `step_id`** — never cluster across steps; the same friction class at a different step is a separate finding
- **same `friction_class` AND overlapping `evidence_locator`** — e.g., two engines both flag `copy-ambiguity` on the same CTA copy on `S2` for the same persona

**Critical rule:** Do NOT cluster across personas. Friction X for persona-A on S2 and friction X for persona-B on S2 are *separate* — the fact that two personas independently surface the same friction is the **cross-persona signal** that SYNTHESIZE highlights, not a deduplication target.

Record the set of engines that produced each cluster (within the same persona × step).

### 7. SCORE — per-persona concurrence + cross-persona universal + per-engine consistency (Pattern H)

Echo scores along **three axes**, all of which can appear on the final report.

#### Axis 1 — Per-cluster concurrence (within one persona × step)

Confidence axis from `_common/MULTI_ENGINE_RECIPE.md` Pattern H:

| Engines in cluster | Confidence label | Interpretation |
|--------------------|------------------|----------------|
| 3 / 3 | `CONFIRMED` | All engines channeled this persona to the same friction at the same step — high-confidence UX problem. |
| 2 / 3 | `LIKELY` | Two engines concur; one missed it — note the silent engine. |
| 1 / 3 | `CANDIDATE` | Only one engine surfaced this. Must pass GROUND (step 8) to ship. |

#### Axis 2 — Cross-persona universality (across persona clusters at the same step)

After per-cluster scoring, identify friction classes that surface across **multiple personas** on the same step:

- `CROSS-PERSONA-UNIVERSAL` — friction class appears in **≥2 personas** at the same step, AND was `CONFIRMED` or `LIKELY` in each persona's cluster. **Strongest signal.** This is friction every kind of user feels at the same point in the flow — usually the most important finding in the report.
- `CROSS-PERSONA-SEGMENT` — friction class appears in 2+ personas at the same step but only as `CANDIDATE` in each. Surface as "segment-level hypothesis; needs grounding."
- `PERSONA-SPECIFIC` — friction surfaced for exactly one persona. Persona-specific insight; do not generalize. (Often valuable: e.g., a11y persona surfacing a screen-reader issue.)

#### Axis 3 — Per-engine consistency (across personas, per engine)

For each engine, check whether its emotional scoring and severity is internally consistent across personas. Strong engine inconsistency (e.g., one engine scores S2 as -3 for the beginner but +1 for the senior while the other two engines score both negative) is a **persona-channeling weakness signal** for that engine — flag it in `engine_notes` synthesis. Do not drop the data; surface it as a calibration note.

#### Perspective axis (Pattern H)

Tag the consolidated finding on each step:

- `CONVERGENT` — all engines reach the same friction verdict at this step (regardless of count of frictions). The story of the step is settled.
- `DIVERGENT-N` — engines split on the step's verdict (e.g., one engine says "fine," two say "broken," or three engines each surface a different friction). `N` = number of distinct dissenting positions. Preserve the split as a feature, not a bug — it's information about edge-cases or engine bias.

**Critical Echo-specific rule (does NOT exist in Judge):** `CANDIDATE` / `DIVERGENT-N` findings are NOT auto-low-value. A single engine surfacing the "silent majority" friction — the one users complain about least loudly because they've normalized it — is exactly the finding the other two engines might smooth over. Preserve all `CANDIDATE` findings through GROUND.

### 8. GROUND — verify CANDIDATE / DIVERGENT findings (Echo main context, never delegated)

For every `CANDIDATE` cluster, the Echo main context must:

1. **Artifact existence check** — does the cited `evidence_locator` (copy / element / route / screenshot region) actually exist in the supplied artifacts? If hallucinated, mark `REJECTED-HALLUCINATION`.
2. **Persona-voice authenticity check** — does the `description` and `confusion_moments` sound like the named persona? Or does it slip into developer/PM language? If inauthentic, mark `REJECTED-VOICE-MISMATCH`.
3. **Severity sanity check** — does the cited severity match the friction class? Cosmetic items scored 4 (blocker) or a11y blockers scored 1 (cosmetic) are calibration errors — adjust or mark `NEEDS-INFO`.
4. **Already-mitigated check** — is the cited friction already addressed by copy / UI / a11y affordances the engine missed? If yes, `REJECTED-ALREADY-MITIGATED`.
5. **Real-data calibration** — if Voice / Trace / Field / session-replay data exists in the project (e.g., `.agents/voice.md`, `.agents/trace.md`), cross-check. Apply confidence tag:
   - `[validated]` — synthetic friction matches real user signal
   - `[supported]` — partial evidence (one source agrees)
   - `[hypothesis]` — no real-data conflict, no real-data support
   - `[synthetic-only]` — no real-data sources available
6. **Mark each as** `VERIFIED-DIVERGENT` (keep with confidence tag), `REJECTED-{reason}` (drop), or `NEEDS-INFO` (escalate).

For `CONFIRMED` and `LIKELY` clusters, run only artifact-existence + persona-voice authenticity + real-data calibration. Three engines rarely fabricate the same artifact in the same way.

### 9. SYNTHESIZE — persona × engine matrix + priority-ranked friction list

Echo's multi-engine output presents both **the persona × engine matrix** (raw view) and a **priority-ranked friction list** (action view). This is the opposite of Judge's "by severity" structure — Echo's value lives in the matrix where Pattern H's both axes are visible.

Synthesis steps:

1. **Cross-persona universal frictions (top section)** — list every `CROSS-PERSONA-UNIVERSAL` finding, ordered by severity × #personas × #engines. These are the strongest signals; they should drive Palette / Experiment handoff first.

2. **Per-step matrix view** — for each step in the flow, present a compact matrix:

   ```
   Step S2: Sign up CTA
                          | codex | agy | claude
   Beginner persona       |  -3   | -3  |  -2     CONFIRMED CONVERGENT
   Senior persona         |  -1   |  0  |  -2     LIKELY DIVERGENT-2
   Mobile user persona    |  -3   | -3  |  -3     CONFIRMED CONVERGENT
   ──────────────────────────────────────────────
   Cross-persona verdict: CROSS-PERSONA-UNIVERSAL  copy-ambiguity, trust-signal-missing
   ```

   Show emotional score in each cell; annotate the verdict row with cross-persona tag and dominant friction classes.

3. **Per-persona journey summary** — for each persona, list the friction points ranked by `CONFIRMED → LIKELY → VERIFIED-DIVERGENT`, with the step and engine attribution attached. Include each persona's overall emotion (Peak-End computed across the run) and completion likelihood.

4. **Divergent-voice insights** — call out every `VERIFIED-DIVERGENT` finding in its own section with engine attribution and the rationale for keeping it. This is where breakthrough findings live.

5. **Engine-channeling notes** — short section noting which engine channeled which persona most distinctively, and any per-engine consistency weakness flagged at SCORE step. Useful for next-session persona prep and for spotting when one engine systematically under- or over-emotes.

6. **Recommended fixes** — aggregate `suggested_fix` strings from all clusters, dedupe, and rank by the friction's severity × cross-persona count. These feed the A/B hypothesis section.

7. **A/B test hypotheses** — generate hypotheses from `CROSS-PERSONA-UNIVERSAL` and high-severity `CONFIRMED` findings (matches Echo's standard `walkthrough` output).

8. **Rejection ledger (condensed)** — count by category — `REJECTED-HALLUCINATION / VOICE-MISMATCH / ALREADY-MITIGATED / NEEDS-INFO`. Preserves SNR transparency without re-introducing noise.

#### Engine-attribution rule

Every friction that ships must carry both an engine-concurrence tag AND a perspective tag (Pattern H two-axis):

- `[codex+agy+claude] [CONVERGENT] [validated]` — strongest signal: 3/3 concurrence + all engines converged + real-data validation
- `[codex+agy] [CONVERGENT] [supported]` — 2/3 + converged + partial real-data
- `[codex+agy+claude] [DIVERGENT-2] [hypothesis]` — 3 engines all surfaced friction at this step but reached 2 distinct verdicts; surface the split
- `[claude-verified] [DIVERGENT-3] [synthetic-only]` — 1/3 verified divergent voice, the three engines disagreed across the step, no real-data calibration available

Cross-persona-universal findings additionally carry a `[CROSS-PERSONA-UNIVERSAL]` or `[CROSS-PERSONA-SEGMENT]` tag.

### 10. DELIVER — output structure

Output follows the existing Echo `walkthrough` report template (`echo/reference/output-templates.md`) with these tri-engine additions:

- **Header summary table** gains engine-status line and dual concurrence stats: `CONFIRMED: N / LIKELY: N / VERIFIED-DIVERGENT: N` AND `CROSS-PERSONA-UNIVERSAL: N / SEGMENT: N / PERSONA-SPECIFIC: N`.
- **Cross-persona universal section** is mandatory in multi mode (single-engine mode treats cross-persona analysis as optional).
- **Per-step matrix view** is mandatory; the compact emotion × persona × engine grid is the signature multi-mode deliverable.
- **Dark pattern findings** — when surfaced by any engine, automatically promote to `CONFIRMED` if any 2 engines flag the same dark pattern (FTC/EU DSA risks are too high to require 3/3 concurrence).
- **AI persona bias disclosure** — every multi-engine report must include the synthetic-only / hypothesis / supported / validated calibration distribution, even if no real-data sources existed. This makes the bias surface visible to the team.

Do not include rejected friction in the main list. Do not surface engine-raw output. Synthetic-true tagging applies to every finding unless calibration upgraded it to `[validated]`.

---

## Parallel Subagent Invocation

Use the Agent tool three times **in the same message** for genuine parallel execution. Each subagent receives a self-contained prompt:

```
You are the {engine} walkthrough subagent for Echo. You channel synthetic users — walk AS the persona through the supplied UI flow, not ABOUT the persona.

# Role
For each persona below, walk through every step of the UI flow independently. You are one of three engines channeling the same personas through the same flow; do not smooth out persona quirks to match expected best practices. Report what the channeled persona actually experiences at each step, even when the friction is small or the experience is positive.

# Personas
{PERSONA_CHANNEL block per persona — include archetype, environmental context, mental model gaps, prior tool exposure, last frustration}

# UI Flow
- Flow name: {scope.flow_name}
- Entry condition: {scope.entry}
- Success condition: {scope.success}
- Steps (walk every step for every persona):
  - S1: {step label} — artifact: {screenshot path / route / copy excerpt}
  - S2: ...
  - Sn: ...
- Mode bias: {walkthrough | confusion | emotion | dark-pattern | a11y}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{JSON schema above}

# Constraints
- Walk EVERY persona through EVERY step — do not skip cells; if a persona would abandon mid-flow, still record the abandonment step and mark `task_success: false`
- Speak in persona voice in `predicted_behavior`, `description`, and `confusion_moments` — first person where natural
- Assign emotional_score at every step (-3 to +3); use cognitive_load 1-4 every step
- Do not invent UI elements, copy, or routes not present in the supplied artifacts — if the artifact is insufficient for a step, mark friction_class `other` with description "evidence insufficient" rather than fabricating
- Report friction even when severity = 1 (cosmetic) — surface, do not pre-filter
- Note in engine_notes which persona you felt strongest channeling and any cell you genuinely struggled with
```

The three subagents return JSON; Echo main context handles NORMALIZE through DELIVER.

---

## Degraded Modes

| Situation | Behavior |
|-----------|----------|
| 1 engine binary missing | Run the other two; flag reduced persona-voice diversity; `CANDIDATE` clusters from the remaining engines require stricter grounding |
| 2 engines fail | Single-engine output; treat every friction as `CANDIDATE`; ground all before reporting; loud `[synthetic-only]` tag throughout |
| All 3 fail | Abort multi mode; degrade to standard `walkthrough` Recipe with the Echo main context |
| User explicitly requests single engine | Skip fan-out; use standard `walkthrough` Recipe |
| Fewer than 3 personas available | Multi mode still runs but with the reduced persona pool — flag persona-representativeness as a risk per `_common/AI_PERSONA_RISKS.md` |
| Artifacts unavailable to one engine (e.g., screenshot unreadable) | That engine emits `friction_class: other / "evidence insufficient"` for affected cells; main context downgrades affected steps to `NEEDS-INFO` rather than dropping |

---

## Why This Works for Cognitive Walkthrough (different from Judge, Plea)

- **Persona-channeling priors differ across engines.** Codex (GitHub/code-heavy), Antigravity (Google product-heavy), and Claude (Anthropic-curated) each have different training-data exposure to how "beginners," "seniors," "mobile users," or "accessibility-dependent users" actually move through a UI. Three independent channelings surface more authentic persona voice diversity than a single engine.
- **Per-persona concurrence raises confidence on each cell.** When all three engines channel beginner-persona to the same friction at the same step, that friction almost certainly reflects a real UX problem (synthetic-vs-validated calibration still applies).
- **Cross-persona universality is the strongest synthetic signal.** Friction that surfaces across 2+ personas × 2+ engines (4+ independent voices at the same step) is the kind of finding that justifies an immediate Palette / Experiment handoff without further validation. The persona × engine matrix makes this signal visible instead of averaging it out.
- **Divergent-voice findings preserve the "normalized friction" insight.** The most valuable Echo finding is often the one no team member noticed — surfaced by exactly one engine, because the other two unconsciously smoothed over the persona's quirk. Pattern H scoring keeps `DIVERGENT` findings visible instead of penalizing them.
- **AI-persona bias risks (WEIRD bias, hallucination, mode-collapse per `_common/AI_PERSONA_RISKS.md`) are partially mitigated by tri-engine.** Different engines have different bias profiles; their disagreement reveals where any single engine is collapsing. Still tag synthetic-true unless calibrated against real Voice/Trace data.
- **Dark pattern detection benefits from cross-engine concurrence.** When 2/3 engines flag the same dark pattern at the same step, regulatory risk is high enough (FTC, EU DSA, CPRA, EU DFA) to treat as `CONFIRMED` even without 3/3 — false negatives in dark-pattern audit are far more costly than false positives.

---

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — Pattern H protocol (this skill's pattern type); shared SCOPE/PREFLIGHT/FAN-OUT/NORMALIZE/CLUSTER mechanics
- `_common/SUBAGENT.md §MULTI_ENGINE` — base engine dispatch and loose-prompt rules
- `_common/AI_PERSONA_RISKS.md` — persona-bias guardrails (still apply in multi mode, per engine)
- `plea/reference/tri-engine-demand.md` — sibling persona × engine matrix flow (demand-generation domain); cross-persona signal logic mirrored here
- `judge/reference/tri-engine-review.md` — canonical Pattern C tri-engine flow; PREFLIGHT/FAN-OUT shared
- `echo/reference/ux-frameworks.md` — emotion model, cognitive load index, Peak-End rule applied at SYNTHESIZE
- `echo/reference/output-templates.md` — base walkthrough report template extended by multi-engine additions
- `echo/reference/cognitive-persona-model.md` — CPM persona dimensions fed into the FAN-OUT prompt
