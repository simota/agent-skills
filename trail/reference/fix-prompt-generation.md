# Trail LLM Fix Prompt Generation

**Purpose:** Trail-specific action verbs, suppression cases, template fields for the `## LLM Fix Prompt` block at the end of every Trail investigation report.
**Read when:** You are writing the `## LLM Fix Prompt` block for a Trail report, choosing an action verb, or deciding whether to suppress.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Trail-specific verbs, suppression cases, template fields.

## Trail Action Verbs

Each fix prompt declares one verb at the top of `# Your task`.

| Verb | When to use | Receiving agent / LLM |
|------|-------------|----------------------|
| `FIX-REGRESSION` | HIGH confidence breaking commit identified, forward fix is straightforward | Builder, Claude, Codex |
| `REVERT` | Breaking commit is isolated, dependent changes are minimal, safe to revert wholesale (use `git revert`, never `reset --hard` on shared history) | Builder + Guardian |
| `REVERT-WITH-FORWARD-FIX` | Breaking commit must be reverted to stop the bleeding, but the original intent was valid — forward fix needed afterward | Builder (revert + re-implement) |
| `INVESTIGATE-FURTHER` | Bisect inconclusive, multiple suspect commits, or non-deterministic reproduction — receiving LLM must verify before changing code | Claude / Codex (investigation mode), or Trail (re-entry) |
| `REFACTOR-FIX` | Regression reflects a structural design issue; spot fix would re-introduce the bug elsewhere | Atlas → Builder |

---

## Verb Selection Heuristic

```
Bisect == HIGH confidence single commit ─┬─ revert is safe & sufficient ────→ REVERT
                                          ├─ original intent valid, forward fix ──→ REVERT-WITH-FORWARD-FIX
                                          └─ scoped forward fix preferred ────→ FIX-REGRESSION

Bisect == MEDIUM (range narrowed but ≥2 candidates) ─→ INVESTIGATE-FURTHER

Bisect == LOW / first-bad is a merge commit not isolatable ─→ INVESTIGATE-FURTHER

Regression reflects design flaw (same pattern in 3+ sites) ─→ REFACTOR-FIX
```

Tiebreakers:
- Use `REVERT` only when history is local-only or the revert is for a shared branch via `git revert` (never `reset --hard` on shared history). Never recommend force-push to main/master.
- For merge commits as first-bad, recommend testing each parent independently before deciding verb (often the integration is at fault, not either parent).
- If Trail escalates to Sentinel (security regression) or Atlas (architectural decay), do not emit a fix prompt — see suppression below.

---

## Trail-Specific Suppression Cases

Universal cases live in `_common/LLM_PROMPT_GENERATION.md`. Trail adds:

| Case | Reason | Note in report |
|------|--------|----------------|
| Trail escalates to Sentinel (security regression detected in commit) | Sentinel owns secure-fix prompts | "Fix prompt suppressed — Sentinel owns remediation prompt." |
| Trail escalates to Atlas (architectural archaeology reveals design issue, not regression) | Atlas owns architectural recommendation | "Fix prompt withheld — finding routed to Atlas as architectural concern, not regression." |
| Bisect identifies a merge commit as first-bad and parents are not yet independently tested | Cannot recommend a fix until the actual breaking change inside the merge is isolated | "Fix prompt withheld — merge commit isolation incomplete; recommend testing parents." |
| Archaeology task (no regression — explaining "why is this code like this?") | No fix is being proposed | "Fix prompt N/A — archaeology only." |
| Evidence is too weak even for `INVESTIGATE-FURTHER` | No supportable next investigation | "Fix prompt withheld — insufficient evidence." |

---

## Per-Regression Fix Prompt Template (Trail Fields)

Trail adds three Trail-specific blocks on top of the universal skeleton:

- `Breaking commit` — SHA + author date + commit message + diff summary
- `Bisect evidence` — good/bad pair + iteration count + test command + custom terms if any
- `Rollback safety` — whether the commit is local-only or shared, dependent changes since the commit, recommended revert strategy

````markdown
## LLM Fix Prompt

```text
# Your task
<VERB> the regression described below.

# Regression context
- Title: [brief description]
- Severity: [Critical | High | Medium | Low]
- First-bad commit: [SHA] ([YYYY-MM-DD] by [author])
- Confidence: [HIGH | MEDIUM | LOW] (Trail's bisect confidence)

# Breaking commit
SHA: <full SHA>
Date: <YYYY-MM-DD>
Author: <author>
Subject: <commit subject line>

Diff summary (lines that introduced the regression):
```diff
<minimal diff hunk that contains the breaking change>
```

Location of breaking change: `<file>:<line>` in `<function>`

# Bisect evidence
Good commit: <SHA> (<date>, <test result>)
Bad commit: <SHA> (<date>, <test result>)
Iterations: <N> (budget: ⌈log₂(<commit count>)⌉)
Test command: `<exact command>`
Custom terms: <"good/bad" or "fast/slow" or "old/new">

# Rollback safety
History status: <local-only | pushed to shared branch | released>
Dependent commits since first-bad: <count and summary>
Recommended strategy: <git revert <SHA> | forward fix | revert + forward fix>
Comms required: <yes — release impact | no — local only>

# Recommended action
Approach: [forward fix strategy OR revert plan]
Files to modify: [list with expected change per file]
Constraints:
- [side effect / backward-compat note]
- [coupling with commits since first-bad]

# Acceptance criteria
- [ ] Test command above passes after the change
- [ ] Regression test added covering the original failure
- [ ] No new test failures in the affected module
- [ ] If REVERT: dependent commits since first-bad are evaluated and re-applied where appropriate

# Ruled-out alternatives (do not revisit)
- [alternative cause 1] — eliminated because [bisect step / log evidence]
- [alternative cause 2] — eliminated because [evidence]

# What NOT to do
- Do not silence the symptom (catch-and-ignore, swallow logs, suppress the error)
- Do not `reset --hard` on shared history — use `git revert` for any pushed commit
- Do not skip the comms step if the breaking commit was already released
- Do not expand scope beyond the cited files unless evidence demands it
```
````

For `INVESTIGATE-FURTHER`, replace "Recommended action" with "Verification plan" (additional bisect runs, parent-isolation steps, or runtime checks). For `REVERT`, expand "Rollback safety" with the comms template and post-revert verification checklist.

---
