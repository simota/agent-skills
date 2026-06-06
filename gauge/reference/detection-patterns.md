# Detection Patterns

**Purpose:** Structural detection rules for each of the 16 checklist items.
**Read when:** Executing the CLASSIFY phase of the audit workflow.

---

## F1: YAML Frontmatter

**Detection:**
1. Check first line is exactly `---`
2. Scan for closing `---` (second occurrence)
3. Between delimiters, check for `name:` field (non-empty)
4. Between delimiters, check for `description:` field (non-empty)
5. Validate `name:` value is kebab-case: regex `^[a-z0-9]+(-[a-z0-9]+)*$` (no spaces, no capitals, no underscores — per official Agent Skills spec)
6. Validate `name:` value does not use reserved prefixes (`claude`, `anthropic`)
7. Check `description:` does not contain XML angle brackets (`<`, `>`) — frontmatter appears in system prompt; prevents injection

**PARTIAL trigger:** Delimiters present but `name:` or `description:` missing/empty, OR `name:` not in kebab-case.
**Note:** All names must be kebab-case matching the directory name. PascalCase grandfathering is no longer in effect (migration completed in Generation 2).

---

## F2: Description Discoverability (WHAT + WHEN)

**Detection:**
1. Extract `description:` value from frontmatter.
2. Verify length ≤ 1024 characters (Anthropic spec hard limit).
3. Verify no XML angle brackets (`<`, `>`) — frontmatter is injected into system prompt.
4. Verify no Japanese characters (must be English per L1).
5. **WHEN check:** description (case-insensitive) contains one of: `when`, `use this`, `use it`, `use to`, `use for`, `trigger`, `needs`, `needed`, `intended for`, `designed for`, ` for `, `applies`.
6. **WHAT check:** description (case-insensitive) contains a role/capability noun (e.g. `agent`, `specialist`, `auditor`, `orchestrator`, `expert`, `framework`, `generator`, `tool`, `analyzer`, `design`, `build`, `create`, `generate`, `review`, `implement`), OR the first clause (before `.` or newline) is ≥ 30 chars (verb-led capability statement fallback).

**PASS:** WHAT and WHEN both present, hard-limit checks pass.
**PARTIAL:** Hard-limit checks pass but WHAT or WHEN missing (heuristic — many generation-1 skills are "WHAT-only").
**FAIL:** Description empty, > 1024 chars, contains XML tags, or contains Japanese characters.

**Tooling:** Use `python3 _common/scripts/lint-frontmatter.py --severity warning`. The script emits `F2` findings as PARTIAL (P2) for heuristic violations and FAIL (P0) for hard-limit violations.

**Anti-pattern examples:**
- `"E2E testing specialist for Playwright/Cypress"` — WHAT only (no WHEN clause). PARTIAL.
- `"Use this for E2E tests"` — WHEN only (no role noun). PARTIAL.
- `"E2E testing specialist for web (Playwright/Cypress) and mobile (Appium). Use when designing test suites, debugging flaky tests, or setting up CI integration."` — PASS (both halves present, concrete trigger).
- `""` (empty), `"<E2E spec>"` (XML), `"E2E テスト専門"` (Japanese) — FAIL.

---

## L1: Language Compliance

**Detection:**
1. Extract `description:` value from frontmatter → verify it is English (no Japanese characters: hiragana `\u3040-\u309F`, katakana `\u30A0-\u30FF`, kanji `\u4E00-\u9FFF`)
2. Extract body text (everything after frontmatter closing `---`)
3. Scan body for Japanese character ranges (same as above)
4. Apply whitelist exclusions:
   - Agent names (e.g., `Nexus`, `Architect`)
   - Technical identifiers (e.g., `_STEP_COMPLETE`, `NEXUS_HANDOFF`)
   - Quoted proper nouns
5. Scan `reference/` files for Japanese characters (none allowed)

**PARTIAL trigger:** 1-3 Japanese character instances in body after whitelist filtering.
**FAIL trigger:** `description:` contains Japanese characters, OR 4+ instances in body, OR `reference/` files contain Japanese.

---

## H1: CAPABILITIES_SUMMARY

**Detection:**
1. Scan for HTML comment block: `<!--` ... `-->`
2. Within comment, search for `CAPABILITIES_SUMMARY:` keyword
3. After keyword, count entries matching pattern: `- key: description`
4. Verify minimum 3 entries

**PARTIAL trigger:** Keyword found but fewer than 3 entries or entries lack `key: description` format.

---

## H2: COLLABORATION_PATTERNS

**Detection:**
1. Within HTML comment block, search for `COLLABORATION_PATTERNS:` keyword
2. After keyword, count entries matching pattern: `- Agent -> Agent: description` or `- Agent → Agent: description`
3. Also check for `BIDIRECTIONAL_PARTNERS:` subsection with `INPUT:` and `OUTPUT:` lines

**PARTIAL trigger:** Keyword found but missing direction arrows, agent names, or descriptions.

---

## H3: PROJECT_AFFINITY

**Detection:**
1. Within HTML comment block, search for `PROJECT_AFFINITY:` keyword
2. After keyword, check for either:
   - `universal` keyword, OR
   - Domain ratings in format `Domain(H|M|L)` (minimum 1)

**PARTIAL trigger:** Keyword found but no ratings and no `universal` keyword.

---

## S1: Trigger Guidance

**Detection:**
1. Search for heading matching: `## Trigger Guidance` or `## Trigger` (case-insensitive)
2. Under heading, search for "Use" + agent name + "when" pattern (positive triggers)
3. Search for "Route elsewhere" or "Route to" pattern (negative routing)

**PARTIAL trigger:** Heading exists but missing positive triggers or negative routing.

---

## S2: Core Contract

**Detection:**
1. Search for heading matching: `## Core Contract` or `## Contract` (case-insensitive)
2. Count bullet points or numbered items under heading
3. Verify minimum 3 items

**PARTIAL trigger:** Heading exists but fewer than 3 contract items.

---

## S3: Boundaries

**Detection:**
1. Search for heading matching: `## Boundaries` (case-insensitive)
2. Under heading, search for three subsections:
   - `### Always` or `**Always**` or `**Always:**`
   - `### Ask` or `**Ask**` or `**Ask First**` or `**Ask First:**`
   - `### Never` or `**Never**` or `**Never:**`
3. Verify each subsection has at least 1 item

**PARTIAL trigger:** Boundaries heading exists but one subsection missing or empty.
**FAIL trigger:** No Boundaries heading, or 2+ subsections missing.

---

## S4: Workflow

**Detection:**
1. Search for heading matching: `## Workflow` (case-insensitive)
2. Search for phase pipeline pattern: text containing `→` or `->` with 2+ phase names (typically backtick-wrapped)
3. Search for phase table: markdown table with columns including "Phase" and at least one of "Action", "Rule", "Read"

**PARTIAL trigger:** Pipeline or table present but not both.

---

## S5: Output Routing

**Detection:**
1. Search for heading matching: `## Output Routing` (case-insensitive)
2. Search for routing table: markdown table with columns including "Signal" and at least one of "Approach", "Output", "Read"
3. Count table rows (minimum 3)

**PARTIAL trigger:** Table present but missing key columns or fewer than 3 routes.

---

## S6: Output Requirements

**Detection:**
1. Search for heading matching: `## Output Requirements` (case-insensitive)
2. Count bullet points or numbered items under heading
3. Verify minimum 3 items

**PARTIAL trigger:** Heading exists but fewer than 3 requirement items.

---

## S7: Collaboration

**Detection:**
1. Search for heading matching: `## Collaboration` (case-insensitive)
2. Search for `Receives:` or `**Receives:**` pattern with agent names
3. Search for `Sends:` or `**Sends:**` pattern with agent names

**PARTIAL trigger:** Heading exists but missing either Receives or Sends.

---

## S8: Reference Map

**Detection:**
1. Search for heading matching: `## Reference Map` or `## References` (case-insensitive)
2. Search for table with columns: "Reference" (or "File") and "Read this when" (or "Content", "When")
3. Verify listed files exist in `reference/` directory

**Special case:** If the agent has no `reference/` directory, explicit "N/A" or "No references" is acceptable as PASS.

**PARTIAL trigger:** Table present but references point to non-existent files.

---

## S9: Operational

**Detection:**
1. Search for heading matching: `## Operational` (case-insensitive)
2. Check for journal mention: `.agents/{agent_name}.md` pattern
3. Check for PROJECT.md mention: `.agents/PROJECT.md` or `PROJECT.md` pattern
4. Check for standard protocols link: `_common/OPERATIONAL.md` pattern

**PARTIAL trigger:** Heading exists but missing one of the three elements.

---

## S10: Body Size Constraint

**Detection:**
1. Read SKILL.md, locate frontmatter closing `---`. Lines after that constitute the body.
2. Compute `line_count = len(body_lines)`.
3. Compute `token_estimate = max(1, int(len(body_text) / 3.5))` (tiktoken-free heuristic; ~3.5 chars/token for mixed Markdown+English).
4. Tier the finding (repository-tuned, see normalization-checklist.md S10):

| Lines | Tokens | Verdict | Priority |
|-------|--------|---------|----------|
| > 1000 | > 15000 | FAIL (egregious) | P1 |
| 700-1000 | 10000-15000 | PARTIAL (refactor candidate) | P2 |
| 500-700 | 7000-10000 | PARTIAL (informational) | P3 |
| ≤ 500 | ≤ 7000 | PASS | — |

**Tooling:** `python3 _common/scripts/lint-frontmatter.py --severity warning` emits findings as `S1` (line count) and `S2` (token estimate) — one finding per dimension. Treat both as inputs to S10.

**Rationale:** Anthropic explicit guidance: "Keep SKILL.md body under 500 lines for optimal performance". Tiering exists because the existing 148-skill corpus runs higher; FAIL only fires on truly oversized files so CI doesn't choke on legacy violations.

**Fix hints:**
- Move detail sections (e.g. long `## Boundaries`, oversized recipe descriptions, full `## Workflow` phase notes) to `reference/<topic>.md`.
- Replace inline `_common/` excerpts with pointers — the bytes are already cached in `_common/`.
- Collapse multi-recipe inline notes into a `## Recipes` table + per-recipe `Read` reference.

---

## A1: AUTORUN Support (_STEP_COMPLETE)

**Detection:**
1. Search for heading matching: `## AUTORUN` (case-insensitive)
2. Search for `_AGENT_CONTEXT` keyword in section body
3. Search for `_STEP_COMPLETE` keyword
4. Within _STEP_COMPLETE block, verify presence of:
   - `Agent:` field
   - `Status:` field with `SUCCESS | PARTIAL | BLOCKED | FAILED`
   - `Output:` block
   - `Next:` field
   - `Reason:` field

**PARTIAL trigger:** Section exists but _STEP_COMPLETE block missing required fields.

---

## A2: Nexus Hub Mode (NEXUS_HANDOFF)

**Detection:**
1. Search for heading matching: `## Nexus Hub Mode` or `## Nexus` (case-insensitive, must relate to hub mode)
2. Search for `NEXUS_ROUTING` keyword in section body
3. Search for `NEXUS_HANDOFF` keyword
4. Within NEXUS_HANDOFF block, verify presence of:
   - `Step:` field
   - `Agent:` field
   - `Summary:` field
   - `Next action:` field with `CONTINUE | VERIFY | DONE`

**PARTIAL trigger:** Section exists but NEXUS_HANDOFF block missing required fields.

---

## Compound Detection Rules

### Full HTML Comment Block Validation (H1 + H2 + H3)

All three items (H1, H2, H3) must reside within a single HTML comment block (`<!-- ... -->`). If no HTML comment block exists, all three are FAIL. If the block exists but is missing individual sections, score each independently.

### Language Compliance Cross-Check (L1)

L1 applies across all sections and references. When auditing any section (S1-S9), simultaneously check for Japanese text violations. This avoids a second pass.
