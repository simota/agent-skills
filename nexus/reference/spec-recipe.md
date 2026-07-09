# `spec` — Interactive feature-proposal → locked specification

**Purpose:** Full phase contract for the `spec` Recipe — take a rough feature idea and refine it **through deep human-in-the-loop dialogue** into a finalized, acceptance-criteria-bearing specification. **Stops at the spec document; writes no code.** The discovery-and-finalize half of `spec → feature`/`apex`, analogous to `charter → enact`.

**Read when:** Executing the `spec` Recipe.

---

## What `spec` is for

A user has a feature idea — possibly vague ("I want notifications") — and wants to **think it through thoroughly in conversation** until there is a spec solid enough to build from. The deliverable is not a verdict and not code: it is a **locked specification** the user explicitly signs off on.

`spec` is the recipe whose **deliverable is the dialogue itself**. Where every other recipe treats user confirmation as a gate around autonomous work, `spec` inverts it: the back-and-forth IS the work, and the spec document is its crystallized output.

### Default Mode: `INTERACTIVE` (exceptional)

`spec` is one of two Recipes (with `delve`) that default to `INTERACTIVE` instead of `AUTORUN_FULL` — `spec` shapes a *new* feature, `delve` excavates an *existing* one. The phase-boundary dialogue checkpoints below are **part of the recipe contract, not the Mode** — so even if `spec` is invoked under `AUTORUN_FULL`/`AUTORUN`, it still stops at each checkpoint for the user to steer. (Recipes = task shape; Modes = execution control; `spec`'s checkpoints are contract-level.) `GUIDED` is acceptable for a lighter touch (confirm only at FRAME / CHALLENGE-pick / LOCK); never silently drop a checkpoint.

---

## Phase contract

`FRAME → EXPAND → CHALLENGE → SHAPE → SPECIFY → LOCK`

### Phase 0 — FRAME (problem before solution)
Establish the shared problem statement **before** any option generation. Plea[claude latent-needs/pain-extraction] surfaces the real job-to-be-done; +Field[claude user-research grounding] when research data exists; +Cast[claude persona] when the audience is unclear. **+Lens[claude reuse-scan] on an existing codebase (skip greenfield):** before fixing the problem, survey what already ships — does a comparable feature/module/pattern already exist, which assets are reusable, and what technical constraints (current stack, data model, integration points) bound the solution. This grounds the spec in the real codebase and prevents an out-of-context spec that re-derives shipped code. Nexus drives Socratic clarification with the user — conducted per `reference/dialogue-protocol.md` (D1–D8: one focus per turn, recognition over recall, concrete anchors, tacit-knowledge probes, paraphrase-back before persisting) — covering: who is this for, what job does it do, what does success look like, what is explicitly out of scope, what constraints (tech / time / compliance) bound it. All dialogue throughout the recipe follows that protocol: checkpoints per D10–D12 (envelope / delta-only / orientation line), engagement calibration per D13–D15, and undecided gaps tracked in the draft's **Assumption Ledger** (D9).
- **Checkpoint (mandatory):** present a 3-5 line problem statement (carrying any reuse/constraint findings from Lens); the user confirms or corrects it. Option generation **cannot start** until the problem statement is confirmed. (Prevents "spec a half-baked idea".)
- **Draft init:** on problem-statement confirmation, write the initial `docs/specs/<slug>.draft.md` (status `draft`, L0 Vision + reuse/constraint findings filled). See **Draft persistence & resume**.

### Phase 1 — EXPAND (diverge)
Generate the option space. Riff[claude Expand/Propose modes — iterative dialogue] ‖ Flux[claude challenge-assumptions / cross-domain reframes]. Produce **3-5 candidate directions**, each with a one-line rationale and rough shape. +Compete[claude+WebSearch] when market/differentiation framing matters.
- **Checkpoint:** present the candidates; the user reacts, eliminates, combines, or adds. Expect **multiple turns** here — this is the divergent heart of the dialogue. Do not converge prematurely. On checkpoint pass, append the surviving candidates to the draft.

### Phase 2 — CHALLENGE (stress-test + converge)
Narrow to ONE direction *with the user*. Magi[claude multi-perspective necessity/trade-off arbitration] + Void[claude subtract scope / YAGNI] + Ripple[claude feasibility/impact] + Omen[claude pre-mortem on the leading candidate when stakes are high]. Each surfaces a distinct pressure: is it necessary, is it over-scoped, is it feasible, how does it fail.
- **Checkpoint (mandatory):** the user makes the **explicit pick** of the single direction to specify. Carry forward rejected directions as recorded "considered but rejected" so the dialogue does not re-derive them. Record the pick and the considered-but-rejected list to the draft.
- **Convergence check:** before looping back to EXPAND, Nexus asks "are we converging, or circling?" If circling ≥ 2 rounds with no new information, offer to (a) lock the leading candidate, or (b) park the disagreement as an Open Question and proceed. Never loop indefinitely.

### Phase 3 — SHAPE (proposal)
Spark[claude feature-proposal] synthesizes the chosen direction into a structured proposal: problem → proposed solution → in-scope → out-of-scope → assumptions → open questions. +Rank[claude] when the direction decomposes into sub-features needing MoSCoW ordering.
- **Checkpoint:** present the proposal; capture the user's edits section by section, then write the agreed proposal sections to the draft.

### Phase 4 — SPECIFY (authoring with mandatory acceptance criteria)
Accord[claude staged elaboration: L0 Vision → L1 Requirements → L2 Detail → L3 Acceptance Criteria] as the spine; +Scribe[claude PRD/SRS/HLD] for narrative spec sections; +Gateway/Schema[claude] when the spec needs API/data-model detail. Author against the **Spec document template** (below) so the artifact is downstream-consumable, and iterate with the user **section by section**, persisting each agreed section to the draft.
- Give every L3 acceptance criterion a **traceable ID (`AC-1`, `AC-2`, …)** mapped to the L1 requirement it verifies — this traceability is what the Spec Quality Gate's Completeness check verifies and what `feature`/`apex`/`orbit` consume as their verification contract.
- **Lock preconditions (both mandatory, verified at LOCK):** (1) the spec carries **testable L3 acceptance criteria** (the difference between a spec and a wish) — +Attest[claude] sanity-checks that each AC is actually verifiable; (2) the spec **passes the Spec Quality Gate** (below). +Echo[claude] for a quick usability sanity-pass on the shaped flow when there is a UI surface.

### Phase 5 — LOCK (sign-off + persist, no code)
**Gate:** do not present for sign-off until **both lock preconditions pass** — testable L3 ACs (Attest) **and** the Spec Quality Gate (below). Then present the complete spec and require the user's **explicit sign-off** ("lock it"). On sign-off:
- **Finalize the draft:** promote `docs/specs/<slug>.draft.md` to the locked `docs/specs/<feature-slug>.md` (status `locked`; override path on request), following the **Spec document template**. Include an explicit **Open Questions / Deferred Decisions** section — parked items (including any Quality-Gate findings downgraded rather than fixed) are recorded, never silently dropped. Archive or remove the `.draft.md` once promoted.
- **Build-path selection (mandatory checkpoint):** before recommending a handoff, ask the user **how** they want the locked spec built. Present the two autonomous build paths as the headline choice, with the supervised recipes as fallbacks:
  - **orbit loop** — turn the spec into a `nexus-autoloop` runner: the spec's L3 acceptance criteria become the loop's completion contract (machine-checkable DONE gate), with operation contract, resumable state, and recovery. Pick when the build is **long-running / unattended / multi-session**, benefits from checkpoint-resume, or the user wants a self-driving runner they can leave alone. Hands off to the `orbit` agent (loop generation) — see `~/.claude/skills/orbit/SKILL.md`.
    - **Executor-engine sub-choice (when orbit is picked):** select which CLI runs each loop iteration — **claude** (Claude Code; default, broadest tool/skill access), **codex** (Codex CLI; latest gpt-5.6 generation — build loops run `gpt-5.6-terra`, requires `multi_agent=true` + `[agents] max_depth >= 2`), or **agy** (Antigravity CLI; headless needs a real pty + artifact capture). Orbit wires the choice into the generated runner's `EXEC_CMD` / engine flags — see `~/.claude/skills/orbit/reference/executor-engines.md`. Pass the picked engine in the orbit handoff so the runner is generated for the right CLI; before handing off, note the engine's prereqs (Codex spawn-depth, agy pty) per `_common/CLI_COMPATIBILITY.md`. If unsure, default **claude**.
  - **apex** — autonomous end-to-end one-shot (design → risk gate → implement loop → AC-verify → ship) in a single sustained run. Pick when the build is **bounded, the user is present**, and one managed run can carry it to ship. Hands off to `/nexus apex`.
  - Decision aid — **orbit when unattended/resumable/goal-style autonomy is the point; apex when a single bounded present run suffices.** Both consume the locked spec's L3 ACs as their verification contract.
  - Fallbacks (supervised, not autonomous): `/nexus feature` (guided single build), `/nexus acceptance` (Tier-S proof-carrying merge), `/nexus essential`/`killer` if the verdict on *which* feature is still open.
- Emit the chosen path as a **handoff recommendation, not execution** — `spec` itself **writes no code**; it is the upstream of the build recipes, mirroring `charter → enact`. (Under `AUTORUN_FULL`/`AUTORUN` the build-path selection is still a contract-level checkpoint and cannot be auto-picked.)

---

## Draft persistence & resume

`spec`'s value is a long multi-turn dialogue, so it must survive interruption. State is persisted **incrementally** to `docs/specs/<slug>.draft.md` — not only at the end.

- **Incremental writes:** at each phase checkpoint pass, append/update the matching draft section (FRAME → L0 Vision + reuse/constraint findings; EXPAND → surviving candidates; CHALLENGE → pick + considered-but-rejected; SHAPE → proposal; SPECIFY → L1/L2/L3 + open questions; every phase → **Assumption Ledger** delta per `reference/dialogue-protocol.md` §3). The draft also records a **current-phase marker** so a resume knows where to re-enter.
- **Invocation forms:** `spec` (new dialogue) · `spec resume [<slug>]` (re-enter from the last checkpoint; `<slug>` omitted → most-recent draft) · `spec <slug-or-path>` (re-open a locked spec for revision — re-enters at SPECIFY and re-runs the lock preconditions before re-locking).
- **Resume behavior:** read the draft, replay the current-phase marker, summarize decisions-so-far back to the user in 3-5 lines for confirmation, then continue the dialogue from that checkpoint. Never silently restart from FRAME.
- **Finalize:** on LOCK the draft is promoted to the locked spec and the `.draft.md` archived/removed (Phase 5).

## Spec Quality Gate (lock precondition)

Before sign-off, the spec is adversarially self-reviewed **as an artifact** — Judge[claude spec-as-artifact review] (+Attest for AC verifiability, +Magi when requirements trade off). The gate scores six dimensions; each must pass, or its finding is explicitly downgraded into Open Questions (never silently passed):

| Dimension | Question |
|-----------|----------|
| Ambiguity | Is any requirement/AC open to more than one reasonable interpretation? |
| Completeness | Does every in-scope requirement have ≥ 1 L3 AC? (L1↔L3 coverage) |
| Consistency | Do scope, requirements, and ACs contradict each other anywhere? |
| Testability | Is every AC verifiable by a machine or a human (Attest)? |
| Scope coherence | Are in-scope / out-of-scope collectively exhaustive and mutually exclusive? |
| Provenance | Is every load-bearing element `elicited` / `ratified` / `parked` — none `silent`? (Provenance Gate, `reference/dialogue-protocol.md` D16; open `ASSUME-n` entries are walked with the user here) |

A gate failure routes back to SPECIFY for a fix, or — with the user's agreement — the gap is parked in Open Questions. The gate is a **lock precondition**: AUTORUN cannot skip it.

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

## Boundaries

- **vs `essential` / `killer`** — those deliver a *verdict* (which ONE feature to build) with minimal dialogue (a single closing AskUserQuestion). `spec` is the *deep multi-turn dialogue* that takes an already-chosen-ish idea and refines it into a full locked spec. Natural pairing: `essential`/`killer` decides *what*, then `spec` shapes the *how* into a buildable spec.
- **vs `feature` / `apex` / `orbit`** — those *build code*. `spec` stops at the spec and, at the LOCK build-path checkpoint, hands off to one of them. (`apex` does its own lightweight discovery→spec inline and ships in one bounded run; `orbit` turns the locked spec's L3 ACs into a `nexus-autoloop` completion contract for unattended/resumable building; choose `spec` when the user wants to **deliberate the spec in conversation** and stop there, then `orbit` for a self-driving loop or `apex` for a single present run.)
- **vs `charter`** — `charter` reads a *whole repository* and produces a team-design document; `spec` takes *one feature idea* and produces *one feature spec* through dialogue.
- **vs `converge`** — `converge` is an *automated* generator-evaluator grading loop (machine rubric); `spec` is *human* dialogue with no automated grader.
- **vs `riff` (agent)** — `riff` is a single-agent brainstorm with no finalized artifact; `spec` orchestrates Riff + Flux + Magi + Void + Spark + Accord into a signed-off spec, with the user steering throughout.
- **vs `accord` / `scribe` (agents)** — those *author* spec documents; `spec` drives the upstream discovery dialogue that decides *what* to specify, then uses them in Phase 4.

## Scale
3-9 agents (Lens reuse-scan in FRAME and Judge in the Quality Gate are conditional add-ons), multiplied by dialogue turns. Light by agent count, deliberately heavy by interaction turns — the value is in the conversation depth, not fan-out.

## Anti-patterns prevented
1. **Spec a half-baked idea** — FRAME checkpoint requires a confirmed problem statement before options.
2. **Endless circling** — Phase 2 convergence check + explicit LOCK gate bound the dialogue.
3. **Spec without acceptance criteria** — Phase 4 mandates testable L3 ACs as the lock precondition.
4. **Silently dropped open questions** — the locked spec carries an explicit Open Questions / Deferred Decisions section.
5. **Jumping to build** — `spec` writes no code; it hands off to `feature`/`apex`/`acceptance`.
6. **Single-pass spec masquerading as dialogue** — human-in-the-loop at every phase boundary; AUTORUN cannot skip the contract-level checkpoints.
7. **Reinvent the wheel / out-of-context spec** — FRAME's Lens reuse-scan surfaces existing assets and codebase constraints before the problem is fixed (skipped only for greenfield).
8. **Lost dialogue on interruption** — incremental draft persistence + `spec resume` re-enter from the last checkpoint instead of restarting.
9. **Locking a low-quality spec** — the Spec Quality Gate (ambiguity / completeness / consistency / testability / scope / provenance) is a lock precondition AUTORUN cannot skip.
10. **Downstream can't consume the spec** — the standard template + L1↔L3 AC traceability give `feature`/`apex`/`orbit` a machine-consumable verification contract.
11. **Silent assumptions inside a signed spec** — the Assumption Ledger (D9) tracks every gap the user did not explicitly decide; the Provenance Gate (D16) blocks LOCK while any load-bearing element is `silent`.
12. **Elicitation-quality failures** (wall-of-questions turns, leading questions at divergence, rubber-stamp checkpoints, vague answers swallowed as consent) — the dialogue itself is conducted per `reference/dialogue-protocol.md` D1–D15.

## Shared protocols

- **Dialogue conduct** → `reference/dialogue-protocol.md` (D1–D16: question craft, answer processing, Assumption Ledger, checkpoint presentation, engagement calibration, Provenance Gate). `spec` cites it rather than re-deriving elicitation rules; only the spec-specific specializations (which draft sections the Ledger lives in, Provenance as a sixth Quality-Gate dimension) are stated here.

## Add-ons
+Lens (reuse-scan + constraint grounding in FRAME on an existing codebase; skip greenfield), +Field (real user-research grounding in FRAME), +Compete (market/differentiation framing in EXPAND), +Cast (persona grounding when the audience is unclear), +Rank (MoSCoW ordering of sub-features in SHAPE), +Omen (pre-mortem before LOCK on high-stakes specs), +Echo (usability sanity-pass when there is a UI surface), +Gateway/Schema (API/data-model detail in SPECIFY), +Judge (spec-as-artifact adversarial review in the Spec Quality Gate).

## Chain template
`FRAME (Plea +Field?/Cast? +Lens?[reuse-scan/constraints] + Socratic dialogue) → ✓confirm-problem + draft-init → EXPAND (Riff ‖ Flux +Compete?) → ✓steer + draft → CHALLENGE (Magi + Void + Ripple +Omen?) → ✓pick + convergence-check + draft → SHAPE (Spark +Rank?) → ✓edit + draft → SPECIFY (Accord +Scribe?/Gateway?/Schema?, L3 ACs with traceable IDs mandatory, Attest? +Echo?) → ✓iterate + draft → LOCK (✓quality-gate: Judge spec-as-artifact +Attest +Magi? — ambiguity/completeness/consistency/testability/scope/provenance[D16 + walk open ASSUME-n] → ✓sign-off → promote draft to docs/specs/<slug>.md per template + Open Questions section → ✓build-path: orbit loop (✓engine: claude|codex|agy) ‖ apex (fallbacks: feature|acceptance|essential|killer) → recommend chosen handoff) [NO CODE]`

Resumable: `spec resume [<slug>]` re-enters from the draft's current-phase marker; `spec <slug-or-path>` re-opens a locked spec for revision (re-enters at SPECIFY, re-runs the lock preconditions).
