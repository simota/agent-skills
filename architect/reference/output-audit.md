# Runtime Output Audit

Read for `audit-verbosity`. Audit 1–5 real runtime responses supplied or explicitly made available by the user. With zero samples, refuse the audit; SKILL.md templates and invented outputs are not observations. Use `_common/OUTPUT_STYLE.md` for tier definitions and exclude protocol envelopes from response measurements.

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
