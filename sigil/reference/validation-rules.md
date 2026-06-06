# Validation Rules

Purpose: load this during `VERIFY` to apply format checks, content checks, the `12`-point quality rubric, and the required validation report.

## Contents

1. Format checks
2. Content checks
3. Quality rubric
4. Failure patterns
5. Report template
6. Relationship to Gauge

## Relationship to Gauge

Sigil's `12`-point rubric and Gauge's `16`-item normalization checklist serve **different decision surfaces** and are not interchangeable:

| Aspect | Sigil 12-point rubric | Gauge 16-item checklist |
|--------|----------------------|--------------------------|
| Purpose | Real-time install gate during CRAFT/VERIFY | Ecosystem-wide format compliance audit |
| Granularity | 4 axes × 0-3 (Format/Relevance/Completeness/Actionability) | 16 binary items (F1/L1/H1-3/S1-9/A1-2/R1) |
| Pass threshold | `9+/12` install, `6-8` recraft, `0-5` abort | Health score percentage with PASS/PARTIAL/FAIL per item |
| Scope | Project-local generated skill | Any SKILL.md including ecosystem agents |
| Frequency | Every install, every refresh | On audit request, after structural change, scheduled |
| Source of truth | This file | `gauge/reference/normalization-checklist.md` |

**Routing rule**: when a generated skill has `ecosystem impact` (PROJECT_AFFINITY: universal or multi-project scope, or it is being promoted into `~/.claude/skills/`), forward the artifact to Gauge for full 16-item validation **after** Sigil's own 9+/12 install gate passes. Gauge is a stricter, format-focused superset; passing Sigil does not imply passing Gauge.

Treat Gauge's checklist as a **read-only input signal** during DISCOVER and CRAFT — use it to inform template choices, but do not let it replace this rubric's quantitative scoring during VERIFY.

## Format Checks

### Frontmatter

| Rule | Check | Severity |
|------|-------|----------|
| YAML block present | File starts with `---` | FAIL |
| `name` field | Non-empty, kebab-case, usually `2-4` words | FAIL |
| `description` field | Non-empty, third-person trigger phrase ("Use when…" / "Analyzes…"), ≤ 1,024 chars (target < 250), no first/second person, no XML angle brackets | FAIL |
| Extra fields | Only keep fields the runtime actually needs | WARN |

### Section Structure

| Section | Micro | Full | Check |
|---------|-------|------|-------|
| H1 title | Required | Required | Single `#` heading matches the skill title |
| Purpose / equivalent | Required | Required | Explains when and why to use the skill |
| Steps or Workflow | Required | Required | Actionable instructions |
| Template section | Optional | Required | Code blocks with language tags |
| Conventions section | Required | Optional | Project-specific rules |
| Error handling | Optional | Required | Failure and recovery patterns |
| Testing section | Optional | Required | Framework-specific validation guidance |
| Checklist | Optional | Required | Actionable completion items |

### Code Blocks

- Every code block MUST have a language tag.
- Template placeholders use `[BracketNotation]`, not `{curly}`.
- Do not include hardcoded machine-specific paths.
- Do not include secrets, tokens, or credentials.

## Content Checks

### Convention Conformity

| Check | Method | Threshold |
|-------|--------|-----------|
| Naming | Compare with `3+` existing files | `100%` match |
| Imports | Compare alias and barrel patterns | Consistent |
| File structure | Compare actual project layout | Consistent |
| Error handling | Compare local patterns | Consistent |
| Test location | Compare colocated vs separate | Consistent |

### Actionability

- Every step must be executable.
- Template code must be syntactically valid.
- File paths must exist in the project's real structure.
- Commands must be runnable in the project context.

### Completeness

Micro minimum:
- Purpose: `1-2` sentences
- Steps: `3+`
- At least one of `Template` or `Conventions`

Full minimum:
- Purpose: `3+` sentences including prerequisites
- Workflow: `3+` phases
- Templates: `2+` patterns
- Explicit `Error Handling`
- Explicit `Testing`
- Checklist with `3+` items

## Quality Scoring Rubric (`12` Points)

### Format (`0-3`)

| Score | Criteria |
|-------|----------|
| `0` | Missing frontmatter or H1 title |
| `1` | Frontmatter present but sections incomplete |
| `2` | All required sections present and structured |
| `3` | Perfect structure, consistent formatting, language tags everywhere |

### Relevance (`0-3`)

| Score | Criteria |
|-------|----------|
| `0` | Wrong framework or technology |
| `1` | Correct framework but generic content |
| `2` | Matches project conventions |
| `3` | Uses exact patterns extracted from project code |

### Completeness (`0-3`)

| Score | Criteria |
|-------|----------|
| `0` | Missing critical steps or sections |
| `1` | Main flow covered but edge cases missing |
| `2` | Common variations covered |
| `3` | Edge cases, error paths, and rollback covered |

### Actionability (`0-3`)

| Score | Criteria |
|-------|----------|
| `0` | Vague or abstract |
| `1` | Some steps need interpretation |
| `2` | All steps are clear and executable |
| `3` | Copy-paste-ready examples and templates |

### Score Interpretation

| Total | Result | Action |
|-------|--------|--------|
| `10-12` | Excellent | Install immediately |
| `9` | Pass | Install |
| `6-8` | Review | Trigger `ON_QUALITY_BELOW_THRESHOLD`, recraft |
| `3-5` | Fail | Mandatory recraft and root-cause review |
| `0-2` | Critical | Abort and re-check `SCAN` data |

## Common Failure Patterns

| ID | Symptom | Cause | Fix |
|----|---------|-------|-----|
| `F1` | Generic template for the wrong stack | `SCAN` skipped or weak | Re-run `SCAN`, confirm framework detection |
| `F2` | Naming or structure mismatch | Weak convention sampling | Read `3+` comparable files and update patterns |
| `F3` | Template references missing dependency | Assumed library not installed | Cross-check imports against manifests |
| `F4` | Workflow stops before done | Domain flow incomplete | Trace the full developer task |
| `F5` | Deprecated API or stale pattern | Project evolved | Run the evolution workflow |
| `F6` | Generated skill overlaps ecosystem agent | Deduplication missed | Re-check agent boundaries and overlap |

## Validation Report Template

```markdown
## Skill Validation Report

### Summary
- **Skills validated**: [count]
- **Passed (9+)**: [count]
- **Review needed (6-8)**: [count]
- **Failed (<6)**: [count]

### Per-Skill Scores

| Skill | Format | Relevance | Completeness | Actionability | Total | Result |
|-------|--------|-----------|-------------|---------------|-------|--------|
| [name] | [0-3] | [0-3] | [0-3] | [0-3] | [0-12] | PASS/REVIEW/FAIL |

### Issues Found
- [Skill name]: [Issue] -> [Recommended fix]

### Sync Status
- `.claude/skills/*/SKILL.md`: [count]
- `.agents/skills/*/SKILL.md`: [count]
- Sync: IN_SYNC | DRIFT_REPAIRED | PARTIAL_FAIL
```
