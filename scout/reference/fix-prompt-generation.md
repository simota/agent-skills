# Scout LLM Fix Prompt Generation

**Purpose:** Scout-specific action verbs, suppression cases, template fields, and worked example for the `## LLM Fix Prompt` block at the end of every Scout investigation report.
**Read when:** You are writing the `## LLM Fix Prompt` block for a Scout report, choosing an action verb, or deciding whether to suppress.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Scout-specific verbs, suppression cases, template fields, and an example.

## Contents

- Scout action verbs
- Verb selection heuristic
- Scout-specific suppression cases
- Per-bug fix prompt template (Scout-specific fields)
- Worked example

---

## Scout Action Verbs

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
- If Scout escalates to Specter/Sentinel, do not emit a fix prompt — see suppression below.
- If the bug spans 4+ files and reflects a design issue, prefer `REFACTOR-FIX` over `FIX`.
- If reproduction failed but root cause is strongly hypothesized (MEDIUM evidence), prefer `INVESTIGATE-FURTHER` over `FIX` to force the receiving LLM to confirm the symptom first.

---

## Scout-Specific Suppression Cases

Universal cases live in `_common/LLM_PROMPT_GENERATION.md`. Scout adds:

| Case | Reason | Note in report |
|------|--------|----------------|
| Scout escalates to Sentinel (security suspicion) | Sentinel owns secure-fix prompts | "Fix prompt suppressed — Sentinel owns remediation prompt." |
| Scout escalates to Specter (concurrency/memory) | Specter owns concurrency-fix prompts | "Fix prompt suppressed — Specter owns remediation prompt." |

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

## Worked Example

**Scenario:** Form submit handler double-fires after user retries on network timeout, causing duplicate orders.

````markdown
## LLM Fix Prompt

```text
# Your task
FIX the bug described below.

# Bug context
- Title: Duplicate order creation on retry after timeout
- Severity: High
- Reproducibility: Always (with throttled network)
- Confidence: HIGH (reproduction + code path traced + 3 customer reports)

# Root cause
The submit handler in `OrderForm.tsx` does not disable the submit button or
guard with an in-flight flag. When the first request times out, the user
clicks Retry; the original request is still pending and completes after the
retry, producing two POSTs to /api/orders.

Location: `src/components/OrderForm.tsx:142` in `handleSubmit()`

# Reproduction
1. Open Chrome DevTools → Network → throttle to "Slow 3G"
2. Fill the order form with valid data
3. Click "Submit"
4. After ~3s with no response, click "Submit" again
5. Wait for both requests to complete

Expected: Exactly one POST /api/orders, exactly one order created.
Actual: Two POST /api/orders, two duplicate orders created.

Exact error / log signature (search for this string):
```
[orders] duplicate insert detected for idempotency_key=null
```

# Recommended fix
Approach: Add an in-flight guard with `isSubmitting` state; disable the
submit button while the request is pending; generate a per-attempt
idempotency key and forward it in the request header so the backend can
deduplicate even if the guard is bypassed.

Files to modify:
- src/components/OrderForm.tsx — add `isSubmitting` state, disable button,
  generate idempotency key
- src/api/orders.ts — forward `Idempotency-Key` header

Constraints:
- Backend already supports `Idempotency-Key` header (verified in
  src/server/orders/handler.ts:88)
- Do not change the form's submit URL or payload shape
- Preserve current error message UX

# Acceptance criteria
- [ ] Throttled-network reproduction above produces exactly one order
- [ ] Submit button is visibly disabled during the in-flight request
- [ ] Regression test covers double-click during pending request
- [ ] No new test failures in src/components/OrderForm.test.tsx

# Ruled-out hypotheses (do not revisit)
- React StrictMode double-invocation — ruled out: bug reproduces in
  production build with StrictMode disabled
- Backend retry middleware — ruled out: server logs show two distinct
  client-initiated requests with different timestamps
- Browser auto-resubmit on connection drop — ruled out: requests originate
  from explicit click events (verified in DevTools)

# What NOT to do
- Do not silence the symptom by deduplicating on the server only — the
  client must guard against the double-click pattern
- Do not change the form's validation logic (out of scope)
- Do not refactor the entire form component; the fix is local to
  handleSubmit and the submit button
```
````

This prompt is self-contained: a coding LLM can act on it without seeing the rest of the Scout report.
