# E2E Testing Anti-Patterns & Test Architecture

Purpose: Use this file to keep Voyager suites small, deterministic, and maintainable.

Contents:
- Anti-patterns that cause brittle or bloated suites
- Flaky root causes, targets, and retry limits
- Suite architecture ratios, tags, and runtime goals
- Maintenance rules that preserve long-term stability

## Anti-Patterns

| Anti-pattern | Symptom | Safer rule |
|--------------|---------|------------|
| Selector fragility | UI refactors break tests for non-user-facing reasons | Prefer `getByRole`, `getByLabel`, or `getByTestId` |
| Test interdependence | One failure cascades through the suite | Make every test create and clean up its own data |
| Excessive waiting | Slow, flaky suites with arbitrary timing | Wait on UI state, network events, or explicit conditions |
| Test bloat | One giant test hides the failing business goal | Split by business outcome |
| Wrong test level | E2E covers logic that belongs in unit or integration tests | Keep E2E for critical user journeys only |
| Test explosion | AI or manual growth creates redundant suites and CI cost | Tag, prune, and keep only business-critical coverage in CI |

### Selector Fragility

```typescript
// Anti-pattern: position-based or CSS-class selectors
await page.click('div:nth-child(3) > button');
await page.click('.btn-primary-v2');

// Safer pattern: semantic or intentional selectors
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByTestId('checkout-button').click();
```

Impact: every UI refactor becomes a test-maintenance event.

### Test Interdependence

```text
Anti-pattern:
  Test A creates a user -> Test B logs in as that user -> Test C updates the profile
  If Test A fails, B and C fail for the wrong reason.

Safer pattern:
  Each test creates its own data -> runs the scenario -> cleans up.
```

Rule: use API-first setup plus a fresh browser context for each test.

### Excessive Waiting

```typescript
// Anti-pattern: arbitrary timeout
await page.waitForTimeout(5000);

// Safer pattern: explicit condition
await page.waitForResponse(resp => resp.url().includes('/api/data'));
await expect(page.getByRole('heading')).toBeVisible();
```

Rule: let Playwright auto-wait whenever possible. Add explicit waits only for a concrete signal.

### Test Bloat

```text
Anti-pattern:
  One 100-step flow covers login -> profile -> search -> cart -> payment -> order confirmation.

Safer pattern:
  - user can log in
  - user can add an item to the cart
  - user can complete checkout
```

### Wrong Test Level

| Do not cover with E2E | Better test level |
|-----------------------|-------------------|
| Input validation rules | Unit |
| Data transformation or formatting | Unit |
| API response shape | Integration / contract |
| Single-component rendering | Component |

### Test Explosion

2026 risk: AI-assisted generation makes it easy to create hundreds of tests. The bottleneck becomes deciding what belongs in CI and what is redundant.

Rules:
- Tag with `@critical`, `@smoke`, or `@regression`.
- Keep CI coverage focused on business-critical paths.
- Prune redundant or low-value tests on a regular cadence.

## Flaky Prevention

### Root Causes

| Cause | Typical share | Primary mitigation |
|-------|---------------|--------------------|
| Timing / async issues | 40% | Auto-waiting and explicit condition waits |
| Test-data pollution | 25% | API-first setup and isolation |
| Environment mismatch | 20% | Ephemeral environments or Docker |
| Shared state | 10% | Fresh browser context and isolated accounts |
| External dependencies | 5% | Network interception and mocks |

### Targets

- Keep flaky rate below `1%`.
- Limit retries to a maximum of `2`.
- Track root cause, not just retry success.

### Flaky Prevention Checklist

```markdown
## Flaky Prevention Checklist

### Design
- [ ] Can the test run independently?
- [ ] Is test data created through an API or factory?
- [ ] Does the test avoid `waitForTimeout()`?
- [ ] Are external services mocked or intercepted when needed?

### Implementation
- [ ] Do locators support Playwright auto-waiting?
- [ ] Are network waits explicit when they matter?
- [ ] Are animations or loading states handled intentionally?
- [ ] Is the test free from date, timezone, and locale fragility?

### CI
- [ ] Do repeated runs surface flake before merge?
- [ ] Is flaky rate below `1%`?
- [ ] Are retries capped at `2`?
- [ ] Is each flaky failure assigned a root cause?
```

## Suite Architecture

### Test Pyramid Ratio

```text
E2E: 5-10%
  -> business-critical journeys only
  -> target runtime below 30 minutes
  -> parallel execution plus sharding
  -> tag-based prioritization

Integration: 20%
Unit: 70%
```

### Recommended Layout

```text
tests/
  e2e/
    auth/
      login.spec.ts
      signup.spec.ts
    checkout/
      cart.spec.ts
      payment.spec.ts
    settings/
      profile.spec.ts
  fixtures/
    auth.fixture.ts
    data.fixture.ts
  pages/
    LoginPage.ts
    CheckoutPage.ts
  helpers/
    api-client.ts
    test-data-factory.ts
```

### Tag Strategy

| Tag | Run timing | Typical content | Target runtime |
|-----|------------|-----------------|----------------|
| `@smoke` | Every PR | Login and the shortest critical flows | `< 5 min` |
| `@critical` | Before merge | Checkout, auth, and data mutation flows | `< 15 min` |
| `@regression` | Nightly | Full E2E suite | `< 30 min` |
| `@visual` | Weekly or manual | Visual regression | Variable |

## Maintenance Rules

Treat test code like production code:
1. Review it.
2. Refactor it.
3. Keep naming consistent, such as `should_verb_when_condition`.
4. Keep helpers and fixtures DRY.
5. Prune dead or redundant tests regularly.

### Patterns That Reduce Cost

| Pattern | Benefit |
|---------|---------|
| Page Object Model | Localizes UI change impact |
| Test-data factory | Centralizes data creation |
| Custom fixtures | Reuses setup logic |
| Network interception | Removes external flake |
| Tag-based execution | Runs only the tests that matter |

Sources: [Thunders.ai: Modern E2E Test Architecture](https://www.thunders.ai/articles/modern-e2e-test-architecture-patterns-and-anti-patterns-for-a-maintainable-test-suite) · [Bunnyshell: E2E Testing Best Practices 2025](https://www.bunnyshell.com/blog/best-practices-for-end-to-end-testing-in-2025/) · [Playwright: Best Practices](https://playwright.dev/docs/best-practices) · [Momentic: Playwright E2E Best Practices](https://momentic.ai/blog/playwright-e2e-testing-best-practices)
