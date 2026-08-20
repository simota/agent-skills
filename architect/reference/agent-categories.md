# Agent Categories

**Purpose:** Full roster of ecosystem agents grouped by category.
**Read when:** You already narrowed the category and need exact members, neighboring agents, or trigger summaries.

## Contents
- Category Overview
- Orchestration (4 agents)
- Investigation (9 agents)
- Implementation (6 agents)
- Testing (3 agents)
- Security (4 agents)
- Review (6 agents)
- Performance (2 agents)
- Documentation (4 agents)
- Architecture (7 agents)
- UX/Design (10 agents)
- DevOps (7 agents)
- Modernization (2 agents)
- Growth (2 agents)
- Analytics (3 agents)
- Git/PR (2 agents)
- Browser (2 agents)
- Data (2 agents)
- Strategy (3 agents)
- Translation (0 agents — absorbed)
- Incident (1 agent)
- Communication (1 agent + Scribe recipe)
- Meta / Tooling (8 agents)
- Creative / Media (2 agents)
- AI / ML (2 agents)
- Category Selection Guide

---

For first-pass category selection, read `reference/agent-category-guide.md` first.
Use this file when the exact current roster inside a category matters.

## Category Overview

| Category | Count | Purpose | Code Generation |
|----------|-------|---------|-----------------|
| Orchestration | 4 | Task coordination and decomposition | No |
| Investigation | 9 | Research and analysis | No |
| Implementation | 6 | Code creation | Yes |
| Testing | 3 | Test creation and resilience verification | Yes |
| Security | 4 | Security analysis and testing | Mixed |
| Review | 6 | Code review, quality, and compliance | Mixed |
| Performance | 2 | Performance optimization | Yes |
| Documentation | 4 | Documentation and UX writing | No (text) |
| Architecture | 7 | System design and structure | Mixed |
| UX/Design | 10 | User experience, interface, and persona | Mixed |
| DevOps | 7 | Infrastructure, CI/CD, and environment | Yes |
| Modernization | 2 | Technology migration | Mixed |
| Growth | 2 | SEO/CRO and retention | Mixed |
| Analytics | 3 | Metrics, experiments, and combinatorial analysis | Mixed |
| Git/PR | 2 | Version control workflows | No |
| Browser | 2 | Browser automation | Yes |
| Data | 2 | Data pipelines and conversion | Mixed |
| Strategy | 3 | Business strategy, game design, and domain advisory | No |
| Incident | 1 | Runtime issue detection and auto-repair | Mixed |
| Communication | 2 | Messaging, specification alignment | Mixed |
| Meta / Tooling | 8 | Ecosystem tools, auditing, knowledge, project-layer design | Mixed |
| Creative / Media | 2 | AI-generated visual, audio, and media content | Yes |
| AI / ML | 2 | AI/ML design, prompt engineering, and reframing | No |
**Total: 89 agents** (4 absorbed: Cipher → Nexus, Bridge/Accord → Scribe, Oath → Canon)

---

## Orchestration (4 agents)

Agents that coordinate other agents or decompose complex tasks.

### Nexus
- **Role**: Team orchestrator
- **Input**: User requests
- **Output**: Agent chain, coordination
- **Trigger**: Complex multi-agent tasks

### Sherpa
- **Role**: Task decomposition guide
- **Input**: Complex tasks
- **Output**: Atomic steps (15 min each)
- **Trigger**: Tasks that need breakdown

### Nexus — `deliver` mode
- **Role**: Scope-adaptive product/MVP delivery Recipe
- **Input**: Product goals (ambiguous or clear)
- **Output**: Complete products through a minimum chain sized as small/medium/epic
- **Trigger**: "Build a product", "full product lifecycle"

### Rally
- **Role**: Multi-session parallel orchestrator
- **Input**: Parallelizable task sets
- **Output**: Claude Code Agent Teams API sessions, merged results
- **Trigger**: "parallel execution", "multi-session", "concurrent tasks"

**Category Characteristics:**
- Never write code directly
- Coordinate other agents or external sessions
- Manage workflows and product lifecycle
- Track progress

---

## Investigation (9 agents)

Agents that research, analyze, and propose without writing code.

> **Note:** Cipher (intent decoder) was absorbed into Nexus.

### Scout
- **Role**: Bug investigator
- **Input**: Bug reports
- **Output**: Root cause analysis, fix locations
- **Trigger**: "investigate", "find cause", "bug"

### Spark
- **Role**: Feature proposer
- **Input**: Feature ideas
- **Output**: Feature specifications (Markdown)
- **Trigger**: "propose", "idea", "new feature"

### Compete
- **Role**: Competitive and personal-brand positioning analyst
- **Input**: Competitor names or an engineer's public portfolio
- **Output**: SWOT analysis, feature matrix, GitHub/blog/LinkedIn/talk positioning
- **Trigger**: "competitor", "differentiation", "compare", "personal brand", "portfolio"

### Voice
- **Role**: Feedback analyst
- **Input**: User feedback data
- **Output**: Sentiment analysis, insights
- **Trigger**: "feedback", "NPS", "review analysis"

### Field
- **Role**: User researcher
- **Input**: Research objectives
- **Output**: Interview guides, personas, journey maps
- **Trigger**: "interview", "persona", "research"

### Triage
- **Role**: Incident responder
- **Input**: Incident reports
- **Output**: Impact assessment, recovery steps
- **Trigger**: "incident", "outage", "recovery"

### Trail
- **Role**: Git history investigator
- **Input**: Regression reports
- **Output**: Root cause from commit history
- **Trigger**: "git history", "regression", "when did this break"

### Lens
- **Role**: Codebase understanding specialist
- **Input**: Codebase, exploration questions
- **Output**: Structure analysis, data flow traces, module responsibility maps
- **Trigger**: "how does this work", "codebase understanding", "trace the flow"

### Trace
- **Role**: Session replay behavioral analyst
- **Input**: User session logs, replay data
- **Output**: Behavioral pattern reports, UX problem narratives
- **Trigger**: "session replay", "user behavior", "behavioral analysis"

**Category Characteristics:**
- Read and analyze code, don't write it
- Produce reports and recommendations
- Gather context for other agents
- Identify problems, not solutions

---

## Implementation (6 agents)

Agents that write production-quality code.

### Builder
- **Role**: Production code and external-API craftsman
- **Input**: Specifications, prototypes, vendor API requirements
- **Output**: Type-safe production code, including image-generation API integrations
- **Trigger**: "implement", "production", "type-safe", "image API"

### Forge
- **Role**: Rapid prototyper
- **Input**: Feature ideas, UI mockups
- **Output**: Working prototypes, MVP
- **Trigger**: "prototype", "quickly", "PoC"

### Artisan
- **Role**: Frontend specialist
- **Input**: UI requirements
- **Output**: React/Vue/Svelte components
- **Trigger**: "frontend", "component", "React"

### Schema
- **Role**: Database designer
- **Input**: Data requirements
- **Output**: Migrations, DDL, ER diagrams
- **Trigger**: "schema", "migration", "DB design"


### Architect
- **Role**: Agent meta-designer
- **Input**: Ecosystem gaps
- **Output**: SKILL.md, reference/*.md
- **Trigger**: "new agent", "design agent"

**Category Characteristics:**
- Write production code
- Focus on quality and type safety
- Follow project conventions
- Generate testable code

---

## Testing (3 agents)

Agents that create and manage tests.

### Radar
- **Role**: Unit/integration test specialist
- **Input**: Code to test
- **Output**: Test files, coverage reports
- **Trigger**: "add tests", "coverage", "edge cases"

### Voyager
- **Role**: E2E test specialist
- **Input**: User flows
- **Output**: Playwright/Cypress tests
- **Trigger**: "E2E", "end-to-end", "user flow"

### Siege
- **Role**: Load/chaos/mutation test specialist
- **Input**: System endpoints, service topology
- **Output**: Load test scripts, contract tests, chaos experiments, mutation reports
- **Trigger**: "load test", "chaos engineering", "mutation test", "resilience"

**Category Characteristics:**
- Write test code
- Focus on coverage, edge cases, and system resilience
- CI/CD integration
- Regression prevention and non-functional verification

---

## Security (4 agents)

Agents that handle security analysis and testing.

### Sentinel
- **Role**: Static security analyst (SAST)
- **Input**: Source code
- **Output**: Vulnerability fixes, security patches
- **Trigger**: "security", "vulnerability", "audit"

### Probe
- **Role**: Dynamic security tester (DAST)
- **Input**: Running application
- **Output**: Penetration test results
- **Trigger**: "penetration", "dynamic test", "OWASP"

### Breach
- **Role**: Red team engineer
- **Input**: Target system, threat model scope
- **Output**: Attack scenarios, MITRE ATT&CK mappings, Purple Team exercises
- **Trigger**: "red team", "threat modeling", "attack scenario", "adversarial"

### Vigil
- **Role**: Detection engineer
- **Input**: Threat intelligence, log sources
- **Output**: Sigma/YARA rules, detection coverage maps, hunting hypotheses
- **Trigger**: "detection rules", "threat hunting", "Sigma", "YARA"

**Category Characteristics:**
- Security-focused analysis (defensive and offensive)
- Vulnerability detection and threat modeling
- Compliance checking
- Risk mitigation and detection engineering

---

## Review (6 agents)

Agents that review and improve code quality, enforce standards, and reduce complexity.

### Judge
- **Role**: Code reviewer
- **Input**: PRs, code changes
- **Output**: Review comments, issue lists
- **Trigger**: "review", "PR check", "code check"

### Zen
- **Role**: Refactoring specialist
- **Input**: Code to improve
- **Output**: Refactored code (same behavior)
- **Trigger**: "refactor", "readable", "clean up"

### Sweep
- **Role**: Dead code remover
- **Input**: Codebase
- **Output**: Unused file detection, safe deletions
- **Trigger**: "unused", "dead code", "cleanup"

### Attest
- **Role**: Specification compliance verifier
- **Input**: Specifications + implementation code
- **Output**: Compliance report, BDD scenarios, traceability matrix
- **Trigger**: "verify against spec", "acceptance criteria", "spec compliance", "BDD scenarios"

### Canon
- **Role**: Standards, regulatory, and legal-document compliance analyst
- **Input**: Codebase, target standards, ToS/privacy policy, jurisdiction
- **Output**: Compliance scores, legal-document gap reports, remediation proposals
- **Trigger**: "standards compliance", "WCAG audit", "OWASP check", "ToS review", "Tokushoho"

### Void
- **Role**: YAGNI verifier and complexity reducer
- **Input**: Code, features, specs, dependencies
- **Output**: Pruning proposals, scope cut recommendations
- **Trigger**: "YAGNI", "scope cut", "simplify", "do we need this"

**Category Characteristics:**
- Quality improvement and complexity reduction
- Code review automation
- Best practices and standards enforcement
- Specification compliance verification (Attest)
- Standards compliance evaluation (Canon)
- No feature changes

---

## Performance (2 agents)

Agents that optimize application performance.

### Bolt
- **Role**: Application optimizer
- **Input**: Slow code/pages
- **Output**: Optimized code
- **Trigger**: "slow", "performance", "optimize"

### Tuner
- **Role**: Database optimizer
- **Input**: Slow queries
- **Output**: Query rewrites, indexes
- **Trigger**: "query", "EXPLAIN", "index"

**Category Characteristics:**
- Performance measurement
- Bottleneck identification
- Optimization implementation
- Before/after comparison

---

## Documentation (4 agents)

Agents that create and maintain documentation and user-facing text.

### Quill
- **Role**: Documentation writer
- **Input**: Code, APIs
- **Output**: JSDoc, TSDoc, README
- **Trigger**: "document", "add comments", "type definitions"

### Scribe
- **Role**: Specification writer
- **Input**: Requirements
- **Output**: PRD, SRS, HLD, LLD documents
- **Trigger**: "specification", "design doc", "PRD"

### Canvas
- **Role**: Diagram creator
- **Input**: Code, concepts, specs
- **Output**: Mermaid diagrams, ASCII art, draw.io
- **Trigger**: "diagram", "visualize", "flowchart"

### Prose
- **Role**: UX writer
- **Input**: UI flows, brand voice guidelines
- **Output**: Microcopy, error messages, onboarding copy, voice & tone guides
- **Trigger**: "microcopy", "error message", "UX writing", "voice and tone"

**Category Characteristics:**
- Text generation (not code)
- API documentation
- Usage examples
- Visual representations
- User-facing copy and content strategy (Prose)

---

## Architecture (7 agents)

Agents that design system architecture and repository structure.

### Atlas
- **Role**: Dependency analyst
- **Input**: Codebase
- **Output**: ADR/RFC, dependency maps
- **Trigger**: "dependency", "architecture", "design"

### Gateway
- **Role**: API designer
- **Input**: API requirements
- **Output**: OpenAPI specs, versioning
- **Trigger**: "API design", "OpenAPI", "endpoint"

### Scaffold
- **Role**: Infrastructure designer
- **Input**: Infrastructure requirements
- **Output**: Terraform, Docker Compose
- **Trigger**: "infrastructure", "Terraform", "environment setup"

### Ripple
- **Role**: Change impact analyzer
- **Input**: Proposed changes
- **Output**: Impact assessment, risk evaluation
- **Trigger**: "impact analysis", "what will break", "change assessment"

### Grove
- **Role**: Repository structure designer
- **Input**: Repository, organizational requirements
- **Output**: Directory designs, docs/ structure, migration plans
- **Trigger**: "repo structure", "directory layout", "monorepo design"

### Grove — `llm` mode
- **Role**: LLM-optimized folder structure designer
- **Input**: Repository, LLM navigation pain points
- **Output**: Folder hierarchy designs, context-efficient layouts, token optimization reports
- **Trigger**: "LLM folder structure", "optimize for AI tools", "context efficiency", "CLAUDE.md hierarchy"

### Vector
- **Role**: Crawl system architect
- **Input**: Data collection requirements, scale parameters
- **Output**: Crawl architecture specs, frontier design, compliance subsystem design
- **Trigger**: "crawl architecture", "distributed crawler", "URL frontier", "web scraping infrastructure"

**Category Characteristics:**
- System-level design
- Long-term planning
- Documentation focus
- Trade-off analysis
- Repository structure optimization (Grove)

---

## UX/Design (10 agents)

Agents that handle user experience, interface design, persona management, and narrative design.

### Vision
- **Role**: Creative director
- **Input**: Design objectives
- **Output**: Design direction, style guides
- **Trigger**: "design direction", "redesign", "vision"

### Palette
- **Role**: UX improver
- **Input**: UI with usability issues
- **Output**: Usability improvements
- **Trigger**: "usability", "cognitive load", "a11y"


### Muse
- **Role**: Design system manager
- **Input**: Inconsistent UI
- **Output**: Token application, visual unity
- **Trigger**: "token", "design system", "dark mode"

### Flow
- **Role**: Animation specialist
- **Input**: UI interactions
- **Output**: CSS/JS animations
- **Trigger**: "animation", "transition", "hover"

### Echo
- **Role**: Persona validator
- **Input**: UI flows
- **Output**: UX confusion reports
- **Trigger**: "persona", "validate", "confusion points"

### Vitrine
- **Role**: Storybook manager
- **Input**: Components
- **Output**: CSF 3.0 stories
- **Trigger**: "Storybook", "story", "catalog"

### Frame
- **Role**: Figma MCP design bridge
- **Input**: Figma files via MCP Server
- **Output**: Structured design context, Code Connect mappings, design system rules
- **Trigger**: "Figma to code", "design context", "Code Connect"

### Cast
- **Role**: Persona casting and lifecycle manager
- **Input**: Diverse data sources (surveys, analytics, interviews)
- **Output**: Persona registry, persona cards, cross-agent sync formats
- **Trigger**: "create persona", "persona registry", "persona lifecycle"

### Saga
- **Role**: Narrative design and use case storyteller
- **Input**: Product features, user scenarios
- **Output**: Use case stories, customer journey narratives, product narratives
- **Trigger**: "use case story", "narrative design", "product narrative"

**Category Characteristics:**
- User-focused design
- Visual consistency
- Accessibility
- Component documentation
- Persona management and lifecycle (Cast)
- Narrative-driven use case design (Saga)

---

## DevOps (6 agents)

Agents that handle infrastructure, tooling, observability, and developer environment.

### Builder
- **Role**: CLI/TUI and developer-environment builder
- **Input**: CLI requirements, dotfile goals, shell/editor preferences
- **Output**: CLI tools, terminal UI, zsh/tmux/neovim/ghostty configuration, macOS automation
- **Trigger**: "CLI", "terminal", "command line", "dotfiles", "AppleScript"

### Gear
- **Role**: CI/CD optimizer
- **Input**: Build configs
- **Output**: Optimized CI/CD, Docker
- **Trigger**: "CI", "build time", "Docker"

### Launch
- **Role**: Release manager and PR reporter
- **Input**: Release requirements or PR history
- **Output**: Versioning, CHANGELOG, release notes, weekly/monthly engineering reports
- **Trigger**: "release", "version", "CHANGELOG", "weekly report", "PR metrics"

### Gear — `gha` mode
- **Role**: GitHub Actions workflow architect
- **Input**: Workflow requirements, existing CI/CD
- **Output**: GHA workflows, Composite Actions, Reusable Workflows, security configs
- **Trigger**: "GHA workflow", "workflow design", "CI security", "pipeline"

### Orbit
- **Role**: Loop automation script generator and operations specialist
- **Input**: Loop goals, contract artifacts, state files
- **Output**: Runner/bootstrap/verify/recover scripts, contract diagnoses, failure classifications
- **Trigger**: "loop automation", "nexus-autoloop", "loop ops", "runner generation"

### Beacon
- **Role**: Observability and reliability engineer
- **Input**: Service topology, SLO requirements
- **Output**: SLO/SLI designs, tracing configs, alert strategies, dashboards, capacity plans
- **Trigger**: "SLO", "observability", "distributed tracing", "alert strategy"

**Category Characteristics:**
- Infrastructure code
- Automation
- Developer experience and environment
- Build optimization
- Observability and reliability (Beacon)

---

## Modernization (1 agent)

Agents that update and modernize codebases. (Modernization scope absorbed into Shift's `detect`/`modernize`/`radar` recipes — see Migration category.)

### Polyglot
- **Role**: Internationalization specialist
- **Input**: Hardcoded strings
- **Output**: i18n implementation
- **Trigger**: "internationalization", "i18n", "translation"

**Category Characteristics:**
- Code transformation
- Compatibility maintenance
- Gradual migration
- Risk mitigation

---

## Growth (2 agents)

Agents that implement growth features.

### Growth
- **Role**: SEO/SMO/CRO specialist
- **Input**: Pages/components
- **Output**: SEO improvements, meta tags
- **Trigger**: "SEO", "OGP", "conversion"

### Growth
- **Role**: Retention strategist
- **Input**: Churn data
- **Output**: Retention features
- **Trigger**: "retention", "engagement", "churn"

**Category Characteristics:**
- Business metrics focus
- User engagement
- Data-driven decisions
- A/B testing ready

---

## Analytics (3 agents)

Agents that handle metrics, experiments, and combinatorial analysis.

### Pulse
- **Role**: Metrics designer
- **Input**: KPI requirements
- **Output**: Tracking events, dashboards
- **Trigger**: "KPI", "tracking", "dashboard"

### Experiment
- **Role**: A/B test designer
- **Input**: Hypotheses
- **Output**: Experiment designs
- **Trigger**: "A/B test", "hypothesis", "feature flag"

### Matrix
- **Role**: Universal combinatorial analyzer
- **Input**: Multi-dimensional axes and values
- **Output**: Minimum coverage sets, execution plans, priority rankings
- **Trigger**: "combination matrix", "coverage analysis", "combinatorial explosion"

**Category Characteristics:**
- Measurement focus
- Statistical rigor
- Hypothesis validation
- Data pipeline integration
- Combinatorial analysis across domains (Matrix)

---

## Git/PR (1 agent)

Agents that manage version control workflows.

### Guardian
- **Role**: PR strategist
- **Input**: Code changes
- **Output**: Commit structure, branch strategy
- **Trigger**: "commit", "branch", "PR preparation"

**Category Characteristics:**
- Git workflow management
- No code changes
- Reporting and analysis
- PR optimization

---

## Browser (1 agent)

Agents that automate browser interactions.

### Vector
- **Role**: Browser automation specialist
- **Input**: Browser tasks
- **Output**: Automated actions, screenshots
- **Trigger**: "browser automation", "scraping", "automate"

**Category Characteristics:**
- Playwright integration
- Visual verification
- Data extraction
- Task automation

---

## Data (2 agents)

Agents that handle data pipelines and transformations.

### Stream
- **Role**: ETL/ELT designer
- **Input**: Data requirements
- **Output**: Pipeline designs, Kafka/Airflow/dbt configs
- **Trigger**: "ETL", "data pipeline", "data flow"

### Scribe
- **Role**: Document converter
- **Input**: Documents in various formats
- **Output**: Converted documents (Markdown ↔ Word/Excel/PDF/HTML)
- **Trigger**: "convert", "document format", "export"

**Category Characteristics:**
- Data transformation
- Format conversion
- Pipeline design
- Quality assurance

---

## Strategy (3 agents)

Agents that simulate and plan business strategy, provide domain-specific advisory, or support multi-perspective decision making.

### Magi
- **Role**: Business strategy simulator
- **Input**: Financial data, market data, competitor intel, KPIs
- **Output**: Strategy roadmap, KPI forecast, scenario analysis, risk matrix
- **Trigger**: "business strategy", "business plan", "SWOT", "simulation", "M&A", "mid-term plan"

### Magi
- **Role**: Multi-perspective decision and strategy advisor
- **Input**: Decision context, founder bottleneck, or named figure whose documented thinking should be applied
- **Output**: Logic/Empathy/Pragmatism analysis, recommendation, pressure test, or attested named-figure lens
- **Trigger**: "decision", "tradeoff", "Go/No-Go", "what should I focus on", "what would <figure> do"


## Translation (0 agents — absorbed)

> **Note:** Bridge and Accord were absorbed into Scribe. Use Scribe's `unified` recipe for cross-functional specification needs including business-technical translation.

---

## Incident (1 agent)

Agents that detect, analyze, and auto-repair runtime issues.

### Mend
- **Role**: Auto-repair agent
- **Input**: Triage diagnoses, Beacon alerts, known failure patterns
- **Output**: Runbook execution, staged verification, rollback plans
- **Trigger**: "auto-repair", "known failure", "runbook execution"

**Category Characteristics:**
- Runtime issue detection
- Concurrency analysis
- Resource management
- Automated repair with safety tiers (Mend)

---

## Communication (1 agent + Scribe recipe)

Agents that design messaging integrations, real-time communication, and cross-functional specification alignment.

### Gateway
- **Role**: Messaging integration & real-time communication specialist
- **Input**: Messaging platform requirements, channel specifications, bot requirements
- **Output**: Channel adapters, webhook handlers, WebSocket servers, bot frameworks
- **Trigger**: "Build a bot", "Webhook handler", "Real-time chat", "Multi-channel messaging"

### Scribe (`cross-team` recipe)
- **Role**: Cross-functional specification aligner
- **Input**: Business/Dev/Design requirements
- **Output**: Integrated spec packages (L0 Vision → L1 Requirements → L2 Team Details → L3 Acceptance Criteria)
- **Trigger**: "unified spec", "cross-team alignment", "specification package"

> **Note:** Bridge and Accord were absorbed into Scribe's `unified` specification workflow.

**Category Characteristics:**
- Messaging platform integration
- Real-time communication design
- Bot development patterns
- Event-driven architecture
- Cross-functional specification alignment (Scribe `cross-team`)

---

## Meta / Tooling (7 agents)

Agents that generate project-specific tooling, audit ecosystem health, curate knowledge, and provide meta-visualization.

### Sigil
- **Role**: Dynamic project-specific skill generator
- **Input**: Project codebase, tech stack, conventions
- **Output**: Claude Code skills (.claude/skills/*.md)
- **Trigger**: "Generate skills for this project", "Create skill for", "Analyze project and suggest skills"

### Sigil — `blueprint` mode
- **Role**: Project operating-layer designer (project-scoped analogue of Architect)
- **Input**: Repository (stack, conventions, recurring tasks, existing .claude/ layer)
- **Output**: Operating-layer blueprint plus separate artifact tasks for Sigil/Nexus/Orbit/Hone/Grove
- **Trigger**: "design the project's agents/recipes/workflows", "operating layer for this repo", "project skill suite", "repo task playbooks", "project routing map"

### Darwin
- **Role**: Ecosystem self-evolution orchestrator
- **Input**: Git metrics, agent journals, activity logs, Health Scores, UQS
- **Output**: Ecosystem state report, evolution actions, dynamic affinity overrides
- **Trigger**: "evolution check", "ecosystem health", "agent fitness"

### Gauge
- **Role**: SKILL.md normalization auditor
- **Input**: SKILL.md files
- **Output**: 16-item compliance scans, fix proposals, best practice reports
- **Trigger**: "skill audit", "normalize SKILL.md", "compliance scan"

### Hone
- **Role**: AI CLI configuration and hooks optimizer
- **Input**: AI CLI configs (~/.codex/, ~/.gemini/, ~/.claude/)
- **Output**: Before/After config proposals, hook proposals (PreToolUse/PostToolUse/Stop), debug reports
- **Trigger**: "optimize CLI config", "audit claude settings", "codex config", "hooks", "PreToolUse"

### Lore
- **Role**: Ecosystem knowledge curator
- **Input**: Agent journals, activity logs, cross-agent patterns
- **Output**: Pattern catalogs, best practice propagation, knowledge decay reports
- **Trigger**: "cross-agent patterns", "knowledge sync", "institutional memory"

**Category Characteristics:**
- Analyzes project context before generating
- Generates Micro (10-80 lines) and Full (100-400 lines) skills
- Does not modify ecosystem agents
- Complements Architect (ecosystem) with project-specific skills
- Orchestrates ecosystem-wide evolution (Darwin)
- Audits and normalizes skill specifications (Gauge)
- Curates cross-agent institutional knowledge (Lore)

---

## Creative / Media (1 agent)

Agents that generate AI-powered visual, audio, and media content.


**Category Characteristics:**
- Generate code that produces creative assets (not assets directly)
- AI API integration (Gemini, Suno, ElevenLabs, Meshy, etc.)
- Media pipeline and format optimization
- Game and content production support

---

## AI / ML (3 agents)

Agents that specialize in AI/ML design, prompt engineering, and cognitive reframing.

### Chisel
- **Role**: Prompt-to-executable-specification translator
- **Input**: A supplied prompt containing vague wording, persona lines, or contradictory instructions; or (hub-invoked) a Nexus intent contract at the `SPECIFY` phase
- **Output**: Ambiguity ledger, derived rules, rewritten prompt, unresolved parameters; or a Specified Brief for a chain
- **Trigger**: "this prompt is vague", "make this prompt explicit", "you are a world-class …", "prompt audit"; `NEXUS_TO_CHISEL_SPECIFY`

### Oracle
- **Role**: AI/ML design and evaluation specialist
- **Input**: AI/ML requirements, evaluation needs
- **Output**: Prompt designs, RAG architectures, evaluation frameworks, MLOps plans
- **Trigger**: "prompt engineering", "RAG design", "LLM evaluation", "MLOps"

### Flux
- **Role**: Thinking refraction agent
- **Input**: Stuck problems, assumptions to challenge
- **Output**: Reframed problem statements, cross-domain analogies, perspective shifts
- **Trigger**: "stuck", "reframe", "different angle", "lateral thinking"

**Category Characteristics:**
- AI/ML domain expertise
- Prompt engineering and evaluation (system design → Oracle; a supplied prompt's wording → Chisel)
- Cognitive reframing and problem restructuring (Flux)
- No code generation (analysis and design focus)

---

## Category Selection Guide

For first-pass category choice, use `reference/agent-category-guide.md`.
Return to this file only when the exact roster inside the chosen category matters.
