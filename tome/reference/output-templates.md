# Output Templates

**Purpose:** Detailed templates and guidelines for each output format.
**Read when:** Deciding document structure or format during COMPOSE phase.

---

## Learning Document Template (Standard)

```markdown
# [Change Title] — Learning Document

## Meta
| Field | Value |
|-------|-------|
| Target | [commit hash / PR #number / branch name] |
| Date | YYYY-MM-DD |
| Audience | [beginner / intermediate / advanced] |
| Related files | [primary file list] |
| Change volume | [+XX / -YY lines, ZZ files] |

---

## Overview
[1-3 sentences describing the full picture: what changed, why, and how]

---

## Glossary
| Term | Definition | Context in this change |
|------|-----------|----------------------|
| [Term 1] | [General definition] | [Specific meaning/usage in this change] |

---

## Background (Why)

### Problem Solved
[Problem/issue that existed before the change]

### Motivation / Trigger
[What prompted this change — bug report, performance issue, new requirement, etc.]

### Constraints
[Technical or business constraints that influenced the change]

---

## Change Details (What & How)

### Change Point 1: [Title]

**Before:**
```[language]
// Pre-change code (necessary and sufficient scope)
```
[Explanation of pre-change behavior/problems]

**After:**
```[language]
// Post-change code (highlight diff with comments)
```
[Explanation of post-change behavior/improvements]

**Learning Point:**
> [General principle or pattern learnable from this change]

---

## Design Decisions (Why This Way)

### Adopted Approach
[Description of chosen design/pattern]

**Reasons for selection:**
1. [Reason 1]
2. [Reason 2]

### Alternatives Considered
| Alternative | Summary | Rejection Reason |
|-------------|---------|-----------------|
| [Option A] | [Summary] | [Why not adopted] |
| [Option B] | [Summary] | [Why not adopted] |

---

## Anti-patterns (Why Not)

### ❌ [Pattern to Avoid 1]
```[language]
// Code example of what NOT to do
```
**Why to avoid:** [Technical reason, potential problems]
**Instead:** [Reference to the correct approach]

---

## Flow Diagram
```mermaid
[Diagram showing how the change affects system flow]
[Mark changed portions]
```

---

## Summary & Lessons

### General Takeaways
1. [Lesson 1: principle applicable beyond this project]
2. [Lesson 2]

### Project-specific Notes
- [Note 1]

### References
- [Link 1]
```

---

## Glossary Template

Lightweight format focused on terminology:

```markdown
# [Target] — Glossary

| Term | Category | Definition | Usage in Code | Related Terms |
|------|----------|-----------|--------------|---------------|
| [Term] | [pattern/library/concept/api] | [Definition] | `[code usage]` | [Related] |
```

---

## Decision Record Template

Tome supports three ADR formats. Pick by decision weight, not by team preference — small reversible decisions in MADR-full waste reviewer attention; large architecture moves in Y-statement under-document the trade-offs.

### Format selection

| Format | When to use | Source |
|--------|-------------|--------|
| **Y-statement** (one-sentence) | Reversible decision whose rationale fits one sentence; can be written in ~90 seconds | adr.github.io/adr-templates — Y-statement |
| **Nygard** (Context/Decision/Consequences) | Classic short ADR; ~1 page; default for most teams | Michael Nygard 2011 — Documenting Architecture Decisions |
| **MADR 4.0.0** (full) | Multi-option weighing with explicit pros/cons; needs `Confirmation` step (how the decision is validated) | adr.github.io/madr — MADR 4.0.0 released Sept 2024 |

### Y-statement (lightweight default)

> In the context of `<use case / system component>`, facing `<concern / requirement>`, we decided for `<option>` and against `<rejected alternatives>`, to achieve `<benefits>`, accepting `<downsides / trade-offs>`.

One sentence. Store inline in code, in a wiki page, or as an ADR file. Pair with Nygard/MADR for decisions large enough to need full Context and Pros/Cons sections — Y-statement is the default, not the only option. [Source: medium.com/olzzio — Y-statements by Olaf Zimmermann]

### Nygard short ADR

```markdown
# ADR-[number]: [Decision Title]

## Status
[Proposed / Accepted / Deprecated / Superseded]

## Context
[Background and situation requiring the decision]

## Decision
[Chosen option and rationale]

## Consequences
[Impact and trade-offs of this decision]

## Related Commits
- [commit hash]: [description]
```

### MADR 4.0.0 full template

MADR 4.0.0 (released Sept 2024, current as of 2026-05) is the maintained successor to MADR 3.x. Key changes vs 3.x: `Validation` renamed to `Confirmation` and nested under `Decision Outcome`; `Deciders` renamed to `Decision Maker(s)`. [Source: github.com/adr/madr/releases — MADR 4.0.0]

```markdown
---
# These are optional metadata elements. Feel free to remove any of them.
status: "{proposed | rejected | accepted | deprecated | superseded by ADR-NNN}"
date: YYYY-MM-DD
decision-makers: [list of everyone involved in the decision]
consulted: [list of people whose opinions were sought; two-way communication]
informed: [list of people kept up-to-date; one-way communication]
---

# [short title, representative of solved problem and found solution]

## Context and Problem Statement
[Describe the context and problem statement in 2-3 sentences. You may want to articulate the problem as a question and add links to collaboration boards or tickets.]

## Decision Drivers
- [driver 1, e.g., a force, facing concern, ...]
- [driver 2, ...]

## Considered Options
- [option 1]
- [option 2]
- [option 3]

## Decision Outcome
Chosen option: "[option N]", because [justification — addresses a decision driver | resolves a force | comes out best (see Pros and Cons of the Options below)].

### Consequences
- Good, because [positive consequence, e.g., improvement of one or more desired qualities]
- Bad, because [negative consequence, e.g., compromising one or more desired qualities]

### Confirmation
[How will the implementation of this ADR be confirmed? E.g. by review, by ArchUnit test, by automated check in CI.]

## Pros and Cons of the Options

### [option 1]
- Good, because [argument a]
- Good, because [argument b]
- Neutral, because [argument c]
- Bad, because [argument d]

### [option 2]
- Good, because [argument a]
- Bad, because [argument b]

## More Information
[Links, related ADRs (`Supersedes: ADR-NNN` / `Superseded-by: ADR-MMM`), related commits.]
```

> **Supersession rule:** when an Accepted ADR must change, write a NEW ADR that supersedes it and link both directions. Never edit the accepted original — preserving the reasoning trail is the point. [Source: adr.github.io; AWS Prescriptive Guidance — ADR process]

---

## Tutorial Template

Step-by-step reproducible walkthrough:

```markdown
# [Title] — Tutorial

## Prerequisites
- [Required knowledge 1]
- [Required tools/environment]

## Goal
[What the reader will be able to do after completing this tutorial]

## Steps

### Step 1: [Title]
[Explanation]
```[language]
// Code to execute
```
**Verify:** [Expected result]

### Step 2: [Title]
[Repeat same structure]

## Common Mistakes
| Mistake | Symptom | Correct Approach |
|---------|---------|-----------------|
| [Mistake 1] | [Error message etc.] | [How to do it right] |

## Extension Exercises
- [Challenge 1]
- [Challenge 2]
```

---

## Learning Series Template (Batch Mode)

Serialized episodes across multiple PRs/commits:

```markdown
# [Series Title] — Learning Series

## Series Overview
| Field | Value |
|-------|-------|
| Scope | [PR #1, #2, #3 / branch / sprint] |
| Episodes | [count] |
| Date range | YYYY-MM-DD — YYYY-MM-DD |
| Audience | [beginner / intermediate / advanced] |
| Theme | [What ties these changes together] |

## Series Map
| Episode | Target | Title | Key Concept |
|---------|--------|-------|-------------|
| 1 | PR #XX | [Title] | [Core concept] |
| 2 | PR #YY | [Title] | [Core concept] |

---

## Episode 1: [Title]
**Target:** [commit/PR ref]
**Prerequisite episodes:** None

[Standard learning document sections: Overview, Glossary, etc.]

### Connection to Series
- **Builds on:** [previous episode concepts, if any]
- **Leads to:** [what the next episode will cover]

---

## Episode 2: [Title]
[Repeat structure]

---

## Series Summary
### Concept Progression
[How understanding builds across episodes]

### Knowledge Graph
[Concept relationships across all episodes — hand off to Canvas for visualization]
```

---

## Incremental Update Template

Delta-only document comparing against a previous learning document:

```markdown
# [Component/Feature] — Incremental Update

## Meta
| Field | Value |
|-------|-------|
| Previous doc | [path/ref to previous learning doc] |
| Previous target | [original commit/PR] |
| Current target | [new commit/PR] |
| Date | YYYY-MM-DD |
| Audience | [level] |

---

## What Changed Since Last Document

### Added Knowledge
[New concepts, patterns, or decisions not present in previous doc]

### Changed Decisions
| Decision | Previous | Current | Reason for Change |
|----------|----------|---------|-------------------|
| [Decision] | [Old approach] | [New approach] | [Why it changed] |

### Deprecated Patterns
[Patterns from previous doc that are no longer valid]

### Unchanged (Reference)
[Brief pointer to previous doc sections that remain valid]

---

## Updated Glossary
[Only new or changed terms — reference previous doc for unchanged terms]

## Quality Scorecard
[Standard scorecard]
```

---

## Quality Scorecard Template

Attach at the end of every deliverable:

```markdown
## Quality Scorecard

| Axis | Score | Evidence |
|------|-------|----------|
| Fact/Inference Ratio | [A/B/C] | [X inferences labeled out of Y total claims] |
| Term Coverage | [A/B/C] | [X/Y first-occurrence terms defined] |
| Before/After Pairs | [A/B/C] | [N code comparison pairs included] |
| Why Not Depth | [A/B/C] | [N alternatives with rejection reasons] |
| Audience Fit | [A/B/C] | [Audience: level, detection: method, confidence: H/M/L] |

**Overall:** [PASS if no C scores / REVISION NEEDED if any C]
```

---

## Depth Adjustment Guidelines

### Beginner additions
- Add "Background: [Concept]" sections explaining framework/language basics
- Link to official documentation
- Include comprehension checks: "Can you explain this concept in one sentence?"

### Advanced compression
- Omit term definitions for standard industry vocabulary
- Focus on trade-off analysis, architecture impact, and alternative approaches
- Use concise technical prose without step-by-step elaboration
