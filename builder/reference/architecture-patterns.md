# Architecture & Design Patterns

> Clean/Hexagonal Architecture, SOLID (2025 interpretation), CUPID, API design selection, error-handling strategy, DI principles, anti-patterns

## 1. Clean / Hexagonal Architecture

> See also: `atlas/reference/architecture-patterns.md` for a full TypeScript folder-structure and code walkthrough of Clean Architecture and Hexagonal Architecture, aimed at analyzing an existing codebase. This section covers the dependency rule and a Go-based Hexagonal implementation example, aimed at greenfield builds.

### Dependency Rule (most important)

> "Source code dependencies can only point inward."

```
[Frameworks] → [Adapters] → [Use Cases] → [Domain/Entities]
   outer            ↓            ↓         inner (most stable)
```

| Layer | Responsibility | Depends on |
|----|------|--------|
| Domain | Entities, value objects, domain services | None |
| Application | Use cases (1 user action = 1 use case) | Domain only |
| Infrastructure | Repository implementations, adapters, DB connections | Application, Domain |
| Frameworks | Web framework, DB driver | Everything inward |

### Hexagonal (Ports & Adapters)

- **Port**: an interface that abstracts interaction with the outside world
- **Adapter**: a concrete implementation of a port

> "Business logic should not depend on the choice of REST/GraphQL, nor on the choice of DB/CSV."

### Hexagonal Architecture — Go Implementation Example

```go
// domain/repository.go — Port (interface)
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
}

// internal/service/user_service.go — Application Core
type UserService struct {
    repo domain.UserRepository  // depends on interface only
}

// internal/adapter/postgres/user_repo.go — Secondary Adapter
type PostgresUserRepo struct { db *pgxpool.Pool }
func (r *PostgresUserRepo) FindByID(ctx context.Context, id string) (*domain.User, error) { /* ... */ }

// internal/adapter/handler/user_handler.go — Primary Adapter
type UserHandler struct { svc *service.UserService }
```

### Selection Guide

| Architecture | Best for | Core principle |
|--------------|----------|---------|
| Clean Architecture | Complex business rules, domain-heavy systems | Dependencies point inward (concentric circles) |
| Hexagonal (Ports & Adapters) | Many external integrations (DB, API, messaging) | Primary/Secondary ports isolate technical detail |
| Feature-based (Screaming) | Mid-sized apps, reducing cognitive load | Directory structure "screams" the domain |
| Simple Layered | Small apps, CRUD-heavy | Controller → Service → Repository |

**Note**: This is a separation-of-concerns principle, not a folder structure — customize per project.

---

## 2. SOLID: 2025 Interpretation

| Principle | Classical interpretation | 2025 application |
|------|-----------|-------------|
| **S**RP | One class, one responsibility | Separate business logic from infrastructure |
| **O**CP | Open for extension, closed for modification | Plugin architecture |
| **L**SP | Subtypes must be substitutable | Prevent integration failures in polymorphic APIs |
| **I**SP | Clients shouldn't depend on unused methods | Small, context-specific contracts |
| **D**IP | Depend on abstractions | Use DI to decouple business logic from infrastructure |

**2025 recognition**: SOLID isn't limited to OOP — it's a universal principle applicable to functional and system-level design too.

### CUPID (complementary framework)

| Property | Meaning |
|-----------|------|
| **C**omposable | Easy to combine, minimal dependencies |
| **U**nix philosophy | Do one thing well |
| **P**redictable | Behaves as expected |
| **I**diomatic | Understandable to other developers |
| **D**omain-based | Models the problem domain |

SOLID = principles for the development process; CUPID = properties of finished code.

---

## 3. API Design Selection

| Protocol | Best case | Characteristics |
|-----------|-------------|------|
| **REST** | CRUD, public APIs | Standard HTTP, widely adopted, low learning cost |
| **GraphQL** | SPA/mobile, complex data | Client-driven, resolves over-fetching |
| **gRPC** | Inter-microservice communication | Binary, 5-7x lower latency, bidirectional streaming |

### 2025 Trend

A coexistence pattern: gRPC internally, REST externally, and a GraphQL gateway for advanced clients.

### Common Principles

- Pagination + filtering (large datasets)
- Rate limiting (role-based)
- Semantic versioning (deprecation notices)
- OAuth 2.0 / JWT / API keys
- Thorough input validation
- Enforce HTTPS

---

## 4. Error-Handling Strategy

| Pattern | Language | Characteristics |
|---------|------|------|
| Error code return | Go | Simple, easy to forget |
| Exceptions (try/catch) | Java, Python, TS | Separates happy path, not explicit in the signature |
| **Result/Either** | Rust, TS, Kotlin | **Explicit + type-safe (recommended)** |

### Result Pattern (recommended for 2025)

- The compiler guarantees every result is handled
- Railway-Oriented Programming composes functions
- TS: neverthrow, Python: Result type, Go: error interface

### Complementary Patterns

| Pattern | Use |
|---------|------|
| Circuit Breaker | Trip when an external service's failure threshold is exceeded |
| Retry with Backoff | Retry with increasing delay |
| Bulkhead | Isolate failures, prevent cascading |

---

## 5. Dependency Injection Principles

### Constructor Injection (most recommended)

Fully initialize with all dependencies at construction time.

### Composition Root

The single place in the app where dependencies are wired and the object graph is instantiated.

### Best Practices

1. **Program against interfaces** (abstractions, not concretions)
2. **Avoid Service Locator** (it hides dependencies)
3. **Keep services small** (many injected dependencies signal an SRP violation)
4. **Avoid stateful static classes** (use singleton services instead)
5. **Don't `new` dependencies directly** (receive them via the constructor)

---

## 6. Code Quality Metrics (2025)

| Metric | Description |
|-----------|------|
| Defect Density | Bugs per KLOC |
| Code Churn | Rate of module change (high = unstable) |
| Cyclomatic Complexity | Complexity of branching |
| Architectural Alignment | Conformance to the design pattern |

**AI-era challenge**: Over 70% of developers use AI coding tools weekly, and 48% report difficulty maintaining quality with AI-generated code. The importance of architectural-conformance review is increasing.

---

## 7. Domain Complexity Assessment

### When to use full DDD
- Business invariants change frequently
- Multiple use cases have conflicting rules
- Domain experts use a distinct language (a Ubiquitous Language exists)
- Complex state transitions and validation rules exist

### When to use Simple CRUD
- No business invariants to protect
- The primary use is storing and retrieving data
- Simple CRUD operations on a single resource
- No complex relations or business rules

### Signs of DDD over-application
- Aggregates with no invariant to protect
- Domain Events with no subscriber
- Repositories that are single-table wrappers with no business logic
- Value Objects that are unvalidated primitive wrappers
- The same boilerplate on every service: Entity → Repository → Service → Controller

### Decision Rule
Ask: "Does this domain have business invariants that change frequently?"
- YES → use DDD tactical patterns (Entity, Value Object, Aggregate)
- NO → use simple CRUD with validation at the boundary

---

## 8. Design Anti-Patterns

| # | Pattern | Problem | Fix |
|---|---------|------|------|
| 1 | God Object | Excessive concentration of responsibility | Apply SOLID, decompose into specialized classes |
| 2 | Spaghetti Code | Tangled, unstructured code | Modularize, separate concerns |
| 3 | Golden Hammer | Applying one tool to every problem | Choose the right tool per problem |
| 4 | Boat Anchor | Leaving unused code in place | YAGNI, prune regularly |
| 5 | Copy-Paste Programming | Duplicating code without understanding it | Refactor into reusable functions |
| 6 | Premature Optimization | Optimizing low-impact parts | Measure → profile → optimize |
| 7 | Service Locator | Hides dependencies | Use constructor injection |

**Source:** [Clean vs Hexagonal Architecture](https://dev.to/dyarleniber/hexagonal-architecture-and-clean-architecture-with-examples-48oi) · [SOLID 2025 (Ethisys)](https://ethisys.co.uk/2025/06/05/building-resilient-software-why-solid-principles-still-matter-in-2025/) · [CUPID (Dan North)](https://dannorth.net/blog/cupid-for-joyful-coding/) · [API Design 2025](https://dev.to/cryptosandy/api-design-best-practices-in-2025-rest-graphql-and-grpc-2666) · [CodeOpinion: STOP Doing Dogmatic DDD](https://codeopinion.com/stop-doing-dogmatic-domain-driven-design/) · [Kranio: DDD Common Mistakes and Anti-Patterns](https://www.kranio.io/en/blog/de-bueno-a-excelente-en-ddd-errores-comunes-y-anti-patrones-en-domain-driven-design---10-10) · [Clean Architecture vs Hexagonal](https://www.vinaypal.com/2025/04/clean-architecture-vs-hexagonal.html)
