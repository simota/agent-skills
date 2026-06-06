# Value vs Effort Matrix Reference

Purpose: Lightweight 2x2 prioritization that plots items on a Value (vertical) × Effort (horizontal) plane and sorts them into four quadrants — Quick Wins, Major Projects, Fill-Ins, Thankless Tasks. Optimized for workshop facilitation, cross-functional consensus, and visible decision-making before any per-item math is required. Lineage: Lean / Agile prioritization (Pick Chart variant, Six Sigma) and Eisenhower's Important/Urgent matrix.

## Scope Boundary

- **rank `value-effort`**: visual 2x2 quadrant assignment with axis-scoring rubrics. Targets workshops, stakeholder alignment sessions, and pre-RICE triage.
- **rank `ice` / `rice` / `wsjf` (elsewhere)**: numerical scoring frameworks. Upgrade from this recipe when the top quadrants need to be ordered *within* themselves.
- **rank `moscow` (elsewhere)**: classification-based, deadline-friendly. Use when stakeholders argue about "must-have" semantics rather than effort.
- **rank `kano` (elsewhere)**: customer-satisfaction lens, not effort lens.
- **Magi (elsewhere)**: multi-perspective deliberation when stakeholders disagree on which axis an item belongs to. This recipe surfaces the disagreement; Magi resolves it.
- **Riff (elsewhere)**: brainstorming and idea expansion. Run Riff before this recipe to fill the candidate set; this recipe sorts what Riff produced.
- **Sherpa (elsewhere)**: task decomposition of the chosen quick-wins / major-projects after sorting.

## Workflow

```
PREPARE   →  collect candidate items (from Spark / Riff / backlog)
          →  agree axis definitions, scoring rubric, and quadrant thresholds with the room

SCORE     →  each participant places dots on a shared 2x2 (physical or digital)
          →  independent placement first, then reveal — anti-anchoring

CLUSTER   →  reconcile dot scatter; items with high variance go to a "discuss" pile
          →  re-score discuss-pile items after a brief case from each side

QUADRANT  →  finalize quadrant assignment per item (Quick Win / Major / Fill-In / Thankless)
          →  draw the 2x2; label every item; photograph or export

ROUTE     →  Quick Wins → Sherpa for immediate decomposition
          →  Major Projects → upgrade to RICE / WSJF for intra-quadrant ordering
          →  Fill-Ins → backlog parking lot
          →  Thankless → Void review (does this need to exist?)
```

## Quadrant Definitions

| Quadrant | Value | Effort | Action |
|----------|-------|--------|--------|
| **Quick Wins** | High | Low | Do first — disproportionate ROI, momentum builders |
| **Major Projects** | High | High | Plan deliberately — sequence, decompose, staff properly |
| **Fill-Ins** | Low | Low | Do when capacity exists — good for new hires or slow weeks |
| **Thankless Tasks** | Low | High | Drop or redesign — explicit YAGNI candidates |

Quadrant lines are thresholds, not midpoints. Workshop the threshold — "high effort = >2 sprints" beats "high effort = above the median."

## Axis Scoring Rubrics

| Score | Value (impact on user / business) | Effort (calendar + complexity) |
|-------|-----------------------------------|--------------------------------|
| 1 | Marginal — nice-to-have | Hours |
| 2 | Localized improvement | Days |
| 3 | Notable — visible to many users | 1-2 weeks |
| 4 | Significant — measurable KPI shift | 1-2 sprints |
| 5 | Strategic — moves North Star metric | 1+ quarter |

Score Value and Effort independently. Mixing them ("it's hard but valuable so I'll call it 3") collapses the matrix.

## Workshop Facilitation Flow

1. **Frame** — write the question on the wall: "What should we work on next quarter?"
2. **Calibrate** — score 2-3 reference items together to anchor the room.
3. **Silent placement** — 5-7 minutes, sticky notes on a printed 2x2 (or Miro board).
4. **Reveal and cluster** — show all placements; clusters become consensus, scatters become discussion.
5. **Discuss outliers only** — do not re-litigate the consensus items.
6. **Finalize** — agree quadrant per item; photograph; assign owners for Quick Wins.
7. **Time-box to 60-90 minutes** — beyond that, decision fatigue inverts placements.

## Integration with Adjacent Frameworks

| Framework | Relationship |
|-----------|--------------|
| **Eisenhower (Urgent/Important)** | Same 2x2 shape, different axes. Run Eisenhower for personal/operational work; Value/Effort for product backlog. |
| **Pick Chart (Six Sigma)** | Direct ancestor: Possible / Implement / Challenge / Kill. Pick is process-improvement-flavored; Value/Effort is product-flavored. |
| **RICE / WSJF** | Upgrade path. Once the top quadrant has 5+ items, the matrix can't sort them — switch to RICE or WSJF for ordering. |
| **MoSCoW** | Complement. Run MoSCoW on the Major Projects quadrant when stakeholders frame work as "must vs should." |
| **Kano** | Run before Value scoring on user-facing features — Kano category modulates Value (Attractive features get a Value bump despite weak survey demand). |

## When to Upgrade

Switch from Value/Effort to a numerical framework when:
- The top quadrant holds more than 5 items and they need ordering.
- Effort estimates need to be defended to finance or PMO.
- A deadline-bound item appears — Value/Effort has no time dimension; use CD3 or WSJF.
- Stakeholders dispute *placements* rather than *priorities* — that's a sign the rubric needs more rigor.

## Anti-Patterns

- Using axis midpoints as quadrant thresholds — half the items end up on lines and the matrix loses decisiveness.
- Letting the highest-paid person place dots first — anchors the room. Always silent placement first.
- Mixing axes ("high value because it's hard") — collapses the 2x2 to a 1D priority list with extra steps.
- Treating Quick Wins as automatic priority — a backlog of only quick wins starves strategic Major Projects and decays the product.
- Skipping the Thankless quadrant — these are the items that should go to Void, not get quietly re-categorized as Fill-Ins.
- Scoring Effort in story points — story points are team-relative; for cross-team workshops use calendar time.
- Workshop > 90 minutes — decision fatigue causes participants to flip placements just to feel done.
- Single-vote placements — at minimum 3 voters per item, or the matrix reflects one person's bias.
- Forgetting to revisit — Value/Effort matrices stale within a quarter as effort estimates and market value shift.

## Handoff

- **To Sherpa**: Quick Wins, with quadrant rationale — Sherpa decomposes into atomic steps for immediate execution.
- **To Spark**: Major Projects needing further feature ideation before decomposition.
- **To Magi**: items with high placement variance (>2 quadrants of disagreement) — escalate to multi-perspective deliberation.
- **To Void**: Thankless Tasks — formal YAGNI review before deletion.
- **To rank `rice` / `wsjf`**: top-quadrant items needing intra-quadrant numerical ordering.
- **To Scribe**: matrix snapshot, quadrant rationale, and decision log for retro and audit.
