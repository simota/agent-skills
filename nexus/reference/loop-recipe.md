# Loop Recipe — Loop-Engineering Dispatcher & Discipline Gate

> `/nexus loop <goal>` — the front-door for "make this a loop" requests. It does **not** run a loop itself: it classifies the loop's *shape*, gates the request against the **loop-engineering preconditions** (the load-bearing rules that separate a reliable loop from a runaway one), then **routes to the engine that owns execution** (`goal` / `converge` / `orbit` / `apex`). Nexus stays the routing/recipe layer; `orbit` is the execution substrate.

Read this file before executing `loop`. The concept, lineage, five anti-patterns, and applicability limits ("when NOT to loop") live in `orbit/reference/loop-engineering.md`; the pattern→primitive map in `reference/loop-engineering-primitives.md`; the maker/checker loop spec in `reference/evaluator-loop-protocol.md`. This recipe **cites** them rather than restating them.

---

## 1. Nature / When to Use / Boundaries

**`loop` is meta/control, not a task shape** (like `converge`). It is a dispatcher: its deliverable is a *correctly-shaped, discipline-gated loop handed to the right engine* — not code, and not a running loop.

Use `loop` when the user wants an agent loop but the **shape and discipline are underspecified** — "automate this with a loop", "run until done", "loop-engineer this", "keep iterating until X". `loop` pins the shape, enforces the preconditions, and delegates.

Route direct (skip `loop`) when the shape is already explicit:

| Already explicit | Go direct to |
|---|---|
| "set up `/goal`" / native single-session goal config | `goal` |
| "iterate to a rubric / quality bar", attended, now | `converge` |
| "generate / audit / recover a nexus-autoloop runner" | `orbit` (skill) |
| "discovery → ship one-shot" | `apex` |

Scale: **1 agent (inline classification + gate)** + the routed engine's range (§8).

---

## 2. The Loop-Engineering Precondition Gate (the value-add)

Before any loop is built, `loop` runs a five-point gate derived from the five loop-engineering moves (`orbit/reference/loop-engineering.md`). **Contract-level checkpoint; AUTORUN cannot skip** — a loop that fails a precondition is a loop that fails *silently and expensively*. Each failed precondition maps to a named anti-pattern; convert it (one focused question) or stop — never route an ungated loop.

| # | Precondition | Failed → anti-pattern | Resolution |
|---|---|---|---|
| 1 | **Verifiable completion oracle** — a command/predicate where exit 0 ⟺ done. Subjective goals ("improve the UX") are rejected. | **loopmaxxing** (no exit condition → infinite API spend) | Convert to a machine-checkable predicate (one question), or stop. Same gate as `goal` Phase 2.5. |
| 2 | **Hard-stop bound** — iteration cap / budget / timeout, enforced *externally* (never agent self-assessment). | **overbaking / runaway** (drift, bizarre scope creep) | Require a bound before launch. `loop ≤ N cycles (default N=3)` in-session; external cap for unattended. |
| 3 | **maker ≠ checker** — the generator does not grade its own work; an independent evaluator/critic decides DONE. | **nodding loop** (self-approval — the most common failure) | Independent evaluator (`converge` Evaluators / `orbit` `CRITIC_MODEL` / `/goal` fresh-model check). Spec: `reference/evaluator-loop-protocol.md`. |
| 4 | **Persistent memory** — state lives outside the conversation (files / DB / git), not in-context. | **amnesiac loop** (no cumulative progress) | filesystem-as-memory (`orbit` state files / `goal` repo state). |
| 5 | **Drift awareness** — accept that quality can decay across iterations even when tests pass (SlopCodeBench: structural erosion in 77% of trajectories). | silent quality erosion | Bound the loop (per #2) + read-a-sample discipline; surface as a run risk — never assert ROI as fact. |

The other two loop-engineering moves are satisfied structurally by the routed engine, not by this gate: **handoff/isolation** — `orbit` runs each iteration in a `git worktree`; **discovery** — the goal/skill supplies the per-turn work.

---

## 3. Phase Contract (AUTORUN chain template)

```
FRAME ── restate goal; classify loop SHAPE
         (native-goal | rubric-quality | unattended-runner | discovery-to-ship)
   ▼
GATE ─── the §2 five-point precondition gate   ★ contract-level; AUTORUN cannot skip
         any precondition unmet → one focused question to convert, else STOP
         (report best-so-far framing + the blocking precondition)
   ▼
ROUTE ── dispatch by SHAPE (§4). Confirm before launch for unattended orbit runs.
   ▼
(DELEGATE) ── the chosen engine owns execution, its own loop cap, and its own resume
   ▼
REPORT ── Loop Design Record + NEXUS_COMPLETE
```

The dispatcher runs inline (classification + gate); it spawns at most one helper (e.g. `Hone` to elicit the oracle, `Magi` to disambiguate shape) before delegating. **It never re-implements the routed engine.**

---

## 4. Routing Table (SHAPE → engine)

| Loop shape | Signals | Route to | Who owns the loop cap |
|---|---|---|---|
| **Native single-session goal** | "set up `/goal`"; one CLI session runs until a written condition holds | `goal` recipe | `/goal` fresh-model check + mandatory hard-stop |
| **In-session rubric quality loop** | attended; iterate one deliverable to a rubric bar *now* | `converge` recipe | `loop ≤ N cycles (default N=3)` |
| **Unattended autonomous runner** | "run until done" unattended, Ralph-style, resumable, recoverable | `orbit` skill | external iteration / budget / timeout cap |
| **Discovery → ship one-shot** | the "loop" is really a full build from discovery to launch | `apex` recipe | apex Phase 6 loop (Orbit-driven) |

Ambiguous between two shapes → ask one focused question (default toward the *less autonomous / more bounded* option).

---

## 5. recipe-contract elements (1-4)

- **Termination bound (element 1):** the dispatcher does not loop → **N/A for `loop` itself**; the **routed engine owns the cap** (converge `loop ≤ N cycles (default N=3)` · orbit external cap · goal mandatory hard-stop). The §2 gate *requires a bound to exist* before routing.
- **Confirm / safety gate (element 2):** §2 gate = **contract-level checkpoint; AUTORUN cannot skip**. Unattended `orbit` runs = **Confirm before launch**. L4 / destructive / 10+ files = **Ask First** (inherited).
- **Resume (element 3):** **N/A for the dispatcher** (single routing pass); resume is owned by the routed engine (orbit / converge checkpoint-resume · goal launch · apex checkpoint-resume).
- **Output report (element 4):** **Loop Design Record** — classified shape, the five-point gate verdict (each precondition: met / converted / blocking), chosen engine + rationale, and the handoff payload. On a STOP (failed gate) it reports which precondition blocked and the conversion needed.

---

## 6. Failure Modes Prevented

| Failure | Mitigation |
|---|---|
| **loopmaxxing** (subjective goal, no exit → infinite spend) | Gate #1 rejects unverifiable oracles |
| **nodding loop** (generator self-approves) | Gate #3 requires maker ≠ checker |
| **amnesiac loop** (no cumulative progress) | Gate #4 requires persistent memory |
| **overbaking / runaway** (drift, scope creep) | Gate #2 requires a hard-stop bound; Gate #5 drift awareness |
| **Wrong-engine routing** (e.g. an unattended need sent to attended `converge`) | §4 shape→engine table + one-question disambiguation |
| **Duplicating `orbit`** (re-implementing the runner at the nexus layer) | `loop` delegates execution; it never generates or runs loop scripts itself |
| **Ungated AUTORUN launch** | §2 gate is AUTORUN-cannot-skip; an unverifiable / unbounded loop never launches |

---

## 7. Boundaries — vs neighbors

- **vs `goal`:** `goal` configures a native `/goal` run (setup only, never runs). `loop` is upstream — it may *route to* `goal` when the shape is native-single-session. `goal` is **not** a runner; for an unattended runner `loop` routes to `orbit`, not `goal`.
- **vs `converge`:** `converge` *is* the in-session rubric Generator-Evaluator loop and runs it now. `loop` routes to `converge` for that shape. If the user already said "iterate to a rubric", go to `converge` direct.
- **vs `orbit` (skill):** `orbit` is the execution substrate (script generation, contracts, audit, recovery, Ralph). `loop` is the nexus routing front-door that hands unattended runs to `orbit`. They are layers, not competitors.
- **vs `apex`:** when the "loop" is really discovery→spec→build→ship, route to `apex` (which internally drives an Orbit loop at Phase 6).

```
Decision Tree
"make a loop / run until done / loop-engineer this"
  ├─ shape already explicit? → go direct (goal | converge | orbit | apex)
  └─ underspecified → loop
       GATE (oracle? bound? maker≠checker? memory? drift-aware?) — fail → convert or STOP
       ROUTE by shape:
         native /goal session ......... goal
         in-session rubric quality ..... converge
         unattended autonomous runner .. orbit   (Confirm before launch)
         discovery → ship .............. apex
```

---

## 8. Scale & Cost

- Dispatcher overhead: **1 agent (inline classification + gate)**, occasionally +1 (oracle elicitation / shape disambiguation). Negligible token cost.
- Total = dispatcher overhead **+ the routed engine's range** (goal 1-3 · converge 4-10 × cycles · orbit per-runner · apex 8-25).
- Suitable for `AUTORUN_FULL` *through the gate* — the gate's contract-level checkpoint still fires, and unattended `orbit` launches still confirm before launch.

---

## 9. Shared protocols (cite, don't re-derive)

| Protocol / reference | Owns | This recipe's use |
|---|---|---|
| `orbit/reference/loop-engineering.md` | concept, lineage, 5 anti-patterns, applicability ("when NOT to loop"), drift evidence | source of the §2 gate |
| `reference/loop-engineering-primitives.md` | pattern→primitive map (`/loop`, `/goal`, worktree, subagents, memory) | which primitive each move binds to |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, single termination oracle | the maker ≠ checker check (#3) + `converge` routing |
| `reference/goal-recipe.md` · `reference/converge-recipe.md` · `orbit/SKILL.md` · `reference/apex-recipe.md` | the routing targets | ROUTE delegation |
