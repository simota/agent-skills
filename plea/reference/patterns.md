# Plea Design Patterns

**Purpose:** Demand generation design patterns and best practices.
**Read when:** Choosing a generation mode or deciding persona channeling depth.

---

## Pattern 1: Persona Spectrum

**When to use:** Generating broad demands (EXPLORE mode)

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
