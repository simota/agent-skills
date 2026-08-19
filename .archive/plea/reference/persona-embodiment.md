# Persona Embodiment

Read this when running the `roleplay` Recipe, when Plea needs to deeply embody a persona before voicing demands, or when persona diversity coverage is in question. This reference holds the Persona Diversity Matrix, the Channeling Template, the Generation Modes that bias demand framing, and the embodiment tactics that drive demand from lived friction rather than abstraction.

---

## Persona Diversity Matrix

Select at least 3 personas per session, drawing from these axes so coverage avoids WEIRD / mode-collapse bias. A single-axis sweep (e.g., 3 different "Proficiency" levels but all engineers on desktop) does NOT count as diversity — span at least 2 axes.

| Axis | Examples |
|------|----------|
| Proficiency | Day-one user / Weekly user / Power user |
| Technical skill | Tech novice / General literacy / Engineer |
| Accessibility | Screen reader dependent / Low vision / Motor disability / Cognitive load sensitive |
| Usage context | Mobile on-the-go / Desktop focused / Multitasking / Shared device |
| Emotional state | Hopeful newcomer / Frustrated continuing user / About to churn / Returning after pause |
| Purpose | Personal use / Team management / Evaluating for purchase / Regulatory compliance |
| Locale / Culture | First-language match / Second-language user / Region with different mental model |
| Disposition / Change stance | Conservative majority / Pragmatist / Early-adopter visionary / **Entrepreneur** / **Revolutionary** / **Maverick (heretic)** |

The **Disposition** axis is the antidote to a demand report full of incremental gripes (see the conservatism guard in `SKILL.md` Core Contract). The mainstream axes above bias toward friction-relief; the change-stance archetypes below are the natural source of **aspirational `ASPIRE`-mode demands** and **bold `H2`/`H3` feature seeds** for Spark. Define them by *behavior and worldview*, never by demographics (the demographic-stand-in anti-pattern applies doubly here). Detailed behavioral anchors + Jung-archetype mapping → **Challenger Archetypes** below.

When Cast personas are available at `.agents/personas/registry.yaml`, prefer those — they carry validated diversity; the change-stance archetypes map onto Cast's Jung **Outlaw / Magician / Creator / Hero** brand archetypes (`cast/reference/archetype-mapping.md`). When Cast is absent, generate proto-personas under `_common/AI_PERSONA_RISKS.md` guardrails and cap confidence at 0.50.

---

## Persona Channeling Template

Fill this template for every selected persona before generating any demand. Channeling is a deliberate embodiment step — not a label.

```yaml
PERSONA_CHANNEL:
  name: "[Persona name]"
  archetype: "[Proficiency] × [Technical skill] × [Usage context]"
  daily_context: "[A typical day for this person]"
  emotional_state: "[Current feeling toward this product]"
  last_frustration: "[Recent irritation — must be concrete, with time and place]"
  competitor_experience: "[Other tools they use and what they take for granted there]"
  unspoken_assumption: "[What this person takes for granted that the team does not]"
```

Each field is mandatory. An empty `last_frustration` or `unspoken_assumption` is a signal that channeling has not landed — pause and ground the persona in a concrete scene before continuing.

---

## Challenger Archetypes (Disposition axis)

The mainstream Diversity-Matrix axes voice **friction-relief** demands ("fix what hurts"). Challenger archetypes voice **transformation** demands ("change what's possible"). They are the persona-level source of the bold, aspirational, anti-conservative demands the `ASPIRE` mode and Spark's `H2`/`H3` Horizon ladder need. Channel them by worldview and behavior — never by demographic or job title.

| Archetype | Worldview | What they demand (and the others miss) | Voice tell | Jung map (Cast) |
|-----------|-----------|----------------------------------------|-----------|-----------------|
| **Entrepreneur** | The product is leverage — a force multiplier for value they're trying to create. Tolerates rough edges if it unlocks capability. | Demands framed as opportunity and leverage: "let me 10x this / automate it / build on top of it / monetize it." Capability over polish. | "If it could just *do X for me*, I'd build a whole workflow around it." | Creator / Magician / Hero |
| **Revolutionary** | The *whole approach* is wrong, not the button. Impatient with incrementalism; wants the category redrawn. | Systemic, category-redefining demands the friction-relief personas never reach because they accept the current frame. | "You're optimizing the wrong thing — nobody should have to do this at all." | Outlaw / Magician |
| **Maverick / Heretic** | Rejects the "correct" / intended way to use the product. Power-uses against the grain. | Escape hatches, scripting, un-sanctioned flexibility, API access — demands the happy-path design actively suppresses. | "I know I'm not *supposed* to use it like this, but here's what I actually do…" | Outlaw / Explorer |
| **Early-adopter visionary** | Lives a release or two in the future; treats what's coming as already overdue. | What's "obviously next" — the demand that looks premature now and obvious in hindsight. | "Everyone will expect this within a year; why don't you have it yet?" | Explorer / Magician |

### Guardrails (mandatory)

- **Addition, not replacement.** Challenger archetypes are layered on top of the mandatory beginner + power-user + edge-case set (Core Contract) — never instead of them. A demand report that is *all* visionaries over-rotates the other way and loses the silent majority.
- **Higher projection-bias risk.** These archetypes amplify the model's own "disruptive/visionary" priors (a distinct `_common/AI_PERSONA_RISKS.md` failure mode). Their demands ceiling at `[hypothesis]` + `synthetic: true` like any synthetic voice, and they are *especially* prone to producing visionary-but-unwanted features — route to Field for real-switcher validation before generalizing.
- **Bold ≠ unmoored.** Even a Revolutionary's demand needs a concrete `last_frustration` and a real scene; "burn it all down" with no grounded friction is FUD, not a demand. The self-rejection gate (`SKILL.md`) still applies.
- **Don't feasibility-filter their ambition.** A challenger demand that "sounds unrealistic" must be surfaced, not silently tamed — that is forbidden feasibility-filtering. Calibration governs confidence; it never governs ambition.

---

## Request Generation Modes

Each Recipe defaults to one Mode (see the Recipes table in `SKILL.md`). The Modes below describe how a persona generates demand — what kind of friction they channel, how broad or narrow their voice is. `COMPETE` and `EDGE` are Mode Modifiers that can overlay any Recipe.

| Mode | Description | When to use |
|------|-------------|-------------|
| `EXPLORE` | Broad, free-form requests from diverse personas | Initial brainstorming, roadmap review (Recipe: `request`) |
| `CHALLENGE` | Counter existing plans and roadmaps | Plan verification, blind spot discovery (Recipe: `challenge`) |
| `DEEP` | Deep-dive into a specific feature or persona | Pre-design user perspective check (Recipes: `need`, `roleplay`, `jtbd`, `5whys`, `opportunity`) |
| `COMPETE` | Voice frustration anchored to competitor experiences | Competitive analysis, differentiation — overlays any Recipe |
| `EDGE` | Requests from minority and extreme use cases | Accessibility, regulated industries, fringe personas — overlays any Recipe |

---

## Embodiment Tactics

Six tactics that move demand generation from abstract to lived. Apply at least one per persona in the `roleplay` Recipe; use them as quality probes in other Recipes.

### "5-Year-Old Test"
Can you explain this feature to a 5-year-old? If not, users won't understand either. Use as a curse-of-knowledge probe: any demand that requires industry vocabulary to express is a demand the user could not have voiced.

### "Competitor Envy"
Start from frustration: "App X already does this, why can't you?" Anchors the demand in a concrete external reference rather than abstract preference. Especially useful in `COMPETE` mode.

### "Worst Day"
Imagine using this product on the user's worst day — exhausted, late, with a flaky network, on a small screen, holding a baby. Demands that survive the worst day are the demands worth shipping. Especially useful in `roleplay`.

### "Silent Majority"
Focus on users who don't speak up but quietly churn. They generate no support tickets and no public reviews — Voice cannot see them. Plea's role is to verbalize the demand they would have voiced if they had stayed. Pair with `_common/AI_PERSONA_RISKS.md` to avoid projecting the loudest persona's voice onto silent users.

### "Reverse Thinking"
Measure real value by asking "Who would suffer if this feature disappeared?" If no persona can name a concrete harm, the demand is weaker than it sounds. Use as a kill-rule probe in the `opportunity` Recipe.

### "Magic Wand"
The Best-Day inverse of Worst Day: "if this product could do *anything* for you, what would make you tell everyone about it?" Removes the implicit feasibility filter so the persona voices the aspirational want, not the resigned compromise. The primary source of `ASPIRE`-mode demands and the natural tactic for the **Challenger Archetypes** above — apply it whenever a session risks returning only incremental gripes.

---

## Single-Persona Depth (`roleplay` Recipe)

The breadth recipes (`request`, `need`) span many personas shallowly. `roleplay` does the opposite: **one persona, deeply** — a sustained first-person embodiment, not a demand list. Depth is the deliverable, so the breadth checks above (≥3 personas, span 2 axes) do **not** apply; the depth method below replaces them.

### Depth rubric (shallow → deep)

| Dimension | Shallow | Deep (target) |
|-----------|---------|---------------|
| Tactic stacking | one tactic applied once | **≥ 3 of the 5 tactics applied to the same persona** (e.g. Worst Day + Silent Majority + Reverse Thinking + 5-Year-Old) |
| Temporal span | a single moment | a full arc — Day-in-the-Life or the journey from first-use to the friction (Pattern 3) |
| Specificity | "the dashboard is confusing" | a named scene with time, place, device, what they were holding, what they said out loud |
| Emotional resolution | one stated emotion | an emotional **trajectory** (e.g. hopeful → confused → resigned → workaround) |

### Character-coherence check (the primary `roleplay` failure mode)

Sustained single-persona embodiment drifts: over a long roleplay the voice slips back to generic/PM register. Hold the line:

- The persona's `unspoken_assumption`, vocabulary register, and `last_frustration` stay **consistent** start to end — no contradicting earlier statements for narrative convenience.
- No mid-roleplay jump to a different persona's perspective (that's a `request`/`need` job, not `roleplay`).
- Zero PM-voice leakage ("the user would benefit from…"). Break-character = restart the scene, don't paper over it.

### Narrative-arc output (for the Scribe / Saga handoff)

`roleplay` hands off to Scribe (user stories) and Saga (narrative). Shape the embodiment into a **story-ready arc**, not raw demands:

```yaml
ROLEPLAY_ARC:
  persona: "[name + PERSONA_CHANNEL ref]"
  setup: "[their world before the friction — what they were trying to accomplish]"
  inciting_friction: "[the moment the product failed them — concrete scene]"
  escalation: "[how it compounded — tie to Frustration Escalation, patterns.md Pattern 6]"
  turning_point: "[workaround adopted, or the decision to churn]"
  demands_surfaced: "[the demands this arc implies — each with calibration tag]"
  emotional_trajectory: "[hopeful → … → resolution]"
```

### Representativeness caveat (stricter than breadth recipes)

A single, vividly-imagined persona is the **highest projection-bias risk** in Plea — depth makes a wrong persona *more* convincing, not more correct. Always:

- Tag the whole roleplay `[hypothesis]` ceiling and `synthetic: true`; deep ≠ representative.
- State explicitly: "this is **one** persona's lived experience, not the market." Recommend a `request`/`multi` breadth pass or Field validation before generalizing any surfaced demand.

---

## Quality Checks

Before handing off demands generated under any of these tactics:

- [ ] Every persona has a filled `PERSONA_CHANNEL` template — no empty `last_frustration` or `unspoken_assumption` fields
- [ ] **Multi-persona recipes** (`request`/`need`): personas span at least 2 axes from the Diversity Matrix · **`roleplay`**: the single persona meets the Depth rubric (≥3 tactics, full arc, character-coherent)
- [ ] Each demand quotes the user voice verbatim — no paraphrasing into PM language
- [ ] If Cast was unavailable, all proto-personas are tagged `confidence ≤ 0.50` and `synthetic: true`
- [ ] At least one demand survives the "Worst Day" probe
- [ ] At least one demand passes the "Reverse Thinking" kill-rule
- [ ] **`ASPIRE` / bold sessions**: ≥1 Challenger Archetype channeled *in addition to* (never instead of) the mandatory beginner + power-user + edge-case set; its demand is grounded in a concrete `last_frustration`, ceilings at `[hypothesis]`, and is not feasibility-filtered
- [ ] No persona was steered toward an opinion that smooths out a contradiction with another persona
- [ ] **`roleplay` only**: zero character breaks / PM-voice leakage; representativeness caveat stated; output shaped as a `ROLEPLAY_ARC`

---

## Anti-Patterns

- **Single-axis sweep**: 3 personas that differ only in proficiency level. Not diversity.
- **Demographic stand-in for behavior**: "Female, 35, in Tokyo" without a behavior or emotional anchor produces generic demand.
- **Persona without a scene**: "Power user" with no daily_context generates abstract requests, not embodied ones.
- **Smoothed contradictions**: When two personas disagree, preserve both voices. The contradiction is the signal.
- **Loudest-voice projection**: Channeling the loudest user (e.g., the engineer who files detailed tickets) and labeling them "the user." Use Silent Majority tactic to counter.
- **PM voice leakage**: "The user would benefit from a streamlined onboarding flow" is not a user voice — it is a PM voice. Translate to first-person friction before continuing.
- **All-visionary over-rotation**: a demand report channeling only Entrepreneurs / Revolutionaries / Mavericks. The Challenger Archetypes are an *addition* for bold demands, not a replacement — drop the silent majority and you trade one bias (incrementalism) for another (disruption-for-its-own-sake).
- **Ungrounded revolutionary**: "tear the whole thing down" with no concrete `last_frustration` or scene. Bold ≠ unmoored — a challenger demand still needs a real friction anchor or it is FUD.
