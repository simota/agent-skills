# Pair Programming Mode

Interactive, increment-by-increment co-implementation where Builder acts as the **driver** (writes production-grade code) and the user acts as the **navigator** (sets direction, reviews each increment, decides go/adjust/redirect). Unlike batch build (implement the whole feature, present once), pair programming is a conversation: propose one small increment, agree on it, implement it, verify it, confirm, then advance.

## When to Use

| Use pair programming | Use batch build (default) |
|----------------------|---------------------------|
| Live session, want to steer as it is built | Spec is locked, want the feature delivered |
| Learning / mentoring / unfamiliar domain | Well-understood change |
| High-uncertainty design — decisions emerge as you go | Clear plan, low ambiguity |
| User explicitly asks to "pair", "build together", or "confirm as we go" | Standard implementation request |

**Not a speed mode.** For throwaway rapid prototyping (speed over quality), use Forge. Builder-pair keeps the full production quality bar — it changes *cadence*, not *standards*.

## Roles: Driver / Navigator Separation

- **Builder = Driver.** Proposes the next increment, writes the code, runs its verification, shows the diff. Owns *how* it is built to the quality bar.
- **User = Navigator.** Owns *what* and *whether* — sets direction, approves each increment, redirects. Decides pace.
- **The navigator is not a passive reviewer.** Builder proposes intent + verification *before* writing, so the user steers before code exists, not after.

Unlike Judge's pair-review (where Judge stays report-only and spawns a distinct driver to preserve generator ≠ evaluator), Builder *is* the generator — pair mode simply makes its build loop interactive and human-steered.

## Protocol

```
SETUP:
  - Agree on the goal + acceptance criteria.
  - Draft an ordered increment plan (smallest shippable units). A Sherpa decomposition can seed this.
  - Agree on the verification path for increment #1 (test / type / contract / expected output) — verification-first.

LOOP until goal met or user ends session:
  1. Builder proposes the NEXT increment (one type module / one function / one vertical slice):
     - what it will implement, why, and the verification that will prove it
  2. User decides: go / adjust scope / redirect / skip
  3. Builder implements THAT increment only — to the full Core Contract quality bar
  4. Builder shows the diff + runs the increment's verification, reports the result
  5. User confirms (accept) or requests a change (bounded iterate — max 2 turns/increment)
  6. Checkpoint. Advance to the next increment.

CLOSE:
  - Run the 5-axis Impact Scope Check (callers / tests / types / configs / docs).
  - Present a session summary + handoff (Radar for tests, Guardian for PR).
```

## Interaction Contract

- **One increment at a time.** Never implement the whole feature then ask for a single approval — the point is steer-as-you-go.
- **Intent before code.** State what + why + verification, get the go-ahead, then write. The navigator steers before code exists.
- **Increment size bounded.** Each increment is reviewable in one sitting (≈ one slice / a small handful of functions). If an increment balloons, split it.
- **Show the diff every time.** Do not advance without the user seeing what changed and confirming.
- **User drives the pace.** Builder proposes and waits; never barrels through multiple increments unprompted.
- **Quality bar unchanged.** Every increment is production-grade — types-first, always-valid domain, boundary `.safeParse()`, no `any`, edge cases handled. Pair mode is not an excuse for rough code (that is Forge).
- **Bounded.** Max increments (default 12) / user-stop / goal-met / diminishing-returns. On bound, hand the remaining plan back as a normal build plan.
- **Checkpoint-resumable.** Persist the increment log so an interrupted session resumes from the last confirmed increment (`pair resume`).

## Verify After Each Increment

Verification is not deferred to the end. After each implemented increment:
- Show the diff of exactly what changed.
- Run the increment's verification (the test / type-check / contract check agreed in SETUP or step 1).
- Report pass/fail; if it introduced a regression or a new edge, surface it as the next increment.
- Only advance once the increment is green and the user confirms.

The final full 5-axis Impact Scope Check still runs at CLOSE — per-increment verification does not replace it.

## Under AUTORUN

Pair mode is INTERACTIVE and cannot run unattended. Under AUTORUN / Nexus AUTORUN:
- Run SURVEY → PLAN, produce the ordered increment plan + verification paths, and return `_STEP_COMPLETE` with `Next: USER` (pair-ready).
- Do **not** implement increments without confirmation — that would defeat the mode.

## Output

At session end, emit a compact summary:

```
Pair Programming Summary
- Goal:              [what was being built]
- Implemented:       [increments accepted, with file:line]
- Deferred / skipped:[increments the user set aside]
- Remaining:         [unbuilt increments from the plan]
- Impact Scope:      [5-axis verdict — Ready | Needs Ripple | Blocked]
- Handoff:           [Radar for tests / Guardian for PR / next increment]
```
