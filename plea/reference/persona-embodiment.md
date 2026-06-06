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

When Cast personas are available at `.agents/personas/registry.yaml`, prefer those — they carry validated diversity. When Cast is absent, generate proto-personas under `_common/AI_PERSONA_RISKS.md` guardrails and cap confidence at 0.50.

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

Five tactics that move demand generation from abstract to lived. Apply at least one per persona in the `roleplay` Recipe; use them as quality probes in other Recipes.

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

---

## Quality Checks

Before handing off demands generated under any of these tactics:

- [ ] Every persona has a filled `PERSONA_CHANNEL` template — no empty `last_frustration` or `unspoken_assumption` fields
- [ ] Personas span at least 2 axes from the Diversity Matrix
- [ ] Each demand quotes the user voice verbatim — no paraphrasing into PM language
- [ ] If Cast was unavailable, all proto-personas are tagged `confidence ≤ 0.50` and `synthetic: true`
- [ ] At least one demand survives the "Worst Day" probe
- [ ] At least one demand passes the "Reverse Thinking" kill-rule
- [ ] No persona was steered toward an opinion that smooths out a contradiction with another persona

---

## Anti-Patterns

- **Single-axis sweep**: 3 personas that differ only in proficiency level. Not diversity.
- **Demographic stand-in for behavior**: "Female, 35, in Tokyo" without a behavior or emotional anchor produces generic demand.
- **Persona without a scene**: "Power user" with no daily_context generates abstract requests, not embodied ones.
- **Smoothed contradictions**: When two personas disagree, preserve both voices. The contradiction is the signal.
- **Loudest-voice projection**: Channeling the loudest user (e.g., the engineer who files detailed tickets) and labeling them "the user." Use Silent Majority tactic to counter.
- **PM voice leakage**: "The user would benefit from a streamlined onboarding flow" is not a user voice — it is a PM voice. Translate to first-person friction before continuing.
