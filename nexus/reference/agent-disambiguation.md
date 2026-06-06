# Agent Disambiguation Guide

**Purpose:** Decision rules for choosing between overlapping agents.
**Read when:** Two or more agents plausibly fit the request.

## Contents
- High Priority — Frequently Confused Pairs
- Medium Priority — Sometimes Confused Pairs
- Low Priority — Rarely Confused
- Small Project Optimization

When multiple agents appear to fit a task, use these decision rules for correct routing.

---

## High Priority — Frequently Confused Pairs

### Gear vs Pipe (DevOps / CI/CD)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Fix CI", "speed up build", "update dependencies" | **Gear** | Maintenance of existing pipelines |
| "Design new workflow", "reusable workflow", "security hardening for GHA" | **Pipe** | New GHA architecture or advanced patterns |
| "Add caching to CI" | **Gear** | Optimization of existing pipeline |
| "Matrix strategy", "composite action design", "OIDC setup" | **Pipe** | Advanced GHA-specific features |
| Docker optimization, local dev setup | **Gear** | Not GHA-specific |
| Observability/alerting setup | **Gear** + Beacon | Infrastructure concern |

**Rule of thumb**: Existing pipeline maintenance → Gear. New GHA workflow design or advanced GHA features → Pipe.

---

### Cast vs Echo vs Field (Persona / User Research)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Create personas", "persona registry", "sync personas across agents" | **Cast** | Persona lifecycle management |
| "Test this UI as a beginner", "walk through this flow" | **Echo** | Persona-based UI simulation |
| "Design interview guide", "usability test plan", "journey mapping" | **Field** | Research methodology design |
| "Update persona with new data" | **Cast** | Persona evolution |
| "What would a mobile user think of this?" | **Echo** | Persona simulation |
| "Analyze survey results" | **Voice** | Feedback data analysis (not persona) |

**Rule of thumb**: Manage/store/evolve personas → Cast. Simulate personas on UI → Echo. Design research methodology → Field.

**Chain pattern**: Cast (create) → Field (validate with methodology) → Echo (simulate on UI)

---

### Lore vs Darwin (Ecosystem Meta)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "What patterns have agents learned?", "cross-agent insights" | **Lore** | Knowledge synthesis and extraction |
| "Is the ecosystem healthy?", "which agents are underused?" | **Darwin** | Ecosystem fitness evaluation |
| "Best practices from past incidents" | **Lore** | Pattern catalog from postmortems |
| "Should we deprecate this agent?", "evolution proposal" | **Darwin** | Lifecycle and evolution decisions |
| "Are there contradicting learnings across agents?" | **Lore** | Contradiction detection |
| "Agent relevance scoring", "ecosystem fitness score" | **Darwin** | Quantitative fitness metrics |

**Rule of thumb**: "What have we learned?" → Lore. "How fit is the ecosystem?" → Darwin. Lore feeds knowledge TO Darwin for evolution decisions.

**Chain pattern**: Lore (synthesize) → Darwin (evaluate) → Architect (improve/create)

---

### Sigil vs Architect (Skill/Agent Creation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Create a new ecosystem agent" | **Architect** | Permanent agent in `~/.claude/skills/` |
| "Generate project-specific skills" | **Sigil** | Ephemeral skills in `.claude/skills/` or `.agents/skills/` |
| "Design SKILL.md (400+ lines) with references" | **Architect** | Full agent design framework |
| "Analyze this project and create shortcuts" | **Sigil** | Project context → lightweight skills |
| "Ecosystem gap analysis" | **Architect** | Ecosystem-level concern |
| "Improve this agent's SKILL.md" | **Architect** | Agent enhancement |

**Rule of thumb**: Ecosystem-wide permanent agent → Architect. Project-specific lightweight skill → Sigil.

---

### Triage vs Mend (Incident Response)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Incident happening", "service down", "what's the severity?" | **Triage** | Diagnosis and assessment needed |
| "Auto-fix", "remediate known issue", "apply runbook" | **Mend** | Known pattern auto-fix |
| Triage diagnosis → known pattern match | **Mend** | Automated remediation of diagnosed issue |
| Triage diagnosis → no pattern match | **Builder** | Manual code fix needed |
| "Postmortem", "incident report" | **Triage** | Documentation and learning |
| "Why did the fix fail?", "rollback needed" | **Mend** → Triage | Mend handles rollback, Triage re-evaluates |

**Rule of thumb**: "What's wrong?" → Triage. "Fix this known problem" → Mend. "Write a code fix" → Builder.

**Chain pattern**: Triage (diagnose) → Mend (auto-fix known) OR Builder (fix unknown) → Radar (verify)

---

### Sentinel vs Breach vs Probe vs Vigil (Security)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Static scan", "find hardcoded secrets", "dependency CVE" | **Sentinel** | Static code analysis |
| "Penetration test", "DAST", "runtime vulnerability" | **Probe** | Dynamic testing against running app |
| "Red team exercise", "attack scenario", "threat model" | **Breach** | Offensive security assessment |
| "Sigma rules", "detection engineering", "threat hunting" | **Vigil** | Defensive detection rules |
| "Security audit" (broad) | **Sentinel** first | Start static, expand as needed |
| "MITRE ATT&CK mapping" | **Breach** (attack) / **Vigil** (detect) | Offense vs defense perspective |
| "Purple team" | **Breach → Vigil** | Attack then validate detection |

**Rule of thumb**: "Find vulnerabilities in code" → Sentinel. "Test running app" → Probe. "Simulate attacks" → Breach. "Build detection rules" → Vigil.

**Chain pattern**: Sentinel (static) → Probe (dynamic) → Breach (red-team) → Vigil (detection) → Builder (fix)

---

### Flux vs Magi (Thinking Support)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "We're stuck", "reframe", "think differently" | **Flux** | Perspective shift, break assumptions |
| "Compare options", "tradeoff analysis", "Go/No-Go" | **Magi** | Structured multi-perspective evaluation |
| "Why are we doing this?" "Question the premise" | **Flux** | Challenge fundamental assumptions |
| "Architecture A vs B vs C" | **Magi** | Weighted criteria comparison |
| "First principles analysis" | **Flux** | Decompose to fundamentals |
| "3-perspective review (logic/empathy/pragmatism)" | **Magi** | V.A.I.R.E.-style evaluation |
| Problem is well-defined, options are clear | **Magi** | Decision among known options |
| Problem is ill-defined or framing seems wrong | **Flux** | Redefine the problem itself |

**Rule of thumb**: "Which option?" → Magi. "Are we asking the right question?" → Flux. Flux reframes; Magi decides.

**Chain pattern**: Flux (reframe) → Magi (decide) → Builder (implement)

---

### Flux vs Riff vs Magi (Thinking Support Trio)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Reframe this", "shift perspective", single-shot analysis | **Flux** | One-time perspective shift |
| "Bounce ideas", "brainstorm with me", "壁打ち", iterative dialogue | **Riff** | Multi-turn interactive exploration |
| "Which should we pick?", "Go/No-Go", verdict needed | **Magi** | Structured decision with vote |
| User wants to explore before knowing what to decide | **Riff** | Open-ended exploration first |
| User is stuck and needs a new frame, not a conversation | **Flux** | Break the frame, then move on |
| User has options and needs a verdict, not more ideas | **Magi** | Converge and decide |

**Rule of thumb**: "Help me think about this" → Riff. "Help me see this differently" → Flux. "Help me decide" → Magi.

**Chain patterns**:
- Flux (reframe) → Riff (explore the new frame) → Magi (decide) → Builder (implement)
- Riff (brainstorm) → Spark (formalize as spec) → Builder (implement)
- Riff (brainstorm) → Void (cut scope) → Builder (implement)

---

### Spark vs Dawn (Idea Generation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Propose a feature for our product", existing data/users/workflows in context | **Spark** | Feature proposal grounded in existing product |
| "今日のアイデア", "週末ハック", "副業プロジェクト案", no existing product context | **Dawn** | Zero-start personal side-project idea |
| "Add X to the app" (existing app) | **Spark** | Product feature proposal |
| "What should I build this weekend?" | **Dawn** | Greenfield personal hack |
| "RICE score this", "JTBD analysis", "OST" | **Spark** | Product discovery frameworks |
| "One idea a day", "every morning give me one" | **Dawn** | Daily ritual, 1-invocation = 1-idea |
| "Coding-agent-ready prompt for a personal project" | **Dawn** | Section 8 implementation prompt |
| Input has product metrics, personas, feedback | **Spark** | Context-bound proposal |
| Input is just "give me something fun to build" | **Dawn** | Context-free ideation |

**Rule of thumb**: Existing product context → Spark. Zero-start personal hack → Dawn. Spark produces RFCs with RICE/JTBD; Dawn produces 8-section side-project briefs with a ready-to-paste agent prompt.

**Chain patterns**:
- Dawn (daily idea) → Forge (prototype) → Builder (production) → Radar (tests)
- Dawn (daily idea) → Zine (article-ify for a skill/tech blog series)
- Spark (feature proposal) → Scribe (formal spec) → Builder (implement)

---

### Pixel vs Artisan vs Forge (UI Implementation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Implement this mockup/screenshot exactly" | **Pixel** | Pixel-faithful reproduction from image |
| "Build this React component" (from spec) | **Artisan** | Production-quality frontend code |
| "Quick prototype to validate idea" | **Forge** | Speed over fidelity |
| "Match this design 1:1" (image provided) | **Pixel** | Visual fidelity is primary goal |
| "Match this Figma design" (Figma URL) | **Frame → Artisan** | Structured design handoff |
| "Responsive landing page from screenshot" | **Pixel** | Image-to-code with responsive adaptation |

**Rule of thumb**: Image input → Pixel. Spec/Figma input → Artisan. Idea validation → Forge.

---

## Medium Priority — Sometimes Confused Pairs

### Artisan vs Forge (Frontend Implementation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Prototype this quickly", "just make it work" | **Forge** | Speed over quality |
| "Production-ready component", "hooks design", "state management" | **Artisan** | Production quality |
| "Validate idea with working demo" | **Forge** | Proof of concept |
| "Convert prototype to production" | **Forge → Artisan** | Standard handoff |
| "Build this React component" (no existing prototype) | **Artisan** | Direct production build |
| Backend mock/API stub | **Forge** | Backend prototyping |

**Rule of thumb**: Uncertain requirements or exploration → Forge first. Clear requirements → Artisan directly. Never use both if requirements are already clear.

---

### Atlas vs Ripple (Architecture Analysis)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Analyze dependencies", "find God Classes", "circular references" | **Atlas** | Current architecture evaluation |
| "What's the impact of changing X?", "is this change safe?" | **Ripple** | Pre-change impact assessment |
| "Create ADR", "architecture decision" | **Atlas** → Magi | Architecture documentation |
| "Should we proceed with this refactor?" | **Ripple** | Risk evaluation before action |
| "Module decomposition strategy" | **Atlas** | Structural analysis |
| "Will renaming this break anything?" | **Ripple** | Change impact |

**Rule of thumb**: "What IS the architecture?" → Atlas. "What HAPPENS IF we change it?" → Ripple.

---

### Scout vs Lens (Code Investigation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Why is X broken?", "find the bug" | **Scout** | Bug-driven investigation |
| "How does X work?", "explain this module" | **Lens** | Comprehension-driven exploration |
| "What caused this regression?" | **Trail** → Scout | Git history then RCA |
| "Does feature X exist?", "where is X implemented?" | **Lens** | Code exploration |
| "Reproduce this error" | **Scout** | Bug reproduction |
| "Map the data flow for X" | **Lens** → Canvas | Understanding then visualization |

**Rule of thumb**: Broken behavior → Scout. Understanding behavior → Lens.

---

### Voice vs Field (User Insights)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Analyze app store reviews", "NPS survey", "sentiment analysis" | **Voice** | Quantitative feedback analysis |
| "Design interview questions", "usability test plan" | **Field** | Research methodology |
| "What are users saying about X?" | **Voice** | Existing feedback collection |
| "What do users NEED from X?" | **Field** | Deep user understanding |
| "Create feedback collection system" | **Voice** | Feedback infrastructure |
| "Create journey map" | **Field** | User experience mapping |

**Rule of thumb**: Collect/analyze existing feedback → Voice. Design new research → Field.

---

### Palette vs Flow (UI Interaction)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Improve usability", "reduce cognitive load", "a11y" | **Palette** | UX quality improvement |
| "Add hover animation", "loading transition", "modal animation" | **Flow** | CSS/JS animation implementation |
| "This button feels unresponsive" | **Palette** | Interaction quality |
| "Animate this page transition" | **Flow** | Motion design |
| "Micro-interaction design" | **Palette** (simple) / **Flow** (complex) | Complexity determines agent |

**Rule of thumb**: UX/usability concern → Palette. Animation implementation → Flow.

---

### Prose vs Palette (Content & UX)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Write error messages", "improve button labels" | **Prose** | Content creation |
| "Evaluate UX quality", "audit interaction patterns" | **Palette** | UX assessment |
| "Onboarding copy", "voice & tone guide" | **Prose** | Content strategy |
| "Form feels confusing" | **Palette** (assess) → Prose (rewrite) | Assessment then content |

**Rule of thumb**: Write/rewrite text → Prose. Evaluate/improve interaction → Palette.

---

### Void vs Zen vs Sweep (Necessity / Quality / Cleanup)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Do we need this?" "YAGNI" "over-engineering" | **Void** | Evaluates whether the thing should exist at all, including non-code assets |
| "Refactor" "improve the code" "make it more readable" | **Zen** | Improves code quality |
| "Dead code" "unused files" | **Sweep** | Physically detects unused code/files |
| "Do we need this process?" "too many meetings" | **Void** | Evaluates whether the process is justified |
| "This document is outdated" | **Void** (evaluate) → Sweep (remove) | Validate the document's necessity, then remove it if warranted |

**Rule of thumb**: "Is it necessary?" → Void. "Is it clean?" → Zen. "Is it being used?" → Sweep.

### Grove vs Nest (Repository Structure / LLM-Optimized Folders)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Repository structure", "directory layout", "monorepo design" | **Grove** | Human developer conventions and CI/CD paths |
| "Optimize folders for LLM", "context cost", "CLAUDE.md hierarchy" | **Nest** | LLM navigation efficiency and cache topology |
| "Agents can't find files", "token budget too high" | **Nest** | LLM-specific discovery and cost optimization |
| "Project organization", "team conventions" | **Grove** | Developer workflow optimization |

**Rule of thumb**: Human developer experience → Grove. LLM/AI tool navigation efficiency → Nest.

---

## Low Priority — Rarely Confused

### Attest vs Judge

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Does this match the spec?", "verify against requirements" | **Attest** | Specification compliance verification |
| "Review this PR", "find bugs", "code quality check" | **Judge** | Code quality and bug detection |
| "BDD scenarios from spec", "acceptance criteria" | **Attest** | Spec-driven scenario generation |
| "Check for security vulnerabilities", "logic errors" | **Judge** | Code-level issue detection |
| Specification document provided as input | **Attest** | Requires spec as source of truth |
| No specification, just code diff | **Judge** | Code review doesn't need spec |

**Rule**: "Does code match spec?" → Attest. "Is code well-written?" → Judge. Attest requires spec input; Judge works on code alone.

### Attest vs Radar

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Generate BDD scenarios from spec" | **Attest** | Scenario generation from spec |
| "Write tests for this function" | **Radar** | Test implementation |
| "Spec traceability matrix" | **Attest** | Spec ↔ code ↔ test mapping |
| "Increase coverage to 80%" | **Radar** | Coverage improvement |
| "Are all acceptance criteria implemented?" | **Attest** | Spec compliance check |
| "Add edge case tests" | **Radar** | Test code writing |

**Rule**: "Are requirements met?" → Attest. "Are tests written?" → Radar. Attest generates BDD scenarios; Radar implements them as test code.

**Chain pattern**: Attest (generate BDD) → Radar (implement tests) → Voyager (E2E from acceptance scenarios)

### Attest vs Warden

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Verify implementation against spec" | **Attest** | Spec compliance |
| "Pre-release quality review" | **Warden** | UX quality gate |
| "Acceptance criteria check" | **Attest** | Criterion-by-criterion verification |
| "V.A.I.R.E. assessment" | **Warden** | UX framework evaluation |
| "Traceability matrix" | **Attest** | Spec ↔ implementation mapping |
| "Pass/fail for release" | **Warden** (after Attest) | Release decision |

**Rule**: "Does code match spec?" → Attest. "Is UX quality sufficient?" → Warden. Use both for complete release gates: Attest (spec compliance) → Warden (UX quality) → Launch.

### Judge vs Zen

**Rule**: "Find problems" → Judge. "Fix code smells" → Zen. Judge discovers, Zen fixes.

### Sentinel vs Probe

**Rule**: Static code scan → Sentinel. Running app penetration test → Probe.

### Quill vs Scribe

**Rule**: Code documentation (JSDoc, README) → Quill. Specification documents (PRD, SRS) → Scribe.

### Helm vs Compete

**Rule**: Business strategy simulation → Helm. Competitive intelligence gathering → Compete. Compete output feeds into Helm input.

### Titan vs Nexus

**Rule**: "Build a product from scratch" → Titan. "Execute this task chain" → Nexus. Titan issues chains TO Nexus.

---

### Fossil vs Lens vs Shift (Legacy / Migration)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Extract business rules from legacy code" | **Trail** `static-rules` | Rule archaeology (absorbed from fossil) |
| "How does this module work?" | **Lens** | Code comprehension |
| "Migrate from framework A to B" | **Shift** `framework` | Migration execution |
| "What are the hidden rules before we migrate?" | **Trail** `static-rules` → Shift | Archaeology then migration |
| "Modernize tech stack" | **Shift** `detect`/`modernize` | Stack-level refresh (absorbed from horizon) |

**Rule of thumb**: "What rules are buried?" → Trail `static-rules`. "How does it work?" → Lens. "Migrate it" → Shift `framework`/`lang`. "Refresh the stack" → Shift `detect`/`modernize`/`radar`.

---

### Cloak vs Oath vs Crypt (Privacy / Compliance / Crypto)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Find PII exposure", "GDPR audit" | **Cloak** | Privacy-focused |
| "SOC2 readiness", "HIPAA controls" | **Oath** | Framework compliance |
| "Encryption design", "key management" | **Crypt** | Cryptographic architecture |
| "Security audit" (broad) | **Sentinel** first | Start with static analysis |

**Rule of thumb**: PII/consent/privacy → Cloak. Regulatory frameworks → Oath. Crypto algorithms/keys → Crypt.

---

### Seek vs Oracle (Search / AI)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Design search index", "Elasticsearch mapping" | **Seek** | Search infrastructure |
| "RAG retrieval layer" | **Seek** (retrieval) + Oracle (LLM) | Split by concern |
| "Prompt engineering", "LLM evaluation" | **Oracle** | AI/ML design |
| "Vector DB selection" | **Seek** | Search engine expertise |

**Rule of thumb**: Search infra → Seek. AI/LLM patterns → Oracle. RAG spans both.

---

### Shard vs Schema (Multi-tenant / DB Design)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Tenant isolation strategy" | **Shard** | Multi-tenant architecture |
| "Database normalization", "ER diagram" | **Schema** | Schema design |
| "RLS policies for tenants" | **Shard** | Tenant-specific policies |
| "Add a new table/column" | **Schema** | Regular schema change |

**Rule of thumb**: Multi-tenant concerns → Shard. General DB design → Schema.

---

### Funnel vs Growth vs Artisan (Landing Page / Marketing)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Design high-converting landing page" | **Funnel** | LP structure & conversion |
| "Improve SEO/CRO across site" | **Growth** | Site-wide optimization |
| "Build React component for LP" | **Artisan** | Frontend implementation |
| "A/B test LP variants" | **Funnel** (design) + Experiment (test) | Split by concern |

**Rule of thumb**: LP structure/conversion → Funnel. SEO/CRO tactics → Growth. Frontend code → Artisan.

---

### Weave vs Builder (Workflow / Implementation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Design state machine", "workflow transitions" | **Weave** | Architecture design |
| "Implement the workflow in code" | **Builder** | Code implementation |
| "Saga pattern for distributed transactions" | **Weave** | Pattern design |
| "Temporal/Step Functions setup" | **Weave** (design) + Builder (impl) | Split by phase |

**Rule of thumb**: "Design the workflow" → Weave. "Build it" → Builder.

---

### Zine vs Scribe vs Prose vs Saga vs Tome (Writing Agents)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Tech blog post for note/Zenn/Qiita/dev.to" | **Zine** | External long-form article |
| "PRD, spec, design document, SRS" | **Scribe** | Internal technical documentation |
| "Error message, button label, UX microcopy" | **Prose** | User-facing short-form text |
| "Customer story, use-case narrative for marketing" | **Saga** | Product narrative |
| "Auto-generate learning doc from git diff" | **Tome** | Diff-driven teaching material |
| "Tutorial / retrospective / announcement article" | **Zine** | External article regardless of topic |
| "Internal README explaining the module" | **Quill** | Code-adjacent docs (not Zine) |
| "Multi-episode series with index article" | **Zine** | Series management is first-class in Zine |
| "Retrospective as a Tome learning doc vs a Zine post" | **Tome** (internal) / **Zine** (external) | Destination audience decides |

**Rule of thumb**: External public article → Zine. Internal spec/doc → Scribe. UI text → Prose. Product story → Saga. Diff → learning doc → Tome.

---

### Tempo vs Weave vs Launch vs Orbit (Scheduling / Time / Flow)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Design cron expression", "timezone/DST handling" | **Tempo** | Temporal logic design |
| "Retry/backoff policy", "idempotency key design" | **Tempo** | Time-related resilience |
| "State machine with retries" | **Tempo** (policy) + Weave (FSM) | Split: Tempo owns timing, Weave owns states |
| "Release scheduling, feature flag rollout" | **Launch** | One-time release events |
| "Autonomous AI loop runner (nexus-autoloop)" | **Orbit** | Script-driven AI loops |
| "Business calendar (JP holidays, fiscal year, banking days)" | **Tempo** | Calendar-as-code |
| "GitHub Actions cron tuning" | **Tempo** (design) + Gear/Pipe (impl) | Tempo picks pattern, Gear/Pipe configures |
| "Backfill missed runs after incident" | **Triage** → **Tempo** (replay plan) → Builder | Tempo designs idempotent replay |

**Rule of thumb**: Recurring time logic → Tempo. State machine → Weave. Release event → Launch. AI agent loop → Orbit.

---

### Grok vs Builder vs Gateway vs Schema (Grammar / API / Data Design)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Design grammar (EBNF/ABNF/PEG)", "parser-generator choice" | **Grok** | Grammar / parser layer |
| "ReDoS-safe regex", "catastrophic backtracking audit" | **Grok** | Regex security design |
| "Internal DSL (fluent API, template literal, YAML-embedded)" | **Grok** | DSL architecture |
| "AST transformation, Babel plugin, jscodeshift, codemod" | **Grok** | AST design / transform |
| "REST/GraphQL API design, OpenAPI spec" | **Gateway** | HTTP API contract |
| "Database schema, migration, ER diagram" | **Schema** | Persistence schema |
| "General business logic implementation" | **Builder** | General implementation |
| "Log parsing with grok patterns (Logstash)" | **Grok** | Pattern engine migration/design |
| "Static security scan of shipped regex" | **Sentinel** | Post-ship audit, not design |
| "Fuzz testing against a parser" | **Radar** | Test execution, not grammar design |

**Rule of thumb**: Textual grammar/pattern/DSL → Grok. HTTP API → Gateway. DB schema → Schema. General impl → Builder. Grok designs; Sentinel audits; Radar tests.

---

### Port vs Native vs Shift (Mobile Migration & Implementation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Web app を iOS / Android にネイティブ移植したい" | **Port** | Web → pure-native blueprint |
| "feature parity matrix between web and mobile" | **Port** | Parity verdicts (Full/Adapted/Deferred/Dropped) |
| "ネイティブアーキテクチャ設計（SwiftUI / Compose）" | **Port** | Per-platform architecture mapping |
| "Strangler Fig phased migration roadmap (web → mobile)" | **Port** | Phased rollout & store-submission timeline |
| "Pure-native vs KMP vs CMP vs RN vs Flutter trade-off" | **Port** | Cross-platform decision support |
| "iOS Swift / SwiftUI を実装したい" | **Native** | Pure-native iOS implementation |
| "Android Kotlin / Jetpack Compose を実装したい" | **Native** | Pure-native Android implementation |
| "Liquid Glass / Material 3 Expressive 採用" | **Native** | iOS 26 / Android 16 modern surfaces |
| "Privacy Manifest / Data Safety を仕上げたい" | **Native** → Cloak | Implementation then privacy review |
| "Passkey / Credential Manager を組み込みたい" | **Native** → Crypt | Implementation then crypto review |
| "TestFlight phased release / Play staged rollout" | **Native** → Launch | Implementation then release planning |
| "React Native / Flutter / KMP / CMP で実装したい" | **out of scope** | Native は対象外。Forge でプロトタイプ可、本番は外部実装 |
| "framework / library / DB の version migration（同一言語内）" | **Shift** `framework`/`lang` | Same-language migration orchestrator |
| "deprecated library 検出と native API 置換" | **Shift** `detect`/`modernize` | Modernization scan (absorbed from horizon) |
| "legacy web business rule 抽出（移植前）" | **Trail** `static-rules` | Read-only archaeology (absorbed from fossil) |

**Rule of thumb**: Web→Native の **設計図** → Port。**実装** → Native。同一言語の移行 → Shift `framework`/`lang`。非推奨検出 → Shift `detect`/`modernize`。Native は React Native / Flutter / KMP / CMP は受けない。

---

### Haul vs Vector vs Trawl vs Sketch (Image / Asset Acquisition)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "商品画像を SKU / JAN / UPC で集めたい" | **Haul** | Identifier-driven product image acquisition |
| "EC サイト / ブランドサイトから商品画像取得" | **Haul** | Multi-source product imagery aggregation |
| "catalog images with provenance & license" | **Haul** | License-aware curation |
| "perceptual hash で重複排除した画像セット" | **Haul** | Cross-source pHash dedup |
| "reverse image search → canonical product URL" | **Haul** (reverse recipe) | Sample image → product canonical |
| "license / provenance audit (no new fetch)" | **Haul** (audit recipe) | Audit-only mode |
| "ログインが必要な保護サイトから画像取得" | **Vector** → **Haul** | Auth handoff then download |
| "1K+ URL/day, 100+ ドメインのフリート規模クロール設計" | **Trawl** | Architecture only |
| "汎用ブラウザ自動化、フォーム入力、スクショ取得" | **Vector** | Generic browser tasks |
| "テキストから画像を生成したい (text-to-image)" | **Sketch** | AI image generation |
| "モックアップから HTML/CSS を再現したい" | **Pixel** | Mockup-to-code |
| "アイコン / SVG イラスト" | **Ink** | Vector asset generation |

**Rule of thumb**: 商品画像の取得 → Haul。汎用ブラウザ → Vector。フリート規模アーキ → Trawl。AI 生成 → Sketch。Haul は license_class 必須、unknown は配信不可。

---

### Sage vs Riff vs Magi vs Helm vs Spark vs Flux (Founder Decisions & Ideation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "office hours" / "I'm stuck" / "what should I focus on" | **Sage** | YC 流アドバイザリー、ボトルネック1点抽出 |
| "founder advisory" / "creative direction reality check" | **Sage** | パターンマッチ + 創業者アンチパターン検出 |
| "review my pitch" / "Demo Day deck" / "投資家向け Q&A 練習" | **Sage** (pitch recipe) | STRUCTURE → CLARITY → TENSION → RESONANCE → REVISE |
| "we just shipped X / hired Y / pivoted Z, postmortem" | **Sage** (retro recipe) | 直近の意思決定/結果の振り返り |
| "we're stuck right now, need to unblock" | **Sage** (triage recipe) | 5 ターン以内の緊急アンブロック |
| "アイデアを出したい、発散したい" | **Riff** | Iterative divergent ideation (4 modes) |
| "新機能を提案して、Markdown spec で" | **Spark** | Feature proposals from existing data/logic |
| "GO / NO-GO の意思決定、複数の選択肢から選びたい" | **Magi** | 三項審議 (Logos/Pathos/Sophia) |
| "四半期 / 年次のシナリオシミュレーション、KPI forecast" | **Helm** | Long-term strategy simulation |
| "前提を疑いたい、視点をずらしたい" | **Flux** | Single-shot reframing |
| "1-3 日で作れる個人プロジェクト案" | **Dawn** | Daily personal idea ritual |

**Rule of thumb**: 1 週間で動かす1つのアクションが欲しい → Sage。発散 → Riff。三項審議 → Magi。長期シナリオ → Helm。機能仕様 → Spark。前提反転 → Flux。Sage は idea を **作らず**、創業者が "避けていること" を言わせる。

---

## Small Project Optimization

For S/M scope projects, skip agents that add overhead without proportional value:

| Skip | Use Instead | When |
|------|-------------|------|
| Vision | Palette/Muse directly | No full UX redesign needed |
| Forge | Artisan directly | Requirements are clear |
| Cast | Echo standalone | Simple persona needs |
| Pipe | Gear | Basic CI/CD only |
| Compete | Skip entirely | Internal tools, no competitors |
| Scribe | Skip entirely | S scope, no formal specs needed |
| Field | Echo directly | No formal research methodology needed |
