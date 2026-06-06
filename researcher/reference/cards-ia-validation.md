# Information Architecture Validation Reference

Purpose: Validate information architecture (IA) through card sorting, tree testing, and first-click testing. Covers open / closed / hybrid card sort design, tree testing (Treejack / PlainFrame), sample-size guidance for IA studies, dendrogram and similarity-matrix analysis, and first-click success thresholds.

## Scope Boundary

- **Researcher `cards`**: IA validation through structured sort / tree-test methods. Category generation, label testing, navigation-path verification, analysis of dendrograms and first-click paths.
- **vs Echo**: Echo runs persona-based cognitive walkthroughs evaluating UI comprehension within a page or flow. Cognitive walkthrough of a UI → Echo; validating whether the navigation structure itself is findable → `cards`.
- **vs Pulse**: Pulse instruments in-product navigation events and measures search / nav funnel performance after launch. In-product nav analytics → Pulse; pre-launch IA validation with moderated or unmoderated participants → `cards`.
- **vs Voice**: Voice mines feedback for "I can't find X" complaints on existing products. Post-launch findability complaints → Voice; proactive IA validation before commit → `cards`.

## Method Selection

| Method | Answers | Use when |
|--------|---------|----------|
| Open card sort | "How do users group these items?" | Early IA work, no existing categories |
| Closed card sort | "Do items fit our proposed categories?" | Validating an existing taxonomy |
| Hybrid card sort | "Do our categories work, and are we missing any?" | Refining a draft IA |
| Tree testing | "Can users find X in this structure?" | Validating a navigation tree |
| First-click testing | "Do users start down the right path?" | Testing specific find-tasks |
| Reverse card sort | "Does our structure match their mental model?" | Late-stage validation before commit |

Default progression: open sort → build hypothesis IA → closed or tree test → first-click on prototypes.

## Sample Sizes for IA Studies

| Method | Minimum n | Recommended n | Rationale |
|--------|-----------|---------------|-----------|
| Open card sort | 15 | 20–30 | Correlations stabilize around 30 (Tullis & Wood, 2004) |
| Closed card sort | 15 | 20–30 | Same correlation basis |
| Tree testing | 50 | 100+ | Task-based, binary success; needs statistical power |
| First-click testing | 20 | 30+ | First-click success correlates 80%+ with task success |
| Moderated IA interview | 5–8 | — | Qualitative depth, not quantitative |

For **multilingual / multi-market IA**: run separate studies per market; do not pool.

## Card Sort Design

- **Card count**: 30–60 cards. Under 30 misses structure; over 80 causes fatigue and dropoff.
- **Card wording**: use real content labels, not feature names. "Reset password" beats "Authentication utility".
- **Card granularity**: consistent level of abstraction — mixing "Settings" with "Change notification sound" biases grouping.
- **Participant brief**: "Group these the way they make sense to you" — do not hint at domain expertise.
- **Open-sort category cap**: none, but flag participants who create >15 categories (often indicates disengagement).
- **Closed-sort forced placement**: always provide an "Unsure" or "Doesn't fit" bucket; forced placement corrupts signal.

## Tree Testing

Tree testing (Treejack, PlainFrame, UserZoom IA) validates a navigation structure without visual design confounds.

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| Success rate | ≥80% | Label and structure support the task |
| Directness | ≥70% | Participants found it without backtracking |
| Time on task | Context-dependent | Compare within study, not absolute |
| First-click success | ≥67% | Strongest predictor of overall task success |

Run **15–25 tasks per test**, each targeting a specific finding. Randomize task order. Budget ~10–15 minutes total per participant.

## First-Click Testing

First-click success is the **single strongest predictor of overall findability** — tasks where the first click is correct succeed ~87% of the time; wrong first click succeeds only ~46% of the time (Bailey et al., 2009).

- Show a static screen, give a task ("Find your billing history"), record the first click location.
- Analyze via click heatmap and success-rate per task.
- A task with <50% first-click success needs label or layout revision before further testing.

## Analysis

### Dendrogram (hierarchical cluster analysis)

- Output of open card sort: a tree showing how often pairs of items were grouped together.
- Read cut-points to identify natural category groupings.
- **Actionable similarity threshold**: typically ≥ 0.60 to 0.70 indicates strong grouping signal.

### Similarity matrix

- Heatmap of co-occurrence: how often each pair of cards appeared together.
- Look for dense "blocks" indicating robust groups, and "bridge" cards that associate with multiple groups — those need careful placement or duplication.

### Standardization grid (closed sort)

- Percentage of participants who placed each card in each category.
- ≥75% agreement: category is clear.
- 50–75%: ambiguous — investigate label or card wording.
- <50%: card does not belong; rework.

## Tool Selection

| Tool | Best for | Notes |
|------|----------|-------|
| Optimal Workshop (OptimalSort, Treejack) | End-to-end card sort + tree test | Industry standard, full analytics |
| UserZoom / UXtweak | Enterprise IA studies | Strong panel integration |
| Maze | Tree test + first-click + prototype test | Fast, integrates with Figma |
| Miro / FigJam + spreadsheet | Moderated card sort, small n | DIY, cheap, no auto-analysis |
| PlainFrame | Lightweight tree testing | Minimal setup |

## Anti-Patterns

- Running tree testing with <50 participants — insufficient for meaningful success-rate CIs.
- Using feature-team language on cards — participants cannot group what they don't recognize.
- Skipping first-click before full usability testing — a wrong first click means you are measuring recovery, not findability.
- Pooling multilingual results — label semantics differ per locale.
- Accepting 60% success as "good enough" for primary navigation — industry norm is ≥80% for top-level tasks.
- Treating dendrogram cut-points as ground truth — always cross-check with qualitative grouping rationale if available.
- Testing IA in isolation from content — the "About" category is meaningless without the pages it contains.
- One-shot validation — IA should be tested iteratively as content and features evolve.

## Handoff

- **To Echo**: once IA is validated, hand off the navigation structure for cognitive walkthrough on representative flows.
- **To Pulse**: recommend nav-path events (e.g. breadcrumb clicks, category-page arrivals) to monitor in production.
- **To Voice**: register IA labels that failed testing so post-launch feedback can be mapped against them.
- **To Canvas**: hand off validated IA tree for sitemap diagramming.
- **Always include** in handoff: n, method, per-task success rates, problem cards / labels, confidence intervals, locale scope.
