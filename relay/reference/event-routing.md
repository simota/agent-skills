# Event Routing Patterns

## Event Schema (Discriminated Union)

```typescript
// Base event interface
interface BaseEvent {
  id: string;
  timestamp: Date;
  version: number;
  source: PlatformType;
  correlationId?: string;
}

// Discriminated union of all event types
type MessagingEvent =
  | MessageReceivedEvent
  | MessageSentEvent
  | MessageEditedEvent
  | MessageDeletedEvent
  | ReactionAddedEvent
  | ReactionRemovedEvent
  | MemberJoinedEvent
  | MemberLeftEvent
  | ChannelCreatedEvent
  | CommandReceivedEvent
  | InteractionEvent
  | WebhookDeliveryEvent
  | ConnectionEvent;

interface MessageReceivedEvent extends BaseEvent {
  type: 'message.received';
  payload: {
    message: UnifiedMessage;
    channelId: string;
    userId: string;
  };
}

interface MessageSentEvent extends BaseEvent {
  type: 'message.sent';
  payload: {
    message: UnifiedMessage;
    channelId: string;
    deliveryStatus: 'sent' | 'delivered' | 'read' | 'failed';
  };
}

interface CommandReceivedEvent extends BaseEvent {
  type: 'command.received';
  payload: {
    command: string;
    args: Record<string, unknown>;
    userId: string;
    channelId: string;
  };
}

interface InteractionEvent extends BaseEvent {
  type: 'interaction.received';
  payload: {
    interactionType: 'button' | 'select' | 'modal' | 'shortcut';
    callbackId: string;
    userId: string;
    data: Record<string, unknown>;
  };
}

interface ConnectionEvent extends BaseEvent {
  type: 'connection.opened' | 'connection.closed' | 'connection.error';
  payload: {
    connectionId: string;
    userId?: string;
    reason?: string;
  };
}
```

## Event Router

```typescript
type EventHandler<T extends MessagingEvent = MessagingEvent> = (
  event: T,
) => Promise<void>;

class EventRouter {
  private handlers = new Map<string, EventHandler[]>();
  private wildcardHandlers: EventHandler[] = [];

  on<T extends MessagingEvent>(
    eventType: T['type'],
    handler: EventHandler<T>,
  ): void {
    const handlers = this.handlers.get(eventType) ?? [];
    handlers.push(handler as EventHandler);
    this.handlers.set(eventType, handlers);
  }

  onAny(handler: EventHandler): void {
    this.wildcardHandlers.push(handler);
  }

  async emit(event: MessagingEvent): Promise<void> {
    // Wildcard handlers first (logging, metrics)
    for (const handler of this.wildcardHandlers) {
      await handler(event);
    }

    // Specific handlers
    const handlers = this.handlers.get(event.type) ?? [];
    await Promise.allSettled(
      handlers.map(handler => handler(event)),
    );
  }
}
```

## Routing Matrix

| Event Type | Primary Handler | Side Effects | DLQ on Failure |
|-----------|----------------|--------------|----------------|
| `message.received` | MessageProcessor | Analytics, Logging | Yes |
| `message.sent` | DeliveryTracker | Analytics | No |
| `command.received` | CommandDispatcher | Logging, Audit | Yes |
| `interaction.received` | InteractionHandler | Analytics | Yes |
| `connection.opened` | PresenceManager | Analytics | No |
| `connection.closed` | PresenceManager | Cleanup | No |
| `member.joined` | WelcomeHandler | Analytics, Notification | No |

## Fan-out / Fan-in Patterns

### Fan-out (One event → Multiple handlers)

```typescript
class FanOutProcessor {
  async process(event: MessagingEvent): Promise<void> {
    const handlers = this.getHandlersForEvent(event.type);

    // Fire-and-forget for non-critical
    const nonCritical = handlers.filter(h => !h.critical);
    Promise.allSettled(nonCritical.map(h => h.handle(event)));

    // Await critical handlers
    const critical = handlers.filter(h => h.critical);
    await Promise.all(critical.map(h => h.handle(event)));
  }
}
```

### Fan-in (Multiple events → One aggregation)

```typescript
class EventAggregator {
  private buffer = new Map<string, MessagingEvent[]>();
  private flushInterval: NodeJS.Timeout;

  constructor(private flushMs = 5000) {
    this.flushInterval = setInterval(() => this.flush(), flushMs);
  }

  add(correlationId: string, event: MessagingEvent): void {
    const events = this.buffer.get(correlationId) ?? [];
    events.push(event);
    this.buffer.set(correlationId, events);
  }

  private flush(): void {
    for (const [correlationId, events] of this.buffer) {
      if (this.isComplete(events)) {
        this.emit('aggregation.complete', { correlationId, events });
        this.buffer.delete(correlationId);
      }
    }
  }

  private isComplete(events: MessagingEvent[]): boolean {
    // Check if all expected events have arrived
    return events.length >= 2; // Example threshold
  }
}
```

## Event Versioning

```typescript
// Version migration pattern
interface EventMigration<TOld, TNew> {
  fromVersion: number;
  toVersion: number;
  migrate(old: TOld): TNew;
}

class EventVersionManager {
  private migrations: EventMigration<unknown, unknown>[] = [];

  register(migration: EventMigration<unknown, unknown>): void {
    this.migrations.push(migration);
    this.migrations.sort((a, b) => a.fromVersion - b.fromVersion);
  }

  upgrade(event: BaseEvent, targetVersion: number): BaseEvent {
    let current = event;

    for (const migration of this.migrations) {
      if (current.version >= targetVersion) break;
      if (current.version === migration.fromVersion) {
        current = migration.migrate(current) as BaseEvent;
      }
    }

    return current;
  }
}
```

## Error Handling in Event Processing

```typescript
class ResilientEventProcessor {
  async process(event: MessagingEvent): Promise<void> {
    try {
      await this.router.emit(event);
    } catch (error) {
      // Classify error
      if (this.isTransient(error)) {
        await this.retryQueue.enqueue(event);
      } else {
        await this.dlq.push({
          id: event.id,
          originalEvent: event,
          error: (error as Error).message,
          attempts: 1,
          firstFailedAt: new Date(),
          lastFailedAt: new Date(),
          metadata: {
            platform: event.source,
            eventType: event.type,
            webhookId: event.id,
          },
        });
      }
    }
  }

  private isTransient(error: unknown): boolean {
    if (error instanceof Error) {
      return ['ECONNREFUSED', 'ETIMEDOUT', 'ENOTFOUND'].some(
        code => error.message.includes(code),
      );
    }
    return false;
  }
}
```
