# Code Quality Contract (Master Reference)

Centralized quality bar for every skill that **writes or modifies code**. Seven axes, each with checkable rules, one canonical anti-pattern, and a citable source. Individual SKILL.md files reference this document instead of restating quality principles.

Consumers: all agents whose `Writes Code` value in `_common/BOUNDARIES.md` is `Yes`, `Fixes only`, `Partial`, or scoped-`Yes`.

**Precedence.** Project conventions (repo lint/format config, existing patterns, CLAUDE.md) win over this file — *except* the `SEC` axis, which is a floor and is never relaxed to match an existing insecure pattern. When this file and a skill's own reference disagree, the skill's domain reference wins for domain mechanics; this file wins for the quality bar.

**Proportionality.** A one-line fix does not need a seven-axis audit. Apply the axes whose surface the change actually touches, and report the rest as `n/a` in the Gate. Padding a trivial change with ceremony is itself a quality defect.

---

## Why This Exists (measured evidence)

| Finding | Number | Source |
|---|---|---|
| AI-generated code introducing a security vulnerability (80 tasks × 100+ LLMs) | **45%** of tasks failed security checks; Java worst at ~72% | [Veracode 2025 GenAI Code Security Report](https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/) |
| Duplicated code blocks per million changed lines | 40.3 (2023) → **73.0** (record high); 2024 was the first year copy/paste exceeded moved (refactored) code | [GitClear — AI Copilot Code Quality 2025](https://www.gitclear.com/ai_assistant_code_quality_2025_research), [The Maintainability Gap (2026)](https://www.gitclear.com/the_ai_code_quality_maintainability_gap) |
| Newly added code revised within two weeks (rework rate) | 5.5% (2020) → **7.9%** (2024) | [GitClear 2025](https://www.gitclear.com/ai_assistant_code_quality_2025_research) |
| Security degradation across iterative AI refinement rounds | Vulnerabilities accumulate as the model iterates on its own output | [arXiv 2506.11022 — Security Degradation in Iterative AI Code Generation](https://arxiv.org/pdf/2506.11022) |

Read: the dominant AI-codegen failure modes are **insecure defaults** and **duplication instead of abstraction** — so `SEC` and `MNT` carry the highest weight in the Gate below.

---

## 1. `SLD` — Solid (structural soundness)

- **SLD-1 — Single reason to change.** One module owns one responsibility. Business logic never sits in the same unit as infrastructure (HTTP, DB, filesystem, clock).
- **SLD-2 — Depend on abstractions at boundaries only.** Inject collaborators that cross a process/IO boundary. Do *not* introduce an interface for a type with exactly one implementation and no boundary — that is speculative generality (`DISP-002`).
- **SLD-3 — Small, context-specific contracts.** A consumer must not be forced to know about methods it never calls. Prefer several narrow ports over one wide service interface.
- **SLD-4 — Judge the result by CUPID properties, not by rule-compliance.** Composable · Unix philosophy (does one thing well) · Predictable · Idiomatic · Domain-based. SOLID describes the *process*; CUPID describes the *finished code*. If a change satisfies SOLID on paper but the result is not predictable or idiomatic, the change failed.

**Anti-pattern — interface-per-class ceremony:**
```ts
// before: DIP applied mechanically — one impl, no boundary, no seam of value
interface IUserMapper { toDto(u: User): UserDto }
class UserMapper implements IUserMapper { toDto(u: User) { /* ... */ } }

// after: plain function; the abstraction goes where a boundary really exists
export const toUserDto = (u: User): UserDto => ({ /* ... */ })
interface UserRepository { findById(id: UserId): Promise<User | null> }  // real IO boundary
```

Sources: [Dan North — CUPID: for joyful coding](https://dannorth.net/cupid-for-joyful-coding/) · [Google eng-practices — What to look for in a code review § Complexity / over-engineering](https://google.github.io/eng-practices/review/reviewer/looking-for.html) · `builder/reference/architecture-patterns.md` § 2 (SOLID 2025 interpretation + CUPID table).

---

## 2. `SEC` — Secure (hard floor — never traded away)

- **SEC-1 — Authorization is checked server-side on every request, per object.** Broken Access Control is `A01:2025`, the #1 risk; SSRF is now folded into it. Never rely on a hidden UI control, a client-supplied role, or a URL that "nobody knows".
- **SEC-2 — No string-built queries, commands, paths, or markup.** Parameterized queries / prepared statements, argv-array process spawning, allow-listed path joins, context-aware output encoding. XSS (`CWE-79`) is the #1 weakness and SQLi (`CWE-89`) #2 in the 2025 CWE Top 25.
- **SEC-3 — Parse untrusted input at the boundary into a typed value; never re-validate downstream.** Reject by allow-list, bound every collection and payload size (`CWE-770`, new to the 2025 Top 25).
- **SEC-4 — No secrets, keys, tokens, or credentials in source, logs, error messages, or fixtures.** Read from the environment/secret manager. Log the fact of a failure, never the secret or the raw payload.
- **SEC-5 — Handle the exceptional path explicitly.** `A10:2025 Mishandling of Exceptional Conditions` is new for 2025: an empty `catch`, a swallowed error, or a failure path that falls through to the success branch is a security defect, not a style issue.
- **SEC-6 — Secure defaults.** Deny by default, least privilege, no debug/verbose mode on by default, dependencies pinned and provenance-checked (`A03:2025 Software Supply Chain Failures`).

**Anti-pattern — the two most common AI-codegen failures in one function:**
```ts
// before: A05 Injection + A01 missing authorization + A10 swallowed error
app.get("/orders/:id", async (req, res) => {
  try {
    const r = await db.query(`SELECT * FROM orders WHERE id = '${req.params.id}'`)
    res.json(r.rows[0])
  } catch { res.json({}) }                      // failure looks like success
})

// after
app.get("/orders/:id", requireAuth, async (req, res) => {
  const id = OrderId.safeParse(req.params.id)
  if (!id.success) return res.status(400).json({ error: "invalid_id" })
  const order = await db.query("SELECT * FROM orders WHERE id = $1", [id.data])  // parameterized
  if (!order.rows[0]) return res.status(404).json({ error: "not_found" })
  if (order.rows[0].userId !== req.user.id) return res.status(404).json({ error: "not_found" })  // per-object authz
  res.json(toOrderDto(order.rows[0]))
})
```

Sources: [OWASP Top 10:2025](https://owasp.org/Top10/2025/0x00_2025-Introduction/) · [2025 CWE Top 25 (CISA/MITRE)](https://www.cisa.gov/news-events/alerts/2025/12/11/2025-cwe-top-25-most-dangerous-software-weaknesses) · [CWE-1435 — 2025 Top 25 member list](https://cwe.mitre.org/data/definitions/1435.html).
Deeper application-security review is `sentinel`'s scope; skill supply-chain trust is `_common/SECURITY.md` (a different concern — do not conflate).

---

## 3. `RDB` — Readable

- **RDB-1 — Names are as long as needed to be unambiguous, and no longer.** Google's bar: "long enough to fully communicate what the item is or does, without being so long that it becomes hard to read."
- **RDB-2 — A reader must understand the unit without scrolling or jumping.** If a function needs a paragraph of explanation, split it. Co-locate behavior with its trigger.
- **RDB-3 — Comments explain *why*, never *what*.** A comment restating the code is a smell (`DISP-003`); the fix is a better name, not a better comment.
- **RDB-4 — Boring beats clever.** Explicit control flow over dense one-liners; no metaprogramming or dynamic dispatch unless explicitness is provably worse.

**Anti-pattern:**
```ts
// before
const p = (d: any[]) => d.filter(x => x.s === 1 && x.t > Date.now() - 864e5).map(x => x.v)
// after
const MILLIS_PER_DAY = 86_400_000
const activeValuesFromLastDay = (records: Record[]): Value[] =>
  records
    .filter(r => r.status === Status.Active && r.updatedAt > Date.now() - MILLIS_PER_DAY)
    .map(r => r.value)
```

Sources: [Google eng-practices — What to look for § Naming / Comments / Complexity](https://google.github.io/eng-practices/review/reviewer/looking-for.html) · full smell taxonomy → `_common/CODE_SMELL_CATALOG.md`.

---

## 4. `MNT` — Maintainable (highest-risk axis for AI codegen)

- **MNT-1 — Never paste a third copy.** Two similar blocks may coexist; the third is an extraction. This is the single most-measured AI-codegen regression — block duplication is at a record high and cloned blocks carry 15-50% more defects.
- **MNT-2 — Before writing new code, search for the existing implementation.** The default AI failure is to re-implement a helper that already exists two directories away. Grep first; extend the existing one.
- **MNT-3 — One consistent style per concern per repo.** Error handling, async style, imports, naming — pick the repo's existing convention, do not introduce a second one. Taxonomy → `_common/CONSISTENCY_FRAMEWORK.md`.
- **MNT-4 — Solve today's problem.** No configuration knob, no plugin layer, no generic abstraction for a requirement nobody has stated (`DISP-002` Speculative Generality; Google explicitly instructs reviewers to be "especially vigilant about over-engineering").
- **MNT-5 — Leave the change surface consistent.** Update callers, types, configs, tests, and docs touched by the change; do not leave a half-migrated pattern behind.

Sources: [GitClear — The Maintainability Gap](https://www.gitclear.com/the_ai_code_quality_maintainability_gap) · [Google eng-practices](https://google.github.io/eng-practices/review/reviewer/looking-for.html) · `_common/CODE_SMELL_CATALOG.md` (`DISP-004` Duplicate Code, `DISP-002` Speculative Generality).

---

## 5. `TST` — Testable

- **TST-1 — Identify the verification path before writing the implementation.** Tests, type signature, schema contract, expected output — the verifier comes first. Code with no verifier is a draft, not a deliverable.
- **TST-2 — Keep the domain pure and push IO to the edges.** Anything requiring a clock, a network, a random source, or global mutable state to test is a design defect, not a testing problem. Inject them.
- **TST-3 — Weight the suite as a pyramid.** Many fast unit tests, fewer service/integration tests, fewest E2E. Fowler's caution applies literally: E2E tests are slow and brittle, so the top of the pyramid stays small.
- **TST-4 — Test behavior at the public contract, not private internals.** A test that breaks on a rename with no behavior change is a maintenance tax.
- **TST-5 — Every bug fix ships a test that fails before the fix.** No red-first evidence, no fix.

**Anti-pattern:**
```ts
// before: untestable — hidden clock + hidden IO
async function expireSessions() {
  const all = await db.sessions.findAll()
  return all.filter(s => s.expiresAt < new Date())   // cannot test without mocking global time
}
// after: pure core, imperative shell
export const selectExpired = (sessions: Session[], now: Date): Session[] =>
  sessions.filter(s => s.expiresAt < now)            // trivially testable, no mocks
async function expireSessions(clock: Clock, repo: SessionRepo) {
  return selectExpired(await repo.findAll(), clock.now())
}
```

Sources: [Martin Fowler — The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) · [Google eng-practices § Tests](https://google.github.io/eng-practices/review/reviewer/looking-for.html). Test-suite depth and flake repair are `radar`'s scope; test smells → `_common/CODE_SMELL_CATALOG.md` § 7.

---

## 6. `PRF` — Performant

- **PRF-1 — Measure before optimizing, and state the number.** "Faster" without a before/after measurement is not a performance change. Where a resource is implicated, interrogate it as Utilization / Saturation / Errors (USE).
- **PRF-2 — Fix algorithmic and IO-shape problems first.** N+1 queries, unbounded fetches, missing indexes, and O(n²) over a growing collection dominate micro-optimizations by orders of magnitude. Micro-tuning a hot loop while an N+1 sits above it is wasted work.
- **PRF-3 — Bound everything that can grow.** Pagination, `LIMIT`, timeouts, retry caps, connection-pool sizes, request body size. Unbounded resource allocation is simultaneously a `PRF` and a `SEC` defect (`CWE-770`).
- **PRF-4 — Do not trade `RDB`/`MNT` for unmeasured speed.** Optimization that obscures intent requires a recorded benchmark justifying it.

**Anti-pattern — N+1:**
```ts
// before: 1 + N queries
const orders = await repo.findByUser(userId)
for (const o of orders) o.items = await repo.findItems(o.id)
// after: 2 queries, bounded
const orders = await repo.findByUser(userId, { limit: PAGE_SIZE })
const items = await repo.findItemsByOrderIds(orders.map(o => o.id))   // single IN (...) query
```

Sources: [Brendan Gregg — The USE Method](https://www.brendangregg.com/usemethod.html) · [AWS Well-Architected — Performance Efficiency pillar](https://aws.amazon.com/architecture/well-architected/). Query-plan work is `tuner`; runtime profiling and tuning loops are `bolt`.

---

## 7. `SCL` — Scalable

- **SCL-1 — Keep processes stateless.** Session and request state lives in an external store, never in instance memory. Stateless services scale horizontally with low overhead; sticky in-process state is the classic scale-out blocker.
- **SCL-2 — Scale horizontally, not by growing one instance.** Prefer many small units over one large one; assume any instance can vanish mid-request.
- **SCL-3 — Assume failure and design the recovery path.** Timeouts, bounded retries with jittered backoff, idempotency keys on anything retryable, circuit breakers on outbound dependencies.
- **SCL-4 — Config from the environment; no environment-specific branches in code.** No `if (env === "prod")` logic paths.
- **SCL-5 — Make the system observable at the seam you just added.** A new boundary with no structured log, metric, or trace cannot be operated. Design → `beacon`.

**Anti-pattern:**
```ts
// before: in-process state — breaks the moment a second instance exists
const rateLimits = new Map<string, number>()
// after: shared store + explicit bound + idempotency
await redis.incrWithExpiry(`rl:${userId}`, WINDOW_SECONDS)
```

Sources: [AWS Well-Architected — Reliability pillar design principles (scale horizontally, automatically recover from failure)](https://aws.amazon.com/architecture/well-architected/) · [AWS Well-Architected — Horizontal scaling concept](https://wa.aws.amazon.com/wellarchitected/2020-07-02T19-33-23/wat.concept.horizontal-scaling.en.html) · [The Twelve-Factor App § VI Processes / § VIII Concurrency](https://12factor.net/processes). Multi-tenant isolation is `shard`; SLO/observability design is `beacon`.

---

## Delegation Map (do not duplicate these here)

| Concern | Owner |
|---|---|
| Smell taxonomy, IDs, severity hints | `_common/CODE_SMELL_CATALOG.md` |
| Consistency axes + severity rubric | `_common/CONSISTENCY_FRAMEWORK.md` |
| Skill/plugin supply-chain trust | `_common/SECURITY.md` (**not** application security) |
| SOLID 2025 interpretation + CUPID table | `builder/reference/architecture-patterns.md` § 2 |
| Application-security review depth | `sentinel` · runtime validation `probe` |
| Test depth, flake repair, coverage | `radar` · resilience/load `siege` |
| Query plans / indexes | `tuner` · runtime profiling `bolt` |
| Impact-scope check before declaring done | `builder` 5-axis check · pre-change `ripple` |

---

## Code Quality Gate (`CQG`)

Any skill that wrote or modified code emits this before declaring done. One line per axis; `n/a` is a valid verdict with a reason, silence is not.

```
CODE_QUALITY_GATE:
  SLD: pass | risk | n/a — <one line>
  SEC: pass | risk | n/a — <one line; `risk` on SEC blocks completion>
  RDB: pass | risk | n/a — <one line>
  MNT: pass | risk | n/a — <duplication checked? existing impl searched?>
  TST: pass | risk | n/a — <verifier that was run, and its result>
  PRF: pass | risk | n/a — <measurement, or why unmeasured is acceptable>
  SCL: pass | risk | n/a — <one line>
  Deferred: <items consciously left, with reason> | none
```

**Blocking rule.** `SEC: risk` blocks completion — fix it or escalate to the user; it is never silently deferred. Every other axis may be `risk` if the reason is stated and the item appears under `Deferred`. Claims must be evidence-bound: `TST: pass` requires a test command that actually ran, and `PRF: pass` requires a number.
