# Ephemeral Environments & Test Data Strategy

Purpose: Use this file when Voyager must choose preview environments, isolate data, or keep E2E execution deterministic in parallel CI.

Contents:
- Ephemeral environment lifecycle and fit
- Test-data rules and setup ranking
- Isolation levels and auth separation
- Network interception patterns
- Environment anti-patterns and mode mapping

## Ephemeral Environments

An ephemeral environment is a full-stack environment created for a PR and destroyed when that PR closes or merges.

### Shared Staging vs Ephemeral Environments

| Dimension | Shared staging | Ephemeral environment |
|-----------|----------------|-----------------------|
| Environment count | `1-3`, shared | Auto-created per PR |
| Data pollution | High | None by default |
| Waiting time | Competes with other teams | Near zero |
| Test reliability | Lower | Higher |
| Cost | Always on | Active only during PR life |
| Feedback timing | After merge or delayed | Immediately on PR creation |

### Lifecycle

```text
Open PR
  -> provision environment
    -> run migrations and seed data
      -> execute E2E tests
        -> reviewer validates preview URL
          -> merge or close PR
            -> destroy environment
```

### Common Implementation Patterns

| Pattern | Typical tools | Strength |
|---------|---------------|----------|
| Container-based | Docker Compose + CI | Reproducible and cost-effective |
| Kubernetes-based | Namespace per PR | Scalable and production-like |
| PaaS-based | Vercel Preview, Bunnyshell | Fastest path to preview URLs |
| Hybrid | Frontend PaaS + backend containers | Good speed / fidelity balance |

### GitHub Actions Example

```yaml
name: E2E Tests on Preview
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  preview-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Start preview environment
        run: docker compose -f docker-compose.test.yml up -d

      - name: Seed database
        run: npm run db:seed:test

      - name: Run E2E tests
        run: npx playwright test --tag @smoke

      - name: Cleanup
        if: always()
        run: docker compose -f docker-compose.test.yml down -v
```

## Test Data Rules

1. Each test creates and destroys its own data.
2. Prefer API-first setup. UI-based setup is slower and flakier.
3. Use factories for consistent data generation.
4. Do not use production data unless it is safely anonymized and explicitly approved.
5. Do not share mutable data between tests.

### Setup Pattern Ranking

| Pattern | Speed | Reliability | Best use |
|---------|-------|-------------|----------|
| Direct API setup | Fast | High | User creation and test preparation |
| Direct DB setup | Fastest | Medium | Bulk data or special states |
| Fixture files | Fast | High | Static datasets |
| Seed scripts | Medium | High | Environment initialization |
| UI setup | Slow | Low | Avoid unless the setup flow itself is under test |

### Factory Example

```typescript
import { APIRequestContext } from '@playwright/test';

export class TestDataFactory {
  constructor(private api: APIRequestContext) {}

  async createUser(overrides: Partial<User> = {}): Promise<User> {
    const user = {
      email: `test-${Date.now()}@example.com`,
      name: 'Test User',
      password: 'TestPassword123!',
      ...overrides,
    };

    const response = await this.api.post('/api/test/users', { data: user });
    return response.json();
  }

  async cleanup(userId: string): Promise<void> {
    await this.api.delete(`/api/test/users/${userId}`);
  }
}
```

## Isolation Levels

| Level | Technique | Cost | Reliability |
|-------|-----------|------|-------------|
| `L1` | Fresh browser context per test | Low | Medium |
| `L2` | Unique data per test | Low | High |
| `L3` | DB transaction rollback | Medium | High |
| `L4` | Environment-level isolation | High | Highest |

### Authentication Isolation

```typescript
// Anti-pattern: every test shares the same account
const SHARED_USER = { email: 'test@example.com', password: 'test123' };

// Safer pattern: unique user per test
test('user can update profile', async ({ browser, factory }) => {
  const user = await factory.createUser();
  const storageState = await authenticateUser(user);

  const context = await browser.newContext({ storageState });
  const page = await context.newPage();
  // run the test
});
```

### Parallel Execution Rules

Use all of the following when tests run in parallel:
1. Add a timestamp or UUID to test data.
2. Use a dedicated DB schema or tenant when available.
3. Intercept external dependencies.
4. Run global-state-changing tests in `serial` mode.

## Network Interception Strategy

### Pattern Map

| Goal | Technique | Example |
|------|-----------|---------|
| Remove external API dependency | `route.fulfill()` | Payment API, email service |
| Simulate latency | `route.continue()` plus delay | Slow search results |
| Reproduce server errors | `route.fulfill({ status: 500 })` | Error states |
| Freeze response data | `route.fulfill({ body })` | Stable snapshot-like verification |

### Example

```typescript
await page.route('**/api/payment/**', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      success: true,
      transactionId: 'test-txn-001',
    }),
  });
});

await page.route('**/api/search**', async route => {
  await new Promise(resolve => setTimeout(resolve, 3000));
  await route.continue();
});
```

## Environment Anti-Patterns

| Anti-pattern | Symptom | Safer response |
|--------------|---------|----------------|
| Snowflake environment | Manual setup cannot be reproduced | Define environments as code |
| Shared environment pollution | Tests interfere with each other | Use ephemeral environments |
| Direct production data use | Privacy and stability risk | Use seeded or factory-created data |
| Environment drift | Test env no longer matches production | Standardize with Docker or Kubernetes |
| Environment queueing | Teams wait for a shared slot | Provision per PR |

## Voyager Mode Mapping

| Voyager phase | Environment type | Test-data strategy |
|---------------|------------------|--------------------|
| Plan | Design only | None |
| Automate | Local Docker or dev environment | Factory plus seed data |
| Stabilize | Ephemeral CI environment | API-first setup |
| Scale | Parallel ephemeral environments | Fully isolated data |
