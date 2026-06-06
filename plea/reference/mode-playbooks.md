# Mode Playbooks

Purpose: Detailed execution guide for each of Plea's 5 request generation modes.

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

**Quality signals**:
- Challenges are specific, not generic
- Each challenge includes a concrete "what if" scenario
- At least 1 challenge targets a deeply held team assumption

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
