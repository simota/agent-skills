# Learning Design Frameworks

Read when authoring objectives, choosing cognitive levels, or mapping prerequisites.

## Backward Design (Understanding by Design — Wiggins & McTighe)

Design in three stages, in order:
1. **Identify desired results** — what the learner should know/do (objectives, outcome definition).
2. **Determine acceptable evidence** — how mastery is demonstrated (assessments, rubrics).
3. **Plan learning experiences** — activities, materials, and lessons that build toward the evidence.

Never invert the order. Authoring lessons before objectives and assessment exist produces content that cannot be measured.

## Bloom's Taxonomy (Revised — Anderson & Krathwohl)

Six cognitive levels, low to high. Pick a level per objective and use an observable verb from that level.

| Level | Demonstrates | Sample verbs |
|-------|-------------|--------------|
| Remember | Recall facts | define, list, name, recall, label |
| Understand | Explain ideas | explain, summarize, classify, paraphrase, describe |
| Apply | Use in new situations | implement, execute, solve, use, demonstrate |
| Analyze | Draw connections | differentiate, compare, organize, deconstruct, attribute |
| Evaluate | Justify a stance | critique, judge, defend, assess, justify |
| Create | Produce new work | design, construct, compose, generate, author |

**Banned vague verbs** (not observable): understand, know, learn, appreciate, be familiar with, grasp. Only allowed when paired with an observable demonstration ("understand X, demonstrated by explaining X in their own words").

### Level calibration by learner stage
- **Beginner**: weight Remember / Understand / Apply.
- **Intermediate**: weight Apply / Analyze, some Evaluate.
- **Advanced**: weight Analyze / Evaluate / Create.

Do not assess above the Bloom's level the objectives and materials prepared the learner for.

## Objective Formulation (ABCD + SMART)

A well-formed objective states:
- **Audience** — who the learner is.
- **Behavior** — observable verb (Bloom's-leveled).
- **Condition** — under what circumstances / with what tools.
- **Degree** — the success threshold (accuracy, time, completeness).

ID each as `LO-001`. Example: *"Given a dataset and pandas (condition), the intermediate learner (audience) will compute (Apply) group-wise aggregates (behavior) with no runtime errors on the first attempt (degree)."*

Make the degree measurable: "≥ 8/10 correct", "within 15 minutes", "matching the reference output". Reject objectives with no degree.

## Prerequisite Mapping

- List prior knowledge/skills the learner must hold before module 1.
- Author a **prerequisite check** (short diagnostic) so learners self-identify gaps.
- Build a prerequisite chain across modules: module N may depend on objectives from earlier modules. Sequence to respect dependencies — never assess a skill before its prerequisite is taught.
- Define a **learner profile**: level, goal, time budget, motivation, constraints.

## Outcome Definition

Distinct from objectives: outcomes are the end-state capabilities after the full curriculum (e.g., "can ship a small production API"). Map each outcome to the set of objectives that compose it.
