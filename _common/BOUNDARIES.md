# Agent Boundaries (Master Reference)

Centralized responsibility boundaries for the entire agent ecosystem. Individual SKILL.md files reference this document instead of maintaining their own Agent Boundaries tables.

For disambiguation of commonly confused agent pairs, see `nexus/reference/agent-disambiguation.md`.

---

## Meta-Orchestration

| Agent | Primary Role | Scope | Writes Code |
|-------|-------------|-------|-------------|
| **Nexus** | Task chain orchestration & execution | Single task chain | Never |
| **Titan** | Product lifecycle delivery (9 phases) | Full product (multi-phase) | Never |
| **Sherpa** | Task decomposition & workflow guidance | Single epic/story → atomic steps | Never |
| **Rally** | Parallel multi-session execution | Concurrent independent tasks | Never |
| **Darwin** | Ecosystem self-evolution | Cross-agent, systemic | Never |
| **Sigil** | Project-specific skill generation | Per-project lightweight skills | SKILL.md only |
| **Architect** | Ecosystem agent design | Permanent agent creation | SKILL.md only |
| **Lore** | Cross-agent knowledge synthesis | Ecosystem-wide pattern extraction & propagation | Never |
| **Gauge** | SKILL.md normalization audit & self-evolution | Per-skill format compliance | Never |

**Key distinctions:**
- Titan issues chains → Nexus executes them → Rally parallelizes when needed
- Sherpa decomposes → Nexus/Rally executes the decomposed steps
- Architect creates permanent ecosystem agents; Sigil creates project-specific skills
- Darwin evaluates ecosystem fitness; Lore curates cross-agent knowledge patterns
- Gauge audits existing SKILL.md format compliance; Architect creates/improves agent packages

## Investigation & Analysis

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Scout** | Bug investigation & root cause analysis | "Why is it broken?" | Never |
| **Lens** | Codebase understanding & exploration | "How does it work?" | Never |
| **Trail** | Git history investigation & regression analysis | "When did it break?" | Never |
| **Triage** | Incident response & recovery planning | "What's the severity? How to recover?" | Never |
| **Ripple** | Pre-change impact analysis | "What happens if we change X?" | Never |
| **Atlas** | Architecture analysis & ADR creation | "What IS the architecture?" | Never |
| **Sweep** | Dead code & unused file detection | "What can we remove?" | Never |
| **Fossil** | Legacy code archaeology | Business rule extraction, migration risk | Never |

**Key distinctions:**
- Broken behavior → Scout. Understanding behavior → Lens. Git history → Trail
- Current architecture → Atlas. Change impact → Ripple
- Incident diagnosis → Triage. Known-pattern auto-fix → Mend. Unknown fix → Builder
- Bug root cause → Scout. Incident severity → Triage
- Legacy system rule extraction → Fossil. Migration execution → Shift

## Security

| Agent | Primary Role | Method | Writes Code |
|-------|-------------|--------|-------------|
| **Sentinel** | Static security analysis | Code scan, CVE check, secret detection | Fixes only |
| **Probe** | Dynamic security testing | OWASP ZAP, penetration testing | Never |
| **Specter** | Concurrency & resource issue detection | Race conditions, memory/resource leaks | Never |
| **Breach** | Red team engineering & threat modeling | STRIDE/PASTA/MITRE ATT&CK, attack simulation | Never |
| **Vigil** | Detection engineering | Sigma/YARA rules, threat hunting, MITRE coverage | Never |
| **Cloak** | Privacy engineering | PII detection, GDPR/CCPA, consent, DPIA | Yes (privacy patterns) |
| **Oath** | Regulatory compliance audit | SOC2/PCI-DSS/HIPAA/ISO 27001, policy-as-code | Yes (OPA policies) |
| **Crypt** | Cryptographic architecture | Algorithm selection, key management, E2EE, post-quantum | Never |
| **Clause** | Legal document review | ToS, privacy policy, tokushoho, clause gap detection | Never |

**Key distinctions:**
- Static code scan → Sentinel. Running app test → Probe. Concurrency → Specter
- Attack simulation → Breach. Detection rules → Vigil. Purple team → Breach → Vigil
- PII/privacy → Cloak. Regulatory frameworks → Oath. Crypto design → Crypt
- Legal document review → Clause. Privacy implementation → Cloak. Regulatory audit → Oath

**Credential Isolation Principle** (Source: Anthropic Managed Agents):
Tokens and secrets must never be reachable from the execution environment where agent-generated code runs. Two patterns:
- **Resource-Bundled Auth**: Use credentials during environment setup (e.g., git clone), then remove access before agent code executes
- **Vault + Proxy**: Store credentials in an external vault; agent calls tools via a proxy that injects credentials — the agent itself never handles tokens

## Implementation

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Builder** | Production backend/logic implementation | Business logic, API, data models | Yes |
| **Artisan** | Production frontend implementation | React/Vue/Svelte, hooks, state | Yes |
| **Forge** | Rapid prototyping (full-stack) | Speed over quality, PoC | Yes |
| **Schema** | Database schema design & migration | Data modeling, normalization | Yes |
| **Anvil** | CLI/TUI development | Terminal interfaces, dev tools | Yes |
| **Arena** | Multi-engine competitive/collaborative development | Codex/Antigravity CLI comparison | Yes |
| **Pixel** | Mockup-to-code faithful reproduction | Image→HTML/CSS with visual verification | Yes |

**Key distinctions:**
- Backend logic → Builder. Frontend → Artisan. Prototyping → Forge → then Artisan/Builder
- Clear requirements → Artisan directly. Exploration needed → Forge first
- Image mockup → Pixel. Figma design → Frame → Artisan. Spec → Artisan directly

## Testing & Quality

| Agent | Primary Role | Scope | Writes Code |
|-------|-------------|-------|-------------|
| **Mint** | Test data & fixture generation | Factory patterns, seed data, PII masking | Yes |
| **Radar** | Unit/integration tests, edge cases, coverage | Test code | Yes |
| **Voyager** | E2E test specialist (Playwright/Cypress) | E2E test infrastructure | Yes |
| **Siege** | Load testing, chaos engineering, resilience | Non-functional testing | Yes |
| **Judge** | Code review & bug detection | PR review, quality check | Never |
| **Zen** | Refactoring & code smell remediation | Readability improvement | Yes (refactor only) |
| **Warden** | V.A.I.R.E. UX quality gate | Pre-release assessment | Never |
| **Attest** | Specification compliance verification | Spec-to-code gap analysis | Never |

**Key distinctions:**
- Find problems → Judge. Fix code smells → Zen
- Unit tests → Radar. E2E tests → Voyager. Load tests → Siege
- Code quality → Judge. UX quality → Warden. Spec compliance → Attest

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
| **Scribe** | Specification documents | PRD, SRS, HLD, test specs | Never |
| **Accord** | Cross-team integrated spec packages | L0-L3 progressive refinement | Never |
| **Canvas** | Visualization | Mermaid diagrams, ASCII art, draw.io | Yes (diagrams) |
| **Morph** | Format conversion | Markdown ↔ Word/Excel/PDF/HTML | Yes (scripts) |
| **Prism** | NotebookLM steering | Audio/Video quality prompts | Never |

| **Saga** | Narrative design & product storytelling | SB7/Pixar/Hero's Journey/JTBD frameworks | Never |
| **Cue** | Video script & storyboard design | Demo/explainer/tutorial scripts, narration | Never |
| **Tome** | Learning document generation from changes | Diffs→teaching materials, decision records | Never |
| **Stage** | Presentation slide generation | Marp/reveal.js/Slidev, speaker notes | Yes (slide markdown) |

**Key distinctions:**
- Code docs (JSDoc, README) → Quill. Spec docs (PRD, SRS) → Scribe. Cross-team specs → Accord. Diagrams → Canvas
- Product narratives/stories → Saga. Video scripts → Cue. Learning docs from code → Tome. Slides → Stage

## Architecture & Structure

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Atlas** | Architecture analysis & decisions | Dependencies, God Class, ADR/RFC | Never |
| **Gateway** | API design & review | OpenAPI, versioning, breaking changes | Yes (specs) |
| **Scaffold** | Infrastructure provisioning | Terraform, Docker, IaC | Yes |
| **Grove** | Repository structure design | Directory layout, conventions | Never |
| **Nest** | LLM-optimized folder structure | Context efficiency, cache topology, progressive disclosure | Never |
| **Shift** | Migration, upgrade & modernization orchestration | Codemod generation, framework/DB/API migration, deprecated library detection, native API replacement, technology radar (absorbed from horizon) | Yes |
| **Trawl** | Crawl system architecture design | URL frontier, distributed crawl, politeness policy, compliance | Never |

**Key distinctions:**
- General repo structure → Grove. LLM-optimized folder structure → Nest. Grove designs for developers; Nest optimizes for LLM navigation
- Crawl system architecture → Trawl. Single-session scraping execution → Vector
- Crawl output pipeline → Stream. Crawl infrastructure provisioning → Scaffold

## UX & Design

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Vision** | Creative direction & design strategy | Design system, redesign, trends | Never |
| **Muse** | Design token management | Color, spacing, typography tokens | Yes |
| **Palette** | Usability improvement | Cognitive load, a11y, interaction quality | Yes |
| **Flow** | Animation & motion | CSS/JS transitions, micro-interactions | Yes |
| **Echo** | Persona-based UI testing | Walk through as user type | Never |
| **Prose** | UX writing | Microcopy, error messages, voice & tone | Yes (text) |
| **Vitrine** | Storybook catalog management | Component documentation, visual regression | Yes |
| **Trace** | Session replay analysis | Behavioral patterns from logs | Never |
| **Director** | Demo video production | Playwright-based recordings | Yes |
| **Reel** | Terminal recording | CLI demo GIF/video | Yes |
| **Frame** | Figma MCP design context extraction | Figma→code bridge, Code Connect | Never |
| **Loom** | Figma Make optimization | Guidelines.md generation, prompt strategy, output validation | Never |
| **Ink** | SVG icon & illustration generation | Grid systems, sprite symbols, a11y | Yes (SVG) |
| **Funnel** | Landing page structure & conversion | AIDA/PAS, CTA, form optimization | Yes |

**Key distinctions:**
- Design direction → Vision. Tokens → Muse. Usability → Palette. Animation → Flow
- Write text → Prose. Test as persona → Echo. Research → Field
- Figma data extraction → Frame. Token definition → Muse. Frame extracts, Muse defines
- Figma Make optimization → Loom. Figma extraction → Frame. Token management → Muse
- Code Connect mapping → Frame + Vitrine. Frame manages Figma side, Vitrine manages code side
- SVG icons/illustrations → Ink. Pixel art → Dot. AI images → Sketch
- Landing page design/conversion → Funnel. SEO/CRO tactics → Growth

## User Research & Personas

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Field** | Research methodology design | Interviews, usability tests, journey maps | Never |
| **Cast** | Persona lifecycle management | Create, store, evolve, sync personas | Never |
| **Echo** | Persona-based UI simulation | Walk through UI as specific persona | Never |
| **Voice** | Feedback collection & analysis | NPS, reviews, sentiment analysis | Yes (integrations) |

**Key distinctions:**
- Manage personas → Cast. Simulate on UI → Echo. Design research → Field. Analyze feedback → Voice

## Strategy & Business

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Spark** | Feature ideation & proposal | New feature specs from existing data | Never |
| **Growth** | SEO/SMO/CRO optimization | Search ranking, conversion, sharing | Yes |
| **Compete** | Competitive intelligence | SWOT, positioning, feature matrix | Never |
| **Bond** | Retention & engagement | Churn prevention, gamification | Never |
| **Experiment** | A/B testing & hypothesis validation | Feature flags, statistical significance | Yes |
| **Pulse** | KPI & metrics infrastructure | Tracking events, dashboards | Yes |
| **Stream** | Data pipeline design | ETL/ELT, Kafka, Airflow, dbt | Yes |
| **Helm** | Business strategy simulation | SWOT/PESTLE, scenario planning | Never |
| **Levy** | Tax filing guidance (Japan) | Income tax, deductions, e-Tax | Never |
| **Crest** | Engineer self-branding strategy | GitHub/blog/LinkedIn/talk positioning | Never |
| **Ledger** | Cloud FinOps & cost optimization | IaC cost estimation, right-sizing, RI/SP | Yes (policies) |

**Key distinctions:**
- Competitive intel → Compete. Business simulation → Helm. Compete feeds into Helm
- Feature ideas → Spark. Growth tactics → Growth. Metrics → Pulse
- Tax filing guidance → Levy. Levy advises on tax law; Builder implements calculation logic
- Cloud cost → Ledger. IaC provisioning → Scaffold. Monitoring → Beacon

## Decision & Intent

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Magi** | Multi-perspective decision making | Logic/Empathy/Pragmatism triad | Never |
| **Flux** | Thinking refraction & perspective shift | Cynefin, TRIZ, lateral thinking, assumption surfacing | Never |

**Key distinctions:**
- "Which option?" → Magi. "Are we asking the right question?" → Flux. Flux reframes; Magi decides

## DevOps & Release

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Gear** | Existing CI/CD maintenance | Dependencies, Docker, build optimization | Yes |
| **Pipe** | New GHA workflow design | Advanced GHA, reusable workflows | Yes |
| **Guardian** | Git/PR governance | Commit strategy, PR quality | Never |
| **Launch** | Release management | Versioning, CHANGELOG, rollback | Yes |
| **Harvest** | PR reporting | Weekly/monthly reports from git data | Never |
| **Latch** | Claude Code hooks | PreToolUse/PostToolUse event system | Yes |
| **Hearth** | Dev environment setup | dotfiles, shell, editor config | Yes |
| **Hone** | AI CLI config audit & optimization | config.toml, settings.json, CLAUDE.md, AGENTS.md, GEMINI.md, rules, MCP, permissions, commands, hooks, extensions | Never |
| **Mend** | Known-pattern auto-remediation | Runtime fix, runbook execution, staged verification | Yes |

**Key distinctions:**
- Existing CI maintenance → Gear. New GHA design → Pipe
- PR strategy → Guardian. Release execution → Launch. PR reports → Harvest
- Operational config → Gear. Runtime remediation → Mend
- AI CLI config audit (Codex, Antigravity (`agy`), Claude Code) → Hone. Claude Code hooks design → Latch. Personal dev env (dotfiles) → Hearth

## Communication & Content

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Relay** | Messaging integration & bot development | WebSocket, webhooks, chat integrations | Yes |
| **Polyglot** | Internationalization (i18n/l10n) | Translations, locale formatting, RTL | Yes |

## Observability

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Beacon** | SRE & observability | SLO/SLI, tracing, alerting, dashboards | Yes |

## Specialized

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Oracle** | AI/ML design & evaluation | Prompts, RAG, LLM patterns, MLOps | Never |
| **Aether** | AITuber system orchestration | Live streaming pipeline, TTS, avatar | Yes |
| **Vector** | Browser automation | Playwright task execution | Yes |
| **Orbit** | Autonomous loop execution | Loop contracts, script generation | Yes |
| **Canon** | Standards compliance | OWASP, WCAG, OpenAPI, ISO 25010 | Never |
| **Matrix** | Combinatorial analysis | Multi-dimensional coverage optimization | Never |
| **Void** | YAGNI verification | Scope cutting, complexity reduction | Never |
| **Sketch** | AI image generation | Gemini API image creation | Yes |
| **Dot** | Pixel art code generation | SVG/Canvas/Phaser 3/Pillow/CSS sprites, tilesets, palettes + Antigravity CLI delegation | Yes |
| **Clay** | AI 3D model generation | Text-to-3D/Image-to-3D API code, Blender Python, Three.js, OpenSCAD, game pipeline (LOD/retopo/UV/QC) | Yes |
| **Tone** | Game audio generation | SFX/BGM/Voice/Ambient/UI audio generation code, LUFS normalization, ffmpeg processing, FMOD/Wwise/engine integration | Yes |
| **Quest** | Game planning & production | GDD, game balance, narrative, economy design | Never |
| **Realm** | Ecosystem gamification visualization | Phaser 3 office sim, XP/rank, interactive HTML map | Yes |
| **Omen** | Pre-mortem analysis & failure mode enumeration | FMEA, fault tree, Swiss Cheese, Murphy audit | Never |
| **Seek** | Search & vector DB architecture | Full-text/vector/hybrid search, RAG retrieval | Partial (mappings) |
| **Shard** | Multi-tenant architecture design | Tenant isolation, RLS, routing, noisy-neighbor | Partial (specs) |
| **Weave** | Workflow & state machine design | FSM/Statechart, Saga patterns, approval flows | Partial (YAML/specs) |
| **Lyric** | Songwriting for Suno AI | Lyrics with metatags, style prompts | Never |
| **Native** | Mobile development | React Native/Flutter/SwiftUI/Jetpack Compose | Yes |
| **Rank** | Priority quantification | ICE/RICE/WSJF/MoSCoW/Kano scoring | Never |

**Key distinctions:**
- Mobile app development → Native. Mobile-responsive frontend → Artisan
- Songwriting/lyrics → Lyric. Audio generation code → Tone
- Priority scoring → Rank. Multi-perspective decisions → Magi
- Pre-mortem / failure analysis → Omen. Change impact → Ripple. Incident response → Triage
