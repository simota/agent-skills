# `spec` — Interactive feature-proposal → locked specification

**Purpose:** Full phase contract for the `spec` Recipe — take a rough feature idea and refine it **through deep human-in-the-loop dialogue** into a finalized, acceptance-criteria-bearing specification. **Stops at the spec document; writes no code.** The discovery-and-finalize half of `spec → feature`/`apex`, analogous to `charter → enact`.

**Read when:** Executing the `spec` Recipe.

---

## What `spec` is for

A user has a feature idea — possibly vague ("I want notifications") — and wants to **think it through thoroughly in conversation** until there is a spec solid enough to build from. The deliverable is not a verdict and not code: it is a **locked specification** the user explicitly signs off on.

`spec` is the recipe whose **deliverable is the dialogue itself**. Where every other recipe treats user confirmation as a gate around autonomous work, `spec` inverts it: the back-and-forth IS the work, and the spec document is its crystallized output.

### Depth modes (`spec depth=light|standard|deep`)

`spec` is deliberately heavy by interaction turns, and that heaviness is wrong for a small, well-understood feature — a user forced through six phases for a settings toggle abandons the recipe and specs nothing. Depth scales the *dialogue*, never the lock preconditions:

| Depth | When | Phases | Panel | Turns |
|-------|------|--------|-------|-------|
| `light` | one bounded change, the problem is already agreed, no real option space | FRAME → SPECIFY → LOCK (EXPAND/CHALLENGE/SHAPE collapse into one confirm) | skipped | ~3-5 |
| `standard` (default) | a normal feature with genuine alternatives | all six | 2 skeptics (claims 1, 3) | ~8-15 |
| `deep` | high-stakes, contested, or expensive-to-reverse; a spec several teams will build against | all six + extended EXPAND | 3 skeptics (all four claims) | ~15-30 |

**Invariant across all three:** testable L3 ACs, the Spec Quality Gate, the Provenance Gate, and explicit sign-off are lock preconditions at every depth — `light` buys fewer *turns*, never a weaker *lock*. Nexus proposes a depth at FRAME with its reason and the user may override; an unstated depth defaults to `standard`. A `light` run that discovers a real option space **escalates to `standard` and says so** rather than under-specifying.

### Default Mode: `INTERACTIVE` (exceptional)

`spec` is one of two Recipes (with `delve`) that default to `INTERACTIVE` instead of `AUTORUN_FULL` — `spec` shapes a *new* feature, `delve` excavates an *existing* one. The phase-boundary dialogue checkpoints below are **part of the recipe contract, not the Mode** — so even if `spec` is invoked under `AUTORUN_FULL`/`AUTORUN`, it still stops at each checkpoint for the user to steer. (Recipes = task shape; Modes = execution control; `spec`'s checkpoints are contract-level.) `GUIDED` is acceptable for a lighter touch (confirm only at FRAME / CHALLENGE-pick / LOCK); never silently drop a checkpoint.

---

## Phase contract

`FRAME → EXPAND → CHALLENGE → SHAPE → SPECIFY → LOCK`

### Phase 0 — FRAME (problem before solution)
Establish the shared problem statement **before** any option generation. Echo[demand: claude latent-needs/pain-extraction] surfaces the real job-to-be-done; +Field[claude user-research grounding] when research data exists; +Cast[claude persona] when the audience is unclear. **+Lens[claude reuse-scan] on an existing codebase (skip greenfield):** before fixing the problem, survey what already ships — does a comparable feature/module/pattern already exist, which assets are reusable, and what technical constraints (current stack, data model, integration points) bound the solution. This grounds the spec in the real codebase and prevents an out-of-context spec that re-derives shipped code. Nexus drives Socratic clarification with the user — conducted per `reference/dialogue-protocol.md` (D1–D8: one focus per turn, recognition over recall, concrete anchors, tacit-knowledge probes, paraphrase-back before persisting) — covering: who is this for, what job does it do, what does success look like, what is explicitly out of scope, what constraints (tech / time / compliance) bound it. All dialogue throughout the recipe follows that protocol: checkpoints per D10–D12 (envelope / delta-only / orientation line), engagement calibration per D13–D15, and undecided gaps tracked in the draft's **Assumption Ledger** (D9).
- **Checkpoint (mandatory):** present a 3-5 line problem statement (carrying any reuse/constraint findings from Lens); the user confirms or corrects it. Option generation **cannot start** until the problem statement is confirmed. (Prevents "spec a half-baked idea".)
- **Draft init:** on problem-statement confirmation, write the initial `docs/specs/<slug>.draft.md` (status `draft`, L0 Vision + reuse/constraint findings filled). See **Draft persistence & resume**.

### Phase 1 — EXPAND (diverge)
Generate the option space. Flux[claude Expand/Propose modes — iterative dialogue] ‖ Flux[claude challenge-assumptions / cross-domain reframes]. Produce **3-5 candidate directions**, each with a one-line rationale and rough shape. +Compete[claude+WebSearch] when market/differentiation framing matters.
- **Checkpoint:** present the candidates; the user reacts, eliminates, combines, or adds. Expect **multiple turns** here — this is the divergent heart of the dialogue. Do not converge prematurely. On checkpoint pass, append the surviving candidates to the draft.

### Phase 2 — CHALLENGE (stress-test + converge)
Narrow to ONE direction *with the user*. Magi[claude multi-perspective necessity/trade-off arbitration] + Void[claude subtract scope / YAGNI] + Ripple[claude feasibility/impact] + Omen[claude pre-mortem on the leading candidate when stakes are high]. Each surfaces a distinct pressure: is it necessary, is it over-scoped, is it feasible, how does it fail.
- **Checkpoint (mandatory):** the user makes the **explicit pick** of the single direction to specify. Carry forward rejected directions as recorded "considered but rejected" so the dialogue does not re-derive them. Record the pick and the considered-but-rejected list to the draft.
- **Convergence check:** before looping back to EXPAND, Nexus asks "are we converging, or circling?" If circling ≥ 2 rounds with no new information, offer to (a) lock the leading candidate, or (b) park the disagreement as an Open Question and proceed. Never loop indefinitely.

### Phase 3 — SHAPE (proposal)
Spark[claude feature-proposal] synthesizes the chosen direction into a structured proposal: problem → proposed solution → in-scope → out-of-scope → assumptions → open questions. +Rank[claude] when the direction decomposes into sub-features needing MoSCoW ordering.
- **Checkpoint:** present the proposal; capture the user's edits section by section, then write the agreed proposal sections to the draft.

### Phase 4 — SPECIFY (authoring with mandatory acceptance criteria)
Scribe[unified: claude staged elaboration: L0 Vision → L1 Requirements → L2 Detail → L3 Acceptance Criteria] as the spine; +Scribe[claude PRD/SRS/HLD] for narrative spec sections; +Gateway/Schema[claude] when the spec needs API/data-model detail. Author against the **Spec document template** (below) so the artifact is downstream-consumable, and iterate with the user **section by section**, persisting each agreed section to the draft.
- Give every L3 acceptance criterion a **traceable ID (`AC-1`, `AC-2`, …)** mapped to the L1 requirement it verifies — this traceability is what the Spec Quality Gate's Completeness check verifies and what `feature`/`apex`/`orbit` consume as their verification contract.
- **Lock preconditions (both mandatory, verified at LOCK):** (1) the spec carries **testable L3 acceptance criteria** (the difference between a spec and a wish) — +Attest[claude] sanity-checks that each AC is actually verifiable; (2) the spec **passes the Spec Quality Gate** (below). +Echo[claude] for a quick usability sanity-pass on the shaped flow when there is a UI surface.

### Phase 5 — LOCK (sign-off + persist, no code)
**Gate:** do not present for sign-off until **both lock preconditions pass** — testable L3 ACs (Attest) **and** the Spec Quality Gate (below). Then present the complete spec and require the user's **explicit sign-off** ("lock it"). On sign-off:
- **Finalize the draft:** promote `docs/specs/<slug>.draft.md` to the locked `docs/specs/<feature-slug>.md` (status `locked`; override path on request), following the **Spec document template**. Include an explicit **Open Questions / Deferred Decisions** section — parked items (including any Quality-Gate findings downgraded rather than fixed) are recorded, never silently dropped. Archive or remove the `.draft.md` once promoted.
- **Build-path selection (mandatory checkpoint):** before recommending a handoff, ask the user **how** they want the locked spec built. Present the two autonomous build paths as the headline choice, with the supervised recipes as fallbacks:
  - **orbit loop** — turn the spec into a `nexus-autoloop` runner: the spec's L3 acceptance criteria become the loop's completion contract (machine-checkable DONE gate), with operation contract, resumable state, and recovery. Pick when the build is **long-running / unattended / multi-session**, benefits from checkpoint-resume, or the user wants a self-driving runner they can leave alone. Hands off to the project-local `orbit` agent when available (loop generation) — see `.claude/skills/orbit/SKILL.md`; otherwise use `goal` or `apex`.
    - **Executor-engine sub-choice (when orbit is picked):** select which CLI runs each loop iteration — **claude** (Claude Code; default, broadest tool/skill access), **codex** (Codex CLI; latest gpt-5.6 generation — build loops run `gpt-5.6-terra`, requires `multi_agent=true` + `[agents] max_depth >= 2`), or **agy** (Antigravity CLI; headless needs a real pty + artifact capture). Orbit wires the choice into the generated runner's `EXEC_CMD` / engine flags — see `.claude/skills/orbit/reference/executor-engines.md`. Pass the picked engine in the orbit handoff so the runner is generated for the right CLI; before handing off, note the engine's prereqs (Codex spawn-depth, agy pty) per `_common/CLI_COMPATIBILITY.md`. If unsure, default **claude**.
  - **apex** — autonomous end-to-end one-shot (design → risk gate → implement loop → AC-verify → ship) in a single sustained run. Pick when the build is **bounded, the user is present**, and one managed run can carry it to ship. Hands off to `/nexus apex`.
  - Decision aid — **orbit when unattended/resumable/goal-style autonomy is the point; apex when a single bounded present run suffices.** Both consume the locked spec's L3 ACs as their verification contract.
  - Fallbacks (supervised, not autonomous): `/nexus feature` (guided single build), `/nexus acceptance` (Tier-S proof-carrying merge), `/nexus essential`/`killer` if the verdict on *which* feature is still open.
- Emit the chosen path as a **handoff recommendation, not execution** — `spec` itself **writes no code**; it is the upstream of the build recipes, mirroring `charter → enact`. (Under `AUTORUN_FULL`/`AUTORUN` the build-path selection is still a contract-level checkpoint and cannot be auto-picked.)

---

## Draft persistence & resume

`spec`'s value is a long multi-turn dialogue, so it must survive interruption. Its bound is structural, not a rubric loop: the Phase 2 convergence check ends exploration, and the explicit **LOCK gate** ends the recipe (a dialogue that will not converge exits `BLOCK` with the open questions listed, never by burning turns). Each phase's checkpoint bullet above already states what gets written to `docs/specs/<slug>.draft.md` at that boundary (plus a **current-phase marker** and the **Assumption Ledger** delta per `reference/dialogue-protocol.md` §3, and the Phase 5 promote-and-archive step) — this section covers only resume-specific behavior:

- **Invocation forms:** `spec` (new dialogue) · `spec resume [<slug>]` (re-enter from the last checkpoint; `<slug>` omitted → most-recent draft) · `spec <slug-or-path>` (re-open a locked spec for revision — re-enters at SPECIFY and re-runs the lock preconditions before re-locking).
- **Resume behavior:** read the draft, replay the current-phase marker, summarize decisions-so-far back to the user in 3-5 lines for confirmation, then continue the dialogue from that checkpoint. Never silently restart from FRAME.

## Spec Quality Gate (lock precondition)

Before sign-off, the spec is adversarially reviewed **as an artifact by an independent agent** — Judge[claude spec-as-artifact review] (+Attest for AC verifiability, +Magi when requirements trade off). "Independent" is load-bearing: the spec's author never scores its own gate (Q9), and the gate is never implemented by telling the authoring agent to re-check itself (P9). The gate scores six dimensions; each must pass, or its finding is explicitly downgraded into Open Questions (never silently passed):

| Dimension | Question |
|-----------|----------|
| Ambiguity | Is any requirement/AC open to more than one reasonable interpretation? |
| Completeness | Does every in-scope requirement have ≥ 1 L3 AC? (L1↔L3 coverage) |
| Consistency | Do scope, requirements, and ACs contradict each other anywhere? |
| Testability | Is every AC verifiable by a machine or a human (Attest)? |
| Scope coherence | Are in-scope / out-of-scope collectively exhaustive and mutually exclusive? |
| Provenance | Is every load-bearing element `elicited` / `ratified` / `parked` — none `silent`? (Provenance Gate, `reference/dialogue-protocol.md` D16; open `ASSUME-n` entries are walked with the user here) |

A gate failure routes back to SPECIFY for a fix, or — with the user's agreement — the gap is parked in Open Questions. The gate is a **lock precondition**: AUTORUN cannot skip it.

### Pre-lock refutation panel (refute-polarity)

The six dimensions above audit the spec **as a document**. They do not ask the harder question: *should this be locked at all?* A spec that is internally consistent, fully traceable, and completely wrong passes all six. So before sign-off, a skeptic panel runs per `_common/ADVERSARIAL_REFUTATION.md` — **refute-polarity, 2-3 independent skeptics, engine-diverse where available**, each prompted to kill the spec rather than evaluate it. `spec`'s specialization is the four **load-bearing claims** a locked spec silently asserts:

| Claim under attack | Skeptic angle |
|--------------------|---------------|
| **The problem is real** | "the stated pain is assumed, not evidenced — no user, telemetry, or research anchor backs it" |
| **This direction beats the rejected ones** | "a direction dropped in CHALLENGE is strictly better under the stated constraints" (re-opens the considered-but-rejected list against the *final* scope, which moved after the pick) |
| **The ACs actually prove the requirements** | "AC-n passes on an implementation that does not satisfy REQ-m" — a green AC that does not entail its requirement is the most expensive defect a spec can ship |
| **The scope boundary holds** | "an out-of-scope item is load-bearing for an in-scope requirement" (the boundary is not actually separable) |

Aggregation follows the protocol §4: **majority refuted-on-evidence → back to CHALLENGE or SPECIFY** (not a park); majority **merely-unproven-because-new → LOCK-with-flag**, the flag recorded in Open Questions with the assumption it rests on. The evidence-vs-novelty discipline (§2) is load-bearing here — a genuinely novel feature must not be blocked for lacking evidence that can only exist after it ships; only an evidence-based refutation blocks. Hard exclusions per §5 apply unchanged.

Panel size scales with depth mode (§ Depth modes): `light` skips the panel, `standard` runs 2 skeptics on claims 1 and 3, `deep` runs 3 across all four claims.

## Spec document template (`docs/specs/<slug>.md`)

Both the draft and the locked spec follow one structure, so downstream `feature`/`apex`/`orbit` consume it without re-parsing prose:

- **Metadata** — slug · feature title · status (`draft` | `locked`) · owner · build-path decision (filled at LOCK).
- **L0 — Vision** — problem · audience (who) · job-to-be-done · success definition.
- **L1 — Requirements** — functional + non-functional, each with a stable ID.
- **L2 — Detail** — per component/team; API (Gateway) and data-model (Schema) detail when relevant.
- **L3 — Acceptance Criteria** — testable, each with a traceable ID (`AC-n`) **mapped to the L1 requirement it verifies**.
- **Scope** — in-scope / out-of-scope (collectively exhaustive, mutually exclusive).
- **Considered but rejected** — directions dropped in CHALLENGE, one-line why (so revision/resume does not re-derive them).
- **Open Questions / Deferred Decisions** — parked items, incl. downgraded Quality-Gate findings.
- **Build-path decision** — orbit (engine: claude | codex | agy) | apex | fallback, recorded at LOCK.

The L1↔L3 traceability (every requirement has an AC; every AC maps to a requirement) is exactly what the Quality Gate's Completeness check verifies and what the build recipes use as their verification contract.

## Handoff contract (what the build recipes receive)

`spec` is upstream of `apex` / `orbit` / `feature` / `acceptance`, and a handoff that ships only a file path forces the downstream recipe to re-derive what the dialogue already settled. The **Spec Handoff Packet** is the contract — emitted at LOCK, consumed without re-parsing prose:

| Field | Content | Consumed by |
|-------|---------|-------------|
| `spec_path` | the locked `docs/specs/<slug>.md` (status `locked`) | all |
| `acceptance_criteria` | the L3 AC set with IDs + L1 mapping + **must-have flags** | `apex` Phase 4→Ship gate (attest threshold), `orbit` completion oracle, `acceptance` Layer A |
| `non_goals` | out-of-scope list, verbatim | scope-bound field of every downstream spawn (P8) |
| `assumption_ledger` | open `ASSUME-n` entries + their provenance status | `apex` Phase 5 Risk Gate, `omen` pre-mortem input |
| `open_questions` | parked items incl. downgraded Quality-Gate findings | Decision Ledger seed (Q4-Q6) — never silently dropped downstream |
| `refutation_flags` | any `LOCK-with-flag` claim + the assumption it rests on | `apex` Risk Gate; becomes a kill-criterion candidate |
| `reuse_findings` | Lens's existing-asset/constraint map from FRAME | `apex` Phase 1 Discovery (skips re-scanning), `feature` Lens step |
| `build_path` | `orbit` (+ executor engine) \| `apex` \| fallback, as decided at LOCK | dispatch |

**Contract rule:** a downstream recipe that receives the packet **does not re-open the settled decisions** — it may surface a contradiction it discovers against real code, but re-litigating the direction is drift (Q7). Conversely, a downstream recipe that finds a **must-have AC unbuildable as written** returns to `spec <slug>` for revision (re-entering at SPECIFY, re-running the lock preconditions) rather than quietly reinterpreting it.

## Boundaries

- **vs `essential` / `killer`** — those deliver a *verdict* (which ONE feature to build) with minimal dialogue (a single closing AskUserQuestion). `spec` is the *deep multi-turn dialogue* that takes an already-chosen-ish idea and refines it into a full locked spec. Natural pairing: `essential`/`killer` decides *what*, then `spec` shapes the *how* into a buildable spec.
- **vs `feature` / `apex` / `orbit`** — those *build code*. `spec` stops at the spec and, at the LOCK build-path checkpoint, hands off to one of them. (`apex` does its own lightweight discovery→spec inline and ships in one bounded run; `orbit` turns the locked spec's L3 ACs into a `nexus-autoloop` completion contract for unattended/resumable building; choose `spec` when the user wants to **deliberate the spec in conversation** and stop there, then `orbit` for a self-driving loop or `apex` for a single present run.)
- **vs `charter`** — `charter` reads a *whole repository* and produces a team-design document; `spec` takes *one feature idea* and produces *one feature spec* through dialogue.
- **vs `converge`** — `converge` is an *automated* generator-evaluator grading loop (machine rubric); `spec` is *human* dialogue with no automated grader.
- **vs `flux` (agent)** — `flux` is a single-agent brainstorm with no finalized artifact; `spec` orchestrates Flux + Flux + Magi + Void + Spark + Scribe[unified] into a signed-off spec, with the user steering throughout.
- **vs `scribe[unified]` / `scribe` (agents)** — those *author* spec documents; `spec` drives the upstream discovery dialogue that decides *what* to specify, then uses them in Phase 4.

## Scale
**3-12 agents**, multiplied by dialogue turns — depth-dependent: `light` 3-5 · `standard` 5-9 · `deep` 8-12 (Lens reuse-scan in FRAME, Judge in the Quality Gate, and the 2-3 refutation skeptics are the conditional additions). Light by agent count, deliberately heavy by interaction turns — the value is in the conversation depth, not fan-out.

## Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| Spec a half-baked idea | FRAME checkpoint requires a confirmed problem statement before options |
| Endless circling | Phase 2 convergence check + explicit LOCK gate |
| Spec without acceptance criteria | Phase 4 mandates testable L3 ACs as the lock precondition |
| Silently dropped open questions | locked spec carries an explicit Open Questions / Deferred Decisions section |
| Jumping to build | `spec` writes no code; hands off to `feature`/`apex`/`acceptance` |
| Single-pass spec masquerading as dialogue | human-in-the-loop at every phase boundary; AUTORUN cannot skip contract-level checkpoints |
| Reinvent the wheel / out-of-context spec | FRAME's Lens reuse-scan (skipped only for greenfield) |
| Lost dialogue on interruption | incremental draft persistence + `spec resume` |
| Locking a low-quality spec | Spec Quality Gate (6 dimensions) is a lock precondition AUTORUN cannot skip |
| Downstream can't consume the spec | standard template + L1↔L3 AC traceability |
| Silent assumptions inside a signed spec | Assumption Ledger (D9) + Provenance Gate (D16) blocks LOCK on any `silent` element |
| Elicitation-quality failures (wall-of-questions, leading questions, rubber-stamp checkpoints, swallowed vague answers) | dialogue conducted per `reference/dialogue-protocol.md` D1–D15 |
| An internally-perfect but wrong spec (consistent/traceable/testable, yet solving no real problem, or ACs a non-conforming impl passes) | pre-lock refutation panel — the six document dimensions cannot catch this |
| Ceremony driving users away from specifying at all | depth modes scale the dialogue without weakening any lock precondition |
| Downstream re-derives the dialogue | Spec Handoff Packet carries the settled state in machine-consumable fields |
| Downstream silently reinterprets an unbuildable AC | contract rule routes it back to `spec <slug>` for revision |

## Shared protocols

- **Dialogue conduct** → `reference/dialogue-protocol.md` (D1–D16: question craft, answer processing, Assumption Ledger, checkpoint presentation, engagement calibration, Provenance Gate). `spec` cites it rather than re-deriving elicitation rules; only the spec-specific specializations (which draft sections the Ledger lives in, Provenance as a sixth Quality-Gate dimension) are stated here.
- **Adversarial refutation** → `_common/ADVERSARIAL_REFUTATION.md` (panel composition, engine diversity, evidence-vs-novelty, polarity, aggregation, hard exclusions). `spec` keeps only its specialization: the four load-bearing claims, refute-polarity, and the depth-scaled panel size.
- **Traceability** → `_common/TRACEABILITY.md` — canonical `REQ-n` / `AC-n` ID discipline that the L1↔L3 mapping and the Handoff Packet's `acceptance_criteria` field depend on.
- **Document quality** → `reference/doc-quality-protocol.md` — the locked spec is a document deliverable; the Spec Quality Gate is its native W12 and adds the spec-specific dimensions on top.

## Add-ons
+Lens (reuse-scan + constraint grounding in FRAME on an existing codebase; skip greenfield), +Field (real user-research grounding in FRAME), +Compete (market/differentiation framing in EXPAND), +Cast (persona grounding when the audience is unclear), +Rank (MoSCoW ordering of sub-features in SHAPE), +Omen (pre-mortem before LOCK on high-stakes specs), +Echo (usability sanity-pass when there is a UI surface), +Gateway/Schema (API/data-model detail in SPECIFY), +Judge (spec-as-artifact adversarial review in the Spec Quality Gate).

## Chain template
`FRAME (Echo[demand] +Field?/Cast? +Lens?[reuse-scan/constraints] + ✓depth-mode + Socratic dialogue) → ✓confirm-problem + draft-init → EXPAND (Flux ‖ Flux +Compete?) → ✓steer + draft → CHALLENGE (Magi + Void + Ripple +Omen?) → ✓pick + convergence-check + draft → SHAPE (Spark +Rank?) → ✓edit + draft → SPECIFY (Scribe[unified] +Scribe?/Gateway?/Schema? +Attest? +Echo?) → ✓iterate + draft → LOCK (✓quality-gate: Judge +Attest +Magi? → ✓refutation-panel: 2-3 skeptics [skipped at depth=light] → ✓sign-off → promote draft to docs/specs/<slug>.md → ✓build-path: orbit loop (✓engine: claude|codex|agy) ‖ apex (fallbacks: feature|acceptance|essential|killer) → emit Spec Handoff Packet) [NO CODE]`

Gate content is not restated here — the six Quality-Gate dimensions live in § Spec Quality Gate, the panel's polarity + four load-bearing claims in § Pre-lock refutation panel, and the mandatory traceable L3 ACs in Phase 4 SPECIFY.

Resumable: `spec resume [<slug>]` re-enters from the draft's current-phase marker; `spec <slug-or-path>` re-opens a locked spec for revision (re-enters at SPECIFY, re-runs the lock preconditions).
