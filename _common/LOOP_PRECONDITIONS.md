# Loop Preconditions — the five-point gate every agent loop passes before it runs

> **Tier:** `orchestration` — activates from the hub, a recipe, or on engine detection. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

**Purpose:** The load-bearing rules that separate a reliable agent loop from a runaway one. Any recipe or skill that is about to **build, configure, or launch a loop** runs this gate first. A loop that fails a precondition is a loop that fails *silently and expensively* — the failure surfaces as burned budget, not as an error.

**Read when:** you are about to set up `/goal`, run a `converge` cycle, generate an `orbit` runner, enter an `apex` implementation loop, or wire any other iterate-until-done mechanism.

**Provenance:** derived from the five loop-engineering moves in `.claude/skills/orbit/reference/loop-engineering.md` (concept, lineage, five anti-patterns, and "when NOT to loop" live there). The pattern → primitive map is `nexus/reference/loop-engineering-primitives.md`; the maker/checker spec is `nexus/reference/evaluator-loop-protocol.md`. This file **cites** them rather than restating them.

---

## The gate

**Contract-level checkpoint; AUTORUN cannot skip.** Each failed precondition maps to a named anti-pattern. Convert it with one focused question, or stop — **never launch an ungated loop**.

| # | Precondition | Failed → anti-pattern | Resolution |
|---|---|---|---|
| 1 | **Verifiable completion oracle** — a command or predicate where exit 0 ⟺ done. Subjective goals ("improve the UX") are rejected. | **loopmaxxing** (no exit condition → unbounded API spend) | Try the conversions below **before** rejecting; stop only when none applies. |
| 2 | **Hard-stop bound** — iteration cap / budget / timeout, enforced **externally**, never by agent self-assessment. | **overbaking / runaway** (drift, bizarre scope creep) | Require a bound before launch: `loop ≤ N cycles (default N=3)` in-session; an external cap for unattended runs. |
| 3 | **maker ≠ checker** — the generator does not grade its own work; an independent evaluator decides DONE. | **nodding loop** (self-approval — the most common failure) | Independent evaluator per `nexus/reference/evaluator-loop-protocol.md` (`converge` Evaluators / `orbit` `CRITIC_MODEL` / `/goal` fresh-model check). |
| 4 | **Persistent memory** — state lives outside the conversation (files / DB / git), not in context. | **amnesiac loop** (no cumulative progress) | Filesystem-as-memory: `orbit` state files, `/goal` repo state. |
| 5 | **Drift awareness** — quality can decay across iterations *even when tests keep passing* (SlopCodeBench: structural erosion in 77% of trajectories). | silent quality erosion | Bound the loop (#2) + read-a-sample discipline. Surface as a run risk — **never assert ROI as fact**. |

### Converting #1 — when the goal is real and only the predicate is missing

Rejection is the wrong default for work that matters but has no obvious exit test, because it
leaves the gate able to handle only the goals that were already easy. A subjective goal is
usually one substitution away from a checkable one: keep the goal, and move the oracle **off the
artifact and onto something countable derived from it**.

| Conversion | Substitute | Checkable because | Used by |
|---|---|---|---|
| **Split oracle** | "the design is good" → "an independent reviewer's open findings reach zero" | the count is observed rather than judged, and the judge is not the maker | `burnish` · `quell` · `newsroom`, on `_common/FINDING_LEDGER.md` |
| **Frontier exhaustion** | "the plan is sound" → "no unanswered question remains whose prerequisites are settled" | the questions form a dependency-ordered set; termination is an empty frontier, and the coverage stays inspectable afterwards | interrogation-shaped work — hardening a plan, design, or decision before it is built |
| **Coverage set** | "we have tested enough" → "every cell of the declared axis set is visited" | the axes are declared before cycle 1, so the denominator cannot move | `matrix` |
| **Differential parity** | "it faithfully reproduces the original" → "the diff against the reference is empty on the declared dimensions" | a diff is computed, not assessed | `_common/DIFFERENTIAL_PARITY.md` |

**Frontier exhaustion has a shape worth naming**, because it is the conversion that fits work with
no artifact yet. Enumerate the open questions, order them by which decisions block which, and ask
**the whole frontier each round** — every question whose prerequisites are already settled. Depth
of the dependency graph then sets the number of rounds, not the count of unknowns; asking one
question per turn re-creates an unbounded loop out of a bounded one. Done is an empty frontier:
every branch visited, nothing left silently assumed.

**The denominator is frozen before cycle 1.** A conversion whose question set, axis list, or
reference can grow mid-loop has rebuilt the unbounded goal under a countable name — the `HD-GAME`
shape, where the metric moved and the property did not. Additions are permitted only as a recorded
scope change that restarts the count, never as a silent extension.

**When nothing converts.** Some goals resist every substitution because the missing input is
experience rather than analysis — "how should this feel?" cannot be settled by discussion at any
depth. Do not loop on them and do not merely refuse: **lower the action tier instead** — build the
throwaway version, run the dry run, produce the one sample — and re-enter the gate carrying the
evidence that was missing (`nexus/reference/autonomy-quality-protocol.md` Q24). That exit is
typed, not a failure, and it is the only honest way past a question analysis cannot reach.

Two further loop-engineering moves are satisfied **structurally by the executing engine**, not by this gate:

- **handoff / isolation** — `orbit` runs each iteration in its own `git worktree`.
- **discovery** — the goal or skill supplies the per-turn work.

## Who runs it, and when

The gate belongs to whoever is closest to launching the loop. Each owner runs it **before** its own setup work, so a loop cannot reach an engine ungated regardless of which door the request came through:

| Owner | Runs the gate at | Notes |
|-------|------------------|-------|
| `nexus goal` | before emitting a launch command | #1 and #2 are already `goal`'s own delivery gate — it **rejects unverifiable goals and unbounded launches** outright. Running this file's gate is the same check, stated once. |
| `nexus converge` | before cycle 1 | #3 is structural (Generator-Evaluator separation); #2 is `max_cycles`. |
| `nexus quell` / `nexus burnish` / `nexus newsroom` | before cycle 1 | #3 is structural (an evaluator independent of the producer + disposition integrity); #4 is the ledger file. All three run on `_common/FINDING_LEDGER.md`, which owns that machinery. `burnish` reports #1 as **converted** — its split oracle is what makes an unverifiable "improve the design" machine-checkable. |
| `nexus apex` | before the implementation loop | #2 is the declared per-loop cap. |
| `orbit` (skill) | before generating a runner | #4 is structural (state files); #5 is the audit discipline. |
| Any other loop-building step | before launch | If no owner above applies, the orchestrating agent runs it inline. |

**Shape first, then gate.** When the user's request does not yet name a loop shape ("automate this with a loop", "run until done", "keep iterating until X"), classify the shape before gating — the shape decides which owner runs it:

| Shape | Signal | Owner |
|-------|--------|-------|
| native single-session goal | "set up `/goal`", unattended single session | `nexus goal` |
| in-session rubric quality loop | attended; iterate one deliverable to a bar *now* | `nexus converge` |
| external-reviewer-to-zero loop | attended; drive a code diff (`quell`), a rendered UI surface (`burnish`), or an article's factual claims (`newsroom`) to a clean independent evaluation | `nexus quell` / `nexus burnish` / `nexus newsroom` |
| unattended runner | long-running, needs scripts / contracts / recovery | `orbit` (skill) |
| discovery → ship one-shot | full feature lifecycle | `nexus apex` |

## Reporting

Whoever runs the gate reports its verdict in its own output — per precondition: **met** / **converted** / **blocking**. A `converted` verdict on #1 names which conversion was used and what the frozen denominator is (the question set, the axis list, the reference, or the reviewer); "converted" without both is not a verdict, because nothing downstream can tell whether the count can still move. On a blocking verdict the run **stops and names the precondition**; it never proceeds with a partial gate or silently downgrades the loop to a single pass.
