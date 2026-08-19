# Official Pattern Taxonomy Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Official pattern integration reference that Lore consults during the CATALOG / PROPAGATE phases.

---

## 1. Integrated Mapping of Official Patterns to Lore Pattern Classification

### Official 5 Patterns → Lore Taxonomy Conversion

| Official Pattern | Lore Domain | Lore Type | Default Confidence | Scope |
|-----------------|-------------|-----------|-------------------|-------|
| Sequential Workflow Orchestration | `PROCESS` | `SUCCESS` | `ESTABLISHED` | `ECOSYSTEM` |
| Multi-MCP Coordination | `INFRA` | `SUCCESS` | `ESTABLISHED` | `ECOSYSTEM` |
| Iterative Refinement | `PROCESS` | `HEURISTIC` | `ESTABLISHED` | `ECOSYSTEM` |
| Context-Aware Tool Selection | `APP` | `HEURISTIC` | `ESTABLISHED` | `ECOSYSTEM` |
| Domain-Specific Intelligence | `DESIGN` | `SUCCESS` | `ESTABLISHED` | `ECOSYSTEM` |

> Official patterns start at the `ESTABLISHED` level based on Anthropic's observations. They can be promoted to `FOUNDATIONAL` once enough evidence accumulates within the ecosystem.

### Official 3 Use-Case Categories → Lore Domain Conversion

| Official Category | Primary Lore Domain | Secondary Domain |
|------------------|--------------------|-----------------|
| Document & Asset Creation | `APP` | `DESIGN` |
| Workflow Automation | `PROCESS` | `INFRA` |
| MCP Enhancement | `INFRA` | `APP` |

---

## 2. Integrating Official Quality Signals with Lore Evidence Classification

### Quantitative Signals

| Official Metric | Lore Evidence Type | Threshold | Mapping |
|----------------|-------------------|-----------|---------|
| Trigger rate 90%+ | Execution evidence | ≥ 90% auto-load | `SUCCESS` pattern if met; `FAILURE` if consistently below |
| 0 failed API calls | Execution evidence | 0 failures per workflow | `SUCCESS` if met; `ANTI` if consistently failing |
| Workflow efficiency (token reduction) | Performance evidence | Baseline comparison | `TRADEOFF` pattern with quantitative data |

### Qualitative Signals

| Official Metric | Lore Evidence Type | Assessment |
|----------------|-------------------|-----------|
| No next-step prompting needed | User behavior evidence | `SUCCESS` when observed; `FAILURE` as anti-pattern |
| Correction-free execution | Consistency evidence | 3-5 identical runs → `PATTERN` confidence |
| First-try accessibility | Usability evidence | New user feedback → `EMERGING` then `PATTERN` |

---

## 3. Integrating Official Iteration Signals with Lore Decay Detection

### Undertriggering → Knowledge Gap Detection

| Official Signal | Lore Mapping | Action |
|----------------|-------------|--------|
| Skill doesn't load when expected | `FAILURE` pattern candidate | Register as `META-FAILURE-NNN` |
| Users manually enabling skills | Usability gap evidence | Propagate to Sigil (description improvement) |
| Support questions about usage | Knowledge gap signal | Propagate to Architect (trigger guidance review) |

### Overtriggering → Anti-Pattern Detection

| Official Signal | Lore Mapping | Action |
|----------------|-------------|--------|
| Skill loads for irrelevant queries | `ANTI` pattern candidate | Register as `META-ANTI-NNN` |
| Users disabling skills | Negative evidence | Propagate to Sigil (negative trigger addition) |
| Confusion about purpose | Design gap signal | Propagate to Architect (scope clarification) |

### Execution Issues → Failure Pattern Detection

| Official Signal | Lore Mapping | Action |
|----------------|-------------|--------|
| Inconsistent results | `FAILURE` pattern candidate | Cross-reference with other agent journals |
| API call failures | `INFRA-FAILURE-NNN` | Propagate to Mend (remediation pattern) |
| User corrections needed | Instruction quality gap | Propagate to Sigil (instruction improvement) |

---

## 4. Official Pattern Cross-Check Rules During the CATALOG Phase

### Official Cross-Check When Registering a New Pattern

1. **Pre-classification check**: Confirm whether the new pattern candidate matches one of the official 5 patterns
2. **If it matches**: Register it as a variant of the official pattern (append a `-V` suffix to the ID)
3. **If it doesn't match**: Register it as a normal new pattern
4. **If it conflicts**: Explicitly record the difference from the official pattern, and promote it to an independent pattern once evidence count ≥ 3

### Pattern Quality Assessment Against Official Criteria

Periodically assess whether registered patterns satisfy the following official criteria:

| Criterion | Check | Source |
|-----------|-------|--------|
| Progressive Disclosure compliance | Does the pattern reflect the 3-level structure? | Official Guide §1 |
| Description quality | Does it include a WHAT+WHEN structure? | Official Guide §2 |
| Testability | Can it be verified across the 3 Areas (Triggering/Functional/Performance)? | Official Guide §3 |
| Error handling | Does it address the 6 troubleshooting categories? | Official Guide §5 |

---

## 5. Official Criteria Distribution Rules During the PROPAGATE Phase

### Relationship Between Distribution Targets and Official Criteria

| Consumer Agent | Relevant Official Knowledge | Propagation Trigger |
|---------------|---------------------------|-------------------|
| **Sigil** | Description writing rules, instruction structure, test methodology | When a decline in skill-generation quality patterns is detected |
| **Architect** | The 5 patterns, success-criteria framework, Progressive Disclosure | When a decline in new-agent design quality patterns is detected |
| **Gauge** | Frontmatter validation spec, 6 troubleshooting categories | When a decline in audit accuracy patterns is detected |
| **Darwin** | Quality signals (quantitative/qualitative), iteration signals | When an opportunity to improve EFS assessment accuracy is detected |
| **Nexus** | The 3 use-case categories, pattern selection guide | When a decline in routing accuracy patterns is detected |

### Official Criteria Reference Format in LORE_INSIGHT

```
LORE_INSIGHT:
  Pattern: [ID]
  Official_Alignment: [ALIGNED | VARIANT | NOVEL | CONTRADICTS]
  Official_Reference: "The Complete Guide to Building Skills for Claude" §[section]
  Evidence: [agent, date, context]
  Implication: [what this means for the consumer]
```
