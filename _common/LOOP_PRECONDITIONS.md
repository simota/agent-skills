# Loop Preconditions — the five-point gate every agent loop passes before it runs

**Purpose:** The load-bearing rules that separate a reliable agent loop from a runaway one. Any recipe or skill that is about to **build, configure, or launch a loop** runs this gate first. A loop that fails a precondition is a loop that fails *silently and expensively* — the failure surfaces as burned budget, not as an error.

**Read when:** you are about to set up `/goal`, run a `converge` cycle, generate an `orbit` runner, enter an `apex` implementation loop, or wire any other iterate-until-done mechanism.

**Provenance:** derived from the five loop-engineering moves in `orbit/reference/loop-engineering.md` (concept, lineage, five anti-patterns, and "when NOT to loop" live there). The pattern → primitive map is `nexus/reference/loop-engineering-primitives.md`; the maker/checker spec is `nexus/reference/evaluator-loop-protocol.md`. This file **cites** them rather than restating them.

---

## The gate

**Contract-level checkpoint; AUTORUN cannot skip.** Each failed precondition maps to a named anti-pattern. Convert it with one focused question, or stop — **never launch an ungated loop**.

| # | Precondition | Failed → anti-pattern | Resolution |
|---|---|---|---|
| 1 | **Verifiable completion oracle** — a command or predicate where exit 0 ⟺ done. Subjective goals ("improve the UX") are rejected. | **loopmaxxing** (no exit condition → unbounded API spend) | Convert to a machine-checkable predicate (one question), or stop. |
| 2 | **Hard-stop bound** — iteration cap / budget / timeout, enforced **externally**, never by agent self-assessment. | **overbaking / runaway** (drift, bizarre scope creep) | Require a bound before launch: `loop ≤ N cycles (default N=3)` in-session; an external cap for unattended runs. |
| 3 | **maker ≠ checker** — the generator does not grade its own work; an independent evaluator decides DONE. | **nodding loop** (self-approval — the most common failure) | Independent evaluator per `nexus/reference/evaluator-loop-protocol.md` (`converge` Evaluators / `orbit` `CRITIC_MODEL` / `/goal` fresh-model check). |
| 4 | **Persistent memory** — state lives outside the conversation (files / DB / git), not in context. | **amnesiac loop** (no cumulative progress) | Filesystem-as-memory: `orbit` state files, `/goal` repo state. |
| 5 | **Drift awareness** — quality can decay across iterations *even when tests keep passing* (SlopCodeBench: structural erosion in 77% of trajectories). | silent quality erosion | Bound the loop (#2) + read-a-sample discipline. Surface as a run risk — **never assert ROI as fact**. |

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

Whoever runs the gate reports its verdict in its own output — per precondition: **met** / **converted** (with what the conversion was) / **blocking**. On a blocking verdict the run **stops and names the precondition**; it never proceeds with a partial gate or silently downgrades the loop to a single pass.
