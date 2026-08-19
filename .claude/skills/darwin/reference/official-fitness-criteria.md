# Official Fitness Criteria Reference

> Sources:
> - "The Complete Guide to Building Skills for Claude" (Anthropic, 2025) — Progressive Disclosure / frontmatter / instruction structure baseline.
> - "New in Claude Managed Agents: dreaming, outcomes, and multiagent orchestration" (Anthropic, 2026-05-06) — adds **Outcomes** rubrics as the new official success-criteria primitive. URL: `https://claude.com/blog/new-in-claude-managed-agents`.

Official-standards-based fitness evaluation reference used by Darwin in the ASSESS / EVOLVE phases.

> **2026-05 update**: Anthropic's Managed Agents now ship a first-class `Outcomes` mechanism in public beta — agent operators write a **rubric** describing what success looks like and the agent works toward it. Internal Anthropic testing measured **up to +10 percentage points** task-success lift over a plain prompting loop (+8.4 pp on docx generation, +10.1 pp on pptx generation). Darwin treats the presence of an explicit Outcomes rubric (or local equivalent) as a positive OSC signal for the *Instruction Structure* and *Error Handling* criteria below. Conversely, an agent stuck on a plain prompting loop with no rubric — when running under Claude Managed Agents — is now an OSC penalty (≥ −10 toward the *Instruction Structure* dimension), because the +10 pp ceiling lift is freely available.

---

## 1. EFS Official Spec Conformance Dimension

Integrate **Official Spec Conformance (OSC)** as a supplementary metric into the existing EFS 5-dimension evaluation.

### OSC Scoring (0-100)

| Criterion | Weight | Scoring | Source |
|-----------|--------|---------|--------|
| **Progressive Disclosure conformance** | 0.25 | Degree of implementation of the 3-tier structure (frontmatter / body / references) | Official Guide §1 |
| **Frontmatter quality** | 0.20 | name (kebab-case) + description (WHAT+WHEN, ≤1024 chars, no XML) | Official Guide §2 |
| **Instruction structure** | 0.20 | Degree of structuring across Steps → Examples → Troubleshooting | Official Guide §2 |
| **Test methodology implementation** | 0.15 | Coverage across the 3 areas of Triggering / Functional / Performance | Official Guide §3 |
| **Composability** | 0.10 | Coexistence with other skills, portability | Official Guide §1 |
| **Error handling** | 0.10 | Troubleshooting coverage (number of the 6 categories addressed) | Official Guide §5 |

### OSC Grades

| Grade | Score | Interpretation |
|-------|-------|---------------|
| S | 95-100 | Fully meets the official spec, exemplary |
| A | 85-94 | Nearly fully conformant with the official spec |
| B | 70-84 | Conformant on major items, room for improvement |
| C | 55-69 | Meets only basic conformance |
| D | 40-54 | Significant deviation from the official spec |
| F | 0-39 | Largely non-conformant with the official spec |

### How It Integrates with EFS

Rather than being a 6th EFS dimension, OSC functions as a **quality correction factor** on the existing 5 dimensions:

```
Adjusted_EFS = EFS × (0.8 + 0.2 × (OSC / 100))
```

- OSC = 100 → EFS × 1.0 (no change)
- OSC = 50 → EFS × 0.9 (10% reduction)
- OSC = 0 → EFS × 0.8 (20% reduction)

> A conservative integration that doesn't break the existing EFS calculation. Higher OSC preserves EFS; lower OSC applies only a mild penalty.

---

## 2. Strengthening RS Evaluation with Official Quality Signals

### Incorporating Official Metrics into the Agent Relevance Score (RS)

Add the following official quality signals as supplementary inputs to the existing RS calculation:

| Signal | RS Impact | Detection Method |
|--------|----------|-----------------|
| Description satisfies WHAT+WHEN | RS +5 | Parsing the YAML frontmatter |
| Progressive Disclosure implemented | RS +5 | Presence and referencing of a `reference/` directory |
| Test methodology defined | RS +3 | Presence of Triggering/Functional test descriptions |
| Error handling documented | RS +2 | Presence of a Troubleshooting section |
| Description is vague | RS -5 | No trigger phrases, generic description |
| `reference/` unused | RS -3 | All information inline in SKILL.md |

---

## 3. Integrating Official Standards into Evolution Triggers

### New Trigger: ET-09 — Official Spec Deviation

| Field | Value |
|-------|-------|
| Trigger ID | `ET-09` |
| Condition | OSC ≤ C (below 55) for any agent |
| Scope | Medium |
| Action | Propose SKILL.md improvement via Architect |
| Priority | After ET-01 through ET-08 |

### Linking Official Standards to Existing Triggers

| Existing Trigger | Official Enhancement |
|-----------------|---------------------|
| `ET-02`: Health Score drop ≥10 | Also evaluate OSC to determine whether official spec deviation is the cause |
| `ET-03`: 3+ unprocessed feedback | Prioritize feedback that reports official-standard violations |
| `ET-05`: Same decision repeated 3+ | Recommend the optimal pattern by matching against official patterns |
| `ET-08`: Average Health Score < B | Include the OSC grade alongside root-cause analysis |

---

## 4. Applying Official Standards by Lifecycle Phase

### Expected OSC by Phase

| Lifecycle Phase | Minimum OSC | Rationale |
|----------------|-------------|-----------|
| `GENESIS` | D (40+) | In the early stage, prioritize establishing the basic structure |
| `ACTIVE_BUILD` | C (55+) | During core feature development, implement Progressive Disclosure |
| `STABILIZATION` | B (70+) | In the stabilization phase, largely conform to the official spec |
| `PRODUCTION` | A (85+) | Production operation requires high official-spec conformance |
| `MAINTENANCE` | A (85+) | Maintain quality even in the maintenance phase |
| `SCALING` | A (85+) | A solid quality foundation is especially important during scaling |
| `SUNSET` | — | Not evaluated |

### Application in the ASSESS Phase

1. Detect the lifecycle phase (existing logic)
2. Look up the Minimum OSC for that phase
3. Calculate the current OSC for each agent
4. Add agents where `Current OSC < Minimum OSC` to the improvement candidate list
5. Include an OSC section in the DARWIN_REPORT

---

## 5. Ecosystem Coverage Analysis by the 3 Official Use-Case Categories

### Agent Mapping by Category

| Official Category | Ecosystem Agents | Coverage |
|------------------|-----------------|----------|
| **Document & Asset Creation** | Scribe, Quill, Morph, Builder | Document/asset generation |
| **Workflow Automation** | Nexus, Nexus[deliver], Sherpa, Sigil, Gear[gha], Launch | Workflow automation |
| **MCP Enhancement** | Frame, Relay, Vector, Hone | MCP integration enhancement |

### Coverage Gap Detection

Evaluate the following in the ASSESS phase:
- Whether each category has sufficient agents
- Whether the balance across categories is appropriate
- Whether uncovered categories are prioritized when proposing new agents

---

## 6. Adding an Official Standards Section to DARWIN_REPORT

### Output Format Extension

```markdown
## Official Spec Conformance (OSC)

| Agent | OSC Score | Grade | Min Required | Status |
|-------|-----------|-------|-------------|--------|
| [name] | [0-100] | [S-F] | [phase-based] | [PASS/BELOW] |

### OSC Summary
- Ecosystem Average: [score]
- Agents Below Minimum: [count]
- Top Improvement Candidates: [list]

### Use Case Coverage
- Document & Asset Creation: [agent count] agents
- Workflow Automation: [agent count] agents
- MCP Enhancement: [agent count] agents
```
