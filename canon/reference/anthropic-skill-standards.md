# Anthropic Skill Standards Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Reference used by Canon in the ASSESS phase to evaluate SKILL.md compliance with the official specification.

---

## 1. Standard Overview

| Field | Value |
|-------|-------|
| Standard Name | Anthropic Agent Skill Specification |
| Publisher | Anthropic |
| Version | 2025 (The Complete Guide to Building Skills for Claude) |
| Scope | Skill design, structure, and distribution across Claude Code / Claude.ai / API |
| Category | AI Agent Quality |
| Canon Category Code | `SKILL` |

---

## 2. Requirements Matrix

### 2.1 Structural Requirements (STR)

| ID | Requirement | Level | Evidence |
|----|------------|-------|---------|
| STR-01 | A `SKILL.md` file exists (case-sensitive) | CRITICAL | File existence check |
| STR-02 | YAML frontmatter is enclosed by `---` delimiters | CRITICAL | YAML parse validation |
| STR-03 | The `name` field is kebab-case | HIGH | Regex: `^[a-z0-9]+(-[a-z0-9]+)*$` |
| STR-04 | `name` matches the folder name | HIGH | String comparison |
| STR-05 | `name` does not contain `"claude"` / `"anthropic"` | CRITICAL | String search |
| STR-06 | A `description` field is present | CRITICAL | Field presence check |
| STR-07 | `description` is 1024 characters or fewer | HIGH | Character count |
| STR-08 | `description` contains no XML tags (`<` `>`) | CRITICAL | Character search |
| STR-09 | The skill folder contains no `README.md` | MEDIUM | File absence check |
| STR-10 | `compatibility` field is 500 characters or fewer (when used) | LOW | Character count |

### 2.2 Description Quality Requirements (DSC)

| ID | Requirement | Level | Evidence |
|----|------------|-------|---------|
| DSC-01 | WHAT (what it does) is described | HIGH | Semantic analysis |
| DSC-02 | WHEN (when to use it / trigger conditions) is described | HIGH | Trigger phrase presence |
| DSC-03 | Concrete tasks/phrases are included | MEDIUM | Actionable keyword detection |
| DSC-04 | Relevant file types are mentioned when applicable | LOW | Context-dependent |
| DSC-05 | Not vague (excludes generic wording like "Helps with projects") | HIGH | Anti-pattern matching |

### 2.3 Instruction Quality Requirements (INS)

| ID | Requirement | Level | Evidence |
|----|------------|-------|---------|
| INS-01 | A step-by-step structure is present | HIGH | Heading/list structure |
| INS-02 | Instructions are concrete and actionable | HIGH | Imperative verb presence |
| INS-03 | An Examples section is present | MEDIUM | Section heading detection |
| INS-04 | Troubleshooting / error handling is described | MEDIUM | Section heading detection |
| INS-05 | Links from `reference/` are appropriate | MEDIUM | Link validity check |
| INS-06 | Critical instructions are placed near the top of the document | LOW | Position analysis |

### 2.4 Progressive Disclosure Requirements (PD)

| ID | Requirement | Level | Evidence |
|----|------------|-------|---------|
| PD-01 | 1st level: frontmatter is minimal yet sufficient for triggering decisions | HIGH | Frontmatter content analysis |
| PD-02 | 2nd level: SKILL.md body focuses on core instructions | MEDIUM | Word count ≤ 5000 recommended |
| PD-03 | 3rd level: details are separated into `reference/` | MEDIUM | Directory structure check |
| PD-04 | Reference links from SKILL.md are explicit | LOW | Reference link presence |

### 2.5 Composability Requirements (CMP)

| ID | Requirement | Level | Evidence |
|----|------------|-------|---------|
| CMP-01 | Designed to coexist with other skills | LOW | Exclusive capability claims absence |
| CMP-02 | Environment dependencies are recorded in the `compatibility` field | LOW | Field content check |

---

## 3. Troubleshooting Compliance Check

In the ASSESS phase, evaluate skill compliance against the following 6 categories:

| Category | Check | Compliant Criteria |
|----------|-------|-------------------|
| Upload Failure | SKILL.md naming, YAML format, name format | STR-01 through STR-05 all PASS |
| Undertriggering | Description quality | DSC-01 through DSC-05 all PASS |
| Overtriggering | Scope clarity, negative triggers | DSC-02 + presence of scope-limiting statements |
| Instructions Not Followed | Instruction structure quality | Key items in INS-01 through INS-06 PASS |
| MCP Connection Issues | Explicit MCP dependencies and error handling | INS-04 + MCP-related troubleshooting |
| Large Context Issues | Progressive Disclosure implementation | PD-01 through PD-04 all PASS |

---

## 4. Compliance Level Determination

### Overall Determination Criteria

| Level | Criteria | Action |
|-------|---------|--------|
| **Compliant** | All CRITICAL PASS + 80%+ of HIGH PASS | Document and maintain |
| **Partial** | All CRITICAL PASS + 50-79% of HIGH PASS | Enhancement recommended |
| **Non-compliant** | 1+ CRITICAL FAIL | Remediation required |

### Severity Timeline

| Severity | Timeline | Examples |
|----------|----------|---------|
| CRITICAL | Immediate | Missing SKILL.md, broken YAML, XML in frontmatter |
| HIGH | 1 sprint | Vague description, no trigger phrases, no steps |
| MEDIUM | 1 month | No examples, no troubleshooting, inline-heavy |
| LOW | Backlog | Missing compatibility field, no negative triggers |

---

## 5. Role Boundary with Gauge

| Aspect | Canon | Gauge |
|--------|-------|-------|
| **Target standard** | Anthropic official skill specification + industry standards | Ecosystem's internal 16-item normalization checklist |
| **Evaluation perspective** | Compliance with external standards | Conformance with internal templates |
| **Output** | Compliance report with citations | PASS/PARTIAL/FAIL with fix snippets |
| **Collaboration** | Canon detects official-standard violations → Gauge performs detailed verification against the internal checklist | Gauge detects structural issues → Canon cross-checks against official standards |

---

## 6. Evidence Format

```
Standard: Anthropic Agent Skill Specification (2025)
Requirement: [ID] [requirement description]
Evidence: [file:line or structural observation]
Status: [Compliant | Partial | Non-compliant]
Finding: [specific observation]
Recommendation: [actionable fix]
Priority: [CRITICAL | HIGH | MEDIUM | LOW]
Remediation Agent: [Sigil | Architect | Gauge]
```
