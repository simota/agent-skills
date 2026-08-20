# Real-time Architecture

## Transport Selection

| Transport | Use Case | Latency | Scaling | Browser Support |
|-----------|----------|---------|---------|-----------------|
| WebSocket | Bidirectional real-time | < 50ms | Complex (sticky sessions) | ✅ |
| SSE | Server → Client push | < 100ms | Simple (stateless) | ✅ (no IE) |
| Long Polling | Fallback | 100-500ms | Simple | ✅ |
| WebTransport | Next-gen bidirectional, datagrams + streams over HTTP/3 | < 50ms | Complex | Chrome / Edge / Firefox stable in 2026 |
| Streamable HTTP (MCP, 2026) | Agent ↔ server with `POST` for requests + `SSE` for responses on the same endpoint | < 100ms | Simple | Server-driven; native HTTP, no special browser API |

### Decision Tree

```
Is this an MCP / AI-agent transport?
├── Yes → Streamable HTTP (MCP 2026 standard)
│         POST for requests, SSE for streaming responses on the same endpoint
└── No
    │
    Need bidirectional communication?
    ├── Yes
    │   ├── High message volume? (>100 msg/sec)
    │   │   ├── Yes → WebSocket + message queue
    │   │   └── No → WebSocket (standalone)
    │   └── Need UDP-like unreliable delivery?
    │       └── Yes → WebTransport (HTTP/3 datagrams + streams)
    └── No (server push only)
        ├── Token-stream LLM output, dashboard, progress, notifications?
        │   └── SSE (Server-Sent Events) — default
        └── Legacy browser support required?
            └── Yes → Long Polling
```

### 2026 LLM / Agent Surface Cheatsheet

| Workload | Transport |
|----------|-----------|
| Plain LLM token streaming (OpenAI / Anthropic / Vercel AI SDK / LangChain delta stream) | SSE |
| Agent with tool-use approval, mid-stream interrupts, multi-turn dialog, multi-agent coordination | WebSocket |
| MCP server | Streamable HTTP (legacy SSE-only MCP servers still work; migrate at next major version) |

Rule: if the user can interrupt, approve, or hand off during the stream, plan for WebSocket from the start — retrofitting bidirectional control onto an SSE pipeline is a rewrite.

## WebSocket Server Design

### Connection Lifecycle

```typescript
interface WebSocketServer {
  // Connection management
  onConnect(handler: (conn: Connection) => void): void;
  onDisconnect(handler: (conn: Connection, reason: string) => void): void;

  // Messaging
  onMessage(handler: (conn: Connection, data: unknown) => void): void;
  send(connId: string, data: unknown): void;
  broadcast(roomId: string, data: unknown, exclude?: string[]): void;

  // Room management
  join(connId: string, roomId: string): void;
  leave(connId: string, roomId: string): void;

  // Health
  getConnectionCount(): number;
  getRoomMembers(roomId: string): string[];
}
```

### Heartbeat / Reconnection

```typescript
// Server-side heartbeat
const HEARTBEAT_INTERVAL = 30_000; // 30 seconds
const HEARTBEAT_TIMEOUT = 10_000;  // 10 seconds to respond

function setupHeartbeat(ws: WebSocket): NodeJS.Timeout {
  let isAlive = true;

  ws.on('pong', () => { isAlive = true; });

  return setInterval(() => {
    if (!isAlive) {
      ws.terminate();
      return;
    }
    isAlive = false;
    ws.ping();
  }, HEARTBEAT_INTERVAL);
}

// Client-side reconnection with exponential backoff
class ReconnectingWebSocket {
  private retryCount = 0;
  private maxRetries = 10;
  private baseDelay = 1000;

  connect(): void {
    const ws = new WebSocket(this.url);

    ws.onopen = () => {
      this.retryCount = 0; // Reset on successful connection
    };

    ws.onclose = (event) => {
      if (event.code !== 1000 && this.retryCount < this.maxRetries) {
        const delay = Math.min(
          this.baseDelay * Math.pow(2, this.retryCount),
          30_000,
        );
        setTimeout(() => this.connect(), delay);
        this.retryCount++;
      }
    };
  }
}
```

### Room Management Pattern

```typescript
interface Room {
  id: string;
  members: Set<string>;
  metadata: Record<string, unknown>;
  createdAt: Date;
}

class RoomManager {
  private rooms = new Map<string, Room>();

  createRoom(id: string, metadata?: Record<string, unknown>): Room {
    const room: Room = {
      id,
      members: new Set(),
      metadata: metadata ?? {},
      createdAt: new Date(),
    };
    this.rooms.set(id, room);
    return room;
  }

  join(roomId: string, connId: string): void {
    const room = this.rooms.get(roomId);
    if (!room) throw new Error(`Room ${roomId} not found`);
    room.members.add(connId);
  }

  leave(roomId: string, connId: string): void {
    const room = this.rooms.get(roomId);
    if (room) {
      room.members.delete(connId);
      if (room.members.size === 0) {
        this.rooms.delete(roomId); // Auto-cleanup empty rooms
      }
    }
  }

  broadcast(roomId: string, data: unknown, exclude?: string[]): string[] {
    const room = this.rooms.get(roomId);
    if (!room) return [];

    const excludeSet = new Set(exclude ?? []);
    return [...room.members].filter(id => !excludeSet.has(id));
  }
}
```

## Horizontal Scaling

### Redis Pub/Sub for Multi-Server

```typescript
import { Redis } from 'ioredis';

class ScalableWebSocketServer {
  private pub: Redis;
  private sub: Redis;

  constructor(redisUrl: string) {
    this.pub = new Redis(redisUrl);
    this.sub = new Redis(redisUrl);
  }

  async initialize(): Promise<void> {
    // Subscribe to broadcast channel
    await this.sub.subscribe('ws:broadcast');

    this.sub.on('message', (channel, message) => {
      const { roomId, data, excludeConnId } = JSON.parse(message);
      this.localBroadcast(roomId, data, excludeConnId);
    });
  }

  // Broadcast across all servers
  async broadcast(roomId: string, data: unknown, excludeConnId?: string): Promise<void> {
    await this.pub.publish('ws:broadcast', JSON.stringify({
      roomId,
      data,
      excludeConnId,
    }));
  }

  private localBroadcast(roomId: string, data: unknown, excludeConnId?: string): void {
    // Send to local connections only
  }
}
```

### Scaling Strategies

| Strategy | Pros | Cons | When to Use |
|----------|------|------|-------------|
| Sticky Sessions (IP hash) | Simple, no shared state | Uneven load, failover issues | < 10K connections |
| Redis Pub/Sub | Simple, proven | Single Redis = SPOF | 10K-100K connections |
| Redis Cluster | HA, scalable | Complex setup | 100K+ connections |
| NATS/RabbitMQ | Robust, features | Additional infra | Enterprise, complex routing |
| Dedicated (Socket.io Adapter) | Turnkey | Vendor lock-in | Rapid development |

## SSE (Server-Sent Events)

```typescript
// Express SSE endpoint
function sseEndpoint(req: Request, res: Response): void {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no', // Disable Nginx buffering
  });

  // Send initial connection event
  res.write(`event: connected\ndata: ${JSON.stringify({ id: connectionId })}\n\n`);

  // Heartbeat to keep connection alive
  const heartbeat = setInterval(() => {
    res.write(': heartbeat\n\n');
  }, 15_000);

  // Cleanup on disconnect
  req.on('close', () => {
    clearInterval(heartbeat);
    removeConnection(connectionId);
  });
}
```

## Library Comparison

| Library | Protocol | Features | Bundle Size | Use Case |
|---------|----------|----------|-------------|----------|
| `ws` | WebSocket | Minimal, fast | 30KB | Production servers |
| `socket.io` | WS + polling | Rooms, namespaces, fallback | 60KB | Full-featured apps |
| `uWebSockets.js` | WebSocket | Extreme perf, C++ | - | High-throughput |
| `@fastify/websocket` | WebSocket | Fastify integration | - | Fastify apps |
| `sse-channel` | SSE | Simple SSE server | 10KB | Server push only |
| `better-sse` | SSE | TypeScript, channels | 15KB | Modern SSE apps |
