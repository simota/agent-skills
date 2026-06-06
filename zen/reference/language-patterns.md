# Multi-Language Refactoring Patterns

Purpose: Use this file for non-TypeScript language patterns or concurrency cleanup that still preserves behavior.

## Contents
- [Language Detection](#language-detection)
- [Python Patterns](#python-patterns)
- [Go Patterns](#go-patterns)
- [Rust Patterns](#rust-patterns)
- [Java Patterns](#java-patterns)
- [Swift Patterns](#swift-patterns)
- [Kotlin Patterns](#kotlin-patterns)
- [Async/Concurrency Patterns](#asyncconcurrency-patterns)
- [Cross-Language Principles](#cross-language-principles)

Language-specific refactoring recipes beyond TypeScript/React. Auto-detect language from file extensions and project config files.

---

## Language Detection

| Indicator | Language |
|-----------|----------|
| `tsconfig.json`, `*.ts`, `*.tsx` | TypeScript → see `typescript-react-patterns.md` |
| `package.json`, `*.js`, `*.jsx` | JavaScript → see `typescript-react-patterns.md` |
| `pyproject.toml`, `setup.py`, `*.py` | Python |
| `go.mod`, `*.go` | Go |
| `Cargo.toml`, `*.rs` | Rust |
| `pom.xml`, `build.gradle`, `*.java` | Java |
| `*.rb`, `Gemfile` | Ruby |
| `*.swift`, `Package.swift` | Swift |

---

## Python Patterns

### Replace Nested Dict with Dataclass

```python
# Before: Raw dict manipulation
def create_user(name, email, role="user"):
    return {
        "name": name,
        "email": email,
        "role": role,
        "created_at": datetime.now(),
    }

user = create_user("Alice", "alice@example.com")
print(user["name"])  # No IDE support, typo-prone

# After: Typed dataclass
@dataclass
class User:
# ...
```

### Simplify Comprehension

```python
# Before: Nested comprehension with filter
result = [transform(item) for item in data if item.active if item.value > threshold]

# After: Extract to generator + named steps
def active_above_threshold(items, threshold):
    return (item for item in items if item.active and item.value > threshold)

result = [transform(item) for item in active_above_threshold(data, threshold)]
```

### Replace Manual Validation with Pydantic

```python
# Before: Manual validation scattered
def create_order(data: dict):
    if "amount" not in data:
        raise ValueError("amount required")
    if not isinstance(data["amount"], (int, float)):
        raise TypeError("amount must be numeric")
    if data["amount"] <= 0:
        raise ValueError("amount must be positive")
    # ... 20 more validation lines

# After: Pydantic model
class OrderRequest(BaseModel):
    amount: Annotated[float, Field(gt=0)]
    currency: str = "USD"
    items: list[OrderItem]
# ...
```

### Context Manager for Resource Cleanup

```python
# Before: Manual cleanup
def process_file(path):
    f = open(path)
    try:
        data = f.read()
        # process...
    finally:
        f.close()

# After: Context manager
def process_file(path):
    with open(path) as f:
        data = f.read()
        # process...
```

### Replace if/elif Chain with Dict Dispatch

```python
# Before: Long if/elif chain
def handle_command(cmd):
    if cmd == "start":
        return start_service()
    elif cmd == "stop":
        return stop_service()
    elif cmd == "restart":
        return restart_service()
    elif cmd == "status":
        return get_status()
    else:
        raise ValueError(f"Unknown command: {cmd}")

# After: Dict dispatch
COMMAND_HANDLERS = {
# ...
```

### Replace Class with NamedTuple for Data

```python
# Before: Full class for simple data
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# After: NamedTuple (immutable, equality, repr for free)
class Point(NamedTuple):
    x: float
    y: float
```

---

## Go Patterns

### Extract Interface at Consumption Point

```go
// Before: Concrete dependency
type OrderService struct {
    db *sql.DB
}

func (s *OrderService) Process(order Order) error {
    // directly uses *sql.DB methods
    _, err := s.db.Exec("INSERT INTO orders ...")
    return err
}

// After: Interface at consumer
type OrderRepository interface {
    Save(order Order) error
}
// ...
```

### Replace Error String Check with Sentinel/Custom Error

```go
// Before: Fragile string comparison
if err != nil && err.Error() == "not found" {
    return nil, nil
}

// After: Sentinel error
var ErrNotFound = errors.New("not found")

if errors.Is(err, ErrNotFound) {
    return nil, nil
}
```

### Wrap Errors with Context

```go
// Before: Raw error return
func processOrder(id string) error {
    order, err := fetchOrder(id)
    if err != nil {
        return err  // caller has no context
    }
    return nil
}

// After: Wrapped with context
func processOrder(id string) error {
    order, err := fetchOrder(id)
    if err != nil {
        return fmt.Errorf("processOrder(%s): fetch failed: %w", id, err)
    }
// ...
```

### Table-Driven Configuration

```go
// Before: Repeated switch
func getTimeout(env string) time.Duration {
    switch env {
    case "dev":
        return 30 * time.Second
    case "staging":
        return 10 * time.Second
    case "prod":
        return 5 * time.Second
    default:
        return 10 * time.Second
    }
}

// After: Table-driven
// ...
```

### Reduce Goroutine Leak with errgroup

```go
// Before: Manual goroutine + channel management
func fetchAll(urls []string) ([]Result, error) {
    ch := make(chan Result, len(urls))
    errCh := make(chan error, len(urls))
    for _, url := range urls {
        go func(u string) { ... }(url)
    }
    // complex collection logic...
}

// After: errgroup
func fetchAll(urls []string) ([]Result, error) {
    g, ctx := errgroup.WithContext(context.Background())
    results := make([]Result, len(urls))
    for i, url := range urls {
// ...
```

---

## Rust Patterns

### Replace unwrap() with Proper Error Handling

```rust
// Before: Panics on error
fn read_config(path: &str) -> Config {
    let content = fs::read_to_string(path).unwrap();
    serde_json::from_str(&content).unwrap()
}

// After: Propagate with ?
fn read_config(path: &str) -> Result<Config, Box<dyn Error>> {
    let content = fs::read_to_string(path)?;
    let config = serde_json::from_str(&content)?;
    Ok(config)
}
```

### Extract Trait for Polymorphism

```rust
// Before: Enum match in every function
fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Circle(r) => std::f64::consts::PI * r * r,
        Shape::Rectangle(w, h) => w * h,
    }
}
fn perimeter(shape: &Shape) -> f64 {
    match shape { ... }
}

// After: Trait dispatch
trait Geometry {
    fn area(&self) -> f64;
    fn perimeter(&self) -> f64;
// ...
```

### Use Iterator Chains Instead of Loops

```rust
// Before: Imperative loop
let mut results = Vec::new();
for item in items {
    if item.is_active() {
        results.push(item.transform());
    }
}

// After: Iterator chain
let results: Vec<_> = items.iter()
    .filter(|item| item.is_active())
    .map(|item| item.transform())
    .collect();
```

### Replace String with Newtype

```rust
// Before: Stringly typed
fn send_email(from: String, to: String, subject: String) { ... }
// Easy to swap arguments by mistake

// After: Newtype wrappers
struct EmailAddress(String);
struct Subject(String);

fn send_email(from: EmailAddress, to: EmailAddress, subject: Subject) { ... }
// Compiler prevents argument swaps
```

### Edition 2024 / 1.85+ Deep-Dive

The patterns above are the cross-language quick reference. For refactor-specific Rust idioms (Edition 2024 baseline) — including:

- Nested `if let` → `?` / `let-else`, RPIT `use<…>` capture, AFIT vs `#[async_trait]`
- `lazy_static!` → `std::sync::LazyLock` (1.80+), `bon::builder` over hand-rolled builders
- Renaming hygiene per Rust API Guidelines (C-CASE, C-NEWTYPE, C-COMMON-CONVERSIONS)
- Magic-number cleanup with `const` vs `let`, `Duration::from_secs(N)`
- Macro hygiene refactors (`$crate::`, `$(,)?` trailing commas)
- Refactor anti-patterns: `Arc<Mutex<T>>`-as-DI, clone-to-silence-borrowck, generic-everywhere bloat

→ Read [`rust-cheatsheet.md`](./rust-cheatsheet.md).

Upstream sources of truth (do not duplicate):

- Bad-pattern catalog: [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md)
- Target idioms / API Guidelines: [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md)
- Edition 2024 language surface: [`builder/reference/rust-language-spec.md`](../../builder/reference/rust-language-spec.md)

---

## Java Patterns

### Replace Null Check Chain with Optional

```java
// Before: Null check chain
String city = null;
if (user != null) {
    Address address = user.getAddress();
    if (address != null) {
        city = address.getCity();
    }
}

// After: Optional chain
String city = Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse(null);
```

### Replace Anonymous Class with Lambda

```java
// Before: Verbose anonymous class
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        handleClick(e);
    }
});

// After: Lambda
button.addActionListener(e -> handleClick(e));

// Or method reference
button.addActionListener(this::handleClick);
```

### Extract Enum for State Machine

```java
// Before: String-based state
if (order.getStatus().equals("PENDING")) { ... }
else if (order.getStatus().equals("SHIPPED")) { ... }

// After: Enum with behavior
enum OrderStatus {
    PENDING {
        @Override public boolean canCancel() { return true; }
    },
    SHIPPED {
        @Override public boolean canCancel() { return false; }
    };
    public abstract boolean canCancel();
}
```

---

## Swift Patterns

### Swift 6.2 Deep-Dive

Cross-language Swift refactors (`Optional` chain → `?`, `class` → `struct`, force-unwrap removal, naming hygiene) follow the same shape as the Java/Kotlin patterns above. For Swift-specific refactor idioms — including:

- Nested `if let` → comma-chained binding (5.7+) / `guard let`
- `ObservableObject` + `@Published` → `@Observable` macro (5.9+)
- Manual `Result` propagation → typed `throws(E)` (6.0+)
- Completion-handler bridging → `async`/`await` + `withCheckedThrowingContinuation`
- `@MainActor`-everywhere → fine-grained isolation (Approachable Concurrency 6.2)
- Floating `Task { }` → structured `async let` / `TaskGroup`
- `XCTest` → Swift Testing (`@Test`, `#expect`)
- Primitive-obsession IDs → typed wrappers
- Naming hygiene per Swift API Design Guidelines

→ Read [`swift-cheatsheet.md`](./swift-cheatsheet.md).

Upstream sources of truth (do not duplicate):

- Bad-pattern catalog: [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md)
- Target idioms / API Design Guidelines: [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md)
- Swift 6.2 language surface: [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md)

---

## Kotlin Patterns

### Kotlin 2.3+ / K2 Deep-Dive

Cross-language Kotlin refactors (null-check chains → `?.let`, `if/else` ladders → `when`, primitive-obsession → `value class`) follow the same shape as the Java patterns above. For Kotlin-specific refactor idioms — including:

- Nested null check → `?.let` chain / Elvis `?:`
- `LiveData` → `StateFlow` + `collectAsStateWithLifecycle`
- `Channel<T>` state → `StateFlow`; `Channel<T>` events → `SharedFlow`
- `Pair<First, Second>` overuse → `data class`
- `data class UserId(val v: String)` → `@JvmInline value class`
- `companion object` utility → top-level function
- `runBlocking` in app code → structured scope
- `kapt` → KSP2 migration
- Scope function decision matrix (`let` / `also` / `apply` / `run` / `with`)
- Naming hygiene per Kotlin Coding Conventions

→ Read [`kotlin-cheatsheet.md`](./kotlin-cheatsheet.md).

Upstream sources of truth (do not duplicate):

- Bad-pattern catalog: [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md)
- Target idioms / Style Guide / Effective Kotlin: [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md)
- K2 language surface: [`builder/reference/kotlin-language-spec.md`](../../builder/reference/kotlin-language-spec.md)

---

## Async/Concurrency Patterns

### TypeScript/JavaScript

#### Promise.all Parallelization

```typescript
// Before: Sequential independent operations
async function loadDashboard(userId: string) {
  const user = await fetchUser(userId);
  const orders = await fetchOrders(userId);
  const notifications = await fetchNotifications(userId);
  return { user, orders, notifications };
}

// After: Parallel with Promise.all
async function loadDashboard(userId: string) {
  const [user, orders, notifications] = await Promise.all([
    fetchUser(userId),
    fetchOrders(userId),
    fetchNotifications(userId),
  ]);
// ...
```

#### Promise Chain → async/await

```typescript
// Before: Nested .then() chain
function processOrder(orderId: string): Promise<Receipt> {
  return fetchOrder(orderId)
    .then(order => validateOrder(order))
    .then(validOrder => calculateTotal(validOrder))
    .then(total => chargePayment(total))
    .then(payment => generateReceipt(payment))
    .catch(err => {
      logger.error('Order processing failed', err);
      throw new AppError('ORDER_FAILED', err.message);
    });
}

// After: Flat async/await
async function processOrder(orderId: string): Promise<Receipt> {
// ...
```

#### Async Error Boundary

```typescript
// Before: Unhandled promise rejections
app.get('/users/:id', (req, res) => {
  fetchUser(req.params.id).then(user => res.json(user));
  // Missing .catch() — unhandled rejection
});

// After: Async error boundary wrapper
const asyncHandler = (fn: RequestHandler) => (req: Request, res: Response, next: NextFunction) =>
  Promise.resolve(fn(req, res, next)).catch(next);

app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await fetchUser(req.params.id);
  res.json(user);
}));
```

### Python

#### asyncio.gather for Parallel Tasks

```python
# Before: Sequential async calls
async def load_dashboard(user_id: str):
    user = await fetch_user(user_id)
    orders = await fetch_orders(user_id)
    notifications = await fetch_notifications(user_id)
    return {"user": user, "orders": orders, "notifications": notifications}

# After: Parallel with asyncio.gather
async def load_dashboard(user_id: str):
    user, orders, notifications = await asyncio.gather(
        fetch_user(user_id),
        fetch_orders(user_id),
        fetch_notifications(user_id),
    )
    return {"user": user, "orders": orders, "notifications": notifications}
```

#### threading → asyncio Migration

```python
# Before: Thread-based concurrency
import threading

def process_items(items):
    results = []
    lock = threading.Lock()

    def worker(item):
        result = expensive_operation(item)
        with lock:
            results.append(result)

    threads = [threading.Thread(target=worker, args=(item,)) for item in items]
    for t in threads:
        t.start()
# ...
```

### Java

#### CompletableFuture Composition

```java
// Before: Blocking sequential calls
public DashboardData loadDashboard(String userId) {
    User user = userService.fetchUser(userId);           // blocks
    List<Order> orders = orderService.fetchOrders(userId); // blocks
    List<Notification> notifs = notifService.fetch(userId); // blocks
    return new DashboardData(user, orders, notifs);
}

// After: Non-blocking with CompletableFuture
public CompletableFuture<DashboardData> loadDashboard(String userId) {
    CompletableFuture<User> userFuture = CompletableFuture.supplyAsync(
        () -> userService.fetchUser(userId));
    CompletableFuture<List<Order>> ordersFuture = CompletableFuture.supplyAsync(
        () -> orderService.fetchOrders(userId));
    CompletableFuture<List<Notification>> notifsFuture = CompletableFuture.supplyAsync(
// ...
```

#### ExecutorService Simplification

```java
// Before: Manual thread pool management
ExecutorService executor = Executors.newFixedThreadPool(10);
List<Future<Result>> futures = new ArrayList<>();
for (String item : items) {
    futures.add(executor.submit(() -> process(item)));
}
List<Result> results = new ArrayList<>();
for (Future<Result> future : futures) {
    results.add(future.get());
}
executor.shutdown();

// After: try-with-resources (Java 19+) or structured approach
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Result>> futures = items.stream()
// ...
```

---

## Cross-Language Principles

These refactoring principles apply regardless of language:

| Principle | Application |
|-----------|-------------|
| **Extract for naming** | If you need a comment, extract and name instead |
| **Replace conditional with polymorphism** | Works in any OO/trait-based language |
| **Guard clauses for early return** | Universal pattern for reducing nesting |
| **Table-driven dispatch** | Dict/map/hash replaces long switch/if-elif chains |
| **Newtype/value objects** | Prevent primitive obsession in any typed language |
| **Iterator/stream over loops** | Available in Python, Rust, Java, JS, Go (with generics) |
