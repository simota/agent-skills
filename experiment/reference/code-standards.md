# Experiment Code Standards

## Good Experiment Code

```typescript
// Clear variant assignment with tracking
const { variant, isTreatment } = useExperiment('checkout_v2');

// Track exposure explicitly
useEffect(() => {
  trackEvent('experiment_exposure', {
    experiment: 'checkout_v2',
    variant
  });
}, [variant]);

// Conditional rendering with clear boundaries
return isTreatment ? <NewCheckout /> : <CurrentCheckout />;
```

## Bad Experiment Code

```typescript
// Random assignment (not deterministic)
const variant = Math.random() > 0.5 ? 'A' : 'B';

// No exposure tracking
return variant === 'A' ? <VariantA /> : <VariantB />;

// Mixing experiment logic with business logic
if (variant === 'A' && user.isPremium && date > someDate) {
  // Confounded!
}
```

## Key Rules

1. **Deterministic assignment** — Always use userId-based hashing, never `Math.random()`
2. **Explicit exposure tracking** — Track every time a user sees a variant
3. **Separation of concerns** — Never mix experiment logic with business logic
4. **Clean variant boundaries** — One clear branch per variant, no nested conditions
