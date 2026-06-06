# Hotfix Release Workflow

Purpose: Emergency patch release for Sev1/Sev2 production issues. Delivers the fix in ≤ 2h with controlled risk: shortened CI, isolated hotfix branch, mandatory rollback readiness, and a backport plan to main.

## When to Trigger

| Signal | Trigger |
|--------|---------|
| Sev1 (prod down / data loss / security breach) | Immediate — activate hotfix |
| Sev2 (degraded prod affecting >10% users) | Within 30 min — activate hotfix |
| Sev3 (minor user impact, workaround exists) | Use normal release flow, not hotfix |
| Security CVE on production | Always hotfix regardless of severity |

**Do not use hotfix for**: features, refactors, nice-to-haves, "while we're at it" changes.

## Timeline Targets (Elite)

| Phase | Duration | Owner |
|-------|----------|-------|
| Incident → root cause confirmed | ≤ 30 min | Scout / Triage |
| Fix implemented + unit tested locally | ≤ 30 min | Builder |
| PR opened + reviewed + merged to hotfix branch | ≤ 30 min | Guardian + Judge |
| CI smoke + deploy to prod | ≤ 30 min | Gear |
| **Total lead time** | **≤ 2h** | |
| Post-incident: backport to main + postmortem | ≤ 48h | Triage + Launch |

## Branch Strategy

```
main        ────●────●────●────────●────
                │                    │
                │                    └─ backport (48h)
tag: v2.4.0 ────┤
                │
hotfix/v2.4.1 ──●─── fix ─── tag v2.4.1 ─── deploy
```

**Never** hotfix directly from main — always branch from the production tag to avoid pulling in unshipped changes.

```bash
# Branch from last production tag, NOT from main
git checkout -b hotfix/v2.4.1 v2.4.0
# ... apply minimal fix ...
git tag v2.4.1
git push origin hotfix/v2.4.1 v2.4.1
```

## Minimal-Diff Principle

- ≤ 50 lines of code changed
- ≤ 3 files touched
- Zero refactoring, formatting, or unrelated cleanup
- Zero new dependencies
- Tests added only for the specific regression

Any deviation requires explicit Go/No-Go from release manager.

## Shortened CI Gates

| Gate | Normal release | Hotfix |
|------|----------------|--------|
| Unit tests (affected paths only) | ✓ | ✓ |
| Lint / typecheck | ✓ | ✓ |
| Smoke E2E (critical path) | ✓ | ✓ |
| Full E2E suite | ✓ | ⏩ skip (run post-deploy) |
| Security scan (gitleaks) | ✓ | ✓ |
| Full dependency scan | ✓ | ⏩ skip |
| Performance regression | ✓ | ⏩ skip |
| Approvals | 2 reviewers | 1 reviewer + on-call lead |

Skipped gates must run asynchronously on `hotfix/*` branch and report before the next release cut.

## Rollback Readiness

**Every hotfix PR must answer:**

1. **Rollback method**: re-deploy previous image tag / revert migration / toggle feature flag
2. **Rollback SLO**: ≤ 5 minutes to revert
3. **Forward-fix plan**: if rollback alone doesn't resolve (e.g., schema change), what's the recovery path
4. **Monitoring window**: minimum 30 min post-deploy with oncall watching

If rollback is not possible (destructive migration, one-way data change), **hotfix is NOT APPROVED** — escalate to incident commander for explicit exception.

## Backport Plan

After hotfix ships:

```
v2.4.0 ────────●──────●── main (needs backport)
               ↑      
               └── fix commit on hotfix/v2.4.1
```

- Cherry-pick the fix commit onto main within 48h
- Verify via merge-base: `git merge-base --is-ancestor <hotfix-sha> main`
- Add regression test to main
- Document in postmortem

## Playbook Template

```markdown
# Hotfix v2.4.1 Playbook

**Incident**: INC-2026-0424-01 (Checkout API 500 errors)
**Severity**: Sev2 (14% of checkout requests failing)
**RCA source**: Scout investigation `#1234` (root cause: null pointer in v2.4.0 commit `a1b2c3d`)

## Fix Summary
- **Change**: null-check added in `checkout/service.ts:payment_flow`
- **Diff**: +8 / -0 lines, 1 file
- **Branch**: `hotfix/v2.4.1` from tag `v2.4.0`

## CI Gates (reduced)
- [x] Unit tests (checkout/*)
- [x] Lint + typecheck
- [x] Smoke E2E
- [x] Secret scan
- [ ] Full E2E (deferred to async job)

## Deployment
- [ ] Tag `v2.4.1` pushed
- [ ] Build artifact published
- [ ] Deploy to canary (5% traffic, 10 min)
- [ ] Promote to 100%

## Rollback Plan
- **Method**: `kubectl rollout undo deploy/checkout-api` → reverts to v2.4.0 image
- **SLO**: < 3 min to revert
- **Trigger condition**: any of {error rate > 0.5%, p95 > 500ms, new 5xx burst}

## Monitoring
- **Window**: 60 min post-deploy, on-call active
- **Dashboards**: [Checkout SLO](link), [Error Budget](link)
- **Success**: error rate < 0.1% for 30 continuous minutes

## Post-Incident (within 48h)
- [ ] Backport `a9b8c7` to main
- [ ] Add regression test `test/checkout/null_payment.spec.ts`
- [ ] Postmortem published
- [ ] Process improvement: add null-check linter rule (handoff Gear)

## Stakeholder Comms
- [ ] #incidents Slack update every 15 min during rollout
- [ ] Status page updated on deploy start / success / failure
- [ ] Customer Support notified when resolved
```

## Anti-Patterns

- Hotfixing from main (pulls in unshipped changes)
- Bundling unrelated fixes ("while we're hotfixing, let's also...")
- Skipping rollback plan (there is no fallback)
- Single reviewer without on-call oversight
- Running only on happy path (missing smoke on the regression path)
- Forgetting to backport (regression reappears on next release)
- No post-deploy monitoring (fix was wrong, nobody notices for hours)
- Treating every Sev3 as hotfix (hotfix fatigue, process erosion)

## Handoffs

- **Scout → Launch**: RCA confirmation triggers hotfix branching decision
- **Builder → Guardian**: fix PR must pass `guardian pr` with hotfix-size allowance
- **Gear → Beacon**: deploy emits events for oncall dashboard
- **Launch → Triage**: if rollback triggers, escalate incident commander
- **Launch → Harvest**: generate abbreviated release note for changelog
