# Inversion Method Reference

Purpose: Solve forward problems by working backward from failure. Charlie Munger's inversion mental model — "invert, always invert" (borrowed from Carl Jacobi) — asks not *how do we succeed* but *what would guarantee failure?*, then systematically avoids those paths. Nassim Taleb's *via negativa* generalizes this: improvement by subtraction (remove what makes things fragile) rather than addition. Inversion fires best when forward analysis is saturated, when survivorship bias clouds the picture, or when goal-positive framing has masked obvious failure modes.

## Scope Boundary

- **flux `inversion`**: invert the goal, enumerate failure-guarantees, derive avoid-list. Produces failure-mode list with avoidance actions, not full RPN scoring.
- **flux `reframe` (default)**: full DEEP pipeline. Inversion is one tool in CHALLENGE; this subcommand isolates it.
- **flux `challenge`**: First Principles and Assumption Reversal. Reversal flips assumptions; inversion flips the *goal*.
- **flux `shift`**: perspective rotation across stakeholders/timeframes. Shift rotates viewpoint; inversion negates the objective.
- **flux `analogy`**: source-domain mapping. Analogy borrows shape; inversion subtracts.
- **omen (elsewhere)**: pre-mortem with RPN/AP scoring of failure modes. Inversion *generates* failure scenarios; Omen *quantifies and ranks* them. Inversion is upstream — feed Omen.
- **riff (Subtract mode, elsewhere)**: iterative subtraction dialogue. Inversion is a single-pass goal-flip; Riff Subtract is multi-turn pruning.
- **void (elsewhere)**: YAGNI scope cutting. Void removes work-not-yet-done; inversion surfaces failure-paths to avoid.

## Workflow

```
ENTER    →  state the goal in positive form
         →  capture context, constraints, desired outcome

INVERT   →  rewrite the goal as its negation
         →  "succeed at X" → "guarantee failure at X"

ENUMERATE →  list ≥10 ways to guarantee that failure
          →  use prompt bank: behaviors, structures, decisions, omissions

CLUSTER  →  group failure-paths by mechanism (technical, social,
            economic, cognitive, temporal)

AVOID    →  derive avoid-list — concrete actions / non-actions
         →  each failure-path → at least one avoidance commitment

VIA NEG  →  apply Taleb subtraction — what to *stop doing* often
            outranks what to start doing

DELIVER  →  hand to Omen (RPN/AP scoring), Magi (decision), or
            user (avoidance commitments)
```

## Munger's Inversion Prompts

- If we wanted to *guarantee* this fails, what would we do?
- What does the failure case look like in detail? Walk it forward.
- Who has tried this and failed? What did they do? (Survivorship-bias antidote.)
- What would a saboteur recommend, knowing the team's blind spots?
- What is the team currently doing that resembles items on the failure list?
- If success requires N things to go right, what is each thing's failure mode?

## Via Negativa (Taleb) Prompts

- What can we *stop doing* that would make this more robust?
- What dependency, if removed, reduces fragility?
- What feature/process/policy adds risk without proportional value?
- What "best practice" are we doing because it is conventional, not because it works?
- Which addition has, historically, made similar systems worse?

## Failure-Mode Categories (enumeration scaffold)

| Category | Example failure-paths |
|----------|-----------------------|
| Technical | Single point of failure, untested critical path, dependency on deprecated API |
| Social | Key person dependency, unaligned incentives, decision-by-consensus on irreversible calls |
| Economic | Negative unit economics masked by growth, cost surprise at scale, vendor lock-in |
| Cognitive | Confirmation bias in metrics, sunk cost commitment, planning fallacy on timeline |
| Temporal | Race condition between teams, market window miss, regulatory deadline misread |
| Structural | Misaligned org-to-system boundary, ownership ambiguity, escalation path missing |

Aim for coverage across categories — single-category failure lists betray a blind spot.

## What-Not-To-Do Anti-Bias

Forward planning is positive-action biased: teams list what to do, not what to stop. Inversion's main value is extracting the *negative* commitments — items the team will not do, paths it will not take, additions it will refuse. These are typically underweighted in planning artifacts and overweighted in postmortems.

## Anti-Patterns

- Inversion-as-rhetoric — saying "let's invert" then continuing forward analysis. Inversion requires actually rewriting the goal as its negation.
- Stopping at 3 failure-paths — the obvious ones surface first. Push to ≥10 to reach non-obvious paths.
- Single-category enumeration — listing only technical failures (or only social ones). Force coverage across all 6 categories.
- Conflating with pre-mortem — inversion *generates* failure scenarios; pre-mortem (Omen) *quantifies* them. Don't skip the handoff.
- Avoidance-list without commitment — listing "don't do X" without an owner or trigger creates theater, not behavior change.
- Survivorship-blind inversion — citing only the failure paths the team already discusses. Seek failure paths from others' postmortems.
- Inverting the wrong granularity — inverting "succeed at the project" is too coarse. Invert specific decisions, milestones, or assumptions.
- Treating via negativa as nihilism — the goal is not to remove everything, but to identify the *fragile-additions* whose removal increases robustness.
- Skipping the avoid-list step — failure-paths without avoidance commitments are entertainment.

## Handoff

- **To Omen**: failure-path list as candidates for RPN/AP scoring and pre-mortem ranking. Inversion is the *generation* engine; Omen is the *prioritization* engine.
- **To Magi**: when avoidance commitments conflict with proposed actions — decision needed.
- **To Riff (Subtract mode)**: via negativa candidates — iterate on what to stop doing.
- **To Spark**: failure-paths sometimes invert into feature ideas (the avoidance becomes the differentiator).
- **To Void**: avoidance commitments that imply scope cuts.
- **To `analogy`**: failure-paths that resemble known patterns from other domains — borrow their countermeasures.
- **To User**: final avoidance commitments with owners and triggers, alongside the original forward plan.
