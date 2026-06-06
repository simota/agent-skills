# Nexus Agent Chain Templates Reference

**Purpose:** Chain **variants by complexity / sub-type** (e.g., FEATURE S/M/L/UI/UX, OPTIMIZE app/db) and dynamic add/skip rules.
**Read when:** You need to pick a variant or apply adjustment rules to an in-flight chain.

**Boundary vs `routing-matrix.md`:** That file gives one *default* chain per task type with Recipe Hints (sub-skill commands) and conditional Additions. This file gives the **complexity-keyed variant catalog** and integration patterns (Forge→Builder, Rally parallel). Use them together: routing-matrix picks the task type, this file picks the right variant.

## Contents
- Chain Templates by Task Type (complexity variants)
- Forge → Builder Integration
- Dynamic Chain Adjustment Rules
- Rally Parallel Chain Variants

Complete chain templates and dynamic adjustment rules.

---

## Chain Templates by Task Type

| Type | Complexity | Chain Template |
|------|------------|----------------|
| BUG | simple | Scout → Lens → Builder → Radar |
| BUG | complex | Scout → Lens → Sherpa → Builder → Radar → Sentinel |
| INCIDENT | SEV1/2 | Triage → Scout → Builder → Radar → Triage (postmortem) |
| INCIDENT | SEV3/4 | Triage → Scout → Builder → Radar |
| API | new | Gateway → Builder → Radar → Quill |
| API | change | Gateway → Builder → Radar |
| FEATURE | S | Builder → Radar |
| FEATURE | M | Sherpa → Forge → Builder → Radar |
| FEATURE | L | Spark → Sherpa → Forge → Builder → Radar → Quill |
| FEATURE | UI | Spark → Forge → Muse → Builder → Lens → Radar |
| FEATURE | UX | Field → Echo → Spark → Builder → Radar |
| REFACTOR | small | Zen → Radar |
| REFACTOR | arch | Atlas → Sherpa → Zen → Radar |
| OPTIMIZE | app | Bolt → Radar |
| OPTIMIZE | db | Tuner → Schema → Builder → Radar |
| SECURITY | static | Sentinel → Builder → Radar → Sentinel |
| SECURITY | dynamic | Sentinel → Probe → Builder → Radar → Probe |
| SECURITY | full | Sentinel → Probe → Builder → Radar → Sentinel → Probe |
| INVESTIGATE | feature | Lens |
| INVESTIGATE | flow | Lens → Canvas |
| INVESTIGATE | onboarding | Lens → Scribe |
| INVESTIGATE | pre-impl | Lens → Builder → Radar |
| DOCS | - | Quill |
| INFRA | cloud | Scaffold → Gear → Radar |
| INFRA | local | Scaffold → Radar |
| QA | - | Lens → Echo → Radar |
| QA | e2e | Voyager → Lens → Radar |
| REVIEW | PR | Judge → Builder/Zen/Sentinel (based on findings) → Radar |
| REVIEW | pre-commit | Judge → Builder (if CRITICAL) |
| UX_RESEARCH | - | Field → Echo → Palette |
| DB_DESIGN | new | Schema → Builder → Radar |
| DB_DESIGN | optimize | Schema → Tuner → Builder → Radar |
| E2E | new | Voyager → Lens |
| E2E | ci | Voyager → Gear |
| COMPARE | quality-critical | Sherpa → Arena → Guardian |
| COMPARE | bug-fix | Scout → Arena → Radar |
| COMPARE | feature | Spark → Arena → Guardian |
| COMPARE | security | Arena → Sentinel → Arena (iterate) |
| BROWSER | data-collection | Vector → Builder |
| BROWSER | bug-reproduction | Scout → Vector → Triage |
| BROWSER | evidence | Vector → Lens → Canvas |
| BROWSER | performance | Vector → Bolt |
| DECISION | architecture | Magi → Builder/Zen (based on verdict) |
| DECISION | strategy | Accord → Magi → Spark |
| DECISION | intent | Forge/Builder |
| ANALYSIS | impact | Ripple → Builder → Radar |
| ANALYSIS | standards | Canon → Builder → Radar |
| ANALYSIS | cleanup | Sweep → Zen → Radar |
| DEPLOY | release | Guardian → Launch |
| DEPLOY | full | Radar → Guardian → Launch → Harvest |
| MODERNIZE | stack | Lens → Shift (detect+modernize) → Sherpa → Builder → Radar |
| MODERNIZE | i18n | Polyglot → Artisan → Radar |
| MODERNIZE | structure | Grove → Sherpa → Zen → Radar |
| UX_DESIGN | flow | Flow → Artisan → Radar |
| UX_DESIGN | creative | Vision → Muse → Forge → Artisan → Radar |
| UX_DESIGN | audit | Warden → Palette → Artisan → Radar |
| UX_DESIGN | storybook | Vitrine → Quill |
| UX_DESIGN | demo | Director → Voyager |
| UX_DESIGN | session | Trace → Echo → Palette |
| FEATURE | frontend | Forge → Artisan → Radar |
| FEATURE | cli | Anvil → Radar |
| TEST | quality | Judge → Zen → Radar (iterative PDCA via Nexus) |
| INVESTIGATE | regression | Trail → Scout → Builder → Radar |
| SECURITY | concurrency | Specter → Builder → Radar |
| DOCS | convert | Morph |
| DOCS | report | Harvest → Morph |
| STRATEGY | seo | Growth → Artisan → Radar |
| STRATEGY | compete | Compete → Spark → Builder → Radar |
| STRATEGY | feedback | Voice → Spark → Builder → Radar |
| STRATEGY | metrics | Pulse → Builder → Radar |
| STRATEGY | retention | Bond → Spark → Builder → Radar |
| STRATEGY | ab-test | Experiment → Builder → Radar |
| STRATEGY | data-pipeline | Stream → Schema → Builder → Radar |
| MARKETING | quick | Compete → Growth → Funnel |
| MARKETING | standard | Cast → Compete → Pulse → Saga → Growth → Funnel → Experiment |
| MARKETING | full | Sherpa → Field → Cast → Compete → Pulse → Saga → Growth → Funnel → Experiment → Scribe |
| MARKETING | positioning | Compete → Cast → Magi → Saga → Echo → Scribe |
| MARKETING | gtm | Compete → Cast → Pulse → Saga → Growth → Funnel → Experiment → Launch → Harvest |
| MARKETING | acquisition | Pulse → Compete → Growth → Funnel → Experiment |
| MARKETING | retention | Pulse → Trace → Bond → Voice → Spark → Experiment |
| MARKETING | content | Saga → Prose → Growth → Artisan → Radar → Pulse |
| MARKETING | brand | Vision → Compete → Cast → Saga → Prose → Muse → Growth |
| MARKETING | personal-brand | Crest → Compete → Prose → Growth |
| MARKETING | b2b-saas | Cast → Compete → Saga → Pulse → Growth → Funnel → Experiment |
| MARKETING | seo-geo | Growth → Prose → Artisan → Radar → Pulse |
| MARKETING | analytics | Pulse → Trace → Canvas → Scribe |
| MARKETING | voc | Voice → Echo → Spark → Experiment |
| MARKETING | persona-driven | Field → Cast → Echo → Compete → Saga → Growth |
| MARKETING | reframe | Flux → Compete → Cast → Magi → Saga → Scribe |
| MARKETING | matrix | Matrix → Compete → Magi → Spark → Scribe |
| MARKETING | first-principles | Flux → Cast → Compete → Pulse → Matrix → Scribe |
| QUALITY | quick | Judge → Zen → Radar → Canvas |
| QUALITY | standard | Judge → Zen → Radar → Sentinel → Canvas |
| QUALITY | full | Judge → Zen → Radar → Sentinel → Atlas → Sweep → Canvas |
| OBSERVABILITY | alert-only | Beacon → Gear |
| OBSERVABILITY | slo-design | Beacon → Gear → Builder → Radar |
| OBSERVABILITY | post-incident | Triage → Beacon → Gear → Builder → Radar |
| AI_FEATURE | eval-only | Oracle → Radar |
| AI_FEATURE | rag | Oracle → Gateway → Builder → Radar |
| AI_FEATURE | llm-pipeline | Oracle → Stream → Builder → Radar → Sentinel |
| PRERELEASE | quick | Warden → Guardian |
| PRERELEASE | standard | Warden → Guardian → Launch |
| PRERELEASE | full | Sentinel → Warden → Radar → Guardian → Launch → Harvest |
| REQUIREMENTS | quick | Accord → Scribe |
| REQUIREMENTS | standard | Accord → Scribe → Sherpa |
| REQUIREMENTS | complex | Accord → Magi → Scribe → Sherpa → Canvas |
| DESIGN_SYSTEM | tokens | Vision → Muse → Artisan → Radar |
| DESIGN_SYSTEM | catalog | Vision → Muse → Vitrine → Quill |
| DESIGN_SYSTEM | full | Vision → Muse → Vitrine → Artisan → Quill → Radar |
| CONTENT | microcopy | Prose → Echo → Artisan |
| CONTENT | onboarding | Prose → Echo → Artisan → Radar |
| CONTENT | i18n | Prose → Polyglot → Artisan → Radar |
| UX_RESEARCH | persona-driven | Cast → Field → Echo → Palette |
| UX_RESEARCH | session-replay | Trace → Field → Echo → Palette |
| DEV_EXPERIENCE | dotfiles | Hearth → Gear |
| DEV_EXPERIENCE | full-env | Hearth → Gear → Latch → Anvil |
| DEV_EXPERIENCE | audit | Hearth → Sentinel → Gear |
| LOAD_TEST | quick | Siege → Bolt |
| LOAD_TEST | standard | Siege → Bolt → Builder → Radar |
| LOAD_TEST | chaos | Siege → Bolt → Triage → Builder → Beacon |
| DEMO | cli-demo | Reel → Quill |
| DEMO | ui-demo | Director → Voyager → Vitrine |
| DEMO | full | Director → Reel → Vitrine → Quill |
| SPRINT_RETRO | quick | Harvest |
| SPRINT_RETRO | standard | Harvest → Canvas |
| SPRINT_RETRO | full | Harvest → Canvas → Quill |
| KNOWLEDGE | quick | Scribe → Prism |
| KNOWLEDGE | full | Scribe → Quill → Prism → Morph |
| KNOWLEDGE | research | Field → Scribe → Prism |
| AITUBER | prototype | Cast → Aether → Builder |
| AITUBER | full | Cast → Aether → Builder → Artisan → Scaffold |
| AITUBER | production | Cast → Aether → Builder → Artisan → Scaffold → Beacon → Radar |
| REVIEW | quick-scan | Judge |
| REVIEW | standard | Judge → Builder → Radar |
| REVIEW | deep-dive | Judge → Zen → Builder → Radar → Sentinel |
| DB_DESIGN | with-streaming | Schema → Stream → Builder → Radar |
| SECURITY | red-team | Sentinel → Breach → Builder → Radar |
| SECURITY | purple-team | Breach → Vigil → Builder → Radar → Sentinel |
| SECURITY | detection | Vigil → Gear → Radar |
| SECURITY | detection-full | Sentinel → Vigil → Gear → Radar → Scribe |
| SECURITY | ai-red-team | Oracle → Breach → Builder → Radar → Sentinel |
| SECURITY | threat-model | Stratum → Breach → Scribe |
| GAME | prototype | Quest → Forge → Builder → Radar |
| GAME | full | Quest → Forge → Builder → Tone → Dot → Radar |
| GAME | 3d-asset | Quest → Vision → Clay → Builder → Radar |
| GAME | audio | Quest → Tone → Builder → Radar |
| GAME | narrative | Quest → Saga → Prose → Builder |
| GAME | soundtrack | Quest → Lyric → Tone → Builder |
| GAME | balance | Quest → Matrix → Radar |
| DESIGN | figma-to-code | Frame → Muse → Artisan → Radar |
| DESIGN | figma-make | Vision → Loom → Frame → Artisan → Radar |
| DESIGN | figma-handoff | Frame → Forge → Builder → Radar |
| DESIGN | token-sync | Frame → Muse → Loom → Artisan |
| DESIGN_SYSTEM | figma-driven | Frame → Vision → Muse → Vitrine → Quill |
| DESIGN_SYSTEM_DOCS | quick | Muse → Vitrine → Quill |
| DESIGN_SYSTEM_DOCS | standard | Muse → Vitrine + Canvas → Quill |
| DESIGN_SYSTEM_DOCS | full | Vision → Muse → Vitrine + Canvas → Artisan → Quill |
| DECISION | deadlock | Magi → Flux → Magi → Builder |
| FEATURE | innovation | Field → Flux → Spark → Builder → Radar |
| STRATEGY | reframe | Accord → Flux → Helm → Scribe |
| REFACTOR | rethink | Atlas → Flux → Atlas → Sherpa → Zen → Radar |
| ARCHITECTURE | c4-model | Lens → Stratum → Canvas → Scribe |
| ARCHITECTURE | c4-review | Stratum → Atlas → Scribe |
| ARCHITECTURE | c4-evolution | Ripple → Stratum → Canvas |
| ARCHITECTURE | deployment | Stratum → Scaffold → Gear → Canvas |
| CREATIVE | image-gen | Vision → Sketch → Artisan |
| CREATIVE | image-to-3d | Vision → Sketch → Clay → Builder |
| CREATIVE | marketing-asset | Growth → Sketch → Prose → Artisan |
| STRATEGY | simulation | Helm → Canvas → Scribe |
| STRATEGY | simulation-full | Compete → Helm → Magi → Scribe → Canvas |
| REQUIREMENTS | narrative | Cast → Saga → Accord → Scribe |
| FEATURE | story-driven | Saga → Spark → Forge → Builder → Radar |
| QA | combinatorial | Matrix → Radar → Voyager |
| DEPLOY | matrix | Matrix → Scaffold → Gear → Radar |
| E2E | matrix | Matrix → Voyager → Lens → Radar |
| SPEC_VERIFY | quick | Attest → Scribe |
| SPEC_VERIFY | standard | Attest → Scribe → Radar → Builder |
| SPEC_VERIFY | full | Attest → Scribe → Radar → Builder → Warden |
| LOOP_OPS | simple | Orbit → Builder → Radar |
| LOOP_OPS | full | Orbit → Builder → Guardian → Radar |
| EVOLUTION | quick | Darwin → Canvas |
| EVOLUTION | standard | Darwin → Architect → Void → Canvas |
| EVOLUTION | full | Darwin → Architect → Void → Lore → Canvas |
| KNOWLEDGE_SYNC | - | Lore → Darwin → Architect |
| SKILL_GEN | quick | Sigil → Lens |
| SKILL_GEN | full | Sigil → Lens → Grove → Gauge |
| YAGNI | quick | Void → Sweep |
| YAGNI | standard | Void → Sweep → Zen → Radar |
| YAGNI | full | Void → Magi → Sweep → Zen → Pulse → Radar |
| REMEDIATE | quick | Mend → Radar |
| REMEDIATE | standard | Mend → Radar → Beacon |
| REMEDIATE | full | Triage → Mend → Radar → Beacon → Vigil |
| GHA_WORKFLOW | new | Pipe → Gear → Radar |
| GHA_WORKFLOW | security | Pipe → Sentinel → Vigil → Gear |
| GHA_WORKFLOW | release | Pipe → Guardian → Launch → Harvest |
| PROJECT | init | Titan → Grove → Scaffold → Pipe → Gear |
| PROJECT | full | Titan → Sherpa → Builder → Radar → Guardian → Launch |
| ECOSYSTEM | skill-audit | Gauge → Architect → Darwin |
| ECOSYSTEM | health-check | Darwin → Gauge → Canvas |
| ECOSYSTEM | visualization | Darwin → Realm → Canvas |
| DEV_EXPERIENCE | cli-audit | Hone → Hearth → Gear |
| DEV_EXPERIENCE | cli-full | Hone → Hearth → Latch → Gear → Sentinel |
| BUSINESS | tax-guide | Levy → Scribe |
| BUSINESS | tax-calc | Levy → Builder → Radar |
| BUSINESS | tax-data | Levy → Schema → Builder → Radar |
| PROJECT | onboarding | Lens → Stratum → Canvas → Scribe → Prism |
| INVESTIGATE | architecture | Lens → Stratum → Atlas → Canvas |
| QA | full | Matrix → Lens → Echo → Radar → Voyager |
| QA | coverage | Matrix → Radar → Sentinel |
| TEST | matrix | Matrix → Judge → Zen → Radar |
| TEST | full | Matrix → Judge → Zen → Radar → Sentinel → Canvas |
| E2E | full | Matrix → Voyager → Lens → Radar → Sentinel |
| REVIEW | matrix | Matrix → Judge → Builder → Radar |
| REVIEW | thorough | Matrix → Judge → Zen → Builder → Radar → Sentinel |
| REVIEW | blind-spot | Judge → Flux → Matrix → Builder → Radar |
| COMPARE | matrix | Matrix → Arena → Guardian |
| COMPARE | thorough | Matrix → Sherpa → Arena → Radar → Guardian |
| FEATURE | explore | Spark → Matrix → Magi → Builder → Radar |
| FEATURE | L-matrix | Spark → Matrix → Sherpa → Forge → Builder → Radar → Quill |
| FEATURE | UX-matrix | Field → Echo → Matrix → Spark → Builder → Radar |
| FEATURE | lateral | Spark → Flux → Matrix → Sherpa → Builder → Radar |
| DECISION | multi-axis | Matrix → Magi → Flux → Scribe |
| DECISION | explore | Flux → Matrix → Magi → Builder |
| STRATEGY | innovation | Flux → Compete → Spark → Matrix → Builder → Radar |
| STRATEGY | pivot | Flux → Helm → Magi → Scribe → Canvas |
| LOAD_TEST | matrix | Matrix → Siege → Bolt → Builder → Radar |
| PRERELEASE | matrix | Matrix → Sentinel → Warden → Radar → Guardian → Launch |
| SECURITY | matrix | Matrix → Sentinel → Probe → Builder → Radar |
| AI_FEATURE | explore | Oracle → Flux → Spark → Builder → Radar |
| REFACTOR | lateral | Flux → Atlas → Sherpa → Zen → Radar |
| INVESTIGATE | reframe | Lens → Flux → Canvas → Scribe |
| INVESTIGATE | first-principles | Flux → Lens → Matrix → Canvas |
| ARCHITECTURE | first-principles | Flux → Stratum → Atlas → Scribe |
| REQUIREMENTS | first-principles | Flux → Accord → Matrix → Scribe |
| BUG | first-principles | Flux → Scout → Lens → Builder → Radar |
| REFACTOR | first-principles | Flux → Atlas → Matrix → Sherpa → Zen → Radar |
| SECURITY | first-principles | Flux → Breach → Matrix → Sentinel → Scribe |
| OPTIMIZE | first-principles | Flux → Bolt → Matrix → Builder → Radar |
| OPTIMIZE | db-matrix | Matrix → Tuner → Schema → Builder → Radar |
| MODERNIZE | first-principles | Flux → Lens → Shift (detect+modernize) → Matrix → Sherpa → Builder → Radar |
| MODERNIZE | migration-matrix | Matrix → Shift (detect+modernize) → Sherpa → Builder → Radar |
| DB_DESIGN | first-principles | Flux → Schema → Matrix → Builder → Radar |
| API | matrix | Matrix → Gateway → Builder → Radar → Quill |
| API | first-principles | Flux → Gateway → Matrix → Builder → Radar |
| INCIDENT | postmortem-deep | Triage → Flux → Scout → Matrix → Scribe |
| INCIDENT | prevention | Flux → Matrix → Sentinel → Beacon → Scribe |
| UX_DESIGN | first-principles | Flux → Vision → Muse → Forge → Artisan → Radar |
| UX_DESIGN | variant-matrix | Matrix → Vision → Muse → Artisan → Radar |
| UX_RESEARCH | matrix | Matrix → Field → Echo → Palette |
| YAGNI | first-principles | Flux → Void → Magi → Sweep → Zen → Radar |
| CONTENT | reframe | Flux → Prose → Echo → Artisan → Radar |
| CONTENT | variant | Matrix → Prose → Echo → Artisan → Radar |
| DEPLOY | environment-matrix | Matrix → Guardian → Launch → Harvest |
| INFRA | matrix | Matrix → Scaffold → Gear → Radar |
| OBSERVABILITY | matrix | Matrix → Beacon → Gear → Builder → Radar |
| AI_FEATURE | first-principles | Flux → Oracle → Matrix → Builder → Radar |
| ECOSYSTEM | first-principles | Flux → Darwin → Architect → Void → Canvas |
| MOCKUP | simple | Pixel → Radar |
| MOCKUP | figma | Frame → Pixel → Radar |
| MOCKUP | full | Frame → Pixel → Muse → Artisan → Warden → Radar |
| MOCKUP | responsive | Pixel → Matrix → Artisan → Radar |
| DESIGN_AUDIT | basic | Pixel[gap-report] → Artisan |
| DESIGN_AUDIT | a11y | Pixel[gap-report] → Canon → Artisan |
| DESIGN_AUDIT | review | Pixel[gap-report] → Judge |
| DESIGN_AUDIT | full | Pixel[gap-report] → Canon → Judge → Artisan → Voyager |
| BRANDING | audit | Crest → Quill |
| BRANDING | full | Crest → Growth → Prose → Quill → Canvas |
| BRANDING | portfolio | Crest → Harvest → Quill |
| GAME | design-matrix | Quest → Matrix → Forge → Builder → Radar |
| GAME | first-principles | Flux → Quest → Saga → Matrix → Scribe |
| GHA_WORKFLOW | matrix | Matrix → Pipe → Gear → Radar |
| DESIGN_SYSTEM | matrix | Matrix → Vision → Muse → Vitrine → Artisan → Radar |
| DESIGN | landing-page | Vision → Prose → Sherpa → Muse → Forge → Artisan → Warden → Radar |
| DESIGN | app-ui-restrained | Vision → Sherpa → Muse → Artisan → Flow → Warden → Radar |
| DESIGN | moodboard-first | Forge → Vision → Sherpa → Muse → Artisan → Radar |
| UX_DESIGN | content-first | Prose → Vision → Sherpa → Muse → Forge → Artisan → Warden |
| UX_DESIGN | motion-intentional | Vision → Flow → Artisan → Warden → Radar |
| DESIGN_SYSTEM | composition | Vision → Sherpa → Muse → Artisan → Flow → Warden → Vitrine → Quill |
| STRATEGY | compete-reframe | Flux → Compete → Matrix → Spark → Scribe |
| STRATEGY | ab-matrix | Matrix → Experiment → Builder → Radar |
| SPEC_VERIFY | matrix | Matrix → Attest → Scribe → Radar |
| KNOWLEDGE | first-principles | Flux → Field → Scribe → Prism |
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
| ASSET_IMAGE | catalog | Haul[catalog] → Cloak |
| ASSET_IMAGE | lookup | Haul[lookup] |
| ASSET_IMAGE | refresh | Haul[refresh] |
| ASSET_IMAGE | reverse | Haul[reverse] → Cloak |
| ASSET_IMAGE | brand | Haul[brand] → Cloak |
| ASSET_IMAGE | audit | Haul[audit] |
| ASSET_IMAGE | for-storybook | Haul[catalog] → Cloak → Vitrine |
| ASSET_IMAGE | for-lp | Haul[catalog] → Cloak → Funnel |
| ASSET_IMAGE | for-mockup | Haul[catalog] → Cloak → Pixel |
| ASSET_IMAGE | for-atelier | Haul[catalog] → Cloak → Atelier |
| ASSET_IMAGE | protected-source | Vector → Haul → Cloak |
| ADVISORY | 1on1 | Sage[1on1] |
| ADVISORY | group | Sage[group] |
| ADVISORY | triage | Sage[triage] |
| ADVISORY | retro | Sage[retro] |
| ADVISORY | pitch | Sage[pitch] |
| ADVISORY | advise-then-build | Sage → Sherpa → Builder |
| ADVISORY | advise-then-validate | Sage → Plea |
| ADVISORY | strategy-handoff | Helm → Sage → Sherpa |
| ADVISORY | feature-reality-check | Spark → Sage |
| ADVISORY | research-to-action | Field → Sage → Sherpa → Builder |

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
- Figma design available → Add Frame before Artisan
- Mockup/screenshot to code → Add Pixel (faithful reproduction from image)
- Detailed design-to-code gap analysis / fidelity audit / design review requested → Add Pixel[gap-report]; chain to Canon for WCAG mapping when a11y is in scope, Judge for report quality review, Artisan for remediation
- Personal branding or portfolio → Add Crest
- Game assets needed → Add Tone/Dot/Clay as applicable
- C4 architecture documentation needed → Add Stratum
- Combinatorial testing needed → Add Matrix before Radar
- Feature has 3+ independent dimensions or variants → Add Matrix after Spark
- Review covers 4+ files across 2+ modules → Add Matrix before Judge
- Test coverage gaps identified → Add Matrix to define coverage matrix
- Comparison involves 3+ candidates or criteria → Add Matrix before Arena
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
- Remediation of known pattern → Replace Scout with Mend
- Ecosystem health check → Add Gauge
- Landing page or marketing site → Use DESIGN/landing-page chain (includes Prose for content-first approach)
- Marketing consulting requested (comprehensive strategy) → Use MARKETING/full (or MARKETING/standard for time-boxed engagements; MARKETING/full embeds Sherpa decomposition because 10-step chains require atomic-step planning)
- Go-to-Market plan for new product/feature → Use MARKETING/gtm
- Positioning, messaging, or category-design needed → Use MARKETING/positioning
- Brand strategy or visual identity for a product/company → Use MARKETING/brand (Vision-led, not Crest)
- Personal/engineer branding (individual portfolio, career, conference visibility) → Use MARKETING/personal-brand (Crest-led, distinct from product brand)
- B2B SaaS marketing (long sales cycle, account-based, narrative-heavy) → Use MARKETING/b2b-saas
- Voice of Customer / NPS / review-mining → Use MARKETING/voc
- AI search visibility / LLM citation optimization (GEO) → Use MARKETING/seo-geo
- Marketing analytics / attribution / funnel instrumentation → Use MARKETING/analytics
- Persona unclear or target segment ambiguous → Use MARKETING/persona-driven (Field-first to derive persona from qualitative data)
- Marketing strategy stuck or contrarian reframing needed → Use MARKETING/reframe
- Marketing requires multi-dimensional analysis (3+ segments × channels × campaigns) → Use MARKETING/matrix
- Customer acquisition cost rising / paid channels saturated → Use MARKETING/acquisition (KPI-first; Pulse defines target CAC/LTV before channel tuning)
- Churn or LTV decline detected → Use MARKETING/retention (includes Trace for session-level churn cause analysis)
- Strategy needs human advisor pressure-testing → Add Sage after Magi (advise-then-validate pattern)
- Synthetic user voice needed when no real customers exist yet → Add Plea before Saga (early-stage persona need generation)
- MARKETING vs STRATEGY routing: STRATEGY/{seo,compete,retention,metrics,ab-test} are single-tactic chains (one specialist + Builder + Radar) for engineering-side implementation. MARKETING/* are consulting chains (multi-specialist, narrative-led, often without code output). Use MARKETING when the deliverable is strategy/messaging/plan; use STRATEGY when the deliverable is code/instrumentation.
- MARKETING/content vs CREATIVE/marketing-asset: MARKETING/content includes Saga (narrative)+Pulse (measurement) for content-strategy; CREATIVE/marketing-asset is image+copy asset production only (Growth→Sketch→Prose→Artisan). Use the former for content marketing plans, the latter for one-off creative deliverables.
- MARKETING/seo-geo vs STRATEGY/seo: MARKETING/seo-geo adds Prose (copy)+Radar (quality gate) for full content+technical SEO; STRATEGY/seo is the narrow 3-step engineering implementation. Default to MARKETING/seo-geo unless the task is purely meta-tag/JSON-LD code.
- App UI with "clean" or "minimal" requirement → Use DESIGN/app-ui-restrained chain
- Visual direction unclear → Add Forge with moodboard mode before Vision
- Content strategy needed → Add Prose before or after Vision
- First viewport has cards/stats/metadata → Warden litmus check triggers composition review
- Design chain spans 5+ agents with implementation (Muse/Forge/Artisan) → Add Sherpa after Vision/Prose direction phase to decompose into atomic steps before implementation begins
- Warden FAIL triggers redesign loop → Add Sherpa to re-decompose revised scope before re-entering implementation agents

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
- Advisory-only chains (Sage 1on1/triage/retro/pitch) → No Rally; Sage is single-session by contract
- Single-agent chains (Quill, Morph) → No Rally
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

### FEATURE Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| FEATURE/L | Spark → Sherpa → Rally(Forge+Artisan, Builder, Radar) | Frontend/Backend Split |
| FEATURE/M (multi-unit) | Sherpa → Rally(Builder×N, Radar) | Feature Parallel |
| FEATURE/fullstack | Rally(Artisan, Builder, Radar) | Frontend/Backend Split |

### BUG Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| BUG/multiple | Rally(Builder×N) → Radar | Feature Parallel |

### REFACTOR Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| REFACTOR/arch (multi-module) | Atlas → Sherpa → Rally(Zen×N) → Radar | Feature Parallel |

### TEST Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| TEST/coverage | Rally(Radar, Voyager) | Specialist Team |

### SECURITY Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| SECURITY/full | Rally(Sentinel, Probe) → Builder → Radar | Specialist Team |

### DOCS Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| DOCS/full | Rally(Quill, Canvas, Vitrine) | Specialist Team |

### MODERNIZE Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| MODERNIZE/stack | Lens → Shift (detect+modernize) → Sherpa → Rally(Builder×N) → Radar | Feature Parallel |

### MOBILE_NATIVE Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| MOBILE_NATIVE/both | Rally(Native[swiftui], Native[compose]) → Radar → Vitrine | Platform Split (iOS / Android) |
| MOBILE_NATIVE/full | Port[blueprint] → Rally(Native[swiftui], Native[compose]) → Radar → Voyager → Cloak → Launch | Platform Split |

See `rally/reference/integration-patterns.md` for detailed team composition and handoff formats.
