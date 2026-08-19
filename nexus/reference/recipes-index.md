# Recipes Index — full subcommand registry

**Purpose:** the complete Recipes table — one row per Recipe (subcommand · when to use · chain template · `Read` reference). Split out of `SKILL.md`, which keeps the mental model (`### Recipe Families`); routing anchors live in `reference/signal-keywords.md`. Those two are needed to *choose*; this file is needed to *execute*. Recipe-vs-Mode orthogonality and the "phase contracts live in `<recipe>-recipe.md`" rule → `SKILL.md` § Recipes.

**Read when:** a subcommand matched at Subcommand Dispatch and you need its chain template and `Read` reference, or you are scanning the full registry to pick a Recipe.

**Authoring:** adding a Recipe touches seven indexes — see `reference/recipe-contract.md` §8. This file is #2 in that list.

---

## Recipes

Fallback is owned by the internal `phase:CLASSIFY` Default dispatch in `SKILL.md`; no Recipe row is marked default.

| Recipe | Subcommand | Default? | When to Use | Chain Template | Read |
|--------|-----------|---------|-------------|----------------|------|
| Bug Fix | `bug` | | Bug reports and fix requests | `Scout[RCA] → Sherpa? → Radar[failing repro] → Builder[root-cause] → Radar[verify] → Guardian`| `reference/routing-matrix.md` |
| Feature | `feature` | | New web/backend/generic feature. **iOS/Android native → `MOBILE_NATIVE` (Native) instead.** | `Lens?[reuse] → Sherpa[spec+AC] → Forge? → Builder → Radar[+verify gate] → Guardian`| `reference/routing-matrix.md` |
| Deliver | `deliver` | | Build and ship a product or MVP with a chain sized to the repository and requested scope. | See `reference/deliver-recipe.md` | `reference/deliver-recipe.md` |
| Security | `security` | | Security response. **`mode=to-zero`** wraps it in a scanner-finding sweep driven to zero at a CVSS floor (`_common/FINDING_LEDGER.md` member; `RISK-ACCEPTED` needs an owner + expiry and re-opens when it lapses). | `Sentinel[triage] → Probe?[confirm-exploit] → Builder[root-cause] → Probe/Radar[verify-closed] → Vigil? → Guardian`| `reference/routing-matrix.md` |
| Refactor | `refactor` | | Internal-only refactor, no external behavior change | `Radar?[safety-net] → Zen → Radar[verify-equivalence] → Guardian`| `reference/routing-matrix.md` |
| Optimize | `optimize` | | Performance-only improvement on *correct* code — measure-first, prove-with-a-number. Defect-caused slowdown → `bug`. **`mode=to-zero`** drives a **set** of budget violations to zero across many targets (`_common/FINDING_LEDGER.md` member; budgets frozen — `BUDGET-RAISED` needs adjudicator ratification, `METRIC-GAMED` blocks, a close needs the declared sample count not one lucky run) | `[locate layer] → Bolt/Tuner/Gear/Scaffold[measure→validity→target→optimize] → Radar[verify-speedup, independent] → Guardian`| `reference/optimize-recipe.md` (deep contract), `reference/routing-matrix.md` (task-type row) |
| Kaizen | `kaizen` |  | Existing-feature continuous improvement covering perf / UX / code-quality / feature-extension. | See `reference/inline-recipes.md` | `reference/inline-recipes.md` |
| Anneal | `anneal` |  | Codebase design audit → prioritized behavior-preserving brush-up. | See `reference/anneal-recipe.md` | `reference/anneal-recipe.md` |
| Restyle | `restyle` |  | UI/visual design improvement of an existing surface — audit → direction → rubric-looped implementation → walkthrough+a11y+no-regression verify. | See `reference/restyle-recipe.md` | `reference/restyle-recipe.md` |
| Converge | `converge` |  | **Quality-convergence loop** — the invocable entry point for the Generator-Evaluator pattern (`reference/evaluator-loop-protocol.md`). | See `reference/converge-recipe.md` | `reference/converge-recipe.md`, `reference/evaluator-loop-protocol.md` |
| Quell | `quell` |  | **Review-to-zero fix loop** — fix → external review engine (Codex default) → repeat until zero open findings at/above the severity floor; disposition ledger + oscillation detection make zero reachable and honest. `profile=general\|refactor` (refactor = Equivalence Gate + frozen tests + behavior-changing fixes deferred). | See `reference/quell-recipe.md` | `reference/quell-recipe.md`, `judge/reference/codex-review-usage.md` |
| Whet | `whet` |  | **Mutation-survivor loop** — run a mutation engine over the frozen scope, kill survivors, re-run, until every declared partition meets its **threshold contract**. `EQUIVALENT` needs a failed distinguishing-test attempt (it shrinks the score's denominator), implementation-mirroring tests raise `TAUTOLOGICAL-KILL`, and code deletion closes as `CLOSED-BY-REMOVAL` rather than as a kill. | See `reference/whet-recipe.md` | `reference/whet-recipe.md`, `siege/reference/mutation-testing-advanced.md` |
| Burnish | `burnish` |  | **Design review-to-zero loop** — capture the rendered surface → external multimodal review engine → fix → re-capture, until zero open hard findings at/above the floor **and** every declared soft axis ≥ 2 (split oracle). Frozen Finding Charter + coordinate-free fingerprints + Appearance Gate keep it convergent. `profile=general\|faithful` (faithful = reference conformance + `REFERENCE-DRIFT` blocks at any severity). | See `reference/burnish-recipe.md` | `reference/burnish-recipe.md`, `reference/quell-recipe.md` |
| Apex | `apex` |  | Full-cycle auto-implementation: discovery → spec → parallel design → risk gate → loop → ship. | See `reference/apex-recipe.md` | `reference/apex-recipe.md` |
| Charter | `charter` |  | Repo-wide analysis → self-driving Charter, team design included — stops at the document. | See `reference/charter-recipe.md` | `reference/charter-recipe.md` |
| Enact | `enact` |  | Execute a Charter end-to-end. | See `reference/enact-recipe.md` | `reference/enact-recipe.md` |
| Operating Layer | `layer` |  | Design + stand up a repo's operating layer — Sigil blueprints and authors, Nexus registers. | See `reference/layer-recipe.md` | `reference/layer-recipe.md` |
| Goal Setup | `goal` | | `/goal` autonomous long-running execution setup. **Gates on a machine-checkable completion oracle + mandatory hard-stop bound** (rejects unverifiable goals). 1-2 agents, no code execution | `Hone → Scribe? → DELIVER` | `reference/goal-recipe.md` |
| Gedanken | `gedanken` |  | Structured thought-experiment reasoning. | See `reference/gedanken-recipe.md` | `reference/gedanken-recipe.md` |
| Delve | `delve` | | Existing-feature deep-dive → evolution-direction dialogue; no code — stops at a named Evolution Map. | See `reference/delve-recipe.md` | `reference/delve-recipe.md` |
| Cartograph | `cartograph` | | Multi-repo reverse-engineering → bird's-eye architecture diagrams + design document; no code — stops at a named Cartography Map. | See `reference/cartograph-recipe.md` | `reference/cartograph-recipe.md` |
| Chronicle | `chronicle` | | Commit-history reverse-engineering → era timeline + storylines + decision log + inferred ethos; no code. | See `reference/chronicle-recipe.md` | `reference/chronicle-recipe.md` |
| Verity | `verity` | | Codebase × documentation coherence audit → a triaged register of contradictions, stale record, and unexplained artifacts; **report-only** — no code, no doc edits, every finding routed. | See `reference/verity-recipe.md` | `reference/verity-recipe.md` |
| Abide | `abide` | | Change-anchored governance audit — a change set vs the **standing** decision record (ADR/RFC, specs, contracts, conventions), including records the change never touched → a triaged Divergence Docket (VIOLATES · SUPERSEDES-SILENTLY · OBSOLETE-COMPLIANCE · UNGOVERNED); **report-only** — never edits a record, every finding routed. | See `reference/abide-recipe.md` | `reference/abide-recipe.md` |
| Spec | `spec` |  | Interactive feature-proposal → locked specification through deep human-in-the-loop dialogue. | See `reference/spec-recipe.md` | `reference/spec-recipe.md` |
| Essential | `essential` |  | Must-have feature **verdict + conditional implementation**. | See `reference/inline-recipes.md` | `reference/inline-recipes.md` |
| Killer | `killer` |  | Killer-feature **verdict + conditional implementation with feature flag**. | See `reference/inline-recipes.md` | `reference/inline-recipes.md` |
| Trim | `trim` |  | Dead-weight feature **removal verdict + conditional excision** — the inverse of `essential`/`killer`. | See `reference/inline-recipes.md` | `reference/inline-recipes.md` |
| Acceptance | `acceptance` |  | Proof-Carrying PR pipeline v2 — Two-Axis (Code + Design). `layer=c` (alias `growth-acceptance`) = post-merge lifecycle. | See `reference/acceptance-recipe.md` | `_common/PROOF_CARRYING.md`, `reference/acceptance-recipe.md`; layer=c blueprint → `_common/GROWTH_BRAND_PROOF.md`, `reference/growth-acceptance-recipe.md` |
| Summit | `summit` |  | Multi-engine **five-team** quality-maximization. | See `reference/summit-recipe.md` | `reference/summit-recipe.md` |
| Podium | `podium` |  | Content-quality maximization. | See `reference/podium-recipe.md` | `reference/podium-recipe.md` |
| Newsroom | `newsroom` |  | **Grounded article production / audit** — every factual claim source-cited and adversarially verified; no speculation ships unlabeled. Confirm release-critical. | See `reference/newsroom-recipe.md` | `reference/newsroom-recipe.md`, `reference/research-grounding.md` |
| Eureka | `eureka` |  | **Novelty-proven invention** — prove a mechanism new against a Prior-Art Ledger. **Always confirm** (`depth=scout` excepted). Contract: `ship=true` is opt-in only (never inferred), mutually exclusive with `depth=scout`. | See `reference/eureka-recipe.md` | `reference/eureka-recipe.md`, `reference/research-grounding.md` |
| Wish | `wish` |  | **Once-in-a-lifetime request** — scarcity-gated one-shot quality ceiling; `domain=lp` = `marquee`. **Always confirm.** | See `reference/wish-recipe.md` | `reference/wish-recipe.md`, `reference/research-grounding.md`; domain=lp blueprint → `reference/marquee-recipe.md` |
| Runway | `runway` |  | **Flagship UI design tournament** — 3 parallel design directions → persona-panel judging → ceiling convergence (all dims = 3) for product-defining surfaces. **Always confirm.** | See `reference/runway-recipe.md` | `reference/runway-recipe.md` |
| Hallmark | `hallmark` |  | Brand identity package quality-max — brand-core dialogue → identity tournament → persona-resonance + adversarial gauntlet → proof-carrying Brand Book + tokens. | See `reference/hallmark-recipe.md` | `reference/hallmark-recipe.md` |
| Rebrand | `rebrand` |  | All-surface brand propagation with a proven-complete guarantee — RESIDUE-GATE × brand rubric; old-brand decommission gated on the completeness proof. | See `reference/rebrand-recipe.md` | `reference/rebrand-recipe.md` |
| Crucible | `crucible` |  | **Operability proof under adversarial conditions** — the design **floor**; binary per-cell oracle. **Always confirm.** | See `reference/crucible-recipe.md` | `reference/crucible-recipe.md` |
| Silhouette | `silhouette` |  | **Distinction proof** — blind attribution vs K competitors, logo stripped. **Always confirm.** | See `reference/silhouette-recipe.md` | `reference/silhouette-recipe.md`, `reference/research-grounding.md` |
| Lattice | `lattice` |  | **Design-system coherence proof** — steady-state conformance. **Ask First** on big-bang / 10+ files. | See `reference/lattice-recipe.md` | `reference/lattice-recipe.md`, `reference/migrate-recipe.md` |
| Assay | `assay` |  | **Experimental proof of design claims** (code/architecture); `apply=true` is opt-in. **Always confirm.** | See `reference/assay-recipe.md` | `reference/assay-recipe.md`, `_common/DIFFERENTIAL_PARITY.md` |
| Chorus | `chorus` |  | **Cross-platform coherence proof** — Idiom × Kinship gates over an Invariant/Variant Contract. **Always confirm.** | See `reference/chorus-recipe.md` | `reference/chorus-recipe.md` |
| Migrate | `migrate` |  | Change-completeness migration. | See `reference/migrate-recipe.md` | `reference/migrate-recipe.md` |
| Transmute | `transmute` |  | **Cross-language rewrite** preserving behavior (TS→Rust, Go→Rust, Python→Go, JS→TS, …). | See `reference/transmute-recipe.md` | `reference/transmute-recipe.md` |
| Clone | `clone` | | Faithful product reproduction — reverse-engineer an existing product's observable surface, rebuild it, and verify the copy by differential parity against a stamped captured baseline. | See `reference/clone-recipe.md` | `reference/clone-recipe.md`, `reference/research-grounding.md` |
| Fuse | `fuse` |  | Multi-source product synthesis. | See `reference/fuse-recipe.md` | `reference/fuse-recipe.md`, `reference/research-grounding.md` |
| Graft | `graft` |  | Concept transplant for innovation. | See `reference/graft-recipe.md` | `reference/graft-recipe.md`, `reference/research-grounding.md` |
| Package | `package` |  | Generalized document-package generator. | See `reference/package-recipe.md` | `reference/package-recipe.md`, `reference/venture-recipe.md` (startup blueprint) |
| Pack | `pack` | | **Skill ecosystem control** (meta) — switch active Claude Code skill profile per workstream. Forms: `list` / `current` / `<name>` / `reset`. **Confirms diff before writing `settings.json`.** | Inline edit (no spawn) | `reference/pack-subcommand.md`, `_common/SKILL_PACKS.md` |

### Signal Keywords → Routing Destination

For natural-language input without an explicit subcommand. **Subcommand match always wins.**

**Canonical table → `reference/signal-keywords.md`** (Core / Specialist / Native / Loop-Migration-Reproduction / Package / Fallback), which also owns the language rule and the per-anchor REDIRECT notes. No anchors are duplicated here.
