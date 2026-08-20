# Seed Data Management

**Purpose:** Idempotent, versioned seed data strategies for test environments.
**Read when:** Designing seed data infrastructure or managing test environment state.

---

## Seed Strategies

### 1. Upsert Pattern (Recommended Default)

Idempotent — safe to run multiple times.

```typescript
// Prisma upsert
async function seedUsers(prisma: PrismaClient) {
  const users = [
    { email: 'admin@test.example.com', name: 'Test Admin', role: 'admin' },
    { email: 'user@test.example.com', name: 'Test User', role: 'user' },
  ];

  for (const data of users) {
    await prisma.user.upsert({
      where: { email: data.email },
      update: data,
      create: data,
    });
  }
}
```

### 2. Truncate-and-Reload Pattern

Fast, deterministic — for isolated test environments.

```typescript
async function resetAndSeed(prisma: PrismaClient) {
  // Truncate in reverse FK order
  await prisma.$executeRaw`TRUNCATE TABLE order_items, orders, users CASCADE`;

  // Seed in FK order
  await seedUsers(prisma);
  await seedOrders(prisma);
  await seedOrderItems(prisma);
}
```

### 3. Snapshot Pattern

Dump known-good state, restore instantly.

```bash
# Create snapshot
pg_dump --data-only --format=custom -f seeds/snapshot_v1.dump testdb

# Restore (fast reset)
pg_restore --clean --if-exists --data-only -d testdb seeds/snapshot_v1.dump
```

### 4. Migration-Integrated Seeds

Seeds bundled with schema migrations.

```
migrations/
├── 001_create_users.sql
├── 001_seed_users.sql          # Runs after migration
├── 002_create_orders.sql
└── 002_seed_orders.sql
```

---

## Versioning Strategies

### Timestamped Files

```
seeds/
├── 20240101_000_base_users.ts
├── 20240101_001_base_products.ts
├── 20240215_000_add_categories.ts
└── 20240301_000_add_test_orders.ts
```

### Environment-Aware Seeds

```
seeds/
├── shared/               # All environments
│   ├── roles.ts
│   └── permissions.ts
├── development/          # Dev only
│   ├── sample_users.ts
│   └── sample_data.ts
├── test/                 # Test only
│   ├── fixtures.ts
│   └── edge_cases.ts
└── staging/              # Staging only
    └── demo_data.ts
```

### Seed Runner

```typescript
interface SeedConfig {
  name: string;
  environment: ('development' | 'test' | 'staging')[];
  dependencies: string[];
  run: (db: Database) => Promise<void>;
}

async function runSeeds(env: string, configs: SeedConfig[]) {
  const applicable = configs.filter(c => c.environment.includes(env));
  const sorted = topologicalSort(applicable); // Respect dependencies

  for (const seed of sorted) {
    const alreadyRun = await db.seedLog.findUnique({ where: { name: seed.name } });
    if (!alreadyRun) {
      await seed.run(db);
      await db.seedLog.create({ data: { name: seed.name, ranAt: new Date() } });
    }
  }
}
```

---

## Deterministic Faker Seeds

```typescript
// Set global seed for reproducibility
import { faker } from '@faker-js/faker';

faker.seed(42); // Same seed = same output every time

// Or per-factory seed
const userFactory = Factory.define<User>(({ sequence }) => {
  faker.seed(1000 + sequence); // Deterministic per record
  return {
    name: faker.person.fullName(),
    email: faker.internet.email(),
  };
});
```

---

## Data Volume Profiles

| Profile | Records | Use Case |
|---------|---------|----------|
| Minimal | 5-10 per entity | Unit tests, fast CI |
| Standard | 50-100 per entity | Integration tests |
| Realistic | 1K-10K per entity | E2E, demo environments |
| Load test | 100K-1M per entity | Performance testing |
| Stress test | 1M+ per entity | Capacity planning |

### Volume Generation

```typescript
async function generateVolume(profile: 'minimal' | 'standard' | 'realistic' | 'load') {
  const counts = {
    minimal: { users: 5, orders: 10, items: 30 },
    standard: { users: 50, orders: 200, items: 600 },
    realistic: { users: 1000, orders: 5000, items: 15000 },
    load: { users: 100000, orders: 500000, items: 1500000 },
  };

  const c = counts[profile];

  // Batch insert for performance
  const batchSize = 1000;
  for (let i = 0; i < c.users; i += batchSize) {
    const batch = userFactory.buildList(Math.min(batchSize, c.users - i));
    await db.user.createMany({ data: batch });
  }
}
```

---

## Best Practices

1. **Idempotency** — Every seed script must be safe to run multiple times
2. **Ordering** — Respect FK dependencies; use topological sort
3. **Isolation** — Test seeds should not interfere with each other
4. **Speed** — Use batch inserts for large volumes; avoid N+1
5. **Cleanup** — Provide teardown/reset alongside seeding
6. **Documentation** — Document what each seed provides and why
