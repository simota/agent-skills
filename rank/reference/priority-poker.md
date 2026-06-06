# Priority Poker (Wideband Delphi) Reference

Purpose: Anonymous, iterative group voting on priority dimensions using a Fibonacci scale, with re-discussion triggered by vote dispersion. Adapts Planning Poker (Grenning, 2002; Cohn) — itself a Wideband Delphi descendant (Boehm and Farquhar, 1970) — from estimation to prioritization. Engineered to mitigate group-think, anchoring, and HiPPO bias by hiding votes until reveal and forcing structured re-discussion when the group disagrees.

## Scope Boundary

- **rank `pokerplan`**: collaborative anonymous voting for priority scoring — typically across one or more dimensions (Value, Effort, Risk, Confidence). Produces calibrated relative scores plus a dispersion log.
- **rank `ice` / `rice` / `wsjf` (elsewhere)**: numerical formulas. Pokerplan is a *method to produce inputs* for these formulas, not a separate scoring framework. Run Pokerplan to score components, then plug into ICE/RICE/WSJF.
- **rank `value-effort` (elsewhere)**: 2x2 visual quadrant. Pokerplan is finer-grained and produces ordered numerics, not quadrants.
- **Magi (elsewhere)**: multi-perspective deliberation. Pokerplan converges votes; Magi explores divergent perspectives. Use Magi when the dispersion rule keeps re-triggering — the disagreement is structural, not noise.
- **Riff (elsewhere)**: brainstorming and idea expansion. Run Riff to produce the candidate set; Pokerplan to prioritize it.
- **Sherpa (elsewhere)**: task decomposition. Pokerplan ranks; Sherpa breaks down the top-ranked.

## Workflow

```
PREPARE   →  agree dimensions to vote on (e.g. Value, Effort, Confidence)
          →  agree scale (Fibonacci 0,1,2,3,5,8,13,21,? coffee-break) and dispersion threshold
          →  select 2-3 reference items at low/mid/high anchors per dimension

CALIBRATE →  walk the room through the reference items together
          →  voters internalize "what does an 8 feel like?" before scoring novel items

VOTE      →  for each item × dimension, voters select a card in private
          →  reveal simultaneously — no early peeks

DISPERSE? →  if max - min > dispersion threshold (default: > 2 Fibonacci steps)
          →  highest and lowest voters explain reasoning (not the average voters)
          →  re-vote up to 3 rounds; persistent dispersion triggers Magi handoff

RECORD    →  log final vote, dispersion history, and reasoning per item
          →  feed scores into ICE / RICE / WSJF or rank directly

PRESENT   →  ranked list with confidence bands derived from final-round dispersion
```

## Fibonacci Scale and Meaning

| Card | Meaning (priority dimension) |
|------|------------------------------|
| 0 | Not applicable / does not contribute |
| 1 | Trivial — barely registers |
| 2 | Small — incremental |
| 3 | Modest — noticeable |
| 5 | Meaningful — clear contribution |
| 8 | Large — significant lever |
| 13 | Major — strategic-level |
| 21 | Massive — likely needs decomposition |
| ? | I don't have enough information |
| ☕ (coffee) | I need a break / let's pause |

The non-linear scale forces relative thinking — voters cannot quibble between 6 and 7. Anything beyond 21 is a signal to break the item down before scoring.

## Dispersion Rule (Re-Discussion Threshold)

| Spread (max - min in Fibonacci steps) | Action |
|----------------------------------------|--------|
| 0-1 step | Accept — strong consensus |
| 2 steps | Accept with note — minor variance |
| 3+ steps | Re-discuss — extremes explain, then re-vote |
| 4+ steps after 3 rounds | Escalate to Magi — structural disagreement |
| Any `?` card | Pause vote — provide missing context first |

Dispersion is the *signal*, not the problem. A high-dispersion item with rich discussion produces better scores than a low-dispersion item that everyone anchored on.

## Calibration via Reference Items

Without anchors, voters drift toward the middle of the scale. Pre-select reference items:

| Anchor | Purpose |
|--------|---------|
| **Low anchor** | A known-trivial item scored as 1-2 — sets the floor |
| **Mid anchor** | A familiar shipped item scored as 5 — sets the mid |
| **High anchor** | A clearly strategic item scored as 13 — sets the ceiling |

Walk the room through anchors first. Re-anchor every 8-10 items as fatigue distorts perception.

## Group-Bias Mitigation Mechanics

| Bias | Mitigation built into Pokerplan |
|------|-------------------------------|
| Anchoring | Cards revealed simultaneously — first speaker can't anchor the room |
| HiPPO | Anonymous reveal — title and salary don't show on the card |
| Group-think | Independent vote before discussion |
| Confirmation | Dispersion rule forces extreme voters to speak, not the median |
| Recency | Reference anchors re-establish baseline mid-session |
| Sunk cost | Item history is hidden during scoring (optional rule) |

These mitigations only work if the rituals are kept: simultaneous reveal, extremes-first discussion, calibration anchors. Skip any one and the bias-protection collapses.

## Online Tool Options

| Tool | Strengths | Notes |
|------|-----------|-------|
| Planning Poker Online (free) | Simple, browser-based | Built for estimation — re-label dimensions for priority |
| Scrum Poker (Atlassian Marketplace) | Jira integration | Stores votes against issues |
| PlanITpoker | Custom decks, anonymous voting | Good async option |
| Miro / FigJam templates | Visual workshop fit | Manually enforce simultaneous reveal |
| Slack/Discord polls | Lowest friction | Vote anonymity weak — avoid for HiPPO-heavy rooms |

For distributed teams, choose a tool that enforces simultaneous reveal — manual reveals leak via timing.

## Anti-Patterns

- Sequential voting (cards shown one at a time) — defeats anchoring protection; the first vote becomes the anchor.
- Allowing non-Fibonacci numbers ("can I vote 6.5?") — destroys the relative scale and re-introduces false precision.
- Skipping calibration anchors — without low/mid/high references, scores drift across sessions and become uncomparable.
- Discussing the median voter on dispersion — extremes hold the information; the median already aligns.
- Scoring more than 8-10 items per session without a break — fatigue compresses scores toward the middle.
- HiPPO speaks first on dispersion — even with anonymous voting, the post-reveal discussion re-introduces hierarchy bias.
- Treating `?` cards as 0 — `?` means "give me data," not "low priority." Pause and provide context.
- Conflating Pokerplan with estimation Planning Poker — same mechanic, different unit. Document the dimension being voted on.
- Re-running until consensus is forced — beyond 3 rounds, you're not converging, you're wearing people down. Hand off to Magi.

## Handoff

- **To rank `rice` / `wsjf` / `ice`**: per-component scores from Pokerplan plug into the chosen formula — Pokerplan produces the inputs, the formula produces the rank.
- **To Magi**: items where dispersion remains > 4 steps after 3 rounds — structural disagreement needs multi-perspective deliberation, not more votes.
- **To Sherpa**: top-ranked items with confidence bands — Sherpa decomposes; high-dispersion items get a flag to re-validate during decomposition.
- **To Spark**: items where multiple voters played `?` — feature ideation needs more substance before re-voting.
- **To Scribe**: vote log, dispersion history, and reasoning per item — auditable record of how the priority was reached.
