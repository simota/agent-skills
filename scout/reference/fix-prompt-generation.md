# Scout LLM Fix Prompt Generation

**Purpose:** Scout-specific action verbs, suppression cases, template fields for the `## LLM Fix Prompt` block at the end of every Scout investigation report.
**Read when:** You are writing the `## LLM Fix Prompt` block for a Scout report, choosing an action verb, or deciding whether to suppress.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Scout-specific verbs, suppression cases, template fields.

## Scout Action Verbs

Compact reference (SKILL.md keeps only this row set; full "when/receiving" detail below): `FIX`, `FIX-WITH-TEST`, `MITIGATE`, `INVESTIGATE-FURTHER`, `REFACTOR-FIX`.

Each fix prompt declares one verb at the top of `# Your task`.

| Verb | When to use | Receiving agent / LLM |
|------|-------------|----------------------|
| `FIX` | HIGH confidence, scoped to identified files, no security/concurrency concern | Builder, Claude, Codex |
| `FIX-WITH-TEST` | HIGH confidence + Scout has Radar-quality regression test specs to bundle | Builder + Radar (combined session) |
| `MITIGATE` | Workaround only — root cause is out of scope, blocked, or owned by another team | Builder |
| `INVESTIGATE-FURTHER` | LOW or MEDIUM confidence — receiving LLM must reproduce and verify hypothesis before changing code | Claude / Codex (investigation mode), or Scout (re-entry) |
| `REFACTOR-FIX` | Fix requires structural change beyond a single function; needs architecture review first | Atlas → Builder |

---

## Verb Selection Heuristic

```
Confidence == HIGH ─┬─ scoped fix, no escalation needed ──→ FIX
                    ├─ regression test bundled with fix ──→ FIX-WITH-TEST
                    └─ structural refactor required ─────→ REFACTOR-FIX

Confidence == MEDIUM ─→ INVESTIGATE-FURTHER (or FIX with verification gate)

Confidence == LOW ───→ INVESTIGATE-FURTHER (always)

Root cause out of scope / blocked ──→ MITIGATE
```

Tiebreakers:
- If Scout escalates to Sentinel, do not emit a fix prompt — see suppression below.
- If the bug spans 4+ files and reflects a design issue, prefer `REFACTOR-FIX` over `FIX`.
- If reproduction failed but root cause is strongly hypothesized (MEDIUM evidence), prefer `INVESTIGATE-FURTHER` over `FIX` to force the receiving LLM to confirm the symptom first.

---

## Scout-Specific Suppression Cases

Universal cases live in `_common/LLM_PROMPT_GENERATION.md`. Scout adds:

| Case | Reason | Note in report |
|------|--------|----------------|
| Scout escalates to Sentinel (security suspicion) | Sentinel owns secure-fix prompts | "Fix prompt suppressed — Sentinel owns remediation prompt." |

---

## Per-Bug Fix Prompt Template (Scout Fields)

Scout adds three Scout-specific blocks on top of the universal skeleton:

- `Reproduction` — numbered repro steps + Expected/Actual + verbatim error/log signature
- `Ruled-out hypotheses` — Scout's documented dead ends with eliminating evidence
- Scout-specific anti-actions in `What NOT to do` (e.g., do not refactor unrelated code)

````markdown
## LLM Fix Prompt

```text
# Your task
<VERB> the bug described below.

# Bug context
- Title: [brief description]
- Severity: [Critical | High | Medium | Low]
- Reproducibility: [Always | Sometimes | Rare]
- Confidence: [HIGH | MEDIUM | LOW] (Scout's diagnostic confidence)

# Root cause
[Cause description — what condition triggers the bug]

Location: `<file>:<line>` in `<function>()`

# Reproduction
1. [Step 1]
2. [Step 2]

Expected: [what should happen]
Actual: [what actually happens]

Exact error / log signature (search for this string):
```
[verbatim error message or log line]
```

# Recommended fix
Approach: [high-level fix strategy]
Files to modify: [list with expected change per file]
Constraints:
- [side effect / backward-compat note]

# Acceptance criteria
- [ ] Reproduction steps above no longer trigger the failure
- [ ] Regression test added covering the failure condition
- [ ] No new test failures in the affected module

# Ruled-out hypotheses (do not revisit)
- [hypothesis 1] — eliminated because [evidence]
- [hypothesis 2] — eliminated because [evidence]

# What NOT to do
- Do not silence the symptom (catch-and-ignore, swallow logs, suppress the error)
- Do not expand scope beyond the cited files unless evidence demands it
- Do not change unrelated code paths in the same commit
```
````

For `INVESTIGATE-FURTHER`, replace "Recommended fix" with "Verification plan". For `MITIGATE`, add "Root cause status". For `REFACTOR-FIX`, add "Structural concern".

---
