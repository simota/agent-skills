# Agent Boundaries (Master Reference)

> **Tier:** `spine` — in effect on every run. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

Centralized responsibility boundaries for the entire agent ecosystem. Individual SKILL.md files reference this document instead of maintaining their own Agent Boundaries tables.

For disambiguation of commonly confused agent pairs, see `nexus/reference/agent-disambiguation.md`.

---

## A boundary is a property of the pair

The `description:` line of a SKILL.md is not documentation — it is the routing signal, and it is most of
what the router has to work with. Its negative clause ("Not for X (Sibling)") is therefore load-bearing:
it is the sentence that stops the nearest neighbour absorbing the request.

**A boundary lives between two files, so sharpening it means editing both.** Narrowing `A` without
widening `B` opens a gap that neither description claims; widening `A` without narrowing `B` creates an
overlap both claim, and the router picks by accident. Either way the change reads as correct in the diff,
because the diff shows one file.

Two consequences:

- **Edit descriptions in pairs.** When a `description:` gains, loses, or moves a negative clause, open the
  named sibling in the same change and state where the line now falls from its side. A one-sided edit is
  reported as incomplete, not as a smaller edit.
- **A routing miss between siblings is a description defect, not a router defect.** When `task-battery.md`'s
  over-capture probes route a request to the wrong one of two neighbours, the fix belongs in the two
  descriptions that failed to separate them — retuning the router around them leaves the ambiguity in place
  and moves the failure somewhere the battery is not looking.

The corollary for new skills: a proposed skill whose boundary cannot be stated from *both* sides is not
yet distinct from its neighbour, and `architect`'s overlap check is the place that decides it.

---

## Meta-Orchestration

| Agent | Primary Role | Scope | Writes Code |
|-------|-------------|-------|-------------|
| **Nexus** | Task-chain orchestration and scope-adaptive product delivery | Single chains through full product/MVP delivery | Never |
| **Sherpa** | Task decomposition & workflow guidance | Single epic/story → atomic steps | Never |
| **Rally** | Parallel multi-session execution | Concurrent independent tasks | Never |
| **Darwin** *(project-local)* | Ecosystem self-evolution | This repository's cross-agent system | Never |
| **Sigil** | Project operating-layer design and artifact authoring | Project skills, recipes, workflows, routing maps | SKILL.md/specs only |
| **Architect** | Ecosystem agent design | Permanent agent creation | SKILL.md only |
| **Lore** *(project-local)* | Cross-agent knowledge synthesis | This repository's journal and pattern lifecycle | Never |
| **Gauge** | SKILL.md normalization audit & self-evolution | Per-skill format compliance | Never |
| **Compass** | Ecosystem navigation & onboarding | Which existing skill fits a request | Never |
| **Prune** | Roster cleanup proposals | Overlap and inactivity audit, merge and sunset plans — propose-only | Never |

**Key distinctions:**
- Compass answers *which skill*; Nexus answers *in what order and runs it*. Compass never executes the work it recommends, and Nexus's LADDER spawns Compass before hand-rolling a chain for an unmatched request (`nexus/reference/routing-matrix.md` § LADDER)
- Compass recommends from the **global** roster as it stands; Sigil designs a **project-local** operating layer that does not exist yet. "Nothing here fits" is Compass's Gap mode, which routes to Architect for a global skill or Sigil for a repo-specific one — the split is global-permanent vs project-scoped, not recommend vs design
- Compass reports a gap; Architect closes it. A request Compass cannot match is not Compass's to solve
- Prune proposes removals and never performs them: a merge is executed by Architect, a sunset needs user approval, and target skills are read-only during the audit. Prune measures the roster as it is (overlap, activity, retention score); project-local Darwin judges where the ecosystem should go; Void cuts scope inside product code, not skills. Prune also owns the `HD-ENTROPY` near-duplication sweep one level below the roster — `_common/` protocols and `*/reference/` files (`_common/HARNESS_DEBT.md` §4)
- Nexus `deliver` sizes and executes product-lifecycle chains; Rally parallelizes independent workstreams when needed
- Sherpa decomposes → Nexus/Rally executes the decomposed steps
- Architect creates permanent ecosystem agents; Sigil designs and authors project-specific operating layers
- Project-local Darwin evaluates this repository's ecosystem fitness; project-local Lore curates its cross-agent knowledge patterns. Availability and fallback: `_common/PROJECT_LOCAL_SKILLS.md`.
- Gauge audits existing SKILL.md format compliance; Architect creates/improves agent packages

## Investigation & Analysis

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Scout** | Bug investigation & root cause analysis | "Why is it broken?" | Never |
| **Lens** | Codebase understanding & exploration | "How does it work?" | Never |
| **Trail** | Git history investigation, regression analysis & legacy archaeology | "When did it break?", business rule extraction | Never |
| **Triage** | Incident response & recovery planning | "What's the severity? How to recover?" | Never |
| **Ripple** | Pre-change impact analysis | "What happens if we change X?" | Never |
| **Atlas** | Architecture analysis & ADR creation | "What IS the architecture?" | Never |
| **Sweep** | Dead code & unused file detection | "What can we remove?" | Never |
| **PDM** | Delivery status reconciliation | "What is built vs what was planned?" | Never |

**Key distinctions:**
- Broken behavior → Scout. Understanding behavior → Lens. Git history → Trail
- Delivery status → PDM. It reconciles two sources — documented intent (specs, roadmap, issues) against implemented code — and reports the gap; Lens explains *how* the code works and reads only one side. "Is feature X shipped?" → PDM; "how does feature X work?" → Lens
- PDM reports status and never acts on it: priority scoring → Rank, conformance to a written spec's acceptance criteria → Attest, release notes and delivery metrics from PR history → Launch. PDM composes these specialists rather than duplicating them
- Current architecture → Atlas. Change impact → Ripple
- Incident diagnosis → Triage. Known-pattern auto-fix → Mend. Unknown fix → Builder
- Bug root cause → Scout. Incident severity → Triage
- Legacy system rule extraction → Trail (`static-rules`). Migration execution → Shift

## Security

| Agent | Primary Role | Method | Writes Code |
|-------|-------------|--------|-------------|
| **Sentinel** | Static security analysis | Code scan, CVE check, secret detection | Fixes only |
| **Probe** | Dynamic security testing | OWASP ZAP, penetration testing | Never |
| **Breach** | Red team engineering & threat modeling | STRIDE/PASTA/MITRE ATT&CK, attack simulation | Never |
| **Vigil** | Detection engineering | Sigma/YARA rules, threat hunting, MITRE coverage | Never |
| **Cloak** | Privacy engineering | PII detection, GDPR/CCPA, consent, DPIA | Yes (privacy patterns) |
| **Canon** | Standards, regulatory, and legal-document compliance | OWASP/WCAG/OpenAPI, SOC2/PCI-DSS/HIPAA/ISO 27001, ToS/privacy/Tokushoho review, policy-as-code | Yes (OPA policies) |
| **Crypt** | Cryptographic architecture | Algorithm selection, key management, E2EE, post-quantum | Never |
| **Chain** | Agent supply-chain audit & compromise response | Skill/plugin/MCP manifests, hidden injection, IoC scan, persistence-first eradication | Never |

**Key distinctions:**
- Static code scan → Sentinel. Running app test → Probe
- Attack simulation → Breach. Detection rules → Vigil. Purple team → Breach → Vigil
- PII/privacy implementation → Cloak. Regulatory frameworks and legal-document review → Canon. Crypto design → Crypt
- Chain's object is the **agent's own supply chain** — the skills, plugins, MCP servers, and hooks this environment loads — not the application under development. A vulnerable npm dependency in the product is Sentinel; a skill that exfiltrates on load is Chain. Eradication precedes rotation: rotating credentials while persistence remains re-arms the attacker with fresh secrets

**Credential Isolation Principle** (Source: Anthropic Managed Agents):
Tokens and secrets must never be reachable from the execution environment where agent-generated code runs. Two patterns:
- **Resource-Bundled Auth**: Use credentials during environment setup (e.g., git clone), then remove access before agent code executes
- **Vault + Proxy**: Store credentials in an external vault; agent calls tools via a proxy that injects credentials — the agent itself never handles tokens

## Implementation

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Builder** | Production logic and external API implementation | Business logic, API/data models, vendor image-generation API integration | Yes |
| **Artisan** | Production frontend implementation | React/Vue/Svelte, hooks, state | Yes |
| **Forge** | Rapid prototyping (full-stack) | Speed over quality, PoC | Yes |
| **Schema** | Database and multi-tenant architecture | Data modeling, migrations, tenant isolation/RLS/routing | Yes |
| **Pixel** | Mockup-to-code faithful reproduction | Image→HTML/CSS with visual verification | Yes |

**Key distinctions:**
- Backend logic → Builder. Frontend → Artisan. Prototyping → Forge → then Artisan/Builder
- Clear requirements → Artisan directly. Exploration needed → Forge first
- Image mockup → Pixel. Figma design → Frame → Artisan. Spec → Artisan directly

## Testing & Quality

| Agent | Primary Role | Scope | Writes Code |
|-------|-------------|-------|-------------|
| **Radar** | Unit/integration tests, edge cases, coverage | Test code | Yes |
| **Voyager** | Cross-platform and iOS E2E specialist | Playwright/Cypress/Appium/Detox/Maestro/XCUITest/snapshots | Yes |
| **Siege** | Load testing, chaos engineering, resilience | Non-functional testing | Yes |
| **Judge** | Code review & bug detection | PR review, quality check | Never |
| **Zen** | Refactoring & code smell remediation | Readability improvement | Yes (refactor only) |
| **Attest** | Specification compliance verification | Spec-to-code gap analysis | Never |

**Key distinctions:**
- Find problems → Judge. Fix code smells → Zen
- Unit tests → Radar. E2E tests → Voyager. Load tests → Siege
- Code quality → Judge. Spec compliance → Attest

## Performance

| Agent | Primary Role | Layer | Writes Code |
|-------|-------------|-------|-------------|
| **Bolt** | Application-level performance | Frontend renders, backend N+1, caching | Yes |
| **Tuner** | Database query performance | EXPLAIN ANALYZE, indexes, query rewriting | Yes |

**Key distinctions:**
- App code slow → Bolt. Query slow → Tuner. Bolt may identify DB issues → hands off to Tuner

## Documentation

| Agent | Primary Role | Output Type | Writes Code |
|-------|-------------|------------|-------------|
| **Quill** | Code documentation | JSDoc/TSDoc, README, type definitions | Yes (docs/types) |
| **Scribe** | Specification documents and cross-team packages | PRD/SRS/HLD/test specs; `cross-team` L0-L3 refinement | Never |
| **Canvas** | Visualization | Mermaid diagrams, ASCII art, draw.io | Yes (diagrams) |
| **Saga** | Narrative design & product storytelling | SB7/Pixar/Hero's Journey/JTBD frameworks | Never |
| **Cue** | Video script, storyboard, and demo production | Demo/explainer/tutorial scripts, narration, Playwright-based recordings | Yes |
| **Tome** | Learning and technical-publication generation | Diffs→teaching materials, decision records, note/Zenn/Qiita/dev.to series | Never |
| **Stage** | Presentation slide generation | Marp/reveal.js/Slidev, speaker notes | Yes (slide markdown) |

**Key distinctions:**
- Code docs (JSDoc, README) → Quill. Spec docs (PRD, SRS) → Scribe. Cross-team specs → Scribe `cross-team`. Diagrams → Canvas
- Product narratives/stories → Saga. Video scripts → Cue. Learning docs from code → Tome. Slides → Stage

## Architecture & Structure

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Atlas** | Architecture analysis & decisions | Dependencies, God Class, ADR/RFC | Never |
| **Gateway** | API design & review | OpenAPI, versioning, breaking changes | Yes (specs) |
| **Scaffold** | Infrastructure provisioning | Terraform, Docker, IaC | Yes |
| **Grove** | Human- and LLM-optimized repository structure | Directory layout, conventions, context efficiency, cache topology | Never |
| **Shift** | Migration, upgrade & modernization orchestration | Codemod generation, framework/DB/API migration, deprecated library detection, native API replacement, technology radar (absorbed from horizon) | Yes |
| **Port** | Web→native porting strategy | Feature parity matrices, native architecture maps, phased Strangler-Fig roadmaps | Never |

**Key distinctions:**
- General repo structure → Grove default modes. LLM navigation/cache topology → Grove `llm`
- Port plans a move **across platforms** — a web product to iOS/Android, where the target language and UI paradigm both change and parity must be decided feature by feature. Shift moves within one platform (framework, library, API, database versions). Port produces the roadmap; Native builds against it. A port whose parity matrix is unwritten is where the schedule fails, not the implementation
- Crawl system architecture and single-session scraping execution → Vector
- Crawl output pipeline → Stream. Crawl infrastructure provisioning → Scaffold

## UX & Design

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Vision** | Creative direction & design strategy | Design system, redesign, trends | Never |
| **Muse** | Design token management | Color, spacing, typography tokens | Yes |
| **Palette** | Usability improvement | Cognitive load, a11y, interaction quality | Yes |
| **Flow** | Animation & motion | CSS/JS transitions, micro-interactions | Yes |
| **Echo** | Persona simulation and synthetic demand | UI walkthroughs, feature requests, JTBD, unmet needs | Never |
| **Prose** | UX writing | Microcopy, error messages, voice & tone | Yes (text) |
| **Vitrine** | Storybook catalog management | Component documentation, visual regression | Yes |
| **Trace** | Session replay analysis | Behavioral patterns from logs | Never |
| **Frame** | Figma MCP design context extraction | Figma→code bridge, Code Connect | Never |
| **Ink** | SVG icon & illustration generation | Grid systems, sprite symbols, a11y | Yes (SVG) |
| **Funnel** | Landing-page conversion and premium production | AIDA/PAS, CTA/forms, multi-stage craft and quality gates | Yes |
| **Atelier** | Design-to-implementation pipeline orchestration | Code→visual→code loop, project design system persisted across agents | Never (delegates) |

**Key distinctions:**
- Design direction → Vision. Tokens → Muse. Usability → Palette. Animation → Flow
- Atelier orchestrates the `DESIGN_WORKFLOW` chain (Vision → Muse/Frame → Forge → Artisan → Vitrine → Canvas) and owns the design system that persists between its stages; Vision produces direction and stops there, Forge builds one prototype. Reach for Atelier only when the loop must close — a single prototype or a direction document does not need an orchestrator
- Write text → Prose. Test as persona or synthesize demand → Echo. Research → Field
- Figma data extraction → Frame. Token definition → Muse. Frame extracts, Muse defines
- Code Connect mapping → Frame + Vitrine. Frame manages Figma side, Vitrine manages code side
- SVG icons/illustrations → Ink. Image-generation API implementation → Builder
- Landing page design/conversion → Funnel. SEO/CRO tactics → Growth

## User Research & Personas

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Field** | Research methodology design | Interviews, usability tests, journey maps | Never |
| **Cast** | Persona lifecycle management | Create, store, evolve, sync personas | Never |
| **Echo** | Persona-based UI and demand simulation | Walkthroughs, synthetic requests, JTBD/switch analysis | Never |
| **Voice** | Feedback collection & analysis | NPS, reviews, sentiment analysis | Yes (integrations) |

**Key distinctions:**
- Manage personas → Cast. Simulate UI or user demand → Echo. Design research → Field. Analyze feedback → Voice

## Strategy & Business

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Spark** | Feature ideation & proposal | New feature specs from existing data | Never |
| **Growth** | SEO/SMO/CRO optimization | Search ranking, conversion, sharing | Yes |
| **Compete** | Competitive and personal-brand positioning | SWOT, feature matrix, GitHub/blog/LinkedIn/talk positioning | Never |
| **Experiment** | A/B testing & hypothesis validation | Feature flags, statistical significance | Yes |
| **Pulse** | KPI & metrics infrastructure | Tracking events, dashboards | Yes |
| **Stream** | Data pipeline design | ETL/ELT, Kafka, Airflow, dbt | Yes |
| **Ledger** | Cloud FinOps & cost optimization | IaC cost estimation, right-sizing, RI/SP | Yes (policies) |

**Key distinctions:**
- Competitive intel → Compete. Business simulation and strategic verdicts → Magi. Compete feeds into Magi
- Feature ideas → Spark. Growth tactics → Growth. Metrics → Pulse
- Cloud cost → Ledger. IaC provisioning → Scaffold. Monitoring → Beacon

## Decision & Intent

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Magi** | Multi-perspective decision making and advisory | Logic/Empathy/Pragmatism triad, founder bottleneck coaching, documented named-figure lenses | Never |
| **Flux** | Thinking refraction & perspective shift | Cynefin, TRIZ, lateral thinking, assumption surfacing | Never |

**Key distinctions:**
- "Which option?", founder pressure-testing, or "How would {named figure} think about this?" → Magi. "Are we asking the right question?" → Flux. Flux reframes; Magi advises or decides according to the selected Recipe
- Flux is one-shot reframing that also carries multi-turn facilitation (Expand / Propose / Evaluate / Subtract) absorbed from `riff`; Magi returns a decision. When the output should be a written feature proposal rather than a developed idea, the object belongs to Spark
- Synthetic user personas → Cast. Named-figure mental-model lenses and founder-mentor advisory → Magi

## DevOps & Release

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Gear** | CI/CD maintenance and GitHub Actions design | Dependencies, Docker, build optimization, advanced GHA | Yes |
| **Guardian** | Git/PR governance | Commit strategy, PR quality | Never |
| **Launch** | Release management and PR reporting | Versioning, CHANGELOG, rollback, weekly/monthly git and PR reports | Yes |
| **Hone** | AI CLI config, hooks, and lifecycle automation | config.toml, settings.json, CLAUDE.md, AGENTS.md, GEMINI.md, rules, MCP, permissions, commands, hooks, extensions | Yes (hooks/config) |
| **Mend** | Known-pattern auto-remediation | Runtime fix, runbook execution, staged verification | Yes |

**Key distinctions:**
- Existing provider-agnostic CI maintenance → Gear `ci`. New GHA design → Gear `gha`
- PR strategy → Guardian. Release execution and PR reports → Launch
- Operational config → Gear. Runtime remediation → Mend
- AI CLI config, Claude Code hooks, personal dev environment, dotfiles, and macOS automation → Hone. CLI/TUI implementation → Builder

## Communication & Content

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Polyglot** | Internationalization (i18n/l10n) | Translations, locale formatting, RTL | Yes |

- Messaging-platform integration (chat adapters, bots, webhooks, realtime transports) → Gateway `messaging`, listed under API & Data

## Observability

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Beacon** | SRE & observability | SLO/SLI, tracing, alerting, dashboards | Yes |

## Specialized

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Oracle** | AI/ML design & evaluation | Prompts, RAG, LLM patterns, MLOps | Never |
| **Chisel** | Prompt → executable specification | Ambiguity detection, criterion translation, role decomposition; hub-invoked at Nexus `SPECIFY` to harden an intent contract into a Specified Brief before a chain spawns | Never |
| **Vector** | Browser automation | Playwright task execution | Yes |
| **Orbit** *(project-local)* | Autonomous loop execution | This repository's loop contracts and script generation | Yes |
| **Canon** | Standards and regulatory compliance | OWASP/WCAG/OpenAPI/ISO 25010 plus `regulatory` audit recipes | Policy code only |
| **Matrix** | Combinatorial analysis | Multi-dimensional coverage optimization | Never |
| **Void** | YAGNI verification | Scope cutting, complexity reduction | Never |
| **Omen** | Pre-mortem analysis & failure mode enumeration | FMEA, fault tree, Swiss Cheese, Murphy audit | Never |
| **Seek** | Search & vector DB architecture | Full-text/vector/hybrid search, RAG retrieval | Partial (mappings) |
| **Weave** | Workflow & state machine design | FSM/Statechart, Saga patterns, approval flows | Partial (YAML/specs) |
| **Native** | Mobile development | React Native/Flutter/SwiftUI/Jetpack Compose | Yes |
| **Rank** | Priority quantification | ICE/RICE/WSJF/MoSCoW/Kano scoring | Never |

**Key distinctions:**
- Mobile app development → Native. Mobile-responsive frontend → Artisan
- The grammar a machine parses — regex, a parser, a DSL — is Builder. A contract between services is Gateway, a contract with a database is Schema. The ReDoS axis is Sentinel: a pattern that is correct and catastrophically backtracking passes every other review
- Weave owns *when* work runs and how time is reasoned about — cron expressions, DST and timezone arithmetic, business-calendar rules, and the backoff curve of a retry — alongside the state transitions themselves. It does not own *what* happens on failure at chain level: that is Nexus error handling. Scheduling infrastructure itself (runners, queues) is Gear or Scaffold
- Priority scoring → Rank. Multi-perspective decisions → Magi
- Pre-mortem / failure analysis → Omen. Change impact → Ripple. Incident response → Triage
- Browser/web automation → Vector. macOS native-app automation (Apple Events) → Hone `automate`. iOS app UI automation → Voyager `ios`
- Runtime macOS app scripting + dotfiles/shell/editor config, AI CLI config and hooks → Hone
- A supplied prompt's vague wording → Chisel. The prompt *system* around it (few-shot, schema, versioning, eval, cost) → Oracle. A spec document for people → Scribe. Verifying an artifact against existing criteria → Attest
- Chisel has two callers: **user-invoked** (a supplied prompt is the object) and **hub-invoked** (Nexus `SPECIFY` — the instruction about to be delegated is the object). It never takes the *user's own live request* as the object; that is Nexus `GATE`
