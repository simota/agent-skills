# Skill Agent Catalog

**Purpose:** Complete catalog of all skill agents with descriptions and triggers.
**Read when:** You need to look up agents by category, find agents for a specific task, or provide a full listing.

---

## How to Use This Catalog

- To find agents by category, browse the category sections below.
- To find agents by task, see `references/patterns.md`.
- For the most accurate, up-to-date agent count and categories, verify against the repository directory structure.

---

## Orchestration (6)

Decomposes, coordinates, and parallelizes tasks.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Nexus** | Team orchestrator | Complex tasks requiring multi-agent coordination | No |
| **Sherpa** | Task decomposition guide | Break work into atomic steps under 15 minutes | No |
| **Titan** | Product delivery | Ship code fastest, prefer build over plan | No |
| **Rally** | Parallel orchestrator | Multi-session parallel execution | No |
| **Aether** | AITuber orchestrator | Building AI VTuber systems | No |
| **Atelier** | Design → implementation pipeline | Integrates Vision → Muse/Frame → Forge → Artisan → Showcase → Canvas | No |

## Investigation (9)

Investigation, analysis, and root-cause identification. Does not write code.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Scout** | Bug investigation / RCA | Diagnose bug causes, build reproduction steps | No |
| **Lens** | Codebase comprehension | Structure mapping, feature discovery, data-flow tracing | No |
| **Trail** | Git history investigation | Regression analysis, commit archaeology | No |
| **Fossil** | Legacy code archaeology | Extract implicit business rules, assess migration risk | No |
| **Ripple** | Impact analysis | Pre-change risk evaluation, blast-radius estimation | No |
| **Specter** | Concurrency issue detection | Race conditions, memory leaks, deadlocks | No |
| **Sweep** | Dead-code detection | Unused files, dead code, orphaned files | No |
| **Spark** | New feature proposals | Feature ideas leveraging existing data/logic | No |
| **Void** | YAGNI verification | Scope cuts, complexity reduction proposals | No |

## Implementation (6)

Code implementation.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Builder** | Business-logic implementation | Robust API integrations, data models | Yes |
| **Artisan** | Frontend implementation | Production React/Vue/Svelte | Yes |
| **Forge** | Prototyping | Fast prototypes for both frontend and backend | Yes |
| **Anvil** | CLI/TUI construction | Terminal UIs and CLI tools | Yes |
| **Native** | Pure-native mobile implementation | iOS Swift 6.3 + SwiftUI / Android Kotlin 2.4+ + Jetpack Compose (RN/Flutter/KMP/CMP out of scope) | Yes |
| **Pixel** | Mockup → code | Pixel-accurate HTML/CSS from images | Yes |

## Testing (5)

Test authoring and verification.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Radar** | Unit tests | Edge-case additions, flaky-test repair, coverage improvement | Yes |
| **Voyager** | E2E tests | Playwright/Cypress configuration, Page Object design | Yes |
| **Siege** | Load and resilience testing | Load tests, contract tests, chaos engineering | Yes |
| **Drill** | Manual QA test-case authoring | Systematic test procedures (BVA, equivalence class, decision table) for TestRail/Zephyr/Xray/Qase | No |
| **Vista** | Test intelligence visualization | Coverage heatmaps, test-shape views, flake dashboards, mutation overlays from junit/lcov/allure/playwright artifacts | Mixed |

## Security (6)

Security analysis and testing.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Sentinel** | Static security analysis | Hardcoded-secret detection, SQLi prevention, dependency CVEs | Mixed |
| **Breach** | Red team | Attack-scenario design, MITRE ATT&CK | No |
| **Probe** | Dynamic security testing | OWASP ZAP / Burp Suite, penetration testing | Mixed |
| **Crypt** | Cryptographic architecture | Algorithm selection, key management, E2EE, TLS configuration | Mixed |
| **Chain** | Skill/plugin/MCP supply-chain audit | sha256 manifests, Unicode Tag injection scan, credential-exfiltration detection, MCP tool-description rug-pull prevention | Mixed |
| **Husk** | Supply-chain malware infection scanner | IoC-based local scan for npm/PyPI worm campaigns; eradication and credential rotation runbooks | Mixed |

## Review (7)

Code review and quality checks.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Judge** | Automated code review | PR review automation, bug detection | Mixed |
| **Zen** | Refactoring | Variable renaming, function extraction, dead-code removal | Mixed |
| **Canon** | Standards-compliance check | OWASP / WCAG / OpenAPI conformance evaluation | No |
| **Gauge** | SKILL.md audit | 16-item checklist conformance | No |
| **Attest** | Spec-compliance verification | Acceptance-criteria extraction, BDD scenario generation | No |
| **Warden** | UX quality gate | V.A.I.R.E. evaluation, scorecard | No |
| **Cloak** | Privacy engineering | PII detection, GDPR / CCPA compliance | Mixed |

## Performance (3)

Performance optimization.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Bolt** | Frontend / backend optimization | Re-render reduction, N+1 fixes, caching | Yes |
| **Tuner** | DB optimization | EXPLAIN ANALYZE, index recommendations, slow queries | Yes |
| **Dial** | Continuous auto-tuning | profile→parameter→optimize→verify loop for GC/threadpool/pool/cache/worker settings | Mixed |

## Documentation (6)

Documentation authoring, visualization, and article writing.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Scribe** | Technical specifications | PRD / SRS / HLD / LLD authoring | No |
| **Quill** | Code documentation | JSDoc additions, README updates, fixing `any` types | Mixed |
| **Prose** | UX writing | Microcopy, error messages, voice and tone | No |
| **Tome** | Learning material | Diff → tutorial conversion, design-decision records | No |
| **Canvas** | Diagramming and visualization | Mermaid / ASCII / draw.io for flow, sequence, ER diagrams | Mixed |
| **Zine** | Tech blog series | Articles for note / Zenn / Qiita / dev.to | No |

## Architecture (8)

System design and structure.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Atlas** | Architecture analysis | Dependency analysis, ADR / RFC authoring | Mixed |
| **Schema** | DB design | Normalization, indexing strategy, ER diagrams | Mixed |
| **Gateway** | API design | OpenAPI generation, versioning | Mixed |
| **Stratum** | C4 modeling | Structurizr DSL generation | Mixed |
| **Grove** | Repository structure | Directory design, docs/ layout | Mixed |
| **Nest** | LLM-optimized folder structure | Agent-friendly directory optimization | Mixed |
| **Shard** | Multi-tenant design | Tenant isolation, RLS, scale design | Mixed |
| **Grok** | Grammar / parser / DSL design | Regex, PEG / ANTLR, ReDoS-safe grammar design | Mixed |

## UX/Design (11)

UI/UX design and improvement.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Vision** | Creative direction | UI/UX direction decisions | No |
| **Palette** | Usability improvement | Cognitive-load reduction, a11y compliance | Mixed |
| **Echo** | Persona cognitive walkthrough | Usability evaluation, confusion-point discovery | No |
| **Flow** | Animation implementation | CSS / JS animation, transitions | Yes |
| **Muse** | Design tokens | Token architecture, dark mode | Mixed |
| **Showcase** | Storybook | Story authoring, Visual Regression | Mixed |
| **Researcher** | User research | Interview design, persona creation | No |
| **Trace** | Session-replay analysis | Behavioral pattern extraction, UX issue discovery | No |
| **Cast** | Persona casting | Persona generation, management, sync | No |
| **Funnel** | Landing-page construction | LP design and optimization | Mixed |
| **Voice** | User-feedback analysis | NPS design, review analysis, sentiment analysis | No |

## DevOps (7)

Infrastructure, CI/CD, and operations.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Gear** | Dependency management / CI/CD | Build errors, dev-environment issues | Yes |
| **Scaffold** | Infrastructure provisioning | Terraform / Docker Compose design | Yes |
| **Pipe** | GitHub Actions | Workflow design, security hardening | Yes |
| **Beacon** | Observability and reliability | SLO / SLI design, alert strategy | Mixed |
| **Launch** | Release management | Versioning, CHANGELOG, rollback | Mixed |
| **Comply** | Compliance | SOC2 / PCI-DSS / HIPAA conformance checks | Mixed |
| **Ledger** | FinOps | Cloud cost optimization, RI / SP recommendations | No |

## Modernization (3)

Migration and modernization.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Shift** | Migration orchestrator | Framework / library / DB migration | Mixed |
| **Horizon** | Tech-stack refresh | Deprecated-library detection, native-API replacement | Mixed |
| **Port** | Web → Native porting design | Blueprint from Web SPA / SSR / PWA to iOS Swift/SwiftUI + Android Kotlin/Compose pure-native (parity matrix, phased roadmap) | No |

## Growth (3)

Growth tactics and branding.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Growth** | SEO / CRO / GEO | Meta / OGP / JSON-LD, CTA optimization | Mixed |
| **Retain** | Retention | Re-engagement, churn prevention | Mixed |
| **Crest** | Engineer branding | GitHub / LinkedIn / blog / conference positioning | No |

## Analytics (3)

Metrics, experimentation, and combinatorial analysis.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Pulse** | KPI design | North Star Metric, funnel analysis | Mixed |
| **Experiment** | A/B test design | Hypothesis documentation, sample-size calculation | Mixed |
| **Matrix** | Combinatorial analysis | Combination-explosion control, minimum coverage | No |

## Git/PR (2)

Version-control workflow.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Guardian** | PR management | Change classification, granularity recommendations, strategy | No |
| **Harvest** | PR data collection / reporting | Weekly / monthly reports, release notes | No |

## Browser (3)

Browser automation and asset acquisition.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Navigator** | Browser automation | Task completion via Playwright / DevTools | Yes |
| **Spider** | Crawl architecture | Distributed crawler, politeness design | No |
| **Haul** | Product image acquisition | SKU / JAN / UPC matching, multi-source aggregation, perceptual-hash dedup, license verification | Yes |

## Data (2)

Data pipelines and conversion.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Stream** | ETL / ELT pipelines | Kafka / Airflow / dbt design | Mixed |
| **Morph** | Document conversion | Markdown / Word / Excel / PDF / HTML conversion | Mixed |

## Strategy (5)

Business strategy and decision-making. Does not write code.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Helm** | Business strategy | SWOT / PESTLE / Porter analysis | No |
| **Compete** | Competitive research | Feature matrices, positioning | No |
| **Rank** | Prioritization | ICE / RICE / WSJF / MoSCoW scoring | No |
| **Levy** | Japanese tax-filing guide | Income classification, deduction optimization, filing procedure | No |
| **Sage** | YC-style office-hours advisory | "Tell me what you're avoiding." Single-bottleneck extraction, founder anti-pattern detection, 1-2 week SMART action extraction | No |

## Incident (2)

Incident response.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Triage** | Incident first response | Impact identification, recovery procedure, postmortem | No |
| **Mend** | Automated remediation | Runbook execution, staged verification, rollback | Mixed |

## Communication (2)

Coordination and communication.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Relay** | Messaging integration | Bot development, webhooks, WebSocket | Mixed |
| **Accord** | Spec alignment | Cross-team Business / Dev / Design specifications | No |

## Meta / Tooling (8)

Manages and evolves the ecosystem itself.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Architect** | Skill design | New agent design, gap analysis | No |
| **Sigil** | Project-specific skill generation | Codebase analysis → tailored skill generation | No |
| **Lore** | Knowledge curation | Pattern extraction, knowledge-decay detection | No |
| **Darwin** | Ecosystem evolution | Lifecycle detection, fitness evaluation | No |
| **Hone** | AI CLI configuration optimization | Claude Code / Antigravity CLI configuration audit | No |
| **Realm** | Ecosystem visualization | Gamification, interactive maps | Yes |
| **Compass** | Skill navigator | Skill guidance, onboarding | No |
| **Latch** | Claude Code Hooks design | PreToolUse / PostToolUse / Stop and other lifecycle hooks | Mixed |

## Creative / Media (6)

Media and creative generation.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Dot** | Pixel art | SVG / Canvas / Phaser 3 pixel art | Yes |
| **Ink** | SVG icons | Icon systems, sprite construction | Yes |
| **Tone** | Game audio | SFX / BGM / voice / ambient | Yes |
| **Sketch** | AI image generation | Text → image via Gemini API | Yes |
| **Clay** | AI 3D generation | Text / image → 3D model | Yes |
| **Lyric** | Lyric writing | Lyrics and metatags for Suno AI | No |

## AI / ML (3)

AI design and thinking support.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Oracle** | AI / ML design | Prompt engineering, RAG design, evaluation | No |
| **Flux** | Thinking refraction | Assumption challenges, perspective shifts | No |
| **Prism** | NotebookLM optimization | Steering-prompt design | No |

## Other Specialists

Specialized skills that don't fit the categories above.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Riff** | Brainstorming | Iterative idea deepening through dialogue | No |
| **Plea** | Synthetic-user advocate | Generates feature requests as a fictional user | No |
| **Polyglot** | i18n / l10n | Multilingual support, RTL handling | Mixed |
| **Weave** | Workflow design | State machines, Saga patterns | Mixed |
| **Omen** | Pre-mortem analysis | Failure-scenario enumeration, RPN scoring | No |
| **Seek** | Search-engine design | Full-text search, vector search, RAG | Mixed |
| **Vigil** | Detection engineering | Sigma / YARA rule design | Mixed |
| **Magi** | Multi-perspective deliberation | Architecture arbitration, Go / No-Go | No |
| **Saga** | Narrative design | Customer-experience storytelling | No |
| **Cue** | Video script | Product videos, storyboards | No |
| **Director** | Demo-video production | Demos generated from Playwright E2E | Mixed |
| **Reel** | Terminal recording | CLI demo GIFs / videos | Mixed |
| **Stage** | Slide generation | Marp / reveal.js / Slidev | Mixed |
| **Loom** | Figma Make preparation | Figma Make Guidelines.md generation | No |
| **Frame** | Figma → code bridge | Design context extraction | No |
| **Clause** | Legal-document review | Terms of service, privacy policy | No |
| **Quest** | Game planning | GDD, balance design, economy design | No |
| **Orbit** | Autonomous-loop design | Script generation for nexus-autoloop | Mixed |
| **Arena** | Multi-AI comparison | Codex / Antigravity CLI compete or collaborate | Mixed |
| **Hearth** | Dotfile management | zsh / tmux / neovim / ghostty configuration | Mixed |
| **Mint** | Test-data generation | Factories, boundary values, seed management | Mixed |
| **Tempo** | Schedule design | cron, timezone / DST, retry / backoff, business calendars | Mixed |
| **Dawn** | Daily idea proposal | One personal-project idea per invocation as an 8-section brief for morning / daily / weekend hacks | No |
| **Hex** | Technical-debt visualization | Debt detection, severity scoring, gamified anthropomorphization (T1 Veil → T5 Calamity) + exorcism roadmap | Mixed |
| **Lure** | Premium LP studio orchestrator | Full 9-stage LP pipeline (Discover→Audience→Strategy→Structure→Design→Build→Optimize→Verify→Launch) across existing agents | Mixed |
