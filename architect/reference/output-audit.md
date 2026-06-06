# Output Audit Reference

**Purpose:** Score runtime output verbosity for an agent and propose Output Contract corrections.
**Read when:** You are running Architect's `audit-verbosity` recipe on a verbose agent's responses.
**Distinct from:** `context-compression.md` (SKILL.md file size) and `validation-checklist.md` §8 (declaration check).

## Contents
- Overview
- Scoring Method
- OUTPUT_AUDIT_REPORT Template
- Workflow
- Decision Rules
- Examples

---

## Overview

Skills can pass `validation-checklist.md` §8 (declared an Output Contract) yet still emit verbose responses. Audit closes that gap: take real output samples, measure density, and propose SKILL.md edits.

Inputs:
- Target skill name
- 1–5 representative output samples (recent runs)
- Current `Output Contract` declaration (default tier, overrides)

Outputs:
- `OUTPUT_AUDIT_REPORT` with quantitative scores
- Concrete diff proposals for the skill's `Output Contract` and (if needed) `Domain bans`
- Severity verdict: `PASS` / `WARN` / `FAIL`

---

## Scoring Method

Five metrics, each computed from the sample text excluding `_STEP_COMPLETE` and `NEXUS_HANDOFF` envelopes.

| Metric | Formula | Pass | Warn | Fail |
|--------|---------|------|------|------|
| `filler_ratio` | filler_lines / total_lines | < 8% | 8–15% | > 15% |
| `tier_compliance` | (samples within declared tier) / samples | 100% | 75–99% | < 75% |
| `format_priority` | structured_blocks / structurable_blocks | > 70% | 40–70% | < 40% |
| `header_echo_count` | unique-header echoes per response | ≤ 1 | 2–3 | ≥ 4 |
| `tautology_count` | restatement/closer phrases per response | 0–1 | 2–3 | ≥ 4 |

### Definitions

- **filler_lines**: lines matching banned patterns from `_common/OUTPUT_STYLE.md` (preamble, request restatement, tautological closers, hedging stacks, capability advertising).
- **structured_blocks**: tables, code blocks, bullet lists actually used.
- **structurable_blocks**: 3+ line prose that compares ≥3 attributes or enumerates ≥3 items (could have been a table/list).
- **header_echo**: response header that is verbatim a SKILL.md section title, used without need.
- **tautology**: "I have completed…", "ご依頼の…を実施しました", "以上で…完了です" type phrases.

### Aggregate verdict

```
FAIL  if any metric is FAIL
WARN  else if ≥2 metrics are WARN
PASS  else
```

---

## OUTPUT_AUDIT_REPORT Template

```yaml
OUTPUT_AUDIT_REPORT:
  agent: "[skill name]"
  date: "[YYYY-MM-DD]"
  samples:
    count: [N]
    source: "[user transcript / explicit user-provided samples]"
  declared_contract:
    default_tier: "[S | M | L | XL]"
    overrides:
      - task: "[task]"
        tier: "[tier]"
  metrics:
    filler_ratio:
      value: "[X%]"
      verdict: PASS | WARN | FAIL
      examples: ["[snippet]"]
    tier_compliance:
      value: "[X%]"
      verdict: PASS | WARN | FAIL
      breaches:
        - sample: 1
          declared: M
          observed_lines: 47
    format_priority:
      value: "[X%]"
      verdict: PASS | WARN | FAIL
      missed_opportunities: ["[3-line prose that should be table]"]
    header_echo_count:
      value: [n]
      verdict: PASS | WARN | FAIL
    tautology_count:
      value: [n]
      verdict: PASS | WARN | FAIL
  aggregate: PASS | WARN | FAIL
  proposals:
    - id: 1
      type: contract_update | domain_ban | tier_adjust | override_add
      target_section: "Output Contract"
      diff: |
        - Default tier: M
        + Default tier: S
        + Task overrides:
        +   - generate-report: M
      rationale: "[why this change]"
  next_steps:
    - "[concrete follow-up, e.g., 'IMPROVE recipe to apply diff']"
```

---

## Workflow

```
COLLECT → MEASURE → PROPOSE → HANDOFF
```

| Phase | Action |
|-------|--------|
| `COLLECT` | Receive ≥1 output sample. Refuse if 0 samples (require empirical input — never grade on speculation). |
| `MEASURE` | Apply 5 metrics. Cite the offending lines from samples in the report. |
| `PROPOSE` | Generate concrete diffs. Prefer tier-adjust > override-add > domain-ban > rewrite. |
| `HANDOFF` | Emit `OUTPUT_AUDIT_REPORT`. If aggregate is FAIL/WARN, suggest IMPROVE recipe handoff. |

---

## Decision Rules

### Choose tier adjustment when:
- `tier_compliance < 75%` AND samples consistently exceed declared tier → tier was wrong from the start (declared too small).
- `tier_compliance < 75%` AND samples are well *under* declared tier → tier was over-allocated, drop a tier.

### Choose override addition when:
- Specific task types systematically violate the default tier in one direction → add per-task override rather than changing default.

### Choose domain-ban addition when:
- Same filler phrase appears in 3+ samples → escalate to skill-specific ban list, not just generic OUTPUT_STYLE rules.
- Header echo for a specific section name appears repeatedly → ban echoing that header.

### Reject the audit when:
- Samples are not actual outputs (e.g., are SKILL.md excerpts, internal notes, code).
- `_STEP_COMPLETE` / `NEXUS_HANDOFF` blocks dominate samples — those envelopes are exempt; require user-facing samples.
- Sample count = 0 — the audit is empirical; do not score on imagined outputs.

---

## Examples

### Example 1: tier mismatch

```
Sample: 47-line response for a status lookup
Declared: default_tier = M (5-15 lines)
Observed: tier_compliance = 0% on 3/3 samples
Diagnosis: status-lookup task should be S, not M
Proposal:
  - Add task override: status-lookup → S
  - Default tier unchanged
```

### Example 2: filler-heavy generator

```
Sample: 65-line response for L-tier deliverable
Declared: default_tier = L
Observed: filler_ratio = 22% (preamble + closing summary)
Diagnosis: tier is fine; banned patterns leak through
Proposal:
  - Add to Domain bans: "Do not include 'Let me now generate…' preamble — start with the deliverable."
  - Add to Domain bans: "Do not append closing summary — output ends at the last deliverable line."
```

### Example 3: header echo problem

```
Sample: response mirrors SKILL.md "Analysis / Proposal / Risks" headers in every output regardless of task
Observed: header_echo_count = 3 per sample
Diagnosis: structural mirroring not warranted at this tier
Proposal:
  - Add to Domain bans: "Headers (Analysis/Proposal/Risks) only at L tier; M tier uses bullet-prefixed claims."
```

---

## Integration

- **Calling agent**: Architect via `audit-verbosity` recipe.
- **Upstream input**: User provides samples, or Judge surfaces verbose outputs as feedback (`JUDGE_TO_ARCHITECT_FEEDBACK`).
- **Downstream**: `IMPROVE` recipe applies the proposed diffs to the skill's SKILL.md (small change, often Safety Level A or B).
- **Logging**: Append audit results to `.agents/architect.md` only if a non-trivial pattern emerges across multiple skills.
