# Agent Guide — running the loop & enforcing principles

How AI agents operate this kit. Two responsibilities: (A) **run the learning loop** when feedback arrives, and (B) **enforce** accepted principles on every UI task.

---

## A. Running the loop

Invoke via `/nexus` (this is the orchestration layer) or run the steps directly. Recommended chain:

```
CAPTURE → ANALYZE (voice ‖ echo ‖ palette) → REVIEW (human, AskUserQuestion) → PROMOTE (muse / vision / lore) → ENFORCE
```

### Step 2 — ANALYZE (the only heavy step)
Spawn in parallel, then synthesize:
- **`voice`** — cluster raw feedback into themes; sentiment + frequency. Input: all `feedback-log.md` entries with `status: new`.
- **`echo`** — cognitive walkthrough of the affected flow; emotional-friction score; pinpoint the confusion moment.
- **`palette`** (optional) — usability/a11y lens on the specific surface.

**Promotion threshold** — only draft a principle when the theme has **≥2 independent feedback items**, OR a **single high-severity** item (data loss, blocked task, a11y blocker). Below threshold: mark feedback `status: analyzed` and leave it to accumulate — do not draft a principle from a lone low-severity opinion.

For themes that clear the threshold, synthesis produces a **draft principle** using `_templates/principle-entry.md` with `status: proposed`. Decide scope:
- True on web **and** iOS **and** Android → `core`.
- Platform-specific → the matching layer (`frontend`/`ios`/`android`) as a **delta** (never duplicate a core rule).

Before drafting, scan `principles/INDEX.md` by tag — if a matching principle exists, propose an **edit** to it rather than a new entry. Mark the source feedback `status: analyzed` and link the draft.

### Step 3 — REVIEW (human gate — mandatory, never auto-approved)
**This gate is never skipped — not even under `/nexus` AUTORUN / AUTORUN_FULL.** An agent must not self-promote a draft to `accepted`; promotion requires an explicit human decision here. Treat REVIEW as an Ask-First checkpoint regardless of execution mode.

Present each draft via `AskUserQuestion`:
```
Proposed principle: <title>
Statement: <rule>
From feedback: <FB ids + 1-line summary>
Scope: <core|frontend|ios|android>
→ [Accept] [Edit] [Reject]
```
- **Accept** → set `status: accepted`, proceed to PROMOTE.
- **Edit** → capture changes, re-present.
- **Reject** → mark source feedback `status: rejected` + `Reject reason`; do not add a principle.

> A single complaint is a signal, not a law. Default to caution: prefer Edit/Reject over promoting an over-broad rule from one data point. `lore` flags drafts that **contradict or duplicate** existing principles before review.

**Conflict resolution** — if a draft contradicts an existing `accepted` principle (beyond the core-vs-platform delta rule), the human decides at REVIEW: (a) **supersede** — deprecate the old (move to its file's `## Archive`, set `Superseded by:`) and accept the new; (b) **scope-narrow** — keep both, restricting one to a platform/context; or (c) **reject** the draft. Never leave two accepted principles in direct conflict.

### Step 4 — PROMOTE
- Append the accepted entry to the correct `principles/*.md` using a kebab-case slug ID (`P-<scope>-<slug>`) — no shared counter, so concurrent promotions never collide.
- Add the principle's row to `principles/INDEX.md` (by-tag + by-scope).
- Mark source feedback `status: promoted` + `Promoted to: P-<scope>-<slug>`.
- If the principle has a **quantitative** part (spacing, color, type scale, durations), encode it as a design token via `muse` so it's machine-enforceable, and record the token name in the entry's `Token:` field.
- Add a reference mockup to `mockups/` (Do, and Before/After if applicable) — `forge` for HTML, `frame` for Figma bridge.

---

## B. Enforcement (every UI task, going forward)

**Before** any design or frontend/native UI work, an agent MUST:
1. Scan `design/principles/INDEX.md` for relevant tags, then read `design/principles/core.md` + the layer matching the target platform (`frontend.md` / `ios.md` / `android.md`). Read only the active list — the `## Archive (deprecated)` section is ignored.
2. Treat every `status: accepted` principle as a hard constraint. Where a `Token:` is set, use the token instead of a literal value.
3. After producing UI, self-check against the relevant principle slugs (or delegate to `canon` for standards compliance).

**At PR review the principles gate is mandatory** for any diff touching UI (`guardian` + `canon`, escalate to `judge` for high-stakes):
- Verify the diff violates no `accepted` principle for its platform. A violation **blocks the PR** until fixed or explicitly waived by a human reviewer.
- Note the enforcement limit honestly: quantitative principles with a `Token:` are machine-checkable; **qualitative principles are reviewer-judgment** — the gate raises them for human attention, it does not auto-prove compliance.
- A violation that reveals a *missing* principle → file it as a new `feedback-log.md` entry (`source: review`) — the loop closes on itself.

### Skill → loop-step map
| Loop step | Primary | Support |
|-----------|---------|---------|
| CAPTURE | manual / `voice` (bulk import) | — |
| ANALYZE | `voice`, `echo` | `palette`, `cast` (personas) |
| REVIEW | human via `AskUserQuestion` | `lore` (dedup/conflict flag) |
| PROMOTE | `muse` (tokens), `lore` (curate) | `vision` (direction), `frame` (Figma) |
| ENFORCE | `vision`, `artisan`, `flow`, `prose`, `native` | `canon`, `palette`, `echo` |
| GATE | `guardian`, `judge` | `canon` |

> Author spawn prompts per `_common/OPUS_48_AUTHORING.md`: front-load the principle IDs to honor, give a length envelope, and state the thinking directive. ANALYZE branches run as parallel `Agent(... run_in_background: true)` spawns.
