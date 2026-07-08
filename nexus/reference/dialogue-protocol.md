# Dialogue Protocol — elicitation quality for dialogue-driven recipes

**Purpose:** The shared discipline for **how** Nexus conducts contract-level, human-in-the-loop dialogue. Recipe references own **when** the dialogue stops (checkpoints, gates); this file owns **how** to ask, how to process answers, and how to prove the final deliverable rests on the user's elicited intent rather than silent assumptions. The deliverable of a dialogue recipe is only as good as the elicitation that produced it.

**Read when:** executing `spec` or `delve` (mandatory — their checkpoints are contract-level dialogue); `gedanken` under `INTERACTIVE`; any recipe's contract-level dialogue moment (`clone` Stack Dialogue, verdict-card closing question, `charter` scope confirmation).

---

## 1. Question craft (D1–D5)

| # | Rule | Discipline |
|---|------|-----------|
| D1 | **One focus per turn** | Ask ONE question (or one AskUserQuestion batching ≤ 4 *independent* dimensions — same bound as `intent-clarification.md` Law 2). Never a wall of open questions: each extra question halves the answer quality of all of them. |
| D2 | **Recognition over recall** | Present candidate answers to react to ("Is it A, B, or something else?") instead of blank open questions ("What are your requirements?"). Users correct a concrete guess far more reliably than they generate from nothing. Use AskUserQuestion with 2–4 genuinely distinct options for discrete picks; free text for open steering. |
| D3 | **Concrete anchor** | Ground abstract questions in a scenario: "walk me through the last time X happened" beats "what do you need from X". When the user speaks abstractly, ask for one concrete instance before persisting the abstraction. |
| D4 | **Polarity discipline** | No leading questions at divergence points (EXPAND / DIVERGE / option picks) — the user's unprimed reaction is the data. Leading is *correct* when confirming a paraphrase ("so the job is X — right?"). Wrong polarity at the wrong point either contaminates divergence or slows convergence. |
| D5 | **Tacit-knowledge probes** | The user's tacit knowledge is load-bearing (spec FRAME, delve GROUND/SURFACE). Elicit it with: **critical incident** ("when did this last fail/shine?"), **contrast** ("why X and not Y?"), **boundary** ("when would this answer be wrong?"), **history** ("what was true when this was built that isn't now?"). |

## 2. Answer processing (D6–D8)

| # | Rule | Discipline |
|---|------|-----------|
| D6 | **Paraphrase-back before persist** | Before writing any user decision to the draft, reflect it back in 1–2 lines in *different words* than the user used (echoing their words verbatim tests nothing). Persist only the confirmed paraphrase. |
| D7 | **Vague-answer rule** | A low-information answer ("sounds fine", "whatever works") gets exactly ONE concretizing follow-up (D2/D3 form). If still vague, do not badger: record the point as an `ASSUME-n` entry (§3) with your chosen default and move on. |
| D8 | **Contradiction surfacing** | When a new answer conflicts with an earlier persisted decision, surface it immediately and explicitly ("this changes DEC-2 from X to Y — intentional?"). Never silently overwrite; never silently keep the old one. The resolution is itself a persisted decision. |

## 3. Assumption Ledger (D9)

Every gap the user did **not** explicitly decide — skipped questions, D7 vague answers, defaults you chose to keep the dialogue moving, D15 delegated decisions — is recorded in an **Assumption Ledger** carried in the draft:

```
| ID | Assumption | Default chosen | Why | Status |
|----|-----------|----------------|-----|--------|
| ASSUME-1 | Notification delivery is best-effort | at-least-once NOT required | user skipped reliability Q | open |
```

- **Lifecycle:** `open` → `confirmed` (user ratifies at a checkpoint) → becomes a decision; or `open` → **Open Questions** at the final gate. `open` entries never silently disappear.
- **Checkpoint duty:** every checkpoint presentation shows the count of open assumptions and lists any *new* ones since the last checkpoint (delta-only, per D10).
- **Final-gate duty:** at LOCK / CHART, walk the remaining `open` entries with the user — each is either ratified or moved to Open Questions / Deferred Decisions. This is what the Provenance Gate (§6) verifies.

## 4. Checkpoint presentation (D10–D12)

| # | Rule | Discipline |
|---|------|-----------|
| D10 | **Envelope + delta-only** | A checkpoint presentation fits ~15 lines. On iteration, present the **delta** since the last turn, never re-dump the whole artifact — the full state lives in the draft file the user can open. An unreadable checkpoint produces a rubber-stamp confirm, which is worse than no checkpoint. |
| D11 | **Option quality** | Options presented for a pick must be genuinely distinct (different trade-offs, not paraphrases), each with a one-line trade-off, with a recommendation marked and its reason stated. 2–4 options; a 5th means the framing is wrong. |
| D12 | **Orientation line** | Every checkpoint opens with one line of state: current phase · decisions locked so far (count) · open assumptions (count). The user steering a long dialogue must never have to ask "where are we?". |

## 5. Engagement calibration (D13–D15)

| # | Rule | Discipline |
|---|------|-----------|
| D13 | **Depth follows signal** | Rich, detailed answers → deepen (more D5 probes, finer options). Terse answers trending shorter → compress: batch dimensions into one AskUserQuestion, propose defaults, lean on the Ledger. Matching the user's bandwidth is part of the contract, not a courtesy. |
| D14 | **Circling detection (all phases)** | If any dialogue point circles ≥ 2 rounds with no new information, name it and offer: (a) lock the leading option, or (b) park it as `ASSUME-n`/Open Question and proceed. (Generalizes the spec Phase 2 convergence check to every phase of every dialogue recipe.) |
| D15 | **Delegate mode** | When the user says "just decide" / "任せる", switch to propose-and-confirm: make the call, record it as `ASSUME-n (delegated)`, and continue. Contract-level checkpoints still fire — but they present the delegated decisions for ratification instead of asking the original questions. Delegation compresses the dialogue; it never deletes the checkpoints. |

## 6. Provenance Gate (D16)

Before the recipe's final sign-off gate (spec LOCK, delve CHART), classify every **load-bearing element** of the deliverable (each L1 requirement, L3 AC, scope boundary, insight, ranked direction) by provenance:

| Class | Meaning | Allowed in the final artifact? |
|-------|---------|-------------------------------|
| `elicited` | traceable to an explicit user utterance (confirmed paraphrase, D6) | yes |
| `ratified` | started as `ASSUME-n`, ratified at a checkpoint | yes |
| `parked` | recorded in Open Questions / Deferred Decisions | yes (as parked) |
| `silent` | none of the above — the dialogue never touched it | **no — the gate fails** |

A `silent` element routes back to one targeted question (D1–D3) or an explicit Ledger entry; the gate re-runs. This is the difference between "a document the user signed" and "the user's intent, crystallized" — and it is cheap: by LOCK/CHART, a well-run Ledger leaves few or zero `silent` elements.

## Failure Modes Prevented

| Failure | Mitigation |
|---------|------------|
| Wall-of-questions turn → shallow answers on all of them | D1 one focus per turn |
| Blank open questions → "I don't know, you decide" spirals | D2 recognition over recall, D3 concrete anchor |
| Leading questions contaminate divergence | D4 polarity discipline |
| Tacit knowledge never surfaces (user didn't know it was relevant) | D5 probes (critical-incident / contrast / boundary / history) |
| Misheard decision persisted to the draft | D6 paraphrase-back in different words |
| Badgering a disengaged user / swallowing a vague answer as consent | D7 one follow-up then Ledger |
| Contradictory answers silently merged | D8 contradiction surfacing |
| **Silent assumptions ship inside a "perfect-looking" deliverable** | D9 Assumption Ledger + D16 Provenance Gate |
| Checkpoint fatigue → rubber-stamp confirms | D10 envelope/delta, D12 orientation, D13 calibration |
| Indistinct options → fake choice | D11 option quality |
| Endless circling on one point | D14 generalized circling detection |
| "Just decide" collapses the contract checkpoints | D15 delegate mode (compresses, never deletes) |

## Wiring (per recipe)

- **`spec`** — FRAME's Socratic clarification runs D1–D8; every checkpoint follows D10–D12; the draft carries the Assumption Ledger (§3) as a section; the Spec Quality Gate adds a **Provenance** dimension (D16) alongside ambiguity/completeness/consistency/testability/scope.
- **`delve`** — GROUND's Socratic clarification runs D1–D8 (D5 history probe is the reason-for-existence tool); the three knowledge-juncture checkpoints follow D10–D12; the Evolution Map's insights and directions pass D16 (an insight the user never validated is `silent`).
- **`gedanken` (INTERACTIVE)** / **`clone` Stack Dialogue** / **verdict-card closing question** — D1–D4 + D10–D11 apply to the single or per-phase dialogue moments; the Ledger is optional (short dialogues rarely need one).

This protocol governs the **hub's own conversation with the user** — it is not a spawn-prompt directive. Spawned agents (Riff, Plea, Magi, …) produce material; Nexus alone runs the dialogue that presents it.
