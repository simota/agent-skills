# Migration Patterns

Strangler Fig / Branch by Abstraction / Parallel Run pattern definitions, implementation steps, and code examples → `reference/migration-strategies.md`.

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
