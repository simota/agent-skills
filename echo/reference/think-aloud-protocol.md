# Think-Aloud Protocol Reference

Purpose: Moderate a think-aloud usability session where participants verbalize thoughts while completing tasks — the single highest-signal technique for uncovering mental-model gaps, cognitive friction, and unstated assumptions. Concurrent think-aloud (CTA) surfaces problems as they occur; retrospective think-aloud (RTA) preserves task performance at the cost of recall fidelity.

## Scope Boundary

- **echo `aloud`**: moderator script, prompt discipline, transcript coding, and finding extraction for think-aloud sessions (concurrent + retrospective variants).
- **echo `walkthrough` (default)**: persona-based cognitive walkthrough — simulated, not observed. Use when you have no users available.
- **echo `heuristic` (elsewhere)**: expert-review prediction. Pair heuristic findings with think-aloud evidence to promote "predicted" to "confirmed."
- **field `usability` (elsewhere)**: study logistics, recruitment, and statistical design. Field owns study design; `aloud` owns in-session moderation technique.
- **voice (elsewhere)**: captured feedback text analysis at scale — think-aloud is small-n deep, voice is large-n shallow.

## Workflow

```
PREP     →  pilot the task list yourself, time each task, strip ambiguity from prompts
         →  brief participant: "tell me what you're thinking, not what you want me to hear"

WARM-UP  →  neutral verbalization exercise (plan a weekend, describe your morning)
         →  calibrates participant to stream-of-consciousness pacing before the real task

OBSERVE  →  assign task, stay silent until intervention is warranted
         →  use ONLY the permitted prompts (see Prompt Discipline below)

PROBE    →  after task end, ask "what were you trying to do when you…" for key moments
         →  clarify ambiguous verbalizations — do not re-run the task

CODE     →  transcript + video → tag utterances by category (confusion, hypothesis, error, emotion)
         →  timestamp every finding to the on-screen state for evidence

REPORT   →  top findings with participant quotes, frequency across n, severity, fix category
         →  pair quantitative completion + SEQ with qualitative verbalization evidence
```

## Prompt Discipline

Think-aloud sessions fail when the moderator talks too much. Use only this permitted set, exactly as worded, and only when the participant has been silent for >10 seconds:

- "What are you thinking right now?"
- "Keep talking."
- "What do you see on the screen?"
- (Silent presence — often the strongest prompt.)

Banned phrases (each one biases the finding):

- "Can you find the…?" — leads the participant to hunt and inflates task completion.
- "Why did you…?" — makes participants rationalize post-hoc, contaminating the real reason.
- "Did you see the…?" — signals the element is important, invalidating discoverability.
- "Most people click the blue button" — social proof contamination.
- "Oh interesting" / "hmm" — micro-reactions cue the participant to elaborate on whatever just happened.

If a participant asks "did I do that right?", respond with "there are no right answers here" and nothing else.

## Concurrent vs Retrospective

| Attribute | Concurrent (CTA) | Retrospective (RTA) |
|-----------|------------------|---------------------|
| When spoken | During task | After task, with screen recording |
| Task time impact | +20-40% slower | Baseline speed |
| Cognitive load | Added verbalization load | Added recall load |
| Fidelity | High — real-time thought | Lower — reconstructed |
| Best for | Discovery, confusion detection | Benchmark studies, time-sensitive tasks |
| Worst for | Speed / accuracy metrics | Deep mental-model probing |
| Minimum sample | n≥5 for 85% issue coverage | n≥8 (RTA adds recall noise) |

Pick CTA by default. Switch to RTA only when task-completion time matters for the decision (e.g., comparative benchmark, competitive study, publication claims).

## Transcript Coding Categories

Code every utterance into at least one category. Multiple tags are allowed.

| Category | Example utterance | Signal |
|----------|-------------------|--------|
| Hypothesis | "I think this button will take me to…" | Mental model — right or wrong |
| Confusion | "Wait, what is this for?" | Information scent failure |
| Error | "Oh, that's not what I wanted." | Mismatch between expectation and outcome |
| Frustration | "Why is this so hard?" | Friction intensity indicator |
| Delight | "Oh, that's nice." | Positive moment — worth preserving |
| Search | "Where would I find…?" | Findability gap |
| Terminology | "Is a 'workspace' the same as a 'project'?" | Vocabulary mismatch |
| Recovery | "Let me go back and try…" | Recoverable vs dead-end indicator |
| Abandonment | "I'd probably give up here." | Existence proof of task failure |
| Self-blame | "I must be doing something wrong." | Classic sign of UX failure masquerading as user failure |

The "self-blame" category is the most important signal — users blaming themselves for unclear UI is a hidden failure mode that quantitative metrics miss entirely.

## Intervention Rules

The moderator intervenes **only** when:

- Participant has been silent for >10 seconds — use "keep talking" once.
- Participant has been stuck on the same screen for >2 minutes — offer "would you like to move on?"
- Participant shows distress — pause, reset, confirm willingness to continue.
- Technical failure blocks the task — reset and resume with the same task.

Never intervene to:

- Explain UI that the participant isn't finding.
- Confirm or correct a hypothesis.
- Move the participant past a problem "for time" (the stuck moment IS the finding).
- Answer "is this right?" — use "there are no right answers here."

## Sample Size Curve (Nielsen / Sauro)

| n | Issue coverage | Notes |
|---|----------------|-------|
| 3 | ~60% | Directional only |
| 5 | ~85% | Default sweet spot |
| 8 | ~95% | Use when population is heterogeneous |
| 12+ | >98% | Diminishing returns; prefer splitting cohorts |

Over-recruiting is expensive and produces noise. Run 5, analyze, add 3 if issues are still appearing at n=5. If cohorts differ meaningfully (novice vs expert, mobile vs desktop), run 5 per cohort, not 5 total.

## Anti-Patterns

- Banning silence — aggressive prompting biases responses toward moderator cues.
- Paraphrasing during transcription — loses the exact words, which are the evidence.
- Coding only confusion and error — missing the self-blame and delight signals produces an incomplete picture.
- Running think-aloud on first-use without warm-up — participants freeze for the first task, misclassified as "confused."
- Combining think-aloud with SUS during task — cognitive load spike contaminates both signals. Always administer SUS at the end.
- Reporting quotes without timestamps — reviewers can't verify evidence, trust erodes.
- Over-recruiting to 15 users to "be thorough" — past 8, additional users surface mostly noise and drive up analysis cost.
- Forgetting the stuck-moment rule — moderators often rescue participants for kindness, destroying the most important evidence in the session.

## Handoff

- **To Palette**: top 3-5 friction findings with timestamped quote, task, participant count, and recommended fix category.
- **To Echo `heuristic`**: cross-reference think-aloud findings against heuristic predictions — confirmed overlaps are highest-confidence fixes.
- **To Echo `sus`**: pair qualitative findings with the session's SUS score for quant+qual triangulation.
- **To Field**: if think-aloud reveals unexpected user segments or jobs-to-be-done, escalate to structured interview study.
- **To Voice**: friction hotspots found in think-aloud → deploy targeted "what would make this easier?" micro-surveys at the exact friction point.
- **To Prose**: terminology-mismatch findings (e.g., users calling "workspace" a "project") → copy audit.
