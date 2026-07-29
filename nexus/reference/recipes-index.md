# Recipes Index — full subcommand registry

**Purpose:** the complete `## Recipes` table for nexus — one row per Recipe with its subcommand, when to use it, its chain template, and the reference to read before executing. Split out of `SKILL.md` so the always-loaded skill body stays under the Anthropic size ceiling; the mental model (`### Recipe Families`) and the routing anchors (`### Signal Keywords`) remain in `SKILL.md` because they are needed to *choose*, while this file is needed to *execute*.

**Read when:** a subcommand matched at Subcommand Dispatch and you need its chain template and `Read` reference, or you are scanning the full registry to pick a Recipe.

**Authoring:** adding a Recipe touches seven indexes — see `reference/recipe-contract.md` §8. This file is #2 in that list.

> **Recipes = task shape; `SKILL.md` `## Modes` = execution control. Orthogonal.** Full phase contracts live in each Recipe's `Read` reference; complex Chain Templates (`See reference/recipes-detail.md`) live there; simple Recipes inline their chain.

---

## Recipes

| Recipe | Subcommand | Default? | When to Use | Chain Template | Read |
|--------|-----------|---------|-------------|----------------|------|
| Auto Classify | `classify` | ✓ | No Recipe specified — auto-classification. **Redirects to a curated Recipe when the resolved intent matches one; ad-hoc chain only for no-Recipe task types.** | `RESOLVE → GATE → MULTI? → REDIRECT? → SELECT → LADDER? → CHAIN_SELECT` | `reference/routing-matrix.md` (Classify Flow contract) |
| Bug Fix | `bug` | | Bug reports and fix requests | `Scout[RCA] → Sherpa? → Radar[failing repro] → Builder[root-cause] → Radar[verify] → Guardian`| `reference/routing-matrix.md` |
| Feature | `feature` | | New web/backend/generic feature. **iOS/Android native → `MOBILE_NATIVE` (Native) instead.** | `Lens?[reuse] → Sherpa[spec+AC] → Forge? → Builder → Radar[+verify gate] → Guardian`| `reference/routing-matrix.md` |
| Security | `security` | | Security response | `Sentinel[triage] → Probe?[confirm-exploit] → Builder[root-cause] → Probe/Radar[verify-closed] → Vigil? → Guardian`| `reference/routing-matrix.md` |
| Refactor | `refactor` | | Internal-only refactor, no external behavior change | `Radar?[safety-net] → Zen → Radar[verify-equivalence] → Guardian`| `reference/routing-matrix.md` |
| Optimize | `optimize` | | Performance-only improvement on *correct* code — measure-first, prove-with-a-number, across any slow layer (code/render · query · network · build · infra · search). Defect-caused slowdown → `bug` | `[locate layer] → Bolt/Tuner/Gear/Scaffold[measure→validity→target→optimize] → Radar[verify-speedup, independent] → Guardian`| `reference/optimize-recipe.md` (deep contract), `reference/routing-matrix.md` (task-type row) |
| Kaizen | `kaizen` |  | Existing-feature continuous improvement covering perf / UX / code-quality / feature-extension. | See `reference/recipes-detail.md` | `reference/inline-recipes.md` |
| Anneal | `anneal` |  | Codebase design audit → prioritized behavior-preserving brush-up. | See `reference/recipes-detail.md` | `reference/anneal-recipe.md` |
| Restyle | `restyle` |  | UI/visual design improvement of an existing surface — audit → direction → rubric-looped implementation → walkthrough+a11y+no-regression verify. | See `reference/recipes-detail.md` | `reference/restyle-recipe.md` |
| Converge | `converge` |  | **Quality-convergence loop** — the invocable entry point for the Generator-Evaluator pattern (`reference/evaluator-loop-protocol.md`). | See `reference/recipes-detail.md` | `reference/converge-recipe.md`, `reference/evaluator-loop-protocol.md` |
| Proactive | `proactive` | | `/Nexus` with no arguments — project state scan | `Scan project → recommend` | `reference/proactive-mode.md` |
| Apex | `apex` |  | Full-cycle auto-implementation: discovery → spec → parallel design → risk gate → loop → ship. | See `reference/recipes-detail.md` | `reference/apex-recipe.md`, `reference/apex-walkthrough.md` |
| Charter | `charter` |  | Repo-wide analysis → self-driving Charter, team design included — stops at the document. | See `reference/recipes-detail.md` | `reference/charter-recipe.md` |
| Enact | `enact` |  | Execute a Charter end-to-end. | See `reference/recipes-detail.md` | `reference/enact-recipe.md` |
| Operating Layer | `layer` |  | Design + stand up a repo's operating layer — Loom designs, Sigil authors, Nexus registers. | See `reference/recipes-detail.md` | `reference/layer-recipe.md` |
| Goal Setup | `goal` | | `/goal` autonomous long-running execution setup. **Gates on a machine-checkable completion oracle + mandatory hard-stop bound** (rejects unverifiable goals). 1-3 agents, no code execution | `Hone → Latch → Scribe? → DELIVER` | `reference/goal-recipe.md` |
| Gedanken | `gedanken` |  | Structured thought-experiment reasoning. | → `reference/recipes-detail.md` §gedanken | `reference/gedanken-recipe.md` |
| Delve | `delve` | | Existing-feature deep-dive → evolution-direction dialogue; no code — stops at a named Evolution Map. | See `reference/recipes-detail.md` | `reference/delve-recipe.md` |
| Cartograph | `cartograph` | | Multi-repo reverse-engineering → bird's-eye architecture diagrams + design document; no code — stops at a named Cartography Map. | See `reference/recipes-detail.md` | `reference/cartograph-recipe.md` |
| Chronicle | `chronicle` | | Commit-history reverse-engineering → era timeline + narrative storylines (feature/fix/improvement/decision) + reconstructed decision log + per-lens deep-dive files (security/domain-design/architecture/performance/design-ux/issues, split per file) + inferred ethos/worldview + repository history document set; no code — stops at a named Chronicle. | See `reference/recipes-detail.md` | `reference/chronicle-recipe.md` |
| Spec | `spec` |  | Interactive feature-proposal → locked specification through deep human-in-the-loop dialogue. | → `reference/recipes-detail.md` §spec | `reference/spec-recipe.md` |
| Essential | `essential` |  | Must-have feature **verdict + conditional implementation**. | See `reference/recipes-detail.md` | `reference/inline-recipes.md` |
| Killer | `killer` |  | Killer-feature **verdict + conditional implementation with feature flag**. | See `reference/recipes-detail.md` | `reference/inline-recipes.md` |
| Trim | `trim` |  | Dead-weight feature **removal verdict + conditional excision** — the inverse of `essential`/`killer`. | See `reference/recipes-detail.md` | `reference/inline-recipes.md` |
| Acceptance | `acceptance` |  | Proof-Carrying PR pipeline v2 — Two-Axis (Code + Design). **Layer preset:** `layer=c` (alias `growth-acceptance`) extends it past merge with the Market/Research/Brand lifecycle gate. | See `reference/recipes-detail.md` | `_common/PROOF_CARRYING.md`, `reference/acceptance-recipe.md`; layer=c blueprint → `_common/GROWTH_BRAND_PROOF.md`, `reference/growth-acceptance-recipe.md` |
| Summit | `summit` |  | Multi-engine **five-team** quality-maximization. | See `reference/recipes-detail.md` | `reference/summit-recipe.md` |
| Podium | `podium` |  | Content-quality maximization. | See `reference/recipes-detail.md` | `reference/podium-recipe.md` |
| Newsroom | `newsroom` |  | **Grounded article production / audit** — every factual claim source-cited and adversarially verified; no speculation ships unlabeled. Confirm release-critical. | See `reference/recipes-detail.md` | `reference/newsroom-recipe.md`, `reference/research-grounding.md` |
| Eureka | `eureka` |  | **Novelty-proven invention** — name the contradiction current solutions accept as given, sweep prior art (inverted polarity: research to *avoid*) + failure archaeology, diverge across six structurally-different generators, kill collisions **with citations**, survive the pentad gate (novelty · value · feasibility · defensibility · **freedom-to-operate**), and prove the mechanism with a **falsification-first** spike before disclosing it. **Always confirm.** A `BLOCK (prior-art saturation)` run still ships its dossier. | See `reference/recipes-detail.md` | `reference/eureka-recipe.md`, `reference/research-grounding.md` |
| Wish | `wish` |  | **Once-in-a-lifetime request** — scarcity-gated one-shot quality-ceiling delivery: crystallize the true wish → **anchor the ceiling to sourced best-in-class exemplars** → **cross-engine blind tournament** → adversarial gauntlet + ceiling convergence on **calibrated** evaluators (all dims = 3) → reception simulation → **One-Shot Gate + Comparative Gate**. Budget-enveloped. **Domain preset:** `domain=lp` (alias `marquee`) fixes a 5-dim LP rubric with machine oracles and drops the Scarcity Gate. **Always confirm.** | See `reference/recipes-detail.md` | `reference/wish-recipe.md`; domain=lp blueprint → `reference/marquee-recipe.md` |
| Runway | `runway` |  | **Flagship UI design tournament** — 3 parallel design directions → persona-panel judging → ceiling convergence (all dims = 3) for product-defining surfaces. **Always confirm.** | See `reference/recipes-detail.md` | `reference/runway-recipe.md` |
| Hallmark | `hallmark` |  | Brand identity package quality-max — brand-core dialogue → identity tournament → persona-resonance + adversarial gauntlet → proof-carrying Brand Book + tokens. | See `reference/recipes-detail.md` | `reference/hallmark-recipe.md` |
| Rebrand | `rebrand` |  | All-surface brand propagation with a proven-complete guarantee — RESIDUE-GATE × brand rubric; old-brand decommission gated on the completeness proof. | See `reference/recipes-detail.md` | `reference/rebrand-recipe.md` |
| Migrate | `migrate` |  | Change-completeness migration. | See `reference/recipes-detail.md` | `reference/migrate-recipe.md` |
| Transmute | `transmute` |  | **Cross-language rewrite** preserving behavior (TS→Rust, Go→Rust, Python→Go, JS→TS, …). | See `reference/recipes-detail.md` | `reference/transmute-recipe.md` |
| Clone | `clone` | | Faithful product reproduction — reverse-engineer an existing product's observable surface, rebuild it, and verify the copy by differential parity against a stamped captured baseline. | See `reference/recipes-detail.md` | `reference/clone-recipe.md`, `reference/research-grounding.md` |
| Fuse | `fuse` |  | Multi-source product synthesis. | See `reference/recipes-detail.md` | `reference/fuse-recipe.md`, `reference/research-grounding.md` |
| Graft | `graft` |  | Concept transplant for innovation. | See `reference/recipes-detail.md` | `reference/graft-recipe.md`, `reference/research-grounding.md` |
| Package | `package` |  | Generalized document-package generator. | See `reference/recipes-detail.md` | `reference/package-recipe.md`, `reference/venture-recipe.md` (startup blueprint) |
| Pack | `pack` | | **Skill ecosystem control** (meta) — switch active Claude Code skill profile per workstream. Forms: `list` / `current` / `<name>` / `reset`. **Confirms diff before writing `settings.json`.** | Inline edit (no spawn) | `reference/pack-subcommand.md`, `_common/SKILL_PACKS.md` |

### Signal Keywords → Recipe

For natural-language input without an explicit subcommand. **Subcommand match always wins.** Keywords are **English canonical anchors**, not a literal allowlist — Nexus translates input (any language/paraphrase) to English intent first, then matches semantically. Output language still follows config.

**Full canonical table** (Core / Specialist / Mobile / Package / Fallback) → `reference/signal-keywords.md`. Most-used Core anchors inlined below:

| Keywords | Recipe |
|----------|--------|
| `bug`, `error`, `broken` | `bug` |
| `feature`, `implement`, `build` | `feature` |
| `security`, `vulnerability`, `CVE` | `security` |
| `refactor`, `clean up`, `code smell` | `refactor` |
| `optimize`, `slow`, `performance`, `speed up`, `latency`, `slow query`, `bottleneck` | `optimize` (`memory leak` → `bug`; post-deploy slowdown, output still correct → `optimize +Trail`; full REDIRECT notes → `reference/signal-keywords.md`) |
| `kaizen`, `improve`, `polish`, `enhance existing`, `refine` | `kaizen` |
| `anneal`, `design audit`, `brush up the codebase`, `harden the architecture`, `design weaknesses` | `anneal` |
| `restyle`, `redesign`, `UI refresh`, `visual polish`, `modernize the UI`, `improve the look and feel` | `restyle` (UI/visual — code-design improvement → `anneal`) |
| `loop`, `make a loop`, `run until done`, `autonomous loop`, `ralph loop` | shape-resolve per `_common/LOOP_PRECONDITIONS.md` → `goal` (native single-session) · `converge` (in-session rubric) · `orbit` skill (unattended runner) · `apex` (discovery→ship). The five-point gate runs at the resolved owner |
| `cartograph`, `reverse-engineer across repos`, `bird's-eye diagram`, `overview diagram`, `architecture map`, `design doc from code`, `understand the system across repos` | `cartograph` |
| `chronicle`, `repository history`, `commit history summary`, `how did we get here`, `evolution of the codebase`, `project timeline`, `git history narrative`, `history of the repo`, `feature/bug/decision history`, `decision log from history`, `design philosophy from history`, `project ethos/worldview` | `chronicle` (era timeline + storylines: feature/fix/improvement/decision + decision log + per-lens deep-dive files: security/domain/architecture/perf/UX/issues + inferred ethos/worldview, from commit history) |
| `eureka`, `invent`, `invention`, `breakthrough`, `genuinely new`, `nobody has done this`, `patentable`, `novel mechanism`, `prior art` | `eureka` (novelty-**proven** invention — a mechanism already proven elsewhere → `graft`; picking among candidates in hand → `killer`; feature ideation inside the known solution space → `spark`) |
| `wish`, `once-in-a-lifetime request`, `favor of a lifetime`, `your absolute best`, `spare nothing`, `no second chance`, `one shot to get this right` | `wish` (scarcity-gated one-shot ceiling; strategic code quality-max → `summit`, standard bar iteration → `converge`) |
| `runway`, `design tournament`, `flagship screen design`, `best possible design` | `runway` (in-product flagship surface — single-direction improvement → `restyle`; acquisition LP → `wish domain=lp` / `marquee`) |
| `hallmark`, `brand identity`, `brand book`, `brand voice`, `visual identity` | `hallmark` (creates the brand — propagation → `rebrand`; personal branding → `crest`) |
| `rebrand`, `brand refresh`, `apply new brand everywhere`, `brand migration` | `rebrand` (completeness-proven propagation; no settled Brand Book → `hallmark` first) |
| `marquee`, `best possible landing page`, `flagship LP`, `one-shot LP` | `wish domain=lp` (alias `marquee` — wish-grade one-shot LP; routine LP → `bazaar`/`funnel`; bare `landing page` overloaded → REDIRECT) |
| `newsroom`, `fact-check`, `verify sources`, `every claim cited`, `no speculation`, `source-grounded article`, `check the article is correct` | `newsroom` (grounding-first article compose/audit — package polish + slides → `podium`; plain article → `zine` direct) |
| `/Nexus` (no arguments) | `proactive` |
| unclear or multi-domain request | `classify` → `reference/intent-clarification.md` |

Specialist anchors (Chain / Cull-Triage-Crypt / Clause-Scribe / Rank-Magi / Omen-Ripple / Matrix / Sketch), native-app / cross-platform anchors (`MOBILE_NATIVE`, `MACOS_NATIVE`, `IOS_UI_TEST`, `PORTING`), and package/domain-preset anchors (research / ai-adoption / legal / saas / media / growth / career / learning / hiring / local-gov) — see `reference/signal-keywords.md`.
