# Work Gate — Per-Deliverable Verdict (Common Definition)

> **Tier:** `spine` — in effect on every run. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

`WORK_GATE` is an **emit format, not a new rule set.** Five of its six axes make already-binding
discipline visible in a fixed position; only `RSK` adds a rule, and it adds it where one was
missing — 67 of the 90 skills write no code, so they never reach `CODE_QUALITY_GATE`'s `SEC`
floor and had no exposure check at all.

The gate answers one question for the reader: *which part of this work should I not trust yet.*

---

## Verdict vocabulary

`pass` · `risk` · `n/a` — per axis, one line each, with the reason on the same line.

**Never a number, never summed.** Axes are not averaged, weighted, or collapsed into a score.
A composite is precisely what lets a `RSK: risk` be offset by five green axes, and this
repository has already paid for that shape once (`nexus/reference/quality-iteration.md` § UQS —
a weighted composite whose inputs are never persisted; `_common/TOKEN_ECONOMY.md` §6 makes the
governing rule general: *a formula with no data source is never presented with a grade band or
wired into a gate*).

`n/a` is a claim, not a blank. It carries a reason and **is never counted as `pass`**. When four
or more axes are `n/a`, the skill states in one line why the gate barely applies — a gate that
is mostly `n/a` is reporting that it was the wrong gate, which is itself useful.

---

## The six axes

| Axis | Question | What it surfaces | Blocking |
|------|----------|------------------|----------|
| `FIT` | Does the deliverable match the request — nothing silently narrowed, nothing silently added? Are dropped items named? | `OPERATIONAL.md` § Completion Contract (frozen ACs, typed deferral, no status inflation) | no |
| `EVD` | Is every load-bearing claim tied to something checkable — `file:line`, command output, a diff, a cited source? | § Completion Contract (claims bound to evidence), `_common/EVIDENCE_LADDER.md` | no |
| `VER` | Was the deliverable checked against something **independent of its author**? Name the check and its result. | § Completion Contract (producer never sole verifier; completion sweep) | no |
| `RSK` | Irreversible actions, security exposure, privacy exposure, or spend the user did not authorize | **new** — the deliverable-agnostic analogue of `CODE_QUALITY.md` § `SEC` | **yes** |
| `CLR` | Can the named consumer — next agent or human — use this without a second pass? | `_common/OUTPUT_STYLE.md` (cognitive load, fixed tail slots) | no |
| `CST` | Was the effort proportional to the deliverable? | `_common/TOKEN_ECONOMY.md` — **counts, not tokens** (see below) | no |

### `RSK` is the floor

`RSK: risk` blocks completion. Fix it, or stop and put it to the user. It is never silently
deferred and never traded against another axis. Code-writing skills emit **both** gates:
`RSK` covers what the deliverable *does* to the world, `SEC` covers what the code *contains*.

### `CST` is stated in counts, never in tokens

`_common/TOKEN_ECONOMY.md` §5 is a standing limit: **no per-skill cost figure is derivable**
(`attributionSkill` is null on ~65% of records and version-biased), and **sub-agent spend must
be reported as an event count, never estimated as tokens**. A `CST` line carrying "~12k tokens"
would be a fabricated measurement.

State instead what the run actually observed: subagent spawns, files read, files written,
reference files loaded, tool-call rounds. `risk` on `CST` means the count is visibly out of
proportion to the deliverable — six subagents for a one-line answer — not that a budget was
exceeded, because there is no budget this repo can measure.

---

## Emit format

```
WORK_GATE:
  FIT: pass | risk | n/a — <scope delta, or "as requested">
  EVD: pass | risk | n/a — <what backs the load-bearing claims>
  VER: pass | risk | n/a — <the independent check that ran, and its result>
  RSK: pass | risk | n/a — <exposure; `risk` blocks completion>
  CLR: pass | risk | n/a — <named consumer, and what they get>
  CST: pass | risk | n/a — <observed counts: spawns / files / rounds>
```

Worked example:

```
WORK_GATE:
  FIT: pass — all three asked items delivered; nothing added
  EVD: risk — the latency claim is an estimate, not a measurement
  VER: pass — pytest 42 passed, ruff clean (independent of the edit)
  RSK: pass — no destructive or outward-facing action
  CLR: pass — for builder: file:line on every change point
  CST: pass — 0 subagents, 6 files read, 2 written
```

## Proportionality

The gate scales with the planning tier of `OPERATIONAL.md` § Completion Contract:

| Tier | Emit |
|------|------|
| **Skip** | Only axes that are not `pass`. All-green emits nothing — a one-line answer does not carry a six-line certificate. |
| **Light** | Full six lines. |
| **Full** | Full six lines, plus the evidence each `pass` rests on where it is not already in the body. |

Ceremony never exceeds the task. `RSK: risk` is emitted at every tier without exception.

---

## Chain aggregation (Nexus)

Nexus renders spoke gates as a **matrix, never a rollup** — skills down, axes across. There is
no chain score. The reader's question is *which skill, which axis*, and a total erases exactly
that. Format: `nexus/reference/output-formats.md` § Work Gate Matrix.

---

## Complexity Budget

Per `_common/HARNESS_DEBT.md` §3b:

| Field | Declaration |
|-------|-------------|
| `failure` | A deliverable ships with a silently narrowed scope, an unverified load-bearing claim, or an irreversible action, and nothing in the output says so. Today 67 of 90 skills have no fixed place to say it — the discipline binds, the disclosure does not. |
| `effect` | Puts the four Completion-Contract failure modes in a fixed, scannable position, and gives non-code skills an exposure floor they lacked. It does **not** catch a confident, well-evidenced, wrong deliverable — every axis measures process, not correctness. Treating a green gate as proof of a right answer is the misuse to watch for. |
| `owner` | `nexus` — it owns the completion protocol this gate surfaces (`reference/autonomy-quality-protocol.md`) and the chain matrix. **Not `gauge`:** gauge audits SKILL.md files statically, and `WORK_GATE` is a runtime emit that appears in no SKILL.md, so there is nothing for gauge to scan. `darwin` runs the removal test below as part of its evaluation cycle. |
| `removal` | Delete when either holds: (1) `attributionSkill` and `isSidechain` become reliable (`TOKEN_ECONOMY.md` §5), so `CST` and `VER` can be computed rather than asserted and a mechanical signal replaces the self-report; or (2) two consecutive `darwin` evaluation cycles find gate verdicts uncorrelated with the defects those cycles actually surfaced — a self-reported gate that does not predict real defects is decoration, and decoration is removed. |
