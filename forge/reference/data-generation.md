# Forge Prototype Data Generation

> Purpose: generate realistic, repeatable sample data for demos and interaction testing.

## Contents

- Faker patterns
- Type-safe factories
- Common entity fixtures

Mock data factories and fixtures for rapid prototyping.

---

## Faker.js Patterns

```typescript
// utils/mockDataFactory.ts
import { faker } from '@faker-js/faker';

// User factory
export function createMockUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    avatar: faker.image.avatar(),
    role: faker.helpers.arrayElement(['admin', 'user', 'moderator']),
    createdAt: faker.date.past().toISOString(),
    ...overrides,
  };
}

export function createMockUsers(count: number): User[] {
  return Array.from({ length: count }, () => createMockUser());
}

// Product factory
export function createMockProduct(overrides: Partial<Product> = {}): Product {
  return {
    id: faker.string.uuid(),
    name: faker.commerce.productName(),
    description: faker.commerce.productDescription(),
    price: parseFloat(faker.commerce.price({ min: 10, max: 500 })),
    image: faker.image.urlLoremFlickr({ category: 'product' }),
    category: faker.commerce.department(),
    inStock: faker.datatype.boolean(),
    rating: faker.number.float({ min: 1, max: 5, fractionDigits: 1 }),
    ...overrides,
  };
}

// Order factory with relations
export function createMockOrder(overrides: Partial<Order> = {}): Order {
  const items = Array.from(
    { length: faker.number.int({ min: 1, max: 5 }) },
    () => ({
      product: createMockProduct(),
      quantity: faker.number.int({ min: 1, max: 10 }),
    })
  );

  return {
    id: faker.string.uuid(),
    user: createMockUser(),
    items,
    total: items.reduce((sum, item) => sum + item.product.price * item.quantity, 0),
    status: faker.helpers.arrayElement(['pending', 'processing', 'shipped', 'delivered']),
    createdAt: faker.date.recent().toISOString(),
    ...overrides,
  };
}

// Seeded data for consistent testing
export function createSeededData(seed: number) {
  faker.seed(seed);
  return {
    users: createMockUsers(10),
    products: Array.from({ length: 20 }, () => createMockProduct()),
    orders: Array.from({ length: 5 }, () => createMockOrder()),
  };
}
```

---

## Type-Safe Mock Factory

```typescript
// utils/factory.ts

type Factory<T> = {
  build: (overrides?: Partial<T>) => T;
  buildList: (count: number, overrides?: Partial<T>) => T[];
};

export function createFactory<T>(defaults: () => T): Factory<T> {
  return {
    build: (overrides = {}) => ({
      ...defaults(),
      ...overrides,
    }),
    buildList: (count, overrides = {}) =>
      Array.from({ length: count }, () => ({
        ...defaults(),
        ...overrides,
      })),
  };
}

// Usage
const userFactory = createFactory<User>(() => ({
  id: String(Math.random()),
  name: 'Test User',
  email: 'test@example.com',
  role: 'user',
}));

const testUser = userFactory.build({ name: 'Custom Name' });
const testUsers = userFactory.buildList(5, { role: 'admin' });
```

---

## Common Entity Samples

```typescript
// mocks/fixtures.ts

export const MOCK_USERS: User[] = [
  {
    id: '1',
    name: 'Alice Johnson',
    email: 'alice@example.com',
    avatar: 'https://i.pravatar.cc/150?u=alice',
    role: 'admin',
  },
  {
    id: '2',
    name: 'Bob Smith',
    email: 'bob@example.com',
    avatar: 'https://i.pravatar.cc/150?u=bob',
    role: 'user',
  },
  {
    id: '3',
    name: 'Carol Williams',
    email: 'carol@example.com',
    avatar: 'https://i.pravatar.cc/150?u=carol',
    role: 'moderator',
  },
];

export const MOCK_PRODUCTS: Product[] = [
  {
    id: 'prod-1',
    name: 'Wireless Headphones',
    price: 99.99,
    image: 'https://via.placeholder.com/300x200?text=Headphones',
    category: 'Electronics',
    description: 'High-quality wireless headphones with noise cancellation.',
    inStock: true,
  },
  {
    id: 'prod-2',
    name: 'Smart Watch',
    price: 199.99,
    image: 'https://via.placeholder.com/300x200?text=Watch',
    category: 'Electronics',
    description: 'Feature-rich smart watch with health tracking.',
    inStock: true,
  },
  {
    id: 'prod-3',
    name: 'Laptop Stand',
    price: 49.99,
    image: 'https://via.placeholder.com/300x200?text=Stand',
    category: 'Accessories',
    description: 'Ergonomic laptop stand for better posture.',
    inStock: false,
  },
];

export const MOCK_ORDERS: Order[] = [
  {
    id: 'order-1',
    userId: '1',
    items: [
      { productId: 'prod-1', quantity: 1, price: 99.99 },
      { productId: 'prod-3', quantity: 2, price: 49.99 },
    ],
    total: 199.97,
    status: 'delivered',
    createdAt: '2024-01-15T10:30:00Z',
  },
  {
    id: 'order-2',
    userId: '2',
    items: [
      { productId: 'prod-2', quantity: 1, price: 199.99 },
    ],
    total: 199.99,
    status: 'processing',
    createdAt: '2024-01-20T14:45:00Z',
  },
];
```
