# Instructor Support & Progress Tracking

Read when authoring facilitator guides, coaching prompts, common-mistake catalogs, progress trackers, or feedback templates.

## Facilitator Guide

Per session/module, give the instructor:
- Objectives and the intended takeaway.
- Timing and pacing notes (where learners typically need more time).
- Discussion prompts and questions to pose.
- The check-for-understanding and what a passing response looks like.
- Materials/setup required ahead of time.

## Workshop Plan

For live/cohort delivery: agenda with timings, activity transitions, group vs individual segments, breaks, and the artifacts produced by the end. Include a "if running behind" cut list and a "if ahead" stretch list.

## Coaching Prompts

Open-ended questions a coach/mentor asks to move a learner forward without giving the answer:
- Diagnostic: "Walk me through what you expected vs what happened."
- Socratic: "What would change if the input were empty/huge/malformed?"
- Reflective: "Which part felt shaky — and what would make it solid?"
- Stretch: "How would you explain this to someone who's never seen it?"

Tie prompts to the module's objectives and common stumbling points.

## Common Mistakes Catalog

Per module, the highest-leverage instructor artifact. For each typical error:
- **Symptom** — what the learner does/says.
- **Root cause** — the underlying misconception.
- **Remedy** — the concrete intervention (re-explanation, counter-example, exercise).

Beginners need failure modes pre-empted, not just the happy path. LLM-generated curricula over-index on the happy path — deliberately enumerate where learners stumble.

## Feedback Templates

Reusable structures for actionable feedback:
- **Strengths / Growth / Next step** — name what worked, what to improve, one concrete next action.
- Tie each comment to a rubric criterion so feedback is non-arbitrary.
- Prefer specific over global ("your aggregation logic double-counts nulls" over "needs work").

## Progress Tracking

| Artifact | Contents |
|----------|----------|
| `study_tracker.csv` | Headered: `date, module, objective_ids, time_spent_min, status, notes`. Status: not-started / in-progress / done / needs-review |
| `review_schedule.md` | Spaced-repetition plan — expanding intervals (e.g., 1d, 3d, 7d, 21d) per concept |
| `reflection_template.md` | Periodic prompts: what I learned, what's still unclear, what I'll do next |
| `habit_plan.md` | Cadence, triggers, and minimum daily/weekly commitment to sustain study |

Checkpoints (see assessment-rubrics.md) feed the tracker: each closed checkpoint advances the learner's recorded status.
