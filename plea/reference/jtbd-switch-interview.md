# Jobs-to-be-Done Switch Interview Reference

Purpose: Generate synthetic JTBD artifacts (Switch interview transcripts, four-forces analyses, Job Maps) when real customer interviews are unavailable or as a triangulation hypothesis to test against real data. Grounded in Christensen's "Milkshake" framing and Moesta/Spiek's Switch interview method. Surfaces the *progress* a user is trying to make rather than the demographic profile, separating functional, emotional, and social dimensions of the same job.

## Scope Boundary

- **plea `jtbd`**: synthetic Switch interview, four-forces table, Job Map, and competing-job analysis from a stated job. Outputs are hypotheses framed in user voice.
- **plea `request` (default)**: persona-led feature requests. Use when the question is "what do users want?" rather than "what progress are they hiring for?"
- **plea `need`**: surfaces team blind spots via curse-of-knowledge patterns — broader than one job.
- **plea `challenge` / `roleplay`**: assumption pushback / deep persona embodiment — not job-anchored.
- **Researcher (elsewhere)**: owns *real-user* JTBD. Real Switch interviews, video coding, and forces ranking from live transcripts are Researcher's domain. Plea generates *synthetic* JTBD as a hypothesis seed — Researcher validates with humans.
- **Spark (elsewhere)**: turns JTBD into feature spec. Plea stops at "the job and the forces"; Spark designs the solution.
- **Voice (elsewhere)**: real feedback analysis. Voice tells you what users said; Plea simulates what users *would* say if interviewed under the Switch protocol.

## Workflow

```
SCOPE      →  state the candidate job-to-be-done (verb + object + context)
           →  list known struggling moments (when does the user "fire" the current solution?)

CHANNEL    →  channel 3+ personas who plausibly hire for this job
           →  for each: first thought, push, pull, anxiety, habit

INTERVIEW  →  run synthetic Switch script: First Thought → Passive Looking → Active Looking
           →  → Deciding → Consuming → Satisfaction. Generate quotes for each beat.

FORCES     →  fill four-forces table per persona (push/pull/anxiety/habit)
           →  flag dominant force; jobs only switch when push + pull > anxiety + habit

MAP        →  produce Job Map across 8 stages (Define → Locate → Prepare → Confirm
           →  → Execute → Monitor → Modify → Conclude). Tag functional/emotional/social per stage.

COMPETE    →  list competing jobs (alternatives the user could "hire" — including non-obvious ones)
           →  surface unexpected substitutes (doing nothing, asking a friend, a spreadsheet)

DELIVER    →  hand off to Researcher for validation, Spark for solution, Accord for spec
```

## The Four Forces

| Force | Direction | What it represents | Sample synthetic prompt |
|-------|-----------|--------------------|-------------------------|
| Push of the situation | Toward switching | Pain with the current solution | "What was happening the day you decided you'd had enough?" |
| Pull of the new solution | Toward switching | Attraction of the alternative | "What did you imagine your life would look like with the new option?" |
| Anxiety about the new | Against switching | Fear of the unknown, switching cost | "What worried you about trying it? What stopped you from buying sooner?" |
| Habit of the present | Against switching | Inertia, sunk cost, comfort | "Why did you keep using the old way even though it wasn't working?" |

A switch only happens when **(push + pull) > (anxiety + habit)**. Synthetic outputs that show pull alone are incomplete — every JTBD output must populate all four forces.

## The Job Map (Universal 8 Stages)

| Stage | What the user is doing | Example friction surface |
|-------|------------------------|--------------------------|
| Define | Determining objectives, planning inputs | Unclear success criteria |
| Locate | Gathering required items / information | Hard to find inputs |
| Prepare | Setting up, organizing | Setup overhead |
| Confirm | Verifying readiness | Uncertainty before committing |
| Execute | Performing the core job | Core friction |
| Monitor | Checking progress while executing | Lack of visibility |
| Modify | Adjusting based on signals | Hard to course-correct |
| Conclude | Finishing, putting away | Cleanup burden |

For each stage, separate the three dimensions:
- **Functional**: what physically/digitally needs to happen
- **Emotional**: how the user wants to feel during this stage
- **Social**: how the user wants to be perceived by others

## Switch Interview Script Template

```yaml
SWITCH_INTERVIEW:
  job_statement: "When [situation], I want to [motivation], so I can [expected outcome]"
  persona: "[Channeled persona name + archetype]"
  timeline:
    first_thought: "[When did the idea of switching first enter your mind?]"
    passive_looking: "[What were you noticing without actively searching?]"
    active_looking: "[When did you start actively comparing options?]"
    deciding: "[What tipped you over the edge?]"
    consuming: "[What was the first use like?]"
    satisfaction: "[Did the new solution deliver the progress you wanted?]"
  quotes: "[3-5 first-person quotes per beat, in the persona's voice]"
```

## Competing-Job Analysis

List every alternative the persona *could* hire — including non-obvious substitutes:
- Direct competitor product
- Adjacent category product
- Manual workaround (spreadsheet, paper, asking a coworker)
- Doing nothing / tolerating the pain
- Hiring a person to do it

For each, score: cost, switching effort, social signal, expected progress. The often-winning alternative is "doing nothing" — every JTBD output must explicitly consider it.

## Anti-Patterns

- **Demographic JTBD**: writing the job as "busy moms aged 30-45 want X." Demographics are not a job. Anchor on situation + motivation + outcome.
- **Feature-flavored jobs**: "users want a dashboard" is a solution, not a job. The job is *the progress* the dashboard would deliver.
- **Only listing pull**: skipping anxiety and habit. Most synthetic JTBD outputs are too optimistic — you must channel the inertia honestly.
- **Single dominant persona**: one persona hires for many jobs; one job is hired by many personas. Generate at least 3 persona×job pairs.
- **Conflating functional with emotional**: "save time" is functional; "feel competent in front of my team" is social. Splitting them surfaces hidden value.
- **Skipping the competing-job step**: if you don't list "doing nothing," you'll over-estimate switch likelihood.
- **Treating synthetic JTBD as evidence**: this is a hypothesis. Always tag outputs `synthetic: true` and route to Researcher for real-user confirmation.

## Handoff

- **To Researcher**: synthetic JTBD as hypothesis seed for real Switch interviews. Researcher recruits real switchers and validates the four-forces ranking. Required: state which forces are highest-uncertainty.
- **To Spark**: validated job statement → solution exploration. Spark designs against the dominant unmet stage on the Job Map.
- **To Accord**: job statement + acceptance criteria phrased as "user achieves [outcome] when [condition]" → spec-package input.
- **To Cast**: PERSONA_FEEDBACK on which job-archetype combinations produced unexpected coverage gaps.
- **To Voice**: cross-check synthetic forces against real review/support sentiment — overlap raises confidence; divergence flags hypothesis weakness.
