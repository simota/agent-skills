# E2E Environment Management

Purpose: Use this file when Voyager must stand up, seed, or parameterize the environments used by E2E suites.

Contents:
- Docker, DB seeding, and preview-environment setup
- Auth state, env vars, mail capture, and service mocking
- Local-only workflow and environment-choice rules

---

## Agent Boundary

| Responsibility | Voyager | Gear | Scaffold |
|----------------|---------|------|----------|
| **E2E-specific Docker Compose** | ✅ Primary | | |
| **Test DB seeding** | ✅ Primary | | |
| **Dynamic preview environments** | ✅ E2E config | | |
| **CI/CD pipeline (general)** | | ✅ Primary | |
| **Docker infrastructure (general)** | | ✅ Primary | |
| **IaC / cloud provisioning** | | | ✅ Primary |
| **Dev environment setup** | | | ✅ Primary |

**Rule of thumb**: Voyager owns E2E-specific environment configuration. Gear owns general CI/Docker. Scaffold owns infrastructure provisioning.

---

## Docker Compose for E2E

### Template

```yaml
# docker-compose.e2e.yml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://test:test@db:5432/testdb
      - REDIS_URL=redis://redis:6379
      - SMTP_HOST=mailhog
      - SMTP_PORT=1025
      - NODE_ENV=test
# ...
```

### Startup Wait Script

```bash
#!/bin/bash
# scripts/wait-for-e2e.sh
set -e

echo "Starting E2E environment..."
docker compose -f docker-compose.e2e.yml up -d

echo "Waiting for services..."
MAX_RETRIES=30
RETRY_COUNT=0

until curl -sf http://localhost:3000/api/health > /dev/null 2>&1; do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "ERROR: App failed to start after $MAX_RETRIES attempts"
# ...
```

---

## Test Database Seeding

### Global Setup with Prisma

```typescript
// e2e/global-setup.ts
import { chromium, FullConfig } from '@playwright/test';
import { execSync } from 'child_process';

async function globalSetup(config: FullConfig) {
  // Reset and seed database
  execSync('npx prisma migrate reset --force --skip-seed', {
    env: { ...process.env, DATABASE_URL: process.env.TEST_DATABASE_URL },
    stdio: 'pipe',
  });

  // Run seed script
  execSync('npx prisma db seed', {
    env: { ...process.env, DATABASE_URL: process.env.TEST_DATABASE_URL },
    stdio: 'pipe',
// ...
```

### Drizzle Seed

```typescript
// e2e/seed/seed.ts
import { drizzle } from 'drizzle-orm/node-postgres';
import { users, products, orders } from '../../src/db/schema';

export async function seedTestData(connectionString: string) {
  const db = drizzle(connectionString);

  // Clean tables in dependency order
  await db.delete(orders);
  await db.delete(products);
  await db.delete(users);

  // Seed users
  const [admin] = await db.insert(users).values([
    { email: 'admin@test.com', name: 'Admin', role: 'admin', passwordHash: '...' },
// ...
```

### Transaction Rollback Strategy

```typescript
// e2e/fixtures/db.fixture.ts
import { test as base } from '@playwright/test';
import { Pool } from 'pg';

export const test = base.extend<{ dbCleanup: void }>({
  dbCleanup: [async ({}, use) => {
    const pool = new Pool({ connectionString: process.env.TEST_DATABASE_URL });

    // Save point before test
    const client = await pool.connect();
    await client.query('BEGIN');
    await client.query('SAVEPOINT test_start');

    await use();

// ...
```

### Data Isolation Strategy

| Strategy | Speed | Isolation | Use When |
|----------|-------|-----------|----------|
| **Transaction rollback** | Fast | High | DB-heavy tests |
| **Unique prefixes** | Fast | Medium | Parallel-friendly |
| **Per-test DB** | Slow | Perfect | Critical financial tests |
| **Truncate + reseed** | Medium | High | Suite-level reset |

```typescript
// ✅ GOOD: Unique data per test (parallel-safe)
test('user signup', async ({ page }) => {
  const uniqueEmail = `test-${Date.now()}@example.com`;
  await page.goto('/signup');
  await page.getByLabel('Email').fill(uniqueEmail);
  // ...
});
```

---

## Dynamic Environment Provisioning

### Vercel Preview + Playwright

```yaml
# .github/workflows/e2e-preview.yml
name: E2E on Preview

on:
  deployment_status:

jobs:
  e2e:
    if: github.event.deployment_status.state == 'success'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
# ...
```

### Dynamic BASE_URL

```typescript
// playwright.config.ts
const getBaseURL = (): string => {
  // PR preview
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  // Staging
  if (process.env.STAGING_URL) return process.env.STAGING_URL;
  // Local
  return process.env.BASE_URL || 'http://localhost:3000';
};

export default defineConfig({
  use: {
    baseURL: getBaseURL(),
  },
});
```

---

## Environment Variable Management

### .env.test Template

```bash
# .env.test
# Database
TEST_DATABASE_URL=postgresql://test:test@localhost:5433/testdb

# App
BASE_URL=http://localhost:3000
NODE_ENV=test

# Auth (test credentials)
TEST_USER_EMAIL=user@test.com
TEST_USER_PASSWORD=Test1234!
TEST_ADMIN_EMAIL=admin@test.com
TEST_ADMIN_PASSWORD=Admin1234!

# External services (test mode)
# ...
```

### CI Secrets Mapping

```yaml
# .github/workflows/e2e.yml
env:
  BASE_URL: http://localhost:3000
  TEST_DATABASE_URL: postgresql://test:test@localhost:5433/testdb
  TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
  TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
  STRIPE_SECRET_KEY: ${{ secrets.STRIPE_TEST_SECRET_KEY }}
```

### dotenv-flow for Environment Switching

```typescript
// e2e/global-setup.ts
import { config } from 'dotenv-flow';

// Loads .env.test → .env.test.local (ignored in git)
config({ path: '.', node_env: 'test' });
```

---

## Test Mail Server

### Mailhog Integration

```typescript
// e2e/utils/mail-helpers.ts
import { APIRequestContext } from '@playwright/test';

export class MailHelper {
  constructor(
    private mailhogUrl: string = 'http://localhost:8025',
    private request: APIRequestContext,
  ) {}

  async getLatestEmail(to: string) {
    const response = await this.request.get(
      `${this.mailhogUrl}/api/v2/search?kind=to&query=${to}`
    );
    const data = await response.json();
    return data.items[0];
// ...
```

### OTP / Magic Link E2E Test

```typescript
test('completes OTP verification', async ({ page, request }) => {
  const mail = new MailHelper('http://localhost:8025', request);
  await mail.clearMailbox();

  const email = `test-${Date.now()}@example.com`;

  // Request OTP
  await page.goto('/signup');
  await page.getByLabel('Email').fill(email);
  await page.getByTestId('send-otp').click();

  // Wait for email delivery
  await page.waitForTimeout(1000); // Acceptable: waiting for external service

  // Extract OTP from email
// ...
```

---

## External Service Mocking

### MSW in E2E Context

```typescript
// e2e/utils/msw-setup.ts
import { createServer } from '@mswjs/http-middleware';
import { http, HttpResponse } from 'msw';

// Start mock server for external APIs
export function startMockServer(port = 9090) {
  const handlers = [
    http.post('https://api.stripe.com/v1/charges', () => {
      return HttpResponse.json({
        id: 'ch_test_123',
        status: 'succeeded',
        amount: 2500,
      });
    }),
    http.get('https://maps.googleapis.com/maps/api/*', () => {
// ...
```

### Stripe Test Mode

```typescript
test('processes payment with Stripe test card', async ({ page }) => {
  await page.goto('/checkout');

  // Use Stripe test card numbers
  const stripeFrame = page.frameLocator('iframe[name^="__privateStripeFrame"]');
  await stripeFrame.getByPlaceholder('Card number').fill('4242424242424242');
  await stripeFrame.getByPlaceholder('MM / YY').fill('12/30');
  await stripeFrame.getByPlaceholder('CVC').fill('123');

  await page.getByTestId('pay-button').click();

  // Stripe test mode processes immediately
  await expect(page.getByTestId('payment-success')).toBeVisible({ timeout: 10000 });
});
```

---

## Local-Only E2E Workflow (No Docker/CI)

For quick setup without Docker Compose or CI infrastructure:

### Minimal Setup

```bash
# 1. Install Playwright
npm init playwright@latest

# 2. Install browsers
npx playwright install chromium

# 3. Create minimal config
# playwright.config.ts is created by init
```

### Local Dev Server Configuration

```typescript
// playwright.config.ts (minimal local setup)
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  retries: 0,
  workers: undefined, // Use all CPUs
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
// ...
```

### SQLite for Local Testing

```typescript
// e2e/global-setup.ts (SQLite - no external DB needed)
import Database from 'better-sqlite3';

async function globalSetup() {
  const db = new Database('test.db');

  // Reset schema
  db.exec(`DROP TABLE IF EXISTS users`);
  db.exec(`CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE,
    name TEXT,
    password_hash TEXT
  )`);

// ...
```

### Run Commands

```bash
# Run all tests
npx playwright test

# Run with UI mode (visual debugging)
npx playwright test --ui

# Run specific test file
npx playwright test e2e/tests/auth/login.spec.ts

# Run headed (see browser)
npx playwright test --headed

# Debug single test
npx playwright test --debug -g "login"
```

### Local vs Docker vs CI Decision

| Factor | Local Only | Docker Compose | Full CI |
|--------|-----------|----------------|---------|
| **Setup time** | 1 min | 5-10 min | 30+ min |
| **DB needed** | SQLite / dev DB | PostgreSQL container | PostgreSQL |
| **External services** | Mock with MSW | Real in containers | Real or mocked |
| **Reliability** | Developer-dependent | Consistent | Consistent |
| **Use when** | Prototyping, learning | Team development | Production pipeline |
