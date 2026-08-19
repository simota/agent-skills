# Mode Playbooks

Purpose: Detailed execution guide for each of Echo[demand]'s 5 request generation modes.

## Mode Selection Guide

```
What is the user's goal?
|
+-- "Explore what users might want" ............ EXPLORE
+-- "Challenge our plans/assumptions" .......... CHALLENGE
+-- "Deep-dive into one feature area" .......... DEEP
+-- "Hear competitor-driven frustration" ....... COMPETE
+-- "Surface minority/edge-case needs" ......... EDGE
+-- "Unclear" .................................. EXPLORE (default)
```

## EXPLORE Mode

**Purpose**: Broad demand discovery across diverse personas.

**When**: Initial brainstorming, roadmap review, new product direction.

**Persona selection**: Maximum diversity — pick from all 6 axes of the Persona Diversity Matrix. Minimum 5 personas.

**Output benchmark**: 15-25 requests across 5+ personas. Requests should span at least 4 different feature categories.

**Quality signals**:
- Requests come from genuinely different perspectives
- At least 2 requests surprise the team
- "Don't build" option is included

## CHALLENGE Mode

**Purpose**: Counter existing plans and surface blind spots.

**When**: Plan verification, pre-launch review, roadmap critique.

**Persona selection**: Deliberately select personas most likely to disagree with current plans. Include: frustrated churner, accessibility-dependent user, non-target-audience user.

**Output benchmark**: 8-15 challenges with specific counterarguments. Each challenge references the specific plan/assumption being countered.

**Discipline (anti synthetic-FUD):** a synthetic Devil's Advocate invents objections as easily as a real user voices them — without rigor, CHALLENGE produces confident noise. Run every challenge through:

1. **Steelman** — restate the team's assumption in its strongest, most reasonable form. If you can't, you don't understand it well enough to counter it. Attacking a strawman is the #1 CHALLENGE failure mode.
2. **Counter** — voice the user-perspective objection (first person, grounded in a persona).
3. **Falsifiable test** — name the concrete observation that would confirm or refute the challenge (funnel metric, A/B result, support-ticket rate, interview finding). **No test ⇒ drop the challenge.** This converts an argument into a resolvable hypothesis the team can settle.
4. **Verdict** — `SURVIVES` (assumption holds), `WEAKENED` (holds with caveats), or `KILLED-pending-test` (likely wrong, run the test). The test settles it, not Echo[demand].

**Quality signals**:
- Each challenge steelmans the assumption before countering it
- Every challenge carries a falsifiable test; zero "untestable" challenges ship
- Each challenge closes with a verdict + the test that resolves it
- Challenges are specific, not generic; at least 1 targets a deeply held team assumption
- Calibration ceiling is `[hypothesis]` — challenges are testable claims, never presented as user fact

## DEEP Mode

**Purpose**: Thorough demand exploration for a single feature area.

**When**: Pre-design phase, feature refinement, competitive gap analysis.

**Persona selection**: 3-5 personas with different relationships to the feature. Include power user, first-time user, and edge-case user.

**Output benchmark**: 8-12 requests, all focused on the target feature. Include: primary use case, edge cases, error scenarios, and adjacent needs.

**Quality signals**:
- Requests cover the full user journey for the feature
- Edge cases and error scenarios are included
- Adjacent/complementary needs are surfaced

## COMPETE Mode

**Purpose**: Voice demands based on competitor experiences.

**When**: Competitive analysis, differentiation strategy, feature parity assessment.

**Persona selection**: Users who actively use competitor products. Include: recent switcher, dual-user, evaluating buyer.

**Output benchmark**: 8-15 requests explicitly referencing competitor experiences. Each request includes: what the competitor does, why the user values it, and what's missing here.

**Quality signals**:
- Specific competitor features are named
- Emotional tone reflects genuine frustration ("App X does this in one click...")
- Requests distinguish must-have parity from nice-to-have

## EDGE Mode

**Purpose**: Surface demands from minority and extreme use cases.

**When**: Accessibility review, inclusivity audit, edge-case discovery.

**Persona selection**: Focus on underrepresented segments. Include: screen reader user, low-bandwidth user, non-native language speaker, elderly user, child (if applicable).

**Output benchmark**: 8-12 requests from 4+ edge-case personas. Focus on barriers, not features.

**Quality signals**:
- Requests reveal barriers that mainstream users don't experience
- Accessibility needs are specific (not just "make it accessible")
- At least 1 request surfaces a legal/compliance risk

## Cross-Mode Patterns

| Pattern | Sequence | Use When |
|---------|----------|----------|
| Broad → Deep | EXPLORE → DEEP | Start wide, then drill into promising areas |
| Challenge → Validate | CHALLENGE → (Echo validation) | Counter assumptions, then verify in existing UI |
| Compete → Prioritize | COMPETE → (Rank scoring) | Gather competitor-driven demands, then prioritize |
| Edge → Mainstream | EDGE → EXPLORE | Start with minorities, extend patterns to mainstream |

## Assumption Challenge (full template)

Generate user-perspective counterarguments to common team assumptions. Used by the `challenge` Recipe / CHALLENGE mode.

### Common "Curse of Knowledge" Patterns

| Team Assumption | User Reality |
|-----------------|-------------|
| "Everyone knows this term" | Most users don't know industry jargon |
| "They'll find it in settings" | Users don't notice the settings screen exists |
| "They'll read the manual" | Users don't read manuals |
| "Previous version users will understand" | New users are always arriving |
| "The error message explains the cause" | Technical error messages cause fear |
| "They can check the API docs" | Non-engineer users don't know APIs exist |

### Challenge Template

```yaml
ASSUMPTION_CHALLENGE:
  team_assumption: "[What the team believes]"
  steelman: "[The assumption in its STRONGEST form — why a smart team holds it. State this before countering; a challenge that beats only a strawman is worthless.]"
  user_reality: "[What users actually experience]"
  user_voice: "[User's own words as counterargument]"
  evidence_type: "[Behavioral observation / Churn data / Support tickets / Competitor comparison]"
  falsifiable_test: "[The concrete observation that would CONFIRM or REFUTE this challenge — e.g. 'funnel drop-off at step 3 > 20%', 'A/B variant lifts activation'. A challenge with no resolving test is synthetic FUD; drop it.]"
  impact: "[Impact if this assumption is wrong]"
  verdict: "SURVIVES | WEAKENED | KILLED-pending-test  # synthetic verdict — the falsifiable_test settles it, not Echo[demand]"
  calibration: "[hypothesis]  # ceiling until the test runs; a synthetic challenge is never user fact"
```
