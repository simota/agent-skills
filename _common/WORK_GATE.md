# Work Gate — Per-Deliverable Verdict (Common Definition)

> **Tier:** `spine` — in effect on every run. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

`WORK_GATE` is an **emit format, not a new rule set.** Most of its axes make already-binding
discipline visible in a fixed position; only `RSK` adds a rule, and it adds it where one was
missing — 67 of the 90 skills write no code, so they never reach `CODE_QUALITY_GATE`'s `SEC`
floor and had no exposure check at all.

The gate answers two questions for the reader: *what did this work have to go on*, and *which
part of it should I not trust yet.*

---

## Shape

Six axes are rated `★1–5`. One axis — `RSK` — is not rated at all.

**Stars are per-axis and are never added, averaged, or weighted into an overall rating.** A
composite is precisely what lets a bad axis be offset by good ones, and this repository has
already paid for that shape once (`nexus/reference/quality-iteration.md` § UQS — a weighted
composite whose inputs are never persisted; `_common/TOKEN_ECONOMY.md` §6 generalizes it: *a
formula with no data source is never presented with a grade band or wired into a gate*).
There is no "overall ★", no chain average, and no `WORK_GATE` total anywhere.

**Bands are coarse on purpose.** Assign **the highest band whose complete description is true** —
the same rule the repository already uses for evidence bands
(`nexus/reference/confidence-scoring.md` § Discrete Evidence Bands: *pseudo-precision is not
evidence*). Five bands exist because five states are distinguishable; a sixth would be invented.

**`n/a` replaces the stars entirely** when an axis does not apply, and it carries a reason. It is
never rendered as ★1 and never counted as ★5. Four or more `n/a` axes require a one-line
statement of why the gate barely applies — a gate that is mostly `n/a` is reporting that it was
the wrong gate, which is itself useful.

### Why `RSK` has no stars

A floor is not a gradient. `RSK` is `pass` or `risk`; `★★★☆☆ 安全` has no meaning and invites
trading exposure against a well-written report. `RSK: risk` **blocks completion** — fix it, or
stop and put it to the user. Code-writing skills emit `CODE_QUALITY_GATE` as well: `RSK` covers
what the deliverable *does* to the world, `SEC` covers what the code *contains*.

---

## Axes

### `IN` — input quality (what the work had to go on)

Rated against the dimension inventory in `_common/CONTEXT_SUFFICIENCY.md` §1. This axis is about
the **request and the context received**, not about the agent's performance — a ★1 `IN` with a
★4 `OUT` is a good run on a bad brief, and that is worth seeing.

`IN` is also the **only star a gate may act on**, and only when the rater is the receiver: at ★★☆☆☆
or below, with a named item the sender held and did not pass, it refuses the handoff
(`_common/HANDOFF.md` § Handoff Admission Gate). The sender's own stars never trigger anything —
self-certification wired into a gate is what `TOKEN_ECONOMY.md` §6 forbids.

| Band | Complete description |
|------|----------------------|
| ★★★★★ | Goal, scope, constraints, target, and success condition all explicit; every source needed was reachable and current |
| ★★★★☆ | All load-bearing dimensions settled; only minor reversible assumptions were made, and they are stated |
| ★★★☆☆ | One non-blocking dimension was partial; a safe reversible default was chosen and recorded |
| ★★☆☆☆ | A load-bearing dimension was unresolved, or two material interpretations remained, and the run proceeded on one |
| ★☆☆☆☆ | Goal or target largely absent, or a required source was unreachable/stale; the deliverable rests on inference |

### `OUT` — output quality (how far the deliverable was actually verified)

Rated by the **evidence rung reached** — `_common/EVIDENCE_LADDER.md` `E0`–`E6`. This is not a
self-assessment of how good the work feels; it is which rung the strongest available check
actually stands on, which is checkable by a reader.

| Band | Complete description |
|------|----------------------|
| ★★★★★ | `E5`–`E6` — integration surface, canary, attestation, or production observation |
| ★★★★☆ | `E4` — an independent oracle: property, metamorphic, mutation, fuzz, or differential |
| ★★★☆☆ | `E3` — automated tests, **or** a re-read against the source spec by a check the author did not also write |
| ★★☆☆☆ | `E1`–`E2` — static analysis, build, or local execution only |
| ★☆☆☆☆ | `E0` — model assertion and self-review only. Never a shipping state for a load-bearing claim |

`OUT` subsumes the older `VER` axis: `E3` and above require an oracle independent of the
producer, so "was it independently checked" is the ★3 boundary rather than a separate line.

### `FIT` — scope match

Surfaces `OPERATIONAL.md` § Completion Contract (frozen ACs, typed deferral, no status inflation).

| Band | Complete description |
|------|----------------------|
| ★★★★★ | Everything asked, nothing added, nothing deferred |
| ★★★★☆ | Everything asked; deferrals are typed with blocker, owner, and route |
| ★★★☆☆ | A part was cut or added, named explicitly, with the reason |
| ★★☆☆☆ | Scope moved and is reported, but the delta is not itemized |
| ★☆☆☆☆ | Scope was silently narrowed or widened |

### `EVD` — claims tied to checkable evidence

Surfaces § Completion Contract (claims bound to evidence).

| Band | Complete description |
|------|----------------------|
| ★★★★★ | Every load-bearing claim carries `file:line`, command output, a diff, or a cited source |
| ★★★★☆ | Every load-bearing claim is backed; incidental claims are not, and are marked as such |
| ★★★☆☆ | Most are backed; the unbacked ones are labelled `UNVERIFIED` |
| ★★☆☆☆ | Backing is present but not traceable — named without a locator |
| ★☆☆☆☆ | Load-bearing claims asserted without backing |

### `CLR` — usable by the named consumer

Surfaces `_common/OUTPUT_STYLE.md` (cognitive load, fixed tail slots).

| Band | Complete description |
|------|----------------------|
| ★★★★★ | Consumer named; result first; every locator resolvable; no term used before defined |
| ★★★★☆ | Consumer named and served; one lookup needed somewhere |
| ★★★☆☆ | Correct and complete, but the consumer must re-order or re-derive to act |
| ★★☆☆☆ | Consumer not named; the reader has to infer who this was for |
| ★☆☆☆☆ | Requires a second pass to be usable at all |

### `CST` — effort proportional to the deliverable

Stated in **counts, never tokens.** `_common/TOKEN_ECONOMY.md` §5 is a standing limit: no
per-skill cost figure is derivable (`attributionSkill` is null on ~65% of records and
version-biased), and sub-agent spend must be reported as an **event count, never estimated as
tokens**. A `CST` line carrying "~12k tokens" would be a fabricated measurement.

Report what the run observed: subagent spawns · files read · files written · tool-call rounds.

| Band | Complete description |
|------|----------------------|
| ★★★★★ | Counts are at or below what the deliverable plainly needed |
| ★★★★☆ | Proportionate; some exploration that did not reach the deliverable |
| ★★★☆☆ | Noticeable rework — a path was taken and abandoned |
| ★★☆☆☆ | Visibly out of proportion, e.g. several subagents for a one-line answer |
| ★☆☆☆☆ | Effort dominated by retries or by re-reading what was already in context |

There is no "over budget" band, because there is no budget this repository can measure.

---

## Emit format

```
WORK_GATE:
  IN  ★★★☆☆ — <what was and was not given at intake>
  FIT ★★★★★ — <scope delta, or "as requested">
  EVD ★★★★☆ — <what backs the load-bearing claims>
  OUT ★★★☆☆ — <E-rung reached, and by which check>
  RSK pass   — <exposure; `risk` blocks completion — never starred>
  CLR ★★★★★ — <named consumer, and what they get>
  CST ★★★★☆ — <spawns / files read / files written / rounds>
```

Worked example:

```
WORK_GATE:
  IN  ★★☆☆☆ — target latency never stated; assumed p95 from the existing SLO
  FIT ★★★★★ — all three asked items delivered; nothing added
  EVD ★★★★☆ — every claim has file:line; the latency figure is labelled UNVERIFIED
  OUT ★★★☆☆ — E3: pytest 42 passed, suite predates this change
  RSK pass   — no destructive or outward-facing action
  CLR ★★★★★ — for builder: file:line on every change point
  CST ★★★★☆ — 0 subagents, 6 files read, 2 written, 9 rounds
```

## Proportionality

Scales with the planning tier of `OPERATIONAL.md` § Completion Contract:

| Tier | Emit |
|------|------|
| **Skip** | `RSK` only if it is not `pass`, plus any axis at ★★☆☆☆ or below. All-good emits nothing — a one-line answer does not carry a seven-line certificate. |
| **Light** | All seven lines. |
| **Full** | All seven lines, plus the evidence behind each rating where it is not already in the body. |

Ceremony never exceeds the task. `RSK: risk` is emitted at every tier without exception.

---

## Chain aggregation (Nexus)

Nexus renders spoke gates as a **matrix, never a rollup** — skills down, axes across, stars in
the cells, no row total and no column average. The reader's question is *which skill, which
axis*. Format: `nexus/reference/output-formats.md` § Work Gate Matrix.

---

## What this gate does not do

Stars measure **process and evidence, not correctness.** A deliverable can be ★5 on every axis
and still be wrong: `OUT ★★★★☆` says an independent oracle ran and agreed, not that the goal
was the right goal. Reading a row of stars as proof of a right answer is the misuse to watch
for, and it is the reason there is no overall rating to read that way.

---

## Complexity Budget

Per `_common/HARNESS_DEBT.md` §3b:

| Field | Declaration |
|-------|-------------|
| `failure` | A deliverable ships with a silently narrowed scope, an unverified load-bearing claim, or an irreversible action, and nothing in the output says so — and separately, a poor result caused by a poor brief is indistinguishable from a poor result caused by poor work. Today 67 of 90 skills have no fixed place to record either. |
| `effect` | Puts the Completion-Contract failure modes in a fixed, scannable position; separates input quality from output quality so a bad brief is visible as a bad brief; gives non-code skills an exposure floor they lacked. It does **not** catch a confident, well-evidenced, wrong deliverable, and the star bands are self-assigned — `IN`, `FIT`, `CLR`, and `CST` have no external check, so they are testimony, not measurement. Only `OUT` is anchored to an artifact a reader can inspect. |
| `owner` | `nexus` — it owns the completion protocol this gate surfaces (`reference/autonomy-quality-protocol.md`) and the chain matrix. **Not `gauge`:** gauge audits SKILL.md files statically, and `WORK_GATE` is a runtime emit that appears in no SKILL.md, so there is nothing for gauge to scan. `darwin` runs the removal test below as part of its evaluation cycle. |
| `removal` | Delete when either holds: (1) `attributionSkill` and `isSidechain` become reliable (`TOKEN_ECONOMY.md` §5), so `CST` and `OUT` can be computed rather than asserted and a mechanical signal replaces the self-report; or (2) two consecutive `darwin` evaluation cycles find star ratings uncorrelated with the defects those cycles actually surfaced — a self-assigned rating that does not predict real defects is decoration, and decoration is removed. Partial removal counts: an axis that never leaves ★★★★★ across a cycle is dropped on its own, without waiting for the whole gate. |
