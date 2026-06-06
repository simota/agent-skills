# Launch Examples

Purpose: Use this file when you need a compact worked example for a standard release, hotfix, feature-flag rollout, or Go/No-Go decision.

## Contents

1. Standard minor release
2. Hotfix release
3. Feature flag rollout
4. Go/No-Go decision

## 1. Standard Minor Release

### Input

```text
Prepare the next release. OAuth sign-in and report export are complete.
```

### Minimal Launch Response Shape

```markdown
## Release Plan: v1.2.0

### Version
- Change type: backwards-compatible feature
- Recommended version: 1.2.0

### CHANGELOG Summary
- Added: OAuth sign-in
- Added: PDF / CSV export
- Fixed: login timeout under load

### Rollback Plan
1. Disable feature flag (< 1 minute)
2. Deployment rollback (2-5 minutes)
3. No DB rollback required

### Release Checklist
- Tests pass
- Staging verified
- CHANGELOG committed
- Tag ready
- Smoke test defined
```

## 2. Hotfix Release

### Input

```text
Production authentication is failing. We need an emergency fix.
```

### Minimal Launch Response Shape

```markdown
## Hotfix Plan: v1.2.1

### Assessment
- Issue: critical authentication failure
- Release type: PATCH hotfix

### Procedure
1. Branch from release tag:
   git checkout -b hotfix/v1.2.1 v1.2.0
2. Apply minimum fix
3. Fast review
4. Deploy with smoke check
5. Tag and cherry-pick back to main

### Rollback
- Roll back to v1.2.0 if the issue persists
- Do not disable authentication entirely without explicit approval
```

## 3. Feature Flag Rollout

### Input

```text
We want to release the new payment flow gradually.
```

### Minimal Launch Response Shape

```markdown
## Feature Flag Rollout Plan: payment-v2

### Flag Metadata
- owner: @payment-team
- expires: 2026-05-15
- cleanup ticket: PAY-789

### Stages
1. Internal only
2. 5%
3. 25%
4. 50%
5. 100%

### Success Criteria
- error rate < 2%
- payment success rate > 99%
- p95 latency < 500ms

### Emergency Rollback
- Disable the flag immediately (< 1 minute)
```

## 4. Go/No-Go Decision

### Input

```text
Can tomorrow's release go out as planned?
```

### Minimal Launch Response Shape

```markdown
## Go/No-Go Decision: v1.2.0

### Result
- Decision: NO-GO
- Blockers: 1

### Mandatory Checks
| Gate | Status | Required |
|------|--------|----------|
| Tests | PASS | Yes |
| Security | PASS | Yes |
| Staging | PASS | Yes |
| Rollback test | PASS | Yes |
| CHANGELOG | FAIL | Yes |

### Next Actions
1. Complete the missing CHANGELOG entry
2. Re-run the Go/No-Go check
3. Release only after all mandatory gates pass
```
