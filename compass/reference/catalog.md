# Skill Agent Catalog

**Purpose:** Complete catalog of 90 global skills and 3 repository-local extensions with descriptions and triggers.
**Read when:** You need to look up agents by category, find agents for a specific task, or provide a full listing.

---

## How to Use This Catalog

- To find agents by category, browse the category sections below.
- To find agents by task, see `reference/patterns.md`.
- For the most accurate, up-to-date agent count and categories, verify against the repository directory structure.

---

## Orchestration (4 global)

Decomposes, coordinates, and parallelizes tasks.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Nexus** | Team orchestrator + product delivery | Multi-agent coordination and scope-adaptive product/MVP delivery (`deliver`) | No |
| **Sherpa** | Task decomposition guide | Break work into atomic steps under 15 minutes | No |
| **Rally** | Parallel orchestrator | Multi-session parallel execution | No |
| **Atelier** | Design → implementation pipeline | Integrates Vision → Muse/Frame → Forge → Artisan → Vitrine → Canvas | No |

## Investigation (8)

Investigation, analysis, and root-cause identification. Does not write code.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Scout** | Bug investigation / RCA | Diagnose bug causes, build reproduction steps | No |
| **Lens** | Codebase comprehension | Structure mapping, feature discovery, data-flow tracing | No |
| **Trail** | Git history investigation & legacy archaeology | Regression analysis, commit archaeology, implicit business-rule extraction (`static-rules`) | No |
| **Ripple** | Impact analysis | Pre-change risk evaluation, blast-radius estimation | No |
| **Sweep** | Dead-code detection | Unused files, dead code, orphaned files | No |
| **Spark** | New feature proposals | Feature ideas leveraging existing data/logic | No |
| **Void** | YAGNI verification | Scope cuts, complexity reduction proposals | No |
| **PDM** | Delivery-status navigator | Planned-vs-implemented reconciliation, feature inventory, roadmap rollup | No |

## Implementation (5)

Code implementation.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Builder** | Business-logic, CLI/TUI, and grammar implementation | API integrations, data models, image-generation APIs, CLI/TUI tools (`cli`), regex / parser / DSL (`grammar`) | Yes |
| **Artisan** | Frontend implementation | Production React/Vue/Svelte | Yes |
| **Forge** | Prototyping | Fast prototypes for both frontend and backend | Yes |
| **Native** | Pure-native mobile implementation | iOS Swift 6.3 + SwiftUI / Android Kotlin 2.4+ + Jetpack Compose (RN/Flutter/KMP/CMP out of scope) | Yes |
| **Pixel** | Mockup → code | Pixel-accurate HTML/CSS from images | Yes |

## Testing (5)

Test authoring and verification.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Radar** | Unit tests and test data | Edge cases, flaky-test repair, coverage, factories / fixtures / seeds (`fixtures`) | Yes |
| **Voyager** | Cross-platform + iOS E2E | Playwright/Cypress/Appium/Detox/Maestro and XCUITest/snapshots (`ios`) | Yes |
| **Siege** | Load and resilience testing | Load tests, contract tests, chaos engineering | Yes |
| **Matrix** | Manual QA test-case authoring | Systematic QA procedures (BVA, equivalence class, decision table) for TestRail/Zephyr/Xray/Qase — `qa-scenario` recipe (absorbed from drill) | No |
| **Canvas** | Test intelligence visualization | Coverage heatmaps, test-shape views, mutation overlays from junit/lcov/allure/playwright artifacts (absorbed from vista; live dashboards → Pulse) | Mixed |

## Security (5)

Security analysis and testing.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Sentinel** | Static security analysis | Hardcoded-secret detection, SQLi prevention, dependency CVEs | Mixed |
| **Breach** | Red team | Attack-scenario design, MITRE ATT&CK | No |
| **Probe** | Dynamic security testing | OWASP ZAP / Burp Suite, penetration testing | Mixed |
| **Crypt** | Cryptographic architecture | Algorithm selection, key management, E2EE, TLS configuration | Mixed |
| **Chain** *(optional: `incident-response`)* | Skill/plugin/MCP supply-chain audit and malware response | sha256 manifests, Unicode injection, IoC campaign scans, quarantine, eradication, and credential-rotation runbooks | Mixed |

## Review (6)

Code review and quality checks.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Judge** | Automated code review | PR review automation, bug detection | Mixed |
| **Zen** | Refactoring | Variable renaming, function extraction, dead-code removal | Mixed |
| **Canon** *(optional: `legal-jp`)* | Standards, regulatory, and legal-document compliance | OWASP/WCAG/OpenAPI, SOC2/PCI-DSS/HIPAA/ISO 27001, ToS/privacy/Tokushoho review | Mixed |
| **Gauge** | SKILL.md audit | 19-item checklist conformance | No |
| **Attest** | Spec-compliance verification | Acceptance-criteria extraction, BDD scenario generation | No |
| **Cloak** | Privacy engineering | PII detection, GDPR / CCPA compliance | Mixed |

## Performance (2)

Performance optimization.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Bolt** | Frontend / backend optimization & continuous auto-tuning | Re-render reduction, N+1 fixes, caching; profile→parameter→optimize→verify loops (absorbed from dial) | Yes |
| **Tuner** | DB optimization | EXPLAIN ANALYZE, index recommendations, slow queries | Yes |

## Documentation (5)

Documentation authoring, visualization, and article writing.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Scribe** | Technical and cross-team specifications | PRD/SRS/HLD/LLD, `cross-team` L0-L3 packages, document format conversion (`convert`) | No |
| **Quill** | Code documentation | JSDoc additions, README updates, fixing `any` types | Mixed |
| **Prose** | UX writing | Microcopy, error messages, voice and tone | No |
| **Tome** | Learning material and technical publications | Diff → tutorial conversion, design-decision records, articles for note / Zenn / Qiita / dev.to | No |
| **Canvas** | Diagramming and visualization | Mermaid / ASCII / draw.io for flow, sequence, ER diagrams | Mixed |

## Architecture (4)

System design and structure.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Atlas** | Architecture analysis | Dependency analysis, ADR / RFC authoring | Mixed |
| **Schema** | DB and tenant architecture | Normalization, migrations, ER diagrams, tenant isolation/RLS/routing (`tenant`) | Mixed |
| **Gateway** | API design and messaging integration | OpenAPI generation, versioning, chat adapters / webhooks / WebSocket (`messaging`) | Mixed |
| **Grove** | Human/LLM repository structure | Directory/docs layout plus LLM navigation and prompt-cache topology (`llm`) | Mixed |

## UX/Design (11)

UI/UX design and improvement.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Vision** | Creative direction | UI/UX direction decisions | No |
| **Palette** | Usability improvement | Cognitive-load reduction, a11y compliance | Mixed |
| **Echo** | Persona walkthrough + synthetic demand | Usability, feature requests, JTBD, 5 Whys, opportunity trees (`demand`) | No |
| **Flow** | Animation implementation | CSS / JS animation, transitions | Yes |
| **Muse** | Design tokens | Token architecture, dark mode | Mixed |
| **Vitrine** | Storybook | Story authoring, Visual Regression | Mixed |
| **Field** | User research | Interview design, persona creation | No |
| **Trace** | Session-replay analysis | Behavioral pattern extraction, UX issue discovery | No |
| **Cast** | Persona casting | Persona generation, management, sync | No |
| **Funnel** | Landing-page construction | LP conversion and premium nine-stage production (`premium`) | Mixed |
| **Voice** | User-feedback analysis | NPS design, review analysis, sentiment analysis | No |

## DevOps (5)

Infrastructure, CI/CD, and operations.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Gear** | Dependency management / CI/CD / GHA | Build errors, pipelines, advanced GitHub Actions (`gha`) | Yes |
| **Scaffold** | Infrastructure provisioning | Terraform / Docker Compose design | Yes |
| **Beacon** | Observability and reliability | SLO / SLI design, alert strategy | Mixed |
| **Launch** | Release management and PR reporting | Versioning, CHANGELOG, rollback, weekly/monthly reports and engineering metrics | Mixed |
| **Ledger** | FinOps | Cloud cost optimization, RI / SP recommendations | No |

## Modernization (2)

Migration and modernization.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Shift** | Migration, upgrade & modernization orchestrator | Framework / library / DB migration; deprecated-library detection (`detect`); native-API replacement (`modernize`); technology radar (`radar`) — absorbed from horizon | Mixed |
| **Port** | Web → Native porting design | Blueprint from Web SPA / SSR / PWA to iOS Swift/SwiftUI + Android Kotlin/Compose pure-native (parity matrix, phased roadmap) | No |

## Growth (1)

Growth tactics and branding.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Growth** | SEO / CRO / GEO and retention | Meta / OGP / JSON-LD, CTA optimization, re-engagement and loyalty design (`retention`) | Mixed |

## Analytics (3)

Metrics, experimentation, and combinatorial analysis.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Pulse** | KPI design | North Star Metric, funnel analysis | Mixed |
| **Experiment** | A/B test design | Hypothesis documentation, sample-size calculation | Mixed |
| **Matrix** | Combinatorial analysis | Combination-explosion control, minimum coverage | No |

## Git/PR (1)

Version-control workflow.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Guardian** | PR management | Change classification, granularity recommendations, strategy | No |

## Browser (1)

Browser automation and asset acquisition.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Vector** | Browser automation and crawl architecture | Task completion via Playwright / DevTools, crawler topology and frontier design (`crawl`) | Yes |

## Data (1)

Data pipelines and conversion.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Stream** | ETL / ELT pipelines | Kafka / Airflow / dbt design | Mixed |

## Strategy (2)

Business strategy and decision-making. Does not write code.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Compete** | Competitive research and personal branding | Feature matrices, product positioning, GitHub / LinkedIn / blog / conference positioning | No |
| **Rank** | Prioritization | ICE / RICE / WSJF / MoSCoW scoring | No |

## Incident (2)

Incident response.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Triage** | Incident first response | Impact identification, recovery procedure, postmortem | No |
| **Mend** | Automated remediation | Runbook execution, staged verification, rollback | Mixed |

## Communication (1 agent + Scribe recipe)

Coordination and communication.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Scribe** (`cross-team`) | Spec alignment | Cross-team Business / Dev / Design specifications | No |

## Meta / Tooling (5 global)

Manages and evolves the ecosystem itself.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Architect** *(`skill-meta`)* | Skill design | New agent design, gap analysis | No |
| **Sigil** *(`skill-meta`)* | Project operating-layer design | Tailored skills plus recipe/workflow/routing-map blueprints (`blueprint`) | No |
| **Hone** *(optional: `ai-cli-admin`)* | AI CLI configuration, hooks, and personal environment | CLI audits, PreToolUse / PostToolUse / Stop hooks, dotfiles and shell/editor config (`env`), macOS AppleScript / JXA automation (`automate`) | Mixed |
| **Compass** | Skill navigator | Skill guidance, onboarding | No |
| **Prune** *(`skill-meta`)* | Skill ecosystem cleanup | Overlap audit, merge-candidate detection, sunset proposals | No |

## Creative / Media (1)

Media and creative generation.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Ink** | SVG icons | Icon systems, sprite construction | Yes |

## AI / ML (3)

AI design and thinking support.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Oracle** | AI / ML design | Prompt engineering, RAG design, evaluation | No |
| **Chisel** | Prompt → executable spec | Ambiguity detection, criterion translation, role decomposition; Nexus `SPECIFY` briefs | No |
| **Flux** | Thinking refraction and ideation | Assumption challenges, perspective shifts, multi-turn Expand / Propose / Evaluate / Subtract dialogue (`ideate`) | No |

## Other Specialists

Specialized skills that don't fit the categories above.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Polyglot** | i18n / l10n | Multilingual support, RTL handling | Mixed |
| **Weave** | Workflow and schedule design | State machines, Saga patterns, cron / timezone / business calendar / backfill (`schedule`) | Mixed |
| **Omen** | Pre-mortem analysis | Failure-scenario enumeration, RPN scoring | No |
| **Seek** | Search-engine design | Full-text search, vector search, RAG | Mixed |
| **Vigil** | Detection engineering | Sigma / YARA rule design | Mixed |
| **Magi** | Multi-perspective deliberation, advisory, and strategy simulation | Architecture arbitration, Go / No-Go, founder coaching, named-figure lenses, business scenario simulation (`simulate`) | No |
| **Saga** | Narrative design | Customer-experience storytelling | No |
| **Cue** | Video script and demo production | Product videos, storyboards, Playwright-generated demos | Mixed |
| **Stage** | Slide generation | Marp / reveal.js / Slidev | Mixed |
| **Frame** | Figma → code bridge | Design context extraction | No |

## Project-local extensions (3)

Available only inside this repository. Check `_common/PROJECT_LOCAL_SKILLS.md` before routing; use its fallback when unavailable.

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Orbit** | Autonomous-loop design | Script generation for this repository's `nexus-autoloop` | Mixed |
| **Lore** | Knowledge curation | `.agents/*.md` synthesis into `METAPATTERNS.md` | No |
| **Darwin** | Ecosystem evolution | Fitness evaluation persisted to `.agents/ECOSYSTEM.md` | No |
