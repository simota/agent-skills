# Skill Review Criteria Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Official criteria reference that Judge consults when reviewing SKILL.md files.

---

## 1. Determining SKILL.md Review Scope

### Conditions for Review

Apply SKILL.md review mode when any of the following holds:

- The review target includes a `SKILL.md` file
- The review target includes a `reference/*.md` file (within a skill)
- A `.md` file with YAML frontmatter was changed
- A change occurred under the `skills/` directory

### How This Differs from Regular Code Review

| Aspect | Code Review | SKILL.md Review |
|--------|------------|----------------|
| Primary Tool | `codex review` CLI | Official criteria checklist |
| Focus | Correctness, security, logic | Structure, description quality, progressive disclosure |
| Severity Scale | CRITICAL-INFO (5 levels) | CRITICAL-LOW (4 levels, based on official criteria) |
| Routing | Builder / Sentinel / Zen | Sigil / Architect / Gauge |

---

## 2. SKILL.md Review Checklist

### Critical (Blocking)

| ID | Check | Rule |
|----|-------|------|
| SK-C01 | `SKILL.md` filename is exact (case-sensitive) | Only `SKILL.md` is allowed |
| SK-C02 | YAML frontmatter `---` delimiters are correct | Both opening and closing are required |
| SK-C03 | A `name` field is present | Required field |
| SK-C04 | A `description` field is present | Required field |
| SK-C05 | No XML tags (`<` `>`) in frontmatter | Security restriction |
| SK-C06 | `name` does not contain `"claude"` / `"anthropic"` | Reserved prefix |

### High (Must Fix)

| ID | Check | Rule |
|----|-------|------|
| SK-H01 | `name` is kebab-case | Regex: `^[a-z0-9]+(-[a-z0-9]+)*$` |
| SK-H02 | `name` matches the folder name | String match |
| SK-H03 | `description` is 1024 characters or fewer | Official limit |
| SK-H04 | `description` states WHAT | Describes what the skill does |
| SK-H05 | `description` states WHEN | Trigger conditions for when to use it |
| SK-H06 | `description` is not vague | Excludes "Helps with projects"-level phrasing |
| SK-H07 | A step-by-step structure exists | Heading or numbered list |

### Medium (Recommended Improvement)

| ID | Check | Rule |
|----|-------|------|
| SK-M01 | An Examples section exists | Concrete user-scenario examples |
| SK-M02 | A Troubleshooting section exists | Documents error handling |
| SK-M03 | The `reference/` directory is utilized | Progressive Disclosure |
| SK-M04 | SKILL.md is 5000 words or fewer | Context efficiency |
| SK-M05 | Critical instructions appear near the top of the document | High-priority instructions placed first |

### Low (Optional Improvement)

| ID | Check | Rule |
|----|-------|------|
| SK-L01 | `compatibility` field is 500 characters or fewer | Official limit |
| SK-L02 | A negative trigger exists (where needed) | Overtriggering prevention |
| SK-L03 | `metadata` includes `author` / `version` | Best practice |
| SK-L04 | No `README.md` exists in the skill folder | Official rule |

---

## 3. Description Quality Assessment

### Good Description Pattern

```yaml
# Pattern: Specific + Actionable + Trigger phrases
description: Analyzes Figma design files and generates developer handoff
documentation. Use when user uploads .fig files, asks for "design specs",
"component documentation", or "design-to-code handoff".
```

**Checkpoints**:
- ✅ Starts with a verb (clear about what it does)
- ✅ Includes trigger phrases (clear about when to use it)
- ✅ Mentions file types (clear about the target)

### Bad Description Anti-Patterns

| Anti-pattern | Example | Issue |
|-------------|---------|-------|
| Too vague | "Helps with projects" | Fails to trigger |
| Missing triggers | "Creates documentation systems" | No WHEN |
| Too technical | "Implements entity model with hierarchical relationships" | Not written from the user's perspective |
| Too long (>1024) | — | Bloats the frontmatter |

### Verdict Logic

```
IF any SK-C* fails → BLOCK (CRITICAL findings)
IF SK-H04 OR SK-H05 fails → REQUEST CHANGES
IF 3+ SK-M* fail → REQUEST CHANGES (accumulation)
ELSE → APPROVE (with notes if SK-L* issues exist)
```

---

## 4. Progressive Disclosure Review

### Verifying the Three-Level Structure

| Level | What to Check | Finding if Missing |
|-------|--------------|-------------------|
| 1st (Frontmatter) | Are `name` + `description` minimal yet sufficient? | SK-H04, SK-H05 |
| 2nd (Body) | Does SKILL.md stay focused on core instructions? | SK-M04 if word count > 5000 |
| 3rd (References) | Are details separated out into `reference/`? | SK-M03 |

### Context Efficiency Assessment

```
IF SKILL.md > 5000 words AND reference/ is empty:
  → Finding: SK-M03 + SK-M04
  → Recommendation: "Move detailed documentation to reference/"

IF SKILL.md < 500 words AND reference/ has 5+ files:
  → Note: Good progressive disclosure structure

IF all content is inline AND no reference/ directory:
  → Finding: SK-M03
  → Recommendation: "Consider progressive disclosure structure"
```

---

## 5. Review Report Format

### SKILL.md Review Finding

```
ID: [SK-C/H/M/L + NN]
Severity: [CRITICAL | HIGH | MEDIUM | LOW]
Location: [SKILL.md:line or structural]
Standard: Anthropic Agent Skill Specification (2025)
Finding: [specific observation]
Recommendation: [actionable fix]
Remediation: [Sigil | Architect | Gauge]
```

### Section to Add to the Summary

```markdown
## Skill Quality Assessment
- Frontmatter: [PASS | FAIL] ([count] issues)
- Description Quality: [PASS | FAIL] ([count] issues)
- Instruction Structure: [PASS | FAIL] ([count] issues)
- Progressive Disclosure: [PASS | FAIL] ([count] issues)
- Overall: [COMPLIANT | PARTIAL | NON-COMPLIANT]
```

---

## 6. Routing

| Finding Type | Route To |
|-------------|---------|
| Frontmatter structure issue | Sigil (regenerate) or Architect (redesign) |
| Description quality issue | Sigil (improve description) |
| Instruction structure issue | Sigil (restructure) |
| Progressive Disclosure issue | Architect (design reference separation) |
| Ecosystem internal standards violation | Gauge (16-item checklist) |
