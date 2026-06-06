# Project Affinity Matrix

Maps each agent to the project types where it provides the most value. Used by Nexus for intelligent routing and team assembly.

---

## Project Type Definitions

| Type | Description | Examples |
|------|-------------|---------|
| **SaaS** | Web application with user accounts, subscriptions, multi-tenant | B2B/B2C platforms, productivity tools |
| **E-commerce** | Online store with cart, checkout, inventory, payments | Shopify stores, marketplace platforms |
| **Dashboard** | Admin panel, analytics, data visualization, CRUD interfaces | CMS admin, monitoring dashboards |
| **CLI** | Command-line tool, terminal utilities | Developer tools, automation scripts |
| **Library** | Reusable package, SDK, framework | npm packages, API clients |
| **API** | Backend API service, microservices | REST/GraphQL backends, webhook services |
| **Mobile** | Mobile application (React Native, responsive-first) | iOS/Android apps, PWAs |
| **Static** | Static site, blog, documentation site | Marketing pages, blogs, docs sites |
| **Data** | Data pipeline, analytics, ETL/ELT | Batch processing, streaming, ML pipelines |

---

## Affinity Levels

| Level | Symbol | Meaning |
|-------|--------|---------|
| **High** | H | Agent is highly relevant; should be included in most workflows |
| **Medium** | M | Agent is useful but not essential; include when scope demands it |
| **Low** | — | Agent has minimal relevance; include only for specific edge cases |

---

## Affinity Matrix

### Universal Agents (High affinity for all project types)

These agents provide value regardless of project type. Nexus should always consider them.

| Agent | Role | Notes |
|-------|------|-------|
| Nexus | Orchestrator | Routes and coordinates all agents |
| Builder | Core implementer | Adapts to any stack |
| Radar | Testing | All languages, all test types |
| Judge | Code review | Language/framework agnostic |
| Zen | Refactoring | Readability improvements everywhere |
| Guardian | Git/PR strategy | All repos need good commits |
| Sherpa | Task breakdown | Complex tasks in any domain |
| Lens | Code investigation | Understands any codebase |
| Scout | Bug investigation | RCA works everywhere |
| Gear | DevOps/CI/CD | Every project needs a pipeline |
| Sweep | Cleanup | Dead code exists everywhere |
| Ripple | Impact analysis | Change analysis is universal |
| Magi | Decision making | Multi-perspective judgment |
| Atlas | Architecture | Dependency analysis for any project |
| Trail | Git archaeology | History investigation |
| Rally | Parallel orchestration | Multi-session for any large task |
| Grove | Repo structure | Every project needs good structure |
| Canvas | Visualization | Diagrams for any architecture |
| Architect | Agent design | Meta-level, project-agnostic |
| Void | YAGNI enforcement | Challenges feature existence everywhere |
| Darwin | Ecosystem evolution | Monitors and evolves the agent ecosystem |
| Titan | Product delivery | Build-first delivery for any scope |
| Sigil | Project skill generation | Project-specific lightweight skills |
| Lore | Knowledge synthesis | Cross-agent pattern extraction |
| Gauge | SKILL.md audit | Format compliance checking |
| Flux | Perspective shift | Reframing and assumption challenge |
| Rank | Priority scoring | ICE/RICE/WSJF quantification |
| Fossil | Legacy archaeology | Business rule extraction |
| Omen | Pre-mortem analysis | Failure mode enumeration |
| Matrix | Combinatorial analysis | Multi-dimensional coverage |

### Frontend / UX Agents

| Agent | SaaS | E-com | Dash | CLI | Lib | API | Mobile | Static | Data |
|-------|------|-------|------|-----|-----|-----|--------|--------|------|
| Artisan | H | H | H | — | — | — | H | M | — |
| Forge | H | H | H | M | — | M | H | M | — |
| Palette | H | H | H | — | — | — | H | M | — |
| Flow | H | H | H | — | — | — | H | M | — |
| Muse | H | H | H | — | — | — | H | M | — |
| Vision | H | H | H | — | — | — | H | M | — |
| Echo | H | H | H | M | — | — | H | — | — |
| Vitrine | H | H | H | — | H | — | M | — | — |
| Frame | H | H | H | — | M | — | H | M | — |
| Loom | H | H | H | — | M | — | H | M | — |
| Ink | H | H | H | — | H | — | H | M | — |
| Prose | H | H | H | M | — | — | H | M | — |
| Funnel | M | H | — | — | — | — | M | H | — |
| Pixel | H | H | H | — | — | — | H | M | — |

### Growth / Product Agents

| Agent | SaaS | E-com | Dash | CLI | Lib | API | Mobile | Static | Data |
|-------|------|-------|------|-----|-----|-----|--------|--------|------|
| Growth | H | H | M | — | — | — | M | H | — |
| Bond | H | H | M | — | — | — | H | — | — |
| Voice | H | H | M | — | — | — | H | — | — |
| Pulse | H | H | M | — | — | — | H | — | M |
| Experiment | H | H | M | — | — | — | M | — | — |
| Field | H | H | M | — | — | — | H | — | — |
| Spark | H | H | M | — | — | — | M | — | — |
| Compete | H | H | — | — | — | — | M | — | — |
| Trace | H | H | M | — | — | — | H | — | — |
| Director | H | H | M | — | — | — | M | — | — |
| Cast | H | H | M | — | — | — | H | — | — |
| Saga | H | H | M | — | — | — | M | — | — |
| Crest | M | — | — | M | H | — | — | — | — |
| Helm | H | M | — | — | — | — | M | — | — |
| Levy | — | — | — | — | — | — | — | — | — |

### Backend / Infrastructure Agents

| Agent | SaaS | E-com | Dash | CLI | Lib | API | Mobile | Static | Data |
|-------|------|-------|------|-----|-----|-----|--------|--------|------|
| Schema | H | H | H | — | — | M | — | — | H |
| Tuner | H | H | H | — | — | M | — | — | H |
| Gateway | H | M | M | — | M | H | M | — | — |
| Scaffold | H | M | M | — | — | H | — | — | H |
| Stream | M | M | M | — | — | M | — | — | H |
| Bolt | H | H | H | — | — | H | M | — | M |
| Shard | H | — | M | — | — | H | — | — | — |
| Seek | H | H | M | — | — | H | — | — | H |
| Trawl | — | M | — | — | — | M | — | — | H |
| Relay | H | M | — | — | — | H | H | — | — |

### Testing / Quality Agents

| Agent | SaaS | E-com | Dash | CLI | Lib | API | Mobile | Static | Data |
|-------|------|-------|------|-----|-----|-----|--------|--------|------|
| Voyager | H | H | H | — | — | — | M | — | — |
| Mint | H | H | H | — | M | H | — | — | H |
| Siege | H | H | M | — | — | H | — | — | M |
| Warden | H | H | M | — | — | — | H | M | — |
| Attest | H | H | M | — | H | H | — | — | — |

### Security Agents

| Agent | SaaS | E-com | Dash | CLI | Lib | API | Mobile | Static | Data |
|-------|------|-------|------|-----|-----|-----|--------|--------|------|
| Sentinel | H | H | M | — | M | H | M | — | — |
| Probe | H | H | M | — | — | H | — | — | — |
| Canon | H | M | M | — | H | H | — | — | — |
| Specter | H | M | M | — | — | H | — | — | H |
| Breach | H | H | M | — | — | H | M | — | — |
| Vigil | H | M | M | — | — | H | — | — | — |
| Cloak | H | H | M | — | — | H | M | — | H |
| Oath | H | H | M | — | — | H | — | — | H |
| Crypt | H | H | M | — | M | H | M | — | — |

### Documentation / Content Agents

| Agent | SaaS | E-com | Dash | CLI | Lib | API | Mobile | Static | Data |
|-------|------|-------|------|-----|-----|-----|--------|--------|------|
| Quill | M | — | M | M | H | H | — | — | — |
| Scribe | H | M | M | M | H | H | — | — | — |
| Accord | H | M | M | — | H | H | — | — | — |
| Morph | M | — | M | — | M | — | — | M | — |
| Harvest | M | — | — | — | M | M | — | — | — |
| Launch | H | M | — | M | H | H | — | — | — |
| Tome | H | M | M | — | H | H | — | — | — |
| Stage | H | M | M | — | M | — | — | M | — |
| Cue | H | H | M | — | — | — | M | — | — |
| Prism | M | — | M | — | — | — | — | — | M |

### CLI / Tool Agents

| Agent | SaaS | E-com | Dash | CLI | Lib | API | Mobile | Static | Data |
|-------|------|-------|------|-----|-----|-----|--------|--------|------|
| Anvil | — | — | — | H | H | M | — | — | — |
| Reel | — | — | — | H | H | — | — | — | — |

### DevOps / Release Agents

| Agent | SaaS | E-com | Dash | CLI | Lib | API | Mobile | Static | Data |
|-------|------|-------|------|-----|-----|-----|--------|--------|------|
| Pipe | H | M | M | M | H | H | — | — | M |
| Latch | H | M | M | M | M | H | — | — | — |
| Hearth | M | — | M | H | H | M | — | — | M |
| Hone | M | — | M | H | H | M | — | — | — |
| Mend | H | H | M | — | — | H | — | — | M |
| Beacon | H | H | M | — | — | H | — | — | H |
| Ledger | H | M | M | — | — | H | — | — | H |

### Architecture Agents

| Agent | SaaS | E-com | Dash | CLI | Lib | API | Mobile | Static | Data |
|-------|------|-------|------|-----|-----|-----|--------|--------|------|
| Stratum | H | M | M | — | M | H | — | — | — |
| Shift | H | M | M | M | H | H | M | — | M |
| Weave | H | M | M | — | — | H | — | — | M |

### Mobile Agents

| Agent | SaaS | E-com | Dash | CLI | Lib | API | Mobile | Static | Data |
|-------|------|-------|------|-----|-----|-----|--------|--------|------|
| Native | M | M | — | — | — | — | H | — | — |

### Specialized Agents

| Agent | SaaS | E-com | Dash | CLI | Lib | API | Mobile | Static | Data |
|-------|------|-------|------|-----|-----|-----|--------|--------|------|
| Polyglot | H | H | M | — | — | — | H | M | — |
| Vector | H | H | H | — | — | — | — | M | — |
| Triage | H | H | M | — | — | H | — | — | — |
| Arena | H | M | — | M | M | H | — | — | — |
| Oracle | H | M | M | — | M | H | — | — | H |
| Aether | — | — | — | — | — | — | — | — | — |
| Orbit | H | M | M | — | — | H | — | — | M |
| Void | H | M | M | M | H | H | — | — | — |
| Sketch | M | M | M | — | — | — | M | M | — |
| Dot | — | — | — | — | — | — | — | — | — |
| Clay | — | — | — | — | — | — | — | — | — |
| Tone | — | — | — | — | — | — | — | — | — |
| Quest | — | — | — | — | — | — | — | — | — |
| Realm | — | — | — | — | — | — | — | — | — |
| Lyric | — | — | — | — | — | — | — | — | — |

---

## Usage by Nexus

### Team Assembly

When Nexus receives a task and knows the project type, use this matrix to:

1. **Must-include**: Universal agents + agents with H affinity for the project type
2. **Consider**: Agents with M affinity (include if task scope demands it)
3. **Skip**: Agents with — affinity (unless explicitly requested)

### Example: SaaS Authentication Feature

```yaml
Project_Type: SaaS
Task: "Add OAuth2 authentication"

Must-include (H for SaaS):
  - Builder (implementation)
  - Sentinel (security)
  - Radar (testing)
  - Gateway (API design)
  - Schema (user model)

Consider (M for SaaS):
  - Quill (API docs)
  - Stream (event logging)

Skip (— for SaaS):
  - Reel (CLI demos)
  - Anvil (CLI tools)
```

### Example: CLI Tool Development

```yaml
Project_Type: CLI
Task: "Build a database migration CLI"

Must-include (H for CLI):
  - Anvil (CLI/TUI)
  - Reel (demo recording)
  - Builder (core logic)

Consider (M for CLI):
  - Forge (prototype)
  - Echo (UX walkthrough)
  - Quill (help text / README)
  - Launch (release management)
  - Arena (multi-engine approach)

Skip (— for CLI):
  - Artisan (frontend)
  - Growth (SEO/CRO)
  - Bond (engagement)
```

---

## In-File Format

Each agent's SKILL.md includes a compact `PROJECT_AFFINITY` tag in its CAPABILITIES_SUMMARY HTML comment:

```
PROJECT_AFFINITY: SaaS(H) E-commerce(H) Dashboard(H) Mobile(H) Static(M)
```

For universal agents:
```
PROJECT_AFFINITY: universal
```

Nexus reads these tags during routing to make informed team assembly decisions.
