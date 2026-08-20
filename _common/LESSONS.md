# Lessons — What Went Wrong, and What Now Catches It

> **Tier:** `authoring` — activates when creating or auditing harness machinery, not during user work. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

**A lesson with no mechanism is a hope, and a hope does not belong in a registry.** Every row below names a failure that actually happened here and the check, limit, or structural change that now catches it. `_common/scripts/lint-lessons.py` rejects a row whose `Mechanism` is empty or reads as an intention — "remember to", "be careful", "always try to". **That refusal is the feature.** A lesson that cannot be mechanised is not recorded as a weaker rule; it is left out, and the harness admits nobody is keeping it.

This is the difference between this file and a journal. `.agents/*.md` holds what an agent learned; that is memory, and memory decays. This file holds only what stopped being a matter of memory.

**Read when:** adding or changing a checker, a gate, or a `_common/` control; auditing whether a past failure is actually prevented; deciding whether a proposed rule can be enforced at all.

---

## Fields

| Field | Rule |
|-------|------|
| `ID` | `L###`, never reused. A deleted lesson's ID stays retired |
| `What happened` | One sentence, past tense, specific. Not the category — the instance |
| `F` | The failure class it belongs to: `F1` / `F2` / `F3` / `F4` (`_common/HARNESS_DEBT.md` § 3b) |
| `Mechanism` | The check, limit, or structural change that catches it **now**. An intention is not a mechanism |
| `Where` | The file that carries the mechanism. Must resolve; a mechanism living nowhere is an intention with a filename |
| `Added` | ISO date. Past `lesson_age_days` (365) the row is re-justified against the current corpus or deleted |

---

## Register

| ID | What happened | F | Mechanism | Where | Added |
|----|---------------|---|-----------|-------|-------|
| L001 | `lint-instructions.py` I1 was written to catch skill-count drift, but its pattern matched neither instruction file's phrasing — it reported `OK` across three unchecked claims, for as long as it had existed. | `F3` | The matcher is broad across phrasings and languages and splits claims by scope; three tests break each phrasing in turn and assert I1 names the wrong number. | `_common/scripts/test_checkers.py` | 2026-08-21 |
| L002 | `lint-contracts.py` CD-3 built its reachability graph over `.agents/`, which is gitignored, so a contract reached only through a journal counted as delivered — the checker reported `OK` locally on exactly the commit CI rejected. | `F3` | `UNTRAVERSED_DIRS` stops the graph at gitignored and archived paths, and a regression test asserts a journal edge does not deliver a contract. | `_common/scripts/lint-contracts.py` | 2026-08-21 |
| L003 | `routing-oracle.py` RO-1 resolved a dead reference by finding a same-named file anywhere in the tree, including `.archive/` — references to retired skills read as live. | `F3` | The `elsewhere` search excludes archived paths, so a reference that resolves only inside `.archive/` is reported dead. | `_common/scripts/routing-oracle.py` | 2026-08-21 |
| L004 | Every hard-fail step in CI was gated on `pull_request` while this repository commits straight to main, so on the path actually used the gates never fired — enforcement existed in the config and nowhere else. | `F3` | The `if:` gates are gone, and `make hooks` installs a pre-commit hook so the checks run before the commit rather than after the push. | `Makefile` | 2026-08-21 |

---

## Adding a row

1. **The failure must have happened**, here, and be describable as an instance. A failure mode imagined during design is a risk (`omen`), not a lesson.
2. **Find the mechanism before writing the row.** If the honest answer is "we will be more careful", stop — that is `_common/VALUES.md` § 2, and the correct outcome is either finding a shape that can be checked or admitting the rule is a hope. Writing the hope down here launders it into an enforcement nobody performs.
3. **A new check needs a test that watches it fail** (`test_checkers.py`), which is itself L001's mechanism generalised.
4. Rows are append-only within a review cycle. Deletion happens at the 30-day sweep, against `Added` and the current corpus.

## Lifecycle

| Field | Value |
|-------|-------|
| `failure` | `F3 — a fix is applied, the reasoning behind it is lost, and the same class of defect returns in a different file with nobody recognising it.` Journals hold the memory today, and journals are per-agent, gitignored, and unread by the checker that would have to enforce anything. |
| `effect` | Catches: a proposed rule that cannot name its mechanism is refused at the point of writing, and a mechanism that was deleted shows up as a `Where` that no longer resolves. Does **not** catch: whether the mechanism actually works — that is `test_checkers.py`'s job, and a row may cite a check that is itself vacuous. |
| `owner` | `gauge` — it owns the checker suite. Register triage at the 30-day cycle sits with `darwin`, falling back to `prune` per `_common/PROJECT_LOCAL_SKILLS.md`. |
| `removal` | Delete when the register has gone two consecutive review cycles with no row added *and* no row's `Where` broken — the failures it tracks have stopped happening, or nobody is recording them, and either way the file is being carried rather than used. |
