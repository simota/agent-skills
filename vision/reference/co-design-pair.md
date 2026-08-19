# Co-Design Pair Mode

Interactive, decision-by-decision co-design where Vision acts as the **driver** (proposes grounded design decisions and directs the cluster to produce them) and the user acts as the **navigator** (chooses among options, steers taste and direction, confirms each increment). Unlike batch `direction` (produce the whole direction doc, present once) or `multi` (a one-shot portfolio to pick from), co-design pair is a conversation: propose one decision as options, agree, produce it (directly recorded or via delegation), confirm, then advance.

## When to Use

| Use co-design pair | Use batch `direction` / `multi` |
|--------------------|----------------------------------|
| Live co-design session, want to steer taste as you go | Direction can be produced then reviewed |
| High-subjectivity brand/aesthetic calls that emerge in dialogue | Scope + brand are already settled |
| Stakeholder wants to own each decision | A portfolio of options for a single pick (`multi`) |
| User explicitly asks to "design together" / "decide as we go" | Standard direction request |

Vision stays a **cue**: it writes no code even in pair mode. When a decision needs a produced artifact (tokens, a prototype, motion), Vision delegates to the cluster (Muse/Forge/Flow/Palette/Frame/Prose) via Nexus and brings the result back for confirmation.

## Roles: Driver / Navigator Separation

- **Vision = Driver.** Proposes the next design decision as 2-3 grounded options (each with rationale, trade-offs, a measurable outcome metric, and a WCAG note), directs production, and shows the increment. Owns *how* the direction is built to Vision's evidence bar.
- **User = Navigator.** Owns *what* and *whether* — picks among options, sets taste and brand direction, redirects, decides pace. In design the navigator is especially central: taste and brand ownership are the user's.
- **Options are the steering wheel.** Vision's "3+ options with trade-offs" rule becomes the per-increment interaction: Vision offers, the user steers by choosing.

This mirrors Builder's pair-programming (skill = driver, user = navigator), NOT Judge's pair-review (skill = report-only navigator that spawns a driver). Vision is a design *generator*; the artifact it drives is the direction/system, not code.

## Protocol

```
SETUP:
  - Agree on the design goal + brand/constraints + success metrics (task-success / conversion / time-on-task).
  - Draft an ordered decision plan (smallest meaningful decisions):
    direction/mood → principles → token direction → key-screen concept → interaction/motion → copy voice.

LOOP until the direction is locked or the user ends the session:
  1. Vision proposes the NEXT decision as 2-3 grounded options
     - each: rationale (evidence, not "looks better"), trade-offs, outcome metric, WCAG 2.2 AA note
  2. User decides: pick / blend / adjust / redirect / defer
  3. Vision records the chosen decision; if it needs a produced artifact, delegate via Nexus
     (Muse=tokens · Forge=prototype · Flow=motion · Palette=interaction · Frame=Figma · Prose=copy)
  4. Vision shows the increment + how it meets the metric + the a11y check
  5. User confirms (accept) or iterates (bounded — max 2 turns/decision)
  6. Checkpoint. Advance to the next decision.

CLOSE:
  - Assemble the direction doc + downstream delegation stubs.
  - VALIDATE: dark-pattern scan, WCAG 2.2 AA, handoff readiness.
  - Present a session summary + handoff.
```

## Interaction Contract

- **One decision at a time, options-first.** Never dump the full direction then ask for a single approval; offer 2-3 options per decision and let the user steer.
- **Evidence on every option.** Each option carries rationale + trade-offs + a measurable outcome metric + a WCAG note — Vision's "no aesthetic decision without data" rule holds per increment.
- **Vision stays a cue.** Vision writes no code; when a decision needs an artifact, delegate to the cluster and bring the result back — never self-implement.
- **Show the increment.** Do not advance until the user has seen the decision (or produced artifact) and confirmed.
- **User drives pace and taste.** Vision proposes and waits; brand/taste ownership is the user's.
- **Bounded.** Max decisions (default 12) / user-stop / direction-locked / diminishing-returns. On bound, assemble the decisions so far into a standard direction doc.
- **Checkpoint-resumable.** Persist the decision log so an interrupted session resumes from the last confirmed decision (`pair resume`).

## Delegation Within a Pair Session

Vision does not produce tokens, prototypes, or code. When an increment needs a produced artifact:
- Delegate through Nexus to the owning skill (Muse/Forge/Flow/Palette/Frame/Prose) with scope + constraints + the agreed decision + success metric.
- Bring the produced artifact back into the session and show it against the metric + a11y check before advancing.
- The per-decision confirmation gate applies to delegated production too (one confirm per increment).

## Under AUTORUN

Co-design pair is INTERACTIVE and cannot run unattended. Under AUTORUN / Nexus AUTORUN:
- Run UNDERSTAND, draft the ordered decision plan + the first decision's 2-3 options, and return `_STEP_COMPLETE` with `Next: USER` (pair-ready).
- Do **not** lock decisions or trigger production without confirmation.

## Output

At session end, emit a compact summary:

```
Co-Design Pair Summary
- Goal:       [what was being designed]
- Decided:    [decisions locked, with the chosen option + metric]
- Delegated:  [artifacts produced via Muse/Forge/Flow/Palette/Frame/Prose]
- Deferred:   [decisions the user set aside]
- Remaining:  [undecided items from the plan]
- Validation: [dark-pattern / WCAG 2.2 AA / handoff-readiness verdict]
- Handoff:    [downstream stubs — Muse/Palette/Flow/Forge/Frame/Prose / next decision]
```
