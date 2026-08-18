# Validation Checklist

**Purpose:** Structured validation checklist for generated skill files.
**Read when:** You need to verify completeness, quality, or Nexus compatibility.

## Contents
- Overview
- Validation Categories
- 1. Structure Validation (REQUIRED)
- 2. Content Quality Validation
- 3. Overlap Check Validation
- 4. Nexus Compatibility Validation
- 5. Style & Conventions Validation
- Validation Report Template
- Quick Validation Checklist
- 6. Context Efficiency Validation (OPTIONAL)
- 7. Opus 5 Readiness Validation (RECOMMENDED)
- 8. Output Density Protocol Validation (REQUIRED)
- Automated Validation Script

---

## Overview

Every generated SKILL.md must pass this validation checklist before being considered complete.

**Pass Criteria:**
- All REQUIRED items must pass
- At least 80% of RECOMMENDED items should pass
- Document any OPTIONAL items that are skipped

---

## Validation Categories

| Category | Items | Weight |
|----------|-------|--------|
| Structure | 15 | 30% |
| Content Quality | 12 | 25% |
| Overlap Check | 5 | 15% |
| Nexus Compatibility | 8 | 15% |
| Style & Conventions | 10 | 15% |

---

## 1. Structure Validation (REQUIRED)

### Frontmatter

- [ ] **S1.1** `name` field present and valid
  - kebab-case format
  - 1-3 syllables
  - No conflicts with existing agents

- [ ] **S1.2** `description` field present and valid
  - English language
  - Maximum 100 characters
  - Includes positive and negative triggers in English

### HTML Comment Section

- [ ] **S1.3** CAPABILITIES_SUMMARY present
  - Inside HTML comment `<!-- -->`
  - 5-10 bullet points
  - Action-oriented verbs

- [ ] **S1.4** COLLABORATION_PATTERNS present
  - Pattern A, B, C (minimum 2)
  - Flow notation (→, ↔)

- [ ] **S1.5** BIDIRECTIONAL_PARTNERS present
  - INPUT list
  - OUTPUT list

### Core Sections

- [ ] **S1.6** Philosophy section present
  - Code block format
  - 3-5 lines
  - Unique to this agent

- [ ] **S1.7** Boundaries section present
  - "Always do:" header (4-8 items)
  - "Ask first:" header (2-5 items)
  - "Never do:" header (3-6 items)

- [ ] **S1.8** INTERACTION_TRIGGERS section present
  - Table with columns: Trigger | Timing | When to Ask
  - Minimum 3 triggers
  - YAML templates for each trigger

### Domain Sections

- [ ] **S1.9** Domain-specific sections present
  - Minimum 3 sections
  - Maximum 10 sections
  - Relevant to agent's specialty

### Collaboration Section

- [ ] **S1.10** Agent Collaboration section present
  - ASCII diagram
  - INPUT PROVIDERS block
  - OUTPUT CONSUMERS block
  - Collaboration patterns table

### Process Sections

- [ ] **S1.11** Journal section present
  - `.agents/[agentname].md` reference
  - "Only add entries when" list
  - "DO NOT journal" list

- [ ] **S1.12** Daily Process section present
  - 3-5 phases
  - Each phase has actions

- [ ] **S1.13** Favorite Tactics / Avoids section present
  - 3-5 tactics
  - 3-5 anti-patterns

### Required Sections

- [ ] **S1.14** Activity Logging section present
  - PROJECT.md reference
  - Example log entry

- [ ] **S1.15** AUTORUN Support section present
  - _AGENT_CONTEXT format
  - _STEP_COMPLETE format

- [ ] **S1.16** Nexus Hub Mode section present
  - NEXUS_HANDOFF format
  - All required fields

- [ ] **S1.17** Output Language section present
  - States Japanese requirement

- [ ] **S1.18** Git Commit Guidelines section present
  - References _common/GIT_GUIDELINES.md
  - Examples with ✅ and ❌

---

## 2. Content Quality Validation

### Clarity

- [ ] **C2.1** Agent role is clear in first paragraph
  - One sentence mission statement
  - Specific outcome mentioned

- [ ] **C2.2** Boundaries are unambiguous
  - No vague terms ("appropriately", "as needed")
  - Specific actions described

- [ ] **C2.3** INTERACTION_TRIGGERS have clear conditions
  - Specific scenarios described
  - No overlap between triggers

### Completeness

- [ ] **C2.4** All YAML templates are valid
  - Correct indentation
  - Required fields present
  - Options array has 2-4 items

- [ ] **C2.5** Code examples are complete
  - Runnable (if applicable)
  - Comments where needed
  - No placeholders like `[TODO]`

- [ ] **C2.6** Handoff formats are defined
  - Input handoff from partners
  - Output handoff to partners

### Consistency

- [ ] **C2.7** Terminology is consistent
  - Same terms throughout
  - Matches existing ecosystem

- [ ] **C2.8** Formatting is consistent
  - Same header levels
  - Same list styles
  - Same code block markers

### Uniqueness

- [ ] **C2.9** Philosophy is unique
  - Not copied from other agents
  - Reflects this agent's specialty

- [ ] **C2.10** Closing statement is unique
  - Memorable phrase
  - References agent identity

### Actionability

- [ ] **C2.11** Daily process is actionable
  - Clear steps
  - Verifiable completion

- [ ] **C2.12** Tactics are specific
  - Not generic advice
  - Applicable to this domain

---

## 3. Overlap Check Validation

- [ ] **O3.1** Ecosystem scan completed
  - All existing agents checked
  - Similarity scores calculated

- [ ] **O3.2** No overlap exceeds 50%
  - If any > 50%, agent rejected
  - Alternative proposed

- [ ] **O3.3** Overlaps 30-50% are documented
  - User confirmation obtained
  - Differentiation statement included

- [ ] **O3.4** Differentiation is clear
  - What makes this agent unique
  - Why existing agents can't do this

- [ ] **O3.5** Overlap report generated
  - Top 3 overlapping agents listed
  - Shared/unique capabilities identified

---

## 4. Nexus Compatibility Validation

### AUTORUN Support

- [ ] **N4.1** _AGENT_CONTEXT format is correct
  - All required fields present
  - Role field matches agent name

- [ ] **N4.2** _STEP_COMPLETE format is correct
  - Status enum: SUCCESS | PARTIAL | BLOCKED | FAILED
  - Handoff format specified
  - Next agent recommendation

### Hub Mode

- [ ] **N4.3** NEXUS_HANDOFF format is complete
  - Step number
  - Agent name
  - Summary (1-3 lines)
  - Key findings
  - Artifacts
  - Risks
  - Open questions
  - Pending Confirmations
  - User Confirmations
  - Suggested next agent
  - Next action

- [ ] **N4.4** Hub-spoke pattern respected
  - No direct agent-to-agent calls
  - Results returned to Nexus

### Routing Integration

- [ ] **N4.5** Category assignment is correct
  - Matches existing category definitions
  - No new category without justification

- [ ] **N4.6** Routing matrix entry proposed
  - Task type identified
  - Primary chain defined
  - Optional additions listed

- [ ] **N4.7** Collaboration patterns are Nexus-compatible
  - Can be orchestrated by Nexus
  - Handoffs are standardized

- [ ] **N4.8** Agent can be invoked via Nexus
  - Clear trigger keywords
  - Unambiguous routing

---

## 5. Style & Conventions Validation

### Language

- [ ] **Y5.1** English for explanations
  - Natural English prose
  - No machine translation artifacts

- [ ] **Y5.2** English for code/identifiers
  - Variable names
  - Function names
  - File paths

- [ ] **Y5.3** Consistent terminology
  - Uses existing ecosystem terms
  - No conflicting definitions

### Formatting

- [ ] **Y5.4** Markdown is valid
  - Headers have correct levels
  - Code blocks have language markers
  - Tables are properly formatted

- [ ] **Y5.5** Line count within range
  - Minimum 400 lines
  - Maximum 1400 lines

- [ ] **Y5.6** No trailing whitespace
  - Clean formatting
  - No excessive blank lines

### Naming

- [ ] **Y5.7** Agent name follows conventions
  - 1-3 syllables
  - Evokes role
  - Easy to type

- [ ] **Y5.8** Section headers are consistent
  - Match template structure
  - Same capitalization

### References

- [ ] **Y5.9** External references are valid
  - `_common/INTERACTION.md` referenced
  - `_common/GIT_GUIDELINES.md` referenced
  - `.agents/PROJECT.md` referenced

- [ ] **Y5.10** Internal references are complete
  - `reference/*.md` files exist
  - All mentioned files are created

---

## Validation Report Template

```markdown
## Validation Report for [AgentName]

### Summary
- **Total Checks:** 50
- **Passed:** [X]
- **Failed:** [Y]
- **Pass Rate:** [Z%]

### Structure Validation: [PASS/FAIL]
| Check | Status | Notes |
|-------|--------|-------|
| S1.1 | ✅/❌ | |
| ... | | |

### Content Quality: [PASS/FAIL]
...
```

---

## Quick Validation Checklist

For rapid validation, use this abbreviated checklist:

```markdown
## Quick Check for [AgentName]

**Structure (must have all):**
- [ ] Frontmatter (name, description)
- [ ] CAPABILITIES_SUMMARY
- [ ] Boundaries (Always/Ask/Never)
- [ ] INTERACTION_TRIGGERS
- [ ] Activity Logging
- [ ] AUTORUN Support
- [ ] Nexus Hub Mode

**Quality (need 80%):**
- [ ] Clear mission statement
- [ ] Unambiguous boundaries
- [ ] Valid YAML templates
...
```

---

## 6. Context Efficiency Validation (OPTIONAL)

Validate context optimization when COMPRESS phase has been applied.

- [ ] **E6.1** Token budget analysis completed
  - Section-level token estimates documented
  - Total estimated tokens within target range

- [ ] **E6.2** Boilerplate ratio < 15%
  - Boilerplate sections identified and measured
  - Deduplication opportunities documented or applied

- [ ] **E6.3** Ma layout compliance checked
  - Zone 1 (first 15%): Identity and boundaries present
  - Zone 4 (last 15%): Actionable templates present
  - Separator frequency: `---` every 50-80 lines
  - Dense/sparse rhythm maintained

- [ ] **E6.4** Compression equivalence verified
  - Behavioral equivalence: same outputs for same inputs
  - Structural equivalence: all required sections present
  - Integration equivalence: AUTORUN/Nexus formats intact
  - Routing equivalence: CAPABILITIES_SUMMARY unchanged

See `reference/context-compression.md` for compression strategies and equivalence verification details.

---

## 7. Opus 5 Readiness Validation (RECOMMENDED)

Validate that generated skills align with Opus 5 default behaviors. See `reference/official-design-patterns.md` Section 11 and `_common/OPUS_5_AUTHORING.md` (P1–P12; P12 is Claude 5 generation-wide, not Opus-specific).

- [ ] **R7.1** Front-loaded context capture
  - Trigger Guidance enumerates first-turn required inputs (target files, success criteria, constraints)
  - INTERACTION_TRIGGERS batch related confirmations rather than serializing them

- [ ] **R7.2** Explicit length control *(both channels)*
  - Output sections specify length envelopes (line counts, bullet counts, table dimensions)
  - Free-form summaries replaced with structured envelopes (`_STEP_COMPLETE`, `## NEXUS_HANDOFF`)
  - Skills that write documents to disk carry a separate no-padding length calibration
  - Long SKILL.md files repeat a one-line brevity reminder near the end

- [ ] **R7.3** Explicit tool-use rationale
  - Tools used by the skill have documented "when" (trigger condition) and "why" (value provided)
  - Eager-read or think-first preferences are stated explicitly when they matter
  - Web access goes through `web_search` (Opus 5-supported); any `web_fetch` dependency is isolated to a step explicitly modelled on Sonnet 5 / Fable 5

- [ ] **R7.4** Subagent delegation caps
  - Delegation criteria + a cap are stated ("only large genuinely independent tracks; prefer one over several")
  - Explicit prohibition on spawning subagents to verify the skill's own work
  - References `_common/SUBAGENT.md` for parallelism-layer choice

- [ ] **R7.5** Thinking-on assumptions
  - Skill does not assume thinking is off, and contains no instruction against thinking/reasoning
  - Depth steered via nudges at decision points ("Think carefully and step-by-step…" / "Prioritize responding quickly…")
  - No hardcoded numeric thinking budgets; cost controlled via effort, not by disabling thinking

- [ ] **R7.6** Effort-level expectations declared
  - Stated against the `high` default; `xhigh` named where coding/agentic work needs it
  - Skills that require `xhigh`/`max` flag this in `description` and Trigger Guidance (with ~64k `max_tokens` note)

- [ ] **R7.7** Delegation-engineer framing
  - Workflow is self-directing for the bulk of execution
  - User check-ins reserved for `Ask first` decisions, not micro-steps

- [ ] **R7.8** Scope discipline — both directions
  - Narrow tasks carry explicit bounds against scope expansion; out-of-scope stated
  - Instructions meant to apply broadly state their scope ("every section, not just the first")
  - No restrictive phrasing that will be obeyed literally at the cost of coverage

- [ ] **R7.9** No redundant verification or narration scaffolding
  - No "verify your work" / "double-check" / "re-verify" / "spawn a subagent to verify" instructions
  - Independent-verifier steps (a *different* agent checks the producer) are intact and distinguishable from self-checks
  - No legacy forced-progress scaffolding ("summarize every N tool calls"); correction narration bounded

- [ ] **R7.10** Coverage-vs-filter (reviewers/detectors only)
  - Finding stage instructs coverage (report all, tag confidence/severity); filtering deferred to a downstream stage
  - Any single-pass self-filter uses a concrete bar, not qualitative terms like "important"

- [ ] **R7.11** Voice & artifact defaults (writers/designers only)
  - Voice baseline stated; warmer tone stated explicitly if the product needs it
  - Document/slide skills pass in the target style or template rather than relying on a default
  - Design/frontend skills give concrete specs or option-proposal, not generic negation

- [ ] **R7.12** Context minimalism (all roles; Claude 5 generation-wide)
  - Style and craft guidance framed as the intended outcome, not as a prohibition list — safety gates, destructive-action confirmations, and protocol contracts are exempt
  - Few-shot examples present only where the output shape is non-obvious (schemas, protocol markers), not where they merely illustrate judgment
  - No instruction duplicated between SKILL.md and its reference or tool description; tool-usage rules live in the tool description
  - References point at real artifacts (code, tests, rubrics, mockups) rather than paraphrasing them

---

## 8. Output Density Protocol Validation (REQUIRED)

Validate that generated skills declare runtime output style. See `_common/OUTPUT_STYLE.md` for the canonical rules.

- [ ] **R8.1** Output Contract section exists in SKILL.md, **or** the skill correctly inherits the `M` default
  - Absent contract = declared `M` (`OUTPUT_STYLE.md` § Inherited default). Inheritance is the expected state for most skills, not a gap.
  - Declare a contract only to say something inheritance does not: different default tier, per-task overrides, or domain bans.
  - Located near `Output Language` section
  - Distinct from `_STEP_COMPLETE` / `NEXUS_HANDOFF` envelopes (those have their own limits)

- [ ] **R8.2** Default tier declared when a contract is present
  - One of `S` / `M` / `L` / `XL`
  - `L`/`XL` only when the deliverable is a long structured document delivered *in the response*. A skill that writes its deliverable to a file stays `M` and summarizes.

- [ ] **R8.3** OUTPUT_STYLE.md is referenced, not duplicated
  - SKILL.md does NOT inline the banned-pattern list, format priority, density rules, or § Conditional Requirements
  - References `_common/OUTPUT_STYLE.md` instead

- [ ] **R8.4** Task overrides declared when applicable
  - Skills with ≥2 distinct task types **that differ in tier** list per-task overrides
  - Overrides justify deviation from default tier (typically smaller for status/lookup, larger for deliverables)

Failure modes (any of these → R8 fails):
- Contract present but default tier missing or invalid.
- Contract present that only restates the inherited `M` with no overrides and no domain bans — pure redundancy, delete it.
- `L`/`XL` declared by a skill whose deliverable is a written file.
- Banned-pattern list copied inline instead of referenced.
- Multi-task skill whose task types differ in tier with no override table.

---

## Automated Validation Script

For programmatic validation:

```yaml
VALIDATION_RULES:
  structure:
    frontmatter:
      required: [name, description]
      name_pattern: "^[a-z]+(-[a-z]+)*$"
      description_max_length: 100

    sections:
      required:
        - "Boundaries"
        - "INTERACTION_TRIGGERS"
        - "Activity Logging"
        - "AUTORUN Support"
        - "Nexus Hub Mode"
        - "Output Language"
# ...
```
