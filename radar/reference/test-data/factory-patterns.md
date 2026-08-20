# Factory Patterns

**Purpose:** Detailed factory pattern implementations across languages and frameworks.
**Read when:** Designing factory structures for a specific tech stack.

> **2026 toolchain.** Factory-style fixtures remain the right tool for deterministic, schema-shaped data. The 2026 additions live next to (not inside) the factories: pair Fishery / Polyfactory / gofakeit with **MSW 2 (Mock Service Worker)** + **`@mswjs/data`** for browser-side mocking and **`msw-auto-mock` v0.19+** for AI-generated mocks from OpenAPI specs (supports OpenAI / Anthropic / Azure providers). For AI agents that drive the browser at test time, the **`msw-mcp`** MCP server lets the agent install / swap MSW handlers dynamically. The factory still owns the data shape; MSW owns the network surface.

---

## Pattern Catalog

### 1. Basic Factory

Simplest pattern — one factory per entity, no relationships.

```typescript
// TypeScript (Fishery)
import { Factory } from 'fishery';
import { faker } from '@faker-js/faker';

const userFactory = Factory.define<User>(({ sequence }) => ({
  id: sequence,
  name: faker.person.fullName(),
  email: faker.internet.email(),
  role: 'user',
  createdAt: faker.date.past(),
  updatedAt: faker.date.recent(),
}));

// Usage
const user = userFactory.build();
const users = userFactory.buildList(5);
```

```python
# Python (Polyfactory)
from polyfactory.factories.pydantic_factory import ModelFactory
from app.models import User

class UserFactory(ModelFactory):
    __model__ = User
    __faker__ = Faker('ja_JP')

    @classmethod
    def name(cls) -> str:
        return cls.__faker__.name()
```

```go
// Go (gofakeit + custom builder)
func NewUser(opts ...func(*User)) *User {
    u := &User{
        ID:    gofakeit.UUID(),
        Name:  gofakeit.Name(),
        Email: gofakeit.Email(),
    }
    for _, opt := range opts {
        opt(u)
    }
    return u
}
```

```ruby
# Ruby (factory_bot)
FactoryBot.define do
  factory :user do
    sequence(:id)
    name { Faker::Name.name }
    email { Faker::Internet.email }
    role { 'user' }
    created_at { Time.current }
  end
end
```

---

### 2. Relational Factory (FK-Aware)

Handles parent-child relationships with automatic dependency resolution.

```typescript
// TypeScript — Parent auto-creation
const orderFactory = Factory.define<Order>(({ sequence, associations }) => ({
  id: sequence,
  user: associations.user || userFactory.build(),
  userId: associations.user?.id ?? userFactory.build().id,
  items: [],
  total: 0,
  status: 'pending',
  createdAt: new Date(),
}));

const orderItemFactory = Factory.define<OrderItem>(({ sequence, associations }) => ({
  id: sequence,
  orderId: associations.order?.id ?? orderFactory.build().id,
  productId: associations.product?.id ?? productFactory.build().id,
  quantity: faker.number.int({ min: 1, max: 10 }),
  unitPrice: faker.number.float({ min: 100, max: 99999, fractionDigits: 0 }),
}));

// Build with consistent parent
const user = userFactory.build();
const order = orderFactory.build({ associations: { user } });
const items = orderItemFactory.buildList(3, { associations: { order } });
```

### Dependency Resolution Order

```
1. Independent entities first (User, Product, Category)
2. One-level dependents (Order → User, Review → Product)
3. Join/bridge tables last (OrderItem → Order + Product)
```

---

### 3. Trait/Variant Pattern

Create named variations for common test scenarios.

```typescript
// Fishery with transient params as traits
const userFactory = Factory.define<User>(({ sequence, transientParams }) => {
  const isAdmin = transientParams.admin ?? false;
  const isDeleted = transientParams.deleted ?? false;
  const isUnverified = transientParams.unverified ?? false;

  return {
    id: sequence,
    name: faker.person.fullName(),
    email: faker.internet.email(),
    role: isAdmin ? 'admin' : 'user',
    emailVerifiedAt: isUnverified ? null : faker.date.past(),
    deletedAt: isDeleted ? faker.date.past() : null,
  };
});

// Named builders
const adminUser = () => userFactory.build({ transientParams: { admin: true } });
const deletedUser = () => userFactory.build({ transientParams: { deleted: true } });
const unverifiedUser = () => userFactory.build({ transientParams: { unverified: true } });
```

```ruby
# factory_bot traits
factory :user do
  name { Faker::Name.name }

  trait :admin do
    role { 'admin' }
  end

  trait :deleted do
    deleted_at { 1.day.ago }
  end

  trait :unverified do
    email_verified_at { nil }
  end
end

# Usage: create(:user, :admin, :deleted)
```

---

### 4. Sequence Pattern

Unique values via auto-incrementing sequences.

```typescript
const userFactory = Factory.define<User>(({ sequence }) => ({
  id: sequence,
  email: `user-${sequence}@test.example.com`,
  username: `testuser${sequence}`,
}));
```

---

### 5. Builder / Fluent Pattern

Chainable API for complex data construction.

```typescript
class UserBuilder {
  private data: Partial<User> = {};

  withRole(role: string) { this.data.role = role; return this; }
  withOrders(count: number) {
    this.data.orders = orderFactory.buildList(count);
    return this;
  }
  deleted() { this.data.deletedAt = new Date(); return this; }
  build(): User { return userFactory.build(this.data); }
}

// Usage
const user = new UserBuilder().withRole('admin').withOrders(3).build();
```

---

## Library Selection Guide

| Language | Library | Strength | Best For |
|----------|---------|----------|----------|
| TS/JS | Fishery | Type-safe, lightweight | TypeScript projects |
| TS/JS | @faker-js/faker | Rich data generation | Any JS/TS project |
| Python | Polyfactory | Pydantic integration | FastAPI/Pydantic projects |
| Python | factory_boy | Django integration | Django projects |
| Ruby | factory_bot | Mature, trait system | Rails projects |
| Go | gofakeit | Fast, built-in | Go projects |
| Rust | fake-rs | Derive macro | Rust projects |
| Java | Instancio | Reflection-based | Java/Spring projects |

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| God Factory | One factory builds everything | Split per entity |
| Hidden Defaults | Default values mask test intent | Use explicit traits |
| DB-Coupled Factory | Factory calls DB directly | Separate build from persist |
| Brittle Sequences | Tests depend on specific IDs | Use relative assertions |
| Fixture Files | JSON/YAML fixtures drift from schema | Use code-based factories |
