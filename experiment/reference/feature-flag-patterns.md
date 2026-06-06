# Feature Flag Patterns

## Flag Types

| Type | Lifecycle | Example |
|------|-----------|---------|
| Release | Short (days-weeks) | New checkout flow |
| Experiment | Medium (weeks) | A/B test variant |
| Ops | Permanent | Kill switch, rate limit |
| Permission | Permanent | Premium features |

## LaunchDarkly Integration

```typescript
import { init } from 'launchdarkly-js-client-sdk';

const client = init('client-key', { key: userId });

const showNewCheckout = client.variation('new-checkout', false);
```

## Custom Feature Flag

```typescript
interface FeatureFlag {
  key: string;
  enabled: boolean;
  variants?: Record<string, unknown>;
  targeting?: { percentage: number; segments?: string[] };
}
```

## Cleanup Checklist
- [ ] Remove flag evaluation code
- [ ] Remove losing variant code
- [ ] Archive flag in management system
- [ ] Update documentation

---

## Platform Comparison Matrix (2026-05)

| Feature | Statsig (OpenAI) | Eppo by Datadog / Datadog Experiments | GrowthBook 3.6+ | LaunchDarkly | PostHog Experiments |
|---------|------------------|---------------------------------------|-----------------|--------------|---------------------|
| **Ownership / 2025 events** | Acquired by OpenAI 2025-09 ($1.1B); CEO became OpenAI CTO of Applications | Eppo acquired by Datadog 2025-05 (~$220M); rebranded "Eppo by Datadog" | Independent OSS company, v3.6 released 2025-05-01 | Independent | Independent OSS |
| **Statistical engine** | CUPED, corrected-alpha always-valid p-values (CAA), sequential, MAB | CUPED++ (works on new-user tests via assignment covariates), GAVI sequential (Howard et al. 2021), Bayesian + Frequentist | Frequentist + Bayesian; Safe Rollouts with one-sided sequential testing on guardrails (3.6) | Dual Frequentist/Bayesian engines, CUPED, sequential testing, MAB — all GA | Bayesian (default) or Frequentist; new experimentation engine with running-time calc + percentile Winsorization |
| **Feature flags** | Full (targeting, rollout, kill switch) | Via Datadog Feature Flags | Full | Industry-leading | Full |
| **Warehouse-native** | Dual (Snowflake, BigQuery, Redshift, Databricks, Athena) | Yes — primary focus | Yes — primary focus | No (event streaming only) | Self-hosted DB or ClickHouse Cloud |
| **Observability integration** | Limited | Native (RUM, APM, logs, traces) | No | No | Native within PostHog |
| **Auto-rollback / safe rollout** | Yes | Via observability guardrails | Yes (Safe Rollouts 3.6) | Yes (via monitoring) | Yes |
| **Open source** | No | No | Yes (self-host) | No | Yes |
| **Best for** | Teams already in OpenAI applications stack | Data warehouse-centric orgs + Datadog stack | Cost-sensitive teams, OSS preference, SQL-defined metrics | Enterprise feature management, dual-engine statistics | OSS + product analytics + flags in one tool |

### Selection Guide (2026-05)

| Your situation | Recommended platform |
|---------------|---------------------|
| Already on OpenAI applications stack, want integrated experimentation | **Statsig** (OpenAI) |
| Metrics live in data warehouse (Snowflake/BigQuery/Databricks) + Datadog observability | **Eppo by Datadog** |
| Warehouse-native, OSS preference, SQL-defined metrics, want safe rollouts with one-sided sequential | **GrowthBook 3.6+** |
| Enterprise FF + SSO + audit logs + dual Frequentist/Bayesian engine | **LaunchDarkly** |
| All-in-one OSS product analytics + flags + experiments | **PostHog** |
| Small team, just need simple feature toggles | Custom implementation (see below) |

Note: PII-sensitive workloads should evaluate the OpenAI-affiliation of Statsig vs the Datadog-affiliation of Eppo against their respective data-processing addenda — both vendor mappings changed in 2025.

---

## Warehouse-Native Integration Pattern

Warehouse-native experimentation analyses experiment results directly in your data warehouse, giving you full control and auditability.

```
┌─────────────┐    exposure events    ┌──────────────────┐
│  Feature    │ ──────────────────▶  │   Data Warehouse  │
│  Flag SDK   │                      │ (Snowflake/BigQuery│
└─────────────┘                      │  /Redshift/etc.)   │
                                     └──────────┬────────┘
                                                │
                                         SQL analysis
                                                │
                                     ┌──────────▼────────┐
                                     │  Experiment Report │
                                     │  (dbt / Jupyter)   │
                                     └───────────────────┘
```

**Exposure table schema:**

```sql
CREATE TABLE experiment_exposures (
  exposure_id       STRING NOT NULL,
  experiment_name   STRING NOT NULL,
  variant           STRING NOT NULL,  -- 'control' | 'treatment'
  user_id           STRING NOT NULL,
  exposed_at        TIMESTAMP NOT NULL,
  session_id        STRING,
  device_type       STRING,
  PRIMARY KEY (experiment_name, user_id)  -- one exposure per user per experiment
);
```

**Analysis query (BigQuery example):**

```sql
WITH exposure AS (
  SELECT
    user_id,
    variant,
    DATE(exposed_at) AS exposure_date
  FROM experiment_exposures
  WHERE experiment_name = 'checkout_redesign'
    AND exposed_at BETWEEN '2024-01-01' AND '2024-01-15'
),
conversions AS (
  SELECT DISTINCT user_id
  FROM order_events
  WHERE event_type = 'purchase'
    AND created_at BETWEEN '2024-01-01' AND '2024-01-22'
)
SELECT
  e.variant,
  COUNT(DISTINCT e.user_id)                         AS users,
  COUNT(DISTINCT c.user_id)                         AS conversions,
  ROUND(COUNT(DISTINCT c.user_id) * 100.0
        / COUNT(DISTINCT e.user_id), 2)             AS conversion_rate_pct
FROM exposure e
LEFT JOIN conversions c USING (user_id)
GROUP BY e.variant
ORDER BY e.variant;
```

---

## Basic Feature Flag Setup

```typescript
// lib/featureFlags.ts
interface FeatureFlag {
  name: string;
  variants: string[];
  allocation: number[];  // Percentage for each variant
  enabled: boolean;
}

const flags: Record<string, FeatureFlag> = {
  'new_checkout_flow': {
    name: 'new_checkout_flow',
    variants: ['control', 'treatment'],
    allocation: [50, 50],
    enabled: true
  }
};

export function getVariant(
  flagName: string,
  userId: string
): string {
  const flag = flags[flagName];
  if (!flag || !flag.enabled) {
    return 'control';
  }

  // Deterministic assignment based on user ID
  const hash = hashUserId(userId, flagName);
  const bucket = hash % 100;

  let cumulative = 0;
  for (let i = 0; i < flag.variants.length; i++) {
    cumulative += flag.allocation[i];
    if (bucket < cumulative) {
      return flag.variants[i];
    }
  }

  return 'control';
}

function hashUserId(userId: string, salt: string): number {
  const str = `${userId}:${salt}`;
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash);
}
```

## React Integration

```tsx
// components/ExperimentProvider.tsx
import { createContext, useContext, ReactNode } from 'react';
import { getVariant } from '@/lib/featureFlags';
import { useUser } from '@/hooks/useUser';
import { trackEvent } from '@/lib/analytics';

interface ExperimentContextValue {
  getExperimentVariant: (experimentName: string) => string;
  trackExposure: (experimentName: string) => void;
}

const ExperimentContext = createContext<ExperimentContextValue | null>(null);

export function ExperimentProvider({ children }: { children: ReactNode }) {
  const { user } = useUser();

  const getExperimentVariant = (experimentName: string): string => {
    return getVariant(experimentName, user?.id || 'anonymous');
  };

  const trackExposure = (experimentName: string): void => {
    const variant = getExperimentVariant(experimentName);
    trackEvent('experiment_exposure', {
      experiment_name: experimentName,
      variant: variant,
      user_id: user?.id
    });
  };

  return (
    <ExperimentContext.Provider value={{ getExperimentVariant, trackExposure }}>
      {children}
    </ExperimentContext.Provider>
  );
}

export function useExperiment(experimentName: string) {
  const context = useContext(ExperimentContext);
  if (!context) {
    throw new Error('useExperiment must be used within ExperimentProvider');
  }

  const variant = context.getExperimentVariant(experimentName);

  // Track exposure on first render
  useEffect(() => {
    context.trackExposure(experimentName);
  }, [experimentName]);

  return {
    variant,
    isControl: variant === 'control',
    isTreatment: variant === 'treatment'
  };
}
```

## Usage Example

```tsx
function CheckoutPage() {
  const { variant, isTreatment } = useExperiment('new_checkout_flow');

  return (
    <div>
      {isTreatment ? (
        <NewCheckoutFlow />
      ) : (
        <CurrentCheckoutFlow />
      )}
    </div>
  );
}
```
