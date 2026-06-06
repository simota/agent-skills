# Privacy & Consent Management

## 2025-2026 Regulatory Timeline (must-know dates)

| Date | Event | What changes | Source |
|------|-------|-------------|--------|
| **2024-07-22** | Google reverses third-party cookie deprecation in Chrome | Cookies stay; Privacy Sandbox de-emphasized, no standalone consent prompt added | [OneTrust — Google drops third-party cookie prompt](https://www.onetrust.com/blog/google-drops-plans-for-third-party-cookie-choice-prompt-in-chrome/) |
| **2025-04-22** | Google formally cancels third-party cookie deprecation; "user choice" model only | Chrome default = third-party cookies allowed; users must opt to block | [Cookie-Script — new future of cookies](https://cookie-script.com/news/new-future-of-cookies-user-choice-vs-browser-deprecation) |
| **2025-06-19** | **IAB TCF v2.3 released** | Replaces v2.2; resolves vendor disclosure signaling ambiguity | [IAB Europe — TCF transition](https://iabeurope.eu/all-you-need-to-know-about-the-transition-to-tcf-v2-3/) |
| **2025-07-21** | **Google Consent Mode v2 silent enforcement begins** in EEA/UK | Sites without proper consent signals lose ad conversions, remarketing, demographics for EEA/UK traffic; 90-95% data drops common on misconfigured WordPress/Shopify | [Seresa — Consent Mode V2 enforcement aftermath](https://seresa.io/blog/privacy-compliance/google-consent-mode-v2-data-loss-what-broke-after-july-2025-enforcement) |
| **2025-10-17** | **Privacy Sandbox APIs retired** | Topics / Protected Audience (FLEDGE) / Attribution Reporting / 7 others deprecated. Only CHIPS, FedCM, Private State Tokens remain | [Adweek — Privacy Sandbox dead](https://www.adweek.com/media/googles-privacy-sandbox-is-officially-dead/) |
| **2026-02-28** | **TCF v2.3 mandatory adoption deadline** | Non-migrated participants: consent strings invalid → "Limited Ads" fallback → potential >50% programmatic revenue loss | [IAB TCF v2.3 publisher guide](https://www.cookieyes.com/blog/iab-tcf-v2-3-explained/) |
| **2026-04-07** | **Japan APPI amendment bill approved by Cabinet** | Adds biometric "Specific Biometric Personal Information" category; child-data protections (<16 parental consent); first-ever **administrative monetary penalties (surcharges)** in APPI history; AI-training statistical processing exemption | [Mori Hamada — APPI 2026 amendments](https://www.morihamada.com/en/insights/newsletters/138006), [Fisher Phillips — APPI 7 steps](https://www.fisherphillips.com/en/insights/insights/japanese-cabinet-approves-appi-amendments) |
| **2026-06-15** | **GA4 + Google Ads consent control split** | Google Signals narrows to "signed-in user behavioral reporting only"; `ad_storage` Consent Mode parameter is the single gate for Google Ads data flow. Turning off Google Signals will no longer stop Google Ads cookie/ID collection. Audit CMP + tag setup before cutover. | [Merkle — GA4 Data Controls 2026](https://www.merkle.com/en/merkle-now/articles-blogs/2026/updates-to-google-analytics-data-controls.html) |

Tactical posture for 2026: assume third-party cookies persist in Chrome, but treat them as legally hazardous (GDPR/ePrivacy still applies). Default to server-side first-party tracking + Consent Mode v2 Advanced (cookieless pings + behavioral modeling) — Advanced Mode recovers ~70% of denied-consent conversions when ≥1,000 daily denied events sustain for 7 days.

## Consent Management

```typescript
// lib/consent.ts
type ConsentCategory = 'analytics' | 'marketing' | 'functional';

interface ConsentState {
  analytics: boolean;
  marketing: boolean;
  functional: boolean;
}

export function getConsentState(): ConsentState {
  const stored = localStorage.getItem('user_consent');
  if (stored) {
    return JSON.parse(stored);
  }
  return {
    analytics: false,
    marketing: false,
    functional: true
  };
}

export function setConsentState(consent: ConsentState) {
  localStorage.setItem('user_consent', JSON.stringify(consent));

  // Update analytics based on consent
  if (consent.analytics) {
    enableAnalytics();
  } else {
    disableAnalytics();
  }
}

export function hasConsent(category: ConsentCategory): boolean {
  return getConsentState()[category];
}
```

## Google Consent Mode v2 — required signals

The CMP **must** forward all four signals (defaults `denied`, updated after user choice) to Google tags before any GA4 / Google Ads event fires:

```javascript
// Default (before consent) — denied
gtag('consent', 'default', {
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  analytics_storage: 'denied',
  wait_for_update: 500
});

// After user choice — update
gtag('consent', 'update', {
  ad_storage: userConsent.marketing ? 'granted' : 'denied',
  ad_user_data: userConsent.marketing ? 'granted' : 'denied',
  ad_personalization: userConsent.marketing ? 'granted' : 'denied',
  analytics_storage: userConsent.analytics ? 'granted' : 'denied'
});
```

Common failure modes (each silently kills EEA/UK measurement):
- CMP loads after gtag (signals arrive too late).
- Only `analytics_storage` is signaled (ads parameters missing → Google Ads goes blind).
- Banner cosmetic-only (no actual signal wiring) — most common WordPress failure.
- Forgetting `wait_for_update` → events fire before consent resolves.
- Using `ad_storage='granted'` based on `functional` instead of `marketing` consent.

After **2026-06-15**: `ad_storage` is the only knob for Google Ads data; treat the GA4 Google Signals toggle as a reporting-only setting that does **not** stop ad data collection.

## Privacy-Safe Tracking

```typescript
// Track only with consent
export function trackEventWithConsent(
  eventName: string,
  properties?: Record<string, unknown>
) {
  if (!hasConsent('analytics')) {
    return;
  }

  // Remove PII from properties
  const safeProperties = removePII(properties);
  trackEvent(eventName, safeProperties);
}

function removePII(
  properties?: Record<string, unknown>
): Record<string, unknown> | undefined {
  if (!properties) return undefined;

  const piiFields = ['email', 'phone', 'name', 'address', 'ip'];
  const safe = { ...properties };

  piiFields.forEach(field => {
    if (field in safe) {
      delete safe[field];
    }
  });

  return safe;
}
```
