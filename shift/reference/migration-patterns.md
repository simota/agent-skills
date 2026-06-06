# Migration Patterns

## Strangler Fig Pattern

Gradually replace legacy code by wrapping it with new implementation:

```
1. Create new implementation alongside old
2. Route traffic/calls through a facade
3. Gradually shift from old to new
4. Remove old code when 100% migrated
```

```typescript
// Facade that allows gradual migration
class PaymentService {
  async process(order: Order) {
    if (featureFlag('new-payment-processor')) {
      return this.newProcessor.process(order);
    }
    return this.legacyProcessor.process(order);
  }
}
```

## Branch by Abstraction

Introduce an abstraction layer before replacing implementation:

```
1. Create interface/abstraction for the component to replace
2. Refactor existing code to use the abstraction
3. Create new implementation of the abstraction
4. Switch implementations (feature flag or config)
5. Remove old implementation
```

## Parallel Run

Run old and new systems simultaneously to verify correctness:

```typescript
// Compare results during migration
async function migrateWithVerification(input: Input) {
  const [oldResult, newResult] = await Promise.all([
    legacySystem.process(input),
    newSystem.process(input)
  ]);

  if (!deepEqual(oldResult, newResult)) {
    logger.warn('Migration mismatch', { input, oldResult, newResult });
  }

  return featureFlag('use-new-system') ? newResult : oldResult;
}
```

## Migration Checklist

**Before migration:**
- [ ] Document current behavior (tests as documentation)
- [ ] Identify all integration points
- [ ] Create feature flag for gradual rollout
- [ ] Define rollback procedure
- [ ] Set up monitoring/alerting for the new system

**During migration:**
- [ ] Migrate in small, reversible increments
- [ ] Run parallel comparison where possible
- [ ] Monitor error rates and performance
- [ ] Keep old code path available for rollback

**After migration:**
- [ ] Remove feature flags and old code paths
- [ ] Update documentation
- [ ] Archive or delete legacy code
- [ ] Retrospective: document lessons learned

## Risk Assessment Matrix

| Change Type | Risk | Approach |
|-------------|------|----------|
| Polyfill removal | Low | Remove after verifying browser support |
| Library upgrade (patch/minor) | Low | Update and run tests |
| Library upgrade (major) | Medium | Read changelog, update incrementally |
| Library replacement | Medium-High | Strangler Fig + feature flag |
| Framework migration | High | Branch by Abstraction + long parallel run |
| Architecture change | Very High | Multi-phase plan with Atlas |
