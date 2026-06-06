# AI-Era Coding Patterns

Purpose: load this when planning or reviewing implementation work in an AI-assisted coding context. Consolidates the 2026 patterns that complement classic SOLID/DRY/KISS/YAGNI — anchored on Anthropic's Claude Code best practices and the cross-skill research distilled across `builder`, `zen`, `radar`, `judge`, and `sherpa`.

## Contents

1. The six load-bearing principles
2. Verification-first (Anthropic "highest-leverage")
3. Make illegal states unrepresentable
4. Parse, don't validate
5. Result / Either over throws
6. Functional core, imperative shell
7. Branded / nominal types
8. Vertical slice architecture
9. Locality of behaviour
10. Explore → Plan → Implement → Commit cycle
11. Slopsquat awareness
12. AI-session smells

## 1. The Six Load-Bearing Principles

These six are the practical 2026 baseline for AI-assisted implementation. Apply them in order; later principles assume the earlier ones hold.

| # | Principle | What it gives the AI agent |
|---|-----------|----------------------------|
| 1 | Verification-first | A deterministic success signal before code is written |
| 2 | Make illegal states unrepresentable | Spec → type checker, exhaustiveness as a free invariant |
| 3 | Parse, don't validate | Single boundary transform from `unknown` to a typed value |
| 4 | Result / Either over throws | Error path in the type system, smaller catch surface |
| 5 | Functional core / imperative shell | A deterministic core the agent can write under PBT |
| 6 | Vertical slice architecture | Feature-sized changes fit one context window |

Layer on Branded Types (per-field nominal guarantees), Locality of Behaviour (co-locate behaviour with its trigger), and Explore → Plan → Implement → Commit (Anthropic's workflow contract) for full coverage.

## 2. Verification-first

> "The single highest-leverage thing you can give an AI coding agent." — Anthropic Claude Code best practices

Lock the verifier *before* implementation. Acceptable verifiers, in descending order of strength:

1. A failing test that reproduces the requirement (executable spec)
2. A screenshot diff target (UI flows)
3. An expected stdout / fixture file (CLI tools)
4. A type signature (when the type is precise enough to encode the requirement)
5. A schema contract (OpenAPI, JSON Schema, Protobuf)

Anti-pattern: "I'll write the code, then add tests." The verifier authored after the implementation inherits the implementation's blind spots and trends toward tautology. See `radar`'s Tautological Test 6-pattern catalog.

Source: code.claude.com/docs/en/best-practices.

## 3. Make Illegal States Unrepresentable

Yaron Minsky's rule: encode invariants in the type system, not in runtime checks. Prefer discriminated unions over boolean flag soup.

```ts
// Wrong: invalid combinations are possible
type Order = {
  state: "draft" | "submitted" | "shipped";
  items?: Item[];
  submittedAt?: Date;
  trackingNumber?: string;
};

// Right: each state carries exactly the fields it needs
type Order =
  | { state: "draft"; items: Item[] }
  | { state: "submitted"; items: NonEmptyArray<Item>; submittedAt: Date }
  | { state: "shipped"; items: NonEmptyArray<Item>; submittedAt: Date; trackingNumber: string };
```

The compiler enforces the spec; exhaustiveness checks (`never` in TypeScript, exhaustive `match` in Rust) catch missing branches. AI codegen self-detects missing branches via exhaustiveness, not by re-reading the spec.

Source: deviq.com/principles/make-illegal-states-unrepresentable/.

## 4. Parse, Don't Validate

Alexis King's rule: at every system boundary, transform `unknown` into a fully-typed value with a single one-way function. Downstream code receives the parsed type and never repeats boundary checks.

```ts
// Wrong: validation that does not narrow the type
function handleOrder(input: unknown) {
  if (!isOrder(input)) throw new Error("invalid");
  // input is still `unknown` — downstream code must check again
}

// Right: parsing that narrows the type
const Order = z.object({ id: z.string().brand<"OrderId">(), items: z.array(Item).min(1) });
function handleOrder(input: unknown) {
  const order = Order.parse(input);  // order: { id: OrderId; items: Item[] }
  // downstream code consumes `order` with full type information
}
```

Recommended 2026 parsers (alphabetical): ArkType, Effect Schema, Valibot, Zod v4. All four support brand types and JSON Schema export.

Source: lexi-lambda.github.io/blogs/2019-11-05-parse-don-t-validate/.

## 5. Result / Either over Throws

Scott Wlaschin's Railway-Oriented Programming: return `Result<T, E>` rather than throw across module boundaries. Reserve throws for non-recoverable invariant violations.

```ts
import { Result, ok, err } from "neverthrow";

function chargeCard(amount: Money): Result<Receipt, ChargeError> {
  if (amount.value <= 0) return err({ kind: "INVALID_AMOUNT" });
  const result = paymentGateway.charge(amount);
  if (!result.ok) return err({ kind: "GATEWAY_FAILED", cause: result.error });
  return ok(result.value);
}
```

Why this matters for AI codegen: when errors are values, the type system forces every caller to handle them, and AI's reflex to wrap everything in `try/catch` is naturally constrained. Effect-TS extends the pattern to effects (concurrency, retries, DI); `neverthrow` keeps it to errors alone.

Source: fsharpforfunandprofit.com/rop/.

## 6. Functional Core, Imperative Shell

Gary Bernhardt's "Boundaries" pattern: pure, deterministic domain logic in the core (no I/O, no clocks, no random); side effects (HTTP, DB, filesystem, time) wrapped in a thin shell at the edges.

```
┌──────────────────────────── shell ────────────────────────────┐
│  HTTP handler  →  parses request, calls core, writes response │
│                                                               │
│         ┌────────────── core (pure) ──────────────┐           │
│         │  pricing rules, state transitions,      │           │
│         │  validation, calculation                │           │
│         └─────────────────────────────────────────┘           │
│                                                               │
│  DB adapter  →  reads/writes via repository interface         │
└───────────────────────────────────────────────────────────────┘
```

The core is the part you let the agent write and verify with property-based tests; the shell is the part a human reviews line by line.

Source: destroyallsoftware.com/talks/boundaries.

## 7. Branded / Nominal Types

```ts
type UserId = string & { __brand: "UserId" };
type OrderId = string & { __brand: "OrderId" };

declare function getUser(id: UserId): User;
declare function getOrder(id: OrderId): Order;

const userId = "abc-123" as UserId;
const orderId = "xyz-789" as OrderId;

getUser(orderId);  // type error — the right kind of `string`, wrong brand
```

Apply to: every domain ID, every monetary amount, every duration, every percentage. Zero runtime cost; eliminates the entire "wrong-string-passed-as-the-right-type" failure class. Zod v4: `z.string().brand<"UserId">()`. Valibot: `brand(string(), "UserId")`. Effect Schema: `Schema.String.pipe(Schema.brand("UserId"))`.

Source: learningtypescript.com/articles/branded-types.

## 8. Vertical Slice Architecture

Organise by feature, not by layer. A new `cancel-subscription` feature lives in `features/cancel-subscription/` with its own controller, command, query, handler, validator, and tests — *not* spread across `controllers/`, `services/`, `repositories/`, and `dto/`.

```
features/
  cancel-subscription/
    handler.ts
    command.ts
    validator.ts
    handler.test.ts
  upgrade-plan/
    handler.ts
    query.ts
    handler.test.ts
```

Reserve Hexagonal / Clean / Onion for stable cross-feature boundaries (auth, persistence, billing-gateway). Layer-per-folder is the canonical over-engineering pattern that AI codegen amplifies — a single feature edit hits 6 files and the agent context window has to span all of them. A vertical slice fits one context window and is independently testable.

Source: jimmybogard.com/vertical-slice-architecture; milanjovanovic.tech/blog/vertical-slice-architecture.

## 9. Locality of Behaviour

Behaviour is co-located with its trigger. A single file beats a 3-file (component + hook + service) split for AI and human comprehension, especially when the duplicate count is `< 3`.

Canonical examples:
- HTMX `hx-*` attributes (the `<button>` declares its own AJAX behaviour)
- Phoenix LiveView (template + handler in the same module)
- React: hook + JSX + Tailwind classes in one file rather than across folders

Trade-off: LoB is at tension with DRY. The rule of thumb is **Rule of Three** (Section 8 of `zen`): first duplicate fine, second yellow, only third triggers extraction. Early abstractions cost more than DRY violations because they encode a wrong concept across multiple call sites.

Source: htmx.org/essays/locality-of-behaviour/.

## 10. Explore → Plan → Implement → Commit Cycle

Anthropic's official workflow contract. Each step has a distinct deliverable and forbidden actions:

| Phase | Allowed | Forbidden |
|-------|---------|-----------|
| Explore | Read code, map symbols, load context | Write code, write spec, write tests |
| Plan | Write a plan artefact (diff sketch, AC list, test stubs) | Write production code |
| Implement | Write code against the locked plan | Re-open scope, change the plan |
| Commit | Run the verifier, produce commit/PR | Skip the verifier, edit tests post-hoc |

Skip Plan only when the change is mechanically obvious (single-file rename, dependency bump). Forcing Plan-mode for cross-file work catches half the failure surface before code is written.

Source: code.claude.com/docs/en/best-practices.

## 11. Slopsquat Awareness

Every AI-suggested `import` / `require` / `use` line is a supply-chain risk. Hallucination rates: 5-21% (Python 5.2%, open-source models 21.7%, Snyk study 19.7% across 576,000 samples). Attackers register the typo-squatted equivalents — the `huggingface-cli` impostor saw 30,000 downloads in 3 months.

Before adding any AI-suggested package:

1. Query the registry's existence endpoint (PyPI JSON API / npm registry / crates.io / RubyGems / Go module proxy).
2. Check publish date and download count.
3. Reject packages with `< 50` total downloads, `< 30 days` since first publish, or names within Levenshtein-2 of a well-known package without explicit confirmation.

Detection at multiple layers:
- `builder` rejects on AI suggestion before commit
- `chain` audits on bundled-artifact intake
- `sentinel` runs registry-side verification on PR

Source: arxiv.org/html/2512.05239v1; snyk.io — Slopsquatting mitigation; trendmicro.com — Slopsquatting.

## 12. AI-Session Smells

Five canonical patterns from Anthropic's "Common failure patterns" — distinct from human code smells. Each maps to a specific fix path.

| Smell | Symptom | Fix |
|-------|---------|-----|
| Kitchen-sink session | One prompt asked for 3 unrelated things, all half-done | Re-scope, then run them as 3 sessions |
| Correcting over and over | Repeated micro-corrections instead of a re-spec | Stop, re-spec, restart |
| Over-specified CLAUDE.md | Project memory > 200 lines, important rules buried | Move hard rules to hooks, content to skills (progressive disclosure) |
| Trust-then-verify gap | User accepted output without running the verifier | Verification-first gate; never accept without verifier evidence |
| Infinite exploration | Agent kept reading without ever moving to plan/implement | Force Plan-mode gate after N exploration steps |

Source: code.claude.com/docs/en/best-practices — Common failure patterns.

## Where Each Principle Is Enforced

| Principle | Enforced in |
|-----------|-------------|
| Verification-first | `radar` (verifier ownership) / `judge` (gates DONE on verifier evidence) / `builder` (refuses to ship without verifier) |
| Make illegal states unrepresentable | `builder` Core Contract / `schema` ID modelling |
| Parse, don't validate | `builder` boundary patterns / `schema` validation strategy |
| Result / Either | `builder` error strategy / `zen` refactor target |
| Functional core / shell | `builder` Hexagonal section / `atlas` structure evaluation |
| Branded types | `builder` type design / `artisan` props/state |
| Vertical slice | `builder` / `atlas` |
| Locality of behaviour | `zen` review observation / `artisan` component design |
| Explore-Plan-Implement-Commit | `sherpa` decomposition / `forge` plan-skip judgement |
| Slopsquat | `builder` / `chain` / `sentinel` |
| AI-session smells | `zen` review observation / `void` (YAGNI) |
