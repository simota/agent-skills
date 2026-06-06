# Migration Risk Assessment

## Risk Matrix

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| Files affected | < 10 | 10-50 | > 50 |
| API changes | None | Minor | Breaking |
| Test coverage | > 80% | 50-80% | < 50% |
| Rollback ease | Simple revert | Partial | Complex |

## Migration Strategies
1. **Big bang** - Replace all at once (low file count)
2. **Strangler fig** - Gradually replace (high file count)
3. **Adapter pattern** - Wrap old with new interface
4. **Feature flag** - Toggle between old/new
