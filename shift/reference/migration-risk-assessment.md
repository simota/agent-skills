# Migration Risk Assessment

Full risk matrix, Strategy Selection Decision Tree, and per-strategy implementation detail → `reference/migration-strategies.md` (`## Strategy Selection Decision Tree`, `## Risk Assessment Matrix`).

## Quick Risk Factors

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| Files affected | < 10 | 10-50 | > 50 |
| API changes | None | Minor | Breaking |
| Test coverage | > 80% | 50-80% | < 50% |
| Rollback ease | Simple revert | Partial | Complex |
