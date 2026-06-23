# Verdict Gate — shared contract for verdict + conditional-implementation recipes

**Purpose:** The shared decision-and-build contract behind the verdict recipes `essential`, `killer`, and `trim` (and the flag clause of `graft`). Each of those recipes runs a refinement funnel, then **delivers a verdict via `AskUserQuestion` and only builds/excises on an explicit Yes**. This file owns the gate so the three recipes stop re-describing it and stop drifting apart.

**Read when:** executing `essential` / `killer` / `trim`, or any recipe that ends in a "build this? [Yes/No/Modify]" decision card. The full per-recipe funnels live in `reference/inline-recipes.md`; the refutation step is `_common/ADVERSARIAL_REFUTATION.md`.

---

## 1. The verdict card (`AskUserQuestion`)

Every verdict recipe converges on **one** outcome and presents it as a card, never a ranked menu:

```
## <Recipe> Verdict
Recommended <build|differentiator|removal>: <single item, or a removal slate>
Why: <2-3 lines>
Source of conviction: <funnel summary, e.g. Plea→Spark→Magi→Rank>
Considered but rejected: <2-3 alternatives, one-line reason each>
Evidence: <recipe-specific — moat class & trajectory (killer) / CoK + usage % + blast radius (trim)>
Survived refutation: <which attacks it withstood; open risk = refuted-on-evidence vs unproven-because-new>
→ <Build|Ship|Remove> this? [Yes / No / Modify]
```

The card is **contract-level**: even under `AUTORUN`/`AUTORUN_FULL` the recipe stops here for the user's pick (the verdict is the deliverable; building on an unconfirmed verdict defeats the recipe).

---

## 2. The three branches

- **Yes → Conditional implementation.** Build/excise, **inheriting the verdict's scope constraint** (single feature / single differentiator / the confirmed removal slate). Engine routing follows summit principles: **Codex owns code-gen** (Builder/Artisan/Radar/Sweep), **Claude owns judgment** (Sherpa/Guardian). Implementation cannot widen scope beyond the verdict.
- **No → Auditable record.** Deliver the verdict as a "decided-not-to-build / -ship / -keep" artifact embedding the evidence + surviving/failed refutations, so the decision is auditable and re-evaluable later. Do **not** run the build phase.
- **Modify → Bounded loop-back.** Capture what to change, re-enter the funnel with the modification as an **added constraint** (not a fresh start), and **carry forward rejected/refuted items as exclusions** so the reframe does not re-derive them. **Bound to 2 Modify loops, then escalate to the user** — never loop indefinitely.

---

## 3. Flag + KPI + kill criterion (high-differentiation builds)

When a Yes ships a **bet** rather than table-stakes (`killer` always; `graft` unless waived at Phase 0), the rollout is gated behind a feature flag that is **not a bare on/off**. It carries three load-bearing parts:

1. **Differentiation / adoption KPI** — the measurable form of the hypothesis (the adoption / retention / switching signal that proves the edge is real).
2. **Ramp schedule** — staged exposure (e.g. 5% → 25% → 100%) gated on the KPI clearing a threshold at each step.
3. **Kill criterion** — the KPI value below which the hypothesis is falsified and the flag rolls back.

A GO-with-flag on an *unproven-but-bold* bet (survived evidence-refutation, still unproven-because-new per `_common/ADVERSARIAL_REFUTATION.md` §2) states plainly on the card that this is a deliberate aggressive bet whose **kill-criterion is the real test**. Hand off to `growth-acceptance` when the +14/+30/+90d measurement loop is warranted.

---

## 4. Destructive verdicts (trim)

A removal verdict is semi-destructive, so the gate adds:
- The card flags any `PUBLIC_API` / `DATA` / irreversible row in-line and **confirms before excision even under AUTORUN**.
- Excision is **phased, flag-off-before-hard-delete**, small-scope per commit (never a big-bang multi-feature delete).
- `SIMPLIFY` verdicts route to `kaizen`/Zen, not deletion.
See `_common/ADVERSARIAL_REFUTATION.md` §5 for the safety-critical / confidence / blast-radius exclusions that precede any removal.

---

## 5. What this gate owns vs each recipe

This file owns the card shape, the three branches, the Modify bound, and the flag/KPI/kill structure. Each recipe (`reference/inline-recipes.md`) keeps **only** its funnel + selection criterion:
- `essential` → necessity funnel (Plea→Spark→Magi→Rank) + the **ambition check** (must-have ≠ timid); single top Must-have.
- `killer` → cross-engine triangulation + **moat-class/trajectory gate** + refutation; single boldest *viable* differentiator; always flagged.
- `trim` → essential×killer 2×2 over the live feature set + defend-polarity refutation; removal slate; phased excision.
