# Common Pitfalls & Solutions

## 1. Peeking Problem

**Problem:** Checking results repeatedly increases false positive rate.

**Solution:** Use sequential testing with alpha spending.

```typescript
function shouldContinue(
  currentPValue: number,
  currentN: number,
  targetN: number,
  alphaSpent: number = 0
): { continue: boolean; decision: 'significant' | 'not_significant' | 'continue' } {
  const progress = currentN / targetN;
  const alphaAvailable = 0.05 * progress - alphaSpent;

  if (currentPValue < alphaAvailable) {
    return { continue: false, decision: 'significant' };
  }

  if (progress >= 1) {
    return { continue: false, decision: currentPValue < 0.05 ? 'significant' : 'not_significant' };
  }

  return { continue: true, decision: 'continue' };
}
```

## 2. Multiple Comparisons

**Problem:** Testing many metrics inflates false positive rate.

**Solution:** Bonferroni correction or pre-register ONE primary metric.

```typescript
function adjustedSignificance(
  numComparisons: number,
  baseAlpha: number = 0.05
): number {
  return baseAlpha / numComparisons;
}

// 5 metrics → significance level = 0.01 per test
```

## 3. Selection Bias

**Problem:** Non-random assignment leads to confounded results.

**Solution:** Use deterministic hashing for assignment.

```typescript
// Good: Deterministic based on user ID
const variant = getVariant('experiment', userId);

// Bad: Random each time
const variant = Math.random() > 0.5 ? 'treatment' : 'control';
```

## 4. Sample Ratio Mismatch (SRM)

**Problem:** The observed ratio of users in each variant deviates significantly from the intended allocation. SRM indicates a data collection or assignment bug — results are untrustworthy even if significant.

**Detection:** Chi-square test on observed vs expected counts.

```typescript
interface SRMCheckInput {
  observed: number[];   // Observed counts per variant [controlN, treatmentN, ...]
  expected: number[];   // Expected proportions [0.5, 0.5] or [0.33, 0.33, 0.34]
}

function checkSRM(input: SRMCheckInput): { hasSRM: boolean; pValue: number; chiSquare: number } {
  const { observed, expected } = input;
  const totalObserved = observed.reduce((a, b) => a + b, 0);
  const expectedCounts = expected.map(p => p * totalObserved);

  // Chi-square statistic: sum of (observed - expected)² / expected
  const chiSquare = observed.reduce((sum, obs, i) => {
    const exp = expectedCounts[i];
    return sum + Math.pow(obs - exp, 2) / exp;
  }, 0);

  // Degrees of freedom = number of groups - 1
  const df = observed.length - 1;
  const pValue = 1 - chiSquareCDF(chiSquare, df);

  return {
    hasSRM: pValue < 0.01, // Use strict threshold for SRM detection
    pValue,
    chiSquare
  };
}

// Chi-square CDF approximation for df=1 and df=2
function chiSquareCDF(x: number, df: number): number {
  if (df === 1) return erf(Math.sqrt(x / 2));
  if (df === 2) return 1 - Math.exp(-x / 2);
  // For df > 2, use normal approximation
  const z = Math.pow(x / df, 1 / 3) - (1 - 2 / (9 * df));
  const sigma = Math.sqrt(2 / (9 * df));
  return normalCDF(z / sigma);
}

function erf(x: number): number {
  const t = 1 / (1 + 0.3275911 * Math.abs(x));
  const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
    - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
  return x >= 0 ? y : -y;
}

function normalCDF(x: number): number {
  return 0.5 * (1 + erf(x / Math.sqrt(2)));
}
```

**Common SRM causes and fixes:**

| Cause | Description | Fix |
|-------|-------------|-----|
| Redirect issues | Treatment redirects cause bot filtering | Exclude pre-redirect events |
| Cache/CDN | Cached pages serve stale variant | Use user-level assignment, not session |
| Client-side bugs | JS errors cause variant to not load | Add error monitoring per variant |
| Logging delays | Treatment events logged with latency | Use exposure timestamp, not event timestamp |
| Eligibility filter | Post-assignment filtering differs by variant | Filter before assignment, not after |

**SRM checklist:** Run SRM check BEFORE interpreting any experiment results. If SRM detected:
1. Stop analysis immediately
2. Investigate assignment and logging pipelines
3. Fix the root cause
4. Restart the experiment

---

## 5. Network Effects and SUTVA Violations

**Problem:** The Stable Unit Treatment Value Assumption (SUTVA) requires that one user's treatment does not affect another user's outcome. This assumption breaks when users interact with each other (social networks, marketplaces, multiplayer).

**Examples of SUTVA violations:**
- Social feed experiment: treated users post more, which changes the feed for control users
- Marketplace pricing: treatment variant prices affect control variant demand
- Notifications: send fewer notifications to treatment group → control group gets more

**Detection:** Compare isolated clusters vs mixed clusters.

**Solution: Cluster Randomization**

Instead of randomizing at the user level, randomize at the cluster level (geographic region, friend group, seller category).

```typescript
interface ClusterAssignment {
  clusterId: string;
  variant: 'control' | 'treatment';
  users: string[];
}

function assignClusters(
  clusters: string[][],
  treatmentFraction: number,
  salt: string
): ClusterAssignment[] {
  return clusters.map((users, idx) => {
    // Deterministic cluster assignment
    const hash = hashUserId(`cluster_${idx}`, salt);
    const bucket = hash % 100;
    const variant: 'control' | 'treatment' =
      bucket < treatmentFraction * 100 ? 'treatment' : 'control';

    return { clusterId: `cluster_${idx}`, variant, users };
  });
}

function hashUserId(userId: string, salt: string): number {
  const str = `${userId}:${salt}`;
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash = hash & hash;
  }
  return Math.abs(hash);
}
```

**Trade-offs of cluster randomization:**

| Aspect | User-Level Randomization | Cluster Randomization |
|--------|-------------------------|----------------------|
| **SUTVA validity** | Violated if network effects exist | Valid when clusters are isolated |
| **Statistical power** | Higher (more independent units) | Lower (fewer, larger units) |
| **Sample size** | Smaller experiment needed | Larger experiment needed (design effect) |
| **Use cases** | Independent users | Social, marketplace, geographic tests |

**Design effect:** With cluster randomization, the effective sample size is reduced by the design effect `DEFF = 1 + (m-1) * ICC`, where `m` is cluster size and `ICC` is the intra-class correlation (within-cluster similarity).
