# Domain Modeling: DDD, CQRS & Event Sourcing

Consolidated reference for the Builder agent covering DDD tactical patterns, CQRS, and Event Sourcing.

---

## 1. DDD Tactical Patterns

### Entity

Entities have identity that persists over time.

```typescript
abstract class Entity<T> {
  protected readonly _id: T;
  constructor(id: T) { this._id = id; }
  get id(): T { return this._id; }
  equals(other: Entity<T>): boolean { return this._id === other._id; }
}

class User extends Entity<UserId> {
  private constructor(id: UserId, private _email: Email, private _name: UserName, private _status: UserStatus) {
    super(id);
  }

  static create(props: CreateUserProps): Result<User, ValidationError> {
    const emailResult = Email.create(props.email);
    if (emailResult.isErr()) return err(emailResult.error);
    const nameResult = UserName.create(props.name);
    if (nameResult.isErr()) return err(nameResult.error);
    return ok(new User(UserId.generate(), emailResult.value, nameResult.value, UserStatus.PENDING));
  }

  activate(): Result<void, DomainError> {
    if (this._status !== UserStatus.PENDING)
      return err(new InvalidStateError('User must be pending to activate'));
    this._status = UserStatus.ACTIVE;
    return ok(undefined);
  }
}
```

### Value Object (with branded types + smart constructors)

Value Objects are immutable and compared by value.

```typescript
abstract class ValueObject<T> {
  protected readonly props: T;
  protected constructor(props: T) { this.props = Object.freeze(props); }
  equals(other: ValueObject<T>): boolean {
    return JSON.stringify(this.props) === JSON.stringify(other.props);
  }
}

class Email extends ValueObject<{ value: string }> {
  private static readonly REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  private constructor(value: string) { super({ value }); }
  static create(email: string): Result<Email, ValidationError> {
    const trimmed = email.trim().toLowerCase();
    return this.REGEX.test(trimmed) ? ok(new Email(trimmed)) : err(new ValidationError('Invalid email format'));
  }
  get value(): string { return this.props.value; }
}

class Money extends ValueObject<{ amount: number; currency: Currency }> {
  private constructor(amount: number, currency: Currency) { super({ amount, currency }); }
  static create(amount: number, currency: Currency): Result<Money, ValidationError> {
    return amount < 0 ? err(new ValidationError('Amount cannot be negative')) : ok(new Money(amount, currency));
  }
  add(other: Money): Result<Money, DomainError> {
    if (this.props.currency !== other.props.currency) return err(new CurrencyMismatchError());
    return Money.create(this.props.amount + other.props.amount, this.props.currency);
  }
}
```

### Aggregate Root (with sizing rules)

Aggregates encapsulate entities and enforce invariants. Only the aggregate root can modify children.

**Aggregate Sizing Rules:**
- Fits on a single screen
- Invariant test: only data needed for a single business rule
- Concurrency signal: if two use cases frequently conflict, split
- Heuristic: "No smaller than an aggregate, no larger than a bounded context"

```
❌ God Aggregate: Order handling items, discounts, payments, shipping, returns
✅ Focused Aggregates: Order (items, status), Payment (amount, method), Shipment (tracking)
```

```typescript
class Order extends Entity<OrderId> {
  private _items: OrderItem[] = [];
  private _status: OrderStatus;
  private _customerId: CustomerId;

  addItem(product: Product, quantity: number): Result<void, DomainError> {
    if (this._status !== OrderStatus.DRAFT)
      return err(new InvalidStateError('Cannot modify confirmed order'));
    const existing = this._items.find(i => i.productId.equals(product.id));
    existing ? existing.increaseQuantity(quantity) : this._items.push(OrderItem.create(product, quantity));
    return ok(undefined);
  }

  confirm(): Result<OrderConfirmed, DomainError> {
    if (this._items.length === 0) return err(new EmptyOrderError());
    if (this._status !== OrderStatus.DRAFT) return err(new InvalidStateError('Order already confirmed'));
    this._status = OrderStatus.CONFIRMED;
    return ok(new OrderConfirmed(this._id, this._customerId, this.totalAmount));
  }

  get totalAmount(): Money {
    return this._items.reduce((sum, item) => sum.add(item.subtotal).unwrap(), Money.zero(Currency.USD));
  }
}
```

### Repository

Interface in domain layer; implementation in infrastructure layer.

```typescript
interface UserRepository {
  findById(id: UserId): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  save(user: User): Promise<void>;
}

class PrismaUserRepository implements UserRepository {
  constructor(private readonly prisma: PrismaClient) {}
  async findById(id: UserId): Promise<User | null> {
    const data = await this.prisma.user.findUnique({ where: { id: id.value } });
    return data ? UserMapper.toDomain(data) : null;
  }
  async save(user: User): Promise<void> {
    const data = UserMapper.toPersistence(user);
    await this.prisma.user.upsert({ where: { id: data.id }, create: data, update: data });
  }
}
```

### Domain Service

Use for business logic that doesn't belong to a single entity or aggregate.

```typescript
class TransferService {
  constructor(private readonly accountRepo: AccountRepository, private readonly eventPublisher: DomainEventPublisher) {}

  async transfer(fromId: AccountId, toId: AccountId, amount: Money): Promise<Result<TransferCompleted, DomainError>> {
    const [from, to] = await Promise.all([this.accountRepo.findById(fromId), this.accountRepo.findById(toId)]);
    if (!from || !to) return err(new AccountNotFoundError());

    const debit = from.debit(amount);
    if (debit.isErr()) return err(debit.error);
    const credit = to.credit(amount);
    if (credit.isErr()) { from.credit(amount); return err(credit.error); } // rollback

    await Promise.all([this.accountRepo.save(from), this.accountRepo.save(to)]);
    const event = new TransferCompleted(fromId, toId, amount);
    await this.eventPublisher.publish(event);
    return ok(event);
  }
}
```

---

## 2. Always-Valid Domain Model

- Factory methods returning `Result<T, E>` — never throw from constructors
- No public setters — state changes only through domain methods
- Invariant enforcement at construction time

```typescript
class Order {
  private constructor(private readonly props: OrderProps) {}

  static create(props: CreateOrderProps): Result<Order, DomainError> {
    if (props.items.length === 0)
      return err(new DomainError('Order must have at least one item'));
    return ok(new Order({ ...props, status: 'draft', createdAt: new Date() }));
  }
}
```

---

## 3. CQRS

### Command / Handler Pattern (lightweight, no MediatR)

Prefer direct handler injection over a heavy bus abstraction for simple use cases.

```typescript
// Marker interfaces + direct injection (no MediatR/bus)
interface ICommand<TResult> { readonly _result?: TResult }
interface ICommandHandler<TCmd extends ICommand<TResult>, TResult> {
  handle(command: TCmd): Promise<Result<TResult, DomainError>>
}

// Direct handler injection into endpoints
app.post('/orders', async (req, res) => {
  const result = await createOrderHandler.handle(new CreateOrderCommand(req.body));
  result.match(
    (order) => res.status(201).json(order),
    (error) => res.status(400).json({ error: error.message })
  );
});

// Full handler example
class CreateOrderHandler implements ICommandHandler<CreateOrderCommand, void> {
  constructor(
    private readonly orderRepo: OrderRepository,
    private readonly productRepo: ProductRepository,
    private readonly eventPublisher: EventPublisher
  ) {}

  async handle(cmd: CreateOrderCommand): Promise<Result<void, DomainError>> {
    const products = await Promise.all(cmd.items.map(i => this.productRepo.findById(i.productId)));
    const orderResult = Order.create(new CustomerId(cmd.customerId));
    if (orderResult.isErr()) return orderResult;
    const order = orderResult.value;
    for (let i = 0; i < cmd.items.length; i++) {
      if (!products[i]) return err(new ProductNotFoundError(cmd.items[i].productId));
      const add = order.addItem(products[i], cmd.items[i].quantity);
      if (add.isErr()) return add;
    }
    await this.orderRepo.save(order);
    for (const event of order.getUncommittedEvents()) await this.eventPublisher.publish(event);
    return ok(undefined);
  }
}
```

### Query / Handler Pattern

Queries bypass the domain model and hit read-optimized views directly.

```typescript
class GetOrdersByCustomerHandler {
  constructor(private readonly readDb: ReadDatabase) {}
  async handle(query: GetOrdersByCustomerQuery): Promise<OrderSummary[]> {
    const result = await this.readDb.query<OrderSummary>(
      `SELECT o.id, o.status, o.total_amount, o.item_count, o.created_at
       FROM order_summaries o WHERE o.customer_id = $1
       ORDER BY o.created_at DESC LIMIT $2 OFFSET $3`,
      [query.customerId, query.limit, (query.page - 1) * query.limit]
    );
    return result.rows;
  }
}

// Read model projection — keeps read store in sync with domain events
class OrderSummaryProjection {
  constructor(private readonly readDb: ReadDatabase) {}
  async handle(event: DomainEvent): Promise<void> {
    if (event.eventType === 'OrderPlaced') {
      const e = event as OrderPlaced;
      await this.readDb.query(
        `INSERT INTO order_summaries (id, customer_id, status, total_amount, item_count, created_at)
         VALUES ($1, $2, 'PLACED', $3, $4, $5)`,
        [e.orderId, e.customerId, e.totalAmount, e.items.length, e.occurredAt]
      );
    } else if (event.eventType === 'OrderShipped') {
      const e = event as OrderShipped;
      await this.readDb.query(
        `UPDATE order_summaries SET status = 'SHIPPED', tracking_number = $2 WHERE id = $1`,
        [e.orderId, e.trackingNumber]
      );
    }
  }
}
```

### When to use CQRS vs simple CRUD

Use CQRS when read and write loads differ significantly, multiple read models serve different consumers, or write-side complexity must be isolated. Use simple CRUD when there is a single read model, no complex domain logic, and no scalability pressure.

---

## 4. Event Sourcing

### Domain Events (intent-rich naming, versioned from v1)

Events must capture business intent, not state diffs. Version from v1; include upcaster functions for schema evolution.

```
❌ OrderUpdated { price: 99.99 }
✅ ProductPriceIncreased { newPrice: 99.99, oldPrice: 89.99, reason: 'promotion' }
```

```typescript
abstract class DomainEvent {
  readonly occurredAt: Date = new Date();
  readonly eventId: string = crypto.randomUUID();
  abstract get eventType(): string;
}

class OrderPlaced extends DomainEvent {
  constructor(readonly orderId: OrderId, readonly customerId: CustomerId,
              readonly items: OrderItem[], readonly totalAmount: Money) { super(); }
  get eventType() { return 'OrderPlaced'; }
}
```

### Event Store

```typescript
class PostgresEventStore implements EventStore {
  async append(streamId: string, events: DomainEvent[], expectedVersion?: number): Promise<void> {
    await this.db.transaction(async (tx) => {
      if (expectedVersion !== undefined) {
        const { rows } = await tx.query('SELECT MAX(version) FROM events WHERE stream_id = $1', [streamId]);
        if (rows[0].max !== expectedVersion) throw new ConcurrencyError('Stream has been modified');
      }
      for (let i = 0; i < events.length; i++) {
        const event = events[i];
        await tx.query(
          `INSERT INTO events (stream_id, event_type, data, metadata, version) VALUES ($1, $2, $3, $4, $5)`,
          [streamId, event.eventType, JSON.stringify(event),
           JSON.stringify({ occurredAt: event.occurredAt }), (expectedVersion ?? 0) + i + 1]
        );
      }
    });
  }
}
```

### Event-Sourced Aggregate

```typescript
abstract class EventSourcedAggregate<TId> {
  protected _id: TId;
  protected _version = 0;
  private _uncommittedEvents: DomainEvent[] = [];

  protected apply(event: DomainEvent): void { this.when(event); this._uncommittedEvents.push(event); }
  protected abstract when(event: DomainEvent): void;
  getUncommittedEvents(): DomainEvent[] { return [...this._uncommittedEvents]; }
  clearUncommittedEvents(): void { this._uncommittedEvents = []; }
  loadFromHistory(events: DomainEvent[]): void { events.forEach(e => { this.when(e); this._version++; }); }
}

class Order extends EventSourcedAggregate<OrderId> {
  private _status = OrderStatus.DRAFT;
  private _items: OrderItem[] = [];

  static create(customerId: CustomerId): Order {
    const order = new Order();
    order.apply(new OrderCreated(OrderId.generate(), customerId));
    return order;
  }

  addItem(product: Product, quantity: number): void {
    if (this._status !== OrderStatus.DRAFT) throw new InvalidOperationError('Cannot modify confirmed order');
    this.apply(new OrderItemAdded(this._id, product.id, quantity, product.price));
  }

  protected when(event: DomainEvent): void {
    switch (event.eventType) {
      case 'OrderCreated': this._id = (event as OrderCreated).orderId; this._status = OrderStatus.DRAFT; break;
      case 'OrderItemAdded': const e = event as OrderItemAdded;
        this._items.push(new OrderItem(e.productId, e.quantity, e.price)); break;
    }
  }
}
```

### Saga Pattern

Use sagas for multi-step workflows across aggregates or services. Compensate in reverse order on failure.

```typescript
class OrderFulfillmentSaga {
  private compensationActions: (() => Promise<void>)[] = [];

  async execute(order: Order): Promise<Result<void, SagaError>> {
    try {
      const reserve = await this.inventoryService.reserve(order.items);
      if (reserve.isErr()) return err(new SagaError('INVENTORY_FAILED', reserve.error));
      this.compensationActions.push(() => this.inventoryService.release(order.items));

      const payment = await this.paymentService.charge(order.customerId, order.totalAmount);
      if (payment.isErr()) { await this.compensate(); return err(new SagaError('PAYMENT_FAILED', payment.error)); }
      this.compensationActions.push(() => this.paymentService.refund(payment.value.transactionId));

      const shipment = await this.shippingService.createShipment(order);
      if (shipment.isErr()) { await this.compensate(); return err(new SagaError('SHIPPING_FAILED', shipment.error)); }

      await this.eventPublisher.publish(new OrderFulfilled(order.id));
      return ok(undefined);
    } catch (error) { await this.compensate(); return err(new SagaError('UNEXPECTED_ERROR', error)); }
  }

  private async compensate(): Promise<void> {
    for (const action of this.compensationActions.reverse()) {
      try { await action(); } catch (e) { console.error('Compensation failed:', e); }
    }
  }
}
```

### Transactional Outbox Pattern

Mandatory for reliable event publishing:
1. Write business data + outbox row in the **same** DB transaction
2. Separate relay process reads committed outbox rows and publishes to broker
3. Consumers must be idempotent (at-least-once delivery guarantee)

Anti-pattern: Direct broker publish in the same transaction as DB write.

```typescript
// OutboxEventPublisher is called within the business transaction
class OutboxEventPublisher implements EventPublisher {
  async publish(event: DomainEvent): Promise<void> {
    await this.db.query(
      `INSERT INTO outbox (event_id, event_type, payload, created_at, published_at) VALUES ($1, $2, $3, NOW(), NULL)`,
      [event.eventId, event.eventType, JSON.stringify(event)]
    );
  }
}

// OutboxProcessor runs as a separate process / cron
class OutboxProcessor {
  async process(): Promise<void> {
    const { rows } = await this.db.query(
      `SELECT * FROM outbox WHERE published_at IS NULL ORDER BY created_at LIMIT 100`
    );
    for (const row of rows) {
      try {
        await this.messageQueue.publish(row.event_type, row.payload);
        await this.db.query(`UPDATE outbox SET published_at = NOW() WHERE event_id = $1`, [row.event_id]);
      } catch (e) { console.error('Failed to publish event:', row.event_id, e); }
    }
  }
}
```

---

## 5. Domain Events vs Integration Events

| Property | Domain Event | Integration Event |
|----------|-------------|-------------------|
| Scope | Within Bounded Context | Across Bounded Contexts |
| Consistency | Synchronous or in-process async | Always asynchronous |
| Consumers | Same BC aggregates/services | Other BCs, external systems |
| Example | OrderItemAdded | OrderConfirmed (public API) |

- Separate types, separate channels
- Application layer translates domain events into integration events
- Rule: Domain events must never be published directly to external systems

---

## 6. Domain Complexity Assessment

**Use full DDD when:**
- Business invariants exist that change frequently
- Multiple use cases with conflicting rules
- Domain experts use specific language (Ubiquitous Language exists)

**Use simple CRUD when:**
- No business invariants to protect
- Mostly data storage and retrieval
- Single table with no complex relationships

**Signs of over-application:**
- Aggregates with no invariants
- Domain Events with no subscribers
- Repositories wrapping single tables with no business logic
- Value Objects that are just wrappers with no validation

---

## Sources

- `builder/reference/ddd-patterns.md` — Entity, Value Object, Aggregate Root, Repository, Domain Service
- `builder/reference/cqrs-patterns.md` — Command/Handler, Query/Handler, Read Model Projection
- `builder/reference/event-sourcing.md` — Domain Event, Event Store, Event-Sourced Aggregate, Saga, Outbox Pattern
