# `delve` — Existing-feature deep-dive → evolution-direction dialogue

**Purpose:** Full phase contract for the `delve` Recipe — take an **already-shipped feature**, excavate it through dialogue past *what it does* to *what is really going on*, surface non-obvious **insights**, and chart **evolution directions** (deepen / broaden / reframe). **Stops at the Evolution Map; writes no code.** The existing-feature, insight-producing analog of `spec` (which shapes a *new* idea) and of `gedanken` (which reasons about an *abstract* hypothetical) — the discovery half of `delve → spec`/`kaizen`/`feature`/`apex`.

**Read when:** Executing the `delve` Recipe. Authored to `reference/recipe-contract.md` (all 8 elements).

---

## What `delve` is for

A user has a **feature that already ships** and the sense that there is *more here* — untapped value, a misunderstood role, an adjacent job it half-serves — and wants to **think it through in conversation** until they have new insight and a set of evolution directions worth pursuing. The deliverable is not code and not a verdict: it is an **Evolution Map** — validated insights about the feature, plus ranked directions to evolve it, each tagged with its axis and a recommended next recipe.

`delve` exists because *deepening an existing feature has a method* distinct from inventing a new one. `spec` starts from a rough idea and converges it to a buildable spec; `kaizen` improves a feature against a fixed quantified target; neither **excavates a shipped feature for the non-obvious truths that reveal where it should evolve**. That excavation is exactly a controlled multi-agent protocol: ground in the real implementation and usage → dig beneath the surface → synthesize insights → diverge to directions → refute → chart. It is the **grounded-existing-feature** member of the Reason family, where `gedanken` is the **abstract-hypothetical** member.

### Default Mode: `INTERACTIVE` (with `spec`)

Like `spec`, `delve` defaults to `INTERACTIVE` — it is one of the two dialogue recipes (`spec` shapes a *new* feature; `delve` excavates an *existing* one). The phase-boundary dialogue checkpoints below are **part of the recipe contract, not the Mode**, so even if `delve` is invoked under `AUTORUN_FULL`/`AUTORUN` it still stops at the **three knowledge-junctures** where the user's tacit knowledge of their own feature is load-bearing: **GROUND** (confirm the feature-as-is), **SURFACE** (validate the insights), **CHART** (pick the directions). Under `INTERACTIVE` the remaining phase boundaries (EXCAVATE / DIVERGE / REFUTE) also become steer points; `GUIDED` is acceptable for a lighter touch (confirm only at the three contract-level checkpoints — never silently drop one). The autonomous excavation work — mapping the implementation, reading usage, challenging baked-in assumptions — still runs without stopping *between* checkpoints. There is **no confirm/safety gate for destructive actions**: `delve` writes no code and ships nothing (same posture as `gedanken`/`spec`/`charter`).

---

## Phase contract

`GROUND → EXCAVATE → SURFACE → DIVERGE → REFUTE → CHART`

### Phase 1 — GROUND (the feature as-is + its reason-for-existence)
Establish what the feature **is today** before exploring what it could become — excavating an imagined feature is the recipe's first failure mode. `Lens`[map the current implementation — structure, responsibility, data flow] unconditionally; +`Pulse`/`Trace`/`Voice`[usage telemetry / session-replay / sentiment] when that data exists; +`Plea`[the job-to-be-done lens — what user need the feature serves]. The feature's **reason-for-existence** — *why* it was originally built and what intent it encoded — is reconstructed from the user's tacit knowledge in the Socratic clarification + `Lens`'s read of the code, **not** from `Plea` (whose domain is user need, not design history). The user holds that tacit context, so Nexus runs Socratic clarification — conducted per `reference/dialogue-protocol.md` (D1–D8; the D5 **history probe** "what was true when this was built that isn't now?" is the reason-for-existence tool) — covering: who uses it, what job it does, what the original intent was, and what has changed since it shipped. All dialogue throughout the recipe follows that protocol: the three knowledge-juncture checkpoints per D10–D12, engagement calibration per D13–D15, and unvalidated gaps tracked in the draft's **Assumption Ledger** (D9).
- **Checkpoint (contract-level; AUTORUN cannot skip):** present a 3-5 line **feature-as-is** summary (current shape + real usage + reason-for-existence). The user confirms or corrects it. Excavation **cannot start** on a misunderstood feature. (Prevents "deep-dive a strawman of how it actually works".)
- **Draft init:** on confirmation, write `docs/evolution/<feature-slug>.draft.md` (status `draft`, feature-as-is section filled). See **Draft persistence & resume**.

### Phase 2 — EXCAVATE (dig beneath the surface)
The deep-dive proper — go past *what it does* to *what is really going on*. Independent lenses (hub-spoke, no shared mutable state — independence is the point):
- `Plea`[latent / unmet needs the feature gestures at but does not serve]
- `Flux`[challenge the assumptions baked into its current shape — what was taken as true when it was built that may no longer hold]
- `Echo`[walkthrough friction — where users stumble, work around it, or under-use it]
- +`Field`[real user-research grounding], +`Compete`[how others solve this same job — the adjacent value next to it], +`Trace`[where real usage diverges from the designed flow]
- Output: an **excavation set** — the non-obvious observations beneath the surface, each tied to evidence from GROUND.

### Phase 3 — SURFACE (synthesize non-obvious insights)
`Magi`[synthesize the excavation into named insights] + `Spark`[name and frame each insight against the existing data/logic — what is cheaply reachable from it]. An **insight** here is a non-obvious truth about the feature (it is underused *because X*; it is load-bearing in a way nobody noticed; the real job is *Y*, not what was built) — **not a restatement of what the feature does**.
- **Deepening loop (EXCAVATE ↔ SURFACE):** if the insight set is thin or merely restates the obvious, loop back to EXCAVATE to dig a *different* seam. **Termination bound:** `loop ≤ 3 cycles (default 3)` (per recipe-contract §2); exit on `insight-saturation` (a rich, non-obvious set is established — the `ACCEPT` analog) / `diminishing-insight (Δ < ε)` (new digs reveal nothing new) / `cap-reached`. On any non-saturation exit, report the insight set reached **plus which seams remain undug** — never silently stop. The saturation judgment is a **heuristic for how much to dig**, not a quality gate — the lenses that surface insights also judge whether to dig further. The **independent** quality check on the insights themselves is the REFUTE phase (a separate skeptic panel, per `_common/ADVERSARIAL_REFUTATION.md`), where confirmation-reasoning and restatements are actually killed; the loop only decides whether more excavation is worthwhile.
- **Checkpoint (contract-level):** present the insights; the user validates against tacit knowledge (confirms, corrects, or adds — they often know *why* an insight is true or false). Persist confirmed insights to the draft.

### Phase 4 — DIVERGE (evolution directions)
From each validated insight, generate evolution directions along **three axes** — the "evolve & deepen" generation:
| Axis | Move |
|------|------|
| **deepen** | make the core job radically better — go deeper on what the feature already does |
| **broaden** | extend the feature to an adjacent job the insight revealed |
| **reframe** | reconceive what the feature fundamentally *is* |

`Riff`[generate directions iteratively] ‖ `Spark`[directions grounded in the existing data/logic — what is reachable] ‖ `Flux`[reframe / cross-domain transplant]. Each direction is tagged with its **axis** + the **insight it springs from** + a rough shape. Diverge deliberately; do not pre-filter for safety here (the gate, not the generator, decides survival).
- Output: a candidate direction set, axis-tagged and insight-linked.

### Phase 5 — REFUTE (pressure-test insights AND directions)
Two distinct stress tests — a direction built on a refuted insight falls with it:
- **Insight refutation** — a skeptic panel per `_common/ADVERSARIAL_REFUTATION.md` (refute ×2-3, cross-engine for prior-diversity) attacks each insight: is it *actually true*, or did we find the insight we wanted (**confirmation reasoning**)? Did we mistake a restatement for an insight (**no-news**)? Is the pattern real or an artifact of one data slice (**false-pattern**)? Apply the evidence-vs-novelty discipline: "the insight is *wrong*" is a defeater (drop it); "the insight is *unverified-because-we-only-just-noticed-it*" is recorded as a **hypothesis to validate**, not a kill.
- **Direction viability** — `Ripple`[systemic / blast-radius impact of each direction] + `Magi`[arbitrate value × feasibility] +`Omen`?[pre-mortem on a bold reframe before it carries to CHART].
- Output: surviving insights (each with an epistemic status: confirmed / hypothesis) + viable directions; refuted insights and non-viable directions recorded, never silently dropped.

### Phase 6 — CHART (the Evolution Map + handoff, no code)
`Magi`/`Spark` synthesize the **Evolution Map**: validated insights → ranked evolution directions, each carrying its axis (deepen/broaden/reframe), the insight it springs from, a value/effort/confidence read, and **a recommended next recipe**. `Scribe`?[author the report].
- **Per-direction handoff routing:** incremental polish to a known metric → `kaizen`; a direction big enough to need a full spec → `spec`; a clear single build → `feature`; full discovery-to-ship in one run → `apex`; "is this direction THE differentiator?" → `killer`; "is this even must-have?" → `essential`.
- **Provenance check (D16):** before presenting the Map, classify each insight and ranked direction — an insight the user never validated at SURFACE, or a direction resting on it, is `silent` and either gets one targeted validation question or is downgraded to hypothesis; open `ASSUME-n` entries are walked with the user here (ratify or park).
- **Checkpoint (contract-level):** the user picks which direction(s) to pursue; `delve` emits the chosen handoff as a **recommendation, not execution** — it writes no code (mirrors `spec → feature`, `charter → enact`, `gedanken → spec`). Under `AUTORUN_FULL`/`AUTORUN` this pick is still contract-level and cannot be auto-selected.
- **Finalize:** promote `docs/evolution/<feature-slug>.draft.md` to the finalized `docs/evolution/<feature-slug>.md`.

---

## Resume

Draft-resume: `delve`'s value is a multi-turn excavation, so it must survive interruption. State is persisted **incrementally** to `docs/evolution/<feature-slug>.draft.md` — at each phase checkpoint pass, append/update the matching section (GROUND → feature-as-is; EXCAVATE → excavation set; SURFACE → confirmed insights + loop trajectory; DIVERGE → axis-tagged directions; REFUTE → survivors + refuted/recorded; CHART → Evolution Map) with a **current-phase marker**.
- **Invocation forms:** `delve <feature>` (new dive) · `delve resume [<slug>]` (re-enter from the last checkpoint; `<slug>` omitted → most-recent draft) · `delve <slug-or-path>` (re-open a finalized Evolution Map to dive further — re-enters at EXCAVATE).
- **Resume behavior:** read the draft, replay the current-phase marker, summarize decisions-so-far back to the user in 3-5 lines for confirmation, then continue from that checkpoint. Never silently restart from GROUND. On CHART the draft is promoted and the `.draft.md` archived/removed.

## Output — Evolution Map

`NEXUS_COMPLETE` with the base `## Nexus Execution Report` plus the named **Evolution Map**:
- **Feature-as-is** — current shape + real usage + reason-for-existence (GROUND).
- **Excavation set** — the non-obvious observations beneath the surface (EXCAVATE), evidence-tied.
- **Insights** — each named non-obvious truth + its epistemic status (confirmed / hypothesis-to-validate) (SURFACE + REFUTE); loop trajectory + any undug seams.
- **Evolution directions** — ranked, each with: axis (deepen / broaden / reframe) · the insight it springs from · rough shape · value/effort/confidence · **recommended next recipe**.
- **Refuted** — insights that failed and directions that were ruled non-viable, with why (recorded, not dropped).
- **Handoff** — the direction(s) the user picked + the recommended build recipe (no code executed).

## Failure Modes Prevented

| Failure | Mitigation |
|---------|------------|
| **Surface-level deep-dive** (restating what the feature does and calling it insight) | EXCAVATE digs past *what* to *latent/why*; SURFACE distinguishes insight from restatement; REFUTE's no-news angle drops restatements |
| **Deep-dive the wrong feature** (excavating a strawman of how it actually works) | GROUND Lens map + usage data + the contract-level confirm-feature checkpoint |
| **Confirmation insight** (found the insight we wanted to find) | REFUTE adversarial panel with evidence-vs-novelty discipline |
| **Blue-sky directions** (evolution ideas with no feasibility or value) | REFUTE Ripple blast-radius + Magi value×feasibility gate |
| **Improve-everything sprawl** (pursue every direction at once) | CHART ranks + the user picks one/few; minimum-viable downstream |
| **Jumping to build** (skip the insight, start coding) | `delve` writes no code; it hands off to spec/kaizen/feature/apex |
| **Reinventing kaizen** (incremental polish dressed up as a deep-dive) | boundary vs `kaizen`; a `deepen` direction explicitly routes *to* `kaizen` rather than doing its job |
| **Insight lost on interruption** | incremental draft persistence + `delve resume` from the current-phase marker |
| **Map elements resting on silent assumptions** (insights/directions the user never actually validated) | D9 Assumption Ledger + CHART Provenance check (D16) per `reference/dialogue-protocol.md` |
| **Elicitation-quality failures** (wall-of-questions GROUND, leading questions before DIVERGE, rubber-stamp checkpoints) | dialogue conducted per `reference/dialogue-protocol.md` D1–D15 |

## Boundaries / vs neighbors

- **vs `kaizen`** — `kaizen` *executes* improvement against a fixed quantified target (PDCA, builds code, ships a Before/After); `delve` *discovers* what to improve and which new directions exist (dialogue, no code, ships an Evolution Map). `delve` is **upstream** of `kaizen`: a `deepen` direction hands off to it. "improve this against a target" → `kaizen`; "what should we even do with this feature?" → `delve`.
- **vs `spec`** — `spec` takes a *new* (often vague) feature idea and converges it to a locked, buildable spec. `delve` starts from an *existing shipped* feature and excavates it for evolution directions. `delve → spec` when a chosen direction needs specifying. The axis is **new idea vs existing feature**.
- **vs `gedanken`** — both are Reason-family, no-code, insight-producing recipes that orchestrate `magi`/`flux`/`omen`. `gedanken` reasons about an **abstract** question/hypothesis inside a *constructed* hypothetical; `delve` excavates a **concrete existing feature** grounded in its real code and usage. "reason through what X would imply" → `gedanken`; "dig into the feature we already ship" → `delve`.
- **vs `essential` / `killer` / `trim`** — those deliver a *verdict* on which ONE feature to build or remove (single closing AskUserQuestion). `delve` produces a *map of directions* for ONE existing feature. `delve → killer` when "is direction X the differentiator?" becomes the open question.
- **vs `spark` (agent)** — `spark` is a single-agent feature *proposal* from existing data/logic; `delve` orchestrates `Lens`+`Plea`+`Flux`+`Echo`+`Magi`+`Riff` into a grounded excavation→insight→direction dialogue with a refutation gate, and uses `Spark` inside SURFACE/DIVERGE.
- **vs `riff` / `flux` (agents)** — `riff` diverges (generates ideas) and `flux` is a single reframing move; `delve` grounds in the real feature, converges to validated insights, *then* diverges to directions, then refutes. Each is one phase of `delve`. A one-off "what could we do with X?" → `riff`/`spark` direct.
- **vs `converge`** — `converge` is an *automated* generator-evaluator grading loop against a machine rubric; `delve`'s EXCAVATE↔SURFACE loop is an exploratory "dig deeper if insight-thin" heuristic with no rubric and no automated grader (its independent quality check is the REFUTE phase, not the loop). Iterate a generator to a quality bar → `converge`; excavate a feature for insight → `delve`.

**Decision tree:**
```
Have an EXISTING shipped feature and want a deep-dive → new insight + evolution directions (no code)?
  NO  → new feature idea to shape into a spec? → spec
        abstract hypothesis to reason through? → gedanken
        improve against a known target? → kaizen
        which ONE feature to build / remove? → essential / killer / trim
  YES → trivial one-off "what could we do with X?" → riff / spark direct (minimum viable chain)
        otherwise (ground → excavate → surface → diverge → refute → chart) → delve
              a chosen direction needs a full spec?            → delve → spec
              a chosen direction is incremental polish to a metric? → delve → kaizen
              a chosen direction is a clear single build?       → delve → feature / apex
              "is this direction THE differentiator?"           → delve → killer
```

## Scale

3-9 agents × excavation/dialogue depth. Light by agent count (a focused dive is GROUND→EXCAVATE→one Magi→REFUTE→CHART ≈ 4-5 agents); deep when EXCAVATE fans across many lenses and the EXCAVATE↔SURFACE deepening loop runs its full depth. Like `spec` and `gedanken`, the value is in excavation and interaction depth, not fan-out width.

## Shared protocols & Add-ons

- **Shared:** dialogue conduct → `reference/dialogue-protocol.md` (D1–D16: question craft, Assumption Ledger, checkpoint presentation, Provenance check at CHART). REFUTE → `_common/ADVERSARIAL_REFUTATION.md` (skeptic panel, evidence-vs-novelty, refute-polarity, aggregation). Downstream handoff at CHART → `spec` / `kaizen` / `feature` / `apex` / `reference/verdict-gate.md` recipes (`killer`/`essential`).
- **Add-ons:** +`Pulse`/`Trace`/`Voice` (usage/sentiment grounding in GROUND when data exists), +`Field` (real user-research grounding in EXCAVATE), +`Compete` (adjacent-value / how-others-solve-the-job in EXCAVATE), +`Cast` (persona-anchored excavation when the audience is unclear), +`Omen` (pre-mortem on a bold reframe in REFUTE), +`Atlas` (structural read when a direction touches module boundaries), +`Scribe` (author the Evolution Map).

## Chain template
`GROUND (Lens[map current impl] +Pulse?/Trace?/Voice?[usage] +Plea?[job-to-be-done lens]; reason-for-existence ← Socratic dialogue + Lens) → ✓confirm-feature-as-is + draft-init → EXCAVATE (Plea[latent needs] ‖ Flux[challenge baked-in assumptions] ‖ Echo[friction/workarounds] +Field?/Compete?/Trace?) → SURFACE (Magi[synthesize insights] +Spark[name vs existing logic]; deepening loop EXCAVATE↔SURFACE ≤ 3 cycles (default 3), stop on insight-saturation | diminishing-insight (Δ<ε) | cap-reached → report insights + undug seams) → ✓validate-insights + draft → DIVERGE (Riff ‖ Spark[grounded directions] ‖ Flux[reframe]; tag axis deepen/broaden/reframe + insight-link) → REFUTE (insight: refute×2-3 per _common/ADVERSARIAL_REFUTATION.md — confirmation/no-news/false-pattern, evidence-vs-novelty → confirmed vs hypothesis; direction: Ripple blast-radius + Magi value×feasibility +Omen?) → CHART (Magi/Spark Evolution Map: ranked directions + axis + recommended next-recipe; ✓provenance D16 + walk open ASSUME-n; Scribe?) → ✓pick-direction → recommend handoff (spec | kaizen | feature | apex | killer | essential) [NO CODE]`

The three dialogue checkpoints (confirm-feature-as-is / validate-insights / pick-direction) and the EXCAVATE↔SURFACE deepening bound are contract-level; resumable via `delve resume [<slug>]` from the draft's current-phase marker. Optional handoff to `spec` / `kaizen` / `feature` / `apex` / verdict recipes at CHART.
