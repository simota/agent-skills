# Pulse Code Standards

## Good Pulse Code

```typescript
// Clear event naming with typed properties
interface CheckoutStartedEvent {
  cart_value: number;
  item_count: number;
  currency: 'JPY' | 'USD';
}

function trackCheckoutStarted(props: CheckoutStartedEvent) {
  trackEvent('checkout_started', props);
}

// Consent-aware tracking
if (hasConsent('analytics')) {
  trackCheckoutStarted({
    cart_value: cart.total,
    item_count: cart.items.length,
    currency: 'JPY'
  });
}
```

## Bad Pulse Code

```typescript
// Vague event names, untyped properties
trackEvent('click', { data: someObject });

// PII in tracking
trackEvent('signup', { email: user.email, phone: user.phone });

// No consent check
trackEvent('page_view', { path: window.location.href });
```
