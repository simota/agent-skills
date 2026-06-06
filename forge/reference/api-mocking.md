# Forge API Mock Patterns

> Purpose: choose the lightest mock strategy that still supports the prototype’s learning goal.

## Contents

- `MSW` handlers
- Inline mock fetch
- `json-server`
- Error response mocking

Mock strategies for rapid prototyping.

---

## MSW Handlers (Full CRUD)

```typescript
// mocks/handlers.ts
import { http, HttpResponse, delay } from 'msw';

interface User {
  id: string;
  name: string;
  email: string;
}

// In-memory store
let users: User[] = [
  { id: '1', name: 'Alice', email: 'alice@example.com' },
  { id: '2', name: 'Bob', email: 'bob@example.com' },
];

export const handlers = [
  // GET /api/users
  http.get('/api/users', async () => {
    await delay(300);
    return HttpResponse.json(users);
  }),

  // GET /api/users/:id
  http.get('/api/users/:id', async ({ params }) => {
    await delay(200);
    const user = users.find(u => u.id === params.id);
    if (!user) {
      return HttpResponse.json({ error: 'User not found' }, { status: 404 });
    }
    return HttpResponse.json(user);
  }),

  // POST /api/users
  http.post('/api/users', async ({ request }) => {
    await delay(500);
    const body = await request.json() as Omit<User, 'id'>;
    const newUser: User = {
      id: String(Date.now()),
      ...body,
    };
    users.push(newUser);
    return HttpResponse.json(newUser, { status: 201 });
  }),

  // PUT /api/users/:id
  http.put('/api/users/:id', async ({ params, request }) => {
    await delay(300);
    const body = await request.json() as Partial<User>;
    const index = users.findIndex(u => u.id === params.id);
    if (index === -1) {
      return HttpResponse.json({ error: 'User not found' }, { status: 404 });
    }
    users[index] = { ...users[index], ...body };
    return HttpResponse.json(users[index]);
  }),

  // DELETE /api/users/:id
  http.delete('/api/users/:id', async ({ params }) => {
    await delay(200);
    const index = users.findIndex(u => u.id === params.id);
    if (index === -1) {
      return HttpResponse.json({ error: 'User not found' }, { status: 404 });
    }
    users.splice(index, 1);
    return new HttpResponse(null, { status: 204 });
  }),
];

// mocks/browser.ts
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';
export const worker = setupWorker(...handlers);

// main.tsx - Start MSW in development
if (process.env.NODE_ENV === 'development') {
  const { worker } = await import('./mocks/browser');
  await worker.start({ onUnhandledRequest: 'bypass' });
}
```

---

## Inline Mock Fetch

```typescript
// utils/mockFetch.ts

// Simple mock fetch wrapper for prototypes
export function createMockFetch<T>(mockData: T, delay = 500) {
  return async (): Promise<T> => {
    await new Promise(r => setTimeout(r, delay));
    return mockData;
  };
}

// With error simulation
export function createMockFetchWithError<T>(
  mockData: T,
  errorRate = 0.1,
  delay = 500
) {
  return async (): Promise<T> => {
    await new Promise(r => setTimeout(r, delay));
    if (Math.random() < errorRate) {
      throw new Error('Simulated network error');
    }
    return mockData;
  };
}

// Usage in component
const fetchUsers = createMockFetch([
  { id: '1', name: 'Alice' },
  { id: '2', name: 'Bob' },
]);

// Full mock API client
export const mockApi = {
  users: {
    list: createMockFetch(MOCK_USERS),
    get: (id: string) => createMockFetch(MOCK_USERS.find(u => u.id === id))(),
    create: (data: Omit<User, 'id'>) => createMockFetch({ id: String(Date.now()), ...data })(),
    update: (id: string, data: Partial<User>) => createMockFetch({ id, ...data } as User)(),
    delete: (id: string) => createMockFetch(undefined)(),
  },
};
```

---

## json-server Setup

```bash
# Quick setup
npm install -D json-server

# Create db.json
cat > db.json << 'EOF'
{
  "users": [
    { "id": "1", "name": "Alice", "email": "alice@example.com" },
    { "id": "2", "name": "Bob", "email": "bob@example.com" }
  ],
  "products": [
    { "id": "1", "name": "Widget", "price": 29.99 },
    { "id": "2", "name": "Gadget", "price": 49.99 }
  ],
  "orders": []
}
EOF

# Run server
npx json-server --watch db.json --port 3001
```

```json
// package.json script
{
  "scripts": {
    "mock-api": "json-server --watch db.json --port 3001 --delay 500"
  }
}
```

---

## Error Response Mocking

```typescript
// mocks/errorHandlers.ts
import { http, HttpResponse, delay } from 'msw';

export const errorHandlers = [
  // 400 Bad Request
  http.post('/api/validate', async ({ request }) => {
    const body = await request.json();
    if (!body.email) {
      return HttpResponse.json(
        { error: 'Validation failed', details: { email: 'Email is required' } },
        { status: 400 }
      );
    }
    return HttpResponse.json({ valid: true });
  }),

  // 401 Unauthorized
  http.get('/api/protected', async ({ request }) => {
    const token = request.headers.get('Authorization');
    if (!token) {
      return HttpResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }
    return HttpResponse.json({ data: 'secret' });
  }),

  // 403 Forbidden
  http.delete('/api/admin/:id', async () => {
    return HttpResponse.json(
      { error: 'Insufficient permissions' },
      { status: 403 }
    );
  }),

  // 404 Not Found
  http.get('/api/users/:id', async ({ params }) => {
    if (params.id === '999') {
      return HttpResponse.json(
        { error: 'User not found' },
        { status: 404 }
      );
    }
    return HttpResponse.json({ id: params.id, name: 'Test User' });
  }),

  // 500 Server Error
  http.get('/api/unstable', async () => {
    await delay(1000);
    return HttpResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }),

  // Network timeout simulation
  http.get('/api/slow', async () => {
    await delay(30000); // 30 second delay
    return HttpResponse.json({ data: 'finally!' });
  }),
];
```
