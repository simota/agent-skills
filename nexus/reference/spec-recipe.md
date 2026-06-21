# `spec` — Interactive feature-proposal → locked specification

**Purpose:** Full phase contract for the `spec` Recipe — take a rough feature idea and refine it **through deep human-in-the-loop dialogue** into a finalized, acceptance-criteria-bearing specification. **Stops at the spec document; writes no code.** The discovery-and-finalize half of `spec → feature`/`apex`, analogous to `charter → enact`.

**Read when:** Executing the `spec` Recipe.

---

## What `spec` is for

A user has a feature idea — possibly vague ("I want notifications") — and wants to **think it through thoroughly in conversation** until there is a spec solid enough to build from. The deliverable is not a verdict and not code: it is a **locked specification** the user explicitly signs off on.

`spec` is the recipe whose **deliverable is the dialogue itself**. Where every other recipe treats user confirmation as a gate around autonomous work, `spec` inverts it: the back-and-forth IS the work, and the spec document is its crystallized output.

### Default Mode: `INTERACTIVE` (exceptional)

`spec` is the one Recipe that defaults to `INTERACTIVE` instead of `AUTORUN_FULL`. The phase-boundary dialogue checkpoints below are **part of the recipe contract, not the Mode** — so even if `spec` is invoked under `AUTORUN_FULL`/`AUTORUN`, it still stops at each checkpoint for the user to steer. (Recipes = task shape; Modes = execution control; `spec`'s checkpoints are contract-level.) `GUIDED` is acceptable for a lighter touch (confirm only at FRAME / CHALLENGE-pick / LOCK); never silently drop a checkpoint.

---

## Phase contract

`FRAME → EXPAND → CHALLENGE → SHAPE → SPECIFY → LOCK`

### Phase 0 — FRAME (problem before solution)
Establish the shared problem statement **before** any option generation. Plea[claude latent-needs/pain-extraction] surfaces the real job-to-be-done; +Field[claude user-research grounding] when research data exists; +Cast[claude persona] when the audience is unclear. Nexus drives Socratic clarification with the user: who is this for, what job does it do, what does success look like, what is explicitly out of scope, what constraints (tech / time / compliance) bound it.
- **Checkpoint (mandatory):** present a 3-5 line problem statement; the user confirms or corrects it. Option generation **cannot start** until the problem statement is confirmed. (Prevents "spec a half-baked idea".)

### Phase 1 — EXPAND (diverge)
Generate the option space. Riff[claude Expand/Propose modes — iterative dialogue] ‖ Flux[claude challenge-assumptions / cross-domain reframes]. Produce **3-5 candidate directions**, each with a one-line rationale and rough shape. +Compete[claude+WebSearch] when market/differentiation framing matters.
- **Checkpoint:** present the candidates; the user reacts, eliminates, combines, or adds. Expect **multiple turns** here — this is the divergent heart of the dialogue. Do not converge prematurely.

### Phase 2 — CHALLENGE (stress-test + converge)
Narrow to ONE direction *with the user*. Magi[claude multi-perspective necessity/trade-off arbitration] + Void[claude subtract scope / YAGNI] + Ripple[claude feasibility/impact] + Omen[claude pre-mortem on the leading candidate when stakes are high]. Each surfaces a distinct pressure: is it necessary, is it over-scoped, is it feasible, how does it fail.
- **Checkpoint (mandatory):** the user makes the **explicit pick** of the single direction to specify. Carry forward rejected directions as recorded "considered but rejected" so the dialogue does not re-derive them.
- **Convergence check:** before looping back to EXPAND, Nexus asks "are we converging, or circling?" If circling ≥ 2 rounds with no new information, offer to (a) lock the leading candidate, or (b) park the disagreement as an Open Question and proceed. Never loop indefinitely.

### Phase 3 — SHAPE (proposal)
Spark[claude feature-proposal] synthesizes the chosen direction into a structured proposal: problem → proposed solution → in-scope → out-of-scope → assumptions → open questions. +Rank[claude] when the direction decomposes into sub-features needing MoSCoW ordering.
- **Checkpoint:** present the proposal; capture the user's edits section by section.

### Phase 4 — SPECIFY (authoring with mandatory acceptance criteria)
Accord[claude staged elaboration: L0 Vision → L1 Requirements → L2 Detail → L3 Acceptance Criteria] as the spine; +Scribe[claude PRD/SRS/HLD] for narrative spec sections; +Gateway/Schema[claude] when the spec needs API/data-model detail. Iterate with the user **section by section**.
- **Lock precondition:** the spec is not lockable until it carries **testable L3 acceptance criteria** (the difference between a spec and a wish). +Attest[claude] to sanity-check that each AC is actually verifiable. +Echo[claude] for a quick usability sanity-pass on the shaped flow when there is a UI surface.

### Phase 5 — LOCK (sign-off + persist, no code)
Present the complete spec. Require the user's **explicit sign-off** ("lock it"). On sign-off:
- Write the finalized spec to `docs/specs/<feature-slug>.md` (override path on request). Include an explicit **Open Questions / Deferred Decisions** section — parked items are recorded, never silently dropped.
- **Build-path selection (mandatory checkpoint):** before recommending a handoff, ask the user **how** they want the locked spec built. Present the two autonomous build paths as the headline choice, with the supervised recipes as fallbacks:
  - **orbit loop** — turn the spec into a `nexus-autoloop` runner: the spec's L3 acceptance criteria become the loop's completion contract (machine-checkable DONE gate), with operation contract, resumable state, and recovery. Pick when the build is **long-running / unattended / multi-session**, benefits from checkpoint-resume, or the user wants a self-driving runner they can leave alone. Hands off to the `orbit` agent (loop generation) — see `/Users/simota/.claude/skills/orbit/SKILL.md`.
    - **Executor-engine sub-choice (when orbit is picked):** select which CLI runs each loop iteration — **claude** (Claude Code; default, broadest tool/skill access), **codex** (Codex CLI; latest model `gpt-5.5`, requires `multi_agent=true` + `[agents] max_depth >= 2`), or **agy** (Antigravity CLI; headless needs a real pty + artifact capture). Orbit wires the choice into the generated runner's `EXEC_CMD` / engine flags — see `/Users/simota/.claude/skills/orbit/reference/executor-engines.md`. Pass the picked engine in the orbit handoff so the runner is generated for the right CLI; before handing off, note the engine's prereqs (Codex spawn-depth, agy pty) per `_common/CLI_COMPATIBILITY.md`. If unsure, default **claude**.
  - **apex** — autonomous end-to-end one-shot (design → risk gate → implement loop → AC-verify → ship) in a single sustained run. Pick when the build is **bounded, the user is present**, and one managed run can carry it to ship. Hands off to `/nexus apex`.
  - Decision aid — **orbit when unattended/resumable/goal-style autonomy is the point; apex when a single bounded present run suffices.** Both consume the locked spec's L3 ACs as their verification contract.
  - Fallbacks (supervised, not autonomous): `/nexus feature` (guided single build), `/nexus acceptance` (Tier-S proof-carrying merge), `/nexus essential`/`killer` if the verdict on *which* feature is still open.
- Emit the chosen path as a **handoff recommendation, not execution** — `spec` itself **writes no code**; it is the upstream of the build recipes, mirroring `charter → enact`. (Under `AUTORUN_FULL`/`AUTORUN` the build-path selection is still a contract-level checkpoint and cannot be auto-picked.)

---

## Boundaries

- **vs `essential` / `killer`** — those deliver a *verdict* (which ONE feature to build) with minimal dialogue (a single closing AskUserQuestion). `spec` is the *deep multi-turn dialogue* that takes an already-chosen-ish idea and refines it into a full locked spec. Natural pairing: `essential`/`killer` decides *what*, then `spec` shapes the *how* into a buildable spec.
- **vs `feature` / `apex` / `orbit`** — those *build code*. `spec` stops at the spec and, at the LOCK build-path checkpoint, hands off to one of them. (`apex` does its own lightweight discovery→spec inline and ships in one bounded run; `orbit` turns the locked spec's L3 ACs into a `nexus-autoloop` completion contract for unattended/resumable building; choose `spec` when the user wants to **deliberate the spec in conversation** and stop there, then `orbit` for a self-driving loop or `apex` for a single present run.)
- **vs `charter`** — `charter` reads a *whole repository* and produces a team-design document; `spec` takes *one feature idea* and produces *one feature spec* through dialogue.
- **vs `converge`** — `converge` is an *automated* generator-evaluator grading loop (machine rubric); `spec` is *human* dialogue with no automated grader.
- **vs `riff` (agent)** — `riff` is a single-agent brainstorm with no finalized artifact; `spec` orchestrates Riff + Flux + Magi + Void + Spark + Accord into a signed-off spec, with the user steering throughout.
- **vs `accord` / `scribe` (agents)** — those *author* spec documents; `spec` drives the upstream discovery dialogue that decides *what* to specify, then uses them in Phase 4.

## Scale
3-8 agents, multiplied by dialogue turns. Light by agent count, deliberately heavy by interaction turns — the value is in the conversation depth, not fan-out.

## Anti-patterns prevented
1. **Spec a half-baked idea** — FRAME checkpoint requires a confirmed problem statement before options.
2. **Endless circling** — Phase 2 convergence check + explicit LOCK gate bound the dialogue.
3. **Spec without acceptance criteria** — Phase 4 mandates testable L3 ACs as the lock precondition.
4. **Silently dropped open questions** — the locked spec carries an explicit Open Questions / Deferred Decisions section.
5. **Jumping to build** — `spec` writes no code; it hands off to `feature`/`apex`/`acceptance`.
6. **Single-pass spec masquerading as dialogue** — human-in-the-loop at every phase boundary; AUTORUN cannot skip the contract-level checkpoints.

## Add-ons
+Field (real user-research grounding in FRAME), +Compete (market/differentiation framing in EXPAND), +Cast (persona grounding when the audience is unclear), +Rank (MoSCoW ordering of sub-features in SHAPE), +Omen (pre-mortem before LOCK on high-stakes specs), +Echo (usability sanity-pass when there is a UI surface), +Gateway/Schema (API/data-model detail in SPECIFY).

## Chain template
`FRAME (Plea +Field?/Cast? + Socratic dialogue) → ✓confirm-problem → EXPAND (Riff ‖ Flux +Compete?) → ✓steer → CHALLENGE (Magi + Void + Ripple +Omen?) → ✓pick + convergence-check → SHAPE (Spark +Rank?) → ✓edit → SPECIFY (Accord +Scribe?/Gateway?/Schema? + L3 ACs mandatory, Attest? +Echo?) → ✓iterate → LOCK (✓sign-off → write docs/specs/<slug>.md + Open Questions section → ✓build-path: orbit loop (✓engine: claude|codex|agy) ‖ apex (fallbacks: feature|acceptance|essential|killer) → recommend chosen handoff) [NO CODE]`
