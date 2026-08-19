# Recipe: `restyle` — UI/visual design improvement of an existing surface

**Purpose:** Take an *already-shipped* UI surface (screen / component / flow — or the whole product when no target is given), audit its current design, set a confirmed design direction, and iteratively improve the **visual · interaction · usability** quality against a rubric — verified by persona re-walkthrough, a11y re-check, and a no-regression gate. The **UI/visual-design member of the Improve family**: where `anneal` improves *code* design and `kaizen` improves *one feature* against a quantified target, `restyle` improves the *design itself* — look, feel, motion, hierarchy, consistency — under an explicit direction, never taste-driven churn.

**Read when:** Executing the `restyle` Recipe.

---

## Invocation & target resolution

```
/nexus restyle <target>          # scope: a screen, component, or flow
/nexus restyle                   # no target → whole-UI audit (confirm-before-launch)
/nexus restyle <target> direction=<brief>   # skip DIRECT dialogue; Vision validates the given brief instead
```

- `<target>` scopes AUDIT to the named surface.
- **No target → whole-UI sweep**: Echo/Palette audit the full surface, Rank orders candidates by **friction × visibility**, and the improvement slate is capped to **top-N (default 5)** with the dropped long-tail recorded — never a silent truncation. No-target runs are **Confirm-before-launch**.

**Default Mode:** `AUTORUN` with the ✓direction-gate (design direction is subjective; implementation is reversible). Escalate to `GUIDED` when the slate touches 10+ files or changes brand-level tokens.

---

## Chain template

```
AUDIT    (Echo[persona walkthrough + friction score] ‖ Palette[usability heuristics + a11y baseline]
          +Frame?[Figma design context] +Muse?[token-drift inventory] +Voice?/Trace?[user signals])
→ DIRECT (Vision[design direction + Design Brief: rubric axes + target scores]
          +Flux?[reframe when the current design's premise is the problem])
→ ✓direction-gate
→ ⟲{ IMPLEMENT (Artisan[components/styles] ‖ Flow?[motion/transitions] ‖ Prose?[microcopy]
                ‖ Muse?[tokenize before ad-hoc styles] ‖ Ink?[icons/assets])
     → VERIFY  (Echo[re-walkthrough vs rubric] + Palette[a11y re-check ≥ baseline]
                + Radar[no-regression on behavior]) }⟲  loop ≤ 3 cycles (default 3)
→ SHIP   (Guardian[phased commits + PR embedding the Lookbook])
```

Engine routing follows summit principles: **Codex owns code-gen** (Artisan / Flow / Muse-apply / Ink), **Claude owns judgment** (Echo / Palette / Vision / Flux / Guardian).

## Phase contract

- **Phase 1 AUDIT (parallel)** — Echo[claude] runs persona walkthroughs of the target surface and captures a **quantified friction/emotion baseline**; Palette[claude] runs usability heuristics + an **a11y baseline** (WCAG level per canon rules). Conditionally add Frame[claude] when a Figma source of truth exists, Muse[claude] for a token-drift inventory (ad-hoc styles vs system), Voice/Trace[claude] when user feedback or session data exists. **The baseline is the entry condition for Phase 3** — "restyle without measuring the current design" cannot proceed.
- **Phase 2 DIRECT (sequential)** — Vision[claude] synthesizes the audit into a **design direction + Design Brief**: 3-6 rubric axes (e.g. hierarchy, consistency, feedback, motion, density, brand fit) each with a current score and a target score, plus explicit **non-goals** (what this restyle will NOT touch). Optional Flux when the audit suggests the surface's *premise* — not its execution — is the problem. The Brief is the loop's single rubric (Generator-Evaluator separation per `reference/evaluator-loop-protocol.md`).
- **✓direction-gate** — present direction + Brief + estimated blast radius. Tier: **Confirm-before-launch when** no-target sweep, full-surface redesign, brand-level token change, or 10+ files; a scoped single-component polish proceeds under AUTORUN with the gate announced. Direction changes after this gate loop back to DIRECT — never mid-IMPLEMENT.
- **Phase 3 IMPLEMENT (parallel within cycle)** — Artisan[codex] implements component/style changes; Flow[codex] motion; Prose[codex] microcopy; Ink[codex] icon/asset gaps; **Muse[codex] tokenizes recurring values *before* Artisan writes ad-hoc styles** (token-first rule). Independent sub-surfaces run parallel per `_common/PARALLEL.md` ownership.
- **Phase 4 VERIFY (the loop gate)** — Echo re-walks the same personas and re-scores the rubric; Palette re-checks a11y (**must be ≥ baseline — a prettier-but-less-accessible cycle fails the gate**); Radar confirms no behavioral regression. Branch: **target-met** (all rubric axes at target, no regression) → SHIP · **iterations remain AND marginal gain ≥ ε** → next cycle (carry the delta, not a fresh audit) · **diminishing-returns (Δ < ε)** or **cap-reached** → stop, record best-so-far + residual gap per axis → SHIP with partial note · **BLOCK** → escalate.
- **Phase 5 SHIP** — Guardian[claude] produces phased small-scope commits and a PR embedding the **Lookbook**.

---

## The eight contract elements

| # | Element | Contract |
|---|---------|----------|
| 1 | Termination bound | `loop ≤ 3 cycles (default 3)`; exits `ACCEPT`/`target-met` · `diminishing-returns (Δ < ε)` · `cap-reached` · `BLOCK`. Non-`ACCEPT` exits report best-so-far + residual gap per rubric axis. |
| 2 | Confirm / safety gate | ✓direction-gate: **Confirm-before-launch when** no-target sweep / full-surface redesign / brand-token change / 10+ files. Standard **Ask First** on 10+ files. |
| 3 | Resume | **checkpoint-resume** (5 phases; `restyle resume` re-enters from the last completed phase, Design Brief + baseline carried forward). |
| 4 | Output report | Named **Lookbook** — per surface: Before/After rubric scores, friction-score delta, a11y result vs baseline, cycles run + stop reason, token changes, and the Design Brief's non-goals honored. |
| 5 | Failure Modes Prevented | Consolidated section below. |
| 6 | Boundaries / vs neighbors | Section below + Decision Tree. |
| 7 | Scale | **5-12 agents × ≤ 3 cycles, medium cost** (cost scales with slate size — the top-N cap is the governor). |
| 8 | Shared-protocol refs | `reference/evaluator-loop-protocol.md` (Brief = rubric, Echo/Palette = independent Evaluators, implement cluster = Generator); `reference/autonomy-quality-protocol.md` (intent contract, Decision Ledger, producer ≠ verifier — Echo/Palette never author the styles they score); `_common/PARALLEL.md` (Phase 3 ownership); `_common/PROPORTION_AND_SPACING.md` (sourced numbers for spacing/measure/grid/touch-target rubric axes — cite §9 defaults when the Brief sets a target score, §1 evidence tiers so a spec-level gap and a craft-convention gap are not scored alike, §4 inner ≤ outer as the density/hierarchy axis test). Verdict/refutation/parity protocols: `N/A` (no verdict, no reproduction claim). |

## Failure Modes Prevented

1. **Taste-driven churn** — no restyle enters IMPLEMENT without an Echo/Palette baseline and a Vision Design Brief with target scores; "make it look better" is forced into rubric axes.
2. **Prettier-but-worse** — Phase 4 requires the friction score to improve AND a11y ≥ baseline; a visually richer cycle that regresses usability or accessibility fails the gate.
3. **Redesign that breaks behavior** — Radar no-regression is a hard gate every cycle; restyle changes presentation, never contracts.
4. **Token drift / one-off styles** — Muse token-first rule: recurring values are tokenized before Artisan writes ad-hoc styles, so the restyle strengthens the design system instead of eroding it.
5. **Unbounded polish** — `loop ≤ 3 cycles (default 3)` + diminishing-returns exit; never burns cycles past marginal value.
6. **Direction whiplash** — the direction is locked at ✓direction-gate; a mid-flight direction change loops back to DIRECT with the gate re-run, never mutates the rubric mid-IMPLEMENT (single termination oracle).
7. **Silent whole-UI truncation** — no-target sweeps cap the slate to top-N by friction × visibility and record the dropped long-tail.

## Boundaries

- **vs `kaizen`** — kaizen improves *one feature* multi-axis (perf/UX/code-quality/extension) against a *quantified metric target*; restyle is the **design-axis specialist across a surface**, driven by a *direction + rubric* rather than one metric. A kaizen UX axis that grows into "actually, redesign this screen" → hand off to restyle.
- **vs `anneal`** — anneal audits and brushes up **code/architecture design** (behavior-preserving internals); restyle improves the **visible design**. The overloaded anchor `improve the design` REDIRECTs on this axis: UI/visual/look-and-feel → restyle; architecture/code design → anneal.
- **vs `feature`** — feature adds a new capability; restyle changes how existing capability looks and feels. New UI *and* new behavior → feature (with Vision in its design step).
- **vs `vision` direct** — Vision alone delivers direction/Design-System decisions with no execution; restyle carries the direction through implementation and verification. Direction-only ask → vision direct (minimum viable chain).
- **vs `palette`/`flow`/`muse` direct** — a single named fix (one a11y issue, one transition, one token) → the specialist direct; restyle is warranted when the surface needs audit → direction → multi-agent execution.
- **vs `burnish`** — restyle **decides** the direction and scores the result with *internal* evaluators against its own Design Brief; burnish takes a **settled** direction and drives the rendered surface to zero open findings from an *external* multimodal review engine (split oracle: hard findings to zero, soft axes to `≥ 2`). `restyle` → `burnish` is the pair: direction first, then review-to-zero. An ask that names no direction and no reviewer stays on restyle.
- **vs `atelier` skill** — atelier orchestrates the full design-to-implementation *pipeline* (extraction, prototypes, visual assets, slides, persistent project design system). When a restyle's scope expands to a product-wide design-system rebuild or asset production, hand off to atelier.
- **vs `funnel[premium]`** (LP studio) — domain-specialized sibling; an LP surface routes there.

### Decision Tree

```
"improve the design" of something
├─ architecture / code design / internal structure → anneal
├─ UI / visual / look-and-feel / interaction
│  ├─ direction decision only, no build → vision direct
│  ├─ one named fix (a11y issue, one animation, one token) → palette/flow/muse direct
│  ├─ landing page → funnel[premium]
│  ├─ product-wide pipeline w/ prototypes+assets+design system → atelier skill
│  ├─ direction already settled; loop it to zero external-review findings → burnish
│  └─ audit → direction → implement → verify on an existing surface → restyle ✓
├─ one feature vs a quantified target (perf/UX/quality mixed) → kaizen
└─ new capability with new UI → feature
```

## Add-ons

+Forge to prototype a risky direction before committing IMPLEMENT · +Vector/vitrine for visual-evidence capture (Before/After screenshots in the Lookbook) · +Experiment to A/B the restyled surface against the baseline when traffic allows · +Canon for a formal WCAG conformance pass · +Field when the audit needs real-user research beyond persona simulation.
