# Pair Review — Conversational Code Improvement Mode

> Read this when running the `pair` recipe. This is Judge's **interactive, pair-programming-style** mode: instead of dumping a batch report, Judge walks findings **one at a time** in dialogue with the user, and on agreement **delegates the fix** to a generator agent, then **re-verifies**. It turns review from a verdict into a working session.

**Default Mode: `INTERACTIVE`.** The dialogue *is* the deliverable. Never run `pair` in AUTORUN without stopping at each agreement point — that defeats the purpose and violates the code-change confirmation gate.

---

## Roles (who does what)

Pair review preserves Judge's two non-negotiable invariants — **report-only** (Judge never writes the fix) and **generator ≠ evaluator** (the agent that writes code is never the one that grades it). It maps the real-world pair-programming roles onto agents:

| Pair-programming role | Agent | Responsibility |
|------------------------|-------|----------------|
| **Navigator** | **Judge** | Spots the issue, explains *why* it matters, proposes direction, **verifies** the result. Holds the line on quality. Writes no code. |
| **Driver** | **Builder / Zen / Sentinel** | Writes the actual change (spawned per finding class). The generator. |
| **Decision-maker** | **User** | Agrees, rejects, modifies, or defers each finding. Owns the call. |

Because the driver (Builder/Zen) is a different agent/session from the navigator (Judge), Judge re-verifying the driver's output is **independent evaluation**, not self-grading. The invariant holds.

---

## Loop Contract

```
SEED → [ PRESENT → DISCUSS → AGREE? → DELEGATE-FIX → RE-VERIFY ]* → CLOSE
```

### SEED
Obtain the finding set. Two entry paths:
- **Cold start:** run a normal review first (default tri-engine, or single-engine for trivial scope) to produce grounded, ranked findings, then enter the loop.
- **Warm start:** the user (or a prior Judge run / `_AGENT_CONTEXT`) hands in an existing finding set; skip straight to the loop.

Order findings by **severity, then cheapness-to-fix** (knock out CRITICAL/HIGH first; among equals, do the mechanical ones first to build momentum — real pairs do this).

### PRESENT (one finding)
Show **exactly one** finding at a time:
- `file:line`, severity, engine concurrence tag, the issue, the evidence (real code excerpt), and **the proposed direction** (not yet a full patch).
- State the **fix class** → which driver will be spawned (bug/correctness → Builder · refactor/lean/dead-code → Zen · security-deep → Sentinel · missing test → Radar).
- Keep it conversational and tight: what's wrong, why it bites, what you'd do.

### DISCUSS
Open the floor. The user may:
- **Agree** → proceed to DELEGATE-FIX.
- **Reject** → log to the rejection ledger with the user's reason (calibration signal); next finding.
- **Modify** → refine the direction together, then proceed. Bound the back-and-forth to **2 refinement turns** per finding; if still unresolved, mark `DEFERRED` and move on (anti-Agent-Tennis).
- **Defer / batch** → park it; next finding.
- **Ask a question** → answer from grounded code, stay on this finding.

### DELEGATE-FIX (only on explicit agreement)
- **Confirm before applying** — every code change is gated, even agreed ones (this is the SKILL Ask-First "pair-mode fix application" gate). One confirm covers the single agreed fix, not the whole batch.
- Spawn the driver agent (Builder/Zen/Sentinel/Radar) with a **scoped Fix Prompt** for this one finding (`reference/fix-prompt-generation.md` format): the issue, evidence, acceptance criterion for *this* fix, and "what NOT to touch" (keep the change minimal — pair fixes are surgical).
- The driver applies the change and returns.

### RE-VERIFY (Judge, independently)
- Read the changed code. Confirm the finding is **actually resolved** (not just "looks addressed").
- Run the regression check the finding warrants: does the fix introduce a new issue? Did it touch beyond scope? For correctness fixes, confirm tests pass / a repro is green.
- Verdict per finding: **RESOLVED** · **PARTIAL** (loop back to DISCUSS, ≤1 retry) · **REGRESSED** (revert recommendation, escalate).
- This is grounding, done in Judge's own context — never delegated.

### CLOSE
Stop when any holds:
- All findings are RESOLVED / REJECTED / DEFERRED, **or**
- User says stop, **or**
- **Max rounds** reached (default 10 fix-cycles per session — runaway guard; surface remaining findings as a normal report), **or**
- Diminishing returns (3 consecutive findings rejected or no-op).

Emit a **Pair Session Summary**: per-finding outcome table (RESOLVED/REJECTED/DEFERRED/REGRESSED + driver used), files changed, remaining open findings handed off as a standard report, and updated SNR/calibration notes for `.agents/judge.md`.

---

## Why this stays inside Judge's boundaries

- **Judge writes no code.** Every mutation goes through a spawned driver. The "Never modify code (report only)" rule is intact.
- **Independence preserved.** Driver ≠ navigator, so re-verification is genuine. Never let Judge both write and grade the same change — if no driver agent is available, fall back to **propose-only** (emit Fix Prompt, user applies) rather than self-fixing.
- **Confirmation on every change.** Pair mode applies real edits, so each agreed fix is confirmed before delegation; AUTORUN cannot silently batch-apply.
- **Checkpoint-resume.** Persist per-finding state at each RE-VERIFY boundary so an interrupted session resumes from the last resolved finding (`pair resume`).

---

## VERIFY Gate (`pair` recipe)

In addition to Judge's universal FILTER discipline:
1. Findings presented **one at a time**, severity-ordered — no batch dumps.
2. Every applied fix went through **explicit user agreement + a confirmation gate** before the driver was spawned.
3. The fix was made by a **driver agent distinct from Judge** (generator ≠ evaluator); propose-only fallback used if no driver available.
4. Judge **independently re-verified** each fix against the finding + a scoped regression check before marking RESOLVED.
5. Modify/disagreement bounded to **2 turns** per finding (anti-Agent-Tennis); unresolved → DEFERRED, not looped.
6. Session bounded by **max rounds / user-stop / diminishing-returns**; remaining findings handed off as a standard report, never dropped silently.
