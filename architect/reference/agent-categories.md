# Agent Categories

**Purpose:** Full roster of ecosystem agents grouped by their primary responsibility.
**Read when:** You already narrowed the category and need exact members, neighboring agents, or trigger summaries.

For first-pass category selection, read `reference/agent-category-guide.md` first. Role boundaries remain authoritative in `_common/BOUNDARIES.md`.

Each global skill appears exactly once below. Secondary capabilities and Recipes belong to their owner; they do not increase the agent count. Project-local extensions have a separate availability gate and are listed after the global roster.

The Agent column gives the installed skill directory name. To open its definition, resolve `<skill-name>/SKILL.md` from the active CLI's global skill root; do not resolve it from Architect's directory or this reference file. Resolve project-local extensions through `_common/PROJECT_LOCAL_SKILLS.md`.

## Category Overview

| Category | Global skills |
|----------|---------------|
| Orchestration | 3 |
| Investigation | 11 |
| Implementation | 6 |
| Testing | 3 |
| Security | 7 |
| Review | 6 |
| Performance | 2 |
| Documentation | 8 |
| Architecture | 7 |
| UX/Design | 9 |
| DevOps | 4 |
| Modernization | 3 |
| Growth | 2 |
| Analytics | 3 |
| Git/PR | 1 |
| Browser | 1 |
| Data | 1 |
| Strategy | 2 |
| Incident | 1 |
| Meta / Tooling | 6 |
| Creative / Media | 1 |
| AI / ML | 3 |

**Total: 90 global skills + 3 project-local extensions.**

Nexus `deliver`, Grove `llm`, Gear `gha`, and Sigil `blueprint` are modes or Recipes of existing skills. Messaging and real-time communication belong to Gateway (Architecture); cross-team specification alignment belongs to Scribe (Documentation); translation belongs to Polyglot (Modernization). These capabilities are not separate agents.

## Orchestration (3 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `nexus` | Orchestrating multi-specialist task chains and scope-adaptive product delivery: classifies intent, selects and executes the minimum viable chain, aggregates results, and verifies acceptance criteria. For multi-domain tasks, build-first delivery, and product lifecycle execution. |
| `sherpa` | Guiding workflows by decomposing complex tasks (Epics) into Atomic Steps under 15 minutes each, with progress tracking and drift prevention. Use when complex decomposition is needed. |
| `rally` | Orchestrating multi-session parallel execution via Claude Code Agent Teams API and Codex CLI Subagents — launch, manage, coordinate concurrent tasks. Use when parallel work is needed. |

## Investigation (11 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `scout` | Investigating bugs via root cause analysis, reproduction steps, and impact assessment. Investigation-only — finds why bugs occur and where to fix them, no code. Use when a bug needs RCA before a fix. |
| `spark` | Proposing new features leveraging existing data/logic as Markdown specifications. Use when brainstorming new features, product planning, or feature proposals are needed. Does not write code. |
| `compete` | Triggers when researching competitive or professional positioning: market intelligence, engineer brands, profiles, and content strategy. Research and strategy only — not code. |
| `voice` | Collecting user feedback via NPS surveys, review analysis, sentiment analysis, feedback classification, and insight extraction reports. Use when establishing feedback loops. |
| `field` | Conducting user research: interview guides, usability test plans, qualitative analysis, persona creation, journey mapping. Use when research design or analysis is needed; complements Echo. |
| `triage` | Responding to incidents: identifies impact scope, formulates recovery procedures, creates postmortems. Use when incident response or disaster recovery is needed. Delegates fixes to Builder. |
| `trail` | Investigating git history, analyzing regression root causes, and performing code archaeology. Time-travels through commits to uncover truth. Use for git history investigation. |
| `lens` | Comprehending and investigating codebases: structure mapping, feature discovery, data flow tracing for 'does X exist?' or 'how does Y work?'. Includes a conversational ask mode. Does not write code. |
| `trace` | Analyzing session replays, extracting persona-based behavioral patterns, and storytelling UX issues. Reads the 'why' from real user operation logs. Works with Field/Echo for persona validation. |
| `pdm` | Navigating delivery status read-only: reconciles planned scope (specs/roadmap/PRD) against implemented code for what's built vs left. Not for priority scoring (Rank) or AC conformance (Attest). |
| `omen` | Enumerating failure modes via pre-mortem analysis. Systematically identifies failure scenarios for plans, designs, and features, scoring them with RPN/AP. Does not write code. |

## Implementation (6 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `builder` | Implementing robust business logic, API integrations, data models, and reproducible AI image-generation code with type safety. Use for production implementation, Gemini image API pipelines, or interactive pair programming. |
| `forge` | Building rapid prototypes for frontend (UI components/pages) and backend (API mocks, simple servers). Use to validate new features or turn ideas into working demos. Working software over perfection. |
| `artisan` | Implementing production frontend code for React/Vue/Svelte: hooks design, state management, Server Components, form handling, data fetching. Converts Forge prototypes to production quality. |
| `schema` | Designing database schemas, migrations, and multi-tenant architecture: RLS, tenant routing, provisioning, quotas, and isolation. Not for query-plan tuning (Tuner). |
| `pixel` | Generating pixel-accurate HTML/CSS code from image mockups (PNG/JPG/screenshots) and performing visual verification for faithful reproduction. Use when mockup-to-code generation is needed. |
| `native` | Implementing production iOS/Android/macOS native features (SwiftUI, Compose) and iterating a screen against a reference design. Not for cross-platform RN/Flutter (Port) or web (Artisan). |

## Testing (3 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `radar` | Adding edge-case tests, repairing flaky tests, and improving coverage. Use when test gaps need filling or regressions need guarding. Supports JS/TS, Python, Go, Rust, and Java. |
| `voyager` | Authoring web and native E2E tests, including Playwright, Appium, XCUITest, device farms, visual regression, and App Store screenshot pipelines. Not for unit/load tests. |
| `siege` | Verifying system resilience via load testing, contract testing, chaos engineering, and mutation testing. Use for limit verification, non-functional testing, or reliability validation. |

## Security (7 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `sentinel` | Analyzing code statically for security flaws: hardcoded secrets, SQL injection, input validation, security headers, dependency CVEs. Not for runtime exploit checks (Probe) or code review (Judge). |
| `probe` | Integrating OWASP ZAP/Burp Suite/Nuclei, planning penetration tests, executing DAST, and scanning for vulnerabilities. For runtime vulnerability validation. Complements Sentinel static analysis. |
| `breach` | Designing red team attack scenarios, threat models, MITRE ATT&CK/OWASP application, Purple Team exercises, and AI/LLM red teaming. Use when adversarial security validation is needed. |
| `vigil` | Engineering detection rules (Sigma/YARA), detection coverage mapping, threat hunting hypotheses, Purple Team Blue side, Detection-as-Code CI/CD. Use when defensive verification is needed. |
| `cloak` | Engineering privacy and data governance: PII detection, data flow mapping, consent patterns, GDPR/CCPA-compliant implementation, DPIA. Use when privacy-by-design is needed. |
| `crypt` | Designing cryptographic architecture: algorithm selection, key management, E2EE, KMS integration, signature verification, TLS. Use when designing crypto protocols or key rotation flows. |
| `chain` | Auditing skill/plugin/MCP supply chains and live package compromise: manifests, hidden injection, IoC scans, persistence-first eradication, and gated credential rotation. Not for app SAST (Sentinel). |

## Review (6 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `judge` | Reviewing code via multi-engine orchestration (Claude + Codex) on three axes — secure, correct, and lean — shipping only findings worth fixing. Use for PR review or pre-commit. Complements Zen. |
| `zen` | Refactoring code: variable naming, function extraction, magic number constants, dead code removal. Does not change behavior. Not for bugs/security (Judge), tests (Radar), or features (Builder). |
| `sweep` | Detecting unnecessary files, unused code, and orphaned files, and proposing safe deletion. Not for removal execution (Builder), repo structure (Grove), or scope cutting (Void). |
| `attest` | Verifying spec compliance: extracts ACs from specs, adversarially checks conformance, generates BDD scenarios and traceability matrices. Use when impl must be proven to match a PRD/SRS/AC. |
| `canon` | Assessing standards, regulatory controls, and legal-document coverage with cited evidence and proposed wording. Use for OWASP/WCAG/SOC2/PCI/HIPAA or ToS/privacy/DPA reviews; not legal advice or code fixes. |
| `void` | Verifying YAGNI, cutting scope, and proposing complexity reductions. A 'subtraction' agent questioning the justification for every feature, dependency, doc, and config. Does not write code. |

## Performance (2 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `bolt` | Optimizing frontend (re-render, memoization, lazy loading) and backend (N+1, indexing, caching, async) performance, plus continuous auto-tuning loops for GC/threadpool/cache/worker settings. |
| `tuner` | Tuning database queries via EXPLAIN ANALYZE, query plan optimization, index recommendations, and slow query detection. Not for schema/migrations (Schema) or non-DB performance (Bolt). |

## Documentation (8 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `quill` | Adding JSDoc/TSDoc, updating READMEs, replacing any types with proper definitions, and adding high-value comments to complex logic. Use for documentation gaps or type safety. |
| `scribe` | Authoring standalone and cross-team specifications: PRD/SRS/HLD/LLD, staged L0-L4 unified packages, BDD acceptance criteria, and traceability. Use for technical or multi-audience documentation; not implementation or architecture decisions. |
| `canvas` | Visualizing code, specs, or context as Mermaid, ASCII, or draw.io diagrams: flowcharts, sequence/state/class/ER, Journey Maps, personas, coverage heatmaps. Use to reverse-document systems visually. |
| `prose` | Writing user-facing UX text including microcopy, error messages, voice and tone design, onboarding copy, and accessibility text. Use when UX writing or content strategy is needed. |
| `cue` | Writing and producing product videos: scripts, storyboards, narration, and reproducible Playwright demo recordings. Use for explainers, onboarding, feature walkthroughs, multi-aspect exports, captions, and video quality checks. |
| `tome` | Converting technical knowledge into durable learning documents and publishable articles. Use for diff-based teaching, decision records, onboarding, note/Zenn/Qiita/dev.to posts, article series, retrospectives, and cross-platform repurposing. |
| `stage` | Generating slides via Marp, reveal.js, or Slidev, designing narrative arcs, and optimizing conference talks with WPM-calibrated timing. Use when creating or pacing presentations. |
| `saga` | Designing narratives that tell product and feature use cases as customer-centric stories. Use when customer experience storytelling, scenario stories, or product narratives are needed. |

## Architecture (7 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `atlas` | Analyzing dependencies, circular references, and God Classes; authoring ADRs/RFCs. Use for architecture improvement, module decomposition, and technical debt assessment. |
| `gateway` | Designing and reviewing APIs: OpenAPI spec generation, versioning strategy, breaking change detection, REST/GraphQL best practices. Use for API design or OpenAPI specs. |
| `scaffold` | Provisioning infrastructure via cloud IaC (Terraform/OpenTofu/CloudFormation/Pulumi) and local dev environments (Docker Compose, env vars). Use for IaC design or multi-cloud provisioning. |
| `ripple` | Analyzing pre-change impact across vertical (dependency chains, files) and horizontal (pattern consistency, naming) dimensions. Use to estimate blast radius before a refactor. No code. |
| `grove` | Designing and auditing repository structure for humans and LLM agents: layouts, monorepos, docs/tests/scripts, progressive disclosure, prompt-cache topology, and safe migrations. |
| `weave` | Designing workflows and state machines. Use when state transition design, invalid transition detection, Saga patterns, or approval flow design is needed. |
| `seek` | Designing search engines and vector DBs for full-text, vector, and hybrid retrieval, including permission-aware retrieval for multi-tenant or per-role corpora. Use for search design, index optimization, the RAG retrieval layer, or deciding where ACL filtering belongs in the query path. |

## UX/Design (9 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `vision` | Directing UI/UX creative work — redesigns, new designs, trend application, Design System construction, Muse/Palette/Flow/Forge orchestration. Use for design direction. Offers a co-design pair mode. |
| `palette` | Improving usability, interaction quality, cognitive load reduction, feedback design, and a11y compliance. Use when improving UX usability or interaction feel. |
| `muse` | Defining and managing design tokens, applying token systems to existing codebases, building design system foundations. Use for spacing, color, typography, dark mode, cross-platform output. |
| `flow` | Implementing CSS/JS animations for hover effects, loading states, modal transitions, and gesture interactions. Use for meaningful motion, interaction feedback, or performance-safe animation. |
| `echo` | Simulating users to evaluate existing flows and generate synthetic demand: cognitive walkthroughs, feature requests, unmet needs, JTBD, and opportunity trees. Not real-user research. |
| `vitrine` | Authoring Storybook stories, component catalogs, and Visual Regression integration (CSF 3.0/Factories, Storybook 10 ESM-only, React Cosmos). Use when building a component catalog. |
| `frame` | Extracting and structuring design context from Figma via MCP Server for downstream implementation agents. Use for Figma-to-code bridging or Code Connect management. |
| `cast` | Casting personas: rapid generation from diverse inputs, registry-based persistence and lifecycle, data-driven evolution, inter-agent sync. Not for UI walkthroughs (Echo) or user research (Field). |
| `atelier` | Orchestrating design-to-implementation pipelines (code to visual to code closed loop), persisting a project design system across agents. Not for a single prototype (Forge) or direction only (Vision). |

## DevOps (4 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `gear` | Managing dependencies, CI/CD, advanced GitHub Actions workflows, containers, secrets, and operational config. Use for build, workflow, or environment work. |
| `launch` | Planning releases and reporting delivery work from GitHub PR history. Use when versioning, CHANGELOGs, rollout or rollback plans, engineering metrics, retrospectives, or stakeholder reports are needed. |
| `beacon` | Engineering observability and reliability: SLO/SLI design, distributed tracing, alerting, dashboards, capacity planning, toil automation, reliability review. Use for instrumentation or SLO definition. |
| `ledger` | Optimizing FinOps and cloud cost: IaC-based estimation, right-sizing, RI/SP recommendations, anomaly detection, budget alerts, AI/GPU workload economics. Use to forecast or cut cloud spend. |

## Modernization (3 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `polyglot` | Implementing i18n and l10n: extracts hardcoded strings to t() functions, integrates Intl API for date/currency/number formatting, manages translation keys, and adds RTL layout support. |
| `shift` | Orchestrating migrations, upgrades, and modernization across frameworks, libraries, APIs, databases, and dependencies. Generates codemods, applies Strangler Fig, verifies equivalence, plans rollback. |
| `port` | Designing web-to-iOS/Android porting strategy: feature parity matrices, native architecture maps, phased Strangler-Fig roadmaps. Not for same-language migration (Shift) or native impl (Native). |

## Growth (2 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `growth` | Optimizing SEO (meta/OGP/JSON-LD/headings), SMO (social sharing), CRO (CTA/form/exit-intent), and GEO (AI citation optimization). Use for search ranking, conversion, or AI visibility. |
| `funnel` | Constructing landing pages from a focused section to a premium multi-stage studio pipeline: structure, copy, conversion, responsive build, craft gates, and launch handoffs. Use when building or optimizing an LP, CTA, conversion flow, or premium launch surface. |

## Analytics (3 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `pulse` | Defining KPIs, tracking events, and dashboards: North Star Metric, funnel and cohort analysis, test-intelligence views. GA4/Amplitude/Mixpanel/PostHog. Use when metrics design is needed. |
| `experiment` | Designing A/B tests: hypothesis docs, sample size, feature flags, significance analysis, CUPED, SRM detection, switchback experiments. Use when hypothesis validation is needed. |
| `matrix` | Controlling combinatorial explosion across multi-dimensional axes: minimum coverage sets, execution plans, test/deploy/UX/risk prioritization. Use when scoping multi-axis combinations. |

## Git/PR (1 global skill)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `guardian` | Gatekeeping Git/PR by classifying change essence and recommending granularity, naming, and strategy. Use when PR preparation or commit strategy is needed. |

## Browser (1 global skill)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `vector` | Automating browsers via Playwright and Chrome DevTools for data collection, form interaction, screenshot capture, and network monitoring. Task completion focus (vs Voyager for E2E testing). |

## Data (1 global skill)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `stream` | Designing ETL/ELT pipelines, visualizing data flows, selecting batch/streaming approaches, and architecting Kafka/Airflow/dbt systems. Use when building data pipelines or managing data quality. |

## Strategy (2 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `magi` | Deliberating decisions and founder priorities through multi-perspective, named-expert, and YC-style advisory lenses. Use for verdicts, office hours, or expert critique; not implementation. |
| `rank` | Quantifying priority by scoring competing items with ICE/RICE/WSJF/MoSCoW/Cost of Delay/Kano. No code. Use to prioritize features/bugs/initiatives or arbitrate Must vs Should at MVP scoping. |

## Incident (1 global skill)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `mend` | Remediating known failure patterns automatically from Triage diagnoses and Beacon alerts: runbooks with safety-tier classification, staged verification, rollback. Use for automated remediation. |

## Meta / Tooling (6 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `sigil` | Designing a repository's project-local operating layer and generating its skills, recipes, workflows, and routing map. Not for global ecosystem agents (Architect) or runtime execution (Nexus). |
| `architect` | Designing new skill agents via gap analysis, overlap detection, SKILL.md + reference generation, and Nexus integration. Not for task orchestration (Nexus) or format-only audits (Gauge). |
| `gauge` | Auditing SKILL.md normalization and compliance: scans the 21-item checklist, classifies violations, produces fix snippets. Use when auditing SKILL.md compliance or ecosystem health. |
| `hone` | Auditing AI CLI configs and designing, configuring, or debugging Claude Code hooks. Use for Codex/agy/Claude Code config reviews, hook lifecycle automation, quality gates, or MCP governance. |
| `compass` | Navigating the skill ecosystem and guiding onboarding. Lists agents, recommends best fit for tasks. Don't use for task execution (Nexus), agent design (Architect). |
| `prune` | Cleaning up the skill ecosystem: auditing the agent roster for overlap and inactivity, proposing merges and sunset plans. Propose-only. Not for ecosystem strategy (Darwin) or code YAGNI (Void). |

## Creative / Media (1 global skill)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `ink` | Generating SVG icons/illustrations, designing icon systems, and constructing sprite symbols. Use when vector assets are needed. |

## AI / ML (3 global skills)

| Agent | Primary responsibility and triggers |
|-------|-------------------------------------|
| `chisel` | Converting a supplied prompt into an executable specification: detects vague quality/quantity/explanation/style/design/technical/judgment wording, role and persona theater, and self-contradiction, then replaces each with a numeric bound, an observable behavior, or a scorable criterion — with a per-term ledger of what changed and what stayed open. Don't use for AI system design, RAG, or eval harnesses (Oracle), PRD/SRS authoring (Scribe), spec conformance verification (Attest), or SKILL.md normalization (Gauge). |
| `oracle` | Designing and evaluating AI/ML systems: prompt engineering, RAG design, LLM application patterns, AI safety, evaluation frameworks, MLOps, cost optimization. Use for AI pipelines or eval harnesses. |
| `flux` | Refracting thinking by challenging assumptions, combining cross-domain knowledge, and shifting perspectives to reframe problems. Use for stuck situations or paradigm shifts. Does not write code. |

## Project-Local Extensions (3)

These extensions are available only when installed in the current project. Check `_common/PROJECT_LOCAL_SKILLS.md` before routing to them; its availability and fallback rules apply. They are not part of the global 90-skill roster.

| Extension | Primary responsibility and triggers |
|-----------|-------------------------------------|
| `darwin` | Orchestrating ecosystem self-evolution: lifecycle-phase detection, agent relevance, cross-agent knowledge synthesis, evolution proposals. Use when auditing skill-ecosystem health or fitness. |
| `lore` | Curating cross-agent knowledge and institutional memory: extracts patterns from agent journals into METAPATTERNS.md, detects knowledge decay, propagates best practices. Use for memory curation. |
| `orbit` | Running autonomous loops for nexus-autoloop. Generates script sets from goals, designs operation contracts, audits live loops, and recovers state — runners that complete reliably. |

## Category Selection Guide

For first-pass category choice, use `reference/agent-category-guide.md`. Return to this file when the exact roster inside the chosen category matters. Read the named skill before choosing its workflow or interpreting a secondary capability.
