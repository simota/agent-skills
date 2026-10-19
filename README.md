# AI Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Global Agents](https://img.shields.io/badge/Global_Agents-90-blue.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A skill collection that enables collaborative development with a team of specialized AI agents.

## Features

- **90 Global Agents + 3 Project-local Extensions** - Broad reusable coverage without exposing repository-specific operating skills everywhere
- **Nexus Orchestrator** - Analyzes tasks and automatically designs optimal agent chains
- **Platform Agnostic** - Works with Claude Code, Codex CLI, Antigravity CLI, and others

## Quick Start

### Installation

**Recommended — one working tree, symlinked into every CLI**

```bash
git clone https://github.com/simota/agent-skills.git ~/repos/agent-skills
cd ~/repos/agent-skills
make link
```

`make link` symlinks each skill directory into `~/.claude/skills`, `~/.agents/skills`, and
`~/.gemini/antigravity-cli/skills` individually, so every CLI reads the same working tree and a single `git pull`
updates all of them. Skills already present in those directories are preserved: a name that already
exists is reported and skipped, never overwritten. Missing destination parents are skipped except for the guarded Codex migration described below, so the same command works on a single-CLI machine. A directory is an installation hint, not a live CLI availability test.

| Command | Effect |
|---------|--------|
| `make link` | Link into all three CLI directories — `link-claude` / `link-codex` / `link-agy` for just one |
| `make status` | Show the link count per CLI (`linked / linkable`) and how many entries each directory holds |
| `make unlink` | Remove only links created by `make link`; other skills and custom aliases stay in place |

**Alternative — clone straight into a CLI directory**

```bash
# For Claude Code
git clone https://github.com/simota/agent-skills.git ~/.claude/skills

# For other platforms
git clone https://github.com/simota/agent-skills.git /path/to/your/skills
```

The shortest path when the target directory does not exist yet and only one CLI needs the skills.

### Usage

```
/Nexus I want to implement a login feature
/Scout Investigate the cause of this bug
/Radar Improve test coverage
/Vision I want to redesign the dashboard with a modern look
```

### Runtime compatibility and legacy Codex installs

Current model/CLI facts and official sources live in [`_common/CLI_COMPATIBILITY.md`](_common/CLI_COMPATIBILITY.md). Skills remain model-agnostic; actual availability, permissions and loading require runtime verification. Gemini CLI and Cursor are secondary readers, not additional installer targets.

Codex skills now use `~/.agents/skills`; settings still use `~/.codex`. The installer preserves old files. To remove **only this repository's old links**, run `make unlink-codex CODEX_DIR="$HOME/.codex/skills"`, inspect the result, then `make link-codex`. Foreign files/links are not removed. If `.agents` is absent but `.codex` exists, the installer creates the new parent only outside the source repository; otherwise create the intended external skill root explicitly.

## Overview

This repository contains 90 globally reusable AI agents and 3 repository-local operating extensions. Each skill specializes in a specific domain and is coordinated by the **Nexus** orchestrator when available in the active profile.

### Roster Counting

- **90 global skills** are the active, reusable roster under `<skill-name>/SKILL.md`.
- **3 project-local extensions** (`orbit`, `lore`, and `darwin`) are repository operating skills and are not included in the global count or global profiles.
- `.claude/skills/` is the canonical project-local location; `.agents/skills/` is a cross-tool mirror, not an additional set of skills.
- `.archive/` holds a retired skill only while `prune`'s sunset protocol keeps it, and is excluded from every active-roster count. It is currently empty; earlier retired packages are recoverable from git history.

The active repository surface is therefore **90 global + 3 project-local = 93 distinct skills**.

## Agent Catalog

> Category-by-category catalog for 90 global agents plus the 3 project-local extensions marked below.

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
| **Gauge** | _"What gets measured gets managed. What gets audited gets normalized."_ - SKILL.md normalization auditor and self-evolving compliance agent. Scans all skills against the 21-item checklist, classifies violations with P0-P3 priority, generates concrete fix snippets, and evolves detection patterns via web research. No code written | Compliance reports, fix plans, dashboards |
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
| **Magi** | _"Three minds, one verdict. Consensus through diversity."_ - Multi-perspective decisions, founder office hours, bottleneck triage, pitch critique, advisory lenses grounded in documented notable-figure thinking, and business scenario simulation (`simulate` Recipe) | Decision and advisory report |
| **Flux** | _"Bend the light. See what was always there."_ - Thinking refraction engine. Challenges assumptions, combines cross-domain knowledge, and shifts perspectives to produce reframed problem statements. Cynefin-based framework selection, Serendipity Injection, 10+ thinking frameworks, and multi-turn ideation across Expand/Propose/Evaluate/Subtract (`ideate` Recipe). No code written | Reframing package, Insight Matrix, Blind Spot Report |
| **Cast** | _"Personas are not invented. They are discovered, born, and evolved."_ - Persona casting agent. Rapid generation, registry management, lifecycle tracking, and cross-agent distribution of personas from diverse inputs | Persona registry |
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
| **Radar** | _"Untested code is unfinished code."_ - Unit/integration test addition, flaky test fixing, coverage improvement, and test-data factories/fixtures (`fixtures` Recipe) | Test code |
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
| **Breach** | _"Think like an attacker. Defend like an engineer."_ - Red team engineering. Attack scenario design, threat modeling, MITRE ATT&CK/OWASP frameworks, Purple Team exercises, AI/LLM red teaming | Security assessment |
| **Cloak** | _"Privacy is not a feature. It's a right."_ - Privacy engineering and data governance. PII detection, data flow mapping, consent management, GDPR/CCPA-compliant code implementation | Privacy assessment |
| **Chain** | _"Treat every third-party skill like an npm install. Audit before invoking."_ - Skill/plugin/MCP intake audit plus live npm/PyPI malware investigation. Generates sha256 manifests, scans Unicode and exfiltration patterns, matches campaign IoCs, and produces persistence-first eradication and credential-rotation runbooks | Supply-chain audit, infection report and recovery runbook |

### Implementation

| Agent | Description | Output |
|-------|-------------|--------|
| **Builder** | _"Types are contracts. Code is a promise."_ - Type-safe production implementation plus Gemini image-generation/editing code, prompt design, batch generation, style transfer, post-processing, provenance, and content-policy gates, plus CLI/TUI construction (`cli`) and regex/parser/DSL authoring (`grammar`) | Production and image-generation code |
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
| **Scribe** | _"A specification is a contract between vision and reality."_ - Specification author for PRD/SRS/HLD/LLD and cross-team L0-L4 packages (`unified` Recipe), including implementation checklists, test specifications, and document format conversion (`convert` Recipe) | Specs, design docs |
| **Quill** | _"Code tells computers what to do. Documentation tells humans why."_ - JSDoc/TSDoc additions, README updates, typing `any` to proper type definitions | Documentation |
| **Tome** | _"Changes are forgotten. Knowledge endures."_ - Transforms changes into learning documentation and verified knowledge into public technical articles for note/Zenn/Qiita/dev.to, including article series and repurposing | Learning docs and technical articles |

**Scribe vs Quill vs Tome responsibilities**:
- **Scribe**: Project documentation (PRD, SRS, design docs, checklists, test specifications) and format conversion (Markdown > PDF/Word/HTML, `convert` Recipe)
- **Quill**: Code documentation (JSDoc/TSDoc, README, type definitions)
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
| **Gateway** | _"APIs are promises to the future. Design them like contracts."_ - API design, review, OpenAPI spec generation, versioning strategy, breaking change detection, and messaging-platform integration (`messaging` Recipe) | API specifications |
| **Grove** | _"A well-structured repository is a well-structured mind."_ - Human- and LLM-optimized repository structure design, including context efficiency, prompt-cache topology, and sharding | Structure design, audit reports |
| **Weave** | _"Every state tells a story. Every transition is a contract."_ - Workflow and state machine design specialist. State transition design, invalid transition detection, Saga patterns, approval flows, and cron/timezone/business-calendar scheduling (`schedule` Recipe) | Designs, diagrams |
| **Seek** | _"The right result at the right time in the right order."_ - Search engine and vector DB design specialist. Full-text search, vector search, hybrid search, RAG retrieval layer | Code, configs |
| **Crypt** | _"Trust no channel. Verify every key."_ - Cryptographic architecture design: algorithm selection, key management, E2E encryption, KMS integration, TLS configuration | Crypto design specs |

**Gateway > Builder > Radar chain**: Gateway (messaging design) > Builder (implementation) > Radar (tests)

### Data

| Agent | Description | Output |
|-------|-------------|--------|
| **Schema** | _"A schema is a contract with the future."_ - DB schema, migration, ER diagram, and multi-tenant isolation/RLS/routing design | Migrations / schema definitions |
| **Stream** | _"Data flows like water. My job is to build the pipes."_ - Data pipelines. ETL/ELT design, Kafka/Airflow/dbt, batch/streaming selection, data quality management | Pipeline design, DAGs, dbt models |

**Schema > Stream chain**: Schema (data model) > Stream (pipeline design)

### DevOps

| Agent | Description | Output |
|-------|-------------|--------|
| **Gear** | _"The best CI/CD is the one nobody thinks about."_ - Dependency management, CI/CD and Docker optimization, plus advanced GitHub Actions workflow design | Configuration files |
| **Scaffold** | _"Infrastructure is the silent foundation of every dream."_ - Cloud infrastructure (Terraform/CloudFormation/Pulumi), local dev environments (Docker Compose), IaC design | Infrastructure config |
| **Hone** | _"A sharp blade cuts clean. A sharp config cuts friction."_ - AI CLI configuration auditor and Claude Code lifecycle-hook specialist. Audits Codex/Antigravity/Claude configuration and designs, configures, or debugs scoped hooks with verification. Also owns the personal environment — dotfiles, shell/editor config, and macOS automation (`env` / `automate` Recipes) | Audit reports, proposals and hook configurations |
| **Ledger** | _"Every dollar has a story. Make it a short one."_ - FinOps and cloud cost optimization. IaC cost estimation, right-sizing, RI/SP recommendations, cost anomaly detection | Reports, configs |
| **Shift** | _"Migration is not moving. It's transforming."_ - Migration and upgrade orchestrator. Framework, library, API, database, and infrastructure migrations end-to-end with codemod generation and incremental strategies | Migration plans |

**Builder vs Hone vs Gear vs Scaffold responsibilities**:
- **Builder**: CLI and TUI construction (`cli` Recipe) — the tool itself
- **Hone**: Personal environment (dotfiles, shell, editor, terminal, macOS automation) plus AI CLI configuration audit and Claude Code event-hook design/configuration/debugging
- **Gear**: Project-level DevOps (CI/CD, Docker, monitoring, Git hooks); `gha` mode owns advanced GitHub Actions
- **Scaffold**: Infrastructure provisioning (cloud, Docker Compose, IaC)

### Internationalization

| Agent | Description | Output |
|-------|-------------|--------|
| **Polyglot** | _"Every language deserves respect. Every user deserves their mother tongue."_ - i18n support. Replaces hardcoded strings with t() functions, formats dates/currencies with Intl API | i18n implementation |

### Growth

| Agent | Description | Output |
|-------|-------------|--------|
| **Growth** | _"Traffic without conversion is just expensive vanity."_ - SEO (meta/OGP/JSON-LD), SMO (social share display), CRO (CTA improvement), and retention/re-engagement design (`retention` Recipe) | Growth initiatives |
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
| **Vector** | _"The browser is a stage. Every click is a scene."_ - Browser automation via Playwright/Chrome DevTools. Data collection, form interaction, screenshots, network monitoring, and crawl-system architecture (`crawl` Recipe) | Automation scripts |

**Cue vs Vitrine responsibilities**:
- **Cue**: Browser (Web UI) demo videos (Playwright, .webm output)
- **Vitrine**: Component catalogs and Storybook stories with visual-regression wiring

## Workflows

### Basic Usage

1. Invoke an agent with `/AgentName`
2. The agent executes the task
3. Suggests handoff to other agents as needed

### Orchestration with Nexus

Use **Nexus** for complex tasks. Nexus operates in the following modes:

| Mode | Trigger | Behavior | Interaction |
|------|---------|----------|-------------|
| **Full Auto** (default) | no marker, or `## NEXUS_AUTORUN_FULL` | Executes all tasks, including COMPLEX, with guardrails | Ask First triggers and guardrail escalations only |
| **Auto** | `## NEXUS_AUTORUN` | Executes simple tasks only; complex tasks fall back to Guided | Ask First triggers, guardrail escalations, and errors |
| **Guided** | `## NEXUS_GUIDED` | Confirms at decision points | Option-based interaction |
| **Interactive** | `## NEXUS_INTERACTIVE` | Confirms at each step | Always interactive |
| **Continue** | `## NEXUS_HANDOFF` | Result handoff | Interaction as needed |

### Interactive Execution (Guided/Interactive)

Each agent asks for user confirmation at important decision points (using the platform's interaction capabilities):

- **Start confirmation** (Interactive only): Confirms approach after chain design, before execution — Guided confirms only at decision points
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
| Estimated steps | 1-2 | 6+ (3-5 = MEDIUM) |
| Affected files | 1-3 | 4+ |
| Security-related | No | Yes |
| Destructive changes | No | Yes |

- **Default (AUTORUN_FULL)**: Executes all tasks, including COMPLEX, with guardrails
- **SIMPLE + NEXUS_AUTORUN**: Fully automatic execution
- **COMPLEX under NEXUS_AUTORUN**: Switches to Guided mode (interaction required)

See `_common/INTERACTION.md` for details.

### Chain Templates by Task Type

> **Source of truth:** base chains (rows without a `/variant`) come from `nexus/reference/routing-matrix.md`; `TYPE/variant` rows come from `nexus/reference/agent-chains.md`. This is a representative excerpt — where it differs, those files win. Variant rows omit the terminal Guardian (SHIP) step that the matrix default adds for code changes; `?` marks an optional step.

#### Investigation & Incidents

| Task | Use | Chain |
|------|-----|-------|
| INVESTIGATE | Does X exist / how does it work | Lens |
| INVESTIGATE/flow | Data/processing flow tracing | Lens > Canvas |
| INVESTIGATE/onboarding | Whole-codebase understanding | Lens > Scribe |
| INVESTIGATE/pre-impl | Investigate, then implement | Lens > Builder > Radar |
| INVESTIGATE/regression | Regression from a past commit | Trail > Scout > Builder > Radar |
| BUG/simple | Simple bug fix | Scout > Lens > Radar > Builder > Radar |
| BUG/complex | Complex bug (RCA required) | Scout > Lens > Sherpa > Radar > Builder > Radar > Sentinel |
| INCIDENT/SEV1/2 | Major incident | Triage > Scout > Builder > Radar > Triage (postmortem) |

> **Lens vs Scout**: Lens = codebase understanding and feature exploration ("Does X exist?", "How does Y flow?"), Scout = bug investigation and root cause analysis ("Why did it break?")

#### Features, APIs & Integrations

| Task | Use | Chain |
|------|-----|-------|
| FEATURE/S | Small feature | Builder > Radar |
| FEATURE/M | Medium feature | Sherpa > Forge > Builder > Radar |
| FEATURE/L | Large feature | Spark > Sherpa > Forge > Builder > Radar > Quill |
| FEATURE/UI | UI-heavy feature | Spark > Forge > Muse > Builder > Lens > Radar |
| FEATURE/frontend | Frontend feature | Forge > Artisan > Radar |
| API/new | New API | Gateway > Builder > Radar > Quill |
| MESSAGING | Chat bots, channel adapters, WebSocket/SSE | Gateway > Builder > Radar |
| WEBHOOK | Webhook contracts and handlers | Gateway > Builder |

#### Design & UX

| Task | Use | Chain |
|------|-----|-------|
| DESIGN/creative | New visual direction to UI | Vision > Muse > Forge > Artisan > Radar |
| DESIGN/flow | Animation / interaction | Flow > Artisan > Radar |
| DESIGN/usability-audit | Usability fixes | Palette > Artisan > Radar |
| DESIGN_SYSTEM/full | Design system build-out | Vision > Muse > Vitrine > Artisan > Quill > Radar |
| UX_RESEARCH | UX research | Field > Echo > Palette |
| UX_RESEARCH/session-replay | Session analysis | Trace > Field > Echo > Palette |

#### Refactoring, Performance & Quality

| Task | Use | Chain |
|------|-----|-------|
| REFACTOR/small | Small refactor | Radar? > Zen > Radar |
| REFACTOR/arch | Architecture improvement | Atlas > Sherpa > Zen > Radar |
| OPTIMIZE/app | Application hotspot | Bolt > Radar |
| OPTIMIZE/db | Database optimization | Tuner > Schema > Builder > Radar |
| YAGNI/standard | Subtract over-engineering | Void > Sweep > Zen > Radar |
| ANALYSIS | Change impact analysis | Ripple > Builder > Radar |
| ANALYSIS/cleanup | Code cleanup | Sweep > Zen > Radar |
| QUALITY/standard | Quality audit | Judge > Zen > Radar > Sentinel > Canvas |

#### Security, Testing & Review

| Task | Use | Chain |
|------|-----|-------|
| SECURITY/static | Static analysis | Sentinel > Builder > Radar > Sentinel |
| SECURITY/dynamic | Dynamic testing | Sentinel > Probe > Builder > Radar > Probe |
| SECURITY/full | Full audit | Sentinel > Probe > Builder > Radar > Sentinel > Probe |
| TEST | Unit / coverage | Radar |
| TEST/e2e | E2E tests | Voyager > Lens > Radar |
| LOAD_TEST/chaos | Chaos engineering | Siege > Bolt > Triage > Builder > Beacon |
| REVIEW/PR | PR review | Judge > Builder/Zen/Sentinel (based on findings) > Radar |

#### AI, Operations & Release

| Task | Use | Chain |
|------|-----|-------|
| AI_FEATURE | LLM feature | Oracle > Builder > Radar |
| AI_FEATURE/rag | RAG pipeline | Oracle > Gateway > Builder > Radar |
| PROMPT_SPEC | Vague prompt to executable spec | Chisel |
| OBSERVABILITY/slo-design | SLO definition & monitoring | Beacon > Gear > Builder > Radar |
| INFRA | Infrastructure setup | Scaffold > Gear > Radar |
| GHA_WORKFLOW/new | New GitHub Actions workflow | Gear[gha] > Radar |
| PRERELEASE/full | Pre-release gate | Sentinel > Radar > Guardian > Launch |
| DEPLOY/full | Full release pipeline | Radar > Guardian > Launch |
| MODERNIZE/stack | Tech stack refresh | Lens > Shift (detect+modernize) > Sherpa > Builder > Radar |

#### Decisions, Strategy & Documents

| Task | Use | Chain |
|------|-----|-------|
| DECISION/architecture | Architecture selection | Magi > Builder/Zen (based on verdict) |
| DECISION/strategy | Strategic decision | Scribe[unified] > Magi > Spark |
| ADVISORY | Office-hours advisory | Magi > (Builder/Echo/Sherpa) |
| STRATEGY/compete | Competitive analysis to implementation | Compete > Spark > Builder > Radar |
| MARKETING/quick | Quick marketing plan | Compete > Growth > Funnel |
| REQUIREMENTS/complex | PRD / requirements | Scribe[unified] > Magi > Scribe > Sherpa > Canvas |
| DOCS | Code documentation | Quill |
| DOCS/report | PR report | Launch[weekly] > Scribe |
| PROJECT/full | Full product from an ambiguous goal | Nexus[deliver] > Sherpa > Builder > Radar > Guardian > Launch |

#### Parallel Execution (Rally Integration)

For large-scale tasks where parallel execution is beneficial, Nexus escalates to Rally (`agent-chains.md` § Rally Parallel Chain Variants).

| Base Chain | Parallel Chain |
|------------|----------------|
| FEATURE/L | Spark > Sherpa > Rally(Forge+Artisan, Builder, Radar) |
| FEATURE/M (multi-unit) | Sherpa > Rally(Builder x N, Radar) |
| FEATURE/fullstack | Rally(Artisan, Builder, Radar) |
| BUG/multiple | Rally(Builder x N) > Radar |
| REFACTOR/arch (multi-module) | Atlas > Sherpa > Rally(Zen x N) > Radar |
| SECURITY/full | Rally(Sentinel, Probe) > Builder > Radar |
| TEST/coverage | Rally(Radar, Voyager) |
| MODERNIZE/stack | Lens > Shift (detect+modernize) > Sherpa > Rally(Builder x N) > Radar |
| DOCS/full | Rally(Quill, Canvas, Vitrine) |

> **Rally Escalation Criteria**: Rally is triggered when there are 2+ independent implementation steps, changes span 4+ files across 2+ domains, or Sherpa detects a `parallel_group`.

> **Nexus parallel vs Rally**: Nexus's built-in `_PARALLEL_BRANCHES` is for lightweight parallelism (each branch < 50 lines). Rally's multi-session parallelism is used for substantial implementation work.

> **Nexus build modes**: `feature` handles one bounded capability, `deliver` sizes a product/MVP chain to scope, and `apex` runs a high-investment discovery-to-ship workflow.

## Shared Knowledge

Agents share knowledge through the `.agents/` directory:

| File | Purpose | When to Update |
|------|---------|---------------|
| `PROJECT.md` | Shared knowledge + activity log | When the task produced a reusable insight or a decision later agents need (`_common/OPERATIONAL.md` § Activity Log) |
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

Shared rules live in `_common/` (`BOUNDARIES.md`, `OPERATIONAL.md`, `INTERACTION.md`, ...); each skill's `## Boundaries` section states its own Always / Ask first / Never rules.

### Boundary Types

| Marker | Meaning |
|--------|---------|
| Always do | Must always be done |
| Ask first | Requires confirmation |
| Never do | Must never be done |

## Directory Structure

```
agent-skills/
├── <skill>/                # one directory per global skill (see Agent Catalog)
│   ├── SKILL.md            # entry point: frontmatter, boundaries, recipes
│   └── reference/          # optional on-demand references
├── .claude/skills/         # project-local skills: darwin, lore, orbit (canonical)
├── .agents/skills/         # synchronized mirror of .claude/skills/
├── _common/                # shared protocols (BOUNDARIES.md, HANDOFF.md, ...)
│   └── scripts/            # checkers behind `make validate` / `make test`
├── _templates/             # SKILL_TEMPLATE.md, PROJECT.md, kits
└── Makefile                # link / unlink / status / validate / test / check / hooks
```

## Usage Examples

### Multi-Agent Collaboration (Nexus)

#### New Feature Development (Auto-execution)

```
/Nexus
I want to add a user profile editing feature
- Edit name, email, and avatar image
- With validation
- Show toast on successful save

## NEXUS_AUTORUN_FULL
```

**Execution chain**: Spark (spec) > Sherpa (task decomposition) > Forge (prototype) > Builder (production implementation) > Radar (tests) > Quill (documentation)

---

#### Bug Fix (Complex Case)

```
/Nexus
Investigate and fix a payment error that only occurs in production.
It doesn't reproduce locally.

## NEXUS_AUTORUN_FULL
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

## NEXUS_INTERACTIVE
```

`## NEXUS_INTERACTIVE` confirms before every step; `/Nexus` with no marker runs as AUTORUN_FULL.

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

#### GUIDED Mode (Confirm at Decision Points)

Nexus runs the chain itself and pauses only at decision points (Ask First triggers, guardrail escalations, or a skill's interaction triggers). Use `## NEXUS_INTERACTIVE` to confirm every step instead:

```
## NEXUS_GUIDED
I want to add a search feature.
```

Nexus designs the chain, runs it, and stops when a decision needs you:

```
## Nexus Plan: Add search feature
- Chain: **Spark** > **Sherpa** > **Builder** > **Radar**
- Current step: 1/4 (Spark)

### Decision needed
Spark proposed two search scopes. Which should Sherpa plan for?
[Options]
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

Follow [CONTRIBUTING.md § 新しいグローバルエージェントの追加](CONTRIBUTING.md#新しいグローバルエージェントの追加) (adding a new global agent): it lists the required sections, the Complexity Budget declaration, every roster that must be updated by hand, and the generators to re-run. A new skill is done when `make check` passes.

### Modifying Agents

Edit each `SKILL.md` directly, following [_templates/SKILL_TEMPLATE.md](_templates/SKILL_TEMPLATE.md). Frontmatter example:

```markdown
---
name: skill-name
description: Agent description
---

[Detailed agent instructions]
```

## License

MIT
