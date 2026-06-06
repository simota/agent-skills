# Attest LLM Fix Prompt Generation

**Purpose:** Attest-specific action verbs, suppression cases, template fields, and worked example for the `## LLM Fix Prompt` block when Attest confirms an AC gap and hands remediation to Builder (or Scribe/Accord for spec rewrites).
**Read when:** Attest has issued a per-criterion verdict of `FAIL` or `PARTIAL` and remediation must be paired with a paste-ready prompt for the receiving agent.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Attest-specific verbs, suppression cases, template fields, and an example.

## Contents

- When Attest emits a Fix Prompt vs withholds
- Attest action verbs
- Verb selection heuristic
- Attest-specific suppression cases
- Per-finding fix prompt template (Attest-specific fields)
- Worked example

---

## When Attest Emits a Fix Prompt vs Withholds

Attest never modifies code. Every confirmed AC gap with sufficient evidence pairs with a Fix Prompt addressed to the agent best positioned to remediate. The prompt is withheld only in the suppression cases below.

| Situation | Action |
|-----------|--------|
| Per-criterion verdict is `FAIL` or `PARTIAL` and the implementation must change | Emit `CLOSE-GAP` (or `BREAKING-CLOSE` if scope is wider) — Builder |
| Implementation behavior is correct but the spec is wrong/outdated/missing the criterion | Emit `RECONCILE-SPEC` — Scribe / Accord |
| AC interpretation is ambiguous and a code change without clarification would miss intent | Emit `INVESTIGATE-FURTHER` — spec author or Attest re-entry |
| AC is not applicable in the current context (deprecated, out-of-scope feature flag) | Emit `WAIVE` — Builder + Scribe (waiver doc) |
| Verification-only mode requested (compliance verdict only, no remediation scope) | **Suppress prompt.** Note "Fix prompt withheld per scope: verification only." |
| Multiple ACs require coordinated spec rewrite | **Suppress per-finding prompts.** Hand the whole bundle to Scribe/Accord. |
| Implementation passes all ACs (no gaps) | **Suppress prompt.** Note "Fix prompt N/A — full conformance verified." |
| Verdict is `NOT_TESTED` (runtime-only) and no static gap is established | **Suppress prompt.** Hand off to Voyager/Radar with runtime plan instead. |

The `ATTEST_TO_BUILDER_HANDOFF` and `ATTEST_TO_SCRIBE_HANDOFF` payloads carry a `fix_prompt` field; populate it whenever the verdict is `FAIL` or `PARTIAL` and a suppression case does not apply.

---

## Attest Action Verbs

Each fix prompt declares one verb at the top of `# Your task`.

| Verb | When to use | Receiving agent |
|------|-------------|----------------|
| `CLOSE-GAP` | Implementation is missing an AC; scoped fix to satisfy the AC | Builder |
| `RECONCILE-SPEC` | Implementation behavior is correct but the spec is wrong/outdated; update spec instead of code | Scribe / Accord |
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
| Attest hands off to Scribe/Accord for spec rewrite (multiple ACs need restructuring) | A per-finding prompt would fragment a coordinated rewrite | "Fix prompt suppressed — Scribe/Accord owns spec rewrite prompt." |
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

## Worked Example (CLOSE-GAP)

**Scenario:** AC requires email-format validation on the registration endpoint, but the implementation accepts any non-empty string, allowing malformed emails to be persisted.

````markdown
## LLM Fix Prompt

```text
# Your task
CLOSE-GAP the acceptance-criterion gap described below.

# AC context
- AC ID: PRD-REG-AC-012
- Priority: HIGH
- Verification verdict: FAIL
- Confidence: HIGH (static + reproducible failing scenario)
- Spec source: `docs/prd/registration.md:§3.2`

# AC verbatim
> The registration endpoint MUST reject email addresses that do not conform
> to RFC 5322 simplified syntax (local-part@domain with at least one dot in
> the domain). Rejected requests MUST return HTTP 400 with error code
> `INVALID_EMAIL_FORMAT`.

# BDD scenario (failing)
Scenario: Registration rejects malformed email address
  Given a registration payload with email "notanemail"
  When the client POSTs to /api/register
  Then the response status is 400
  And the response body contains error code "INVALID_EMAIL_FORMAT"

Currently observed: response status is 201 (user created with malformed email).

# Evidence
The handler validates only that `email` is a non-empty string. No format check
is applied before persistence.

Implementation location: `src/api/register.ts:48` in `registerHandler()`

Implementation snippet (verbatim):
```
const { email, password } = req.body;
if (!email || !password) {
  return res.status(400).json({ error: "MISSING_FIELDS" });
}
const user = await db.users.insert({ email, password_hash: hash(password) });
return res.status(201).json({ id: user.id });
```

Database state after sending `email: "notanemail"`:
```
id  | email       | created_at
----+-------------+--------------------
42  | notanemail  | 2026-05-01 10:23:01
```

# Recommended action
Approach: Add a format-validation step using Zod (already a project dependency)
between the existence check and the database insert. On validation failure,
return HTTP 400 with error code `INVALID_EMAIL_FORMAT` per the AC.

Files to modify:
- src/api/register.ts — insert Zod schema parse before db.users.insert
- src/api/register.test.ts — add scenarios for "notanemail", "missing@dot",
  "@nodomain.com", and a passing valid email

Constraints:
- Public response shape on success must remain `{ id: number }` — do not add fields
- Error code string must be exactly `INVALID_EMAIL_FORMAT` (matches downstream consumers)
- Do not modify ACs other than PRD-REG-AC-012 in this change

# Acceptance criteria
- [ ] BDD scenario above passes (POST with "notanemail" returns 400 + INVALID_EMAIL_FORMAT)
- [ ] AC PRD-REG-AC-012 reaches verdict `PASS` on Attest re-run
- [ ] Regression tests added for at least 3 malformed-email patterns
- [ ] One passing-valid-email test confirms no false-rejection regression
- [ ] No new test failures in src/api/register.test.ts
- [ ] No malformed emails inserted in test database after the change

# Ruled-out alternatives (do not revisit)
- Validate at the database layer (CHECK constraint) — eliminated: AC requires
  HTTP 400 + specific error code, which a DB constraint cannot produce
- Custom regex inline — eliminated: Zod is already in use elsewhere; project
  convention is to centralize validation schemas
- Reject only at the gateway/WAF — eliminated: AC is a backend contract,
  gateway-level filtering would not satisfy a direct API consumer test

# What NOT to do
- Do not silence the symptom (try/catch around the insert and ignore validation errors)
- Do not expand scope beyond PRD-REG-AC-012; password complexity (PRD-REG-AC-013)
  and rate limiting (PRD-REG-AC-018) are out of scope for this change
- Do not modify the spec to match the current permissive behavior — the spec is
  correct; the implementation is wrong
- Do not skip the BDD scenario assertion in regression tests
- Do not bundle unrelated AC fixes into the same change — one verb, one finding
```
````

This prompt is self-contained: Builder can act on it without seeing the rest of the Attest compliance report.
