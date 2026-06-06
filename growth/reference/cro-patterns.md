# CRO (Conversion Rate Optimization) Patterns

## 2026 Benchmarks (CRO planning baseline)

| Metric | 2026 figure | Source |
|--------|------------|--------|
| Average landing-page conversion (all industries) | **4.6%** (top 10% ≥ 11.5%) | searchlab.nl 2026 CRO stats |
| E-commerce conversion | 1–4% typical, 5%+ high-performer | crobenchmark.com |
| Cart abandonment (all e-comm) | **70–72%** (mobile 73–75%, desktop 65–68%) | Baymard 2026 |
| Top abandonment reasons | High shipping cost **49%**, account required **24%** | Baymard |
| Form fields → conversion | 3 fields **23.1%**, 5 fields **17.0%**, 7 fields **11.4%**, 10+ fields **6.9%** | digitalapplied.com 2026 |
| Multi-step vs single-page form | **+14%** for multi-step | digitalapplied.com 2026 |

[Source: Baymard Institute — *Cart Abandonment Rate 2026*, https://baymard.com/lists/cart-abandonment-rate]
[Source: Searchlab — *CRO Statistics 2026*, https://searchlab.nl/en/statistics/conversion-optimization-statistics-2026]
[Source: Digital Applied — *Form Conversion Rate Benchmarks 2026*, https://www.digitalapplied.com/blog/form-conversion-rate-benchmarks-2026-data-points]

> **Tooling note (2025-09):** OpenAI acquired **Statsig for $1.1B** (all-stock) on 2025-09-02, with founder Vijaye Raji becoming OpenAI's CTO of Applications. Statsig continues to operate independently for external customers, but expect roadmap drift toward OpenAI-centric features; teams locked into Statsig should monitor pricing and Enterprise SLAs. Alternatives: GrowthBook (OSS), Optimizely Feature Experimentation, LaunchDarkly, Eppo, VWO. [Source: CNBC, https://www.cnbc.com/2025/09/02/openai-buys-statsig-for-1point1-billion-hires-ceo-as-applications-exec.html]

## CTA Best Practices

| Element | Best Practice | Example |
|---------|--------------|---------|
| Copy | Action-oriented verb | "Start free trial" not "Submit" |
| Color | High contrast to background | Primary brand color |
| Size | Large enough to tap (44x44px min) | Full-width on mobile |
| Position | Above the fold, after value prop | Hero section |
| Urgency | Time/scarcity when genuine | "3 spots left" |

## Form Optimization

1. Reduce fields to minimum required
2. Use inline validation (not on submit)
3. Show progress for multi-step forms
4. Auto-focus first field
5. Use appropriate input types (email, tel, etc.)

## Exit Intent Detection

```typescript
document.addEventListener('mouseout', (e) => {
  if (e.clientY < 0) {
    showRetentionOverlay();
  }
});
```

## Social Proof Patterns
- Customer count: "Join 10,000+ teams"
- Logos: Trusted by [Company logos]
- Testimonials: Quote with photo and name
- Rating: "4.8/5 from 500+ reviews"

## 2026 CRO Trends

### AI-Powered Personalization

Dynamically optimize content per user segment in real time. AI search visitors convert at ~4.4× the rate of traditional organic search traffic — segment AI-referred visitors and serve high-intent CTAs first. Reported up to 200% conversion lift in e-commerce when combined with funnel-stage personalization.

```typescript
interface UserSegment {
  industry: string;
  plan: 'free' | 'pro' | 'enterprise';
  visitCount: number;
}

interface HeroContent {
  headline: string;
  cta: string;
  socialProof: string;
}

function getPersonalizedHero(segment: UserSegment): HeroContent {
  if (segment.plan === 'enterprise') {
    return {
      headline: 'Scale securely across your entire organization',
      cta: 'Talk to sales',
      socialProof: 'Trusted by Fortune 500 companies',
    };
  }
  if (segment.visitCount === 0) {
    return {
      headline: 'Get started in 5 minutes',
      cta: 'Start free trial',
      socialProof: 'Join 50,000+ teams',
    };
  }
  return {
    headline: 'Welcome back — pick up where you left off',
    cta: 'Continue',
    socialProof: '4.8/5 from 2,000+ reviews',
  };
}
```

### Multi-Armed Bandit Testing

Unlike A/B tests with fixed 50/50 splits, bandit algorithms dynamically shift traffic to the best-performing variant.

```typescript
interface Variant {
  id: string;
  conversions: number;
  impressions: number;
}

// Thompson Sampling: choose variant with probability proportional to posterior
function selectVariant(variants: Variant[]): string {
  const samples = variants.map(v => {
    // Beta distribution sample approximation
    const alpha = v.conversions + 1;
    const beta = v.impressions - v.conversions + 1;
    return { id: v.id, sample: sampleBeta(alpha, beta) };
  });
  return samples.reduce((best, curr) => curr.sample > best.sample ? curr : best).id;
}

function sampleBeta(alpha: number, beta: number): number {
  // Approximation using gamma samples
  const x = gammaSample(alpha);
  const y = gammaSample(beta);
  return x / (x + y);
}

function gammaSample(shape: number): number {
  // Marsaglia and Tsang method (simplified)
  return -Math.log(Math.random()) * shape;
}
```

### Micro-Conversion Optimization

Track small intent signals (demo views, chat interactions, scroll depth) as leading indicators before the primary conversion.

```typescript
type MicroConversionEvent =
  | { type: 'demo_watched'; durationMs: number }
  | { type: 'chat_opened'; source: string }
  | { type: 'pricing_scrolled'; reachedBottom: boolean }
  | { type: 'feature_hovered'; featureId: string };

function trackMicroConversion(event: MicroConversionEvent): void {
  // Score each micro-conversion by predicted downstream value
  const scores: Record<MicroConversionEvent['type'], number> = {
    demo_watched: 10,
    chat_opened: 7,
    pricing_scrolled: 5,
    feature_hovered: 2,
  };

  const score = scores[event.type];
  const currentScore = Number(sessionStorage.getItem('intent_score') ?? '0');
  sessionStorage.setItem('intent_score', String(currentScore + score));

  // Trigger high-intent CTAs when score crosses threshold
  if (currentScore + score >= 20) {
    showHighIntentCTA();
  }

  navigator.sendBeacon('/analytics', JSON.stringify({ ...event, score }));
}

function showHighIntentCTA(): void {
  document.getElementById('sticky-cta')?.classList.remove('hidden');
}
