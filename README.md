# AI Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Global Agents](https://img.shields.io/badge/Global_Agents-100-blue.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A skill collection that enables collaborative development with a team of specialized AI agents.

## Features

- **100 Global Agents + 3 Project-local Extensions** - Broad reusable coverage without exposing repository-specific operating skills everywhere
- **Nexus Orchestrator** - Analyzes tasks and automatically designs optimal agent chains
- **Platform Agnostic** - Works with Claude Code, Codex CLI, Antigravity CLI, and others

## Quick Start

### Installation

```bash
# For Claude Code
git clone https://github.com/simota/agent-skills.git ~/.claude/skills

# For other platforms
git clone https://github.com/simota/agent-skills.git /path/to/your/skills
```

### Usage

```
/Nexus I want to implement a login feature
/Scout Investigate the cause of this bug
/Radar Improve test coverage
/Vision I want to redesign the dashboard with a modern look
```

## Overview

This repository contains 100 globally reusable AI agents and 3 repository-local operating extensions. Each skill specializes in a specific domain and is coordinated by the **Nexus** orchestrator when available in the active profile.

## Agent Catalog

> Category-by-category catalog for 100 global agents plus the 3 project-local extensions marked below.

### Orchestration

| Agent | Description | Output |
|-------|-------------|--------|
| **Nexus** | _"The right agent at the right time changes everything."_ - Team orchestrator and scope-adaptive product delivery owner. Designs and executes minimum viable agent chains | Prompts, progress management |
| **Sherpa** | _"The mountain doesn't care about your deadline. Plan accordingly."_ - Task decomposition guide. Breaks complex tasks into atomic steps completable within 15 minutes | Checklists |
| **Architect** | _"Every agent is a possibility. Every SKILL.md is a birth certificate."_ - Meta-designer that creates new skill agents. Ecosystem gap analysis, duplication detection, SKILL.md generation | SKILL.md, references |
| **Rally** | _"One task, many hands. Parallel by design."_ - Multi-session parallel orchestrator. Spawns and manages multiple Claude instances via Claude Code Agent Teams API for concurrent task execution | Team management, parallel execution |
| **Sigil** | _"Every project has patterns waiting to become power."_ - Dynamic skill generator. Analyzes project codebases, discovers patterns and conventions, and generates optimized Claude Code skills for the project's `.claude/skills/` directory | Project-specific skills |
| **Orbit** *(project-local)* | _"Give me a goal. I'll give you a runner that finishes."_ - Nexus-autoloop completion specialist for this repository. Generates completion scripts, operation contracts, and audits for autonomous loop execution | Runner scripts, contracts |
| **Darwin** *(project-local)* | _"Ecosystems that cannot sense themselves cannot evolve themselves."_ - Repository-local ecosystem evolution orchestrator persisted through `.agents/ECOSYSTEM.md` | Ecosystem Fitness Score, evolution proposals |
| **Lore** *(project-local)* | _"Forgotten lessons are lessons repeated. Institutional memory is the compound interest of experience."_ - Repository-local curator that synthesizes `.agents/*.md` into `METAPATTERNS.md` | METAPATTERNS.md, knowledge insights |
| **Gauge** | _"What gets measured gets managed. What gets audited gets normalized."_ - SKILL.md normalization auditor and self-evolving compliance agent. Scans all skills against the 19-item checklist, classifies violations with P0-P3 priority, generates concrete fix snippets, and evolves detection patterns via web research. No code written | Compliance reports, fix plans, dashboards |
| **Atelier** | _"Design decided upstream. Assets produced downstream. atelier is the studio floor in between."_ - Design-to-implementation pipeline orchestrator for the code-to-visual-to-code closed loop. Coordinates Vision → Muse/Frame → Forge → Artisan → Vitrine → Canvas to deliver design extraction, prototypes, visual assets, slides, and production together while persisting a project design system across downstream agents | Design system package, integrated deliverables |
| **Compass** | _"When in doubt, ask Compass. It finds the right skill for the task."_ - Skill ecosystem navigator and onboarding guide. Lists global agents and available project-local extensions, recommends best fit, and helps newcomers discover the right specialist | Recommendations, agent maps |
| **Prune** | _"A garden grows by what you cut, not what you plant."_ - Ecosystem cleanup auditor. Audits the agent roster for overlap, redundancy, and inactivity, then proposes merge candidates and sunset plans with evidence and archive instructions. Propose-only, no execution | Merge/sunset proposals, archive instructions |

### Investigation & Planning (Non-coding)

| Agent | Description | Output |
|-------|-------------|--------|
| **Scout** | _"Every bug has a story. I read the ending first."_ - Bug investigation and root cause analysis (RCA). Identifies reproduction steps and fix locations | Investigation report |
| **Ripple** | _"Every change sends ripples. Know where they land before you leap."_ - Pre-change impact analysis. Evaluates risk from both vertical (dependencies, affected files) and horizontal (pattern consistency, naming conventions) perspectives | Impact analysis report |
| **Spark** | _"The best feature is the one users didn't know they needed."_ - Feature proposals. Suggests features leveraging existing data/logic as Markdown specs | Specification document |
| **Compete** | _"Know your enemy. Know the market. Know yourself."_ - Competitive research, differentiation, positioning, and engineering-professional branding across GitHub, LinkedIn, portfolios, publishing, and conference presence | Competitive analysis, positioning and brand strategy |
| **Voice** | _"Feedback is a gift. Analysis is unwrapping it."_ - User feedback collection, NPS survey design, sentiment analysis, and insight extraction | Feedback report |
| **Field** | _"Good research asks the right questions. Great research changes what you thought was the question."_ - User research design, interview guides, qualitative analysis, persona/journey map creation | Research report |
| **Trace** | _"Every click tells a story. I read between the actions."_ - Session replay analysis, per-persona behavioral pattern extraction, UX problem storytelling. Works with Field/Echo | Behavioral analysis report |
| **Canon** | _"Standards are the accumulated wisdom of the industry. Apply them, don't reinvent them."_ - Standards, regulatory-control, and legal-document review. Evaluates OWASP/WCAG/OpenAPI/ISO 25010, SOC2/PCI-DSS/HIPAA/ISO 27001, ToS, privacy policies, DPA/EULA, cookie consent, and advertising claims | Compliance and legal-review report |
| **Lens** | _"See the code, not just search it."_ - Codebase comprehension specialist. Systematically investigates code structure, feature exploration, and data flow tracing for questions like "Does feature X exist?", "How does flow Y work?", "What is this module's responsibility?" | Investigation report |
| **Magi** | _"Three minds, one verdict. Consensus through diversity."_ - Multi-perspective decisions, founder office hours, bottleneck triage, pitch critique, and advisory lenses grounded in documented notable-figure thinking | Decision and advisory report |
| **Flux** | _"Bend the light. See what was always there."_ - Thinking refraction engine. Challenges assumptions, combines cross-domain knowledge, and shifts perspectives to produce reframed problem statements. Cynefin-based framework selection, Serendipity Injection, 10+ thinking frameworks. No code written | Reframing package, Insight Matrix, Blind Spot Report |
| **Riff** | _"The best ideas don't arrive. They evolve — one riff at a time."_ - Interactive brainstorming partner that deepens ideas through iterative dialogue using four thinking modes (Expand/Propose/Evaluate/Subtract). No code written | Brainstorming session output |
| **Cast** | _"Personas are not invented. They are discovered, born, and evolved."_ - Persona casting agent. Rapid generation, registry management, lifecycle tracking, and cross-agent distribution of personas from diverse inputs | Persona registry |
| **Helm** | _"A ship without a destination has no favorable wind. A ship without a helm has no direction at all."_ - Business strategy simulation agent. Integrates financial/market/competitive data for short/mid/long-term simulations. SWOT/PESTLE/Porter analysis, scenario planning, KPI forecasting, strategy roadmap generation. No code written | Strategy simulation report |
| **Matrix** | _"Infinite combinations, finite resources. Matrix finds the minimum that covers the maximum."_ - Universal multi-dimensional analysis agent. Controls combinatorial explosion from arbitrary axis×value inputs. Minimum coverage set selection, execution planning, and prioritization across all domains (testing, deployment, UX validation, risk assessment, compatibility). No code written | Matrix analysis, coverage optimization plan |
| **Saga** | _"Facts are remembered 5-10% of the time. Stories raise that to 65-70%. The customer is the hero. The product is the guide."_ - Narrative design agent. Structures product and feature use cases as customer-centric stories. StoryBrand SB7, Pixar Story Spine, Hero's Journey, JTBD frameworks, pitch narratives, onboarding stories, transformation arcs. No code written | Narrative document |
| **Omen** | _"Plan for the worst. Build for the best."_ - Pre-mortem analysis and failure mode enumeration. Systematically identifies failure scenarios, scores with RPN/AP. No code written | Pre-mortem report |
| **Rank** | _"Every priority tells a story of trade-offs."_ - Priority quantification. Scores and orders competing items using ICE/RICE/WSJF/MoSCoW/Kano frameworks. No code written | Priority report |
| **PDM** | _"Show where the project stands — planned, built, and the gap between."_ - Project delivery status navigator (PdM-style, read-only). Reconciles planned scope (specs/issues/roadmap/PRD) against implemented code to produce feature inventories, unimplemented-feature lists, roadmap rollups, and WBS views | Feature inventory, gap list, roadmap rollup |

**Scout > Ripple > Builder chain**: Scout (bug investigation) > Ripple (fix impact analysis) > Builder (implementation)
**Ripple > Guardian chain**: Ripple (impact analysis) > Guardian (PR strategy)
**Field > Trace > Echo chain**: Field (persona definition) > Trace (real-data validation) > Echo (simulation confirmation)
**Sentinel > Canon > Builder chain**: Sentinel (vulnerability detection) > Canon (OWASP compliance evaluation) > Builder (fix implementation)
**Gateway > Canon > Gateway chain**: Gateway (API design) > Canon (OpenAPI/RFC compliance check) > Gateway (corrections)
**Echo > Canon > Palette chain**: Echo (UX issues) > Canon (WCAG compliance evaluation) > Palette (accessibility fixes)
**Field > Cast > Echo chain**: Field (research data) > Cast (persona integration) > Echo (UI validation)
**Trace > Cast chain**: Trace (behavioral data) > Cast (persona evolution)

### Git/PR Management

| Agent | Description | Output |
|-------|-------------|--------|
| **Guardian** | _"Every commit tells a story. Make it worth reading."_ - Git/PR gatekeeper. Signal/Noise analysis of changes, commit granularity optimization, branch naming, PR strategy proposals | Analysis report, PR preparation |
| **Launch** | _"Shipping is not the end. It's the beginning of accountability."_ - Release management plus read-only GitHub PR collection, weekly/monthly/client reporting, DORA/SPACE metrics, retrospectives, and PDF export | Release plans, CHANGELOG and delivery reports |
| **Trail** | _"Every bug has a birthday. Every regression has a parent commit. Find them."_ - Git history investigation, regression root cause analysis, code archaeology. Travels back in time to uncover the truth | History investigation report |

**Guardian > Judge > Zen chain**: Guardian (PR preparation) > Judge (review) > Zen (fixes)
**Guardian > Launch chain**: Guardian (change analysis) > Launch (release plan)
**Trail > Scout chain**: Trail (regression identification) > Scout (detailed investigation)

### Quality Assurance

| Agent | Description | Output |
|-------|-------------|--------|
| **Radar** | _"Untested code is unfinished code."_ - Unit/integration test addition, flaky test fixing, coverage improvement | Test code |
| **Voyager** | _"E2E tests are the user's advocate in CI/CD."_ - Cross-platform and iOS E2E specialist. Playwright/Cypress/Appium/Detox/Maestro plus XCUITest and App Store snapshots | E2E test code |
| **Sentinel** | _"Security is not a feature. It's a responsibility."_ - Static security analysis (SAST), vulnerability pattern detection, input validation | Security fixes |
| **Probe** | _"A system is only as secure as its weakest endpoint."_ - Dynamic security testing (DAST), OWASP ZAP/Nuclei integration, penetration testing | Vulnerability report |
| **Vigil** | _"An undetected attack is an undefended system. Vigil ensures nothing passes unseen."_ - Detection Engineering agent. Sigma/YARA rule design, detection coverage mapping (MITRE ATT&CK), threat hunting hypothesis design, Purple Team Blue side execution, Detection-as-Code CI/CD integration | Detection rules, coverage maps |
| **Judge** | _"Good code needs no defense. Bad code has no excuse."_ - Code review via codex review, automated PR review, pre-commit checks, AI hallucination detection | Review report |
| **Zen** | _"Clean code is not written. It's rewritten."_ - Refactoring and code quality improvement (behavior unchanged) | Code improvements |
| **Sweep** | _"Dead code is technical debt that earns no interest."_ - Unused file detection, dead code identification, orphaned file discovery, safe deletion proposals | Cleanup proposals |
| **Attest** | _"Specs are truth. Code is evidence. Attest finds the gaps."_ - Specification compliance verifier. Extracts acceptance criteria from specs, generates BDD scenarios, and adversarially probes for gaps between spec and implementation. Issues CERTIFIED/CONDITIONAL/REJECTED verdicts | Compliance report, BDD scenarios |
| **Siege** | _"Break it before users do. Fix it before they notice."_ - Advanced testing specialist. Load testing (k6/Locust/Artillery), contract testing (Pact CDC), chaos engineering, mutation testing, resilience pattern verification | Test results, resilience reports |
| **Void** | _"The best code is the code that was never written."_ - YAGNI enforcement, scope cutting, complexity reduction proposals. Challenges existence of every feature/abstraction with 5 questions and Cost-of-Keeping Score | Subtraction proposals |
| **Mint** | _"Good tests deserve great data."_ - Test data and fixture generation specialist. Factory patterns, boundary value generation, synthetic data, seed management | Test data, fixtures |
| **Breach** | _"Think like an attacker. Defend like an engineer."_ - Red team engineering. Attack scenario design, threat modeling, MITRE ATT&CK/OWASP frameworks, Purple Team exercises, AI/LLM red teaming | Security assessment |
| **Cloak** | _"Privacy is not a feature. It's a right."_ - Privacy engineering and data governance. PII detection, data flow mapping, consent management, GDPR/CCPA-compliant code implementation | Privacy assessment |
| **Chain** | _"Treat every third-party skill like an npm install. Audit before invoking."_ - Skill/plugin/MCP intake audit plus live npm/PyPI malware investigation. Generates sha256 manifests, scans Unicode and exfiltration patterns, matches campaign IoCs, and produces persistence-first eradication and credential-rotation runbooks | Supply-chain audit, infection report and recovery runbook |

### Implementation

| Agent | Description | Output |
|-------|-------------|--------|
| **Builder** | _"Types are contracts. Code is a promise."_ - Type-safe production implementation plus Gemini image-generation/editing code, prompt design, batch generation, style transfer, post-processing, provenance, and content-policy gates | Production and image-generation code |
| **Artisan** | _"Prototypes promise. Production delivers."_ - Production frontend implementation craftsman. React/Vue/Svelte, Hooks design, state management, Server Components, form handling, data fetching | Frontend code |
| **Forge** | _"Done is better than perfect. Ship it, learn, iterate."_ - Prototyping. Prioritizes working software over perfection. Outputs types.ts, errors.ts, forge-insights.md for Builder handoff | MVP/PoC |
| **Native** | _"Every pixel ships. Every platform matters."_ - Pure-native mobile implementation specialist for iOS (Swift 6.3 + SwiftUI + Liquid Glass) and Android (Kotlin 2.4+ + Jetpack Compose + Material 3 Expressive). Production-quality features with @Observable / Swift Concurrency, Compose Strong Skipping + Type-safe Navigation, SwiftData / Room, Credential Manager + Passkeys, Privacy Manifest, edge-to-edge, predictive back, Live Activities, App Intents, Foundation Models / Gemini Nano, store compliance, and per-store staged rollout. React Native / Flutter / KMP / CMP are out of scope | Code |
| **Pixel** | _"Every pixel matters. Fidelity is non-negotiable."_ - Faithful reproduction agent. Generates pixel-accurate HTML/CSS from image mockups (PNG/JPG/screenshots) and performs visual verification | HTML/CSS code |

### AI/ML

| Agent | Description | Output |
|-------|-------------|--------|
| **Oracle** | _"AI is only as good as its architecture. Design it, measure it, trust nothing."_ - AI/ML design and evaluation specialist. Prompt engineering, RAG architecture, LLM application patterns, safety guardrails, evaluation frameworks, MLOps, cost optimization | Design specs, evaluation reports |
| **Chisel** | _"A vague word is a decision you left to chance. Carve it into something that can be checked."_ - Prompt-to-executable-specification translator. Detects vague quality/quantity/style/design/judgment wording, dissolves persona and title lines into capabilities, reconciles contradictory instructions, and records what was deliberately left open | Ambiguity ledger, specified prompt |

**Oracle > Builder > Radar chain**: Oracle (AI/ML design) > Builder (implementation) > Radar (tests)
**Oracle > Stream > Builder chain**: Oracle (RAG design) > Stream (data pipeline) > Builder (implementation)
**Oracle > Sentinel > Oracle chain**: Oracle (safety design) > Sentinel (security review) > Oracle (refinement)

### Performance

| Agent | Description | Output |
|-------|-------------|--------|
| **Bolt** | _"Speed is a feature. Slowness is a bug you haven't fixed yet."_ - Application performance improvement. Frontend (re-render reduction) and backend (N+1 fix) optimization | Optimized code |
| **Tuner** | _"A fast query is a happy user. A slow query is a lost customer."_ - DB performance optimization. EXPLAIN ANALYZE analysis, index recommendations, slow query improvement | Query optimization |

### Observability/SRE

| Agent | Description | Output |
|-------|-------------|--------|
| **Beacon** | _"You can't fix what you can't see. You can't see what you don't measure."_ - Observability and reliability engineering specialist. SLO/SLI design, distributed tracing, alerting strategy, dashboard design, capacity planning, toil automation | SLO definitions, observability specs |

**Beacon > Gear > Builder chain**: Beacon (observability design) > Gear (monitoring implementation) > Builder (instrumentation)
**Triage > Beacon > Gear chain**: Triage (incident postmortem) > Beacon (monitoring improvements) > Gear (implementation)

### UI/UX

| Agent | Description | Output |
|-------|-------------|--------|
| **Vision** | _"Design is not how it looks. Design is how it feels."_ - Creative direction. Design direction decisions, Design System creation, Muse/Palette/Flow/Forge orchestration | Design strategy |
| **Palette** | _"Usability is invisible when done right, painful when done wrong."_ - Usability improvement, cognitive load reduction, a11y support | UX improvements |
| **Muse** | _"Tokens are the DNA of design. Mutate them with care."_ - Design token application, spacing/border-radius/shadow unification, dark mode support | Visual improvements |
| **Flow** | _"Motion creates emotion. Animation breathes life."_ - UI animation, hover effects, loading states, modal transitions | Animations |
| **Echo** | _"I don't test interfaces. I feel what users feel."_ - Persona validation and synthetic demand. Reports UI confusion, feature requests, JTBD, and unmet needs | UX report |
| **Vitrine** | _"Components without stories are components without context."_ - Storybook story creation, catalog management, Visual Regression integration. CSF 3.0 format | Storybook Stories |
| **Prose** | _"Words are the smallest unit of design. Get them wrong, and nothing else matters."_ - User-facing text specialist. Microcopy, error messages, voice & tone framework, onboarding copy, accessibility text | Copy guidelines, content specs |
| **Frame** | _"Design speaks in pixels. I translate it to code."_ - Figma MCP Server bridge agent. Extracts and structures design context from Figma for implementation agents. Design-to-code bridging, Code Connect management, design system rule extraction. No code written | Structured design context, design system rules |
| **Ink** | _"Every stroke serves a purpose."_ - SVG icon/illustration generation, icon system design, and sprite symbol construction | SVG assets |

### Documentation

| Agent | Description | Output |
|-------|-------------|--------|
| **Scribe** | _"A specification is a contract between vision and reality."_ - Specification author for PRD/SRS/HLD/LLD and cross-team L0-L3 packages, including implementation checklists and test specifications | Specs, design docs |
| **Quill** | _"Code tells computers what to do. Documentation tells humans why."_ - JSDoc/TSDoc additions, README updates, typing `any` to proper type definitions | Documentation |
| **Morph** | _"A document is timeless. Its format is temporary."_ - Document format conversion (Markdown <> Word/Excel/PDF/HTML). Converts Scribe specs and Launch reports to various formats | Converted documents |
| **Tome** | _"Changes are forgotten. Knowledge endures."_ - Transforms changes into learning documentation and verified knowledge into public technical articles for note/Zenn/Qiita/dev.to, including article series and repurposing | Learning docs and technical articles |

**Scribe vs Quill vs Morph vs Tome responsibilities**:
- **Scribe**: Project documentation (PRD, SRS, design docs, checklists, test specifications)
- **Quill**: Code documentation (JSDoc/TSDoc, README, type definitions)
- **Morph**: Format conversion (Markdown > PDF/Word/HTML, etc.)
- **Tome**: Change-based learning materials and external-facing articles for note/Zenn/Qiita/dev.to, including series management

### Visualization

| Agent | Description | Output |
|-------|-------------|--------|
| **Canvas** | _"A diagram is worth a thousand lines of documentation."_ - Design visualization. Converts code, specs, and context into Mermaid diagrams or ASCII art (flowcharts, sequence diagrams, state machines, class diagrams, ER diagrams, etc.) | Mermaid diagrams / ASCII Art |
| **Cue** | _"Every frame tells a story."_ - Video scripts, storyboards, narration, and Playwright feature-demo production with multi-aspect recording, captions, quality gates, voiceover, transcript, and thumbnails | Video plans, demos and publication assets |
| **Stage** | _"Every slide is a stage."_ - Marp/reveal.js/Slidev slide generation, story composition design, conference talk optimization | Slide decks |


### Architecture

| Agent | Description | Output |
|-------|-------------|--------|
| **Atlas** | _"Dependencies are destiny. Map them before they map you."_ - Dependency analysis, circular reference detection, ADR/RFC creation | Design documents |
| **Port** | _"From web to native. Translate the experience, not just the code."_ - Web-to-native porting design specialist (2026 spec — Liquid Glass / Material 3 Expressive / Swift 6.3 / targetSdk 36 / Privacy Manifest / 5.1.2(i) AI disclosure aware). Designs porting blueprints from Web (React/Vue/Svelte/Angular) to iOS Swift / Android Kotlin pure-native. Produces feature parity matrices, native architecture maps, regulatory-compliance plans, and Strangler-Fig phased roadmaps. Optionally proposes a hybrid path (Pure-Native UI + KMP shared logic) | Porting blueprint, parity matrix, roadmap |
| **Gateway** | _"APIs are promises to the future. Design them like contracts."_ - API design, review, OpenAPI spec generation, versioning strategy, breaking change detection | API specifications |
| **Grove** | _"A well-structured repository is a well-structured mind."_ - Human- and LLM-optimized repository structure design, including context efficiency, prompt-cache topology, and sharding | Structure design, audit reports |
| **Weave** | _"Every state tells a story. Every transition is a contract."_ - Workflow and state machine design specialist. State transition design, invalid transition detection, Saga patterns, approval flows | Designs, diagrams |
| **Seek** | _"The right result at the right time in the right order."_ - Search engine and vector DB design specialist. Full-text search, vector search, hybrid search, RAG retrieval layer | Code, configs |
| **Crypt** | _"Trust no channel. Verify every key."_ - Cryptographic architecture design: algorithm selection, key management, E2E encryption, KMS integration, TLS configuration | Crypto design specs |
| **Trawl** | _"Design the web that catches the web."_ - Crawl system architecture design. Distributed crawler design, URL frontier management, politeness policies, legal compliance | Architecture specs |
| **Tempo** | _"Time is not a scalar — it's a minefield of conventions."_ - Scheduling and time-aware logic architect. Cron expression design, timezone/DST handling, retry/backoff policies, idempotency keys, backfill strategies, and business-calendar design (JP holidays, fiscal year, banking days) | Schedule specs, cron configs, retry policies |
| **Grok** | _"Understand the shape before writing the parser."_ - Pattern, regex, parser, and DSL design specialist. Grammar authoring (EBNF/PEG), ReDoS-safe regex, parser-generator selection (ANTLR4/tree-sitter/Chevrotain), internal DSL architecture, AST transformation | Grammar specs, parser designs, DSL specs |

### Communication

| Agent | Description | Output |
|-------|-------------|--------|
| **Relay** | _"Every message finds its way. Every channel speaks the same language."_ - Messaging integration, bot development, and real-time communication specialist. Channel adapters, webhook handlers, WebSocket servers, event-driven architecture | Channel adapters, message handlers, bot framework |

**Relay > Builder > Radar chain**: Relay (messaging design) > Builder (implementation) > Radar (tests)
**Gateway > Relay chain**: Gateway (webhook API spec) > Relay (handler design)

### Data

| Agent | Description | Output |
|-------|-------------|--------|
| **Schema** | _"A schema is a contract with the future."_ - DB schema, migration, ER diagram, and multi-tenant isolation/RLS/routing design | Migrations / schema definitions |
| **Stream** | _"Data flows like water. My job is to build the pipes."_ - Data pipelines. ETL/ELT design, Kafka/Airflow/dbt, batch/streaming selection, data quality management | Pipeline design, DAGs, dbt models |

**Schema > Stream chain**: Schema (data model) > Stream (pipeline design)

### DevOps

| Agent | Description | Output |
|-------|-------------|--------|
| **Anvil** | _"The terminal is the first interface. Make it unforgettable."_ - CLI/TUI and dev-tool implementation plus personal shell/editor/terminal/dotfile setup and safe macOS automation with AppleScript/JXA | CLI/TUI code and environment configuration |
| **Gear** | _"The best CI/CD is the one nobody thinks about."_ - Dependency management, CI/CD and Docker optimization, plus advanced GitHub Actions workflow design | Configuration files |
| **Scaffold** | _"Infrastructure is the silent foundation of every dream."_ - Cloud infrastructure (Terraform/CloudFormation/Pulumi), local dev environments (Docker Compose), IaC design | Infrastructure config |
| **Hone** | _"A sharp blade cuts clean. A sharp config cuts friction."_ - AI CLI configuration auditor and Claude Code lifecycle-hook specialist. Audits Codex/Antigravity/Claude configuration and designs, configures, or debugs scoped hooks with verification | Audit reports, proposals and hook configurations |
| **Ledger** | _"Every dollar has a story. Make it a short one."_ - FinOps and cloud cost optimization. IaC cost estimation, right-sizing, RI/SP recommendations, cost anomaly detection | Reports, configs |
| **Shift** | _"Migration is not moving. It's transforming."_ - Migration and upgrade orchestrator. Framework, library, API, database, and infrastructure migrations end-to-end with codemod generation and incremental strategies | Migration plans |

**Anvil vs Hone vs Gear vs Scaffold responsibilities**:
- **Anvil**: Personal environment (dotfiles, shell, editor, terminal)
- **Hone**: AI CLI configuration audit and Claude Code event-hook design/configuration/debugging
- **Gear**: Project-level DevOps (CI/CD, Docker, monitoring, Git hooks); `gha` mode owns advanced GitHub Actions
- **Scaffold**: Infrastructure provisioning (cloud, Docker Compose, IaC)

### Internationalization

| Agent | Description | Output |
|-------|-------------|--------|
| **Polyglot** | _"Every language deserves respect. Every user deserves their mother tongue."_ - i18n support. Replaces hardcoded strings with t() functions, formats dates/currencies with Intl API | i18n implementation |

### Growth

| Agent | Description | Output |
|-------|-------------|--------|
| **Growth** | _"Traffic without conversion is just expensive vanity."_ - SEO (meta/OGP/JSON-LD), SMO (social share display), CRO (CTA improvement) | Growth initiatives |
| **Bond** | _"Acquisition is expensive. Retention is profitable."_ - Retention strategies, re-engagement, churn prevention. Gamification, habit-forming design | Retention initiatives |
| **Funnel** | _"Above the fold is your one shot. Make every pixel convert."_ - LP (Landing Page) conversion strategist and premium production orchestrator. Framework-based structure design (AIDA/PAS/BAB/4Ps), hero section craft, CTA placement strategy, social proof hierarchy, mobile-first responsive implementation | LP structure, copy, specs |

### Analytics

| Agent | Description | Output |
|-------|-------------|--------|
| **Pulse** | _"What gets measured gets managed. What gets measured wrong gets destroyed."_ - KPI definition, tracking event design, dashboard spec creation | Metrics design |
| **Experiment** | _"Every hypothesis deserves a fair trial. Every decision deserves data."_ - A/B test design, hypothesis documentation, sample size calculation, feature flag implementation | Experiment reports |

### Operations

| Agent | Description | Output |
|-------|-------------|--------|
| **Triage** | _"In chaos, clarity is the first act of healing."_ - Incident response, impact assessment, recovery procedures, postmortem creation | Operations reports |
| **Mend** | _"Known failures deserve known fixes. Speed of recovery defines reliability."_ - Auto-repair agent for known failure patterns. Receives Triage diagnostics and Beacon alerts, executes runbooks based on safety tier classification, performs staged verification, and manages rollback | Repair results, verification reports |

**Triage > Mend > Beacon chain**: Triage (diagnosis) > Mend (auto-repair) > Beacon (monitoring recovery)

### Browser Automation

| Agent | Description | Output |
|-------|-------------|--------|
| **Vector** | _"The browser is a stage. Every click is a scene."_ - Browser automation via Playwright/Chrome DevTools. Data collection, form interaction, screenshots, network monitoring | Automation scripts |

**Cue vs Vitrine responsibilities**:
- **Cue**: Browser (Web UI) demo videos (Playwright, .webm output)

## Workflows

### Basic Usage

1. Invoke an agent with `/AgentName`
2. The agent executes the task
3. Suggests handoff to other agents as needed

### Orchestration with Nexus

Use **Nexus** for complex tasks. Nexus operates in the following modes:

| Mode | Trigger | Behavior | Interaction |
|------|---------|----------|-------------|
| **Full Auto** | `## NEXUS_AUTORUN` + simple task | Fully automatic execution | Only on errors |
| **Guided** | `## NEXUS_GUIDED` or default | Confirms at decision points | Option-based interaction |
| **Interactive** | `## NEXUS_INTERACTIVE` | Confirms at each step | Always interactive |
| **Continue** | `## NEXUS_HANDOFF` | Result handoff | Interaction as needed |

### Interactive Execution (Guided/Interactive)

Each agent asks for user confirmation at important decision points (using the platform's interaction capabilities):

- **Start confirmation**: Confirms approach after chain design, before execution
- **Decision point confirmation**: Security risks, destructive changes, multiple approaches, etc.
- **Questions as options**: Choose from 2-4 options ("Other" is always available)

```yaml
# Example option-based question
questions:
  - question: "A potential security vulnerability was found. How would you like to proceed?"
    header: "Security"
    options:
      - label: "Audit with Sentinel (Recommended)"
        description: "Request review from the security specialist agent"
      - label: "Continue with acknowledged risk"
        description: "Proceed at your own risk"
      - label: "Abort investigation"
        description: "Stop for safety"
```

### Automatic Mode Selection by Complexity

| Indicator | SIMPLE | COMPLEX |
|-----------|--------|---------|
| Estimated steps | 1-2 | 3+ |
| Affected files | 1-3 | 4+ |
| Security-related | No | Yes |
| Destructive changes | No | Yes |

- **SIMPLE + NEXUS_AUTORUN**: Fully automatic execution
- **COMPLEX**: Automatically switches to Guided mode (interaction required)

See `_common/INTERACTION.md` for details.

### Chain Templates by Task Type

#### Investigation & Understanding

| Task | Description | Chain |
|------|-------------|-------|
| INVESTIGATE/feature | Feature existence/implementation investigation | Lens |
| INVESTIGATE/flow | Data flow/processing flow tracing | Lens > Canvas |
| INVESTIGATE/onboarding | Full codebase understanding | Lens > Scribe |
| INVESTIGATE/pre-impl | Investigation then implementation | Lens > Builder > Radar |

> **Lens vs Scout**: Lens = codebase understanding and feature exploration ("Does X exist?", "How does Y flow?"), Scout = bug investigation and root cause analysis ("Why did it break?")

#### Bug Fixes

| Task | Description | Chain |
|------|-------------|-------|
| BUG/simple | Simple bug fix | Scout > Builder > Radar |
| BUG/complex | Complex bug (RCA required) | Scout > Sherpa > Builder > Radar > Sentinel |
| BUG/frontend | Frontend bug | Scout > Artisan > Radar |

#### Feature Development

| Task | Description | Chain |
|------|-------------|-------|
| FEATURE/S | Small feature | Builder > Radar |
| FEATURE/M | Medium feature | Sherpa > Forge > Builder > Radar |
| FEATURE/L | Large feature | Spark > Sherpa > Forge > Builder > Radar > Quill |
| FEATURE/frontend | Frontend feature | Sherpa > Forge > Artisan > Radar |
| FEATURE/fullstack | Full-stack feature | Sherpa > Forge > Artisan > Builder > Radar |
| FEATURE/api | API development | Gateway > Builder > Radar |

#### UI/UX

| Task | Description | Chain |
|------|-------------|-------|
| UI/new | New UI implementation | Vision > Forge > Vitrine > Muse > Artisan > Radar |
| UI/redesign | UI redesign | Vision > Muse > Palette > Flow > Artisan > Radar |
| UI/component | Component creation | Forge > Vitrine > Muse > Artisan > Radar |
| UI/animation | Animation addition | Flow > Artisan > Radar |
| UX/research | UX research | Field > Echo > Palette |
| UX/improve | UX improvement | Echo > Palette > Artisan > Radar |
| UX/session-analysis | Session analysis | Trace > Echo > Palette |
| UX/persona-validation | Persona validation | Field > Trace > Echo |

#### Refactoring

| Task | Description | Chain |
|------|-------------|-------|
| REFACTOR/small | Small refactor | Zen > Radar |
| REFACTOR/arch | Architecture improvement | Atlas > Sherpa > Zen > Radar |
| REFACTOR/legacy | Legacy modernization | Shift (detect) > Sherpa > Zen > Radar |

#### Performance

| Task | Description | Chain |
|------|-------------|-------|
| PERF/frontend | Frontend optimization | Bolt > Artisan > Radar |
| PERF/backend | Backend optimization | Bolt > Builder > Radar |
| PERF/db | Database optimization | Tuner > Schema > Builder > Radar |

#### AI/ML

| Task | Description | Chain |
|------|-------------|-------|
| AI/rag | RAG pipeline design | Oracle > Stream > Builder > Radar |
| AI/llm-app | LLM application design | Oracle > Builder > Radar |
| AI/safety | AI safety review | Oracle > Sentinel > Oracle |
| AI/prompt-ops | Prompt engineering & evaluation | Oracle > Radar |
| AI/prompt-spec | Turning a vague prompt into an executable spec | Chisel |

#### Observability/SRE

| Task | Description | Chain |
|------|-------------|-------|
| SRE/slo | SLO definition & monitoring | Beacon > Gear > Builder |
| SRE/observability | Full observability setup | Beacon > Gear > Builder > Radar |

#### Security

| Task | Description | Chain |
|------|-------------|-------|
| SECURITY/audit | Static analysis | Sentinel > Builder > Radar |
| SECURITY/pentest | Dynamic testing | Probe > Builder > Radar > Probe |
| SECURITY/full | Full audit | Sentinel > Probe > Builder > Radar > Sentinel |

#### Testing

| Task | Description | Chain |
|------|-------------|-------|
| TEST/unit | Unit test addition | Radar |
| TEST/e2e | E2E test addition | Voyager |
| TEST/coverage | Coverage improvement | Radar > Voyager |
| TEST/load | Load testing | Siege > Bolt |
| TEST/chaos | Chaos engineering | Siege > Triage > Builder |
| TEST/contract | Contract testing | Gateway > Siege > Radar |
| TEST/mutation | Mutation testing | Siege > Radar |

#### Review

| Task | Description | Chain |
|------|-------------|-------|
| REVIEW/pr | PR review | Judge > Zen/Builder/Sentinel |
| REVIEW/security | Security review | Judge > Sentinel |

#### Git/PR

| Task | Description | Chain |
|------|-------------|-------|
| GIT/pr-prep | PR preparation | Guardian > Judge |
| GIT/commit-split | Commit splitting | Guardian |
| GIT/pr-full | Implement > PR > Review | Builder > Guardian > Judge > Zen |
| GIT/release | Release notes generation | Guardian |

#### Decision Making

| Task | Description | Chain |
|------|-------------|-------|
| DECISION/arch | Architecture selection | Magi > Builder/Zen |
| DECISION/strategy | Strategic decisions | Magi > Spark |
| DECISION/office-hours | Founder office hours advisory | Magi > Builder/Echo[demand]/Sherpa |
| DECISION/retro | Postmortem on a recent decision/outcome | Magi |

#### Analysis

| Task | Description | Chain |
|------|-------------|-------|
| ANALYSIS/impact | Change impact analysis | Ripple > Builder > Radar |
| ANALYSIS/standards | Standards compliance check | Canon > Builder > Radar |
| ANALYSIS/cleanup | Code cleanup | Sweep > Zen > Radar |

#### Subtraction & Culture

| Task | Description | Chain |
|------|-------------|-------|
| SUBTRACT/feature-gate | Feature proposal subtraction gate | Spark > Void > Magi |
| SUBTRACT/scope-check | Scope validation | Sherpa > Void > Sherpa |
| SUBTRACT/arch-simplify | Architecture over-engineering detection | Atlas > Void > Zen |

#### Documentation

| Task | Description | Chain |
|------|-------------|-------|
| DOCS/prd | PRD creation | Scribe |
| DOCS/srs | SRS creation | Scribe |
| DOCS/design | Design document creation | Scribe |
| DOCS/spec-to-build | Spec to implementation | Spark > Scribe > Sherpa > Builder |
| DOCS/code | Code documentation | Quill |
| DOCS/component | Component documentation | Vitrine > Quill |
| DOCS/architecture | Architecture diagrams | Canvas |
| DOCS/convert | Format conversion | Morph |
| DOCS/report | PR report | Launch > Morph |
| DOCS/learning | Change-based learning doc | Tome |
| DOCS/onboarding | Onboarding material from changes | Trail > Tome |

#### Demo & Recording

| Task | Description | Chain |
|------|-------------|-------|
| DEMO/prototype | Prototype demo | Forge > Cue > Growth |

#### Infrastructure & DevOps

| Task | Description | Chain |
|------|-------------|-------|
| INFRA/ci | CI/CD setup | Gear > Radar |
| INFRA/cloud | Cloud setup | Scaffold > Gear |
| INFRA/cli | CLI development | Anvil > Radar |

#### Deploy & Release

| Task | Description | Chain |
|------|-------------|-------|
| DEPLOY/release | Release execution | Guardian > Launch |
| DEPLOY/full | Full pipeline | Radar > Guardian > Launch |

#### Modernization

| Task | Description | Chain |
|------|-------------|-------|
| MODERNIZE/stack | Tech stack refresh | Lens > Shift (detect+modernize) > Sherpa > Builder > Radar |
| MODERNIZE/i18n | Internationalization | Polyglot > Artisan > Radar |
| MODERNIZE/structure | Repository structure improvement | Grove > Sherpa > Zen > Radar |

#### Strategy & Growth

| Task | Description | Chain |
|------|-------------|-------|
| STRATEGY/seo | SEO improvement | Growth > Artisan > Radar |
| STRATEGY/compete | Competitive analysis to implementation | Compete > Spark > Builder > Radar |
| STRATEGY/feedback | Feedback integration | Voice > Spark > Builder > Radar |
| STRATEGY/metrics | Metrics infrastructure | Pulse > Builder > Radar |
| STRATEGY/retention | Retention initiatives | Bond > Spark > Builder > Radar |
| STRATEGY/ab-test | A/B test design | Experiment > Builder > Radar |
| STRATEGY/data | Data pipeline | Stream > Schema > Builder > Radar |

#### Game Development

| Task | Description | Chain |
|------|-------------|-------|

#### Parallel Execution (Rally Integration)

For large-scale tasks where parallel execution is beneficial, Nexus escalates to Rally.

| Task | Description | Parallel Chain |
|------|-------------|---------------|
| FEATURE/L (parallel) | Large-scale full-stack | Sherpa > Rally(Artisan + Builder + Radar) |
| FEATURE/fullstack (parallel) | Frontend + Backend | Rally(Artisan, Builder, Radar) |
| FEATURE/multi (parallel) | Multiple independent features | Sherpa > Rally(Builder x N, Radar) |
| BUG/multiple (parallel) | Multiple independent bug fixes | Rally(Builder x N) > Radar |
| REFACTOR/arch (parallel) | Multi-module refactoring | Atlas > Sherpa > Rally(Zen x N) > Radar |
| SECURITY/full (parallel) | Static + dynamic parallel scan | Rally(Sentinel, Probe) > Builder > Radar |
| TEST/coverage (parallel) | Unit + E2E parallel testing | Rally(Radar, Voyager) |
| MODERNIZE/stack (parallel) | Multi-area modernization | Shift (detect+modernize) > Sherpa > Rally(Builder x N) > Radar |
| DOCS/full (parallel) | Code docs + diagrams + stories | Rally(Quill, Canvas, Vitrine) |

> **Rally Escalation Criteria**: Rally is triggered when there are 2+ independent implementation steps, changes span 4+ files across 2+ domains, or Sherpa detects a `parallel_group`.

> **Nexus parallel vs Rally**: Nexus's built-in `_PARALLEL_BRANCHES` is for lightweight parallelism (each branch < 50 lines). Rally's multi-session parallelism is used for substantial implementation work.

#### Product Lifecycle (`Nexus deliver`)

| Task | Description | Chain |
|------|-------------|-------|
| PROJECT/full | Full product from ambiguous goal | `Nexus deliver` (scope-adaptive lifecycle) |
| PROJECT/mvp | MVP-focused delivery | `Nexus deliver` (minimum viable specialist chain) |

> **Nexus build modes**: `feature` handles one bounded capability, `deliver` sizes a product/MVP chain to scope, and `apex` runs a high-investment discovery-to-ship workflow.

#### Other

| Task | Description | Chain |
|------|-------------|-------|
| INCIDENT | Incident response | Triage > Scout > Builder |
| TEST/quality | Iterative quality improvement | Judge > Zen > Radar |
| INVESTIGATE/regression | Regression investigation | Trail > Scout > Builder > Radar |

#### Messaging & Real-time

| Task | Description | Chain |
|------|-------------|-------|
| MESSAGING/bot | Bot development | Relay > Builder > Radar |
| MESSAGING/webhook | Webhook handler | Gateway > Relay > Builder > Radar |
| MESSAGING/realtime | Real-time communication | Relay > Scaffold > Builder > Radar |
| MESSAGING/multi-channel | Multi-channel integration | Relay > Builder > Radar |

## Shared Knowledge

Agents share knowledge through the `.agents/` directory:

| File | Purpose | When to Update |
|------|---------|---------------|
| `PROJECT.md` | Shared knowledge + activity log | **Required for all agents after completing work** |
| `{agent}.md` | Agent-specific learnings | When domain-specific discoveries are made |

### PROJECT.md Structure

- **Architecture Decisions** - Record of architecture choices
- **Domain Glossary** - Unified terminology
- **API & External Services** - External service constraints
- **Known Gotchas** - Known pitfalls
- **Security Considerations** - Security constraints
- **Performance Budgets** - Performance targets
- **Activity Log** - Agent work history

## Agent Principles

All agents follow these principles:

### Common Rules

- **Changes under 50 lines** - Aim for small, safe changes
- **Respect existing patterns** - Follow project conventions
- **Run tests** - Run tests before and after changes
- **Journal only significant learnings** - Don't record routine work

### Boundary Types

| Marker | Meaning |
|--------|---------|
| Always do | Must always be done |
| Ask first | Requires confirmation |
| Never do | Must never be done |

## Directory Structure

```
skills/
├── _common/
│   └── INTERACTION.md  # Shared interaction rules
├── _templates/
│   └── PROJECT.md      # Project knowledge template
├── architect/SKILL.md  # Agent design meta-designer
├── anvil/SKILL.md      # CLI/TUI construction
├── artisan/SKILL.md    # Frontend implementation
├── atelier/SKILL.md    # Design-to-implementation pipeline orchestrator
├── atlas/SKILL.md      # Architecture
├── attest/SKILL.md     # Specification compliance verification
├── beacon/SKILL.md     # Observability/SRE
├── bolt/SKILL.md       # Performance
├── builder/SKILL.md    # Production implementation
├── canon/SKILL.md      # Standards compliance (OWASP/WCAG/OpenAPI/ISO)
├── canvas/SKILL.md     # Visualization
├── cast/SKILL.md       # Persona casting & registry management
├── compass/SKILL.md    # Skill ecosystem navigator and onboarding guide
├── compete/SKILL.md    # Competitive research
├── .claude/skills/darwin/SKILL.md  # Project-local ecosystem evolution
├── echo/SKILL.md       # Persona validation
├── experiment/SKILL.md # A/B test design
├── flow/SKILL.md       # Animation
├── forge/SKILL.md      # Prototyping
├── funnel/SKILL.md     # LP structure design and conversion strategy
├── frame/SKILL.md      # Figma design-to-code bridge
├── gauge/SKILL.md      # SKILL.md normalization audit & self-evolution
├── gateway/SKILL.md    # API design
├── gear/SKILL.md       # DevOps
├── grove/SKILL.md      # Repository structure design
├── growth/SKILL.md     # SEO/CRO
├── guardian/SKILL.md   # Git/PR management
├── helm/SKILL.md       # Business strategy simulation
├── hone/SKILL.md       # Codex CLI config audit & optimization
├── judge/SKILL.md      # Code review (codex review)
├── launch/SKILL.md     # Release management
├── lens/SKILL.md       # Codebase comprehension & investigation
├── .claude/skills/lore/SKILL.md    # Project-local knowledge curator
├── magi/SKILL.md       # Multi-perspective decision making
├── matrix/SKILL.md     # Universal multi-dimensional analysis
├── mend/SKILL.md       # Known failure auto-repair
├── morph/SKILL.md      # Document format conversion
├── muse/SKILL.md       # Design
├── vector/SKILL.md  # Browser automation
├── nexus/SKILL.md      # Orchestrator
├── .claude/skills/orbit/SKILL.md   # Project-local Nexus-autoloop extension
├── oracle/SKILL.md     # AI/ML design & evaluation
├── palette/SKILL.md    # UX
├── polyglot/SKILL.md   # i18n
├── prose/SKILL.md      # UX writing & content strategy
├── probe/SKILL.md      # Dynamic security testing (DAST)
├── pulse/SKILL.md      # Metrics design
├── quill/SKILL.md      # Documentation
├── radar/SKILL.md      # Testing
├── rally/SKILL.md      # Multi-session parallel orchestrator
├── relay/SKILL.md      # Messaging integration & real-time communication
├── field/SKILL.md # User research
├── ripple/SKILL.md     # Pre-change impact analysis
├── bond/SKILL.md     # Retention
├── trail/SKILL.md     # Git history investigation
├── riff/SKILL.md       # Interactive brainstorming partner
├── scaffold/SKILL.md   # Infrastructure
├── schema/SKILL.md     # DB schema design
├── siege/SKILL.md      # Advanced testing (load/contract/chaos/mutation)
├── scribe/SKILL.md     # Project documentation (PRD/SRS/design docs)
├── scout/SKILL.md      # Bug investigation
├── sentinel/SKILL.md   # Static security analysis (SAST)
├── sherpa/SKILL.md     # Task decomposition
├── sigil/SKILL.md      # Dynamic project-specific skill generation
├── vitrine/SKILL.md   # Storybook story management
├── spark/SKILL.md      # Feature proposals
├── stream/SKILL.md     # Data pipelines
├── sweep/SKILL.md      # Dead code detection
├── tome/SKILL.md       # Change-to-learning documentation
├── trace/SKILL.md      # Session replay analysis
├── triage/SKILL.md     # Incident response
├── tuner/SKILL.md      # DB performance optimization
├── vision/SKILL.md     # Creative direction
├── void/SKILL.md       # YAGNI enforcement & complexity reduction
├── voice/SKILL.md      # User feedback
├── voyager/SKILL.md    # E2E testing
└── zen/SKILL.md        # Refactoring
```

## Usage Examples

### Single Agent Usage

> Category-by-category examples for 100 global agents and 3 project-local extensions.

#### Orchestration

##### Chain Design (Nexus)

```
/Nexus
I want to implement a login feature. What steps should I follow?
```

**Output**: Task classification (FEATURE/M), recommended chain (Sherpa > Forge > Builder > Radar), prompt for the first step

---

##### Task Decomposition (Sherpa)

```
/Sherpa
The payment feature implementation task is too complex to organize. Please break it down.
```

**Output**: List of atomic steps completable within 15 minutes, progress checklist, specific instructions for the first task to start

---

##### Agent Design (Architect)

```
/Architect
Design an agent specialized in input validation.
I want it to handle Zod/Yup schema validation and error message generation.
```

**Output**: SKILL.md (complete specification), reference/*.md (3-7 domain-specific knowledge files), Nexus integration design

---

##### Product Delivery (`Nexus deliver`)

```
/Nexus deliver
Build me a task management SaaS with team collaboration features.
```

**Output**: Scope-classified product delivery — reuse scan, acceptance criteria, implementation, independent verification, and optional release preparation through the minimum viable chain.

---

##### Project Skill Generation (Sigil)

```
/Sigil
Analyze this project and generate useful skills for the team.
```

**Output**: Tech stack analysis, skill opportunity discovery, Micro/Full skills generated to `.claude/skills/` (e.g., new-page, new-api-route, deploy-flow)

---

##### Targeted Skill Creation (Sigil)

```
/Sigil
Generate a skill for creating new API routes in this Express project.
```

**Output**: Project-specific `new-route.md` skill with templates matching the project's existing patterns and conventions

---

**Architect vs Sigil responsibilities**:
- **Architect**: Designs universal ecosystem agents (400-1400 lines, SKILL.md)
- **Sigil**: Generates project-specific skills from live context (10-400 lines, .claude/skills/)

---

##### Autoloop Completion Scripts (Orbit)

> Repository-local: available only inside this repository through `.claude/skills/orbit/` or `.agents/skills/orbit/`.

```
/Orbit
Generate completion scripts for the Nexus autoloop that deploys and validates a staging environment.
Ensure the loop halts on test failures.
```

**Output**: Runner script with halt conditions, operation contract (SLA/budget/guardrails), audit checklist

---

#### Investigation & Planning

##### Bug Investigation (Scout)

```
/Scout
Users are reporting they can't log in. Please investigate the cause.
```

**Output**: Investigation report including reproduction steps, root cause, files to fix, and recommended fix approach

---

##### Feature Proposal (Spark)

```
/Spark
Suggest features to improve this application's usability.
```

**Output**: Feature proposal specification (Markdown) leveraging existing data/logic

---

##### Session Replay Analysis (Trace)

```
/Trace
The checkout flow has a high abandonment rate. Please analyze actual session data.
```

**Output**: Frustration signal detection, per-persona behavioral patterns, UX problem report

---

##### Persona Validation (Trace)

```
/Trace
Validate the "Mobile-First Millennial" persona defined by Field against real data.
```

**Output**: Persona definition validity check, sub-segment discovery, handoff to Field

**Trace vs Echo vs Field responsibilities**:
- **Field**: Creates personas (from interviews and research)
- **Trace**: Validates personas with real data (from session logs)
- **Echo**: Embodies personas to validate UI (simulation)

---

##### Persona Casting (Cast)

```
/Cast
Generate 5 user personas for our e-commerce platform from these analytics data and support tickets.
Register them in the persona registry for use by Echo and Field.
```

**Output**: Persona cards (demographics, goals, frustrations, tech proficiency), registry entries in unified format, downstream agent sync configuration

---

#### Git/PR Management

##### PR Preparation (Guardian)

```
/Guardian
Before creating a PR from this branch, suggest a commit structure and PR strategy.
```

**Output**: Signal/Noise analysis of changes, commit split plan, branch naming suggestions, PR description draft

---

##### Commit Splitting (Guardian)

```
/Guardian
I have changes across 47 files. Split them into appropriately granular commits.
```

**Output**: Commit split plan by logical unit, example git add commands

---

##### Branch Naming (Guardian)

```
/Guardian
Suggest a branch name for the task "Add OAuth2 to user authentication".
```

**Output**: Convention-compliant branch name candidates (e.g., feat/oauth2-integration)

---

**Guardian vs Judge vs Zen responsibilities**:
- **Guardian**: PR preparation (change analysis, commit structure, branch naming)
- **Judge**: PR review (bug detection, issue identification)
- **Zen**: Code fixes (refactoring, quality improvement)

---

##### Weekly Work Report (Launch)

```
/Launch
Summarize this week's PR activity into a report.
```

**Output**: Markdown report with PR statistics, category distribution, contributor rankings, and highlights

---

##### Release Notes Generation (Launch)

```
/Launch
Generate release notes from PRs between v1.1.0 and v1.2.0.
```

**Output**: Changelog-format release notes categorized into Features/Bug Fixes/Improvements/Breaking Changes

---

##### Individual Work Report (Launch)

```
/Launch
Create a monthly work report for @username.
```

**Output**: Detailed PR activity for the specific user, category breakdown, weekly trends, highlights

---

---

#### Quality Assurance

##### Test Addition (Radar)

```
/Radar
Check test coverage for this area and add missing tests.
```

**Output**: Added edge case tests, boundary value tests, and error case tests

---

##### E2E Test Creation (Voyager)

```
/Voyager
Create E2E tests for the flow from login to purchase completion.
```

**Output**: Playwright/Cypress E2E test code (with Page Object Model design, auth state management, CI integration config)

---

##### Security Audit (Sentinel)

```
/Sentinel
Audit the security of this API.
```

**Output**: Vulnerability detection (SQL injection, XSS, etc.) and fix code

---

##### PR Review (Judge)

```
/Judge
Review this PR. Check for bugs and security issues.
```

**Output**: Automated review via codex review, severity-ranked issue list, suggested fix agents

---

##### Pre-commit Check (Judge)

```
/Judge
Review the changes before committing.
```

**Output**: Review of uncommitted changes, bug/security issue detection, commit go/no-go decision

---

##### Refactoring (Zen)

```
/Zen
This file has poor readability. Please refactor it.
```

**Output**: Readable code split by responsibility (behavior unchanged)

**Note**: Review agent responsibilities:
- **Judge**: PR review via codex review, bug detection, AI hallucination detection (no code modifications)
- **Zen**: Code quality **improvement** (refactoring, readability enhancement)

---

##### YAGNI Verification (Void)

```
/Void
Is this helper utility really needed? It was added 6 months ago but I'm not sure anyone uses it.
```

**Output**: Subtraction Proposal with Cost-of-Keeping Score, blast radius analysis, and REMOVE/SIMPLIFY/DEFER/KEEP recommendation

---

#### Implementation

##### Production Implementation (Builder)

```
/Builder
The prototype works, but please bring it up to production quality.
```

**Output**: Production code with type safety, error handling, and validation added

**Builder capabilities**:
- **Clarify Phase**: Detects spec ambiguity, presents questions or multiple proposals
- **Design Phase**: TDD (test-first design)
- **Build Phase**: Event Sourcing / CQRS / Saga pattern support
- **Validate Phase**: N+1 detection, caching strategy, performance optimization
- **Forge handoff**: types.ts > Value Object, errors.ts > DomainError, forge-insights.md > Business Rules

---

##### Prototyping (Forge)

```
/Forge
Create a prototype of this screen. A working state is fine for now.
```

**Output**: Quickly built UI component that works with mock data

---

##### Frontend Implementation (Artisan)

```
/Artisan
Bring the user profile prototype created by Forge to production quality.
Ensure TypeScript strict mode, proper error handling, and accessibility.
```

**Output**: Type-safe, production-quality React/Vue/Svelte components, custom Hooks, state management integration

**Artisan's key areas**:
- **Hooks design**: Custom Hook creation, proper useEffect/useMemo usage
- **State management**: Zustand/Jotai/Redux Toolkit selection and implementation
- **Server Components**: Server/client separation in React 19/Next.js App Router
- **Form handling**: React Hook Form + Zod validation
- **Data fetching**: Caching strategy with TanStack Query/SWR

---

#### Performance

##### Performance Improvement (Bolt)

```
/Bolt
This page loads slowly. Please improve it.
```

**Output**: Bottleneck identification and optimization (memoization, lazy loading, query improvement, etc.)

**Bolt's scope**:
- **Frontend**: Re-render reduction, React.memo/useMemo, lazy loading, bundle size
- **Backend**: N+1 detection, DataLoader introduction, connection pooling, async processing

---

##### DB Performance Optimization (Tuner)

```
/Tuner
The product listing page query is slow. Analyze with EXPLAIN ANALYZE and optimize.
```

**Output**: Execution plan analysis, index recommendations, query rewrite

**Bolt vs Tuner responsibilities**:
- **Bolt**: Application layer (how queries are issued, caching)
- **Tuner**: Database layer (how queries execute, indexes)

---

#### UI/UX

##### Creative Direction (Vision)

```
/Vision
I want to redesign the dashboard with a modern look.
The current design feels dated, so incorporate current design trends.
```

**Output**: Three design direction proposals, style guide for the selected direction, delegation plan to Muse/Palette/Flow/Forge

---

##### Design Review (Vision)

```
/Vision
Review the current UI design and identify areas for improvement.
```

**Output**: Heuristic evaluation results, prioritized improvement list, assigned agent for each improvement

---

##### UX Improvement (Palette)

```
/Palette
We received feedback that this form has poor usability. Please improve it.
```

**Output**: Feedback improvements, cognitive load reduction, error display improvements

---

##### Design Unification (Muse)

```
/Muse
The design lacks consistency. Please unify it.
```

**Output**: Unification to design tokens, spacing/border-radius/shadow adjustments

---

##### UI Animation (Flow)

```
/Flow
Add animations to this screen to improve interactions.
```

**Output**: Appropriate transitions, hover effects, loading animations added

---

##### Persona Validation (Echo)

```
/Echo
Validate this UI's usability from an elderly user persona's perspective.
```

**Output**: UX report with confusion points and improvement proposals from the specified persona's perspective

---

##### Storybook Story Creation (Vitrine)

```
/Vitrine
Create Storybook stories for the newly created Button component.
```

**Output**: CSF 3.0 Story file (all variants, interaction tests, autodocs)

**Vitrine capabilities**:
- **CREATE**: New component story creation
- **MAINTAIN**: Existing story updates, CSF3 migration
- **AUDIT**: Story coverage and quality auditing

---

##### Storybook Coverage Audit (Vitrine)

```
/Vitrine
Audit current Storybook coverage. Identify missing stories.
```

**Output**: Coverage report, quality scores, improvement action list

---

#### Documentation

##### PRD Creation (Scribe)

```
/Scribe
Create a PRD (Product Requirements Document) for the user authentication feature.
Include social login and two-factor authentication in scope.
```

**Output**: Complete PRD (overview, user stories, functional requirements, non-functional requirements, acceptance criteria, edge cases)

---

##### SRS Creation (Scribe)

```
/Scribe
Create an SRS (Software Requirements Specification) for the payment module.
Stripe integration and subscription support are required.
```

**Output**: Complete SRS (functional requirements, data model, API specs, non-functional requirements, traceability matrix)

---

##### Implementation Checklist Creation (Scribe)

```
/Scribe
Create an implementation checklist for the search feature.
```

**Output**: Pre-implementation checks, phase-by-phase tasks, quality assurance checks, pre-deployment verification

---

##### Test Specification Creation (Scribe)

```
/Scribe
Create a test specification for the order flow.
Cover normal cases, error cases, and boundary values comprehensively.
```

**Output**: Test case list (ID, priority, steps, expected results), test data, traceability

---

**Scribe vs Quill responsibilities**:
- **Scribe**: Project documentation (specifications, design docs, checklists)
- **Quill**: Code documentation (JSDoc, README, type definitions)

---

##### Learning Document Generation (Tome)

```
/Tome
Explain the changes in this PR as a learning document for intermediate developers.
```

**Output**: Learning document with glossary, before/after comparisons, design decision records, and anti-pattern warnings

---

##### Documentation Addition (Quill)

```
/Quill
Add documentation to this function. There's feedback that the logic is hard to understand.
```

**Output**: JSDoc/TSDoc, usage examples, parameter descriptions added

---

#### Visualization

##### Diagram Creation (Canvas)

```
/Canvas
Visualize this authentication flow as a diagram.
```

**Output**: Mermaid-format sequence diagrams, flowcharts, state machine diagrams, etc.

---

##### Reverse-engineer Diagrams from Code (Canvas)

```
/Canvas
Visualize the processing flow in src/services/payment/
```

**Output**: Flowchart or sequence diagram generated by analyzing the code

---

##### Conversation Context Organization (Canvas)

```
/Canvas
Organize our conversation so far into a mind map.
```

**Output**: Mind map organizing the conversation content

---

##### ASCII Art Diagrams (Canvas)

```
/Canvas
Create an ASCII art diagram of this API's processing flow.
```

**Output**: ASCII-format flowchart displayable in terminals and code comments

---

##### AI Image Generation Code (Builder)

```
/Builder
Generate Python code to create product thumbnail images using Gemini API.
Include batch generation for multiple products.
```

**Output**: Production-ready Python code with Gemini API integration, prompt optimization, batch processing, cost estimation

---


#### Architecture

##### Architecture Analysis (Atlas)

```
/Atlas
Analyze code dependencies and clarify the impact scope of changes.
```

**Output**: Dependency map, problem area identification, ADR/RFC for improvements

---

##### Modernization (Shift)

```
/Shift detect
Check library versions in use and identify deprecated or vulnerable ones.
```

**Output**: Deprecated library detection, alternative proposals, migration PoC (use `Shift modernize` for native-API swaps, `Shift radar` for tech-maturity assessment)

---

##### API Design (Gateway)

```
/Gateway
Design user management API endpoints. Follow REST API best practices.
```

**Output**: OpenAPI specification, endpoint design, versioning strategy

---

##### API Breaking Change Detection (Gateway)

```
/Gateway
Check if this PR's changes break API backward compatibility.
```

**Output**: List of breaking changes, affected clients, migration guide

---

#### Data

##### DB Schema Design (Schema)

```
/Schema
Design a DB schema for the order management system.
Consider relationships between orders, line items, customers, and products.
```

**Output**: ER diagram (Mermaid format), DDL, migration files, index design

**Schema vs Tuner responsibilities**:
- **Schema**: Logical design (table structure, relations, normalization)
- **Tuner**: Physical optimization (index tuning, query improvement)

---

##### Migration Creation (Schema)

```
/Schema
Create a migration to add a profile image URL to the users table.
```

**Output**: Both Up/Down migrations, rollback procedures

---

#### DevOps

##### CLI/TUI Construction (Anvil)

```
/Anvil
Create a command-line tool. Include help display, progress bars, etc.
```

**Output**: CLI with argument parsing, help generation, progress bars, colored output

---

##### CI/CD Improvement (Gear)

```
/Gear
CI execution time is too long. Please reduce it.
```

**Output**: Cache optimization, parallelization, removal of unnecessary steps

---

##### Infrastructure Setup (Scaffold)

```
/Scaffold
Create Terraform configuration for building a staging environment on AWS.
```

**Output**: Terraform/CloudFormation/Pulumi configuration files, environment variable templates

---

##### AI CLI Config Audit (Hone)

```
/Hone
Audit my Codex CLI configuration and suggest optimizations based on latest best practices.

/Hone
Audit my Antigravity CLI settings.json and safety settings for best practice alignment.

/Hone
Audit my Claude Code permissions and MCP server configuration for security best practices.
```

**Output**: Audit report with Before/After diff proposals, priority classification, safety labels

---

##### Personal Dev Environment Setup (Anvil)

```
/Anvil
Optimize my zsh configuration. It's slow to start up and I want better completions.
```

**Output**: Optimized .zshrc with startup profiling, lazy-loading plugins, and completion configuration

---

##### Dotfile Management (Anvil)

```
/Anvil
Set up my neovim configuration with LSP support and lazy.nvim plugin management.
```

**Output**: init.lua structure, lazy.nvim setup, LSP configuration, keybindings

**Anvil vs Hone vs Gear vs Scaffold responsibilities**:
- **Anvil**: Personal environment (dotfiles, shell, editor, terminal)
- **Hone**: AI CLI configuration audit and Claude Code event-hook design/configuration/debugging
- **Gear**: Project-level DevOps (CI/CD, Docker, monitoring, Git hooks)
- **Scaffold**: Infrastructure provisioning (cloud, Docker Compose, IaC)
- **Gear[gha]**: GitHub Actions workflow design (triggers, security, performance, PR automation)

---

##### GitHub Actions Workflow Design (Gear[gha])

```
/Gear gha
Design a CI/CD workflow for this monorepo. We need path-based triggers, parallel jobs for each package, and SHA-pinned actions.
```

**Output**: GitHub Actions workflow YAML with path filters, job dependency graph, security-hardened permissions, cache strategy

---

##### CI Security Hardening (Gear[gha])

```
/Gear gha
Audit our GitHub Actions workflows for security issues. Check permissions, action pinning, and secret handling.
```

**Output**: Security audit report, remediation plan with SHA-pinned actions, minimal permissions configuration, OIDC recommendations

---

##### Claude Code Hook Setup (Hone)

```
/Hone
Add a hook to prevent writing to .env files and run tests before stopping.
```

**Output**: Hook configuration in settings.json (PreToolUse for file protection, Stop for test enforcement), backup creation, restart reminder

---

##### Hook Debugging (Hone)

```
/Hone
My PreToolUse hook isn't firing. Help me debug it.
```

**Output**: Diagnostic checklist, `claude --debug` analysis, manual test commands, fix recommendations

---

##### Local Development Environment Setup (Scaffold)

```
/Scaffold
Set up a Docker Compose environment so new developers can start immediately.
```

**Output**: docker-compose.yml, .env.example, setup scripts

---

#### Communication

##### Slack Bot Development (Relay)

```
/Relay
Build a Slack bot that responds to /remind commands and sends scheduled reminders.
Support thread replies and slash commands.
```

**Output**: Channel adapter design, command parser specification, webhook handler middleware chain, event routing matrix

---

##### Multi-Channel Notification (Relay)

```
/Relay
Design a notification system that sends alerts to both Slack and Discord.
Each platform should display messages in its native format.
```

**Output**: Unified message schema, platform-specific adapters, fan-out routing design

---

**Relay vs Gateway vs Stream responsibilities**:
- **Relay**: Messaging platform integration (channel adapters, webhooks, WebSocket, bots)
- **Gateway**: REST/GraphQL API design (OpenAPI specs, versioning, endpoints)
- **Stream**: Data pipelines (ETL/ELT, Kafka, Airflow, batch processing)

---

#### Internationalization

##### i18n Implementation (Polyglot)

```
/Polyglot
Internationalize the application for global expansion.
```

**Output**: Hardcoded strings converted to i18n, date/currency format internationalization

---

#### Growth

##### SEO Improvement (Growth)

```
/Growth
Improve the preview display when sharing on social media.
```

**Output**: OGP tags, meta information, structured data added

---

##### Retention Initiatives (Bond)

```
/Bond
User retention rates are declining. Suggest retention improvement strategies.
```

**Output**: Retention analysis framework, re-engagement trigger design, gamification proposals

---

#### Analytics

##### Metrics Design (Pulse)

```
/Pulse
Define KPIs for this service and design tracking events.
```

**Output**: KPI definitions, event design, dashboard specifications

---

##### A/B Test Design (Experiment)

```
/Experiment
Design an A/B test to verify the effect of changing the CTA button color.
```

**Output**: Hypothesis document, sample size calculation, feature flag implementation guide

---

#### Operations

##### Incident Response (Triage)

```
/Triage
API responses are slow in production. Please handle initial response.
```

**Output**: Impact assessment, recovery procedures, escalation decisions

---

##### Postmortem Creation (Triage)

```
/Triage
Create a postmortem for the recent incident.
```

**Output**: Incident timeline, root cause, prevention measures

---

#### Investigation & Planning (Additional)

##### Competitive Research (Compete)

```
/Compete
Analyze competitors A and B and identify differentiation points.
```

**Output**: Competitive feature matrix, SWOT analysis, positioning map

---

##### User Research Design (Field)

```
/Field
Design user interviews to validate the new feature.
```

**Output**: Interview guide, question list, persona/journey map

---

##### Feedback Analysis (Voice)

```
/Voice
Analyze recent app store reviews and extract insights.
```

**Output**: Sentiment analysis, feedback classification, improvement priority list

---

#### Security (Additional)

##### Dynamic Security Testing (Probe)

```
/Probe
Conduct penetration testing on the authentication API.
```

**Output**: OWASP ZAP/Nuclei scan results, vulnerability report, fix priority

**Sentinel vs Probe responsibilities**:
- **Sentinel**: Static analysis (SAST) - reads code to detect vulnerabilities
- **Probe**: Dynamic testing (DAST) - attacks running application to detect vulnerabilities

---

### Multi-Agent Collaboration (Nexus)

#### New Feature Development (Auto-execution)

```
/Nexus
I want to add a user profile editing feature
- Edit name, email, and avatar image
- With validation
- Show toast on successful save

## NEXUS_AUTORUN
```

**Execution chain**: Spark (spec) > Sherpa (task decomposition) > Forge (prototype) > Builder (production implementation) > Radar (tests) > Quill (documentation)

---

#### Bug Fix (Complex Case)

```
/Nexus
Investigate and fix a payment error that only occurs in production.
It doesn't reproduce locally.

## NEXUS_AUTORUN
```

**Execution chain**: Scout (investigation) > Sherpa (task decomposition) > Builder (fix) > Radar (regression tests) > Sentinel (security verification)

---

#### Large-scale Refactoring

```
/Nexus
The authentication module has become spaghetti code.
I want to refactor it to follow Clean Architecture.
```

**Execution chain**: Atlas (architecture design) > Sherpa (phased plan) > Zen (refactoring) > Radar (tests)

---

#### UI Feature Addition

```
/Nexus
Add a review submission feature to the product detail page.
I want users to be able to input star ratings and comments.
```

**Execution chain**: Spark (spec) > Forge (UI prototype) > Muse (design adjustment) > Builder (implementation) > Radar (tests)

---

### Step-by-Step Execution (Manual Control)

#### Gradual Feature Development

```
/Nexus
I want to add a search feature.
```

#### AUTORUN Mode (Automatic Execution - Recommended)

```
## NEXUS_AUTORUN_FULL
I want to add a search feature.
```

Nexus automatically executes the chain:

```
## Nexus Execution: Add search feature
- Chain: **Spark** > **Sherpa** > **Builder** > **Radar**
- Mode: AUTORUN_FULL

### Executing Step 1/4: Spark
_AGENT_CONTEXT:
  Role: Spark
  Task: Create search feature specification

[Creating specification as Spark...]

_STEP_COMPLETE:
  Agent: Spark
  Status: SUCCESS
  Next: Sherpa

### Executing Step 2/4: Sherpa
[Automatically proceeding to next step...]
```

**No copy-paste needed** - automatically executes to the final deliverable.

#### GUIDED Mode (Manual Handoff)

When invoking each agent manually:

```
## NEXUS_GUIDED
I want to add a search feature.
```

Nexus designs the chain and presents the next step:

```
## Nexus Plan: Add search feature
- Chain: **Spark** > **Sherpa** > **Builder** > **Radar**
- Current step: 1/4

### Next Step: Spark
Invoke **Spark** with the following context:
[Context information]
```

---

### Task Decomposition in Practice (Sherpa)

#### Breaking Large Tasks into Small Steps

```
/Sherpa
I want to implement an e-commerce checkout flow.
```

**Output**:

```
## Sherpa's Guide
**Current Objective:** Checkout flow implementation
**Progress:** 0/8 steps completed

### NOW: Create type definitions for cart contents
Define CartItem and CartSummary interfaces.
*(Shall I invoke Builder?)*

### Upcoming Path:
- [ ] Create cart API endpoint
- [ ] Shipping address input form
- [ ] Payment method selection UI
- [ ] Order confirmation screen
- [ ] Order completion processing
- [ ] Error handling
- [ ] Add tests

**Status:** On Track
```

## Customization

### Adding New Agents

1. Create `skills/[AgentName]/SKILL.md`
2. Define `name` and `description` in frontmatter
3. Specify boundaries (Always do / Ask first / Never do)
4. Add AUTORUN Support and Nexus Hub Mode sections

### Modifying Agents

Edit each `SKILL.md` directly. Format:

```markdown
---
name: AgentName
description: Agent description
---

[Detailed agent instructions]
```

## License

MIT
