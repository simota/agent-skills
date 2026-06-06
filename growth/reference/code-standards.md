# Growth Code Standards

## Good Growth Code

```typescript
// Rich Snippet (JSON-LD) for Search Engines
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Awesome Tool",
  "description": "Boost your productivity..."
}
</script>

// Clear Call-to-Action (CTA) with descriptive link
<a href="/signup" className="btn-primary" onClick={trackSignupClick}>
  Start your free trial
</a>
```

## Google Consent Mode v2

Consent Mode v2 is required for Google Ads conversion modeling when users decline cookies. It introduces 4 parameters and must be loaded before any Google tag.

### Required Parameters

| Parameter | Controls |
|-----------|----------|
| `analytics_storage` | GA4 measurement cookies |
| `ad_storage` | Google Ads cookies |
| `ad_user_data` | Sending user data to Google for ads |
| `ad_personalization` | Personalized advertising |

### Advanced Mode Implementation (with conversion modeling)

```typescript
type ConsentValue = 'granted' | 'denied';

interface ConsentState {
  analytics_storage: ConsentValue;
  ad_storage: ConsentValue;
  ad_user_data: ConsentValue;
  ad_personalization: ConsentValue;
}

// Step 1: Initialize gtag with default denied state BEFORE loading gtag.js
// This must run synchronously before the Google tag script
function initConsentMode(defaultState: Partial<ConsentState> = {}): void {
  window.dataLayer = window.dataLayer ?? [];
  function gtag(...args: unknown[]) { window.dataLayer.push(args); }

  // Set defaults — denied by default for GDPR compliance
  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    wait_for_update: 500, // ms to wait for CMP to respond
    ...defaultState,
  });
}

// Step 2: After user interacts with CMP, update consent state
function updateConsent(state: ConsentState): void {
  function gtag(...args: unknown[]) { window.dataLayer.push(args); }
  gtag('consent', 'update', state);
}

// Step 3: Typical CMP integration pattern
function onCMPResponse(userAcceptedAll: boolean): void {
  if (userAcceptedAll) {
    updateConsent({
      analytics_storage: 'granted',
      ad_storage: 'granted',
      ad_user_data: 'granted',
      ad_personalization: 'granted',
    });
  } else {
    // Partial consent — analytics only, no ad personalization
    updateConsent({
      analytics_storage: 'granted',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
    });
  }
}

// HTML load order (CRITICAL — CMP and consent init must precede gtag.js)
// <script>/* initConsentMode() call */</script>
// <script>/* CMP SDK */</script>
// <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"></script>
```

> **Advanced Mode** enables conversion modeling for users who declined consent, recovering ~20-30% of conversion signal. Requires enrolling the property in Google Ads and GA4 settings.

## Bad Growth Code

```typescript
// "Click here" is bad for SEO and Accessibility
<a href="/signup">Click here</a>

// Missing Open Graph tags (looks ugly on Twitter/Slack)
<head>
  <title>Home</title>
  {/* No description, no image... */}
</head>
```
