# Language Idioms: TypeScript, Go, Python, Rust

> Per-language idiomatic patterns, project structure, type safety, error handling, and testing.
>
> **Swift and Kotlin do not have inline sections in this file.** Their depth lives in dedicated deep-dive references in this same directory:
> - Swift 6.2+ / Xcode 26: [`swift-language-spec.md`](./swift-language-spec.md), [`swift-best-practices.md`](./swift-best-practices.md), [`swift-anti-patterns.md`](./swift-anti-patterns.md)
> - Kotlin 2.3+ / K2: [`kotlin-language-spec.md`](./kotlin-language-spec.md), [`kotlin-best-practices.md`](./kotlin-best-practices.md), [`kotlin-anti-patterns.md`](./kotlin-anti-patterns.md)
>
> Platform/UI specifics (SwiftUI / Liquid Glass / iOS HIG / Jetpack Compose / Material 3 Expressive) live in the `native` skill, not here.

## 1. TypeScript (6.0 / tsgo 7.0)

### Idioms

- `satisfies` operator: validates type conformance while preserving inferred type
- `as const` assertions: preserve literal types, replace runtime enums
- Template literal types for combinatorial string unions
- `using` / `await using` declarations (Explicit Resource Management) for deterministic cleanup of DB connections, file handles, HTTP clients
- ESM-first; barrel exports via `index.ts`

```typescript
// satisfies: type-safe config with preserved inference
const colors = { red: [255, 0, 0], green: "#00FF00" } satisfies Record<string, Color>;
colors.red.map(v => v * 2);  // OK: tuple type preserved (not Color)

// as const enum alternative (no runtime cost)
const Status = { Pending: "pending", Approved: "approved" } as const;
type Status = (typeof Status)[keyof typeof Status];

// Template literal types
type FullEndpoint = `${"GET" | "POST"} ${"/users" | "/posts"}`;
```

### Project Structure

- Feature-based directories (not type-based layers)
- Node.js backend: `"module": "NodeNext"`, `"moduleResolution": "NodeNext"`
- Frontend (bundler): `"module": "ESNext"`, `"moduleResolution": "Bundler"`

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "verbatimModuleSyntax": true
  }
}
```

### Type Safety

Branded types with Zod v4 (stable):

```typescript
// Zod v4: branded types
const UserIdSchema = z.uuid().brand<'UserId'>();  // v4: top-level z.uuid()
type UserId = z.infer<typeof UserIdSchema>;

// Zod v4: @zod/mini for tree-shaking
import { z, string, object } from '@zod/mini';

// Zod v4: built-in JSON Schema export + unified error field
const jsonSchema = UserSchema.toJSONSchema();
z.string({ error: 'Must be a string' });
```

Manual branded types / type guards:

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };
type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;
getUser(orderId);  // Compile error

// Exhaustiveness check
function getArea(shape: Shape): number {
    switch (shape) {
        case "circle": return Math.PI;
        case "square": return 1;
        default:
            const _exhaustive: never = shape;  // error when new Shape added
            return _exhaustive;
    }
}

// Type guard (prefer over `as` assertion)
function isUser(v: unknown): v is User {
    return typeof v === "object" && v !== null && "name" in v;
}
```

### Error Handling

- `neverthrow` `Result<T, E>` for domain errors; `throw` only for programming bugs
- `fromPromise` for async operations

```typescript
import { fromPromise } from 'neverthrow';

async function createUser(email: string): Promise<Result<User, DomainError>> {
    return fromPromise(db.insert({ email }), (e) => new DbError(e));
}
```

### Testing

```typescript
// Vitest + AAA pattern
describe("UserService", () => {
    it("creates user with valid email", async () => {
        const repo = { save: vi.fn().mockResolvedValue({ id: "1" }) };
        const result = await new UserService(repo).create({ email: "a@b.com" });
        expect(result.isOk()).toBe(true);
        expect(repo.save).toHaveBeenCalledOnce();
    });
});

// Type-level testing
expectTypeOf(parseId("123")).toEqualTypeOf<UserId>();

// MSW for API boundary mocking; testcontainers for integration
const container = await new PostgreSqlContainer().start();

// Property-based (fast-check)
fc.assert(fc.property(fc.array(fc.integer()), xs => sorted(xs).length === xs.length));
```

---

## 2. Go (1.22+)

### Idioms

- Accept interfaces, return structs
- `range` over int (1.22), range-over-func iterators (1.23), generic type aliases (1.24)
- Structured logging with `slog` (stdlib); `any` instead of `interface{}` (1.18+)

```go
// Go 1.22+: range over int
for i := range 10 { fmt.Println(i) }

// Go 1.23+: range-over-func iterators
func Filter[T any](s []T, fn func(T) bool) iter.Seq[T] {
    return func(yield func(T) bool) {
        for _, v := range s {
            if fn(v) && !yield(v) { return }
        }
    }
}

// Go 1.24: generic type aliases
type Set[T comparable] = map[T]struct{}
```

### Project Structure

```
myproject/
├── cmd/api/main.go          # entry point (wiring only)
├── internal/                 # Go-enforced private packages
│   ├── user/                 # feature-based (handler/service/repo)
│   └── product/
├── pkg/                      # public library (omit if not needed)
├── api/                      # OpenAPI/Protobuf definitions
└── go.mod
```

Hexagonal variant: `internal/domain/` → `application/` → `adapter/` (http/postgres/redis).

Rules: no `utils/`, `helpers/`, `common/`; prefer flat over deep; use `internal/` aggressively.

Functional options:

```go
type Option func(*Server)
func WithTimeout(d time.Duration) Option { return func(s *Server) { s.timeout = d } }
func NewServer(addr string, opts ...Option) *Server {
    s := &Server{addr: addr, timeout: 30 * time.Second}
    for _, opt := range opts { opt(s) }
    return s
}
```

### Type Safety

- Generics with type constraints for domain repositories
- Constructor injection with interfaces (not concrete types)

```go
type UserService struct {
    repo   UserRepository  // interface, not *PostgresRepo
    logger *slog.Logger
}
func NewUserService(repo UserRepository, logger *slog.Logger) *UserService {
    return &UserService{repo: repo, logger: logger}
}
```

### Error Handling

```go
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil { return nil, fmt.Errorf("GetUser(%s): %w", id, err) }
    return user, nil
}

if errors.Is(err, ErrNotFound) { /* 404 */ }
var validErr *ValidationError
if errors.As(err, &validErr) { /* handle */ }
// errors.Join for multiple validation errors (Go 1.20+)
```

- `panic` only for initialization failures; `errgroup` for concurrent error aggregation

### Testing

```go
// Table-driven + t.Parallel()
func TestUserService_Create(t *testing.T) {
    tests := []struct{ name, email string; wantErr bool }{
        {"valid", "a@b.com", false},
        {"invalid", "invalid", true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            _, err := NewUserService(&mockRepo{}).Create(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("wantErr=%v, got %v", tt.wantErr, err)
            }
        })
    }
}
```

| Command | Purpose |
|---------|---------|
| `go test -race ./...` | Race condition detection (mandatory) |
| `go test -coverprofile=c.out` | Coverage |
| `go test -bench=. -benchmem` | Benchmarks |

- Mocks: interface-based manual mocks; `t.Helper()` for helpers; `httptest` for HTTP
- Integration: `testcontainers-go`; property-based: `testing/quick` / `gopter`

```go
container, _ := postgres.Run(ctx, "postgres:16")
connStr, _ := container.ConnectionString(ctx)
```

---

## 3. Python (3.12+)

### Idioms

- PEP 695 type parameter syntax (no `TypeVar` boilerplate)
- Structural pattern matching (`match`/`case`)
- `asyncio.TaskGroup` over `asyncio.gather` for structured concurrency
- `frozen @dataclass` for domain entities; Pydantic only at API boundaries

```python
# PEP 695: new generic syntax
class Stack[T]:
    def __init__(self) -> None: self._items: list[T] = []
    def push(self, item: T) -> None: self._items.append(item)
    def pop(self) -> T: return self._items.pop()

type Vector = list[float]

# TaskGroup: automatic cancellation on exception (prefer over gather)
async def process_batch(items: list[str]) -> list[str]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process_item(item)) for item in items]
    return [t.result() for t in tasks]

# Semaphore for concurrency control
async def fetch_with_limit(client: httpx.AsyncClient, url: str) -> str:
    async with asyncio.Semaphore(10):
        return (await client.get(url)).text
```

### Project Structure

```
my-app/
├── pyproject.toml
├── uv.lock              # commit to VCS
├── .python-version
├── src/my_app/
│   ├── __init__.py
│   ├── py.typed         # PEP 561 (libraries)
│   └── main.py
└── tests/
    ├── conftest.py
    └── test_main.py
```

`uv` as default package manager (10x+ faster than pip):

```bash
uv init my-project && uv add fastapi pydantic
uv add --dev pytest ruff mypy && uv run pytest
```

`pyproject.toml` replaces `setup.py` + `requirements.txt`. Commit `uv.lock`; never use `pip install`.

Key `pyproject.toml` tool settings:
- `[tool.ruff.lint] select = ["E","W","F","UP","B","I","SIM","RUF"]`
- `[tool.mypy] python_version = "3.12", strict = true, plugins = ["pydantic.mypy"]`
- `[tool.pytest.ini_options] asyncio_mode = "auto"`

### Type Safety

Pydantic v2 at API boundaries; `frozen @dataclass` for domain entities:

```python
from pydantic import BaseModel, Field, model_validator
from typing import Annotated
from dataclasses import dataclass

# API boundary (Pydantic)
class CreateUserRequest(BaseModel):
    email: Annotated[str, Field(pattern=r'^[\w.-]+@[\w.-]+\.\w+$')]
    age: Annotated[int, Field(ge=0, le=150)]

# Domain entity (frozen dataclass, NOT BaseModel)
@dataclass(frozen=True)
class User:
    id: str
    email: str
    age: int
```

- mypy `--strict` in CI; pyright for IDE feedback
- `Protocol` for structural subtyping

```python
class Serializable(Protocol):
    def to_dict(self) -> dict[str, object]: ...

def save[T: Serializable](item: T) -> None:
    db.insert(item.to_dict())
```

### Error Handling

- Custom exception hierarchies for OOP-style domain errors
- `returns.Result` for functional pipelines (optional)
- `Pydantic ValidationError` at API boundaries → HTTP 422
- `ExceptionGroup` + `except*` for concurrent error aggregation (3.11+)

### Testing

```python
@pytest.mark.parametrize("input_val, expected", [
    ("hello", "HELLO"), ("", ""),
    pytest.param("mixed", "MIXED", id="mixed_case"),
])
def test_to_upper(input_val: str, expected: str):
    assert to_upper(input_val) == expected

# Async (asyncio_mode = "auto" removes @pytest.mark.asyncio)
async def test_fetch_user():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        assert (await client.get("/users/1")).status_code == 200

# Property-based (hypothesis)
@given(st.lists(st.integers()))
def test_sort_preserves_elements(xs: list[int]):
    assert Counter(sorted(xs)) == Counter(xs)

# Integration (testcontainers)
with PostgresContainer("postgres:16") as pg:
    engine = create_engine(pg.get_connection_url())
```

- Mocks: `unittest.mock` with `autospec=True`; `AsyncMock` for coroutines; `respx` for httpx
- Fixture scopes: `function` (default) / `module` / `session` (DB connections)

---

## 4. Rust (Edition 2024, 1.85+)

> **See also (deep-dive references):**
> - [`rust-language-spec.md`](./rust-language-spec.md) — Edition 2024 breaking changes, ownership/lifetimes/variance, GATs, dyn compatibility, async desugaring (Pin, RPITIT, AFIT, async closures), macros, the canonical UB list + Stacked/Tree Borrows, atomics, FFI, `no_std`, const-eval, and the 1.75→1.92 stabilization timeline.
> - [`rust-best-practices.md`](./rust-best-practices.md) — full Rust API Guidelines C-* checklist, error-handling decision tree (thiserror/anyhow/snafu/eyre), workspace patterns, the 2026 cargo+toolchain stack with annotated `deny.toml`, seven-layer testing strategy, perf practices (allocator/SIMD/PGO/BOLT), 21-row production crate matrix, structured-concurrency idioms, docs & doctest discipline, release/distribution, and a 2023→2026 migration cheatsheet.
> - [`rust-anti-patterns.md`](./rust-anti-patterns.md) — 256 anti-patterns across 14 categories (ownership, lifetimes, types, async, errors, perf, traits, macros, unsafe, cargo, testing, security, API design, WASM/embedded) cross-referenced with 40+ Clippy lints and a copy-pasteable `[lints.clippy]` block.
>
> The 20 anti-patterns below remain the short-form baseline. The deep-dive files extend, not replace.

### Idioms

- `let-else` for early-return / unhappy-path-first flow (1.65+)
- `?` operator + `anyhow::Context::context` / `with_context` for error context chains
- `Option<T>` / `Result<T, E>` combinators (`map`, `and_then`, `ok_or`, `unwrap_or_else`) over `match` for simple lifts
- Iterator chains over imperative loops; `collect::<Result<Vec<_>, _>>()` to short-circuit on first error
- `match` with exhaustive arms over nested `if let` chains; let compiler enforce coverage
- `From` / `Into` for infallible, `TryFrom` / `TryInto` for fallible conversions; never hand-roll `to_*` if `From` fits
- Function signatures take `&str` / `&[T]` / `&Path` (not `&String` / `&Vec<T>` / `&PathBuf`); use `AsRef<T>` / `impl AsRef<T>` for ergonomic callers
- Newtype pattern for domain IDs (`struct UserId(Uuid);`) — opt-in `#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]` only as needed
- Builder pattern via the `bon` crate (`#[bon::builder]`) — 2026 idiomatic; hand-roll only for non-trivial state machines
- `Cow<'_, str>` for APIs that may borrow or own depending on input
- `async fn` in traits (stable since 1.75); reach for `async-trait` only when you need `dyn Trait` object safety
- `LazyLock` (stable 1.80) / `OnceLock` (stable 1.70) replace `lazy_static!` and `once_cell::sync::Lazy`
- Trait upcasting (stable 1.86) — `&dyn Sub` to `&dyn Super` without explicit `as_super()`
- `core::error::Error` (re-exported as `std::error::Error`) for `no_std`-friendly library error traits

```rust
// let-else: bail early, keep happy path flat
let Some(user) = repo.find(id).await? else {
    return Err(DomainError::NotFound { id });
};

// ? + anyhow::Context: typed origin, human context chain
use anyhow::Context;
let cfg = fs::read_to_string(&path)
    .with_context(|| format!("failed to read config at {}", path.display()))?;

// Iterator: short-circuit on first parse failure
let ids: Vec<UserId> = raw.iter()
    .map(|s| s.parse::<UserId>())
    .collect::<Result<_, _>>()?;

// Newtype + derives only when needed
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, serde::Serialize, serde::Deserialize)]
pub struct UserId(uuid::Uuid);

// async in trait (no async-trait crate needed for static dispatch)
pub trait UserRepo: Send + Sync {
    async fn find(&self, id: UserId) -> Result<Option<User>, RepoError>;
}
```

#### Async & Concurrency

- Pick the Tokio flavor explicitly: `#[tokio::main(flavor = "current_thread")]` for CLIs / single-threaded servers, multi-thread (default) for HTTP servers
- Wrap CPU-bound or blocking I/O in `tokio::task::spawn_blocking`; never call sync I/O directly inside an async fn
- Structured concurrency: `tokio::task::JoinSet` for dynamic fan-out, store `JoinHandle` if you spawn — never orphan a task
- `tokio::select!` requires every branch to be cancellation-safe; read each future's docs before composing
- Use **bounded** `tokio::sync::mpsc::channel(N)` for backpressure; `broadcast` for fan-out, `watch` for latest-value
- Spawned futures must be `Send + 'static`; `Arc<RwLock<T>>` only when read-heavy and contention is measured — default to `Arc<Mutex<T>>`
- Never hold a `std::sync::MutexGuard` across `.await` (the guard is `!Send`); either drop before await or switch to `tokio::sync::Mutex` — but prefer `std::sync::Mutex` (faster) and restructure the code to release before yielding

```rust
use tokio::task::JoinSet;

let mut set = JoinSet::new();
for url in urls { set.spawn(fetch(url)); }
while let Some(res) = set.join_next().await {
    let body = res??;  // join error, then task error
    // ...
}
```

### Project Structure

```
my-crate/
├── Cargo.toml
├── Cargo.lock           # commit for both bin AND lib (2024+ guidance)
├── rust-toolchain.toml  # pin channel/components
├── deny.toml            # cargo-deny config
├── src/
│   ├── main.rs / lib.rs
│   ├── domain/          # pure types, no I/O
│   ├── application/     # use cases
│   └── adapter/         # http, db, fs
├── tests/               # integration tests (one binary per file)
└── benches/             # criterion benches
```

Workspace `Cargo.toml`:

```toml
[workspace]
resolver = "3"                         # Edition 2024 default

[workspace.package]
edition      = "2024"
rust-version = "1.85"                  # declare MSRV explicitly

[workspace.lints.clippy]
pedantic = { level = "warn", priority = -1 }
unwrap_used = "warn"
expect_used = "warn"
```

Rules: feature flags **additive only** (never mutually exclusive — breaks `cargo build --all-features`); `rustfmt` + `clippy -- -D warnings` enforced in CI; lockfile committed everywhere.

Toolchain — `cargo-deny` (license / advisory / source), `cargo-audit` (RUSTSEC vulns), `cargo-machete` (unused deps), `cargo-nextest` (parallel test runner), `cargo-hack` (feature-matrix builds).

Production crates (2026 baseline):

| Concern | Default | Notes |
|---------|---------|-------|
| HTTP server | `axum` | tokio-native, tower middleware |
| HTTP client | `reqwest` | `hyper` directly only when you need low-level |
| DB | `sqlx` | compile-time-checked SQL; `sea-orm` for ActiveRecord, `diesel` for DSL |
| Serde | `serde` + `serde_json` + `rmp-serde` / `bincode` v2 | DTO layer, not domain types |
| Time | `jiff` | tz-aware, modern; `time` for `no_std`; avoid new `chrono` adoption |
| UUID | `uuid` (feature `v7`) | time-sortable IDs |
| Logging | `tracing` + `tracing-subscriber` | not `log` |
| Config | `figment` / `config` + explicit struct | parse-don't-validate at startup |
| CLI | `clap` v4 (derive) | derive macros over builder API |

### Type Safety

Make illegal states unrepresentable; lean on the type system before runtime checks.

```rust
// Sum types over boolean flag soup
pub enum Order {
    Draft     { items: Vec<Item> },
    Submitted { items: NonEmpty<Item>, submitted_at: Timestamp },
    Shipped   { tracking: TrackingNumber, shipped_at: Timestamp },
}

// Typestate: compile-time state machine
pub struct Connection<S> { socket: TcpStream, _state: PhantomData<S> }
pub struct Closed; pub struct Open;
impl Connection<Closed> { pub fn open(self) -> Connection<Open> { /* ... */ } }
impl Connection<Open>   { pub fn send(&mut self, _: &[u8]) { /* ... */ } }
// `connection.send()` on Closed = compile error, no runtime branch

// Sealed trait: prevent downstream impls
mod private { pub trait Sealed {} }
pub trait Component: private::Sealed { /* ... */ }

// Forward-compatible public enums / structs
#[non_exhaustive]
pub enum ApiError { NotFound, Unauthorized, RateLimited { retry_after: Duration } }
```

### Error Handling

- **Library crates**: `thiserror` enum, one variant per failure mode, `#[from]` for transparent wrapping, never expose `Box<dyn Error>` in public API
- **Binary / application crates**: `anyhow::Result<T>` with `.context()` chains; `fn main() -> anyhow::Result<()>`
- Never mix `thiserror` and `anyhow` in the **same crate's public surface** — `anyhow::Error` erases the type information `thiserror` exists to preserve
- Reserve `panic!` for invariant violations that mean the program is fundamentally broken; never for control flow

```rust
// Library: typed errors
#[derive(Debug, thiserror::Error)]
pub enum UserError {
    #[error("user {0} not found")]
    NotFound(UserId),
    #[error("invalid email: {0}")]
    InvalidEmail(String),
    #[error(transparent)]
    Db(#[from] sqlx::Error),
}

// Binary: anyhow with context
fn main() -> anyhow::Result<()> {
    let cfg = load_config().context("loading config")?;
    run(cfg).context("running server")?;
    Ok(())
}
```

### Testing

```rust
// Unit tests co-located
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rejects_invalid_email() {
        let err = User::new("not-an-email").unwrap_err();
        assert!(matches!(err, UserError::InvalidEmail(_)));
    }

    #[tokio::test(flavor = "current_thread")]
    async fn finds_existing_user() { /* ... */ }
}

// rstest: parameterized + fixtures
#[rstest]
#[case("a@b.com", true)]
#[case("not-an-email", false)]
fn validates_email(#[case] input: &str, #[case] ok: bool) {
    assert_eq!(Email::parse(input).is_ok(), ok);
}

// proptest: property-based
proptest! {
    #[test]
    fn sort_preserves_multiset(xs in prop::collection::vec(0i32..1000, 0..100)) {
        let mut sorted = xs.clone(); sorted.sort();
        prop_assert_eq!(xs.iter().sum::<i32>(), sorted.iter().sum::<i32>());
    }
}

// insta: snapshot
#[test]
fn renders_invoice() { insta::assert_yaml_snapshot!(render(&invoice)); }
```

| Tool | Purpose |
|------|---------|
| `cargo nextest run` | Parallel runner; ~3x faster than `cargo test`, per-test isolation |
| `criterion` | Statistical benchmarks under `benches/` |
| `mockall` | Mocks — but prefer trait injection + hand-rolled fakes |
| `tests/` directory | Integration tests; each file = its own crate-level binary |

### Anti-Patterns

| # | Pattern | Do this instead |
|---|---------|-----------------|
| 1 | `.unwrap()` / `.expect()` in production code | Return `Result`; allow only in tests, `main`, or with `// SAFETY:` proof comment |
| 2 | Defensive `.clone()` to escape the borrow checker | Redesign ownership; clone only when semantically required |
| 3 | `&Vec<T>` / `&String` / `&PathBuf` in signatures | `&[T]` / `&str` / `&Path` — generic over storage |
| 4 | Wrapping every field in `Arc<Mutex<T>>` | Design ownership first; reach for `Arc` when sharing is required, not preemptively |
| 5 | Holding `std::sync::MutexGuard` across `.await` | Drop guard before await, or use `tokio::sync::Mutex` (only if guard *must* cross await) |
| 6 | `panic!` for control flow | Return `Result<T, E>`; reserve panic for unrecoverable invariant violations |
| 7 | `futures::executor::block_on` inside async code | Compose with `.await`; `block_on` deadlocks on multi-thread runtimes |
| 8 | Over-generic `fn f<T: Trait>(...)` everywhere | Use `&dyn Trait` when monomorphization bloat or compile time matters |
| 9 | Explicit `'a` annotations the compiler could elide | Trust lifetime elision; annotate only when the borrow checker actually demands it |
| 10 | `Result<(), Box<dyn Error>>` in library public API | Concrete `thiserror` enum so callers can match variants |
| 11 | `lazy_static!` / `once_cell::sync::Lazy` | `std::sync::LazyLock` (1.80+) / `OnceLock` (1.70+) |
| 12 | `s + &t + &u` string concatenation | `format!("{s}{t}{u}")` or `String::push_str` in a loop |
| 13 | Deeply nested `if let Some(x) = ... { if let Some(y) = ... { ... } }` | `?` operator, `let-else`, or `Option::and_then` chains |
| 14 | Auto-deriving `Clone`/`Copy`/`Debug`/`Hash`/`Eq` on every struct | Derive deliberately — `Copy` on large structs hurts perf, `Debug` on secrets leaks |
| 15 | `impl Deserialize for DomainEntity` directly | Define a DTO struct with `Deserialize`, then `TryFrom<Dto> for Entity` enforces invariants |
| 16 | `unsafe { ... }` / `mem::transmute` without `// SAFETY:` comment | Document invariants the caller / surrounding code must uphold |
| 17 | Mutually exclusive `#[cfg(feature = "...")]` flags | Features must be additive; gate with separate crates or runtime config |
| 18 | `tokio::spawn(fut)` and dropping the `JoinHandle` | Store in `JoinSet` or await the handle; orphaned tasks hide panics and leak |
| 19 | `mpsc::unbounded_channel()` | Use bounded `channel(N)` — backpressure is a feature, not a limitation |
| 20 | Re-exporting transitive dep types (`pub use reqwest::Client`) in public API | Wrap in a newtype; otherwise consumers pin to your transitive versions |

---

## 5. Cross-Language Principles

### Testing Trophy

```
    ╱ E2E ╲           few: critical user journeys
   ╱ Integration ╲    many: API/DB boundaries, component connections
  ╱ Unit ╲            moderate: pure functions, business logic
 ╱ Static Analysis ╲  always: type checkers, lint
```

### Mock Strategies

| Principle | Rule |
|-----------|------|
| Mock at boundaries only | External I/O, network, DB — not internal collaborators |
| Own your mocks | Wrap third-party libs; mock the wrapper |
| Test behavior, not implementation | Assert outputs/side-effects, not call order |

### Property-Based Testing

| Property | Example |
|----------|---------|
| Round-trip | `decode(encode(x)) == x` |
| Idempotency | `f(f(x)) == f(x)` |
| Element preservation | `Counter(sort(x)) == Counter(x)` |
| Invariants | `0 <= normalize(x) <= 1` |

| Language | Tool |
|----------|------|
| TypeScript | fast-check |
| Go | `testing/quick`, gopter |
| Python | hypothesis |

### Test Quality Targets

| Metric | Target |
|--------|--------|
| Branch coverage | 80%+ |
| Mutation score | 70%+ |
| Flaky rate | < 1% |
| Unit test speed | < 1s per test |

### Anti-Patterns (All Languages)

| # | Pattern | Fix |
|---|---------|-----|
| 1 | Inter-test dependencies | Fully isolate each test (no shared mutable state) |
| 2 | Testing implementation details | Test observable behavior |
| 3 | Excessive mocking | Complement with integration tests |
| 4 | `sleep` in tests | Use events / polling / testcontainers |
| 5 | Large snapshot assertions | Small, focused assertions |

---

**Sources:**
- [satisfies operator (2ality)](https://2ality.com/2025/02/satisfies-operator.html)
- [Total TypeScript Patterns](https://www.totaltypescript.com/four-essential-typescript-patterns)
- [TypeScript 5.8 Release](https://devblogs.microsoft.com/typescript/announcing-typescript-5-8/)
- [Go 1.24 Release Notes](https://go.dev/blog/go1.24)
- [Go Anti-patterns (hackmysql)](https://hackmysql.com/golang/go-antipatterns/)
- [ThreeDots Clean Architecture](https://threedots.tech/post/introducing-clean-architecture/)
- [Python 3.12 What's New](https://docs.python.org/3/whatsnew/3.12.html)
- [Real Python uv Guide](https://realpython.com/python-uv/)
- [Ruff Configuration](https://docs.astral.sh/ruff/configuration/)
- [Rust Edition 2024 / 1.85 announcement](https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Tokio — Shared state & cancellation safety](https://tokio.rs/tokio/tutorial/shared-state)
- [thiserror vs anyhow](https://nick.groenen.me/notes/thiserror-vs-anyhow/)
- [bon — builder macros](https://bon-rs.com/)
- [cargo-nextest](https://nexte.st/)
- [Testing Trophy (Kent C. Dodds)](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
- [Property-Based Testing with Hypothesis](https://semaphore.io/blog/property-based-testing-python-hypothesis-pytest)
