# Task-to-Skill Mapping Patterns

**Purpose:** Common scenarios and the recommended agent(s) for each.
**Read when:** You need to match a user's task to the best skill agent(s).

---

## Quick Decision Tree

```
User request
  │
  ├─ Write code
  │   ├─ New feature implementation → Builder
  │   ├─ Prototype → Forge
  │   ├─ Frontend → Artisan
  │   ├─ CLI / TUI → Builder
  │   └─ Mobile (iOS / Android pure-native) → Native
  │
  ├─ Fix code
  │   ├─ Bug investigation → Scout
  │   ├─ Refactoring → Zen
  │   ├─ Performance (whole app) → Bolt
  │   ├─ Performance (DB / queries) → Tuner
  │   └─ Security fix → Sentinel
  │
  ├─ Test
  │   ├─ Unit tests → Radar
  │   ├─ E2E tests → Voyager
  │   └─ Load / resilience tests → Siege
  │
  ├─ Design
  │   ├─ Architecture → Atlas
  │   ├─ DB design → Schema
  │   ├─ API design → Gateway
  │   └─ UI / UX design → Vision
  │
  ├─ Write documentation
  │   ├─ Technical specifications → Scribe
  │   ├─ Code documentation → Quill
  │   ├─ UX writing → Prose
  │   └─ Learning material → Tome
  │
  ├─ Review
  │   ├─ Code review → Judge
  │   ├─ Security audit → Sentinel
  │   └─ Standards compliance → Canon
  │
  ├─ Investigate / analyze
  │   ├─ Codebase comprehension → Lens
  │   ├─ Git history → Trail
  │   ├─ Legacy code analysis → Trail (`static-rules`)
  │   ├─ Impact analysis → Ripple
  │   └─ Competitive research → Compete
  │
  ├─ DevOps / infrastructure
  │   ├─ CI / CD → Gear[gha]
  │   ├─ IaC → Scaffold
  │   ├─ Dependency management → Gear
  │   └─ Monitoring design → Beacon
  │
  ├─ Planning / strategy
  │   ├─ Task decomposition → Sherpa
  │   ├─ Multi-agent coordination → Nexus
  │   ├─ Prioritization → Rank
  │   ├─ Release planning → Launch
  │   └─ Founder office hours → Magi[advisor]
  │
  ├─ Migration / modernization
  │   ├─ Web → Native porting design → Port
  │   ├─ Framework migration → Shift
  │   └─ Deprecated-library detection → Shift `detect`
  │
  └─ Other
      ├─ Browser automation / product image acquisition → Vector
      ├─ i18n → Polyglot
      ├─ SVG icons → Ink
      └─ Idea generation → Flux
```

---

## Scenario-Based Patterns

### "Fix a bug"

| Situation | Recommendation | Reason |
|-----------|----------------|--------|
| Unknown root cause | Scout → Builder | Scout pinpoints the cause; Builder fixes it |
| Regression | Trail → Scout → Builder | Trail identifies the offending commit |
| Performance degradation | Bolt | Performance specialist |
| Security vulnerability | Sentinel → Builder | Sentinel detects; Builder fixes |

### "Add a new feature"

| Situation | Recommendation | Reason |
|-----------|----------------|--------|
| Spec is clear | Builder | Direct implementation |
| Spec is vague | Scribe → Builder | Define spec first, then implement |
| Need a prototype | Forge | Fast prototyping |
| Large feature | Sherpa → Nexus | Decompose, then orchestrate |

### "Improve code quality"

| Situation | Recommendation | Reason |
|-----------|----------------|--------|
| Refactoring | Zen | Improve readability and structure |
| Test gaps | Radar | Add tests |
| Doc gaps | Quill | JSDoc / comments |
| Dead code | Sweep | Detect and remove |

### "Strengthen security"

| Situation | Recommendation | Reason |
|-----------|----------------|--------|
| Static analysis | Sentinel | Codebase security audit |
| Dynamic testing | Probe | DAST execution |
| Red team | Breach | Attack-scenario design |
| Crypto design | Crypt | Cryptographic architecture |

### "Improve deploy / operations"

| Situation | Recommendation | Reason |
|-----------|----------------|--------|
| CI / CD | Gear[gha] | GitHub Actions specialist |
| Infrastructure | Scaffold | IaC design |
| Monitoring / alerting | Beacon | SLO / SLI design |
| Incident response | Triage → Mend | Investigate, then auto-remediate |

### "Improve UI / UX"

| Situation | Recommendation | Reason |
|-----------|----------------|--------|
| Design direction | Vision | Creative direction |
| Usability improvement | Palette | Interaction quality |
| Animation | Flow | CSS / JS animation |
| User testing | Echo | Persona cognitive walkthrough |
| Mockup → code | Pixel | Generate HTML / CSS from images |

---

## Multi-Agent Chain Patterns

### Feature Development Chain
```
Scribe (spec) → Builder (impl) → Radar (tests) → Judge (review)
```

### Bug Fix Chain
```
Scout (investigate) → Builder (fix) → Radar (add tests)
```

### Security Audit Chain
```
Sentinel (static) → Probe (dynamic) → Breach (red team)
```

### Architecture Improvement Chain
```
Atlas (analyze) → Ripple (impact) → Builder (impl) → Judge (review)
```

### UX Improvement Chain
```
Echo (walkthrough) → Vision (direction) → Palette (improvements) → Flow (animation)
```

### Performance Optimization Chain
```
Tuner (DB) → Bolt (app) → Beacon (monitoring)
```

### Legacy Modernization Chain
```
Trail `static-rules` (analyze legacy rules) → Shift `detect` (deprecated dep scan) → Shift `framework`/`lang` (execute migration)
```

### Web-to-Native Porting Chain
```
Lens / Atlas (web survey) → Port (blueprint) → Native (iOS / Android impl) → Voyager (mobile E2E) → Launch (phased rollout)
```

### Founder Advisory Chain
```
Magi[advisor] (bottleneck + action) → Sherpa (decompose) / Builder (implement) / Echo[demand] (validate)
```

### Product Image Acquisition Chain
```
Vector (acquire) → Cloak (PII review) → Vitrine / Funnel / Pixel / Atelier (downstream delivery)
```

---

## "Don't Use" Quick Reference

A reverse lookup to prevent common mistakes.

| Goal | Easy mistake | Correct skill | Reason |
|------|--------------|---------------|--------|
| Code implementation | Scout | Builder | Scout only investigates |
| E2E tests | Radar | Voyager | Radar handles unit tests |
| DB optimization | Schema | Tuner | Schema designs; Tuner optimizes |
| PR review | Zen | Judge | Zen does refactoring |
| API spec | Quill | Gateway | Quill is for in-code docs |
| Browser automation | Voyager | Vector | Voyager is for E2E tests |
| Release management | Guardian | Launch | Guardian manages PRs |
| Codebase comprehension | Scout | Lens | Scout is for bug investigation; Lens for general comprehension |
| System architecture | Schema | Atlas | Schema is DB-only; Atlas is overall architecture |
| Technical specifications | Quill | Scribe | Quill is for in-code docs |
| Production implementation | Forge | Builder | Forge produces prototypes |
| Web → mobile porting | Native | Port | Native implements; Port produces blueprint and parity matrix |
| Idea ideation (divergent) | Magi | Flux | Magi advises or decides; Flux is divergent brainstorming |
| Strategic decision | Magi[advisor] | Magi[decide] | Advisory pressure-testing and a binding verdict are separate Magi Recipes |
| Long-term scenarios | Magi | Magi | Magi handles a bounded decision; Magi handles quarterly+ scenarios |

When in doubt, ask "Does this skill change code?":
- Changes code: Builder, Zen, Artisan, Bolt
- Doesn't change code: Scout, Judge, Atlas, Sentinel

---

## Output Formats

### Recommendation Format

```markdown
## Recommendation: [Task summary]

### 1. [Agent Name] (top pick)
- **What it does**: [one-line description]
- **Why this one**: [why it fits the user's situation]
- **How to use**: `/[agent-name] [example instruction]`
- **Caveat**: [when not to use, if any]

### 2. [Agent Name] (alternative)
- **What it does**: [one-line description]
- **When to pick this instead**: [conditions favoring it over option 1]

### Next step
[Concrete action proposal]
```

### Comparison Format

```markdown
## Comparison: [Agent A] vs [Agent B]

| Aspect | Agent A | Agent B |
|--------|---------|---------|
| Primary role | ... | ... |
| Code generation | yes / no | yes / no |
| Input | ... | ... |
| Output | ... | ... |
| When to use | ... | ... |

### How to choose
- [Condition 1] → Agent A
- [Condition 2] → Agent B
- [Condition 3] → Both (Agent A → Agent B chain)
```
