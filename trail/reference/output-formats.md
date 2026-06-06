# Trail Output Formats

## Timeline Visualization

```
                    TRAIL TIMELINE
    ════════════════════════════════════════════

    ✓ GOOD: v2.0.0 (abc1234) 2024-01-01
    │
    │ ○ def5678 - Add user caching
    │ │   Author: alice@example.com
    │ │   Files: +2, ~1
    │
    │ ○ ghi9012 - Update dependencies
    │ │   Author: bob@example.com
    │ │   Files: ~1
    │
    │ ● jkl3456 - Refactor auth module  ← BREAKING
    │ │   Author: charlie@example.com
    │ │   Files: ~5, -1
    │ │
    │ │   This commit changed the token validation
    │ │   logic, breaking existing sessions.
    │
    │ ○ mno7890 - Fix typo in docs
    │   Author: dave@example.com
    │   Files: ~1
    │
    ✗ BAD: HEAD (pqr1234) 2024-01-15

    Legend: ✓ Good  ✗ Bad  ● Breaking  ○ Neutral
```

## Investigation Summary

```markdown
## Trail Investigation Summary

| Property | Value |
|----------|-------|
| **Investigation Type** | Regression Hunt |
| **Symptom** | Login fails with "Invalid token" |
| **Search Range** | v2.0.0..HEAD (47 commits) |
| **Bisect Steps** | 6 |
| **Root Cause** | jkl3456 |
| **Confidence** | High (95%) |

### Breaking Commit Details

commit jkl3456789abcdef
Author: charlie@example.com
Date: 2024-01-10

Refactor auth module for better performance

- Simplified token validation
- Removed legacy compatibility layer
- Updated session handling

### Why It Broke

The commit removed the legacy compatibility layer that handled
tokens in the old format. Existing sessions had tokens in the
old format, causing validation failures.

### Recommended Actions

1. **Immediate:** Revert jkl3456 or add backward compatibility
2. **Short-term:** Migrate existing sessions to new token format
3. **Long-term:** Add integration tests for token compatibility
```
