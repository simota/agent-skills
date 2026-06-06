# Normalization Checklist (Audit Reference)

**Purpose:** Defines the 18-item checklist with PASS/PARTIAL/FAIL criteria and P0-P3 priority classification.
**Read when:** Starting any SCAN or CLASSIFY phase.
**Source:** `.agents/skill-normalization-checklist.md` (ecosystem master checklist).

**Recent additions (Generation 3):**
- `F2` Description Discoverability — WHAT + WHEN check (P0). Routing accuracy depends on it; Anthropic Complete Guide explicitly mandates both.
- `S10` Body Size Constraint — line + token thresholds (P1). Anthropic recommendation is `<500 lines / <5000 tokens`. Repository-tuned tiers in `reference/detection-patterns.md`.
- Automated detection for F1/F2/F3/N1/N2/C1/C2/S1/S2 is available via `python3 _common/scripts/lint-frontmatter.py --severity warning`. Use that as the source-of-truth scanner; this checklist remains the human-readable contract.

---

## 18-Item Checklist

### F1: YAML Frontmatter

| Status | Criteria |
|--------|----------|
| PASS | `---` delimiters present, contains **exactly** `name:` and `description:` (no custom keys); body contains an explicit capability declaration line (e.g. "Tools used:" or equivalent prose stating the tools/MCP/network surface the skill touches) |
| PARTIAL | Delimiters present and `name:` + `description:` exist, but the body lacks an explicit capability declaration |
| FAIL | No YAML frontmatter block, OR frontmatter contains keys outside `name:` and `description:` (e.g. `tools:`, `capabilities:`, `required_tools:`, `permissions:`, `trust:`) |

**Detection — custom-key rejection:** the official Anthropic Agent Skills spec defines the frontmatter as `name` + `description` only. Any other key indicates either format drift (forward-compatibility risk) or a smuggling attempt. Treat any custom frontmatter key as `FAIL`, classify as **P0** when the key looks security-sensitive (`permissions:`, `trust:`, `capabilities:` with elevated scopes), **P1** otherwise. Escalate `P0` cases to `chain` for full intake audit. [Source: platform.claude.com — Agent Skills Overview; `_common/SECURITY.md`]

**Detection — body capability declaration:** scan the SKILL.md body (after frontmatter) for an explicit declaration of the tools / MCP servers / network hosts the skill expects to use. Acceptable formats include a `Tools used: Read, Edit, Bash` line, a "Network allowlist:" line, or a short paragraph naming the touchpoints. Absence of any such declaration is `PARTIAL` (not `FAIL`) because capability mismatch is detected at runtime by `chain` audits; the declaration here is an authoring expectation, not a hard runtime gate.

### F2: Description Discoverability (WHAT + WHEN)

| Status | Criteria |
|--------|----------|
| PASS | `description:` ≤1024 chars, English only, no XML angle brackets, contains BOTH a WHAT statement (capability — verb/noun phrase describing the agent's role) AND a WHEN trigger phrase (`"Use when ..."`, `"Triggers when ..."`, `"Use this for ..."`, `"... when X is needed"`, etc.) |
| PARTIAL | Description is well-formed but contains only WHAT or only WHEN (heuristic — not both) |
| FAIL | Description empty, >1024 chars, contains XML tags, contains Japanese characters, OR completely lacks both WHAT and WHEN |

**Detection — WHAT+WHEN heuristic:** Anthropic Complete Guide ("The description is critical for skill selection: Claude uses it to choose the right Skill from potentially 100+ available Skills") mandates both halves. The lint script's WHEN allowlist is intentionally broad (`when`, `use this`, `use to`, `trigger`, `for `, `needs`, `intended for`, `designed for`) and the WHAT allowlist favors role nouns (`agent`, `specialist`, `auditor`, `orchestrator`, ...). PARTIAL is the expected state for the majority of generation-1 skills; FAIL only fires on truly broken descriptions.

**Priority:** **P0** — description is the *single* routing signal. Misrouting cascades into wrong agent selection across the whole ecosystem.

**Source:** [platform.claude.com — Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf).

---

### L1: Language Compliance

| Status | Criteria |
|--------|----------|
| PASS | `description:` is in English; body (headings, text, tables, bullets) is in English; `reference/` files are English only |
| PARTIAL | Body contains minimal Japanese (1-3 instances) outside technical terms/proper nouns |
| FAIL | `description:` contains Japanese characters, or body contains significant Japanese text (4+ instances) |

**Detection:** Scan `description:` for Japanese characters (hiragana/katakana/kanji) — must be absent. Scan body for hiragana/katakana/kanji characters. Whitelist: agent names, tool names, technical terms, proper nouns.

### H1: CAPABILITIES_SUMMARY

| Status | Criteria |
|--------|----------|
| PASS | HTML comment block contains `CAPABILITIES_SUMMARY:` with 3+ capability entries in `key: description` format |
| PARTIAL | Block present but fewer than 3 entries or malformed format |
| FAIL | No CAPABILITIES_SUMMARY block |

### H2: COLLABORATION_PATTERNS

| Status | Criteria |
|--------|----------|
| PASS | HTML comment block contains `COLLABORATION_PATTERNS:` with directed patterns (Agent -> Agent: description) |
| PARTIAL | Block present but missing direction arrows or descriptions |
| FAIL | No COLLABORATION_PATTERNS block |

### H3: PROJECT_AFFINITY

| Status | Criteria |
|--------|----------|
| PASS | HTML comment block contains `PROJECT_AFFINITY:` with domain ratings (e.g., `Game(H) SaaS(L)`) or `universal` |
| PARTIAL | Block present but no ratings or `universal` keyword |
| FAIL | No PROJECT_AFFINITY line |

### S1: Trigger Guidance

| Status | Criteria |
|--------|----------|
| PASS | Section with heading containing "Trigger" exists; includes "Use X when" list AND "Route elsewhere" list |
| PARTIAL | Section exists but missing one of the two lists |
| FAIL | No Trigger Guidance section |

### S2: Core Contract

| Status | Criteria |
|--------|----------|
| PASS | Section with heading containing "Core Contract" or "Contract" exists; contains 3+ commitment items |
| PARTIAL | Section exists but fewer than 3 items |
| FAIL | No Core Contract section |

### S3: Boundaries

| Status | Criteria |
|--------|----------|
| PASS | Section contains all three subsections: Always, Ask (First), Never |
| PARTIAL | Section exists but missing one subsection |
| FAIL | No Boundaries section or missing two+ subsections |

### S4: Workflow

| Status | Criteria |
|--------|----------|
| PASS | Section contains phase pipeline (e.g., `PHASE1 → PHASE2 → ...`) AND phase table with columns |
| PARTIAL | Pipeline or table present but not both |
| FAIL | No Workflow section |

### S5: Output Routing

| Status | Criteria |
|--------|----------|
| PASS | Section contains signal-to-output routing table with columns: Signal, Approach/output, Read next |
| PARTIAL | Table present but missing columns or fewer than 3 routes |
| FAIL | No Output Routing section |

### S6: Output Requirements

| Status | Criteria |
|--------|----------|
| PASS | Section lists 3+ required elements for every deliverable |
| PARTIAL | Section exists but fewer than 3 elements |
| FAIL | No Output Requirements section |

### S7: Collaboration

| Status | Criteria |
|--------|----------|
| PASS | Section contains both `Receives:` and `Sends:` entries with agent names and context |
| PARTIAL | Section exists but missing Receives or Sends |
| FAIL | No Collaboration section |

### S8: Reference Map

| Status | Criteria |
|--------|----------|
| PASS | Section contains reference table with `Reference` and `Read this when` columns; all listed files exist in `reference/` |
| PARTIAL | Table present but incomplete or references missing |
| FAIL | No Reference Map section (N/A acceptable if agent has no `reference/` directory) |

### S9: Operational

| Status | Criteria |
|--------|----------|
| PASS | Section mentions journal file (`.agents/{name}.md`), PROJECT.md logging, and links to `_common/OPERATIONAL.md` |
| PARTIAL | Section exists but missing one of the three elements |
| FAIL | No Operational section |

### S10: Body Size Constraint

| Status | Criteria |
|--------|----------|
| PASS | SKILL.md body (lines after frontmatter closing `---`) ≤ 500 lines AND ~≤ 5000 tokens (approx via `chars / 3.5`) — meets Anthropic recommendation |
| PARTIAL | 500-700 lines OR 5000-10000 tokens — refactor candidate, move detail to `reference/` |
| FAIL | > 1000 lines OR > 15000 tokens (egregious — progressive disclosure not applied) |

**Detection:** Use the lint script's tiered output (S1 = line count, S2 = token estimate). Repository-tuned tiers:

| Lines | Tokens | Priority |
|-------|--------|----------|
| > 1000 | > 15000 | **P1** (egregious — block merge in CI) |
| 700-1000 | 10000-15000 | **P2** (refactor candidate) |
| 500-700 | 7000-10000 | **P3** (over Anthropic recommendation, informational) |

**Rationale:** Anthropic guidance is "Keep SKILL.md body under 500 lines for optimal performance" but the existing 148-skill corpus runs higher. Generation-3 audit tiers the thresholds so P0/P1 fire only on truly egregious sizes; refactor work is queued at P2/P3. As skills migrate detail to `reference/`, raise the floors over time.

**Source:** [platform.claude.com — Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf).

**Fix hints:**
- Move "Reference Map" entries' detail bodies to `reference/<topic>.md`
- Collapse long Recipes tables into a top-level table + per-recipe inline notes only
- Promote oversized "Core Contract" / "Boundaries" subsections into `reference/`
- Verify `_common/` protocol references are pointers, not inlined excerpts (the bytes are already cached)

---

### A1: AUTORUN Support (_STEP_COMPLETE)

| Status | Criteria |
|--------|----------|
| PASS | Section describes `_AGENT_CONTEXT` parsing AND contains `_STEP_COMPLETE` YAML block with Status, Output, Next, Reason fields |
| PARTIAL | Section exists but _STEP_COMPLETE block is incomplete |
| FAIL | No AUTORUN Support section |

### A2: Nexus Hub Mode (NEXUS_HANDOFF)

| Status | Criteria |
|--------|----------|
| PASS | Section describes `NEXUS_ROUTING` detection AND contains `NEXUS_HANDOFF` block with Step, Agent, Summary, Next action fields |
| PARTIAL | Section exists but NEXUS_HANDOFF block is incomplete |
| FAIL | No Nexus Hub Mode section |

---

## Priority Classification

| Priority | Scope | Items | Rationale |
|----------|-------|-------|-----------|
| **P0 (Critical)** | Ecosystem integration + routing | A1, A2, S7, **F2** | Required for AUTORUN execution, agent collaboration, **and skill selection** (F2: description is the single routing signal) |
| **P1 (High)** | Quality and consistency | S2, S3, S4, L1, **S10** | Core behavioral contract, safety boundaries, workflow definition, language standard, **body size egregious tier** |
| **P2 (Medium)** | Discoverability and routing | S1, S5, S6 | Trigger conditions, output routing, deliverable requirements |
| **P3 (Low)** | Metadata and reference | F1, H1, H2, H3, S8, S9 | Frontmatter, machine-readable metadata, reference pointers, operational logging |

### Priority-Based Fix Order

1. Fix all P0 violations first (ecosystem cannot function without these).
2. Fix P1 violations (quality and behavioral consistency).
3. Fix P2 violations (improve discoverability and routing accuracy).
4. Fix P3 violations (metadata completeness).

---

## Architect Exemplar Reference

Architect (`architect/SKILL.md`) is the reference standard for all 16 items. When generating fix snippets, cite the corresponding Architect section as exemplar:

| Item | Architect Section Reference |
|------|------------------------------|
| F1 | YAML frontmatter block (kebab-case name) |
| F2 | `description:` field (WHAT capability + WHEN trigger phrase) |
| L1 | Full file (English description, English body) |
| H1 | `CAPABILITIES_SUMMARY` comment block |
| H2 | `COLLABORATION_PATTERNS` comment block |
| H3 | `PROJECT_AFFINITY` comment line |
| S1 | "Trigger Guidance" section |
| S2 | "Core Contract" section |
| S3 | "Boundaries" section (Always/Ask First/Never) |
| S4 | "Workflow" section (pipeline + phase table) |
| S5 | "Output Routing" section (signal table + routing rules) |
| S6 | "Output Requirements" section |
| S7 | "Collaboration" section (Receives/Sends + overlap boundaries) |
| S8 | "Reference Map" section |
| S9 | "Operational" section |
| S10 | Body size ≤ 500 lines / ~5000 tokens |
| A1 | "AUTORUN Support" section (_STEP_COMPLETE YAML) |
| A2 | "Nexus Hub Mode" section (NEXUS_HANDOFF block) |

---

## R1: Recipes / Subcommand Dispatch (optional, RECOMMENDED for Tier 1-2)

| Status | Criteria |
|--------|----------|
| PASS | `## Recipes` table present AND `## Subcommand Dispatch` section present (bare heading, no parenthetical suffix) AND exactly one row marked `✓` in Default? column AND every Subcommand matches `^[a-z][a-z0-9-]{1,15}$` AND no reserved words (default/auto/help/list) AND ≤ 7 recipes |
| PARTIAL | Recipes section present but with warnings only (>7 recipes) OR minor formatting drift recoverable by `python3 _common/scripts/validate-recipes.py` |
| FAIL | Any of: `## Recipes` exists without `## Subcommand Dispatch`; decorated heading `## Subcommand Dispatch (default: xxx)`; multiple or zero ✓ defaults; reserved word used as subcommand; kebab-case violation; duplicate subcommands within the skill |
| SKIP | Skill intentionally omits Recipes (Tier 3 or <3 distinct modes) — record as INFO, not FAIL |

**Detection:** Run `python3 _common/scripts/validate-recipes.py`. Parse its ERROR/WARN/INFO output per skill. Canonical protocol: `_common/RECIPES.md`.

**Priority:** P2 (quality hygiene). Heading integrity (H-REC-01/02) and Default count (R-REC-01) uplift to **P1** because they break the Subcommand Dispatch contract end-users rely on.

**Fix hints:**
- Missing `## Subcommand Dispatch` → append a standard dispatch block (see `_common/RECIPES.md` §SKILL.md Structure)
- Decorated heading → `sed -i '' 's/^## Subcommand Dispatch (default: [a-z0-9-]*)$/## Subcommand Dispatch/'`
- `compass/reference/recipes-directory.md` stale → `python3 _common/scripts/generate-recipes-directory.py`
