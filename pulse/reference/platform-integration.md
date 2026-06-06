# Analytics Platform Integration

## Platform Landscape (2026-05 snapshot)

| Platform | Status (2026-05) | 2024-2026 highlight | Source |
|----------|-----------------|---------------------|--------|
| **GA4** | Default web analytics; biggest disruption pending | Consent Mode v2 silent enforcement began **2025-07-21** in EEA/UK (sites without proper signals saw 90-95% data drop). Server-side GTM **v3.2.0 (2025-09)** moved Google JS loading to Web Container Client. **2026-06-15 cutover**: GA4 Google Signals narrows to "signed-in user behavioral reporting only"; `ad_storage` Consent Mode parameter becomes the single gate for Google Ads data flow. | [Merkle — GA4 Data Controls 2026](https://www.merkle.com/en/merkle-now/articles-blogs/2026/updates-to-google-analytics-data-controls.html), [Seresa — Consent Mode V2 July 2025 enforcement](https://seresa.io/blog/privacy-compliance/google-consent-mode-v2-data-loss-what-broke-after-july-2025-enforcement), [Google sGTM release notes](https://developers.google.com/tag-platform/tag-manager/server-side/release-notes) |
| **Amplitude (NASDAQ: AMPL)** | Public; AMPL on NASDAQ since 2021-09-28 direct listing. Acquired **Iteratively** (2021, integrated as Amplitude Data) and **InfiniGrow** (2026-02, marketing analytics) | Autocapture GA, "Ask Amplitude" (formerly Spark AI), session replay + heatmaps, $49/mo Plus plan (mid-market re-entry) | [Wikipedia — Amplitude, Inc.](https://en.wikipedia.org/wiki/Amplitude,_Inc.) |
| **Mixpanel** | Independent; private. Pricing rebuild **2025-02** — fully event-based, **first 1M events/mo free**, Growth $0.28/1K events | Spark (AI query builder), AI Replay Summaries, Magic Playlists, **MCP Server** (Claude/ChatGPT/Cursor conversational analytics), session replay incl. React Native, **re-launched experimentation + feature flags late 2025** after earlier sunset | [Mixpanel docs — pricing](https://docs.mixpanel.com/docs/pricing), [Mixpanel blog — pricing transparency](https://mixpanel.com/blog/pricing-transparency-product-analytics/) |
| **PostHog** | OSS + cloud; consolidating product analytics + session replay + feature flags + experiments + surveys + error tracking + CDP + data warehouse | "Max" renamed to **PostHog AI** (2025) — agent inside the product that writes SQL, creates flags/surveys, plans to watch session recordings | [PostHog AI docs](https://posthog.com/docs/posthog-ai), [PostHog handbook — working with Max/PostHog AI](https://posthog.com/handbook/engineering/working-with-max-ai) |
| **Heap** | Part of **Contentsquare** since **2023-12-07** (acquisition completed). No longer independent — folded into Contentsquare Product Analytics (experience + product analytics unified). | Pricing and roadmap now controlled by Contentsquare | [Contentsquare press — acquisition complete](https://contentsquare.com/press/contentsquare-completes-acquisition-heap/) |
| **Snowplow** | License change **2024-01-08** — moved core pipeline to **Snowplow Limited Use License Agreement (SLULA)**. No longer Apache 2.0 for new releases. OSS fork **OpenSnowcat** (Apache 2.0) emerged in response. Pre-2024 OSS Collector 3.x has known CVEs — patch or front with reverse proxy enforcing payload limits. | [Snowplow OSS license change post](https://snowplow.io/snowplow-oss-license-change), [Snowplow security advisory](https://support.snowplow.io/hc/en-us/articles/26318139354909) |
| **RudderStack** | Warehouse-native CDP; **IaC-driven governance** + tracking-plan-as-code launched 2025; Databricks "Customer 360" pattern | [RudderStack — IaC governance launch](https://www.prnewswire.com/news-releases/rudderstack-accelerates-ai-native-growth-launches-iac-driven-governance-for-trusted-customer-context-302676493.html) |
| **Statsig** | Acquired by **OpenAI 2025-09-02 for $1.1B** (all-stock); founder Vijaye Raji became **CTO of Applications** at OpenAI. Operates independently from Seattle, still serves existing customers — but governance is now OpenAI. Treat as a strategic risk for vendor lock-in audits. | [OpenAI — Statsig acquisition announcement](https://openai.com/index/vijaye-raji-to-become-cto-of-applications-with-acquisition-of-statsig/) |
| **dbt Semantic Layer** | **GA October 2024** after June 2024 public preview. 2025: Tableau Cloud GA, Power BI preview, new YAML spec, Trino support — central candidate for "single metric definition" feeding GA4/Amplitude/Mixpanel/PostHog. | [dbt Cloud 2025 release notes](https://docs.getdbt.com/docs/dbt-versions/2025-release-notes), [dbt Semantic Layer docs](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl) |
| **Avo (tracking plan)** | Integrates with Amplitude Data (Amplitude's own tracking-plan product, originally **Iteratively** acquired 2021); branch-merge → publish flow. | [Avo docs — Amplitude Data publishing](https://www.avo.app/docs/publishing/publishing/amplitude-data) |

Selection rule of thumb (2026): if you want a single bundled analytics+replay+flags+experiments stack and OSS option, default to PostHog. If you need mature mid-market product analytics with strong cohort UX, Amplitude or Mixpanel. If you need warehouse-native data ownership, RudderStack or Snowplow (OSS license check required). Avoid building new dependency on Statsig governance assumptions without an exit plan.

## GA4 Implementation

```typescript
// lib/analytics.ts
import { getAnalytics, logEvent, setUserProperties } from 'firebase/analytics';

const analytics = getAnalytics();

// Track event
export function trackEvent(
  eventName: string,
  properties?: Record<string, unknown>
) {
  logEvent(analytics, eventName, properties);
}

// Set user properties
export function setUserTraits(traits: Record<string, unknown>) {
  setUserProperties(analytics, traits);
}

// Track page view
export function trackPageView(pagePath: string, pageTitle: string) {
  logEvent(analytics, 'page_view', {
    page_path: pagePath,
    page_title: pageTitle
  });
}
```

**GA4 hard limits (2026-05, free tier)**:
- 500 distinct event names per property
- 25 parameters per event (incl. auto-collected → ~20-22 custom slots)
- 50 event-scoped custom dimensions + 50 custom metrics; 25 user-scoped dimensions
- Parameter name ≤ 40 chars, parameter value ≤ 100 chars (silently truncated)
- Event-level retention: **default 2 months, max 14 months** on free tier (must be manually extended); Large/XL properties force-capped at 2 months
- BigQuery export free-tier cap **~1M events/day**; explorations sample above 10M events
- Source: [GA4 configuration limits](https://support.google.com/analytics/answer/12229528?hl=en)

## Amplitude Implementation

```typescript
// lib/analytics.ts
import * as amplitude from '@amplitude/analytics-browser';

amplitude.init(process.env.NEXT_PUBLIC_AMPLITUDE_API_KEY!);

export function trackEvent(
  eventName: string,
  properties?: Record<string, unknown>
) {
  amplitude.track(eventName, properties);
}

export function identifyUser(
  userId: string,
  traits?: Record<string, unknown>
) {
  amplitude.setUserId(userId);
  if (traits) {
    const identify = new amplitude.Identify();
    Object.entries(traits).forEach(([key, value]) => {
      identify.set(key, value as string);
    });
    amplitude.identify(identify);
  }
}

export function trackRevenue(
  productId: string,
  price: number,
  quantity: number
) {
  const revenue = new amplitude.Revenue()
    .setProductId(productId)
    .setPrice(price)
    .setQuantity(quantity);
  amplitude.revenue(revenue);
}
```

Amplitude 2026 notes: Autocapture available out-of-the-box; tracking plan governance via Amplitude Data (former Iteratively codebase); Ask Amplitude (formerly Spark AI) gives natural-language insight queries.

## Mixpanel Implementation

```typescript
// lib/analytics.ts
import mixpanel from 'mixpanel-browser';

mixpanel.init(process.env.NEXT_PUBLIC_MIXPANEL_TOKEN!);

export function trackEvent(
  eventName: string,
  properties?: Record<string, unknown>
) {
  mixpanel.track(eventName, properties);
}

export function identifyUser(
  userId: string,
  traits?: Record<string, unknown>
) {
  mixpanel.identify(userId);
  if (traits) {
    mixpanel.people.set(traits);
  }
}

export function trackPageView() {
  mixpanel.track_pageview();
}
```

Mixpanel 2026 notes: First **1M events/month free** since 2025-02 pricing rebuild ($0.28/1K events on Growth above the free tier). Session replay incl. React Native + Magic Playlists + AI Summaries available. **MCP Server** lets Claude/ChatGPT/Cursor query Mixpanel data conversationally — useful for agent-driven analytics workflows.

## PostHog Implementation

```typescript
// lib/analytics.ts
import posthog from 'posthog-js';

posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
  api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST,
  capture_pageview: false, // we'll trigger manually for SPA
  person_profiles: 'identified_only',
});

export function trackEvent(
  eventName: string,
  properties?: Record<string, unknown>
) {
  posthog.capture(eventName, properties);
}

export function identifyUser(
  userId: string,
  traits?: Record<string, unknown>
) {
  posthog.identify(userId, traits);
}
```

PostHog 2026 notes: All-in-one (product analytics + session replay + feature flags + experiments + surveys + error tracking + CDP + data warehouse + LLM observability). **PostHog AI** (formerly Max) acts as in-product analyst — writes SQL, creates flags, plans to analyze session recordings. OSS-friendly when self-hosted.

## React Hook for Analytics

```typescript
// hooks/useAnalytics.ts
import { useCallback, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { trackEvent, trackPageView } from '@/lib/analytics';

export function useAnalytics() {
  const pathname = usePathname();

  // Auto-track page views
  useEffect(() => {
    trackPageView(pathname, document.title);
  }, [pathname]);

  // Track custom events
  const track = useCallback((
    eventName: string,
    properties?: Record<string, unknown>
  ) => {
    trackEvent(eventName, {
      ...properties,
      page_path: pathname
    });
  }, [pathname]);

  return { track };
}

// Usage
function CheckoutButton() {
  const { track } = useAnalytics();

  const handleClick = () => {
    track('checkout_started', { cart_value: 9800 });
    // ... proceed to checkout
  };

  return <button onClick={handleClick}>Checkout</button>;
}
```
