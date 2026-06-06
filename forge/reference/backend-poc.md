# Forge Backend PoC Templates

> Purpose: provide the smallest useful backend scaffolds for prototype-only server behavior.

## Contents

- Express CRUD
- Fastify CRUD
- In-memory storage
- WebSocket example

Minimal server templates for rapid prototyping.

---

## Express Minimal CRUD Server

```typescript
// server/index.ts
import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

// In-memory storage
interface Item {
  id: string;
  name: string;
  completed: boolean;
}

let items: Item[] = [
  { id: '1', name: 'Task 1', completed: false },
  { id: '2', name: 'Task 2', completed: true },
];

// GET all
app.get('/api/items', (req, res) => {
  res.json(items);
});

// GET by ID
app.get('/api/items/:id', (req, res) => {
  const item = items.find(i => i.id === req.params.id);
  if (!item) return res.status(404).json({ error: 'Not found' });
  res.json(item);
});

// POST create
app.post('/api/items', (req, res) => {
  const newItem: Item = {
    id: String(Date.now()),
    name: req.body.name,
    completed: false,
  };
  items.push(newItem);
  res.status(201).json(newItem);
});

// PUT update
app.put('/api/items/:id', (req, res) => {
  const index = items.findIndex(i => i.id === req.params.id);
  if (index === -1) return res.status(404).json({ error: 'Not found' });
  items[index] = { ...items[index], ...req.body };
  res.json(items[index]);
});

// DELETE
app.delete('/api/items/:id', (req, res) => {
  const index = items.findIndex(i => i.id === req.params.id);
  if (index === -1) return res.status(404).json({ error: 'Not found' });
  items.splice(index, 1);
  res.status(204).send();
});

const PORT = 3001;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
```

---

## Fastify Minimal Server

```typescript
// server/fastify.ts
import Fastify from 'fastify';
import cors from '@fastify/cors';

const fastify = Fastify({ logger: true });

await fastify.register(cors);

interface Item {
  id: string;
  name: string;
}

let items: Item[] = [];

// Routes
fastify.get('/api/items', async () => items);

fastify.get<{ Params: { id: string } }>('/api/items/:id', async (request, reply) => {
  const item = items.find(i => i.id === request.params.id);
  if (!item) return reply.status(404).send({ error: 'Not found' });
  return item;
});

fastify.post<{ Body: { name: string } }>('/api/items', async (request, reply) => {
  const newItem = { id: String(Date.now()), name: request.body.name };
  items.push(newItem);
  return reply.status(201).send(newItem);
});

fastify.delete<{ Params: { id: string } }>('/api/items/:id', async (request, reply) => {
  items = items.filter(i => i.id !== request.params.id);
  return reply.status(204).send();
});

// Start
try {
  await fastify.listen({ port: 3001 });
} catch (err) {
  fastify.log.error(err);
  process.exit(1);
}
```

---

## In-Memory Storage Pattern

```typescript
// server/storage.ts

export class InMemoryStore<T extends { id: string }> {
  private items: Map<string, T> = new Map();

  getAll(): T[] {
    return Array.from(this.items.values());
  }

  getById(id: string): T | undefined {
    return this.items.get(id);
  }

  create(item: Omit<T, 'id'>): T {
    const newItem = { ...item, id: String(Date.now()) } as T;
    this.items.set(newItem.id, newItem);
    return newItem;
  }

  update(id: string, updates: Partial<T>): T | undefined {
    const item = this.items.get(id);
    if (!item) return undefined;
    const updated = { ...item, ...updates };
    this.items.set(id, updated);
    return updated;
  }

  delete(id: string): boolean {
    return this.items.delete(id);
  }

  seed(items: T[]): void {
    items.forEach(item => this.items.set(item.id, item));
  }

  clear(): void {
    this.items.clear();
  }
}

// Usage
const userStore = new InMemoryStore<User>();
userStore.seed(MOCK_USERS);
```

---

## WebSocket Simple Implementation

```typescript
// server/websocket.ts
import { WebSocketServer, WebSocket } from 'ws';

const wss = new WebSocketServer({ port: 8080 });

const clients = new Set<WebSocket>();

wss.on('connection', (ws) => {
  clients.add(ws);
  console.log('Client connected');

  // Send welcome message
  ws.send(JSON.stringify({ type: 'connected', message: 'Welcome!' }));

  // Handle incoming messages
  ws.on('message', (data) => {
    const message = JSON.parse(data.toString());
    console.log('Received:', message);

    // Broadcast to all clients
    clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({
          type: 'broadcast',
          from: 'server',
          data: message,
        }));
      }
    });
  });

  ws.on('close', () => {
    clients.delete(ws);
    console.log('Client disconnected');
  });
});

console.log('WebSocket server running on ws://localhost:8080');

// Client-side usage
// const ws = new WebSocket('ws://localhost:8080');
// ws.onmessage = (event) => console.log(JSON.parse(event.data));
// ws.send(JSON.stringify({ type: 'chat', text: 'Hello!' }));
```
