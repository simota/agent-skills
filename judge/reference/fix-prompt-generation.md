# Judge LLM Fix Prompt Generation

**Purpose:** Judge-specific action verbs, suppression cases, template fields for the `## LLM Fix Prompt` block that pairs each consensus-level Judge finding with a paste-ready instruction prompt for the receiving agent (typically Builder).
**Read when:** Judge has shipped a VERIFIED finding (3/3 CONFIRMED, 2/3 LIKELY, or 1/3 grounded CANDIDATE that survived FILTER) and the finding warrants downstream action rather than escalation to a specialist.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Judge-specific verbs, suppression cases, template fields.

## When Judge Emits a Fix Prompt vs Suppresses

Judge is review-only — it does not ship code. The Fix Prompt is the bridge between Judge's report and the receiving agent (Builder, Atlas, etc.). Pair it with every shipped consensus-level finding; suppress it for nit-only output and for findings escalated to a specialist that owns its own remediation prompt.

| Situation | Action |
|-----------|--------|
| Finding is CONFIRMED (3/3) or LIKELY (2/3) and warrants a fix in the same PR | Emit Fix Prompt with `APPLY-FIX` (or appropriate scoped verb) → Builder |
| Finding is grounded CANDIDATE (1/3 verified by Judge main context read) | Emit Fix Prompt with `APPLY-FIX` if HIGH-confidence after grounding; otherwise `INVESTIGATE-FURTHER` |
| Finding requires significant rework (design or approach is wrong) | Emit Fix Prompt with `REWRITE` → Builder + Atlas |
| PR is fundamentally wrong; restart from spec rather than patch | Emit Fix Prompt with `REVERT-AND-RESTART` → Builder + Scribe/Scribe[unified] |
| Review identifies need for API or contract change | Emit Fix Prompt with `BREAKING-FIX` → Builder + Guardian + Launch |
| Review confidence MEDIUM; need to verify finding before changing code | Emit Fix Prompt with `INVESTIGATE-FURTHER` → Builder (investigation mode) or Judge re-entry with more engines |
| Finding flagged but not blocking; advisory only | Emit Fix Prompt with `DOWNGRADE` → Builder (advisory, no enforcement) |
| Finding is nit-only / style-only (no behavioral concern) | **Suppress Fix Prompt.** Note `Fix prompt N/A — nit-level feedback only; author's discretion.` |
| Security smell detected during review | **Suppress Fix Prompt** — escalate to Sentinel (Sentinel owns remediation prompt) |
| Refactoring suggestion, no bug | **Suppress Fix Prompt** — route to Zen (Zen owns refactoring) |
| Single-engine finding without consensus and grounding inconclusive | **Suppress Fix Prompt** — require consensus before action |

The Fix Prompt is required for every consensus-level finding that ships in the main findings list. Silent omission breaks downstream Builder expectations.

---

## Judge Action Verbs

Each fix prompt declares one verb at the top of `# Your task`.

| Verb | When to use | Receiving agent |
|------|-------------|----------------|
| `APPLY-FIX` | Confirmed bug/issue in PR, scoped fix in same PR (HIGH confidence, multi-engine consensus) | Builder (PR author) |
| `REWRITE` | Implementation needs significant rework — design or approach is wrong | Builder + Atlas |
| `REVERT-AND-RESTART` | PR is fundamentally wrong; restart from spec rather than patch | Builder + Scribe/Scribe[unified] |
| `BREAKING-FIX` | Review identifies need for API or contract change | Builder + Guardian + Launch |
| `INVESTIGATE-FURTHER` | Review confidence MEDIUM; need to verify finding before changing code | Builder (in investigation mode) or Judge re-entry with more engines |
| `DOWNGRADE` | Finding flagged but not blocking; author should consider but may defer | Builder (advisory only — no enforcement) |

---

## Verb Selection Heuristic

```
Engine concurrence + grounding ─┬─ 3/3 CONFIRMED, scoped fix ──────→ APPLY-FIX
                                ├─ 2/3 LIKELY, scoped fix ─────────→ APPLY-FIX
                                ├─ 1/3 grounded VERIFIED ──────────→ APPLY-FIX or INVESTIGATE-FURTHER
                                └─ grounding inconclusive ─────────→ INVESTIGATE-FURTHER

Scope of fix ─┬─ same PR, < 100 lines, no breaking ──────────────→ APPLY-FIX
              ├─ design/approach wrong, multi-file rework ───────→ REWRITE
              ├─ PR premise wrong, easier to restart from spec ──→ REVERT-AND-RESTART
              └─ requires API/contract change ──────────────────→ BREAKING-FIX

Severity ─┬─ bug-blocking ──────────────────────────────────────→ APPLY-FIX (or REWRITE)
          ├─ bug-non-blocking ──────────────────────────────────→ APPLY-FIX
          ├─ smell ─────────────────────────────────────────────→ DOWNGRADE (advisory)
          └─ style ─────────────────────────────────────────────→ Suppress (route to Zen)
```

Tiebreakers:
- 3/3 CONFIRMED + bug-blocking → always `APPLY-FIX`. Multi-engine consensus on a blocking bug is the highest-confidence Judge signal; no investigation needed.
- `BREAKING-FIX` always cross-links to Guardian + Launch — breaking changes need release coordination and PR-classification re-review.
- `REVERT-AND-RESTART` is reserved for cases where the PR's premise is wrong (wrong spec interpretation, wrong feature scope, wrong architectural decision). Cross-link to Scribe (spec rewrite) or Scribe[unified] (specification alignment) so the restart has a corrected baseline.
- `INVESTIGATE-FURTHER` for 1/3 findings: only emit if the grounding read surfaced corroborating evidence; otherwise suppress (single-engine without consensus is below shipping bar).

---

## Judge-Specific Suppression Cases

Universal cases live in `_common/LLM_PROMPT_GENERATION.md`. Judge adds:

| Case | Reason | Note in report |
|------|--------|----------------|
| Judge ships nit-only / style-only feedback (no behavioral concern) | Style is Zen's domain; nit-level feedback should not block or pre-formulate fixes | "Fix prompt N/A — nit-level feedback only; author's discretion." |
| Judge escalates to Sentinel (security smell detected during review) | Sentinel owns the security remediation prompt with OWASP/CWE classification | "Fix prompt suppressed — Sentinel owns security remediation prompt." |
| Judge escalates to Zen (refactoring suggestion, no bug) | Zen owns refactoring; pre-formulated fix prompt would constrain Zen's analysis | "Fix prompt withheld — finding routed to Zen as refactoring suggestion." |
| Single-engine finding without consensus (LOW confidence) | Acting on un-grounded single-engine findings erodes Judge's signal-to-noise ratio | "Fix prompt withheld — single-engine finding; require consensus before action." |

In all suppression cases, write the one-line note in the report. Silent omission breaks downstream expectations and makes the suppression invisible to the PR author.

---

## Per-Finding Fix Prompt Template (Judge Fields)

Judge adds these Judge-specific blocks on top of the universal skeleton:

- `Engine consensus` — which of {Codex, Antigravity, Claude Code} flagged this; consensus level (3/3, 2/3, 1/3-grounded)
- `Grounding evidence` — file:line references that ground the finding in actual code (Judge requires grounded findings)
- `PR context` — PR title/branch + diff hunks where the finding lives
- `Severity` — `bug-blocking | bug-non-blocking | smell | style` (Judge's behavioral severity, separate from CRITICAL/HIGH/MEDIUM/LOW classification)
- For `REWRITE` — `Design concern` section explaining why a one-line patch is insufficient
- For `REVERT-AND-RESTART` — `Spec gap` section identifying which spec/requirement was misinterpreted
- For `BREAKING-FIX` — `User-facing impact` and `Rollback plan` sections (mirrors Sentinel)
- For `INVESTIGATE-FURTHER` — replace `# Recommended action` with `# Verification plan`

````markdown
## LLM Fix Prompt

```text
# Your task
<VERB> the review finding described below.

# Finding context
- Title: [brief description]
- Severity: [bug-blocking | bug-non-blocking | smell | style]
- Classification: [CRITICAL | HIGH | MEDIUM | LOW | INFO]
- Engine consensus: [3/3 CONFIRMED | 2/3 LIKELY | 1/3-grounded VERIFIED] — [list engines]
- PR: [PR title or branch]
- Diff hunk: [file:line-range of the change being reviewed]

# Defect
[What the bug/issue is and how it manifests]

Location: `<file>:<line>` in `<function>()`

# Grounding evidence
Code as it stands today:
```
[verbatim code snippet showing the defect]
```

Why this is a defect:
- [reasoning grounded in actual code, not engine output]
- [trace through execution / data flow that exhibits the issue]

Engine outputs (for traceability — do NOT re-litigate):
- Codex: [summary of codex finding, if any]
- Gemini: [summary of agy finding, if any]
- Claude Code: [summary of claude finding, if any]

# Recommended action
Approach: [strategy — minimal scoped change to address the defect]
Files to modify: [list with expected change per file]
Constraints:
- [coupling, side effect, or backward-compat note]
- [test additions required]

# [REWRITE only — Design concern]
- Why a one-line patch is insufficient: [structural reason]
- Recommended design direction: [high-level approach]
- Atlas consultation needed: [yes/no — if yes, what question]

# [REVERT-AND-RESTART only — Spec gap]
- Spec/requirement misinterpreted: [reference to spec section]
- Corrected interpretation: [what the spec actually requires]
- Restart baseline: [Scribe/Scribe[unified] deliverable to consume before re-implementing]

# [BREAKING-FIX only — User-facing impact]
- API shape change: [yes/no — describe]
- Client breaking change: [yes/no — describe]
- Migration steps for clients: [list]

# [BREAKING-FIX only — Rollback plan]
- How to revert: [git revert SHA, feature flag toggle, etc.]
- Pre-deploy verification: [staging test, canary, etc.]
- Comms required: [release notes section, breaking change advisory, etc.]

# Acceptance criteria
- [ ] Defect no longer reproduces (verifiable by [test / scenario])
- [ ] Regression test added covering the defect's trigger
- [ ] No new test failures in the affected module
- [ ] Engine consensus re-runs (if requested) confirm finding is resolved
- [ ] [REWRITE] Atlas review of new design direction completed

# Ruled-out alternatives (do not revisit)
- [alternative 1] — eliminated because [evidence, e.g., engine cross-check showed this approach has same defect]
- [alternative 2] — eliminated because [evidence]

# What NOT to do
- Do not silence the symptom (catch-and-ignore, swallow logs, suppress the warning)
- Do not expand scope beyond the cited files unless evidence demands it
- Do not bundle unrelated changes (style fixes, refactors, copy edits) into this PR
- Do not re-litigate the engine outputs above — Judge has already grounded this finding
- [domain-specific anti-action]
```
````

For `INVESTIGATE-FURTHER`, replace `# Recommended action` with `# Verification plan`:

```text
# Verification plan
Steps to confirm or refute the finding before changing code:
1. [reproduction step — exact command, input, or scenario]
2. [observation point — what to capture]
3. [decision criterion — what confirms the defect; what refutes it]

Engines to re-run (if applicable): [list]
```

For `DOWNGRADE`, the prompt is advisory; soften acceptance criteria to "consider":

```text
# Acceptance criteria (advisory)
- [ ] Author has read this finding and decided whether to address now or later
- [ ] If deferred, a tracking issue / TODO is filed referencing this finding ID
```

---
