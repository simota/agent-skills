# Sample Size Calculator

## Power Analysis Formula

```
n = (Z_α/2 + Z_β)² × (p₁(1-p₁) + p₂(1-p₂)) / (p₁ - p₂)²
```

Where:
- Z_α/2 = Z-score for significance level (1.96 for 95%)
- Z_β = Z-score for power (0.84 for 80%)
- p₁ = baseline conversion rate
- p₂ = expected conversion rate (baseline + MDE)

## TypeScript Implementation

```typescript
interface SampleSizeParams {
  baselineConversion: number;  // Current conversion rate (e.g., 0.05 for 5%)
  mde: number;                 // Minimum detectable effect (e.g., 0.1 for 10% relative lift)
  power: number;               // Statistical power (typically 0.8)
  significance: number;        // Significance level (typically 0.05)
}

function calculateSampleSize(params: SampleSizeParams): number {
  const { baselineConversion, mde, power, significance } = params;

  // Z-scores
  const zAlpha = 1.96;  // for 5% two-tailed
  const zBeta = 0.84;   // for 80% power

  const p1 = baselineConversion;
  const p2 = baselineConversion * (1 + mde);
  const pPooled = (p1 + p2) / 2;

  const numerator = Math.pow(
    zAlpha * Math.sqrt(2 * pPooled * (1 - pPooled)) +
    zBeta * Math.sqrt(p1 * (1 - p1) + p2 * (1 - p2)),
    2
  );
  const denominator = Math.pow(p2 - p1, 2);

  return Math.ceil(numerator / denominator);
}

// Example: 5% baseline, 10% relative lift
const sampleSize = calculateSampleSize({
  baselineConversion: 0.05,
  mde: 0.10,
  power: 0.80,
  significance: 0.05
});
// Result: ~31,000 per variant
```

## Quick Reference Table

| Baseline | 5% Lift | 10% Lift | 20% Lift |
|----------|---------|----------|----------|
| 1% | 1.6M | 400K | 100K |
| 5% | 310K | 78K | 20K |
| 10% | 150K | 38K | 9.5K |
| 20% | 68K | 17K | 4.3K |
| 50% | 16K | 4K | 1K |

*Sample size per variant, 80% power, 5% significance, two-tailed*

| Baseline | MDE | Power 80% | Power 90% |
|----------|-----|-----------|-----------|
| 5% | 10% rel | 31,234 | 41,792 |
| 5% | 20% rel | 7,854 | 10,508 |
| 10% | 10% rel | 14,313 | 19,147 |
| 10% | 20% rel | 3,622 | 4,846 |
| 20% | 10% rel | 6,344 | 8,486 |
| 20% | 20% rel | 1,621 | 2,169 |

## Duration Calculation

```typescript
function calculateDuration(
  sampleSizePerVariant: number,
  dailyTraffic: number,
  variants: number = 2
): number {
  const totalSampleNeeded = sampleSizePerVariant * variants;
  return Math.ceil(totalSampleNeeded / dailyTraffic);
}

// Example: 31K per variant, 10K daily traffic
const duration = calculateDuration(31000, 10000, 2);
// Result: 7 days minimum
```

Minimum recommended: 7 days (to capture weekly patterns)
Maximum recommended: 30 days (to avoid novelty effects)
