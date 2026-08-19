# Echo[demand] Design Patterns

**Purpose:** Demand generation design patterns and best practices.
**Read when:** Choosing a generation mode or deciding persona channeling depth.

---

## Pattern 1: Persona Spectrum

**When to use:** Generating broad demands (EXPLORE mode — the `request` default Recipe)

Select 3-7 personas evenly from diversity matrix axes, intentionally avoiding overlap.

```yaml
PERSONA_SPECTRUM:
  selection_rules:
    - Always include both ends of proficiency (beginner + power user)
    - Include at least 1 accessibility persona
    - Include 2+ personas with different emotional states
  anti_pattern:
    - Don't let all personas be "ideal users"
    - Don't let technical skill skew in one direction
```

### Default calibration for `request` (uncalibrated EXPLORE)

The `request` Recipe usually runs without real Voice/Trace/Field data. Tag every emitted demand even so — downstream agents (Spark, Rank, Scribe[unified]) and the `growth-acceptance` Insight Ledger need the confidence signal, and `[hypothesis]`/`[synthetic-only]` demands are **not** Ledger-citable evidence (`_common/GROWTH_BRAND_PROOF.md` G11).

```yaml
REQUEST_DEFAULT_CALIBRATION:
  no_real_data_consulted:
    plausible_demand: "[hypothesis]"      # realistic; flag for Field/Voice validation
    possible_ai_artifact: "[synthetic-only]"  # over-sanitized / WEIRD / jargon-flavored; review for removal
  real_data_consulted:                    # only when Voice/Trace/Field input is present
    direct_match: "[validated]"
    implied_match: "[supported]"
  rule: never emit an untagged demand; never default to [validated]/[supported] without a cited match
```

### Self-rejection ledger (all Recipes)

Before emitting, run each candidate demand through the gate and record drops by category. This is the single-engine equivalent of the `multi` Recipe's rejection ledger.

```yaml
SELF_REJECTION_GATE:
  drop_if:
    voice-mismatch: reads as PM/dev framing, not first-person user
    criteria-vague: no testable acceptance condition a user could confirm
    persona-fabricated: empty/ungrounded last_frustration or unspoken_assumption
    feasibility-filtered: dropped because it "seemed hard" — FORBIDDEN; count must be 0
  emit: "| category | dropped_count | example |" table in the report
```

---

## Pattern 2: Devil's Advocate

**When to use:** Generating counterarguments to existing plans or roadmaps (CHALLENGE mode)

Intentionally argue against decisions the team believes are "correct" from a user perspective.

```yaml
DEVILS_ADVOCATE:
  steps:
    1. Clarify the team's decision or plan
    2. Identify users who don't benefit from this decision
    3. Embody those users and verbalize counterarguments
    4. Don't judge whether the counterargument is valid (users are subjective)
  output: List of counterarguments + affected user segments
```

---

## Pattern 3: Day-in-the-Life

**When to use:** Generating deep-dive demands for a specific feature (DEEP mode)

Follow a persona through their day, mining demands at every product touchpoint.

```yaml
DAY_IN_THE_LIFE:
  timeline:
    morning: "[Wake up to commute]"
    work_start: "[First 30 minutes of work]"
    mid_day: "[Focused work session]"
    interruption: "[Interruption / multitasking]"
    end_of_day: "[Daily report / reflection]"
  at_each_touchpoint:
    - What is this persona trying to do?
    - What happens with the current product?
    - What would ideally happen?
    - What emotion arises from the gap?
```

---

## Pattern 4: Competitor Envy

**When to use:** Generating demands based on competitor experiences (COMPETE mode)

Start from positive experiences users had with competitor products, then voice frustration and demands.

```yaml
COMPETITOR_ENVY:
  structure:
    competitor_experience: "[Positive experience with competitor]"
    current_gap: "[Gap with own product]"
    user_frustration: "[User's frustration (first person)]"
    demand: "[Specific demand]"
  caution:
    - Voice experience gaps, not feature-copy requests
    - Include context for why the competitor experience felt good
```

---

## Pattern 5: Edge Voice

**When to use:** Mining demands from minority and edge-case users (EDGE mode)

Generate voices that standard user research misses — few in number but critically important.

```yaml
EDGE_VOICE:
  target_personas:
    - Screen reader users
    - Slow connection users
    - Non-native speakers
    - Elderly users
    - One-handed operation users
    - Users with color vision diversity
  principle: |
    Minority demands often represent latent
    inconveniences shared by many users.
    Be mindful of the curb-cut effect.
```

---

## Pattern 6: Frustration Escalation

**When to use:** Understanding the process by which users reach churn

Verbalize how small frustrations accumulate stage by stage until the user leaves.

```yaml
FRUSTRATION_ESCALATION:
  levels:
    1_notice: "Hmm, that's a bit inconvenient (but whatever)"
    2_annoy: "This again... starting to get irritated"
    3_workaround: "Guess I'll just find my own way around it"
    4_compare: "Other tools don't have this problem"
    5_decide: "That's it, I'm switching"
  at_each_level:
    - What demand would the user voice at this stage?
    - How would they feel if heard at this stage?
    - What happens if this stage is passed?
```

---

## Pattern 7: Unmet-Need Elicitation (`need` Recipe, DEEP mode)

**When to use:** The `need` Recipe — surfacing latent needs the user **cannot articulate**. An unmet need is, by definition, never voiced directly; Echo[demand] must infer it from observable *proxies* of friction.

### Latent-need taxonomy (where unmet needs hide)

| Proxy signal | What it reveals | Probe question (channel the persona) |
|--------------|-----------------|--------------------------------------|
| **Workaround / compensating behavior** | a missing capability (user built a manual hack — spreadsheet, copy-paste, second tool) | "What did you do *instead*?" |
| **Abandonment / drop-off** | friction at a specific step (user starts a task and quits) | "Where did you give up, and what stopped you?" |
| **Non-consumption / avoidance** | a barrier — fear, complexity, distrust (user never enters an area) | "What did you never even try? Why not?" |
| **Over-service / feature-fatigue** | a need for simplicity/defaults (user uses 10%, feels overwhelmed) | "What do you ignore entirely?" |
| **Tolerated pain / resignation** | normalized friction — the curse of low expectations (user stopped complaining) | "What do you just put up with?" |
| **Adjacent-tool leakage** | an unmet boundary need (part of the job done in another app) | "Where do you leave this product to finish the job?" |

### Elicitation method

1. For each persona, walk **Day-in-the-Life** (Pattern 3); at each touchpoint run the six probe questions above.
2. Capture the **proxy**, then translate it into the **underlying unmet need** — report the need, never the workaround itself (the spreadsheet is not the demand; the missing capability is).
3. Cross-persona: a latent need surfacing for ≥ 2 personas is a **curb-cut candidate** (minority friction shared silently by many).
4. Pair each surfaced need with the curse-of-knowledge table (SKILL Assumption Challenge) to name the team blind spot it exposes.

### Calibration posture (stricter than `request`)

Latent needs are unvoiced, so they cannot be `[validated]`/`[supported]` from user *speech* — only from **behavioral evidence**. Ceiling at `[hypothesis]` until Trace (observed workaround/drop-off) or Field (contextual inquiry) confirms the proxy exists. Never tag a latent need `[validated]` without behavioral data. Default handoff is **Field/Trace for validation first**, then Spark/Scribe[unified].

### Disambiguation vs sibling DEEP Recipes

| Recipe | Lane | Escalate from `need` when |
|--------|------|---------------------------|
| `need` | breadth-first latent-need discovery across personas (this pattern) | — |
| `5whys` | depth-first root cause of **one** surfaced need | a single need needs its root unmet driver |
| `jtbd` | the progress/job + switch forces for **one** job | the need is really "what job is being hired?" |
| `opportunity` | structure needs into an Outcome→Opportunity→Solution tree | you have many needs and must prioritize toward an outcome metric |
