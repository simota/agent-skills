# Interleaving Tests

## What Is Interleaving?

Interleaving is an online evaluation technique for ranking systems (search, recommendations) that is **10–100x more sensitive** than traditional A/B testing for the same sample size.

Instead of showing users exclusively one ranker's results, interleaving *merges* results from two rankers into a single list and observes which ranker's items users prefer via implicit feedback (clicks, purchases, engagement).

**Why it's more sensitive:** Each user simultaneously evaluates both rankers, eliminating between-user variance. The signal is within-user preference, not between-group rate differences.

---

## Traditional A/B vs Interleaving

| Aspect | Traditional A/B | Interleaving |
|--------|----------------|--------------|
| **Assignment** | Users see one ranker exclusively | Users see a merged list from both rankers |
| **Signal** | Between-group metric difference | Within-user item preference |
| **Sensitivity** | Baseline | 10–100× higher |
| **Sample needed** | Large (weeks of traffic) | Small (hours to days) |
| **Metric** | Conversion rate, engagement rate | Win rate (A vs B) |
| **Limitations** | Slow; high variance | Cannot estimate absolute metric impact |
| **Typical use** | Final ship/no-ship decision | Fast candidate screening |

**Rule of thumb:** Use interleaving to quickly screen 10+ ranker candidates down to 2–3 finalists; use A/B testing for the final ship decision with business metric validation.

---

## Team Draft Interleaving (TDI)

Team Draft Interleaving is the standard algorithm for interleaving two ranked lists. It constructs a merged list while tracking which ranker "owns" each position.

### Algorithm

```
Input:  List A = [a1, a2, a3, ...], List B = [b1, b2, b3, ...]
Output: Merged list I, ownership map team[position]

1. Flip a fair coin to decide which ranker picks first (reduces ordering bias)
2. Repeat until merged list has desired length k:
   a. Let the current team pick their highest-ranked item not yet in I
   b. Add that item to I; record team ownership
   c. The OTHER team also claims this item if it appears in their top-k
      (prevents the first team from always getting credit for shared items)
   d. Alternate picking teams
```

### TypeScript Implementation

```typescript
interface InterleavingResult {
  mergedList: string[];
  ownership: Map<string, 'A' | 'B' | 'both'>; // item → owning ranker
}

function teamDraftInterleave(
  rankA: string[],  // Ranker A's ordered list of item IDs
  rankB: string[],  // Ranker B's ordered list of item IDs
  k: number         // Number of items to show
): InterleavingResult {
  const merged: string[] = [];
  const ownership = new Map<string, 'A' | 'B' | 'both'>();
  const inMerged = new Set<string>();

  // Coin flip: 0 = A picks first, 1 = B picks first
  let turn: 'A' | 'B' = Math.random() < 0.5 ? 'A' : 'B';

  const posA = { idx: 0 };
  const posB = { idx: 0 };

  while (merged.length < k) {
    const [picker, other, pickerPos, otherList] =
      turn === 'A'
        ? ['A' as const, 'B' as const, posA, rankB]
        : ['B' as const, 'A' as const, posB, rankA];

    const pickerList = turn === 'A' ? rankA : rankB;
    const pickerPosRef = turn === 'A' ? posA : posB;
    const otherPosRef = turn === 'A' ? posB : posA;

    // Advance picker's pointer to the next item not yet in merged list
    while (pickerPosRef.idx < pickerList.length && inMerged.has(pickerList[pickerPosRef.idx])) {
      pickerPosRef.idx++;
    }
    if (pickerPosRef.idx >= pickerList.length) break;

    const chosenItem = pickerList[pickerPosRef.idx];
    merged.push(chosenItem);
    inMerged.add(chosenItem);
    ownership.set(chosenItem, picker);

    // If the other ranker also has this item in their remaining top-k, mark as 'both'
    const otherRemainingRank = otherList.indexOf(chosenItem);
    if (otherRemainingRank !== -1 && otherRemainingRank < k) {
      ownership.set(chosenItem, 'both');
    }

    turn = other;
  }

  return { mergedList: merged, ownership };
}
```

### Computing Wins from Clicks

After users interact with the merged list, tally clicks by owning ranker:

```typescript
interface InterleavingOutcome {
  winner: 'A' | 'B' | 'tie';
  clicksA: number;
  clicksB: number;
}

function scoreInterleaving(
  clickedItems: string[],
  ownership: Map<string, 'A' | 'B' | 'both'>
): InterleavingOutcome {
  let clicksA = 0;
  let clicksB = 0;

  for (const item of clickedItems) {
    const owner = ownership.get(item);
    if (owner === 'A') clicksA++;
    else if (owner === 'B') clicksB++;
    // 'both' clicks are discarded (jointly owned items don't differentiate rankers)
  }

  const winner = clicksA > clicksB ? 'A' : clicksB > clicksA ? 'B' : 'tie';
  return { winner, clicksA, clicksB };
}
```

### Aggregating Win Rate Across Users

```typescript
interface InterleavingExperimentResult {
  totalUsers: number;
  winsA: number;
  winsB: number;
  ties: number;
  winRateA: number;     // wins / (wins + losses), ties excluded
  pValue: number;
  isSignificant: boolean;
}

function aggregateInterleavingResults(
  outcomes: InterleavingOutcome[],
  significance = 0.05
): InterleavingExperimentResult {
  const winsA = outcomes.filter(o => o.winner === 'A').length;
  const winsB = outcomes.filter(o => o.winner === 'B').length;
  const ties = outcomes.filter(o => o.winner === 'tie').length;

  // Binomial test on (winsA, winsB), ignoring ties
  // H₀: P(A wins) = 0.5
  const n = winsA + winsB;
  const winRateA = n > 0 ? winsA / n : 0.5;

  // Normal approximation to binomial
  const se = Math.sqrt(0.25 / n);
  const zScore = (winRateA - 0.5) / se;
  const pValue = 2 * (1 - normalCDF(Math.abs(zScore)));

  return {
    totalUsers: outcomes.length,
    winsA,
    winsB,
    ties,
    winRateA,
    pValue,
    isSignificant: pValue < significance
  };
}

function normalCDF(x: number): number {
  const t = 1 / (1 + 0.3275911 * Math.abs(x));
  const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
    - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
  return x >= 0 ? 0.5 * (1 + y) : 0.5 * (1 - y);
}
```

---

## When to Use Interleaving

### Applicable Conditions

- **Ranking systems**: search results, recommendation feeds, product listings, ad ranking
- **Implicit feedback available**: clicks, purchases, watch time (not survey-based ratings)
- **Fast iteration needed**: screening many ranker candidates quickly (model architecture changes, feature ablations, hyperparameter sweeps)
- **Sufficient impressions per user**: each merged list needs ≥1 click to produce signal

### Limitations

| Limitation | Description | Mitigation |
|------------|-------------|------------|
| **No absolute metric estimate** | Win rate tells you A > B, not by how much in business terms | Follow up winning candidate with A/B test |
| **Position bias** | Users click higher-ranked items regardless of quality | Use position-debiased click models or Balanced Interleaving variant |
| **Ranker correlation** | If A and B return very similar lists, few items are exclusively owned | Ensure candidates differ meaningfully before interleaving |
| **Click sparsity** | Low-traffic queries produce many tie outcomes, reducing power | Aggregate over sessions; filter to high-traffic slices |
| **Only pairwise comparison** | Compares exactly two rankers at a time | Run multiple pairwise comparisons or use Multileaving for 3+ rankers |

### Decision Flow

```
Have a ranking change? (search / rec / ads)
        │
        ▼
Interleaving screen (hours–days)
        │
   ┌────┴────┐
 A wins   B wins / tie
   │
   ▼
A/B test A vs current (weeks)
        │
   ┌────┴────┐
Significant?   Not significant
   │                │
 Ship A         Abandon / iterate
```

---

## Industry Examples

### Airbnb — Search Ranking

Airbnb uses interleaving to evaluate search ranking models at high velocity. Because each listing's desirability varies by user, within-user comparisons via interleaving dramatically reduce the noise from between-user preference heterogeneity. They report interleaving requires **~100x fewer users** to reach the same statistical power as A/B tests for ranking changes.

Reference: "Interleaving in Online Experiments at Airbnb" (Airbnb Engineering Blog)

### Expedia — Hotel Search

Expedia's experimentation team uses interleaving as a pre-screen step in their ranking pipeline. Candidate models are evaluated with interleaving first; only models showing statistically significant preference gains proceed to full A/B tests with business metric (booking conversion) measurement.

This two-stage approach reduced their time-to-decision for ranking experiments from weeks to days.

### Netflix — Recommendation Rows

Netflix has published research on using interleaving to evaluate recommendation algorithms for row ordering and within-row ranking. The key advantage in their setting is that users implicitly signal row and item preference through scrolling and hover behavior, providing rich implicit feedback for interleaving scoring.

### LinkedIn — Feed Ranking

LinkedIn applies interleaving in their feed ranking pipeline to evaluate engagement model updates. They use a variant called **Balanced Interleaving** that addresses position bias by ensuring both rankers contribute equally to top positions across the experiment population.

---

## Multileaving (3+ Rankers)

When comparing more than two rankers simultaneously, standard interleaving extends to **multileaving**. The Team Draft algorithm generalizes: each ranker takes turns picking their top un-selected item, and clicks are attributed to the owning ranker.

Multileaving enables comparing N candidates in a single experiment, but:
- Attribution becomes ambiguous when multiple rankers claim an item
- Statistical analysis requires pairwise win rate matrices across all ranker pairs
- Recommended for ≤5 rankers simultaneously; beyond that, noise dominates

```typescript
// Multileaving win matrix output
interface MultileavingResult {
  rankers: string[];
  // winMatrix[i][j] = fraction of impressions where ranker i beat ranker j
  winMatrix: number[][];
}
```

---

## References

- Chapelle et al., "Large-scale validation and analysis of interleaved search evaluation" (2012) — foundational TDI paper
- Schuth et al., "Probabilistic Multileave for Online Retrieval Evaluation" (2015)
- Airbnb Engineering: "Interleaving in Online Experiments at Airbnb"
- Bradley & Terry, "Rank analysis of incomplete block designs: I. The method of paired comparisons" (Biometrika 1952) — paired-comparison foundation
- Chiang et al., "Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference" (arXiv:2403.04132, 2024) — applies Bradley-Terry + bootstrap CIs to pairwise human votes; same within-user variance-reduction insight as interleaving, scaled to LLM evaluation
- Frick et al. / LMSYS — "Prompt-to-Leaderboard" (arXiv:2502.14855) — extends Arena methodology with Vovk-Wang e-values for valid early stopping in model ranking

## LLM evaluation: pairwise preference as a cousin of interleaving

LMSYS Chatbot Arena uses the same statistical insight as interleaving — within-user pairwise comparison removes between-user variance — applied to LLM outputs instead of ranked lists. Two LLMs answer the same prompt; a human picks the better response; preferences are aggregated under a Bradley-Terry (1952) model into Elo-like scores with bootstrap confidence intervals. The 2025 methodology layer adds Vovk & Wang (2021) e-values to obtain valid sequential stopping over the live leaderboard. When evaluating LLM features (prompt changes, model upgrades, retrieval changes), pairwise voting (manual or LLM-as-judge) is the direct LLM-domain analog of `teamDraftInterleave` for ranking systems — reach for it before reaching for between-arm A/B on aggregate quality scores. See also `reference/adaptive-experimentation.md` § "LLM / AI Feature Experimentation".
