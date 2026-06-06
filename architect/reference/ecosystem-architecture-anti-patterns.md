# Ecosystem Architecture Anti-Patterns

**Purpose:** Ecosystem modularity, governance, and growth failure patterns.
**Read when:** The proposal may fragment the ecosystem or erode discoverability.

## Contents
- 1. The Seven Core Ecosystem Anti-Patterns
- 2. Modular Design Principles
- 3. Governance Drift Patterns
- 4. Platform Design Lessons
- 5. Ecosystem Health Metrics
- 6. Architect Integration

## 1. The Seven Core Ecosystem Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Mitigation |
|---|-------------|---------|----------|------------|
| **EA-01** | **Big Ball of Mud** | The ecosystem grows without structure | Agent boundaries are unclear and dependencies stay implicit | Use categories and explicit `COLLABORATION_PATTERNS` |
| **EA-02** | **The Blob (God Agent)** | One agent absorbs too many responsibilities | `10+` capabilities and heavy overlap with neighbors | Enforce specialization and split responsibilities |
| **EA-03** | **Gas Factory** | Building a complex ecosystem for simple needs | Many low-usage agents and high learning cost | Apply the 80% rule and design backward from real demand |
| **EA-04** | **Modularity Violation** | Agents that should be independent always change together | Change impact cascades unpredictably | Redefine boundaries and visualize the dependency graph |
| **EA-05** | **Phantom Agent** | An agent is defined but rarely used | Usage below `10%`, stale docs, no collaboration pull | Audit usage regularly and retire inactive agents |
| **EA-06** | **Circular Dependency** | Agents depend on each other cyclically | Flows like `A → B → C → A` and loop risk | Enforce one-way dependency direction or introduce a mediator |
| **EA-07** | **Erosion** | Gradual drift away from the intended architecture | Naming drift, pattern mismatch, document decay | Run periodic health audits and automate governance checks |

---

## 2. Modular Design Principles

```
Five principles of a modular ecosystem:

  1. High cohesion:
     ✅ Each agent's responsibilities are tightly related
     ❌ Unrelated functions coexist in one agent
     → 1 agent = 1 domain = 1 specialization

  2. Loose coupling:
     ✅ Dependencies stay minimal
     ❌ A change in Agent A ripples through B, C, and D
     → Standardize interfaces with handoff templates

  3. Information hiding:
     ✅ `CAPABILITIES_SUMMARY` defines the external API
     ❌ Internal implementation detail leaks across agents
     → Keep `reference/` as internal detail and `SKILL.md` as external surface

  4. Substitutability:
     ✅ Different agents can honor the same handoff contract
     ❌ One irreplaceable agent becomes a hard dependency
     → Use standardized handoff formats

  5. Incremental adoption:
     ✅ Add new agents gradually
     ❌ Big-bang ecosystem expansion
     → Expand category by category

Modularity anti-patterns:

  ❌ Feature Envy:
    Agent A constantly depends on B's data or functions
    → Redefine the boundary or merge the pair

  ❌ Shotgun Surgery:
    One change affects many agents
    → Redistribute responsibilities or move shared pieces to `_common/`

  ❌ Speculative Generality:
    Agents are created for possible future needs
    → Require demand from at least 3 concrete product needs before adding one
```

---

## 3. Governance Drift Patterns

```
Five drift patterns:

  Drift-01: Naming drift
    Cause: new agents are added without checking existing naming rules
    Symptom: near-duplicate names such as analyze / analysis / analyzer
    Mitigation: require `naming-conventions.md`

  Drift-02: Structure drift
    Cause: `SKILL.md` template is interpreted too freely
    Symptom: inconsistent section structure between agents
    Mitigation: enforce `skill-template.md` plus `validation-checklist.md`

  Drift-03: Collaboration-pattern drift
    Cause: handoff formats are not standardized
    Symptom: INPUT / OUTPUT descriptions diverge wildly
    Mitigation: enforce standard handoff templates

  Drift-04: Category drift
    Cause: ambiguous category classification for new agents
    Symptom: one category contains unrelated agents
    Mitigation: validate against `agent-categories.md`

  Drift-05: Quality drift
    Cause: `Health Score` is not measured regularly
    Symptom: some references become stale or inconsistent
    Mitigation: run the PDCA loop in `review-loop.md`
```

---

## 4. Platform Design Lessons

```
Platform-as-product principles:

  1. Prioritize internal developer experience:
     → Optimize for the skill designer's workflow
     → Provide templates, checklists, and validation tooling

  2. Incremental complexity:
     Level 0: `_common/` only
     Level 1: `SKILL.md` template
     Level 2: `reference/` for deeper domain knowledge
     Level 3: Nexus integration plus self-evolution

  3. Documentation is API:
     → `SKILL.md` = agent API surface
     → `CAPABILITIES_SUMMARY` = routing metadata
     → `reference/` = internal implementation docs
     → Documentation quality sets system quality

  4. Design for attraction, not coercion:
     → Deliver value instead of forcing adoption
     → Share successful patterns
     → Keep the entry barrier low and the ceiling high

Scaling cautions:

  ❌ Linear growth from dozens of agents to 100+ agents
    → Category overload and poorer discoverability

  ✅ Subdivide categories and route hierarchically
    → Nexus → category hub → specialist agent
    → Reach the right agent through staged narrowing
```

---

## 5. Ecosystem Health Metrics

| Metric | Target | Measurement |
|-------|--------|-------------|
| Agent usage rate | `80%+` of agents used at least monthly | `journal` and `.agents/PROJECT.md` |
| Overlap rate | Less than `30%` overlap between agents | `overlap-detection.md` scoring |
| Average `Health Score` | Grade `B (80+)` or better | `review-loop.md` formula |
| Documentation freshness | Updated within one sprint | Last-modified audit |
| Category balance | `2-8` agents per category | `agent-categories.md` |
| Orphan count | `0` | INPUT / OUTPUT partner validation |

---

## 6. Architect Integration

```
How Architect uses this reference:
  1. Screen for EA-01 through EA-07 during `ENVISION`
  2. Check modular principles during new-agent design
  3. Detect governance drift during ecosystem expansion
  4. Validate ecosystem-health metrics during `VALIDATE`

Quality gates:
  - `10+` capabilities → propose a split (prevents EA-02)
  - Usage `<10%` → retire or merge candidate (prevents EA-05)
  - `8+` agents in one category → subdivide the category
  - Non-standard handoff format → enforce template (prevents Drift-03)
  - Circular dependency detected → redesign dependency direction (prevents EA-06)
  - `Health Score < C (70)` → create an improvement plan (prevents EA-07)
```

**Source:** [InfoQ: Architecture Trends 2025](https://www.infoq.com/articles/architecture-trends-2025/) · [O'Reilly: Software Architecture Patterns, Antipatterns, and Pitfalls](https://www.oreilly.com/library/view/software-architecture-patterns/0642572221119/) · [Brainhub: Software Architecture Patterns](https://brainhub.eu/library/software-architecture-patterns)
