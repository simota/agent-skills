# Attest LLM Fix Prompt Generation

**Purpose:** Attest-specific action verbs, suppression cases, template fields for the `## LLM Fix Prompt` block when Attest confirms an AC gap and hands remediation to Builder (or Scribe/Scribe[unified] for spec rewrites).
**Read when:** Attest has issued a per-criterion verdict of `FAIL` or `PARTIAL` and remediation must be paired with a paste-ready prompt for the receiving agent.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Attest-specific verbs, suppression cases, template fields.

## When Attest Emits a Fix Prompt vs Withholds

Attest never modifies code. Every confirmed AC gap with sufficient evidence pairs with a Fix Prompt addressed to the agent best positioned to remediate. The prompt is withheld only in the suppression cases below.

| Situation | Action |
|-----------|--------|
| Per-criterion verdict is `FAIL` or `PARTIAL` and the implementation must change | Emit `CLOSE-GAP` (or `BREAKING-CLOSE` if scope is wider) — Builder |
| Implementation behavior is correct but the spec is wrong/outdated/missing the criterion | Emit `RECONCILE-SPEC` — Scribe / Scribe[unified] |
| AC interpretation is ambiguous and a code change without clarification would miss intent | Emit `INVESTIGATE-FURTHER` — spec author or Attest re-entry |
| AC is not applicable in the current context (deprecated, out-of-scope feature flag) | Emit `WAIVE` — Builder + Scribe (waiver doc) |
| Verification-only mode requested (compliance verdict only, no remediation scope) | **Suppress prompt.** Note "Fix prompt withheld per scope: verification only." |
| Multiple ACs require coordinated spec rewrite | **Suppress per-finding prompts.** Hand the whole bundle to Scribe/Scribe[unified]. |
| Implementation passes all ACs (no gaps) | **Suppress prompt.** Note "Fix prompt N/A — full conformance verified." |
| Verdict is `NOT_TESTED` (runtime-only) and no static gap is established | **Suppress prompt.** Hand off to Voyager/Radar with runtime plan instead. |

The `ATTEST_TO_BUILDER_HANDOFF` and `ATTEST_TO_SCRIBE_HANDOFF` payloads carry a `fix_prompt` field; populate it whenever the verdict is `FAIL` or `PARTIAL` and a suppression case does not apply.

---

## Attest Action Verbs

Each fix prompt declares one verb at the top of `# Your task`.

| Verb | When to use | Receiving agent |
|------|-------------|----------------|
| `CLOSE-GAP` | Implementation is missing an AC; scoped fix to satisfy the AC | Builder |
| `RECONCILE-SPEC` | Implementation behavior is correct but the spec is wrong/outdated; update spec instead of code | Scribe / Scribe[unified] |
| `BREAKING-CLOSE` | Closing the gap requires a breaking change (API contract, behavior change visible to clients) | Builder + Guardian + Launch |
| `INVESTIGATE-FURTHER` | AC interpretation ambiguous; need to clarify with spec author / stakeholder before changing code | Spec author OR Attest re-entry with clarified spec |
| `WAIVE` | AC not applicable in the current context; document waiver with rationale | Builder + Scribe (waiver doc) |

---

## Verb Selection Heuristic

```
Verdict == FAIL ──┬─ implementation correct, spec wrong ─→ RECONCILE-SPEC
                  ├─ AC interpretation unclear ──────────→ INVESTIGATE-FURTHER
                  ├─ scoped code fix, no client breakage ─→ CLOSE-GAP
                  └─ closing gap breaks public surface ──→ BREAKING-CLOSE

Verdict == PARTIAL ─┬─ missing aspect is in spec only ───→ RECONCILE-SPEC
                    ├─ missing aspect requires code ────→ CLOSE-GAP
                    └─ AC no longer applicable ─────────→ WAIVE

Verdict == AMBIGUOUS (after extraction) ──────────────→ INVESTIGATE-FURTHER

AC explicitly out of scope (feature flag off, deprecated) ─→ WAIVE
```

Tiebreakers:
- `BREAKING-CLOSE` always cross-links to Guardian and Launch — breaking changes need release coordination and PR gate review.
- `RECONCILE-SPEC` requires the implementation evidence be cited verbatim so Scribe can write the new AC against observed behavior, not Attest's interpretation.
- `INVESTIGATE-FURTHER` replaces "Recommended action" with "Verification plan" (steps to confirm or refute the AC interpretation before any code or spec change).
- `WAIVE` requires both a Builder handoff (to gate the AC out of regression suites) and a Scribe handoff (to record the waiver with rationale and expiry).

---

## Attest-Specific Suppression Cases

Universal cases live in `_common/LLM_PROMPT_GENERATION.md`. Attest adds:

| Case | Reason | Note in report |
|------|--------|----------------|
| Verification-only mode (no fix scope; report compliance verdict only) | Out of scope for this engagement | "Fix prompt withheld per scope: verification only." |
| Attest hands off to Scribe/Scribe[unified] for spec rewrite (multiple ACs need restructuring) | A per-finding prompt would fragment a coordinated rewrite | "Fix prompt suppressed — Scribe/Scribe[unified] owns spec rewrite prompt." |
| AC interpretation requires stakeholder decision (not a code/spec problem) | Acting before the decision risks rework | "Fix prompt withheld — pending stakeholder decision on [AC ID]." |
| Implementation passes all ACs (no gaps found) | Nothing to remediate | "Fix prompt N/A — full conformance verified." |
| Verdict is `NOT_TESTED` (runtime-only) with no static gap established | Runtime owner (Voyager/Radar) is the correct recipient, not Builder | "Fix prompt suppressed — runtime verification routed to [Voyager/Radar]." |

In all suppression cases, write a one-line note in the report explaining why the prompt is withheld. Silent omission breaks downstream expectations.

---

## Per-Finding Fix Prompt Template (Attest Fields)

Attest adds these Attest-specific blocks on top of the universal skeleton:

- `AC ID` — the acceptance criterion identifier from the source spec (e.g., `PRD-AUTH-AC-007`)
- `AC verbatim` — the AC text quoted from the spec (no paraphrasing)
- `Spec source` — file path + line/section in the spec document
- `BDD scenario` — Given/When/Then scenario that exercises the AC
- `Verification verdict` — `PASS` | `FAIL` | `PARTIAL` | `NOT_TESTED` | `AMBIGUOUS`
- `Evidence` — test output, log line, code snippet, or runtime observation that supports the verdict
- For `BREAKING-CLOSE` — `Client impact` and `Rollout/comms plan`
- For `RECONCILE-SPEC` — `Observed behavior` and `Proposed AC rewrite`
- For `WAIVE` — `Waiver rationale` and `Expiry/revisit trigger`

````markdown
## LLM Fix Prompt

```text
# Your task
<VERB> the acceptance-criterion gap described below.

# AC context
- AC ID: [e.g., PRD-AUTH-AC-007]
- Priority: [CRITICAL | HIGH | MEDIUM | LOW]
- Verification verdict: [FAIL | PARTIAL | AMBIGUOUS]
- Confidence: [HIGH | MEDIUM | LOW]
- Spec source: `<spec-file>:<section>` or `<spec-file>:<line>`

# AC verbatim
> [exact AC text quoted from the spec — do not paraphrase]

# BDD scenario (failing)
Scenario: [scenario title]
  Given [precondition]
  When [trigger action]
  Then [expected observable outcome — currently NOT observed]

# Evidence
[Static or static-runtime observation that supports the verdict.
Quote test output, log line, or code snippet verbatim.]

Implementation location: `<file>:<line>` in `<function>()`

Implementation snippet (verbatim):
```
[verbatim code, log, or output]
```

# Recommended action
Approach: [scoped strategy to satisfy the AC without expanding scope]
Files to modify: [list with expected change per file]
Constraints:
- [coupling, side effect, or backward-compat note]
- Do not modify ACs other than [AC ID] in this change.

# [BREAKING-CLOSE only — Client impact]
- API shape change: [yes/no — describe]
- Behavior change visible to clients: [yes/no — describe]
- Migration steps for clients: [list]

# [BREAKING-CLOSE only — Rollout/comms plan]
- Feature flag / staged rollout: [plan]
- Release notes section: [content]
- Pre-deploy verification: [staging test, canary]

# [RECONCILE-SPEC only — Observed behavior]
[Verbatim description of what the implementation actually does]

# [RECONCILE-SPEC only — Proposed AC rewrite]
> [draft AC text that matches observed behavior — Scribe will finalize]

# [WAIVE only — Waiver rationale]
[Why this AC does not apply in the current context]

# [WAIVE only — Expiry/revisit trigger]
[Date or condition that re-opens the AC for verification]

# Acceptance criteria
- [ ] BDD scenario above passes (Given/When/Then observable outcome holds)
- [ ] AC [AC ID] reaches verdict `PASS` on Attest re-run
- [ ] Regression test added covering the scenario
- [ ] No new test failures in the affected module
- [ ] [BREAKING-CLOSE] Guardian + Launch sign-off recorded
- [ ] [RECONCILE-SPEC] Spec updated with new AC text and version bumped
- [ ] [WAIVE] Waiver doc recorded in [path] with expiry condition

# Ruled-out alternatives (do not revisit)
- [alternative 1] — eliminated because [evidence]
- [alternative 2] — eliminated because [evidence]

# What NOT to do
- Do not silence the symptom (catch-and-ignore the failing branch, mock the AC away)
- Do not expand scope beyond [AC ID]; other ACs in the same spec are out of scope for this change
- Do not modify the spec to match buggy behavior unless verb is `RECONCILE-SPEC`
- Do not skip the BDD scenario assertion in regression tests
- Do not bundle unrelated AC fixes into the same change — one verb, one finding
```
````

For `INVESTIGATE-FURTHER`, replace "Recommended action" with "Verification plan" (steps to confirm or refute the AC interpretation before changing anything).

---
