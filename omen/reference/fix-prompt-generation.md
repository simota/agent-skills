# Omen LLM Fix Prompt Generation

**Purpose:** Omen-specific action verbs, suppression cases, template fields, and worked example for the `## LLM Fix Prompt` block paired with every actionable failure mode (RPN above threshold, AP not Low, not classified `ACCEPT-RISK`).
**Read when:** Omen has enumerated failure modes via FMEA / pre-mortem / fault tree / Swiss Cheese / HAZOP and one or more modes warrant downstream action.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Omen-specific verbs, suppression cases, template fields, and an example.

## Contents

- When Omen emits a Fix Prompt
- Omen action verbs
- Verb selection heuristic
- Omen-specific suppression cases
- Per-failure-mode fix prompt template (Omen-specific fields)
- Worked example

---

## When Omen Emits a Fix Prompt

Omen does not write code, so every actionable failure mode is a hand-off. Pair a Fix Prompt with the failure mode whenever:

| Situation | Action |
|-----------|--------|
| RPN > 200 OR AP = High | Emit Fix Prompt with `ADD-GUARDRAIL`, `ADD-MONITOR`, or `ADD-RUNBOOK` |
| RPN 100-200 OR AP = Medium, with concrete defensive control | Emit Fix Prompt with `ADD-GUARDRAIL` or `ADD-MONITOR` |
| Severity ≥ 9 (catastrophic), regardless of RPN | Emit Fix Prompt — severity 9 always actionable per Core Contract |
| Underlying control not feasible this cycle, workaround exists | Emit Fix Prompt with `MITIGATE` |
| RPN/AP unclear because failure rate or blast radius unknown | Emit Fix Prompt with `INVESTIGATE-FURTHER` (route to Pulse / Beacon) |
| Mode classified `ACCEPT-RISK` with documented rationale and trigger | Suppress Fix Prompt; record acceptance note |
| Plan-review-only mode (stakeholder discussion, no actions yet) | Suppress Fix Prompt for the whole report |

The `OMEN_TO_*` handoff (Builder, Beacon, Triage, Mend, Pulse) carries a `fix_prompt` field; populate it whenever Omen does NOT classify the mode as `ACCEPT-RISK`.

---

## Omen Action Verbs

Each fix prompt declares one verb at the top of `# Your task`.

| Verb | When to use | Receiving agent |
|------|-------------|----------------|
| `ADD-GUARDRAIL` | Add code-level prevention or detection for the failure mode (input validation, circuit breaker, idempotency key, rate limiter) | Builder |
| `ADD-MONITOR` | Instrument observability for early detection (metric, alert, log assertion, SLO burn signal) | Beacon + Builder |
| `ADD-RUNBOOK` | Prepare an incident-response playbook for the failure mode without changing code yet | Triage + Mend |
| `MITIGATE` | Workaround for an unavoidable failure mode (graceful degradation, fallback path, queue-and-retry) | Builder |
| `INVESTIGATE-FURTHER` | RPN/AP unclear; collect failure-rate or blast-radius data before deciding action | Pulse / Beacon (data collection), or Omen re-entry |
| `ACCEPT-RISK` | Risk acknowledged; no action this cycle. Record rationale and trigger condition for revisit | Decision-maker (no agent action) |

---

## Verb Selection Heuristic

```
Severity == 9 or 10 (catastrophic) ─┬─ no concrete control yet ────────→ INVESTIGATE-FURTHER
                                     ├─ control exists, code change ────→ ADD-GUARDRAIL
                                     ├─ underlying blocked, workaround ─→ MITIGATE
                                     └─ runbook is the only response ──→ ADD-RUNBOOK

RPN > 200 OR AP == High ─┬─ detection gap is the critical layer ──────→ ADD-MONITOR
                          ├─ prevention gap is the critical layer ─────→ ADD-GUARDRAIL
                          ├─ recovery gap is the critical layer ───────→ ADD-RUNBOOK
                          └─ data missing for scoring ──────────────────→ INVESTIGATE-FURTHER

RPN 100-200 OR AP == Medium ─→ ADD-GUARDRAIL or ADD-MONITOR (whichever closes the bigger Swiss-Cheese gap)

RPN < 100 AND AP == Low AND Severity < 9 ─→ ACCEPT-RISK (with trigger condition for revisit)
```

Tiebreakers:
- Severity ≥ 9 always emits a Fix Prompt — catastrophic severity cannot be offset by low occurrence per Core Contract.
- When detection AND prevention are both gaps, prefer `ADD-GUARDRAIL` (prevention) and cross-link a follow-up `ADD-MONITOR` so the receiving agents see both layers.
- `ADD-RUNBOOK` is the right choice when the failure is rare-but-survivable and code-level prevention has poor cost / benefit.
- `MITIGATE` always documents why the underlying fix is not happening this cycle (cost, dependency, scope) — otherwise the receiving LLM may try to "really" fix it and exceed scope.

---

## Omen-Specific Suppression Cases

Universal cases live in `_common/LLM_PROMPT_GENERATION.md`. Omen adds:

| Case | Reason | Note in report |
|------|--------|----------------|
| Plan-review-only invocation (enumerate modes for stakeholder discussion, no action yet) | Out of scope for this engagement | "Fix prompt withheld per scope: plan review only." |
| Failure mode is incident-response specific (Triage owns the response prompt) | Triage is the natural prompt owner | "Fix prompt suppressed — Triage owns incident-response remediation prompt." |
| Failure mode falls outside ownership (3rd-party service, infrastructure team) | Cannot be acted on by this team's coding LLM | "Fix prompt withheld — failure mode owned by [external team]; coordinate via [channel]." |
| All identified failure modes are `ACCEPT-RISK` | No actionable items | "No fix prompts emitted — all enumerated modes accepted as residual risk." |
| Security failure mode escalated to Sentinel | Sentinel owns the security-specific remediation prompt | "Fix prompt suppressed — Sentinel owns security remediation prompt." |

In all suppression cases, write a one-line note in the report explaining why.

---

## Per-Failure-Mode Fix Prompt Template (Omen Fields)

Omen adds these Omen-specific blocks on top of the universal skeleton:

- `Failure mode ID` — tracking identifier (e.g., `FM-007`) so the receiving LLM and stakeholders can cross-reference the FMEA table
- `RPN score` — Severity × Occurrence × Detection (1-1000), and/or `AP score` (Low / Medium / High)
- `Failure scenario` — ordered "if X happens then Y, then Z" causal chain
- `Detection gap` — what would currently prevent or detect this failure (often "nothing")
- `Trigger condition for revisit` — for `ACCEPT-RISK` only — what observation should re-open the decision

````markdown
## LLM Fix Prompt

```text
# Your task
<VERB> the failure mode described below.

# Failure mode context
- Failure mode ID: [e.g., FM-007]
- Title: [brief description]
- RPN score: [S × O × D = N]  (Severity [1-10], Occurrence [1-10], Detection [1-10])
- AP score: [High | Medium | Low] (AIAG-VDA, when applicable)
- Severity rationale: [why S = N — blast radius, user impact, data loss potential]
- Confidence: [HIGH | MEDIUM | LOW] (Omen's enumeration confidence)
- Source method: [pre-mortem | FMEA | fault tree | Swiss Cheese | HAZOP | bowtie]

# Failure scenario
1. [trigger / upstream cause]
2. [propagation step]
3. [observed failure mode]
4. [downstream impact / blast radius]

Location of risk: `<file or component>:<line or surface>` in `<function or boundary>`

# Detection gap
What currently prevents or detects this failure: [list current controls; if none, write "None — defense layers all permeable for this scenario"]
Swiss-Cheese layers analyzed: [layers with holes that align]

# Recommended action
Approach: [defensive control strategy — guardrail type, monitor SLI, runbook structure]
Files / surfaces to modify: [list with expected change per file]
Defensive controls:
- [library / pattern, e.g., `idempotency-key middleware`, `circuit-breaker (resilience4j)`, `Zod schema at boundary`]
- [framework-native control, e.g., DB unique constraint, queue dead-letter handler]
Constraints:
- [coupling / side-effect / backward-compat note]
- [latency / throughput budget if guardrail is hot-path]

# [MITIGATE only — Underlying status]
- Why the underlying cause is not addressed this cycle: [cost / dependency / scope reason]
- When it should be addressed: [trigger / next cycle]

# [INVESTIGATE-FURTHER only — Verification plan]
- Data to collect: [failure rate, blast radius sample, log query]
- Tooling: [Pulse query, Beacon dashboard, log scan]
- Decision threshold: [score adjustment that flips action verb]

# Acceptance criteria
- [ ] Guardrail / monitor / runbook in place at the cited location
- [ ] Failure scenario step [N] no longer reaches step [N+1] without detection
- [ ] Regression test added covering the trigger condition
- [ ] No new test failures in the affected module
- [ ] [ADD-MONITOR] Alert fires within [latency budget] of trigger event
- [ ] [ADD-RUNBOOK] Runbook reviewed by Triage owner

# Ruled-out alternatives (do not revisit)
- [alternative 1] — eliminated because [evidence, e.g., framework guarantee, prior incident outcome]
- [alternative 2] — eliminated because [evidence]

# What NOT to do
- Do not silence the symptom (catch-and-ignore, swallow logs, suppress the alert)
- Do not over-engineer beyond the cited failure mode — defense in depth is welcome but new dependencies require justification
- Do not bundle unrelated failure modes into the same change (one failure mode per prompt per Universal Rule 9)
- Do not weaken the existing Swiss-Cheese layers while adding the new one
- Do not expand scope beyond the cited files / surfaces unless evidence demands it
```
````

For `ACCEPT-RISK`, no Fix Prompt is emitted; instead the report records:

```text
- Failure mode ID: FM-NNN
- Disposition: ACCEPT-RISK
- Rationale: [why action is deferred]
- Trigger condition for revisit: [observation that reopens the decision — e.g., "occurrence rate > 1/week", "new tenant onboarded above 10k events/sec", "regulatory change"]
- Owner: [decision-maker name / role]
- Review date: [YYYY-MM-DD]
```

---

## Worked Example (ADD-GUARDRAIL)

**Scenario:** Pre-mortem on a new payments checkout flow surfaces a duplicate-charge failure mode caused by client retries on flaky network conditions. No idempotency control exists today.

````markdown
## LLM Fix Prompt

```text
# Your task
ADD-GUARDRAIL the failure mode described below.

# Failure mode context
- Failure mode ID: FM-007
- Title: Duplicate payment charge on client retry of /checkout
- RPN score: 9 × 6 × 7 = 378  (Severity 9, Occurrence 6, Detection 7)
- AP score: High
- Severity rationale: Customer is double-charged in production, triggers chargeback and trust loss; per-incident cost ~$50 plus reputational damage. Severity 9 (single-customer financial loss with regulatory exposure under PSD2 dispute rules).
- Confidence: HIGH (Omen pre-mortem + payment-team incident history corroborates)
- Source method: pre-mortem + FMEA

# Failure scenario
1. User submits checkout, the request reaches Stripe and the charge succeeds.
2. The 200 response is lost on the user's mobile network (timeout at our edge).
3. The browser auto-retries POST /checkout (default fetch retry on transient error).
4. Our handler accepts the retried request with no replay guard, calls Stripe again, and a second charge succeeds.
5. The user sees one order but two charges; chargeback and refund workflow triggers.

Location of risk: `src/api/checkout.ts:88` in `createCheckoutHandler()` (POST entrypoint, no idempotency key)

# Detection gap
What currently prevents or detects this failure: None at the application layer.
- Stripe idempotency keys: not used
- Database unique constraint on (user_id, cart_hash, minute_bucket): not present
- Client-side debounce: 300ms only; mobile retry triggers > 1s later
Swiss-Cheese layers analyzed: client retry guard (hole), edge dedupe (hole), application idempotency (hole), database constraint (hole), Stripe replay protection (hole when key absent). All five layers permeable.

# Recommended action
Approach: Require an `Idempotency-Key` header on POST /checkout. Persist (key, response) for 24h; on replay, return the stored response without re-invoking Stripe. Forward the same key as Stripe's `Idempotency-Key` header so the upstream layer is also protected.
Files / surfaces to modify:
- src/api/checkout.ts — read `Idempotency-Key` header, look up in cache, short-circuit on hit
- src/lib/idempotency.ts — new module: Redis-backed key store with 24h TTL, atomic put-if-absent
- src/lib/stripe-client.ts — pass `Idempotency-Key` to Stripe SDK
- src/api/checkout.test.ts — add replay tests
- web/checkout-form.tsx — generate UUIDv4 per submit, send in header
Defensive controls:
- Redis SET NX EX 86400 for atomic key reservation
- Stripe SDK native `idempotencyKey` option (Stripe stores 24h, matches our TTL)
- Reject requests missing the header with 400 (after a 2-week observability period in warn-only mode)
Constraints:
- Latency budget: idempotency check must add < 5ms p99 (Redis is in-VPC)
- Backward compatible during rollout: warn-only mode for 2 weeks, then enforce
- Do not change the `/checkout` response shape

# Acceptance criteria
- [ ] All POST /checkout calls require Idempotency-Key after enforcement date
- [ ] Replay of identical key within 24h returns the original response without calling Stripe
- [ ] Stripe receives the same Idempotency-Key (verified in Stripe dashboard request logs)
- [ ] Regression test covers: (a) network-loss replay, (b) deliberate double-click, (c) key collision across users (must reject)
- [ ] Failure scenario step 4 no longer reaches step 5 in test harness
- [ ] No new test failures in src/api/checkout.test.ts
- [ ] Beacon alert fires when idempotency cache miss-rate spikes (cross-link to ADD-MONITOR FM-007-M)

# Ruled-out alternatives (do not revisit)
- Client-side debounce only — eliminated: does not address mobile network retries that fire seconds later, and trusts the client
- Database unique constraint on (user_id, cart_hash) — eliminated: cart contents may change legitimately within seconds; constraint produces false rejects
- Stripe-side idempotency key alone without local store — eliminated: still calls Stripe network on every replay, wasting quota and adding latency; also returns Stripe's response wrapper which leaks internal IDs
- Disable client retry — eliminated: cannot enforce on third-party browsers / native apps

# What NOT to do
- Do not silence the symptom by issuing automatic refunds on detected duplicates — root cause stays open
- Do not skip the warn-only rollout — clients without the header will hard-fail in production
- Do not log the full Idempotency-Key value (treat as a request secret)
- Do not bundle unrelated checkout changes (UI tweaks, analytics events) into this PR
- Do not weaken Stripe webhook signature verification while adding this guardrail
- Do not expand scope beyond the cited files unless evidence demands it
```
````

This prompt is self-contained: a coding LLM (Builder) can act on it without seeing the rest of the Omen FMEA report. The cross-link to a paired `ADD-MONITOR` for the same failure mode (FM-007-M) is explicit so Beacon can pick up the detection layer in parallel.
