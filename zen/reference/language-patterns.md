# Multi-Language Refactoring Patterns
Purpose: Use this file for non-TypeScript language patterns or concurrency cleanup that still preserves behavior.
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
## Rust Patterns
- **Replace unwrap() with Proper Error Handling**
- **Extract Trait for Polymorphism**
- **Use Iterator Chains Instead of Loops**
- **Replace String with Newtype**
### Edition 2024 / 1.85+ Deep-Dive
- Nested `if let` → `?` / `let-else`, RPIT `use<…>` capture, AFIT vs `#[async_trait]`
- `lazy_static!` → `std::sync::LazyLock` (1.80+), `bon::builder` over hand-rolled builders
- Renaming hygiene per Rust API Guidelines (C-CASE, C-NEWTYPE, C-COMMON-CONVERSIONS)
- Magic-number cleanup with `const` vs `let`, `Duration::from_secs(N)`
- Macro hygiene refactors (`$crate::`, `$(,)?` trailing commas)
- Refactor anti-patterns: `Arc<Mutex<T>>`-as-DI, clone-to-silence-borrowck, generic-everywhere bloat
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Swift Patterns
### Swift 6.2 Deep-Dive
- Nested `if let` → comma-chained binding (5.7+) / `guard let`
- `ObservableObject` + `@Published` → `@Observable` macro (5.9+)
- Manual `Result` propagation → typed `throws(E)` (6.0+)
- Completion-handler bridging → `async`/`await` + `withCheckedThrowingContinuation`
- `@MainActor`-everywhere → fine-grained isolation (Approachable Concurrency 6.2)
- Floating `Task { }` → structured `async let` / `TaskGroup`
- `XCTest` → Swift Testing (`@Test`, `#expect`)
- Primitive-obsession IDs → typed wrappers
- Naming hygiene per Swift API Design Guidelines
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Kotlin Patterns
### Kotlin 2.3+ / K2 Deep-Dive
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
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Cross-Language Principles
| Principle | Application |
|-----------|-------------|
| **Extract for naming** | If you need a comment, extract and name instead |
| **Replace conditional with polymorphism** | Works in any OO/trait-based language |
| **Guard clauses for early return** | Universal pattern for reducing nesting |
| **Table-driven dispatch** | Dict/map/hash replaces long switch/if-elif chains |
| **Newtype/value objects** | Prevent primitive obsession in any typed language |
| **Iterator/stream over loops** | Available in Python, Rust, Java, JS, Go (with generics) |
