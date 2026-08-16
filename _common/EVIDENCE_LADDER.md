# Evidence Ladder Protocol

Cross-skill discipline for deciding **how much independent evidence a change must carry before it ships**, and for detecting the failure where implementation and its verifier share the same mistake. Verification is not raising the model's confidence — it is **adding independent observations capable of finding the error**.

**Read when:** planning what to verify before implementing; selecting the evidence set for a change; auditing whether a green test suite actually proves anything; deciding whether an AI-written test is admissible evidence for AI-written code.

**Audience:** `radar`, `voyager`, `siege`, `attest`, `mint`, `judge`, `guardian`, `sentinel`, `beacon`, `mend`, `nexus[acceptance]`, `nexus[apex]`, `rally`.

**Prerequisites:** none. **Composes with:** `_common/PROOF_CARRYING.md` (which criticality tier of PR gets a full evidence package — *orthogonal*: PROOF_CARRYING answers *which PRs are gated and by whom*, this file answers *how far up the evidence stack one change must climb*), `_common/DIFFERENTIAL_PARITY.md` (E4's differential mechanism), `_common/TRACEABILITY.md` (AC IDs).

---

## 1. The ladder

Seven levels. What rises as you climb is not effort — it is **distance from the implementation's own hypothesis**. E0 and E3 can both be produced by the same model from the same misunderstanding; E4 and above cannot, by construction.

| Level | Evidence | Mechanism | Independent of the implementer's assumptions? |
|-------|----------|-----------|-----------------------------------------------|
| `E0` | **Model Assertion** | change explanation, self-review, reasoning trace | **No.** Weakest rung. Useful to start, never to ship. |
| `E1` | **Static Evidence** | types, compiler, lint, SAST, architecture/dependency rules | Partially — an external rule engine, but only over syntax and declared contracts. |
| `E2` | **Local Execution** | build, reproduce, smoke | Partially — the runtime disagrees with the model, but only on paths actually run. |
| `E3` | **Automated Tests** | unit, integration, contract | **Only if the oracle is independent** (§3). A test written from the same context as the code is E0 wearing a green check. |
| `E4` | **Independent Test** | property, metamorphic, mutation, fuzz, differential | **Yes** — each derives its expectation from a source other than the implementation. |
| `E5` | **Integration Evidence** | preview env, policy check, attestation, canary | Yes — the real integration surface rejects what local mocks accepted. |
| `E6` | **Production Observation** | SLO, trace, incident, user outcome, reconciliation | Yes — the only rung measuring the real input distribution. |

**Not every change climbs to E6.** A README typo does not get a canary. The ladder is a selection device, not a checklist to exhaust: pick the levels whose *failure mechanism* matches the change's *risk mechanism*, that detect **different** failures, and that land **before** the decision is made.

### Choosing the required floor

Score the change, then take the highest floor any dimension demands:

| Dimension | Ask | Raises floor toward |
|-----------|-----|---------------------|
| `user_impact` | how many users see a wrong result, and how loudly? | E3 → E5 |
| `security_impact` | can this widen a privilege, leak, or bypass a control? | **E4 minimum**, E5 approval |
| `data_impact` | can this corrupt, lose, or mis-attribute persisted data? | **E4 minimum**, E6 reconciliation |
| `novelty` | is this a pattern the repo has never verified before? | E4 |
| `rollback_cost` | if wrong in production, how expensive is undo? | E5 rehearsal, E6 monitor |

Weight `security_impact` and `data_impact` heavily — they are the two where a silent pass is unrecoverable. The score is not a substitute for judgment; its job is to **force the argument to happen before implementation**, not after.

### Write the plan before the code

```yaml
evidence_plan:
  change: refresh token rotation
  risk: { security: high, data: medium, blast_radius: high }
  E1: [typecheck, sast, dependency_rule]
  E2: [build, reproduce token reuse]
  E3: [unit, integration, contract with mobile client]
  E4: [property "used token cannot be reused", fuzz token parser, independent security review]
  E5: [preview env, policy attestation, canary 1%]
  E6: [auth failure SLO, reuse detection metric, rollback threshold]
  independent_oracle: protocol_test_vectors
  not_verified: [legacy client older than supported window]
  owner: identity_team
```

`not_verified` is a required field, not an optional one. An evidence plan that lists only what passed is a marketing document.

---

## 2. Circular Verification — the failure this protocol exists to prevent

**Symptom:** the same agent generates the implementation, the tests, and the explanation. Every test passes. The behavior is wrong.

**Mechanism:** implementation, expected value, and rationale all derive from one reading of the spec. Internal consistency is therefore high — and internal consistency does not bound external correctness. If the model read "the deadline excludes the end date" and the business means the opposite, the code and the assertion carry the *same* error and the suite is green.

**Why it is worse than an ordinary bug:** the wrong behavior is now pinned by a regression test. The correct fix presents as "a change that breaks tests" and gets rejected in review.

**"Ask a different model" is not independence.** Two models may share training data, the same public docs, and the same benchmark patterns. Independence comes from a different **evidence mechanism**, not a different vendor: a compiler observes syntax and types, a property observes an invariant, a differential run observes divergence from existing behavior, a production metric observes the real world.

### Expected-value provenance

For any assertion, the admissibility question is *where the expected value came from*:

| Provenance | Admissible as | Note |
|------------|---------------|------|
| Derived from the spec, a domain example, or a published standard/test vector | **Independent** | Strongest. Prefer for anything at E3+. |
| Taken from production records or the pre-change implementation | **Independent** (differential) | Encodes current truth, not intended truth — pair with spec review for behavior changes. |
| Confirmed by the domain owner | **Independent** | Required where the rule is business policy, not computation. |
| Read off the implementation under test | **Not independent** | Records what the code does. Cannot detect that the code is wrong. |
| Generated by the same agent, same session, same context as the code | **Not independent** | Default state of unguarded AI test generation. |

**Rule:** any change whose floor is E4 or above must carry at least one assertion whose provenance is in the first three rows.

### Independence calibration

When a common cause is suspected, these do not fix it — and these do:

| Common cause | Weak additional evidence | Genuinely independent evidence |
|--------------|--------------------------|--------------------------------|
| Spec misunderstanding | more tests from the same explanation | domain example, contract, user validation |
| API/symbol does not exist as assumed | ask another model | official versioned docs, compiler, runtime smoke |
| Tests are weak | raise coverage | mutation, fuzz, replay of known failures |
| Retrieval gap | regenerate the answer | corpus coverage check, retrieved-source audit |
| Tool call believed to have succeeded | the model's success message | external receipt, query the system state |
| "It can be rolled back" | it says so in the runbook | staging/production rollback rehearsal |

The left column is what teams reach for by reflex, and it is the column that leaves the failure in place.

### Breaking the loop — cheapest first

1. Give the spec **invariants, examples, counterexamples, and non-goals** before generation, so the expectation has a source outside the code.
2. **Separate the contexts**: author the oracle in a session that has never seen the implementation, or before it exists.
3. Add **one E4 mechanism** — a property, a mutation run over the changed lines, or a differential against the old path.
4. Record in the PR **what the tests prove and what they do not**.

---

## 3. Change-type evidence recipes

Starting plans, not standards — adjust for jurisdiction, architecture, data, SLO, and team capability. Each names the failure the evidence must catch, because evidence that does not match the risk mechanism is volume, not proof.

| # | Change type | Failure focus | Evidence plan |
|---|-------------|---------------|---------------|
| `R01` | Small UI / copy change | DOM role & accessible name, locale fallback, viewport visual diff — not snapshots alone | E1 lint/type · E2 component render · E3 a11y/visual regression · E5 preview |
| `R02` | REST/GraphQL API addition | schema, authz, validation, idempotency, error contract, rate limit — verified separately | E1 schema/type · E3 contract/integration · E4 abuse/fuzz · E5 consumer preview · E6 error rate |
| `R03` | DB schema migration | expand-migrate-contract, lock time, backfill, checksum, forward recovery | E1 migration lint · E2 representative copy · E3 old/new compatibility · E5 staging load · E6 canary metrics |
| `R04` | Authn / authz change | privilege escalation, tenant crossing, revocation, clock skew, fail-closed — before the happy path | E1 policy/dependency rule · E3 protocol/integration · E4 abuse & negative property · E5 security approval · E6 auth error rate |
| `R05` | Payment / billing logic | minor units, rounding, timezone, idempotency, ledger consistency, provider partial failure | E1 money type · E3 contract/integration · E4 property/differential · E5 shadow invoice · E6 reconciliation |
| `R06` | Dependency update | changelog, breaking change, publisher, license, CVE, build reproducibility, runtime behavior | E1 lockfile/SBOM/scanner · E3 full regression · E5 artifact provenance · E6 error & resource |
| `R07` | Legacy component extraction | call inventory, characterization, dual read/write, cutover, rollback | E1 dependency graph · E3 characterization · E4 differential · E5 shadow · E6 business reconciliation |
| `R08` | Performance optimization | bottleneck hypothesis, representative workload, tail percentile, correctness, resource trade-off | E0 profile · E2 microbenchmark · E3 load/regression · E5 production-like · E6 p95/p99 & saturation |
| `R09` | Security fix | reproduction conditions, attack surface, patch completeness, regression — without publishing exploit detail | E1 SAST/dependency/policy · E3 regression · E4 abuse/fuzz · E5 security review · E6 detection telemetry |
| `R10` | Incident remediation | timeline, change, metric, trace, hypothesis, **disconfirming** evidence | E0 reproduction/telemetry · E2 minimal fix · E3 regression · E5 canary · E6 recovery & no recurrence |
| `R11` | LLM answer-quality change | schema, critical failures, representative & adversarial slices, human calibration, latency/cost together | Test: schema & forbidden action · Eval: groundedness/utility/abstention · Online: feedback & escalation |
| `R12` | RAG / retrieval change | source coverage, freshness, tenant isolation, recall, precision, citation entailment | E1 schema/ACL · E3 retrieval set · E4 conflict/stale/empty corpus · E6 no-evidence & citation audit |
| `R13` | Tool calling addition | argument schema, identity, target, authorization, idempotency, timeout, receipt | E1 schema/policy · E3 broker integration · E4 malicious arguments · E5 sandbox action · E6 audit & rollback |
| `R14` | Granting an agent production write | delegation boundary, capability, approval, two-phase execution, budget, rollback rehearsal | E1 policy-as-code · E3 simulation · E4 bypass & partial failure · E5 explicit approval · E6 action receipt & business metric |
| `R15` | Model / provider switch | task-specific quality, data region, retention, tool & structured output, latency, cost, outage | E1 contract · E3 offline eval · E4 critical slices · E5 shadow · E6 canary & fallback |
| `R16` | Prompt / policy update | change reason, targeted failure, regression scope, token growth, conflicting instructions, rollback | E1 syntax/template · E3 regression set · E4 injection & conflict · E5 shadow · E6 violation & abstention |
| `R17` | Retrieval index rebuild | document count, coverage, ACL, duplicates, freshness, index↔source correspondence | E1 manifest · E3 golden queries · E4 missing & conflict · E5 shadow index · E6 citation & no-result |
| `R18` | Secret / network policy change | target allowlist, TTL, scope, DNS/proxy, audit, revocation, break-glass | E1 policy test · E3 denied/allowed paths · E4 exfiltration simulation · E5 security approval · E6 egress log |
| `R19` | AI feature touching personal data | purpose, lawful basis, minimization, retention, training use, subprocessor, deletion | E1 data flow & classification · E3 redaction/access · E5 privacy & legal review · E6 audit & deletion exercise |
| `R20` | Supply chain / build change | source integrity, hermeticity, dependency, provenance, identity, secret isolation | E1 config/policy · E3 reproducible build · E4 tamper simulation · E5 attestation/signature · E6 artifact verification |
| `R21` | Rollback / recovery mechanism | execution time, data compatibility, external side effects, owner, communication | E2 local rollback · E3 state transition · E5 staging rehearsal · E6 recovery time & integrity |

**Delegation notes that recur:** short diffs are not automatically low risk (`R01` — legal copy, consent, billing, delete confirmations need the domain owner). Patch-version auto-merge is not a safe default (`R06`). An agent can write a migration but cannot decide the acceptable lock window (`R03`). An AI's repository summary is not evidence of understanding (`R07`). An AI's root cause is a hypothesis and must not delay the rollback decision (`R10`). Natural-language confirmation is not a control — the broker rejects (`R13`). Never start an agent at full production write; climb read-only → draft → sandbox → approved (`R14`). Change model, prompt, and index one at a time or you cannot isolate the cause (`R15`, `R17`).

---

## 4. Evidence Bundle completion criteria

An Evidence Bundle is **not** a collection of things that passed. It exists so someone can decide, so it must carry:

- which **risk** each piece of evidence addresses (evidence with no named risk is filler);
- the **failures** — failed runs, flaky reruns, excluded cases;
- what is **not verified**, and who accepts that residual risk by name;
- **model / tool versions and environment deltas**, so the run is reproducible;
- a summary separated from raw artifacts when volume would hide the decision point.

If the bundle cannot answer "what would have to be true for this to be wrong, and did we look?", it is not done.

---

## 5. Verification Debt — when generation outruns verification

Generation is instant; understanding, testing, integration, and production observation are finite. When arrival rate exceeds verification capacity, unverified state accumulates and it stops being knowable which changes are safe.

**Where it comes from:** multiple concurrent agents, parallel branches, AI test generation, and short-horizon KPIs — with no limit on arrival rate and no management of WIP, age, or risk.

**Detection signals** (read per risk class, never as a single average): generated-vs-verified gap · PR age · review wait · flaky rate · rework rate · owner coverage · count of open `not_verified` items.

**Response:** cap agent WIP rather than adding reviewers; drain highest-risk and oldest first; delete branches and PRs that are no longer wanted instead of carrying them; repair the test signal itself — a suite nobody trusts produces no verification regardless of how often it runs.

**Residual:** a temporary gap is normal and not a defect. The failure mode is unverified state that has acquired **no risk class and no deadline**.

---

## 6. Anti-patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Requiring E6 for everything | verification cost collapses throughput; teams then bypass the gate entirely |
| Treating coverage as the ceiling metric | coverage measures execution, not detection — climb to E4 (mutation) instead |
| Adding a second AI reviewer as "independence" | shared priors, not an independent mechanism (§2) |
| Golden/snapshot updated without reading the diff | converts an oracle into a transcript of whatever the code now does |
| Piling on evidence at the same level | five E3 suites detect one class of failure; one E4 detects another |
| Evidence that arrives after the decision | unread proof is not proof |
| Static analysis nobody trusts | stale rules, high false positives, easy suppression — signal degrades to noise; fix trust before adding tools |
