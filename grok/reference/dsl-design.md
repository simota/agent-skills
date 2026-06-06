# DSL Design

**Purpose:** Architecture patterns and trade-off guidance for designing internal and external domain-specific languages.
**Read when:** Deciding whether to build a DSL, choosing between internal and external, picking an embedding style, planning DSL evolution, or reviewing an existing DSL.

## Contents
- Internal vs external DSL
- Six internal DSL architectures
- External DSL considerations
- Design principles
- Evolution and versioning
- Anti-patterns

---

## Internal vs External DSL

### Internal DSL (host-language embedded)

The DSL is valid host-language syntax. Users write host code that happens to look domain-specific.

**Pros:**
- No separate parser, no separate build step.
- Full host-language tooling (IDE, debugger, type checker) works.
- Composition with host functions is free.
- Lower activation energy for host-language developers.

**Cons:**
- Syntax is constrained by the host.
- Domain experts must learn host syntax.
- Error messages leak host-language stack traces.
- Discoverability depends on host IDE (fluent chains work in TS; less so in Lisp).

### External DSL (standalone syntax)

The DSL has its own grammar and parser; text is parsed separately from host code.

**Pros:**
- Syntax optimized for the domain, unconstrained.
- Non-programmers can write it.
- Full control over error messages.
- Can be targeted by multiple host runtimes.

**Cons:**
- Requires a parser (see `parser-generators.md`).
- Requires separate tooling (highlighter, formatter, linter).
- Integration with host types is indirect.
- Version migration is harder.

### When to choose which

| Factor | Lean internal | Lean external |
|--------|---------------|---------------|
| Audience | Host-language developers | Non-programmers, domain experts |
| Reuse of host tooling | Critical | Not needed |
| Editor experience | IDE-native is enough | Custom syntax highlighting needed |
| Config vs behavior | Behavior | Config / declarative |
| Cross-runtime use | Single host | Multi-runtime |
| Investment | Small-to-medium | Medium-to-large |

**Heuristic:** start internal, upgrade to external only when a real domain-expert audience emerges.

---

## Six Internal DSL Architectures

### 1. Fluent API (builder pattern)

Chained method calls; each method returns a builder, possibly of a more refined type.

**Examples:** Kysely, Drizzle ORM, Jest `expect().toBe()`, MockK, AssertJ.

```typescript
const q = db.selectFrom('user')
  .where('age', '>', 18)
  .orderBy('created_at', 'desc')
  .select(['id', 'name'])
  .limit(10);
```

**Pros:**
- Discoverable: IDE autocomplete shows next-step methods.
- Type-safe progression possible via phantom types or conditional types.
- Reads left-to-right in English order.

**Cons:**
- Deep chains can hit type-inference limits (especially in TS).
- Cyclic or branching syntax is awkward.
- State carried in the builder can leak across calls if mutable.

**Type-state pattern (TypeScript):**

```typescript
interface Draft { from(tbl: string): WithFrom; }
interface WithFrom { where(...): WithFrom; select(...): Query; }
interface Query { execute(): Promise<Row[]>; }
```

Each method returns the next stage; missing methods are unreachable.

### 2. Template literal DSL

Tagged templates embed a foreign syntax inside host strings; a tag function parses the literal at runtime or compile time.

**Examples:** `styled-components`, `gql` from `graphql-tag`, GROQ (Sanity), Prisma Client's `$queryRaw`.

```typescript
const Button = styled.button`
  padding: 8px 16px;
  background: ${props => props.primary ? 'blue' : 'gray'};
`;

const query = gql`
  query User($id: ID!) {
    user(id: $id) { id name }
  }
`;
```

**Pros:**
- Dedicated syntax inside the string; IDE plugins provide highlighting (ESLint plugins, VSCode extensions).
- Interpolation is first-class (`${...}` slots).
- Build-time extraction possible (Prisma generates types from SQL).

**Cons:**
- Without IDE plugin, just a string — no syntax highlighting, no error checking.
- Interpolation can be a security hazard (SQL injection in naive implementations).
- Parser must handle injected expressions.

### 3. S-expression embedded

Lisp dialects (Clojure, Racket, hy, Scheme) make macros the DSL mechanism. Code is data (homoiconic).

**Examples:** Clojure `honeysql`, Racket's `#lang`, Lisp macros broadly.

```clojure
(-> {:select [:id :name]
     :from [:user]
     :where [:> :age 18]}
    sql/format)
```

**Pros:**
- Macros let the DSL modify evaluation semantics, not just library calls.
- Homoiconicity makes AST manipulation trivial.

**Cons:**
- Steep onboarding for non-Lispers.
- Macros can obscure control flow.

### 4. YAML / JSON-based

The DSL is a schema-validated data document; an interpreter walks the structure.

**Examples:** Kubernetes manifests, CircleCI config, GitHub Actions workflows, Ansible playbooks, OpenAPI specs.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
```

**Pros:**
- Tool-friendly (JSON Schema validation, language-agnostic).
- Non-programmers can author with templates.
- Git-diffs are meaningful.

**Cons:**
- Logic is awkward: ternaries become template expressions (`${{ ... }}` in GHA), loops become `for-each` constructs.
- Readability degrades as indentation deepens.
- Schema validation can only catch structural errors; semantic errors slip through.

**Best practices:**
- Use JSON Schema / OpenAPI Schema / CUE for validation.
- Provide a formatter (prettier, yamllint).
- Reserve DSL for config; extract logic to real code or to a dedicated expression language (CEL, JSONata, jq).

### 5. Ruby-style internal DSL

Ruby's blocks + `method_missing` + `instance_eval` enable DSLs that look like declarative languages.

**Examples:** Sinatra (`get '/users' do ... end`), RSpec (`describe ... do it ... end`), Rails routes, Rake tasks, Capistrano deploys.

```ruby
describe User do
  context 'when new' do
    it 'has no id' do
      expect(User.new.id).to be_nil
    end
  end
end
```

**Pros:**
- Reads close to natural language.
- Blocks naturally map to domain concepts (suites, contexts, steps).
- Metaprogramming makes the DSL concise.

**Cons:**
- Magic surface: `method_missing` traps are hard to debug.
- Refactoring tools struggle to track method resolution.
- Newcomers don't know what's available without reading docs.

### 6. Kotlin DSL

Trailing-lambda syntax + extension functions + infix notation + `@DslMarker` annotation.

**Examples:** Gradle Kotlin DSL, Jetpack Compose, Ktor routing, Exposed SQL.

```kotlin
routing {
    get("/users") {
        call.respond(Users.all())
    }
    post("/users") {
        val user = call.receive<User>()
        Users.insert(user)
        call.respond(HttpStatusCode.Created)
    }
}
```

**Pros:**
- Type-safe; IDE autocomplete works.
- `@DslMarker` prevents accidental scope leakage.
- Trailing lambda reads like a block-oriented language.

**Cons:**
- Kotlin-specific — no portable equivalent in most languages.
- Scope management (implicit `this`) can confuse readers.

---

## External DSL Considerations

When to promote an internal DSL to external:

- Target authors are non-programmers (policy writers, game designers, marketers).
- You need multi-runtime execution (same DSL runs in a JVM backend and a JS frontend).
- Custom syntax would meaningfully improve clarity (query languages often qualify).
- Tool investment is justified (you can afford a parser, formatter, linter, language server).

See `parser-generators.md` for implementation choices.

**LSP integration:** any modern external DSL should have a Language Server Protocol implementation for editor support. `vscode-languageserver-node` (TS), `lsp4j` (Java), `tower-lsp` (Rust) are canonical starting points.

**Formatter:** every external DSL needs a formatter. Inconsistent whitespace is the first sign of a half-baked language.

---

## Design Principles

### Closed vocabulary

Define the complete set of keywords / operators / built-ins up front. Say no to additions. A DSL's value comes from constraint; unbounded DSLs become general-purpose languages (and bad ones).

Examples of closed vocabularies that have held:
- SQL's SELECT/FROM/WHERE/GROUP BY/ORDER BY (additions are rare and deliberate).
- CSS selectors (pseudo-class additions are deliberated in CSSWG).

### Composition over primitives

A small set of composable combinators beats a large set of special-case features. The language grows by users combining primitives, not by you adding new keywords.

Parser combinators (`ts-parsec`, `parsimmon`) are themselves a DSL following this principle: `seq`, `alt`, `many`, `opt` compose into arbitrary grammars.

### Errors reference DSL lexicon, not host language

A GraphQL error should say "unknown field `userId` on type `User`; did you mean `user_id`?", not "TypeError: Cannot read property 'resolve' of undefined".

For internal DSLs, catch host exceptions at the DSL boundary and re-throw with DSL context. For external DSLs, design error messages from first principles (see Elm/rustc style in `parser-generators.md`).

### Explicit version field

Every DSL document starts with a version:

```yaml
version: 2
rules:
  - ...
```

```typescript
// Internal DSL: version in imports
import { defineConfig } from 'vite/v5';
```

Without a version, evolution is impossible without breaking every existing document.

### Progressive disclosure

Simple cases use simple syntax; complex cases require more syntax. 80% of users should never see 20% of the language.

Example: Prettier's config is JSON by default; escape hatches to JS config only when needed.

### Declarative over imperative

DSLs shine for declarative domains (config, queries, UI layout, state machines). Imperative DSLs compete with the host language and usually lose. If you find yourself adding `if`, `for`, `while` to a DSL, reconsider whether a library API is the right abstraction.

---

## Evolution and Versioning

### Backward-compatible additions

- Adding a new optional field: safe.
- Adding a new keyword that does not conflict with existing identifiers: safe.
- Adding a new operator with lower precedence than existing ones: usually safe.

### Breaking changes

- Removing a keyword: breaking.
- Changing operator precedence: breaking.
- Tightening validation: breaking for documents that were previously lenient.

### Deprecation protocol

1. Announce deprecation in release notes.
2. Emit warnings for deprecated syntax (DSL must have a warning channel — design it early).
3. Provide a migration tool (codemod; see `ast-transforms.md`).
4. Hold for at least one major version before removal.
5. Remove with clear upgrade path documented.

### Version gates

```yaml
version: 2
feature-flags:
  - new-query-syntax
```

Allow opt-in to experimental features without committing to them in version 2's stable surface.

### Migration tools

For any DSL with external users, ship a codemod. For internal DSLs, the codemod is an AST transform over host code (see `ast-transforms.md`). For external DSLs, the codemod is a source-to-source transformation using your own parser.

---

## Anti-patterns

### 1. Turing-complete config

A configuration language should not be Turing-complete. When users can write arbitrary loops and conditionals in your config, you have reinvented a programming language with worse tooling.

**Examples of this going wrong:** Jenkins declarative pipelines that grew a `script { ... }` escape hatch and became full Groovy; Helm's Go template language inside YAML.

**Rule:** if logic is unavoidable, provide a bounded expression language (CEL, JSONata, jq, Rego, Starlark) rather than a general-purpose escape hatch.

### 2. Stringly-typed DSL

Representing dates, numbers, durations, enums as strings parsed at interpretation time. Loses all host-language type checking.

```typescript
// BAD
const schedule = { when: '2025-03-01T10:00:00Z', duration: '15m' };

// BETTER
const schedule = { when: new Date('2025-03-01T10:00:00Z'), duration: Duration.minutes(15) };
```

When an external text format is required (e.g., config files), parse on load and fail fast with specific errors.

### 3. Host-language stack trace leakage

```
Error: Cannot read properties of undefined (reading 'resolve')
  at GraphQLObjectType.resolveField (graphql/execution/execute.ts:542)
  at ...
```

User sees host internals. Catch at DSL boundary and produce DSL-level diagnostics with source positions.

### 4. Unbounded syntax sprawl

Every user request becomes a new keyword. Within two years the DSL is larger than the domain it modeled.

**Rule:** close the vocabulary; new needs become library calls in the host language, not new DSL syntax.

### 5. Silent semantics

DSL syntax that looks like host syntax but does something different.

```ruby
# Ruby DSL
describe 'calculator' do
  let(:x) { 1 }
  it 'adds' do
    expect(x + 1).to eq(2)  # what is 'eq'? what is 'expect'?
  end
end
```

Acceptable when documented; hostile when developers have to guess. Mitigate with IDE hover-docs and discoverable method names.

### 6. Breaking changes without migration

Shipping a new major version and saying "rewrite your 10,000 YAML files". Always ship a codemod; if you can't automate the migration, the change is probably too breaking.

### 7. Ambiguity in input

Ordered-choice PEG DSLs where `a` shadows `ab` because `a` comes first in the grammar. Users hit subtle bugs that are hard to explain. See `parser-generators.md`.

### 8. No LSP / no formatter for external DSL

Shipping an external DSL in 2026 without a language server or formatter is a non-starter. Users expect autocomplete, go-to-definition, auto-formatting. Budget for this upfront.

---

## Checklist: Ship-Ready DSL

- [ ] Audience identified (developers / domain experts / both)
- [ ] Internal vs external decision justified
- [ ] Host embedding style chosen (fluent / template / s-expr / YAML / Ruby / Kotlin)
- [ ] Closed vocabulary enumerated
- [ ] Composition primitives identified
- [ ] Version field location decided
- [ ] Evolution policy documented (deprecation protocol, migration tool plan)
- [ ] Error messages reference DSL lexicon, not host
- [ ] For external DSL: formatter + LSP + syntax highlighter budgeted
- [ ] Anti-pattern check (not Turing-complete, not stringly-typed, no host-stack leakage)
- [ ] Three realistic example programs exist and read naturally
