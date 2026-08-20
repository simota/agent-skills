# Full Routing Matrix

**Purpose:** Canonical task-type → **default chain** mapping with Recipe Hints (per-step sub-skill commands) and conditional Additions.
**Read when:** The quick-start matrix in SKILL.md is insufficient and you need the full task-type catalog.

**Boundary vs `agent-chains.md`:** This file gives one row per task type with the *default* chain. `agent-chains.md` lists **complexity variants** (e.g., `FEATURE/S`, `FEATURE/M`, `FEATURE/L`, `FEATURE/UI`, `FEATURE/UX`) and dynamic adjustment rules. Start here to pick the task type; switch to `agent-chains.md` when complexity sub-typing matters.

Complete task type → agent chain mapping. The SKILL.md Routing Quick Start contains the top patterns; this file contains the full matrix.

---

## Classify Flow — Internal Default Dispatch Phase Contract

CLASSIFY is the internal `phase:CLASSIFY` Default dispatch when **no Recipe subcommand and no Signal-Keyword match** fires; it is not a Recipe or subcommand. It resolves intent and routes to the *best* chain, preferring a curated Recipe over an ad-hoc one. Phases: `RESOLVE → GATE → MULTI? → REDIRECT? → SELECT → LADDER? → CHAIN_SELECT`.

- **RESOLVE (intent)** — apply `intent-clarification.md` (GATHER git log / `.agents/PROJECT.md` / history → READ tone/scope/urgency → DECIDE). Produce a one-line intent statement **with stated assumptions** (Three Laws #3: never hide assumptions).
- **GATE (confidence floor)** — assign `context_confidence` from the discrete evidence bands in `confidence-scoring.md`. `< 0.60` OR 2+ valid interpretations → ask **ONE** focused question with options (CIPHER_GATE), integrate the answer, re-type the unknown dimensions, and assign a new band. Never build a chain on a sub-floor classification — proceeding on a guessed intent is forbidden (`Never: ignore blocking unknowns`). **GATE is not skippable by reaching LADDER**: a sub-floor score on the SCOPE dimension (how literal/broad the ask is — `_common/CONTEXT_SUFFICIENCY.md`) still requires GATE's clarifying question before proceeding, even when the intent also turns out to match no Recipe/task-type. Only routing-dimension certainty ("no skill fits, and SCOPE/intent are otherwise clear") skips straight to LADDER without a further GATE question. **Tone precedence**: a frustrated tone compresses GATE's question to exactly ONE tightest-framing question with pre-filled safest-default options — it never authorizes zero questions on a sub-floor classification (`intent-clarification.md` § Tone & Scope Interpretation Patterns, Precedence rule).
- **MULTI? (multi-domain check — mandatory step, not a disconnected note)** — before REDIRECT/SELECT commit to a single chain, explicitly test whether the resolved intent spans **2+ independent domains** (e.g. "add OAuth *and* fix the slow dashboard"). This check must fire on every walk of the flow, immediately after GATE — a literal, mechanical walk of RESOLVE→GATE→REDIRECT that never pauses to ask "is this actually one domain?" is exactly how the second domain of a mixed request silently drops. If 2+ domains are found: do NOT force one chain — decompose with **Sherpa** into per-domain subtasks, route each independently (each subtask re-enters at its own GATE — a subtask can be sub-floor on confidence even when the combined request passed GATE — then proceeds through REDIRECT? and the rest of the flow), then run as parallel tracks under hub-spoke ownership. One chain straddling domains is an anti-pattern. If exactly one domain, proceed to REDIRECT.
- **REDIRECT (Recipe-match check — the key step)** — before building an ad-hoc chain, translate the resolved intent to English canonical intent and test it against the Recipe set (semantic match, per the Signal Keywords table). If it maps to a Recipe (`bug` / `feature` / `security` / `refactor` / `optimize` / `kaizen` / `apex` / …), **redirect to that Recipe and run its phase contract** — do NOT hand-roll a chain that shadows a curated one. CLASSIFY builds an ad-hoc chain ONLY for task types with **no Recipe** (the matrix-only types below). This prevents a worse ad-hoc chain from silently replacing a maintained Recipe.
- **SELECT (task-type → chain)** — for the no-Recipe case: classify into one of the task types below, take its default chain, apply Sherpa-skip / add-when adjustments (§ Sherpa Skip & Chain Adjustment below), and check guardrail needs (L4 / destructive / 10+ files).
- **LADDER (no task-type match — the true-gap case)** — if RESOLVE's intent matches neither a Recipe (REDIRECT) nor a row in the Task Type table below (SELECT), do NOT hand-roll a chain yet. Spawn `compass(recommend)` as a hub-spoke step with the resolved intent. If `compass` returns a fit (1-3 candidate skills), redirect to that skill's default Recipe or explicit Default dispatch and record `fallback_taken: compass-invoked`. If `compass` returns Gap mode (no matching skill — `compass/SKILL.md` Output Routing, "No matching skill" row), spawn `architect` with the gap signal to produce a proposal artifact (`ARCHITECT_TO_NEXUS_HANDOFF`) and record `fallback_taken: architect-invoked`. Present the proposal to the user before building a new skill (Ask First: "Approving creation of a new skill via LADDER" — `nexus/SKILL.md` § Ask First; distinct from the "first-time use of a newly registered agent" bullet, which governs a *subsequent* chain that includes an already-registered new agent). Only on explicit user decline does CLASSIFY fall back to an ad-hoc chain — record `fallback_taken: neither — reason: user declined gap-fill` and log it as `Fallback: ad-hoc (reason: user declined gap-fill)`, never silent. **Exception (LADDER triviality/meta carve-out)**: a direct-answer request — a one-line **factual/lookup** question with a single correct answer, or a meta-question about the harness itself (e.g. "what does CLASSIFY do?") — answers directly without walking the ladder; this carve-out is narrow and bounded to non-task-shaped requests only (see `nexus/SKILL.md` § Never). A one-line **judgment/decision** question (e.g. "REST or GraphQL for the new API?") is NOT carve-out-eligible — it is task-shaped (DECISION → Magi, or gedanken per the verdict-seeking rule in `signal-keywords.md`) and routes through REDIRECT with Three-Laws assumption disclosure. Any request that asks for work product (code, a document, an analysis, a chain of steps) is task-shaped and the ladder remains mandatory. **Non-closable gap**: if `architect` determines the requested act is legally/physically restricted to a licensed human (e.g. a USPTO filing under 37 CFR 11.5), it declines the gap-fill proposal and surfaces the boundary instead — outcome remains `fallback_taken: architect-invoked` with an explicit boundary note (not `neither`; the ladder was walked, it just could not close the gap with a skill). Both `compass` and `architect` spawns use the standard Agent Spawn Template (`reference/hub-authoring.md` § Agent Spawn Template) and therefore inherit the same agy/codex silent-output mitigations (`_common/CLI_COMPATIBILITY.md §9.2/§9.3`) as every other Nexus spawn — no separate handling needed.

**Exit:** a selected chain (or Recipe redirect, or LADDER outcome) + confidence ≥ floor + documented intent/assumptions → `CHAIN_SELECT` → gated `SPECIFY?` (`specify-phase.md`) → `EXECUTE`. **`SPECIFY` never substitutes for `GATE`**: it hardens the *language* of an intent contract that already cleared the confidence floor, and specifying a guessed intent only yields a precise instruction to do the wrong thing.

**Anti-patterns prevented** (prevents: ad-hoc chain shadowing a curated Recipe → REDIRECT, routing on a guessed intent → GATE, one overloaded chain for a multi-domain ask → MULTI?, hidden assumptions → RESOLVE, silent ad-hoc fallback with no compass/architect consultation → LADDER)

---

## Orchestration Gate — the rung below "one agent"

Core Rule #1 picks the smallest chain. This gate asks the question underneath it: **should this be orchestrated
at all?** The rule minimizes among chains and therefore always yields one; a request that wants a fixed
sequence, or a single tool call, or an answer, gets a chain anyway — and pays coordination cost for structure
it never needed.

**Climb from the bottom, and record why each rung failed.** Evaluate in order — *direct answer · single tool
call · fixed sequence · one agent · a chain* — and take the first that suffices. When you skip a rung, name
the specific thing it could not do. "It might get more complex later" is not that reason: the future is
discounted, the coordination cost is paid today.

**Do not orchestrate when any of these holds:**

- **The steps are fixed and the exceptions are enumerable.** A known sequence with deterministic checks is a
  procedure, and a procedure executed by a chain is slower, costlier, and harder to audit than the same
  procedure written down.
- **One agent already has the context and the authority.** Splitting it produces context transfer and merge
  work, not parallelism.
- **The split is by role name only.** Planner/Researcher/Critic over one model, one context, and one set of
  permissions adds call count and failure points, not capability. If ownership, authority, knowledge, failure
  containment, and independent evolution are the same on both sides, it is one agent with stages.
- **Nobody owns the outcome if it fails.** If you cannot name, in advance, who is accountable when the chain
  produces a wrong result, the chain has no owner — it has participants. Fix that before adding steps.
- **Nothing verifies the result.** With no independent check, more steps produce more confident output, not
  more correct output.
- **The effect is irreversible and the controls for it do not exist.** See the Action-Tier ceiling in
  `routing-learning.md` — a `T4` effect under a `T1` ceiling is not a chain-design problem; it is a decision
  to make the effect reversible or to keep a human on the commit.

**Prefer proposal-then-commit over an agent that commits.** A chain that produces a proposal and lets a
deterministic step or a human commit needs almost none of the machinery above. Embedding the final
irreversible effect inside the agent loop is the most expensive available option, and it is rarely the one the
request required.

**Record the rejection, and make it re-openable.** When the answer is "do not orchestrate", say so with the
rung that sufficed and the reason the next rung was unnecessary — and name what would change the answer (a
second owner appears, the exception set stops being enumerable, an independent release cadence is needed).
A rejection with a stated re-open condition is a decision; a rejection without one gets silently re-litigated
on the next similar request.

**This gate cannot be satisfied by adding agents.** If it fires, the remedy is a smaller shape, never a
better-supervised larger one.

---

| Task Type | Primary Chain | Recipe Hints | Additions |
|-----------|---------------|-------------|-----------|
| BUG | Scout → **Sherpa?** → Radar → Builder → Radar → Guardian | Scout[RCA+defect-confirm], Sherpa[epic], Radar[failing repro test], Builder[root-cause fix], Radar[verify+regression], Guardian[pr] | +Sentinel (security), +Trail (regression from a past commit), +Ripple (blast radius). Skip Sherpa only when single-file atomic fix. **Reproduce-before-fix**; phase contract → § Sherpa Skip & Chain Adjustment below |
| INCIDENT | Triage → Scout → Builder | Triage[respond], Scout[bug], Builder[fix] | +Mend (known pattern), +Radar, +Triage (postmortem), +Flux (deep postmortem), +Matrix[combine] (failure scenarios) |
| FEATURE | Lens? → **Sherpa** → Forge? → Builder → Radar → Guardian | Lens[reuse-scan], Sherpa[spec+AC], Forge[spike], Builder[api], Radar[edge+verify-gate+per-AC], Guardian[pr] | +Muse/+Palette (UI), +Artisan (frontend prod), +Matrix (variant exploration), +Flux[reframe] (lateral thinking), +Flux[ideate] (idea exploration). Lens reuse-scan on existing codebases (skip greenfield). Forge only when approach unproven (spike, not shipped). Skip Sherpa only when single-file atomic change. Phase contract → § Sherpa Skip & Chain Adjustment below |
| INVESTIGATE | Lens | Lens[map] | +Scout (bug-related), +Canvas (viz), +Trail[bisect] (git) |
| BRAINSTORM | Flux | Flux[ideate] | +Flux[reframe] (reframe first), +Spark (spec after), +Magi (decide after), +Void (prune after) |
| DECISION | Magi | Magi[decide] | +Scribe[unified: vision] (biz-tech), +Flux[reframe] (reframe), +Flux[ideate] (explore before deciding) |
| SECURITY | Sentinel → Probe? → Builder → Probe/Radar → Vigil? → Guardian | Sentinel[triage+SAST], Probe[confirm-exploit/verify-closed], Builder[root-cause fix], Radar[regression], Vigil[detection rule], Guardian[security-aware PR] | +Breach (red-team scenario), +Shift (dependency CVE → upgrade), +Crypt (crypto fix), +Cloak/+Canon[regulatory] (privacy/compliance). **Confirm-exploit before & verify-closed after**; phase contract → § Sherpa Skip & Chain Adjustment below |
| REFACTOR | Radar? → Zen → Radar → Guardian | Radar[safety-net characterization], Zen[refactor], Radar[verify-equivalence], Guardian[behavior-neutral PR] | +Atlas[analyze] (architectural), +Grove[audit] (structure), +Grove[llm: audit] (folder structure), +Sherpa (multi-file). **Green-before-refactor**; safety-net skip for tool-assisted pure rename/extract. **→ `quell profile=refactor`** when the refactor must be driven to a clean external review (the loop keeps this contract as its Equivalence Gate — `reference/quell-recipe.md` §5a). Phase contract → § Sherpa Skip & Chain Adjustment below |
| OPTIMIZE | [locate layer] → Bolt/Tuner/Gear/Scaffold → Radar → Guardian | Bolt[profile+optimize: code/render/CPU/alloc/bundle], Tuner[explain+optimize: query/plan/index], Gear[build/CI/bundle], Scaffold[infra/runtime sizing], Radar[verify-speedup+no-regression — **independent of the optimizer**], Guardian[PR w/ Speedup Report] | +Trail (bisect a perf regression to the offending commit), +Scout (localize unknown hotspot layer), +Schema (DB index/migration — Ask First), +Gateway (network/payload contract), +Seek (search/ranking latency), +Siege (load-test), +Beacon (define the budget / prod SLO), +Flux (first-principles), +Matrix (target combos). **Measure-first / prove-with-a-number / profile-validity (Amdahl ≥ 20%)**. **Boundary**: one-shot fix at a measured hotspot on *correct* code — defect-caused slowdown → BUG; continuous parameter self-tuning (GC/threadpool/pool/cache-size loop) → AUTO_TUNING; a **set** of budget violations swept to zero across many targets → `mode=to-zero` (`_common/FINDING_LEDGER.md` member, `optimize-recipe.md` §3a — and it does **not** inherit AUTO_TUNING's self-measurement exception). Deep contract → `reference/optimize-recipe.md`; phase order → § OPTIMIZE Phase Contract below |
| KAIZEN | (Lens + Pulse?/Echo?/Voice?/Trace?) → Spark → Magi → (Bolt/Tuner ‖ Palette/Prose/Flow ‖ Zen/Sweep ‖ Artisan/Builder)[axis-prioritized] → Radar → Pulse?/Echo? [re-measure] → Guardian | Lens[map], Spark[propose], Magi[prioritize], Bolt[frontend]/Tuner[explain], Palette[usability]/Prose[microcopy], Zen[refactor]/Sweep[dead-code], Artisan[component]/Builder[api], Radar[regression], Guardian[pr] | +Scout (root-cause), +Atlas (structural), +Ripple (impact). **Boundary**: existing-feature polishing across multiple axes; differs from REFACTOR (internal-only), OPTIMIZE (perf-only), FEATURE (new capability) |
| ANALYSIS | Ripple → Builder → Radar | Ripple[impact], Builder[fix], Radar[edge], Canon[owasp], Sweep[dead] | +Canon (standards), +Sweep (cleanup) |
| API | Gateway → Builder → Radar | Gateway[design], Builder[api], Radar[edge] | +Quill[docstring], +Schema[design] |
| DEPLOY | Guardian → Launch | Guardian[pr], Launch[plan] | +Launch[weekly] (reporting) |
| MODERNIZE | Shift → Builder → Radar | Shift[detect+modernize], Builder[crud], Radar[coverage] | +Polyglot (i18n), +Grove (structure), +Flux (first-principles), +Matrix (migration paths) |
| DOCS | Quill | Quill[docstring] | +Canvas[flow], +Scribe[convert] (format export), +Scribe (specs) |
| STRATEGY | Spark → Builder → Radar | Spark[propose], Builder[ddd], Radar[edge], Growth[seo], Pulse[kpi], Experiment[ab], Compete[matrix], Compete[swot], Growth[retention], Voice[nps] | +Growth/Compete/Voice/Pulse/Experiment, +Magi[simulate] (scenario sim) |
| STRATEGY_SIM | Magi | Magi[simulate], Compete[matrix], Compete[swot], Compete[battle-card] | +Compete (intel), +Pulse (KPI), +Magi[decide] (verdict), +Scribe (docs), +Canvas (viz), +Sherpa (execution) |
| MARKETING | Cast → Compete → Pulse → Saga → Growth → Funnel → Experiment | Cast[generate] (persona), Compete[matrix]/[swot] (competition), Pulse[kpi] (metrics first), Saga[story] (narrative), Growth[seo]/[cro]/[geo] (channels), Funnel[landing] (LP), Experiment[ab] (validation), Voice[nps] (VoC), Echo (message-reception check), Magi (positioning verdict) | +Sherpa (full chain, mandatory for ≥7 steps), +Field (qualitative persona derivation), +Magi (scenario sim), +Vision (product brand), +Compete[brand] (personal brand only), +Prose (copy), +Muse (brand tokens), +Trace (churn/session analysis), +Growth (churn ops), +Launch (GTM execution and reporting), +Echo[demand] (synthetic user voice when no real customers), +Magi[advisor] (advisor pressure-test), +Flux (reframe), +Matrix (multi-segment). **Boundary vs STRATEGY**: MARKETING/* delivers strategy/messaging/plan; STRATEGY/{seo,compete,retention,metrics,ab-test} delivers code/instrumentation for a single tactic. |
| INFRA | Scaffold → Gear → Radar | Scaffold[terraform], Gear[deps], Radar[edge] | +Builder[cli] (CLI tools), +Gear[gha] (GHA workflows) |
| GHA_WORKFLOW | Gear[gha] | Gear[gha], Sentinel[scan] | +Launch (release), +Sentinel (security) |
| PARALLEL | Rally | Rally[parallel], Sherpa[epic] | +Sherpa (decomposition), see Rally escalation |
| PROJECT | Nexus[deliver] | Nexus[deliver] | Scope-adaptive product/MVP delivery through the minimum viable specialist chain |
| MESSAGING | Gateway → Builder → Radar | Gateway[messaging], Builder[api], Radar[edge] | +Sentinel (security), +Scaffold (infra — required when connections are persistent and must scale horizontally). Covers chat-platform adapters, bot command frameworks, and realtime transports (WebSocket / SSE) as one integration surface — the `relay` merge of 2026-08-20 left them a single owner and a single Recipe, so `BOT` and `REALTIME` are no longer separate task types. Trigger: "Slack/Discord/LINE integration", "chat bot", "slash command", "WebSocket", "SSE", "realtime presence", "channel adapter". Inbound/outbound webhook *contracts* (HMAC, idempotency, DLQ) are `WEBHOOK` |
| WEBHOOK | Gateway → Builder | Gateway[webhook], Builder[api] | +Radar (tests), +Sentinel (security) |
| HOOKS | Hone | Hone[hook] | +Gear (Git hooks), +Sentinel (security) |
| SKILL_GEN | Sigil | Sigil[generate], Architect[create] | +Lens (codebase analysis), +Grove (structure), +Sigil[blueprint] (when the request is a whole project agent/recipe/workflow suite, not one skill) |
| PROJECT_LAYER | Sigil[blueprint] → Sigil | Sigil[blueprint], Sigil[generate] | Curated recipe: `layer` (`reference/layer-recipe.md`). +Lens (codebase analysis), +Nexus (routing/chain registration), +project-local Orbit when available (loop runners; otherwise Nexus[goal/apex]), +Hone (enforcement hooks), +Grove (placement). Sigil designs the project operating layer and authors its artifacts; runtime stays with Nexus. |
| EVOLUTION | Darwin (project-local) / Prune → Architect (fallback) | Darwin[health] when available; otherwise Prune[audit], Architect[improve] | Apply `_common/PROJECT_LOCAL_SKILLS.md`; +Void (sunset), +Canvas (viz) |
| KNOWLEDGE_SYNC | Lore (project-local) / Tome or Scribe (fallback) | Lore[curate] when available; otherwise Tome or Scribe | Apply `_common/PROJECT_LOCAL_SKILLS.md`; +Architect (design insights), +Nexus (routing feedback) |
| QUALITY | Judge → Canvas | Judge[pr], Radar[coverage] | +Zen[naming] (smells), +Radar (coverage), +Sentinel (security), +Atlas[analyze] (arch), +Sweep (dead code), +Matrix (combinatorial) |
| UX_RESEARCH | Field → Echo → Palette | Field[interview], Echo[walkthrough], Palette[usability], Trace[replay], Trace[persona] | +Cast[generate] (persona), +Trace (session data) |
| E2E | Voyager → Lens | Voyager[playwright], Radar[edge] | +Gear (CI), +Echo (persona-based), +Matrix (test matrix) |
| BROWSER | Vector → Builder | Vector[collect], Scout[bug], Builder[fix] | +Scout (bug repro), +Bolt[frontend] (perf), +Lens (evidence) |
| MACOS_AUTOMATION | Hone | Hone[automate] | +Weave[schedule] (cron/launchd timing), +Hone[hook] (wire as Claude Code hook), +Vector (web step before native step), +Sentinel (security screen generated do-shell-script/subprocess), +Scout (diagnose broken automation). macOS-only; dictionary-first, TCC-aware, destructive ops gated behind dry-run |
| DB_DESIGN | Schema → Builder → Radar | Schema[design], Builder[ddd], Radar[edge] | +Tuner[explain] (optimize), +Atlas[analyze] (arch review) |
| OBSERVABILITY | Beacon → Gear → Builder | Beacon[slo], Builder[fix] | +Triage (incident link), +Scaffold (capacity) |
| AI_FEATURE | Oracle → Builder → Radar | Oracle[prompt], Builder[api], Radar[edge] | +Gateway (API), +Stream (pipeline), +Sentinel (safety) |
| PROMPT_SPEC | Chisel | Chisel[spec], Chisel[scan] (detection only), Chisel[role] (persona lines only), Chisel[audit] (checklist scoring) | +Oracle (the prompt is a **production asset** — versioning, eval gates, or enforcement-layer routing needed; also when the complaint is a *bad output* rather than vague wording, since the five-layer triage decides whether wording is the problem at all), +Scribe (derived criteria should become a durable spec doc), +Attest (criteria set to verify an artifact against), +Magi (an instruction conflict needs a product verdict). **Boundary**: the *text the user supplies* is the object → Chisel; the user's own live request being ambiguous → CLASSIFY GATE (`intent-clarification.md`), never Chisel |
| PRERELEASE | Guardian → Launch | Guardian[strategy], Launch[plan] | +Sentinel (security gate), +Radar (test gate) |
| REQUIREMENTS | Scribe[unified] → Scribe → Sherpa | Scribe[unified: vision], Scribe[prd], Sherpa[epic], Echo[demand], Saga[story], Saga[scenario] | +Canvas (diagram), +Magi[decide] (decision), +Saga (narrative), +Cast[generate] (persona) |
| DESIGN_SYSTEM | Vision → Muse → Vitrine → Quill | Vision[system], Muse[tokens], Vitrine[story] | +Palette[usability] (a11y), +Artisan[component] (impl) |
| DESIGN_SYSTEM_DOCS | Muse → Vitrine + Canvas → Quill | — | +Vision (direction), +Artisan (live examples) |
| CONTENT | Prose → Echo → Artisan | Prose[microcopy], Prose[errors], Prose[onboarding], Voice[nps], Voice[review], Voice[sentiment] | +Polyglot (i18n), +Field (insights) |
| DEV_EXPERIENCE | Hone → Gear | Hone[env], Gear[deps], Hone[hook] | +Builder[cli] (tooling the environment needs), +Sigil (project skills), +Hone[audit] (AI CLI audit) |
| LOAD_TEST | Siege → Bolt → Builder | Siege[load], Siege[contract], Siege[chaos], Siege[mutation], Bolt[frontend], Builder[fix], Radar[edge] | +Beacon[slo] (SLO), +Triage (resilience), +Matrix (scenario combos) |
| DEMO | Cue → Quill | Cue[demo], Cue[record] | +Cue[scenario] (scenario), +Cue[onboard] (onboarding), +Vitrine (catalog), +Growth (marketing) |
| SPRINT_RETRO | Launch → Canvas | Launch[weekly], Canvas[flow] | +Quill[docstring] (publish), +Triage (incident link) |
| KNOWLEDGE | Scribe | Scribe[prd] | +Quill (polish), +Scribe[convert] (format export) |
| REVIEW | Judge → Builder | Judge[pr], Builder[fix] | +Zen (refactor), +Sentinel (security), +Matrix (impact dimensions), +Flux (blind-spot) |
| YAGNI | Void → Sweep/Zen | Void[prune] | +Magi (approval), +Pulse (usage data) |
| REMEDIATE | Mend → Radar | Mend[runbook], Radar[regression] | +Beacon[slo] (SLO check), +Gear (infra config), +Triage (escalation) |
| SPEC_VERIFY | Attest | Attest[verify], Attest[bdd], Attest[trace], Radar[coverage] | +Scribe (spec gaps), +Radar (BDD→tests), +Builder (violation fixes) |
| LOOP_OPS | Orbit (project-local) / Nexus[goal/apex] (fallback) | Orbit[generate] when available; otherwise Nexus[goal/apex] | Apply `_common/PROJECT_LOCAL_SKILLS.md`; +Builder (script changes), +Guardian (commit policy), +Radar (verification closure) |
| DESIGN | Frame → Artisan → Radar | Frame[extract], Artisan[component], Radar[edge], Pixel[reproduce] | +Muse[tokens] (tokens), +Vision (direction), +Forge (prototype) |
| DESIGN_WORKFLOW | Atelier (orchestrator) | Atelier[pipeline], Forge[ui], Forge[fullstack] | Full design→code loop: Vision → Muse/Frame → Forge → Artisan → Vitrine → Canvas. Persists design system to `.agents/design-system/`. Use when the task spans design direction + tokens + prototype + implementation + catalog in a single pipeline |
| ARCHITECTURE | Atlas → Canvas | Atlas[analyze], Canvas[flow] | +Lens[discover] (analysis), +Scribe[hld] (docs), +Ripple[impact] (impact) |
| CREATIVE | Vision → Builder → Artisan | Builder[image], Ink[icon] | +Builder[image-edit] (image edit), +Builder[image-prompt] (prompt opt), +Ink[illustration] (illust), +Growth (marketing). **Image-generation engine default**: when actual image assets are the deliverable, use Codex built-in `image_gen`; use Builder's Gemini API path when the deliverable is reproducible generation code (seeds/batch/metadata) or fine parameter control is required |
| MOCKUP | Pixel → Radar | Pixel[reproduce], Radar[coverage], Flow[hover] | +Frame (Figma source), +Muse (tokens), +Flow[loading] (loading states), +Flow[transition] (transitions) |
| DESIGN_AUDIT | Pixel[gap-report] → Canon/Judge | Pixel[gap], Pixel[verify], Pixel[audit] | +Artisan (remediation), +Muse (token regression), +Voyager (VRT baseline). Trigger: "gap analysis", "fidelity audit", "design review". Produces 8-dim × 5-severity × 9-RC Markdown+JSON report with visual artifacts. **Reviewed self-measurement loop** (RO-3 allowlisted): Pixel[gap]→Pixel[verify] is the same specialist re-running its own audit instrument, not a producer grading its own correctness claim — see `routing-oracle.py` `RO3_REVIEWED_EXCEPTIONS` |
| BRANDING | Compete → Quill | Compete[brand] | +Growth (SEO/SMO), +Canvas (viz), +Prose (content), +Launch[pr-flow] (portfolio evidence) |
| ECOSYSTEM | Darwin (project-local) → Gauge → Canvas / Prune → Architect (fallback) | Darwin[health] when available; otherwise Prune[audit], Architect[improve] | Apply `_common/PROJECT_LOCAL_SKILLS.md`; +Void (prune) |
| PRIVACY | Cloak → Builder → Radar | Cloak[pii], Builder[fix], Radar[edge] | +Canon[regulatory] (regulatory), +Sentinel (static scan), +Canon (standards) |
| COMPLIANCE | Canon[regulatory] → Builder → Radar | Canon[soc2], Builder[fix], Radar[coverage] | +Cloak (privacy), +Canon (standards), +Scribe (policy docs) |
| CRYPTO | Crypt → Builder → Radar | Crypt[algorithm], Builder[fix], Radar[edge] | +Sentinel (security review), +Probe (TLS validation) |
| VIDEO_SCRIPT | Cue | Cue[script], Cue[storyboard], Cue[demo] | +Cue[narration] (narration), +Cue[explainer] (explainer), +Cue[scenario] (scenario design), +Cue[record] (Playwright recording), +Prose (copy), +Growth (marketing) |
| LEGACY | Trail → Shift → Builder | Trail[static-rules], Builder[harden], Radar[coverage] | +Shift[plan] (migration), +Trail[history] (git history), +Lens[discover] (exploration), +Tome (documentation) |
| LANDING_PAGE | Funnel → Artisan → Radar | Funnel[build], Funnel[cta], Forge[landing], Radar[edge], Builder[image], Flow[hover] | +Growth (SEO/CRO), +Prose (copy), +Pixel[reproduce] (mockup), +Ink[icon] (icons), +Flow[transition] (transitions), +Echo (persona test) |
| FINOPS | Ledger → Scaffold → Gear | Ledger[estimate], Ledger[rightsizing], Ledger[ri-sp], Ledger[anomaly], Ledger[ai-gpu] | +Pulse (metrics), +Beacon (monitoring), +Canvas (dashboard spec) |
| TEST_DATA | Radar | Radar[fixtures], Radar[coverage] | +Schema (DB fixtures), +Siege (load data), +Builder (factory impl) |
| SEARCH | Seek → Builder → Radar | Seek[fulltext], Seek[vector], Seek[hybrid], Seek[index], Seek[rag], Builder[api], Radar[edge] | +Oracle[rag] (RAG/embeddings), +Schema (indexes), +Tuner[explain] (query perf), +Vector[crawl] (crawl source) |
| MULTI_TENANT | Schema[tenant] → Builder | Schema[tenant], Builder[ddd], Radar[edge] | +Sentinel (security), +Scaffold (infra), +Radar (isolation tests) |
| MIGRATION | Shift → Builder → Radar | Shift[plan], Builder[harden], Radar[regression] | +Trail (static-rules legacy analysis + history), +Shift[modernize] (native API replacement) |
| PRESENTATION | Stage → Canvas | Stage[marp], Stage[conference], Stage[timing] | +Stage[reveal] (reveal.js), +Stage[slidev] (Slidev/Vue), +Cue[script] (narrative), +Quill (content), +Scribe[convert] (export) |
| LEARNING | Tome → Quill | Tome[learn] | +Canvas (diagrams), +Trail (change context) |
| WORKFLOW | Weave → Builder → Radar | Weave[design], Builder[api], Radar[edge] | +Canvas (diagram), +Schema (persistence), +Attest (spec verify) |
| ARTICLE | Tome → Growth | Tome[note], Tome[zenn], Tome[qiita], Tome[devto], Tome[article-series] | +Prose (microcopy polish), +Stage (slide version), +Saga (narrative reshape), +Canvas (article diagrams), +Scribe[convert] (PDF/Word export). Trigger: "tech blog", "note/Zenn/Qiita/dev.to", "article series", "article" |
| SCHEDULE | Weave → Builder → Gear | Weave[schedule], Builder[api], Radar[edge] | +Weave[retry] (retry state machine), +Beacon[alerts] (schedule SLO/alerts), +Gear[gha] (GHA cron), +Voyager[playwright] (temporal test scenarios), +Judge (correctness review), +Triage (incident → replay plan). Trigger: "cron", "timezone", "DST", "retry/backoff", "backfill", "business calendar" |
| GRAMMAR | Builder → Radar | Builder[grammar], Builder[crud], Sentinel[injection], Radar[edge] | +Sentinel (regex security audit), +Canon (grammar → standards compliance), +Atlas (parser module boundary), +Shift (codemod migration), +Judge (grammar review). Trigger: "regex", "parser", "grammar", "DSL design", "AST transform", "ReDoS" |
| PORTING | Lens/Atlas → Port → Native → Voyager → Launch | Port[blueprint], Port[parity], Port[map], Port[roadmap], Native[swiftui], Native[compose], Voyager[playwright], Launch[plan] | +Trail (web business-rule extraction), +Field (mobile user research), +Vision (mobile design direction), +Frame (Figma mobile handoff), +Scaffold (project skeleton), +Gateway (mobile-friendly BFF), +Schema (local DB), +Polyglot (i18n), +Cloak (Privacy Manifest), +Crypt (Passkey/Keychain). UI component-name lookup (Web ↔ HIG ↔ Material 3) → `port/reference/ui-terminology-matrix.md` |
| MOBILE_NATIVE | Native → Radar → Vitrine → Launch | Native[swiftui], Native[compose], Native[liquidglass], Native[expressive], Native[offline], Native[push], Native[deeplink], Native[passkey], Native[privacy], Native[rollout], Native[store], Native[visualloop] | +Port (porting blueprint as input), +Forge (prototype validation), +Vision (design direction), +Muse (mobile tokens), +Voyager (mobile E2E), +Cloak (Privacy Manifest review), +Crypt (Passkey/Keychain). `visualloop` when a reference image/design is the target and the screen must be iterated against it. Pure-native only — RN/Flutter/KMP/CMP out of scope |
| MACOS_NATIVE | Native[macos] → Radar → Vitrine → Launch | Native[macos], Native[macdist] | +Forge (prototype validation), +Vision (Mac design direction — `vision/reference/apple-design-trends.md`), +Muse (tokens), +Hone[automate] (automation-readiness / scripting surface of the shipped app), +Cloak (privacy + TCC purpose strings), +Crypt (Keychain / code-signing key handling), +Gear (CI signing + notarization wiring). Pure macOS native — Catalyst-vs-native is an explicit decision (`native/reference/catalyst-decision.md`); iOS/Android → `MOBILE_NATIVE`; automating an *existing* Mac app (AppleScript/JXA) → Hone `automate`, not Native |
| IOS_UI_TEST | Voyager[ios] → Gear → Launch | Voyager[ios], Gear[ci], Launch[plan] | +Launch (App Store screenshot release step). XCUITest and snapshot scope use Voyager `ios`; Appium/Detox/Maestro use Voyager's platform modes. |
| ADVISORY | Magi → (Builder/Echo/Sherpa) | Magi[advisor] | +Magi[simulate] (long-term strategy → tactical), +Spark (feature idea reality check), +Field (user findings → next action), +Sherpa (multi-step action decomposition), +Builder (committed action implementation), +Echo[demand] (synthetic-user validation). Trigger: "office hours", "what should I focus on", "I'm stuck", "creative direction reality check", "review my pitch", "Demo Day deck", "investor pitch". 1 session = 1 bottleneck + 1-3 SMART actions |
| SUPPLY_CHAIN_AUDIT | Chain | Chain[manifest], Chain[scan], Chain[intake], Chain[pin] | +Sentinel (app-side SAST contrast), +Gauge (SKILL.md format audit), +Hone (hook design), +Gear (CI/CD config). Active malware infection uses Chain's incident Recipes; SECURITY covers application vulnerabilities |
| FIGURE_CHANNELING | Magi | Magi[advisor] | +Flux[reframe] (reframe first, then apply a thinker known for that frame), +Flux[ideate] (expert mental models as ideation seeds), +Scribe/Quill (write the reading up). **Advisory lenses are not a verdict** — choose Magi[decide] explicitly when arbitration is requested; open brainstorming → Flux[ideate]; synthetic user personas → Cast. Every claim carries an ATTESTED/INFERRED/SPECULATIVE tag; fabricated quotes are stripped; deceptive uses are refused |
| MALWARE_RESPONSE | Chain → Triage → Crypt | Chain[malware-scan], Chain[eradicate], Chain[rotate], Triage[respond], Crypt[rotation] | +Vigil (Sigma/YARA rule authoring), +Sentinel (static rescan), +Trail (git history of infection vector). Always scan before credential rotation; wrong rotation order can trigger destructive retaliation payloads |
| AUTO_TUNING | Bolt → Tuner? → Radar | Bolt[profile], Bolt[tuning-loop], Bolt[verify] (auto-tuning absorbed from dial), Tuner[explain] | +Schema (DB pool tuning), +Beacon (SLO observation), +Siege (load-test validation), +Gear (env vars / config changes). Don't confuse with OPTIMIZE (one-shot) or LOAD_TEST (Siege-led). **Reviewed self-measurement loop** (RO-3 allowlisted): Bolt's profile→tuning-loop→verify is a continuous re-profile cycle matching OPTIMIZE's own ITERATE pattern, not a missing independent verifier — see `routing-oracle.py` `RO3_REVIEWED_EXCEPTIONS` |
| LEGAL_REVIEW | Canon → Scribe | Canon[tos], Canon[privacy], Canon[tokushoho], Canon[legal-gap], Scribe[policy] | +Canon[regulatory] (SOC2/GDPR translation), +Cloak (PII handling design), +Vigil (regulation → detection rule), +Scribe (policy documentation). Legal advice belongs to a lawyer — Canon covers document completeness and risk flags only |
| PRIORITIZE | Rank → Magi | Rank[ice], Rank[rice], Rank[wsjf], Rank[moscow], Rank[kano], Rank[cod] | +Magi[decide] (final verdict), +Spark (candidate generation), +Pulse (KPI evidence), +Echo[demand] (user-value evidence), +Magi[simulate] (strategic alignment), +Void (cut bottom items). Don't confuse with MAGI (qualitative arbitration) or VOID (scope cutting) |
| PREMORTEM | Omen → Ripple | Omen[premortem], Omen[fmea], Omen[rpn], Omen[ap], Ripple[impact] | +Magi (failure-scenario selection), +Echo (UX failure modes), +Experiment (validation experiment design), +Triage (postmortem contrast), +Matrix (failure-scenario combinations). Pre-event — Triage's postmortem is post-event |
| MANUAL_QA | Matrix | Matrix[qa-scenario], Matrix[equiv-class] | +Radar (bridge to auto tests), +Radar (test data), +Voyager (automation candidates for E2E), +Attest (spec compliance). Trigger anchors → `reference/signal-keywords.md`. Automated code belongs to Radar/Voyager |
| TEST_INTELLIGENCE | Canvas/Pulse | Canvas[heatmap], Canvas[traceability], Canvas[test-shape], Pulse[flake-dashboard], Pulse[regression-timeline], Pulse[mutation-overlay] (absorbed from vista) | +Radar (fix test bodies), +Voyager (consume E2E results), +Siege (load-test results). Trigger anchors → `reference/signal-keywords.md`. Visualization side — writing tests belongs elsewhere |
| PROJECT_STATUS | PDM | PDM[status], PDM[features], PDM[gaps], PDM[roadmap], PDM[wbs], PDM[ask] | +Lens[map] (code-feature evidence), +Attest (AC conformance → status refinement), +Rank (prioritize the roadmap), +Sherpa (decompose epics into execution), +Scribe (author spec gaps), +Trail (when features landed), +Canvas (roadmap/status viz). **Boundary**: read-only reconciliation of *planned scope vs implemented code*; differs from PROJECT (Nexus[deliver] delivery lifecycle), PRIORITIZE (Rank scoring), SPEC_VERIFY (Attest AC conformance), REQUIREMENTS (Scribe[unified]/Scribe authoring), INVESTIGATE (Lens code comprehension) |

---

## Sherpa Skip & Chain Adjustment

### FEATURE Phase Contract

`feature` is the highest-traffic Recipe; its chain row is a summary. Phase semantics (read before executing a non-trivial feature):

- **SURVEY (Lens, conditional) — reuse before you build** — for any feature added to an **existing** codebase, scan for reusable implementations BEFORE decomposing: does the function / component / hook / pattern already exist? Extend or compose the existing one instead of reinventing it. Skip only for greenfield. The most common feature-implementation waste is re-deriving code that already ships — this step is the guard (repo rule: don't re-implement what already exists).
- **SPEC (Sherpa)** — decompose into atomic steps AND **lock acceptance criteria + scope boundary before any code** (front-loaded ACs become Radar's test targets and the VERIFY gate). Fold SURVEY's reuse findings into the plan (build-on-existing vs build-new, stated per step). Skip Sherpa only when the change is single-file atomic, but still state the ACs inline.
- **PROTOTYPE (Forge, conditional)** — run **only when the approach is unproven** (new UI pattern, uncertain API shape, integration risk). Forge output is a **throwaway spike to validate feasibility, NOT the shipped artifact**. Skip for well-understood CRUD/backend additions — Builder goes straight to production. Prevents both "rebuild from scratch, lose the spike's learnings" and "ship the prototype as production".
- **BUILD (Builder; +Artisan for frontend production)** — production implementation carrying forward the spike's validated decisions and SURVEY's reuse plan. UI surface routing: **+Muse** when introducing new design tokens/visual primitives, **+Palette** when interaction-heavy, **Artisan** owns frontend production code. Backend/CLI features skip all three.
- **VERIFY (Radar + gate)** — Radar adds edge-case/regression tests; THEN the **VERIFY gate requires existing build + test + lint/typecheck green** against the locked ACs. Not "new tests pass" — the whole check suite. Additionally confirm **each locked AC is actually satisfied** (covered by a test or demonstrated behavior), not merely that the suite is green — convergence on green ≠ the feature does what the spec required. A feature is not done until the gate passes (repo quality rule).
- **SHIP (Guardian)** — PR-prep: commit granularity, PR title/description, ACs linked to evidence.

**Anti-patterns prevented** (prevents: prototype-shipped-as-production → PROTOTYPE, feature-without-acceptance-criteria → SPEC, new-tests-green-but-build-broken → VERIFY full suite, no PR discipline → SHIP, reinventing code that already ships → SURVEY, green suite that doesn't meet the spec → VERIFY per-AC)

### BUG Phase Contract

Bug-fixing has a best-practice order the default chain must honor — **reproduce before you fix**:

- **RCA (Scout)** — root-cause analysis: why the bug occurs, where to fix, reproduction steps, impact/blast radius. **Confirm it IS a defect** (not expected behavior / misconfig / user error) before proceeding — a misread "bug" exits here with an explanation, no code.
- **DECOMPOSE (Sherpa, conditional)** — only when the fix touches 3+ files or spans components. Skip for single-component atomic fixes.
- **REPRODUCE-FIRST (Radar)** — encode Scout's reproduction steps as a **failing automated test BEFORE any fix**. The failing test is the acceptance criterion: red now, green after the fix. A regression test written *after* the fix can't prove it actually addresses the reported bug — it never failed.
- **FIX (Builder)** — fix the **root cause** Scout identified, not the symptom. Symptom-only patches (swallowing the error, masking the output, broad `try/except`) are rejected — repo rule: fix root causes, don't silence.
- **VERIFY (Radar + gate)** — the repro test now **passes** (bug gone), the existing build + test suite stays green (no new regression), and Scout's blast-radius areas are spot-checked. `+Sentinel` when the bug has a security dimension.
- **SHIP (Guardian)** — PR carrying the repro test + root-cause explanation, so the fix is auditable and the regression is permanently guarded.

**IMAGE BRANCH (screenshot attached)** — when the bug report carries a screenshot/error-screen image, two extra obligations bind:
- **At CLASSIFY**: run the full `_common/IMAGE_INPUT.md` pipeline including the mandatory five-section bug-report analysis (Observations / Inferred context / Problem points / Improvement proposals / Open questions). The **structured reading — never the raw image alone — enters Scout's `_AGENT_CONTEXT`**; image Ask-First triggers override AUTORUN.
- **At VERIFY**: when the defect is visually observable and a capture path exists, add the **Visual Fix Loop** (`IMAGE_INPUT.md` § Visual Fix Loop): re-capture the same screen post-fix and compare per Problem point (`resolved`/`unresolved`/`regressed`/`not-capturable`). No capture path → the visual claim is marked `UNVERIFIED` in `NEXUS_COMPLETE`, never silently asserted.
- Improvement proposals from the analysis that the user did not bundle stay **incidental** — listed in `NEXUS_COMPLETE` follow-ups, not folded into the fix scope.

**Anti-patterns prevented** (prevents: regression test that never actually failed → REPRODUCE-FIRST red→green, symptom patch leaving the cause live → FIX root-cause, fix that breaks something else → VERIFY suite+blast-radius, "fix" for a non-bug → RCA gate, no PR/regression guard → SHIP, downstream agents re-interpreting raw screenshot pixels → IMAGE BRANCH structured reading, visually-reported defect claimed fixed without an after-capture → IMAGE BRANCH Visual Fix Loop)

### SECURITY Phase Contract

A security fix is only real when the exploit is **confirmed closed** — static detection alone is faith-based. Order:

- **TRIAGE (Sentinel + severity)** — classify the finding: severity (CVSS), exploitability, and scope (**own code** vs **dependency CVE** vs **config/secret**). Severity sets urgency; scope sets the route — a dependency CVE routes to `Shift` (upgrade path), not a code patch. **Confirm it is a real vulnerability, not a SAST false positive**, before mobilizing.
- **CONFIRM-EXPLOIT (Probe / Breach, conditional)** — for dynamically-reachable vulns, **prove it is actually exploitable** (DAST / red-team) before fixing: don't burn effort on a false positive, and capture the working exploit as the verification oracle (the security analogue of bug's failing repro test). Skip for self-evident static issues (hardcoded secret, obvious injection sink).
- **FIX (Builder)** — fix the **root cause at the right layer** (parameterize the query, validate/encode at the boundary, rotate-and-vault the secret) — not a surface filter the next payload bypasses. Repo rule: defense at the boundary, don't silence.
- **VERIFY-CLOSED (Probe / Radar + gate)** — **re-run the exploit/DAST: the vuln no longer reproduces.** Radar encodes the attack as a regression test; the existing suite stays green. For secrets: confirm rotation AND removal from git history (a fix that leaves the secret in history is not closed).
- **DETECT (Vigil, conditional)** — add a detection rule (Sigma / Detection-as-Code) so reintroduction or in-the-wild exploitation is caught. Recommended for high-severity or recurring vuln classes.
- **SHIP (Guardian)** — **security-aware PR**: do NOT disclose exploit details in a public commit before the patch is deployed; link to the advisory/CVE; coordinate disclosure timing.

#### `security mode=to-zero` — the scanner-finding sweep

The phases above handle **a** vulnerability (or a triaged set) once. `mode=to-zero` wraps them in a loop whose completion oracle is a **scanner's finding set over a frozen scope** driven to zero at a CVSS floor. It is a member of `_common/FINDING_LEDGER.md` — **read that file before running this mode** — and declares its five slots there rather than restating the machinery:

| Slot | `security mode=to-zero` |
|------|-------------------------|
| **(a) Evaluator** | SAST / SCA / DAST scanners run by `Sentinel` (static) and `Probe` (dynamic) — deterministic tools, independent of the fixer by construction |
| **(b) Frozen scope** | the scan scope × the scanner set × the CVSS floor (default `floor=high`) |
| **(c) Identity** | **derived** — code findings `sha1(rule_id ⊕ normalized_path ⊕ enclosing_symbol)`, dependency findings `sha1(advisory_id ⊕ package ⊕ manifest)`. **Line numbers excluded** |
| **(d) Validity gate** | the existing **VERIFY-CLOSED** discipline, per cycle: the exploit no longer reproduces, the suite is green, and the service still starts and serves — a fix that closes a vuln by breaking availability fails the gate |
| **(e) Invariant** | behavior and availability preserved. No profiles |

**Disposition added:** `RISK-ACCEPTED (owner, expiry)`. Risk acceptance is this domain's `WONTFIX`, and it is also its **self-dismissal analogue** (`FINDING_LEDGER.md` §6): a scan reaches zero fastest by accepting everything. So an acceptance without a **named owner and an explicit expiry date** is invalid; acceptance of a CRITICAL/HIGH finding is **Ask First**; and an acceptance whose expiry has passed **re-opens as `OPEN`** on the next run rather than persisting silently. `FALSE-POSITIVE-RATIFIED` keeps CONFIRM-EXPLOIT as its refute-polarity mechanism — the attempt to *prove* exploitability is what a dismissal must fail at.

Scope stays frozen: a fix requiring changes outside the scan scope is `DEFERRED` with a route, and a dependency CVE still routes to `Shift` for the upgrade path rather than being patched in place.

**Recurrence-prevention note**: "make sure it never happens again" is a distinct ask from DETECT — Vigil's detection rule catches this vuln *class* recurring or being exploited in the wild (reactive, after-the-fact). A recurrence-prevention request additionally adds `+Hone` (HOOKS — e.g. a pre-commit/CI hook that blocks the specific pattern from being reintroduced, proactive/mechanical). Both can apply together; neither substitutes for the other.

**Add-ons**: `+Crypt` (cryptographic design fix), `+Shift` (dependency CVE → upgrade), `+Cloak`/`+Canon[regulatory]` (privacy/compliance dimension), `+Sentinel` re-scan after fix, `+Hone` (recurrence-prevention hook, distinct from Vigil detection — see note above).

**Anti-patterns prevented** (prevents: "fixing" a SAST false positive → TRIAGE+CONFIRM-EXPLOIT, band-aid filter → FIX root-cause/right-layer, faith-based unvalidated fix → VERIFY-CLOSED re-run, vuln class silently reintroduced → DETECT rule, premature exploit disclosure → SHIP, secret left in git history → VERIFY-CLOSED history check)

### REFACTOR Phase Contract

Refactoring's invariant is **no external behavior change** — and the only proof of that is a test suite that passes identically before and after. The order matters:

- **SAFETY-NET (Radar, first — green before you refactor)** — refactoring is safe **only under a passing suite**; the tests are what prove behavior is preserved. Confirm the code under refactor has green coverage; if it's untested, add **characterization tests that pin current behavior FIRST**. You cannot preserve behavior you never captured. (This is the Fowler precondition the default `Zen → Radar` order inverts.) **Skip only** for tool-assisted pure rename/extract where the compiler/type-system guarantees equivalence.
- **SCOPE-GUARD** — confirm this is **internal-only**: no public API / signature / output-contract change. If external behavior must change, it is a `feature` or `bug`, not a refactor — redirect. Keeps the invariant honest.
- **REFACTOR (Zen)** — rename / extract / constant-ify / dead-code removal in **small reversible steps**. `+Atlas` when module boundaries move, `+Grove`/`+Grove[llm]` for structure, `+Sherpa` for multi-file.
- **VERIFY-EQUIVALENCE (Radar + gate)** — re-run the **SAME suite**: identical pass results (no behavior delta), build/lint green, public surface unchanged. Not just "tests pass" — *the same tests pass the same way*. A refactor that changes a test's expected value is a behavior change masquerading as a refactor.
- **SHIP (Guardian)** — **behavior-neutral** PR/commit, reviewable as a pure refactor, kept separate from any behavior-changing work.

**Anti-patterns prevented** (prevents: refactoring untested code with no behavior proof → SAFETY-NET green-first, "refactor" that changes external behavior → SCOPE-GUARD, silent behavior drift → VERIFY-EQUIVALENCE, behavior change mixed into an unreviewable commit → SHIP behavior-neutral)

### OPTIMIZE Phase Contract

Performance work has one law — **measure, don't guess** — and the default `Bolt/Tuner → Radar` chain skips the measurement entirely.

**Deep contract → `reference/optimize-recipe.md`** (layer taxonomy → tool binding, Profile-Validity gate incl. the Amdahl share, Speedup Report schema, checkpoint-resume, handoffs). Phase order:

`DEFECT-CHECK → LOCATE → MEASURE → PROFILE-VALIDITY → TARGET-GATE → OPTIMIZE → VERIFY → [ITERATE] → SHIP`

Full phase-by-phase detail, Add-ons, and Boundary → `reference/optimize-recipe.md` §3 / §13 / §10.

**Anti-patterns prevented** (prevents: MEASURE-FIRST, DEFECT-CHECK redirect, TARGET-GATE+ITERATE cap, VERIFY prove-with-number, VERIFY prod-representative, VERIFY cold-path/invalidation — full list `reference/optimize-recipe.md` §9)

### Sherpa Skip Conditions

Skip Sherpa from the default chain only when ALL apply:
- Task touches ≤ 2 files
- No implicit intermediate steps
- Single atomic operation completable in one focused step

### Chain Adjustment Rules

- `3+` files touched → add Sherpa (if not already in chain).
- Ambiguous or multi-step requirements → add Sherpa.
- `3+` test failures → add Sherpa for re-decomposition.
- Security-sensitive changes → add Sentinel or Probe.
- UI changes → add Muse or Palette.
- Slow database path → add Tuner.
- `2+` independent implementation tracks → consider Rally.
- `<10` changed lines with existing tests → Radar may be skipped.
- Pure documentation work → skip Radar and Sentinel unless the change affects executable behavior.

### Clarification and Decision Rules

Canonical: `SKILL.md` § Routing Quick Start (unclear context → inspect git state + `.agents/PROJECT.md` → one focused question) and § Safety Contract (auto-decision reversibility rule; the Ask First confirm triggers).

### Chain Design Rejection Rules

Reject a proposed expansion before execution when any row applies. These are structural gates, not advisory anti-pattern labels.

| Signal | Reject | Use instead |
|--------|--------|-------------|
| Fixed, enumerable procedure | An AI-selected multi-agent path | Direct answer, single tool call, or deterministic sequence |
| Subtasks are not independently verifiable | Role-name-only decomposition | One owner with internal stages |
| Dependencies or merge ownership are undefined | Parallel or hierarchical fan-out | Define dependency edges, one merge owner, and a verification gate first |
| Critical operation needs an unqualified fallback | Dynamic fallback routing | Stop and escalate to the user or the qualified owner |
| A delegated action is open-ended | “Handle appropriately” or free-form action choice | Closed action enum with required parameters and an explicit reject path |
| Run lacks a total budget or terminal condition | Retry/loop/fan-out expansion | Declare time, spawn/token, retry, and completion bounds first |
| Handoff would forward raw history | Full-context propagation | Pass the intent contract, state delta, evidence, and unresolved items only |
