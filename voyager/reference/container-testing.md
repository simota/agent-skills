# Container-Based Testing

Purpose: Use this file when Voyager must set up or maintain container-based E2E test environments using Testcontainers, Docker Compose, or cloud container services.

Contents:
- Testcontainers for Node.js basic setup
- Playwright integration with containers
- Testcontainers Cloud for CI
- Docker Compose vs Testcontainers decision guide
- Dynamic port mapping and auto-cleanup patterns

---

## Testcontainers for Node.js

### Basic Setup

```bash
npm install --save-dev testcontainers
```

```typescript
// e2e/setup/containers.ts
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { GenericContainer, StartedTestContainer } from 'testcontainers';

let postgres: StartedPostgreSqlContainer;
let redis: StartedTestContainer;

export async function startContainers() {
  // Start PostgreSQL with dynamic port mapping
  postgres = await new PostgreSqlContainer('postgres:16-alpine')
    .withDatabase('testdb')
    .withUsername('testuser')
    .withPassword('testpass')
    .start();

  // Start Redis
  redis = await new GenericContainer('redis:7-alpine')
    .withExposedPorts(6379)
    .start();

  return {
    postgresUrl: postgres.getConnectionUri(),
    redisPort: redis.getMappedPort(6379),
    redisHost: redis.getHost(),
  };
}

export async function stopContainers() {
  await postgres?.stop();
  await redis?.stop();
}
```

### Integration with Playwright Global Setup

```typescript
// e2e/global-setup.ts
import { FullConfig } from '@playwright/test';
import { startContainers } from './setup/containers';

export default async function globalSetup(config: FullConfig) {
  const { postgresUrl, redisPort, redisHost } = await startContainers();

  // Pass to tests via environment variables
  process.env.DATABASE_URL = postgresUrl;
  process.env.REDIS_URL = `redis://${redisHost}:${redisPort}`;

  // Store handles for teardown
  (globalThis as any).__CONTAINERS__ = { postgresUrl, redisPort };
}
```

```typescript
// e2e/global-teardown.ts
import { stopContainers } from './setup/containers';

export default async function globalTeardown() {
  await stopContainers();
}
```

```typescript
// playwright.config.ts
export default defineConfig({
  globalSetup: './e2e/global-setup.ts',
  globalTeardown: './e2e/global-teardown.ts',
  // ...
});
```

---

## testcontainers-node-playwright

For spinning up the application under test itself inside a container:

```bash
npm install --save-dev @testcontainers/playwright
```

```typescript
// e2e/setup/app-container.ts
import { GenericContainer, Wait } from 'testcontainers';
import path from 'path';

export async function startAppContainer() {
  const container = await new GenericContainer('node:20-alpine')
    .withBindMounts([
      {
        source: path.resolve(__dirname, '../..'),
        target: '/app',
        mode: 'ro',
      },
    ])
    .withWorkingDir('/app')
    .withCommand(['npm', 'run', 'start:test'])
    .withExposedPorts(3000)
    .withWaitStrategy(Wait.forHttp('/health', 3000))
    .start();

  return {
    baseURL: `http://${container.getHost()}:${container.getMappedPort(3000)}`,
    container,
  };
}
```

### Trace Extraction from Container

```typescript
// Extract Playwright traces from a container run
import { execSync } from 'child_process';

export function extractTraces(containerId: string, outputDir: string) {
  execSync(
    `docker cp ${containerId}:/app/test-results/. ${outputDir}`,
    { stdio: 'inherit' }
  );
}
```

---

## Testcontainers Cloud

For CI environments where Docker-in-Docker (DinD) is unavailable or unreliable:

```bash
# Install Testcontainers Cloud agent
npm install --save-dev @testcontainers/cloud
```

```yaml
# .github/workflows/e2e.yml
- name: Setup Testcontainers Cloud
  uses: atomicjar/testcontainers-cloud-setup-action@v1
  with:
    token: ${{ secrets.TC_CLOUD_TOKEN }}

- name: Run E2E tests
  run: npx playwright test
  env:
    TESTCONTAINERS_HOST_OVERRIDE: tc.testcontainers.cloud
```

Benefits:
- No DinD required — containers run on Testcontainers Cloud infrastructure
- Native GitHub Actions integration
- Consistent container behavior across local and CI

---

## Docker Compose vs Testcontainers Decision Guide

| Factor | Docker Compose | Testcontainers |
|--------|---------------|----------------|
| **Approach** | YAML declarative | Code-first (TypeScript) |
| **Dynamic config** | Limited (env substitution) | Full programmatic control |
| **Port mapping** | Fixed or semi-fixed | Fully dynamic (no conflicts) |
| **Cleanup** | Manual (`docker compose down`) | Automatic (Ryuk daemon) |
| **Parallelism** | Requires manual project naming | Isolated per test run by default |
| **CI complexity** | Requires DinD or service containers | Works with Testcontainers Cloud |
| **Best for** | Multi-service infra teams, shared environments | Code-centric teams, parallel E2E runs |

**Decision rule:**
- Use **Docker Compose** when the environment is owned by infra/DevOps and shared across multiple tools.
- Use **Testcontainers** when E2E tests own their environment, parallelism matters, or DinD is unavailable.

---

## Dynamic Port Mapping and Auto-Cleanup

### Dynamic Port Assignment

```typescript
// Never hard-code ports — always use getMappedPort()
const container = await new GenericContainer('redis:7')
  .withExposedPorts(6379)
  .start();

// Get the host-side dynamic port
const redisPort = container.getMappedPort(6379);
const redisHost = container.getHost();

// Use in connection string
const client = createClient({ url: `redis://${redisHost}:${redisPort}` });
```

### Auto-Cleanup with Ryuk

Testcontainers starts a `ryuk` sidecar that automatically removes containers when the test process exits — even on crash:

```typescript
// Ryuk is enabled by default. Disable only in special cases:
process.env.TESTCONTAINERS_RYUK_DISABLED = 'true'; // NOT recommended

// Prefer explicit cleanup in afterAll for deterministic teardown
afterAll(async () => {
  await container.stop({ timeout: 10000 });
});
```

### Container Reuse Pattern (for fast local iteration)

```typescript
// Enable reuse to skip container startup on repeated test runs
const container = await new PostgreSqlContainer()
  .withReuse()  // Container persists between runs if config is identical
  .start();
```

> Warning: `.withReuse()` should not be used in CI — containers must be isolated per run.

---

## Common Patterns

### Wait for Service Readiness

```typescript
import { Wait } from 'testcontainers';

// Wait for HTTP endpoint
.withWaitStrategy(Wait.forHttp('/health', 3000).forStatusCode(200))

// Wait for log output
.withWaitStrategy(Wait.forLogMessage('Server started'))

// Wait for port to be open
.withWaitStrategy(Wait.forListeningPorts())
```

### Environment Variables in Container

```typescript
const container = await new GenericContainer('myapp:latest')
  .withEnvironment({
    NODE_ENV: 'test',
    DATABASE_URL: postgres.getConnectionUri(),
    REDIS_URL: `redis://${redis.getHost()}:${redis.getMappedPort(6379)}`,
  })
  .start();
```

Sources: [Testcontainers for Node.js](https://node.testcontainers.org/) · [Testcontainers Cloud Docs](https://testcontainers.com/cloud/) · [testcontainers-node GitHub](https://github.com/testcontainers/testcontainers-node)
