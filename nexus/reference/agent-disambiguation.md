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

### Gear modes (DevOps / CI/CD)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Fix CI", "speed up build", "update dependencies" | **Gear** | Maintenance of existing pipelines |
| "Design new workflow", "reusable workflow", "security hardening for GHA" | **Gear `gha`** | New GHA architecture or advanced patterns |
| "Add caching to CI" | **Gear** | Optimization of existing pipeline |
| "Matrix strategy", "composite action design", "OIDC setup" | **Gear `gha`** | Advanced GHA-specific features |
| Docker optimization, local dev setup | **Gear** | Not GHA-specific |
| Observability/alerting setup | **Gear** + Beacon | Infrastructure concern |

**Rule of thumb**: Existing provider-agnostic pipeline maintenance → Gear `ci`. New GitHub Actions workflow design or advanced GHA features → Gear `gha`.

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

Both are project-local extensions. Apply `_common/PROJECT_LOCAL_SKILLS.md` before routing; when unavailable, use `Tome`/`Scribe` for durable knowledge or `Prune` → `Architect` for ecosystem evaluation and improvement.

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

### Sigil vs Architect (Skill / Agent / Layer Creation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Create a new ecosystem agent" | **Architect** | Permanent agent in `~/.claude/skills/` |
| "Generate project-specific skills" | **Sigil** | Ephemeral skills in `.claude/skills/` or `.agents/skills/` |
| "Design SKILL.md (400+ lines) with references" | **Architect** | Full agent design framework |
| "Analyze this project and create shortcuts" | **Sigil** | Project context → lightweight skills |
| "Ecosystem gap analysis" | **Architect** | Ecosystem-level concern |
| "Improve this agent's SKILL.md" | **Architect** | Agent enhancement |
| "Design this repo's agents, recipes, AND workflows together" | **Sigil `blueprint`** | Project **operating layer** as one system before artifact authoring |
| "Author one project skill body" | **Sigil** | Single skill, not a coordinated suite |
| "What agent owns which repo task?" (project routing map) | **Sigil `blueprint`** | Project-local routing-map design (consumed by Nexus) |

**Rule of thumb**: Ecosystem-wide permanent agent → Architect. One project-specific artifact → Sigil authoring mode. A coordinated *set* of project agents/recipes/workflows → Sigil `blueprint`, with runtime registered in Nexus.

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

### Flux vs Magi (Thinking Support)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Reframe this", "shift perspective", single-shot analysis | **Flux[reframe]** | One-time perspective shift |
| "Bounce ideas", "brainstorm with me", "rubber-duck session", iterative dialogue | **Flux[ideate]** | Multi-turn interactive exploration |
| "Which should we pick?", "Go/No-Go", verdict needed | **Magi** | Structured decision with vote |
| **A real person is named** — "what would Feynman do here?", "critique this as Christensen would", "panel of Buffett + Munger on this" | **Magi[channel/conclave]** | Named-figure documented thinking as an advisory lens |
| User wants to explore before knowing what to decide | **Flux[ideate]** | Open-ended exploration first |
| User is stuck and needs a new frame, not a conversation | **Flux[reframe]** | Break the frame, then move on |
| User has options and needs a verdict, not more ideas | **Magi** | Converge and decide |
| User wants *a specific documented thinker's* frame, not any new frame | **Magi[advisor]** | Flux invents a frame; Magi applies a documented person's |

**Rule of thumb**: "Help me think about this" → Flux[ideate]. "Help me see this differently" → Flux[reframe]. "Help me decide" → Magi[decide]. **"Help me see this as _<named person>_" → Magi[advisor].**

**The named-figure Recipe boundary is a documented individual.** A real, *named* person → Magi[channel/conclave/critique]. A school/movement/collective, or no person at all → Flux. A synthetic user persona → Cast. A fixed founder-mentor archetype (no name) → Magi[advisor]. Named-figure Recipes produce a **reading, not a verdict** — every claim is tagged `ATTESTED` / `INFERRED` / `SPECULATIVE`; a requested decision continues to Magi[decide].

**Chain patterns**:
- Flux[reframe] (new frame) → Flux[ideate] (explore it) → Magi (decide) → Builder (implement)
- Flux[ideate] (brainstorm) → Spark (formalize as spec) → Builder (implement)
- Flux[ideate] (brainstorm) → Void (cut scope) → Builder (implement)
- **Magi[advisor] → Magi[decide] → Builder** — the canonical "expert lens for a decision" path
- **Flux[reframe] → Magi[advisor]** — reframe first, then borrow the mind that fits it
- **Magi[advisor] → Flux[ideate]** — expert mental models as ideation seeds

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

**Rule of thumb**: Uncertain requirements or exploration → Forge first ("just make it work", backend mock/API stub). Clear requirements ("hooks design", "state management", production-ready component) → Artisan directly. "Convert prototype to production" is the standard Forge → Artisan handoff; never use both if requirements are already clear.

---

### Atlas vs Ripple (Architecture Analysis)

**Rule of thumb**: "What IS the architecture?" → Atlas (dependency graphs, God Classes, module decomposition, "create ADR" → Magi). "What HAPPENS IF we change it?" → Ripple ("is this change safe?", "will renaming this break anything?").

---

### Scout vs Lens (Code Investigation)

**Rule of thumb**: Broken behavior → Scout ("find the bug", "reproduce this error"). Understanding behavior → Lens ("how does X work?", "does feature X exist?"). Regression root cause → Trail (history) → Scout (RCA); data-flow mapping → Lens → Canvas (visualize).

---

### Voice vs Field (User Insights)

**Rule of thumb**: Collect/analyze existing feedback → Voice ("NPS survey", "sentiment analysis", "what are users saying about X?", feedback collection systems). Design new research → Field ("usability test plan", "journey map", "what do users NEED from X?").

---

### Palette vs Flow (UI Interaction)

**Rule of thumb**: UX/usability concern → Palette ("reduce cognitive load", "a11y", "this button feels unresponsive"). Animation implementation → Flow ("hover animation", "loading transition", "animate this page transition"). Micro-interaction design: simple → Palette, complex → Flow.

---

### Prose vs Palette (Content & UX)

**Rule of thumb**: Write/rewrite text → Prose ("error messages", "button labels", "onboarding copy", "voice & tone guide"). Evaluate/improve interaction → Palette ("audit interaction patterns"). "Form feels confusing" → Palette (assess) → Prose (rewrite).

---

### Void vs Zen vs Sweep (Necessity / Quality / Cleanup)

**Rule of thumb**: "Is it necessary?" → Void ("YAGNI", "over-engineering", "do we need this process?" — includes non-code assets). "Is it clean?" → Zen ("make it more readable"). "Is it being used?" → Sweep ("dead code", "unused files"). An outdated document → Void (validate necessity) → Sweep (remove).

### Chisel vs Oracle vs Scribe vs Attest (Prompt Language / Prompt System / Spec / Conformance)

All four make requirements explicit; they differ by **what the object is** and **when in the lifecycle they act**.

| Route to | When the object is | Deliverable |
|----------|--------------------|-------------|
| **Chisel** | A **supplied prompt's wording** — "high quality", "concise", "modern", "as appropriate", "latest", "you are a world-class X" | Ambiguity ledger + rewritten prompt as an executable spec |
| **Oracle** | The **prompt system** around it — few-shot policy, structured output, versioning, eval gates, cost, RAG or agent architecture | AI design + eval/guardrail contracts |
| **Scribe** | A **document for people** — PRD / SRS / HLD / LLD | Specification document |
| **Attest** | A **finished artifact vs criteria that already exist** | Conformance verdict + traceability matrix |

**Rule of thumb**: Chisel changes the words of an instruction so a machine can execute and a third party can score it. Oracle decides what the instruction should be part of. Scribe writes for humans. Attest checks afterwards.

**Two traps:**
- **The user's own request being ambiguous is not a Chisel task.** That is the internal CLASSIFY GATE (`intent-clarification.md`). Chisel needs *supplied prompt text as an object*.
- **A bad output is not evidence of a vague prompt.** Run Oracle's five-layer triage (Instruction / Context / Capability / Tool / Evaluation) before routing to Chisel — retrieval and evaluator failures are routinely misdiagnosed as prompt failures.

Prompt text inside a `SKILL.md` splits the same way: the file's structure and normalization → `Gauge` / `Sigil` / `Architect`; the vague wording inside its instructions → Chisel.

---

### Grove modes (Repository Structure / LLM-Optimized Folders)

**Rule of thumb**: Human developer experience → Grove default modes ("directory layout", "monorepo design", "team conventions", CI/CD paths). LLM/AI tool navigation efficiency → Grove `llm` ("context cost", "CLAUDE.md hierarchy", "agents can't find files", "token budget too high").

---

### Magi vs Spark vs Echo[demand] (JTBD — Jobs-To-Be-Done)

Three skills hold full JTBD content, each applying it through a different lens — this is
intentional multi-lens coverage, not duplication. Route by *what the JTBD output feeds*.

**Rule of thumb**: strategy/competitive-set ("market/category strategy via JTBD", "disruption") →
Magi (`jobs-to-be-done.md`); feature targeting ("feature brief", "proposal hypothesis") → Spark
(`persona-jtbd.md`); demand/switch interview ("forces of progress for demand", "why users would
switch") → Echo `demand` (`demand-jtbd-switch-interview.md`). Value Proposition Canvas (jobs/pains/gains zoom-in)
lives in **Spark** (`value-proposition-canvas.md`) and pulls its jobs block from `persona-jtbd.md`.

---

### Magi vs Compete vs Spark (Market Sizing — TAM/SAM/SOM)

Three skills size markets, each for a different decision. Route by *the decision the number
informs*, not the acronym.

**Rule of thumb**: whole-business/entry strategy ("strategic market headroom", "entry scoring",
"portfolio sizing") → Magi (`market-sizing-strategy.md`); competitor-relative ("market size vs
competitors", "competitive TAM", "share capture") → Compete (`market-sizing.md`); per-feature
upside ("how much can this feature earn", "opportunity upper bound") → Spark (`opportunity-sizing.md`).

---

### Chain Modes (Malware / Supply-Chain)

**Rule of thumb**: "Is something already infected right now?" → Chain's malware-response Recipes. "Should we trust this before we let it in?" → Chain's intake/audit Recipes.

---

### Voyager modes (Mobile / Cross-Platform UI Testing)

**Rule of thumb**: Pure-iOS XCUITest/screenshot pipeline → Voyager `ios` ("accessibility-identifier query", "fastlane snapshot", "App Store screenshot pipeline"). Cross-platform E2E (Appium/Detox/Maestro/Playwright) → Voyager's platform modes.

---

### Vector vs Voyager (Browser Automation)

**Rule of thumb**: One-off browser task completion → Vector ("collect data", "fill this form", "capture a screenshot"). Durable regression E2E test authoring → Voyager ("write a regression E2E test", "durable test suite").

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

### Judge vs Zen

**Rule**: "Find problems" → Judge. "Fix code smells" → Zen. Judge discovers, Zen fixes.

### Sentinel vs Probe

**Rule**: Static code scan → Sentinel. Running app penetration test → Probe.

### Quill vs Scribe

**Rule**: Code documentation (JSDoc, README) → Quill. Specification documents (PRD, SRS) → Scribe.

### Magi vs Compete

**Rule**: Business strategy simulation → Magi. Competitive intelligence gathering → Compete. Compete output feeds into Magi input.

### Nexus build recipes

**Rule**: One bounded capability → Nexus `feature`. A product/MVP build whose chain must adapt to scope → Nexus `deliver`. A high-investment discovery-to-ship run → Nexus `apex`.

---

### Trail vs Lens vs Shift (Legacy / Migration)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Extract business rules from legacy code" | **Trail** `static-rules` | Rule archaeology (absorbed from fossil) |
| "How does this module work?" | **Lens** | Code comprehension |
| "Migrate from framework A to B" | **Shift** `framework` | Migration execution |
| "What are the hidden rules before we migrate?" | **Trail** `static-rules` → Shift | Archaeology then migration |
| "Modernize tech stack" | **Shift** `detect`/`modernize` | Stack-level refresh (absorbed from horizon) |

**Rule of thumb**: "What rules are buried?" → Trail `static-rules`. "How does it work?" → Lens. "Migrate it" → Shift `framework`/`lang`. "Refresh the stack" → Shift `detect`/`modernize`/`radar`.

---

### Cloak vs Canon[regulatory] vs Crypt (Privacy / Compliance / Crypto)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Find PII exposure", "GDPR audit" | **Cloak** | Privacy-focused |
| "SOC2 readiness", "HIPAA controls" | **Canon[regulatory]** | Framework compliance |
| "Encryption design", "key management" | **Crypt** | Cryptographic architecture |
| "Security audit" (broad) | **Sentinel** first | Start with static analysis |

**Rule of thumb**: PII/consent/privacy → Cloak. Regulatory frameworks → Canon[regulatory]. Crypto algorithms/keys → Crypt.

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

### Schema modes (Multi-tenant / DB Design)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Tenant isolation strategy" | **Schema `tenant`** | Multi-tenant architecture |
| "Database normalization", "ER diagram" | **Schema** | Schema design |
| "RLS policies for tenants" | **Schema `tenant`** | Tenant-specific policies |
| "Add a new table/column" | **Schema** | Regular schema change |

**Rule of thumb**: Multi-tenant concerns → Schema `tenant`. General DB design → Schema's schema/migration modes.

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

### Tome vs Scribe vs Prose vs Saga (Writing Agents)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Tech blog post for note/Zenn/Qiita/dev.to" | **Tome** | External long-form article |
| "PRD, spec, design document, SRS" | **Scribe** | Internal technical documentation |
| "Error message, button label, UX microcopy" | **Prose** | User-facing short-form text |
| "Customer story, use-case narrative for marketing" | **Saga** | Product narrative |
| "Auto-generate learning doc from git diff" | **Tome** | Diff-driven teaching material |
| "Tutorial / retrospective / announcement article" | **Tome** | External article regardless of topic |
| "Internal README explaining the module" | **Quill** | Code-adjacent docs (not Tome) |
| "Multi-episode series with index article" | **Tome** | Series management is first-class in Tome |
| "Retrospective as a learning doc or a public post" | **Tome** | Destination audience selects the Tome Recipe and format |

**Rule of thumb**: External public article → Tome. Internal spec/doc → Scribe. UI text → Prose. Product story → Saga. Diff → learning doc → Tome.

---

### Weave vs Launch vs Orbit (Scheduling / Time / Flow)

Orbit is project-local. Apply `_common/PROJECT_LOCAL_SKILLS.md`; when unavailable, use `Nexus[goal/apex]` for bounded execution or `Sherpa` for decomposition.

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Design cron expression", "timezone/DST handling" | **Weave[schedule]** | Temporal logic design |
| "Retry/backoff policy", "idempotency key design" | **Weave[retry]** | Time-related resilience |
| "State machine with retries" | **Weave[retry]** + **Weave[design]** | One owner: `retry` sets the backoff policy, `design` sets the states |
| "Release scheduling, feature flag rollout" | **Launch** | One-time release events |
| "Autonomous AI loop runner (nexus-autoloop)" | **Orbit** | Script-driven AI loops |
| "Business calendar (JP holidays, fiscal year, banking days)" | **Weave[schedule]** | Calendar-as-code |
| "GitHub Actions cron tuning" | **Weave[schedule]** + Gear[gha] (impl) | Weave picks the pattern, Gear configures the runner |
| "Backfill missed runs after incident" | **Triage** → **Weave[schedule]** (replay plan) → Builder | Weave designs idempotent replay |

**Rule of thumb**: Recurring time logic → Weave[schedule]. State machine → Weave[design]. Release event → Launch. AI agent loop → Orbit.

---

### Builder vs Gateway vs Schema (Grammar / API / Data Design)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Design grammar (EBNF/ABNF/PEG)", "parser-generator choice" | **Builder[grammar]** | Grammar / parser layer |
| "ReDoS-safe regex", "catastrophic backtracking audit" | **Builder[grammar]** (design) + **Sentinel** (audit) | Builder writes the pattern, Sentinel audits the shipped one |
| "Internal DSL (fluent API, template literal, YAML-embedded)" | **Builder[grammar]** | DSL architecture |
| "AST transformation, Babel plugin, jscodeshift, codemod" | **Builder[grammar]** (design) + **Shift** (migration) | Builder shapes the transform, Shift orchestrates the rollout |
| "REST/GraphQL API design, OpenAPI spec" | **Gateway** | HTTP API contract |
| "Database schema, migration, ER diagram" | **Schema** | Persistence schema |
| "General business logic implementation" | **Builder** | General implementation |
| "Log parsing with builder patterns (Logstash)" | **Builder** | Pattern engine migration/design |
| "Static security scan of shipped regex" | **Sentinel** | Post-ship audit, not design |
| "Fuzz testing against a parser" | **Radar** | Test execution, not grammar design |

**Rule of thumb**: Textual grammar/pattern/DSL → Builder. HTTP API → Gateway. DB schema → Schema. General impl → Builder. Builder designs; Sentinel audits; Radar tests.

---

### Port vs Native vs Shift (Mobile Migration & Implementation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Port web app to iOS / Android as native" | **Port** | Web → pure-native blueprint |
| "feature parity matrix between web and mobile" | **Port** | Parity verdicts (Full/Adapted/Deferred/Dropped) |
| "Native architecture design (SwiftUI / Compose)" | **Port** | Per-platform architecture mapping |
| "Strangler Fig phased migration roadmap (web → mobile)" | **Port** | Phased rollout & store-submission timeline |
| "Pure-native vs KMP vs CMP vs RN vs Flutter trade-off" | **Port** | Cross-platform decision support |
| "Implement iOS Swift / SwiftUI" | **Native** | Pure-native iOS implementation |
| "Implement Android Kotlin / Jetpack Compose" | **Native** | Pure-native Android implementation |
| "Adopt Liquid Glass / Material 3 Expressive" | **Native** | iOS 26 / Android 16 modern surfaces |
| "Finalize Privacy Manifest / Data Safety" | **Native** → Cloak | Implementation then privacy review |
| "Integrate Passkey / Credential Manager" | **Native** → Crypt | Implementation then crypto review |
| "TestFlight phased release / Play staged rollout" | **Native** → Launch | Implementation then release planning |
| "Implement in React Native / Flutter / KMP / CMP" | **out of scope** | Out of Native scope. Forge for prototypes; production requires external implementation |
| "Version migration of framework / library / DB (same language)" | **Shift** `framework`/`lang` | Same-language migration orchestrator |
| "Detect deprecated libraries and replace with native APIs" | **Shift** `detect`/`modernize` | Modernization scan (absorbed from horizon) |
| "Extract legacy web business rules (pre-port)" | **Trail** `static-rules` | Read-only archaeology (absorbed from fossil) |

**Rule of thumb**: Blueprint/design for Web→Native → Port. **Implementation** → Native. Same-language migration → Shift `framework`/`lang`. Deprecated-library detection → Shift `detect`/`modernize`. Native does not handle React Native / Flutter / KMP / CMP.

---

### Magi vs Flux vs Spark (Founder Decisions & Ideation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "office hours" / "I'm stuck" / "what should I focus on" | **Magi** | YC-style advisory; extract the single bottleneck |
| "founder advisory" / "creative direction reality check" | **Magi** | Pattern match + founder anti-pattern detection |
| "review my pitch" / "Demo Day deck" / "investor Q&A practice" | **Magi** (pitch recipe) | STRUCTURE → CLARITY → TENSION → RESONANCE → REVISE |
| "we just shipped X / hired Y / pivoted Z, postmortem" | **Magi** (retro recipe) | Retrospective on recent decisions and outcomes |
| "we're stuck right now, need to unblock" | **Magi** (triage recipe) | Emergency unblock within 5 turns |
| "I want to generate ideas, diverge" | **Flux[ideate]** | Iterative divergent ideation (4 modes) |
| "Propose a new feature as a Markdown spec" | **Spark** | Feature proposals from existing data/logic |
| "GO / NO-GO decision, pick among multiple options" | **Magi** | Three-perspective deliberation (Logos/Pathos/Sophia) |
| "Quarterly / annual scenario simulation, KPI forecast" | **Magi[simulate]** | Long-term strategy simulation |
| "Question assumptions, shift perspective" | **Flux[reframe]** | Single-shot reframing |

**Rule of thumb**: One actionable move to make this week → Magi[advisor]. Diverge → Flux[ideate]. Three-perspective deliberation → Magi[decide]. Long-term scenario → Magi[simulate]. Feature spec → Spark. Flip assumptions → Flux[reframe]. Magi does **not** generate ideas — it surfaces what the founder is avoiding.

---

## Small Project Optimization

For S/M scope projects, skip agents that add overhead without proportional value:

| Skip | Use Instead | When |
|------|-------------|------|
| Vision | Palette/Muse directly | No full UX redesign needed |
| Forge | Artisan directly | Requirements are clear |
| Cast | Echo standalone | Simple persona needs |
| Gear[gha] | Gear | Basic CI/CD only |
| Compete | Skip entirely | Internal tools, no competitors |
| Scribe | Skip entirely | S scope, no formal specs needed |
| Field | Echo directly | No formal research methodology needed |
