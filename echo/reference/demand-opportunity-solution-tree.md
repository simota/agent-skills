# Opportunity Solution Tree Reference

Purpose: Connect a single business outcome to the experiments that move it, via a visible tree of opportunities and candidate solutions. From Teresa Torres' *Continuous Discovery Habits*. Forces teams to enumerate opportunities *before* solutions and to design experiments *under* solutions — preventing solution-first thinking and output-framed roadmaps. In Echo[demand]'s hands, the tree is populated with synthetic user opportunities (unmet needs, pain points, desires) channeled from personas, then routed to real teams for prioritization and validation.

## Scope Boundary

- **echo `opportunity`**: builds an OST anchored on a stated outcome. Outputs the four-layer hierarchy (Outcome → Opportunity → Solution → Experiment) populated with synthetic content.
- **echo `request` (default)**: list of feature requests, not structured into a tree. Use OST when the question is "where should we invest discovery effort?" rather than "what do users want?"
- **echo `need`**: lateral blind-spot scan. OST is hierarchical and outcome-anchored.
- **echo `jtbd`**: a JTBD analysis is upstream of OST — the job statement often becomes the outcome or first-level opportunity. JTBD is forces-and-stages; OST is hierarchy-and-experiments.
- **echo `5whys`**: cleans up a single request into a root need. OST organizes *many* needs against *one* outcome.
- **Field (elsewhere)**: real-user OST evidence. Field runs ongoing interviews and populates real opportunities from transcripts. Echo[demand] generates a synthetic seed tree to compare against.
- **Spark (elsewhere)**: takes a chosen solution branch and produces a feature spec. Echo[demand] stops at the experiment level — Spark elaborates the solution into shippable scope.
- **Experiment (elsewhere)**: designs and runs the actual test. Echo[demand] drafts experiment hypotheses; Experiment owns sample size, instrumentation, and analysis.
- **Voice (elsewhere)**: real review/support sentiment that should populate opportunity nodes. Echo[demand] generates synthetic opportunities to triangulate with Voice.

## Workflow

```
ANCHOR     →  state the outcome — a measurable change in user behavior
           →  reject output framing ("ship feature X") and OKR confusion ("hit target Y")

STRIP      →  enumerate opportunities under the outcome. Each is an unmet need,
           →  pain, or desire — *not* a solution. Phrased in user voice.
           →  cluster duplicates; split fat opportunities into specific sub-opportunities.

BRANCH     →  for each opportunity, builder 2-4 candidate solutions.
           →  resist anchoring on the first solution that comes to mind.
           →  include "do nothing" or "non-product" options when honest.

EXPERIMENT →  for each solution, design the smallest test that would reduce
           →  the largest risk. Must have: hypothesis, leading indicator,
           →  decision rule (what would make us drop this branch?).

PRUNE      →  rank opportunities by impact × evidence × strategic fit
           →  prune low-evidence + low-impact branches; retain a few high-uncertainty
           →  high-impact branches as exploration bets.
           →  SYNTHETIC-TREE CAVEAT: every node is self-generated, so the evidence axis is
           →  near-zero by construction — do NOT cut a high-impact branch for "low evidence"
           →  (circular). The evidence axis must split "no real evidence yet → validate" from
           →  "implausible AI artifact ([synthetic-only]) → cut". Prune only the latter.
           →  Name the LOAD-BEARING opportunity: highest impact × highest synthetic-uncertainty —
           →  if it's wrong, the most of the tree collapses. Field validates this node FIRST.

CADENCE    →  schedule the tree as a living artifact — weekly review, weekly experiment
           →  treat opportunities as discovered (not invented); add as research arrives.

DELIVER    →  hand tree to Field for population validation,
           →  to Spark for solution elaboration,
           →  to Experiment for test execution.
```

## The Four-Layer Hierarchy

| Layer | What it is | Phrased as | Cardinality |
|-------|-----------|------------|-------------|
| Outcome | Measurable user-behavior change | "Increase weekly active editing sessions" | 1 per tree |
| Opportunity | Unmet user need / pain / desire | "I can't pick up where I left off" | 5-15 per outcome |
| Solution | Candidate intervention | "Auto-resume last session" | 2-4 per opportunity |
| Experiment | Smallest test of the riskiest assumption | "Prototype + 5 unmoderated tests" | 1-3 per solution |

Strict rule: **every layer above must constrain the layer below**. A solution that doesn't trace cleanly to an opportunity, which traces to the outcome, gets cut. This is the discipline OST enforces.

## Outcome Anchoring

A real outcome is:
- **Behavioral**: something the user *does* differently
- **Measurable**: countable from product instrumentation
- **Causally connected**: improving it should drive business goals

| Anti-pattern | Example | Why it fails |
|--------------|---------|--------------|
| Output framing | "Ship the new editor by Q3" | Describes shipping, not user behavior |
| Business KPI | "Increase ARR by 20%" | Too far from user behavior; can't tree under it |
| Vanity metric | "More signups" | Not connected to value delivery |
| Activity metric | "Reduce open tickets" | Internal team activity |
| Real outcome | "Increase share-link clicks per active user per week" | Behavioral, measurable, leading |

If the stated outcome is wrong, fix it before populating the tree.

## Opportunity Stripping

Phrase every opportunity as the user would describe their pain or unmet desire — not as the team would describe a problem.

| Reject | Accept |
|--------|--------|
| "Performance issues" (team frame) | "I keep refreshing because I don't know if my changes saved" |
| "Need onboarding" (solution-flavored) | "I opened the app and didn't know what to do first" |
| "Better integrations" (vague) | "I lose 10 min every morning copying data from spreadsheet to dashboard" |

Cluster duplicates. Split overly broad opportunities (e.g. "the experience is slow") into specific friction points until each is testable.

## Solution Branching

For each opportunity, generate at least 2 solution candidates *before* picking one. Single-solution opportunities indicate anchoring bias.

```yaml
OPPORTUNITY_NODE:
  text: "[User-voice unmet need]"
  evidence: { real: [refs], synthetic: [refs] }
  calibration: "[hypothesis]"   # [synthetic-only] if it reads as an AI artifact; [supported]/[validated]
                                # only with a cited real/Voice/Field match (reference/calibration.md).
                                # Only [validated]/[supported] nodes are growth-acceptance Insight-Ledger-citable.
  parent_outcome: "[Outcome ID]"
  solutions:
    - id: S1
      summary: "[Intervention]"
      experiments:
        - hypothesis: "[If we ship S1, then [behavior change], because [reason]]"
          riskiest_assumption: "[The thing most likely to break]"
          test: "[Smallest action that tests it]"
          leading_indicator: "[What we'd measure in <1 week]"
          decision_rule: "[Threshold below which we drop this branch]"
    - id: S2
      summary: "[Alternative intervention]"
      experiments: [ ... ]
```

## Experiment Design

Each experiment must answer: **what is the smallest test that would reduce the largest risk?**

| Element | Bad | Good |
|---------|-----|------|
| Hypothesis | "S1 will help users" | "If we auto-resume sessions, retention day-2 rises ≥3pp, because users currently churn from re-orientation cost" |
| Riskiest assumption | not stated | "Users notice and trust the auto-resume" |
| Test | "Build and ship" | "Clickable prototype + 5 unmoderated user tests" |
| Leading indicator | "Retention" (lagging) | "Time-to-first-meaningful-action in test, ≤30s" |
| Decision rule | not stated | "If <3/5 testers reach the resumed state without help, kill branch" |

Bad experiments are large, late, and lack a kill rule. Good experiments are small, early, and have explicit failure criteria.

## Weekly Cadence (Continuous Discovery Habits)

Torres' habits are weekly, not quarterly:
- **Weekly interviews**: at least 1 customer interview per week (Field).
- **Weekly tree update**: add new opportunities, deprecate stale ones, mark experiments closed.
- **Weekly experiment**: at least one experiment running.
- **Weekly opportunity selection**: pick the next opportunity to invest in based on evidence and impact.

The tree is a living artifact. A static OST is a roadmap by another name and defeats the purpose.

## Anti-Patterns

- **Solution-first thinking**: starting with a solution and reverse-engineering an opportunity to justify it. Build top-down.
- **Output framing**: anchoring the tree on "ship X" instead of a behavioral outcome.
- **OKR confusion**: using a quarterly business KPI as the outcome (too lagging, too far from user behavior). Use a *user-behavior* outcome that drives the OKR.
- **Single solution per opportunity**: indicates anchoring; force at least 2 candidates.
- **No kill rule on experiments**: without decision rules, every branch lives forever — defeats pruning.
- **Tree as one-time artifact**: built once, never revisited. OST only works as a continuous habit.
- **Mixing real and synthetic evidence without tags**: synthetic opportunities that look real cause over-confident prioritization. Always tag `synthetic: true` and a per-node `calibration` on Echo[demand]-generated nodes.
- **Skipping the prune step**: a 50-node tree without pruning is a wishlist, not a discovery artifact.
- **Circular prune on a synthetic tree**: cutting a high-impact branch because it has "low evidence" — but YOU generated every node, so all evidence is synthetic. Cut only `[synthetic-only]` implausible nodes; high-impact `[hypothesis]` nodes go to Field to validate, not the bin.
- **No load-bearing node named**: shipping the tree without flagging which opportunity, if wrong, collapses the most branches — Field then validates in the wrong order.

## Handoff

- **To Field**: synthetic tree as scaffolding. Field runs weekly interviews and replaces synthetic opportunity nodes with real-user-evidenced ones, **starting with the load-bearing opportunity** (highest impact × uncertainty). Tag swap status and promote `calibration` (`[hypothesis]` → `[supported]`/`[validated]`) as real evidence arrives.
- **To Spark**: chosen solution branch → feature spec. Echo[demand] hands the solution + winning experiment results; Spark elaborates scope.
- **To Experiment**: experiment hypothesis + riskiest assumption + decision rule → test execution. Experiment owns instrumentation and analysis.
- **To Rank**: opportunities + impact × evidence × strategic-fit scores → prioritization output.
- **To Scribe[unified]**: outcome-level statement + retained opportunity branches → spec-package "why" section.
- **To Voice**: cross-check synthetic opportunity nodes against real review/support text — convergence raises confidence; divergence flags hypothesis weakness or coverage gap.
- **To Cast**: PERSONA_FEEDBACK on which personas surfaced which opportunity branches — coverage signal for the persona registry.
