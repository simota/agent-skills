# Enhancement Proposal Framework

**Purpose:** Scoring and proposal framework for improving an existing skill.
**Read when:** You are evaluating or planning an improvement instead of creating a new skill.

## Contents
- Overview
- Health Score Assessment
- Grade Interpretation
- Enhancement Proposal Template
- Priority Classification
- Improvement Workflow (Detailed)
- Proposal Presentation Format
- Integration with Review Loop

---

## Overview

The Enhancement Proposal Framework formalizes Architect's "Improve Existing" workflow. It provides structured templates for Health Score assessment, gap analysis, proposal generation, and implementation tracking.

---

## Health Score Assessment

### Scoring Components

```
HEALTH_SCORE = Structure(30%) + Content(25%) + Integration(20%) + Activity(15%) + Freshness(10%)
```

### Structure Score (30%)

| Check Item | Points | Criteria |
|-----------|--------|----------|
| SKILL.md exists and well-formed | 10 | Frontmatter, philosophy, boundaries present |
| Reference files (3+ files) | 8 | Minimum 3 domain-specific reference files |
| handoff-formats.md exists | 4 | Dedicated handoff file (ecosystem standard) |
| Standard sections complete | 5 | All required sections per skill-template.md |
| Line count in range (400-1400) | 3 | Not too sparse, not too bloated |

**Maximum: 30 points**

### Content Score (25%)

| Check Item | Points | Criteria |
|-----------|--------|----------|
| CAPABILITIES_SUMMARY complete | 5 | All capabilities listed for Nexus routing |
| Boundaries well-defined | 5 | Always (4-8), Ask (2-5), Never (3-6) items |
| INTERACTION_TRIGGERS with templates | 5 | Table + YAML question templates |
| Domain expertise depth | 5 | Reference files contain actionable knowledge |
| Daily Process defined | 5 | Step-by-step operational procedure |

**Maximum: 25 points**

### Integration Score (20%)

| Check Item | Points | Criteria |
|-----------|--------|----------|
| BIDIRECTIONAL_PARTNERS defined | 5 | Clear INPUT and OUTPUT partners listed |
| Collaboration patterns (2+) | 5 | Named patterns with flow diagrams |
| Handoff templates complete | 5 | Both inbound and outbound handoffs |
| AUTORUN support | 3 | _AGENT_CONTEXT and _STEP_COMPLETE defined |
| Nexus Hub Mode | 2 | NEXUS_HANDOFF format defined |

**Maximum: 20 points**

### Activity Score (15%)

| Check Item | Points | Criteria |
|-----------|--------|----------|
| Activity Logging section | 5 | PROJECT.md logging instructions present |
| Journal section | 5 | Agent journal with clear guidelines |
| Git guidelines reference | 5 | Commit/PR format defined or referenced |

**Maximum: 15 points**

### Freshness Score (10%)

| Check Item | Points | Criteria |
|-----------|--------|----------|
| Recent updates (< 30 days) | 4 | File modified within last 30 days |
| Ecosystem alignment | 3 | Agent count, categories match current state |
| No deprecated patterns | 3 | No stale references or outdated formats |

**Maximum: 10 points**

### Context Efficiency Score (Bonus: +0 to 10)

Applied as a tiebreaker on top of the base 100-point Health Score.

| Check Item | Points | Criteria |
|-----------|--------|----------|
| Boilerplate ratio < 15% | 3 | Deduplication applied to common sections |
| Token budget within target | 3 | Section-level token estimates documented |
| Ma layout compliance | 2 | Zone 1-4 structure followed |
| Compression equivalence verified | 2 | 4-axis verification passed |

**Maximum Bonus: 10 points** (added to base score, used only as tiebreaker for same-grade agents)

See `reference/context-compression.md` for detailed methodology.

---

## Grade Interpretation

| Score | Grade | Action | Response Time |
|-------|-------|--------|---------------|
| 90-100 | A | No action needed | — |
| 80-89 | B | Minor improvements optional | Next cycle |
| 70-79 | C | Schedule improvements | < 2 weeks |
| 60-69 | D | Priority improvements | < 1 week |
| < 60 | F | Immediate attention | < 24 hours |

---

## Enhancement Proposal Template

```yaml
ENHANCEMENT_PROPOSAL:
  agent: "[Agent name]"
  date: "[YYYY-MM-DD]"
  architect_assessment:
    health_score_current: [0-100]
    grade_current: "[A-F]"
    health_score_projected: [0-100]
    grade_projected: "[A-F]"

  breakdown:
    structure: { score: [0-30], issues: ["..."] }
    content: { score: [0-25], issues: ["..."] }
    integration: { score: [0-20], issues: ["..."] }
    activity: { score: [0-15], issues: ["..."] }
    freshness: { score: [0-10], issues: ["..."] }

  proposals:
    - id: 1
      title: "[Enhancement title]"
      priority: P1 | P2 | P3
      category: structure | content | integration | activity | freshness
      description: "[What to add/change]"
      current_gap: "[What is missing or broken]"
      expected_impact:
        score_delta: [+N points]
        affected_components: ["structure", "integration"]
      files:
        - path: "[file path]"
          action: create | edit
          description: "[What changes]"

  implementation_order:
    - phase: P1
      proposals: [1, 2]
      estimated_files: [count]
    - phase: P2
      proposals: [3, 4]
      estimated_files: [count]
    - phase: P3
      proposals: [5, 6]
      estimated_files: [count]
```

---

## Priority Classification

### P1 — Critical Gaps

Criteria (any one qualifies):
- Missing ecosystem-standard file (e.g., handoff-formats.md)
- Broken or missing integration with declared partners
- Health Score component below 50% of maximum
- Functionality gap that blocks downstream agents

### P2 — Important Improvements

Criteria:
- Underdeveloped workflow or methodology
- AUTORUN coverage gap
- Content depth below peer agents in same category
- Missing but non-blocking collaboration patterns

### P3 — Nice-to-Have Enhancements

Criteria:
- Ecosystem-level tooling improvements
- Automation of manual processes
- Advanced capabilities beyond core mission
- Future-proofing for anticipated ecosystem growth
- Context efficiency optimization (token budget, Ma layout, boilerplate reduction)

---

## Improvement Workflow (Detailed)

### Step 1: ASSESS — Calculate Health Score

```
1. Read SKILL.md and all reference files
2. Read key collaboration partner SKILL.md files
3. Score each of the 5 components using the checklist above
4. Calculate weighted total
5. Assign grade
```

Output: Health Score Report

```yaml
HEALTH_SCORE_REPORT:
  agent: "[name]"
  score: [0-100]
  grade: "[A-F]"
  breakdown:
    structure: [0-30]
    content: [0-25]
    integration: [0-20]
    activity: [0-15]
    freshness: [0-10]
  top_issues:
    - "[Issue 1 — highest impact]"
    - "[Issue 2]"
    - "[Issue 3]"
```

### Step 2: GAP — Identify Improvement Points

```
1. Compare against skill-template.md standard sections
2. Compare against peer agents in same category
3. Check bidirectional partner expectations (do partners reference this agent?)
4. Identify missing handoff templates
5. Check AUTORUN coverage for all task types
```

Analysis dimensions:
- **Structural gaps**: Missing files, sections, or standard patterns
- **Content gaps**: Shallow methodology, missing templates
- **Integration gaps**: Broken partner links, missing handoffs
- **Consistency gaps**: Patterns that differ from ecosystem norms

### Step 3: PLAN — Create Improvement Plan

```
1. Group gaps into enhancement proposals
2. Classify priority (P1/P2/P3)
3. Estimate file changes per proposal
4. Define implementation order (dependencies)
5. Project Health Score improvement per phase
```

### Step 4: IMPLEMENT — Execute Improvements

```
1. Create new reference files first (no line-number dependencies)
2. Edit SKILL.md from bottom to top (avoid line shifts)
3. Use parallel agents for independent file changes
4. Verify no Japanese in new content (if English-only requested)
```

Implementation strategies:
- **New files**: Create complete files via Write tool
- **SKILL.md edits**: Edit from end of file upward to prevent line number drift
- **Parallel execution**: Independent files can be edited concurrently via Task agents
- **Bottom-to-top rule**: When making multiple edits to the same file, start with the highest line number

### Step 5: VALIDATE — Verify Improved Score

```
1. Run grep checks for key content presence
2. Scan for language violations (Japanese in English-only content)
3. Recalculate Health Score
4. Compare before/after
5. Report results
```

Validation checklist:
- [ ] All proposed changes are present in files
- [ ] No unintended content removed
- [ ] New files follow ecosystem conventions
- [ ] SKILL.md line count still in 400-1400 range
- [ ] Health Score improved as projected

---

## Proposal Presentation Format

When presenting enhancement proposals to users, follow this structure:

```
## [Agent Name] Enhancement Proposal

### Current Health Score: [X]/100 (Grade [Y])

| Category | Weight | Score | Weighted | Key Issue |
|---------|--------|-------|----------|-----------|
| Structure | 30% | ... | ... | ... |
| Content | 25% | ... | ... | ... |
| Integration | 20% | ... | ... | ... |
| Activity | 15% | ... | ... | ... |
| Freshness | 10% | ... | ... | ... |

---

### P1: Critical Gaps

#### Enhancement 1: [Title]
**Current gap**: [What is missing]
**Proposed addition**: [What to add]

#### Enhancement 2: [Title]
...

### P2: Important Improvements
...

### P3: Nice-to-Have
...

---

### Projected Health Score (after P1): [X]/100 (Grade [Y])

| Category | Current | After P1 | Improvement |
|---------|---------|----------|-------------|
| ... | ... | ... | ... |

**Implementation files (P1):**
| File | Action | Content |
|------|--------|---------|
| ... | create/edit | ... |
```

---

## Integration with Review Loop

The Enhancement Framework connects to the existing Review Loop (`review-loop.md`):

| Review Loop Phase | Enhancement Framework Role |
|-------------------|---------------------------|
| PLAN | Use Health Score Assessment to identify targets |
| DO | Use Improvement Workflow to execute changes |
| CHECK | Use Validation step to measure improvement |
| ACT | Feed results back into next Review cycle |

### Trigger Mapping

| Review Trigger | Enhancement Action |
|----------------|-------------------|
| SCHEDULED (weekly) | Run batch Health Score on priority agents |
| ON_AGENT_CREATION | Score new agent 7 days post-creation |
| ON_ECOSYSTEM_CHANGE | Re-assess changed agents |
| ON_QUALITY_ALERT | Immediate P1 enhancement proposal |
