# Assessment, Rubrics & Alignment

Read when designing quizzes, rubrics, self-assessment, or running the alignment audit.

## Constructive Alignment

Objectives, learning activities, and assessment must point at the same target (Biggs). Operationalize via an **alignment matrix**:

| LO-ID | Bloom's level | Material(s) | Assessment item(s) | Status |
|-------|---------------|-------------|--------------------|--------|
| LO-001 | Apply | exercises §2 | quiz Q3, Q4 | Covered |
| LO-002 | Analyze | reading §4 | — | ALIGNMENT_GAP |

Flags:
- `ALIGNMENT_GAP` — an objective with no assessment evidence.
- `ORPHAN_ASSESSMENT` — an assessment item that traces to no objective.

A curriculum with either flag is not yet teachable; resolve before delivery.

## Assessment Type Selection

| Type | Measures | Good for Bloom's |
|------|----------|------------------|
| Multiple-choice quiz | Recall, discrimination | Remember, Understand |
| Short answer / explanation | Reasoning | Understand, Analyze |
| Applied exercise / coding task | Skill execution | Apply, Analyze |
| Project / portfolio | Synthesis | Create, Evaluate |
| Peer / self-assessment | Reflection, metacognition | any (formative) |

Match assessment Bloom's level to the objective. Do not assess at a higher level than taught.

## Quiz Authoring (`quizzes.csv`)

Headered CSV. Columns: `id, lo_id, question, option_a, option_b, option_c, option_d, correct_answer, explanation, blooms_level`.
- Every quiz row carries its `lo_id` for traceability.
- Distractors must be plausible (target known misconceptions), not filler.
- `explanation` states why the answer is correct AND why common distractors are wrong.

## Rubric Authoring (`rubric.md`)

A rubric is a criteria × levels grid. Standard 4-level scale:

| Criterion | Novice | Developing | Proficient | Exemplary |
|-----------|--------|-----------|------------|-----------|
| (criterion) | (descriptor) | (descriptor) | (descriptor) | (descriptor) |

Rules:
- Descriptors are observable and distinguishable — a grader should land on the same level independently.
- Criteria derive from the objectives being assessed.
- Avoid single-word descriptors ("Good", "Poor"); describe what the work shows.

## Self-Assessment

Give learners a checklist or "I can…" statements mapped to objectives, plus a confidence scale. Self-assessment is formative — it guides study, it does not grade.

## Final-Project Evaluation

Combine the project brief's acceptance criteria with a rubric. State the passing threshold and how the score maps to the outcome definition.

## Progress Checkpoints

Place checkpoints at module boundaries. Each checkpoint: which objectives it verifies, the evidence (quiz/exercise/project), and the remediation path if the learner does not pass.
