# Nexus Agent Chain Templates Reference

**Purpose:** Chain **modifications** only — complexity/sub-type variants that differ from the default chain, dynamic addition/skip triggers, and Rally parallel escalation.
**Read when:** You already know the task type and need a variant, or you need to adjust an in-flight chain.

**Scope boundary (post-cleanup):** **Base chains live in `routing-matrix.md`** — it is the single source of truth for "which agents fire for task type X", including Recipe Hints and conditional Additions. This file holds only the *delta*: rows whose chain differs from that default. A row that merely restated the routing-matrix default has been removed; if a task type is absent here, use `routing-matrix.md` unchanged. Task types unique to this file (QA, TEST, COMPARE, UX_DESIGN) have no routing-matrix row and are fully owned here.

## Contents
- Chain Variants by Task Type (deltas from routing-matrix defaults)
- Forge → Builder Integration
- Dynamic Chain Adjustment Rules
- Rally Parallel Chain Variants

---

## Chain Variants by Task Type

Each row is a **deviation** from the `routing-matrix.md` default for that task type. Read the default there first; apply the variant here when its complexity/sub-type key matches.

**Rows are work-phase deltas, not full ship chains.** They deliberately omit the terminal **Guardian** (SHIP) step that `routing-matrix.md`'s default chains end with: Guardian still runs after the variant whenever the task type's matrix row includes it, and is simply not repeated on every row. Rows for types with no matrix row (QA, TEST, COMPARE, UX_DESIGN) and rows whose deliverable is not a code change (advisory, strategy, document packages) end where they are written — no Guardian is implied there.

| Type | Complexity | Chain Template |
|------|------------|----------------|
| BUG | simple | Scout → Lens → Builder → Radar |
| BUG | complex | Scout → Lens → Sherpa → Builder → Radar → Sentinel |
| INCIDENT | SEV1/2 | Triage → Scout → Builder → Radar → Triage (postmortem) |
| INCIDENT | SEV3/4 | Triage → Scout → Builder → Radar |
| API | new | Gateway → Builder → Radar → Quill |
| FEATURE | S | Builder → Radar |
| FEATURE | M | Sherpa → Forge → Builder → Radar |
| FEATURE | L | Spark → Sherpa → Forge → Builder → Radar → Quill |
| FEATURE | UI | Spark → Forge → Muse → Builder → Lens → Radar |
| FEATURE | UX | Field → Echo → Spark → Builder → Radar |
| FEATURE | frontend | Forge → Artisan → Radar |
| FEATURE | cli | Builder → Radar |
| FEATURE | innovation | Field → Flux → Spark → Builder → Radar |
| FEATURE | story-driven | Saga → Spark → Forge → Builder → Radar |
| REFACTOR | small | Zen → Radar |
| REFACTOR | arch | Atlas → Sherpa → Zen → Radar |
| REFACTOR | rethink | Atlas → Flux → Atlas → Sherpa → Zen → Radar |
| OPTIMIZE | app | Bolt → Radar |
| OPTIMIZE | db | Tuner → Schema → Builder → Radar |
| SECURITY | static | Sentinel → Builder → Radar → Sentinel |
| SECURITY | dynamic | Sentinel → Probe → Builder → Radar → Probe |
| SECURITY | full | Sentinel → Probe → Builder → Radar → Sentinel → Probe |
| SECURITY | red-team | Sentinel → Breach → Builder → Radar |
| SECURITY | purple-team | Breach → Vigil → Builder → Radar → Sentinel |
| SECURITY | detection | Vigil → Gear → Radar |
| SECURITY | detection-full | Sentinel → Vigil → Gear → Radar → Scribe |
| SECURITY | ai-red-team | Oracle → Breach → Builder → Radar → Sentinel |
| SECURITY | threat-model | Breach → Scribe |
| INVESTIGATE | flow | Lens → Canvas |
| INVESTIGATE | onboarding | Lens → Scribe |
| INVESTIGATE | pre-impl | Lens → Builder → Radar |
| INVESTIGATE | regression | Trail → Scout → Builder → Radar |
| INVESTIGATE | architecture | Lens → Atlas → Canvas |
| DOCS | convert | Scribe |
| DOCS | report | Launch[weekly] → Scribe |
| INFRA | local | Scaffold → Radar |
| QA | - | Lens → Echo → Radar |
| QA | e2e | Voyager → Lens → Radar |
| REVIEW | PR | Judge → Builder/Zen/Sentinel (based on findings) → Radar |
| REVIEW | pre-commit | Judge → Builder (if CRITICAL) |
| REVIEW | quick-scan | Judge |
| REVIEW | standard | Judge → Builder → Radar |
| REVIEW | deep-dive | Judge → Zen → Builder → Radar → Sentinel |
| UX_RESEARCH | persona-driven | Cast → Field → Echo → Palette |
| UX_RESEARCH | session-replay | Trace → Field → Echo → Palette |
| DB_DESIGN | optimize | Schema → Tuner → Builder → Radar |
| DB_DESIGN | with-streaming | Schema → Stream → Builder → Radar |
| E2E | ci | Voyager → Gear |
| COMPARE | quality-critical | Sherpa → Guardian |
| COMPARE | bug-fix | Scout → Radar |
| COMPARE | feature | Spark → Guardian |
| COMPARE | security | Sentinel |
| BROWSER | bug-reproduction | Scout → Vector → Triage |
| BROWSER | evidence | Vector → Lens → Canvas |
| BROWSER | performance | Vector → Bolt |
| DECISION | architecture | Magi → Builder/Zen (based on verdict) |
| DECISION | strategy | Scribe[unified] → Magi → Spark |
| DECISION | intent | Forge/Builder |
| DECISION | deadlock | Magi → Flux → Magi → Builder |
| ANALYSIS | standards | Canon → Builder → Radar |
| ANALYSIS | cleanup | Sweep → Zen → Radar |
| DEPLOY | full | Radar → Guardian → Launch |
| MODERNIZE | stack | Lens → Shift (detect+modernize) → Sherpa → Builder → Radar |
| MODERNIZE | i18n | Polyglot → Artisan → Radar |
| MODERNIZE | structure | Grove → Sherpa → Zen → Radar |
| UX_DESIGN | flow | Flow → Artisan → Radar |
| UX_DESIGN | creative | Vision → Muse → Forge → Artisan → Radar |
| UX_DESIGN | audit | Palette → Artisan → Radar |
| UX_DESIGN | storybook | Vitrine → Quill |
| UX_DESIGN | demo | Cue[demo] → Voyager |
| UX_DESIGN | session | Trace → Echo → Palette |
| UX_DESIGN | content-first | Prose → Vision → Sherpa → Muse → Forge → Artisan |
| UX_DESIGN | motion-intentional | Vision → Flow → Artisan → Radar |
| TEST | quality | Judge → Zen → Radar (iterative PDCA via Nexus) |
| STRATEGY | seo | Growth → Artisan → Radar |
| STRATEGY | compete | Compete → Spark → Builder → Radar |
| STRATEGY | feedback | Voice → Spark → Builder → Radar |
| STRATEGY | metrics | Pulse → Builder → Radar |
| STRATEGY | retention | Growth → Spark → Builder → Radar |
| STRATEGY | ab-test | Experiment → Builder → Radar |
| STRATEGY | data-pipeline | Stream → Schema → Builder → Radar |
| STRATEGY | reframe | Scribe[unified] → Flux → Magi → Scribe |
| STRATEGY | simulation | Magi → Canvas → Scribe |
| STRATEGY | simulation-full | Compete → Magi → Scribe → Canvas |
| MARKETING | quick | Compete → Growth → Funnel |
| MARKETING | full | Sherpa → Field → Cast → Compete → Pulse → Saga → Growth → Funnel → Experiment → Scribe |
| MARKETING | positioning | Compete → Cast → Magi → Saga → Echo → Scribe |
| MARKETING | gtm | Compete → Cast → Pulse → Saga → Growth → Funnel → Experiment → Launch |
| MARKETING | acquisition | Pulse → Compete → Growth → Funnel → Experiment |
| MARKETING | retention | Pulse → Trace → Growth → Voice → Spark → Experiment |
| MARKETING | content | Saga → Prose → Growth → Artisan → Radar → Pulse |
| MARKETING | brand | Vision → Compete → Cast → Saga → Prose → Muse → Growth |
| MARKETING | personal-brand | Compete[brand] → Prose → Growth |
| MARKETING | b2b-saas | Cast → Compete → Saga → Pulse → Growth → Funnel → Experiment |
| MARKETING | seo-geo | Growth → Prose → Artisan → Radar → Pulse |
| MARKETING | analytics | Pulse → Trace → Canvas → Scribe |
| MARKETING | voc | Voice → Echo → Spark → Experiment |
| MARKETING | persona-driven | Field → Cast → Echo → Compete → Saga → Growth |
| MARKETING | reframe | Flux → Compete → Cast → Magi → Saga → Scribe |
| QUALITY | quick | Judge → Zen → Radar → Canvas |
| QUALITY | standard | Judge → Zen → Radar → Sentinel → Canvas |
| QUALITY | full | Judge → Zen → Radar → Sentinel → Atlas → Sweep → Canvas |
| OBSERVABILITY | alert-only | Beacon → Gear |
| OBSERVABILITY | slo-design | Beacon → Gear → Builder → Radar |
| OBSERVABILITY | post-incident | Triage → Beacon → Gear → Builder → Radar |
| AI_FEATURE | eval-only | Oracle → Radar |
| AI_FEATURE | rag | Oracle → Gateway → Builder → Radar |
| AI_FEATURE | llm-pipeline | Oracle → Stream → Builder → Radar → Sentinel |
| PRERELEASE | quick | Guardian |
| PRERELEASE | full | Sentinel → Radar → Guardian → Launch |
| REQUIREMENTS | quick | Scribe[unified] → Scribe |
| REQUIREMENTS | complex | Scribe[unified] → Magi → Scribe → Sherpa → Canvas |
| REQUIREMENTS | narrative | Cast → Saga → Scribe[unified] → Scribe |
| DESIGN_SYSTEM | tokens | Vision → Muse → Artisan → Radar |
| DESIGN_SYSTEM | full | Vision → Muse → Vitrine → Artisan → Quill → Radar |
| DESIGN_SYSTEM | figma-driven | Frame → Vision → Muse → Vitrine → Quill |
| DESIGN_SYSTEM | composition | Vision → Sherpa → Muse → Artisan → Flow → Vitrine → Quill |
| DESIGN_SYSTEM_DOCS | quick | Muse → Vitrine → Quill |
| DESIGN_SYSTEM_DOCS | full | Vision → Muse → Vitrine + Canvas → Artisan → Quill |
| CONTENT | onboarding | Prose → Echo → Artisan → Radar |
| CONTENT | i18n | Prose → Polyglot → Artisan → Radar |
| DEV_EXPERIENCE | dotfiles | Hone[env] → Gear |
| DEV_EXPERIENCE | full-env | Hone[env] → Gear → Hone[hook] |
| DEV_EXPERIENCE | audit | Hone[env] → Sentinel → Gear |
| DEV_EXPERIENCE | cli-audit | Hone → Hone[env] → Gear |
| DEV_EXPERIENCE | cli-full | Hone → Hone[env] → Gear → Sentinel |
| LOAD_TEST | quick | Siege → Bolt |
| LOAD_TEST | standard | Siege → Bolt → Builder → Radar |
| LOAD_TEST | chaos | Siege → Bolt → Triage → Builder → Beacon |
| DEMO | ui-demo | Cue[demo] → Voyager → Vitrine |
| DEMO | full | Cue[demo] → Vitrine → Quill |
| SPRINT_RETRO | quick | Launch[weekly] |
| SPRINT_RETRO | full | Launch[weekly] → Canvas → Quill |
| KNOWLEDGE | full | Scribe → Quill → Scribe |
| KNOWLEDGE | research | Field → Scribe |
| SPEC_VERIFY | quick | Attest → Scribe |
| SPEC_VERIFY | standard/full | Attest → Scribe → Radar → Builder |
| LOOP_OPS | simple | Orbit (project-local) / Nexus fallback → Builder → Radar |
| LOOP_OPS | full | Orbit (project-local) / Nexus fallback → Builder → Guardian → Radar |
| EVOLUTION | quick | Darwin → Canvas |
| EVOLUTION | standard | Darwin → Architect → Void → Canvas |
| EVOLUTION | full | Darwin → Architect → Void → Lore → Canvas |
| SKILL_GEN | quick | Sigil → Lens |
| SKILL_GEN | full | Sigil → Lens → Grove → Gauge |
| YAGNI | standard | Void → Sweep → Zen → Radar |
| YAGNI | full | Void → Magi → Sweep → Zen → Pulse → Radar |
| REMEDIATE | standard | Mend → Radar → Beacon |
| REMEDIATE | full | Triage → Mend → Radar → Beacon → Vigil |
| GHA_WORKFLOW | new | Gear[gha] → Radar |
| GHA_WORKFLOW | security | Gear[gha] → Sentinel → Vigil |
| GHA_WORKFLOW | release | Gear[gha] → Guardian → Launch |
| PROJECT | init | Nexus[deliver] → Grove → Scaffold → Gear[gha] |
| PROJECT | full | Nexus[deliver] → Sherpa → Builder → Radar → Guardian → Launch |
| PROJECT | onboarding | Lens → Canvas → Scribe |
| ECOSYSTEM | skill-audit | Gauge → Architect → Darwin |
| DESIGN | figma-to-code | Frame → Muse → Artisan → Radar |
| DESIGN | figma-handoff | Frame → Forge → Builder → Radar |
| DESIGN | token-sync | Frame → Muse → Artisan |
| DESIGN | landing-page | Vision → Prose → Sherpa → Muse → Forge → Artisan → Radar |
| DESIGN | app-ui-restrained | Vision → Sherpa → Muse → Artisan → Flow → Radar |
| DESIGN | moodboard-first | Forge → Vision → Sherpa → Muse → Artisan → Radar |
| ARCHITECTURE | deployment | Scaffold → Gear → Canvas |
| CREATIVE | marketing-asset | Growth → Builder[image] → Prose → Artisan |
| MOCKUP | figma | Frame → Pixel → Radar |
| MOCKUP | full | Frame → Pixel → Muse → Artisan → Radar |
| MOCKUP | responsive | Pixel → Matrix → Artisan → Radar |
| DESIGN_AUDIT | basic | Pixel[gap-report] → Artisan |
| DESIGN_AUDIT | a11y | Pixel[gap-report] → Canon → Artisan |
| DESIGN_AUDIT | review | Pixel[gap-report] → Judge |
| DESIGN_AUDIT | full | Pixel[gap-report] → Canon → Judge → Artisan → Voyager |
| BRANDING | full | Compete[brand] → Growth → Prose → Quill → Canvas |
| BRANDING | portfolio | Compete[brand] → Launch[weekly] → Quill |
| FIGURE_CHANNELING | critique | Magi[advisor] → User/Builder |
| FIGURE_CHANNELING | decide | Magi[advisor] → Magi[decide] → Builder |
| FIGURE_CHANNELING | reframe-first | Flux → Magi[advisor] → Magi[decide] |
| FIGURE_CHANNELING | ideation-seed | Magi[advisor] → Flux → Spark |
| FIGURE_CHANNELING | founder | Magi[advisor] → Magi[advisor] |
| FIGURE_CHANNELING | write-up | Magi[advisor] → Scribe |
| PORTING | survey-only | Lens → Atlas → Port[survey] |
| PORTING | parity | Port[parity] |
| PORTING | blueprint | Lens → Atlas → Port[blueprint] |
| PORTING | full | Lens → Atlas → Field → Port[blueprint] → Native → Voyager → Launch |
| PORTING | regulatory | Port[regulatory] → Cloak → Crypt → Scribe |
| PORTING | xplat-decision | Port[xplat] → Magi |
| MOBILE_NATIVE | ios | Native[swiftui] → Radar |
| MOBILE_NATIVE | android | Native[compose] → Radar |
| MOBILE_NATIVE | both | Native[swiftui] + Native[compose] → Radar → Vitrine |
| MOBILE_NATIVE | offline | Native[offline] → Schema → Radar |
| MOBILE_NATIVE | passkey | Native[passkey] → Crypt → Radar |
| MOBILE_NATIVE | privacy | Native[privacy] → Cloak → Radar |
| MOBILE_NATIVE | rollout | Native[rollout] → Launch |
| MOBILE_NATIVE | full | Port[blueprint] → Native[swiftui] + Native[compose] → Radar → Voyager → Cloak → Launch |
| ADVISORY | advise-then-build | Magi[advisor] → Sherpa → Builder |
| ADVISORY | advise-then-validate | Magi[advisor] → Echo[demand] |
| ADVISORY | strategy-handoff | Magi → Magi[advisor] → Sherpa |
| ADVISORY | feature-reality-check | Spark → Magi[advisor] |
| ADVISORY | research-to-action | Field → Magi[advisor] → Sherpa → Builder |

**Single-agent sub-type variants** are not tabled — they are the Recipe Hints in `routing-matrix.md`. Examples: `ADVISORY/{1on1,group,triage,retro,pitch}` = `Magi[<mode>]`; `FIGURE_CHANNELING/{single,panel}` = `Magi[advisor]` / `Magi[advisor]`.

---

## Forge → Builder Integration

When using Forge → Builder chains, Forge MUST output:
- `types.ts` → Builder converts to Value Objects
- `errors.ts` → Builder converts to DomainError classes
- `forge-insights.md` → Builder uses as business rules reference

Builder then applies:
1. **Clarify Phase**: Parse Forge outputs, detect ambiguities
2. **Design Phase**: TDD (test skeleton first), domain model design
3. **Build Phase**: Type-safe implementation with Event Sourcing/CQRS if needed
4. **Validate Phase**: Performance optimization, error handling verification

---

## Dynamic Chain Adjustment Rules

### Addition Triggers

- 3 consecutive test failures → Re-decompose with Sherpa
- Security-related code changes → Add Sentinel
- Security needs runtime validation → Add Probe after Sentinel
- UI changes included → Consider Muse/Palette
- UX assumptions need validation → Add Field before Echo
- Code changes exceed 50 lines → Consider refactoring with Zen
- Type errors occur → Return to Builder to strengthen type definitions
- Database queries slow (>100ms) → Add Tuner
- New tables/schemas needed → Add Schema before Builder
- Critical user flow changes → Add Voyager for E2E coverage
- Multi-page feature implementation → Add Voyager
- Builder detects ON_AMBIGUOUS_SPEC → Escalate to user or return to Spark
- Complex distributed workflow → Builder activates Event Sourcing/Saga patterns
- High read/write ratio disparity → Builder applies CQRS pattern
- Red team assessment requested → Add Breach after Sentinel
- Detection rules needed → Add Vigil
- Problem framing stuck → Add Flux for perspective shift
- User names a real notable figure ("what would <figure> do here?", "critique this as <figure>") → Use Magi[channel/critique] for the advisory reading; invoke Magi[decide] only when a verdict is requested
- A decision panel keeps producing the same in-house viewpoints → Add Magi[advisor] before Magi[decide] to inject named-expert mental models
- Ideation has gone flat with generic ideas → Add Magi[advisor] before Flux so expert frameworks seed the brainstorm
- Figma design available → Add Frame before Artisan
- Mockup/screenshot to code → Add Pixel (faithful reproduction from image)
- Detailed design-to-code gap analysis / fidelity audit / design review requested → Add Pixel[gap-report]; chain to Canon for WCAG mapping when a11y is in scope, Judge for report quality review, Artisan for remediation
- Personal branding or portfolio → Add Compete[brand]
- Combinatorial testing needed → Add Matrix before Radar
- Feature has 3+ independent dimensions or variants → Add Matrix after Spark
- Review covers 4+ files across 2+ modules → Add Matrix before Judge
- Test coverage gaps identified → Add Matrix to define coverage matrix
- Load test targets multiple endpoints/scenarios → Add Matrix before Siege
- Prerelease covers multiple platforms/environments → Add Matrix before Sentinel
- Approach stuck or single-perspective bias detected → Add Flux for reframing
- Feature ideation yields < 2 options → Add Flux before Spark
- Architecture decision has hidden assumptions → Add Flux before Magi
- Review finds no issues but confidence is low → Add Flux for blind-spot check
- First principles analysis requested or root assumptions questioned → Add Flux at chain start, combine with Matrix for decomposition
- Optimization target unclear or premature → Add Flux before Bolt/Tuner to question "are we optimizing the right thing?"
- Migration involves 3+ technology dimensions → Add Matrix before Shift `detect` for migration path analysis
- Postmortem reveals recurring pattern → Add Flux after Triage for deeper root cause reframing
- API design has 3+ resource types or versioning concerns → Add Matrix before Gateway
- UX design has 3+ user segments or device types → Add Matrix before Vision
- Deployment targets multiple environments/regions → Add Matrix before Guardian
- Content needs A/B testing across segments → Add Matrix before Prose
- Marketing requires multi-dimensional analysis (3+ segments × channels × campaigns) → Add Matrix to the MARKETING chain
- Remediation of known pattern → Replace Scout with Mend
- Ecosystem health check → Add Gauge

> **Matrix / Flux variants are derived, not enumerated.** `<TYPE>|matrix` = `Matrix → <base chain>` and `<TYPE>|first-principles` = `Flux → <base chain>` (optionally with Matrix inserted for decomposition) are generated on demand by applying the Matrix/Flux triggers above to the base chain in `routing-matrix.md`. They are deliberately absent from the variant table — do not re-add them as rows.

### Chain Selection Disambiguation

- Landing page or marketing site → Use DESIGN/landing-page (includes Prose for content-first approach)
- Marketing consulting requested (comprehensive strategy) → Use MARKETING/full (or the default MARKETING chain in `routing-matrix.md` for time-boxed engagements; MARKETING/full embeds Sherpa decomposition because 10-step chains require atomic-step planning)
- Brand strategy or visual identity for a product/company → Use MARKETING/brand (Vision-led, not Compete's personal-brand Recipe)
- Personal/engineer branding (individual portfolio, career, conference visibility) → Use MARKETING/personal-brand (Compete-led, distinct from product brand)
- Persona unclear or target segment ambiguous → Use MARKETING/persona-driven (Field-first to derive persona from qualitative data)
- Customer acquisition cost rising / paid channels saturated → Use MARKETING/acquisition (KPI-first; Pulse defines target CAC/LTV before channel tuning)
- Churn or LTV decline detected → Use MARKETING/retention (includes Trace for session-level churn cause analysis)
- Strategy needs human advisor pressure-testing → Add Magi[advisor] after the initial evidence frame
- Synthetic user voice needed when no real customers exist yet → Add Echo[demand] before Saga (early-stage persona need generation)
- MARKETING vs STRATEGY routing: STRATEGY/{seo,compete,retention,metrics,ab-test} are single-tactic chains (one specialist + Builder + Radar) for engineering-side implementation. MARKETING/* are consulting chains (multi-specialist, narrative-led, often without code output). Use MARKETING when the deliverable is strategy/messaging/plan; use STRATEGY when the deliverable is code/instrumentation.
- MARKETING/content vs CREATIVE/marketing-asset: MARKETING/content includes Saga (narrative)+Pulse (measurement) for content-strategy; CREATIVE/marketing-asset is image+copy asset production only (Growth→Builder→Prose→Artisan). Use the former for content marketing plans, the latter for one-off creative deliverables.
- MARKETING/seo-geo vs STRATEGY/seo: MARKETING/seo-geo adds Prose (copy)+Radar (quality gate) for full content+technical SEO; STRATEGY/seo is the narrow 3-step engineering implementation. Default to MARKETING/seo-geo unless the task is purely meta-tag/JSON-LD code.
- App UI with "clean" or "minimal" requirement → Use DESIGN/app-ui-restrained chain
- Visual direction unclear → Add Forge with moodboard mode before Vision
- Content strategy needed → Add Prose before or after Vision
- Design chain spans 5+ agents with implementation (Muse/Forge/Artisan) → Add Sherpa after Vision/Prose direction phase to decompose into atomic steps before implementation begins

### Rally Parallel Escalation Triggers

- Chain has 2+ independent implementation steps → Escalate to Rally for parallel execution
- Sherpa decomposition produces `parallel_group` → Delegate to Rally via SHERPA_TO_RALLY_HANDOFF
- Feature scope spans 4+ files across 2+ domains (frontend/backend/DB) → Rally with Frontend/Backend Split
- Chain includes both Artisan and Builder implementation → Rally with Frontend/Backend Split
- 3+ independent bug fixes needed → Rally with Feature Parallel
- Implementation + test + docs needed simultaneously → Rally with Code/Test/Docs Triple
- Multi-module refactoring identified → Rally with Feature Parallel after Atlas/Sherpa

### Rally Non-Escalation (Keep Sequential)

- Investigation-only chains (Lens, Scout, Trail) → No Rally
- Advisory-only chains (Magi 1on1/triage/retro/pitch) → No Rally; the advisory Recipe is single-session by contract
- Single-agent chains (Quill, Scribe) → No Rally
- Changes under 10 lines total → No Rally
- High-risk security changes → Prefer sequential with checkpoints
- Each branch needs < 50 lines of code → Nexus _PARALLEL_BRANCHES sufficient

### Skip Triggers

- Changes under 10 lines AND tests exist → May skip Radar
- Pure documentation changes → Skip Radar/Sentinel
- Config files only → Only relevant agent
- Sentinel-only static issues → May skip Probe
- Schema unchanged → May skip Tuner

---

## Rally Parallel Chain Variants

When Rally is activated for parallel execution, standard chains transform into parallel variants.

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| FEATURE/L | Spark → Sherpa → Rally(Forge+Artisan, Builder, Radar) | Frontend/Backend Split |
| FEATURE/M (multi-unit) | Sherpa → Rally(Builder×N, Radar) | Feature Parallel |
| FEATURE/fullstack | Rally(Artisan, Builder, Radar) | Frontend/Backend Split |
| BUG/multiple | Rally(Builder×N) → Radar | Feature Parallel |
| REFACTOR/arch (multi-module) | Atlas → Sherpa → Rally(Zen×N) → Radar | Feature Parallel |
| TEST/coverage | Rally(Radar, Voyager) | Specialist Team |
| SECURITY/full | Rally(Sentinel, Probe) → Builder → Radar | Specialist Team |
| DOCS/full | Rally(Quill, Canvas, Vitrine) | Specialist Team |
| MODERNIZE/stack | Lens → Shift (detect+modernize) → Sherpa → Rally(Builder×N) → Radar | Feature Parallel |
| MOBILE_NATIVE/both | Rally(Native[swiftui], Native[compose]) → Radar → Vitrine | Platform Split (iOS / Android) |
| MOBILE_NATIVE/full | Port[blueprint] → Rally(Native[swiftui], Native[compose]) → Radar → Voyager → Cloak → Launch | Platform Split |

See `rally/reference/integration-patterns.md` for detailed team composition and handoff formats.
