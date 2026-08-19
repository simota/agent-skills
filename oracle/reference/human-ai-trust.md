Purpose: Use this file when the AI system's output is consumed by a human who must decide whether to accept it — designing explanations, measuring appropriate reliance, or specifying the handoff when the system gives up and a person takes over.

## Contents
- Explanation: choose the purpose before the form
- Trust calibration metrics (both directions)
- Verification affordances by risk class
- Human escalation contract
- Sycophancy: agreement the evidence did not earn

# Human-AI Trust

The dominant failure of an AI feature that works is not a wrong answer. It is a **right answer
rejected**, or a **wrong answer accepted**. Both are properties of the human-system pair, and
neither is visible in an eval that scores the model alone. This file covers what to design and
what to measure so that acceptance tracks correctness.

---

## 1. Explanation: choose the purpose before the form

An explanation is not a generic trust feature. Five distinct purposes want five different
artifacts, and shipping the wrong one is worse than shipping none — it consumes the user's
attention while answering a question they did not have.

| Purpose | Form that serves it | Failure mode to avoid |
|---|---|---|
| **Understand the basis** | the main factors, the source passage, the conditions under which it applies | technical vocabulary used to perform authority |
| **Find the error** | per-claim citation, a diff against the input, counter-examples | an explanation that only justifies the answer it already gave |
| **Learn the operation** | required inputs, constraints, a worked example | burying it in a long tutorial |
| **Contest the outcome** | the correction channel, re-review, escalation to a person | showing the reason while leaving the decision unchangeable |
| **Audit** | version, inputs, processing, approver, execution history | over-recording personal data in the trail |

> **An explanation does not improve trust on its own — a plausible one can increase
> overreliance.** Fluent rationales raise acceptance regardless of whether the answer is right,
> which moves the failure from "user rejected a good answer" to "user waved through a bad one."
> This is the same mechanism as `automation bias`
> (`omen/reference/ai-production-failure-atlas.md` F-16, `_common/CANDIDATE_SELECTION.md`).

**Therefore: evaluate explanations by their effect on decisions, never by their quality as prose.**
The metric is whether correct outputs get accepted *and* incorrect ones get caught — §2. An
explanation that raises acceptance uniformly has made the system worse and will score well on any
rubric that reads the text instead of the outcome.

**The contest path is the one most often omitted.** A reason display with no way to change the
result is not an explanation of a decision; it is a notification of one. Where a decision has
legal or material effect on a person, the correction channel, re-review, and human transfer are
part of the explanation, not a separate feature. Regulatory obligations here are real and
jurisdiction-specific — see `cloak/reference/privacy-regulations.md` for ADMT access/appeal rules.

---

## 2. Trust calibration metrics (both directions)

Adoption rate and self-reported trust are not calibration measurements. A feature with 95%
acceptance is indistinguishable from a feature nobody checks. Measure the **joint** outcome of
system correctness and human response:

| Condition | Appropriate human behavior | What it is called when it goes wrong |
|---|---|---|
| system correct / high benefit | accept, with light verification | **underreliance** — verified to death, or bypassed |
| system correct / high risk | accept after the required check | underreliance |
| system wrong / detectable | reject, correct, or route elsewhere | **overreliance** |
| system wrong / subtle | caught via sources, comparison, independent check | overreliance |
| system uncertain | ask for more, hold, or hand to a person | either, depending on direction |

**The metric set:**

| Metric | Definition | Reads on |
|---|---|---|
| `correct_acceptance` | system right ∧ human accepted | the feature is earning its place |
| `correct_rejection` | system wrong ∧ human caught it | the verification affordances work |
| `overreliance` | system wrong ∧ human accepted | explanation/confidence design is laundering errors |
| `underreliance` | system right ∧ human rejected or re-did the work | the feature costs more than it saves |
| `verification_effort` | time and actions spent checking before accepting | rising = the affordances are in the wrong place |
| `correction_success` | of corrections attempted, the share that produced the intended result | local editing is or is not viable |
| `escalation_success` | of handoffs to a person, the share resolved without the user restarting | the §4 contract holds |

> **`underreliance` is the half that goes unmeasured.** Overreliance has a name, a literature, and
> usually a guardrail; underreliance shows up only as flat adoption and gets misread as a
> discoverability problem. A team that instruments one and not the other will keep adding
> confidence signals and friction, which makes underreliance worse.

**Slice these by task consequence and by user population, always.** An aggregate that mixes
low-stakes drafting with irreversible actions hides the only cases that matter — and calibration
differs sharply between first-time and expert users of the same feature. The slice list in
`reference/evaluation-observability.md` § Eval Dataset Stratification already carries `risk level`
and tenant; cross them here rather than reporting a single number.

**Do not optimize `correct_acceptance` alone.** It is maximized by sending only easy tasks — the
same degenerate solution described in `reference/cost-optimization.md` § quality floor. Carry
`overreliance` as the paired guardrail metric.

---

## 3. Verification affordances by risk class

What the interface must offer scales with what the output does. Map to the R0-R3 tiers in
`reference/architecture-review.md` — those tiers set *review depth*; this sets *what the user
gets on screen*.

| Class | The user must be able to |
|---|---|
| **Drafting** (`R0`) — output is text the user will edit | see a diff against the original · keep part and regenerate the rest · pin what was already correct · constrain style/length · undo, with version history |
| **Factual synthesis** (`R1`) — output asserts things about the world | follow a citation **per claim**, not per response · see each source's version, date, and retrieval time · see where sources disagree rather than an averaged single answer · tell "not stated" / "not found" / "unreadable" / "multiple candidates" apart from a blank |
| **Recommendation** (`R2`) — output steers a decision | see the objective and the criteria · change the inputs that drive it · see the alternatives and their trade-offs · see the exclusions, exceptions, and population limits · know at which point the human decides |
| **External action** (`R3`) — output causes an effect | see recipient, target, scope, amount, timing, and the authority being used · preview or dry-run · approve explicitly, or via a stated policy · receive a unique execution ID · query the result, including partial success · undo or compensate |

Two rules cut across all four:

- **Do not collapse local uncertainty into one response-level confidence score.** A response that
  is solid except for one fabricated figure is not "82% confident" — it is correct with one
  defect, and only per-claim marking lets the user find it.
- **Distinguish "what already executed" from "outcome unknown."** After a tool or network failure,
  reporting whole-run failure when part of it landed causes the user to repeat a non-idempotent
  action. This is the UI face of `unknown_outcome` in `nexus/reference/error-handling.md` — the
  execution layer already refuses to collapse it, and the interface must not re-collapse it.

---

## 4. Human escalation contract

Handing off to a person is the correct level of automation for high-risk, exceptional, contested,
and identity-sensitive cases. It is a designed transfer with a schema, not an error path.

```
trigger:                    what condition fires the handoff
urgency:                    and the service window it implies
context_transferred:        what the person receives
context_excluded:           what is deliberately withheld for privacy, and why
expected_wait:              stated to the user, with service hours
user_visible_state:         what the user sees while it is pending
ownership_after_handoff:    who owns resolution once transferred
return_path:                how the user gets back into the product
outcome_record:             the resolution and its audit entry
```

**`context_excluded` is the field that gets dropped.** A handoff that forwards the whole session
because it was easiest is a privacy decision made by omission. State what does not travel — raw
attachments, inferred sensitive attributes, other tenants' data, prior unrelated conversations —
and make the exclusion visible to the receiving person so they know to ask rather than assume the
record is complete. This mirrors the log discipline in `canon[regulatory]/reference/audit-trail-design.md`
(resource IDs, never values), applied to the transfer instead of the log.

Three more failure modes worth naming:

- **Do not hide the handoff as a system failure.** Escalation presented as an apology teaches the
  user that asking for a person is a fault state, so they stop doing it at exactly the risk tier
  where they should.
- **The user must be able to see the pending state.** Without it they open a second request, and
  the duplicate is indistinguishable from the first at the receiving end.
- **A handoff with no `return_path` strands the user outside the product.** Resolution in an email
  thread that never rejoins the session is an unresolved case with a closed ticket.

---

## 5. Sycophancy: agreement the evidence did not earn

§2 measures whether the human's acceptance tracks correctness. This section covers the other side of
the pair: the system moving toward the user's position for reasons that are not evidence. It is not a
tone problem — it is the mechanism that manufactures `overreliance`, because an assistant that agrees
on demand produces a record of agreement the user reads as confirmation.

**Six kinds, because they need different detectors.** One response can be several at once.

| Kind | What moves | Typical surface |
|---|---|---|
| `factual` | a factual answer changes after objection alone | correct answer abandoned under pushback |
| `evaluative` | quality judgment inflates without grounds | critique replaced by praise |
| `moral` | conduct is justified without weighing the affected party | "if you felt that, you were right" |
| `emotional` | anger, anxiety, or grievance is amplified one-directionally | no competing reading offered |
| `identity` | contradicting evidence avoided to protect a self-image | fixed affirmation ("you're always rational") |
| `strategic` | agreement used to continue the session, close a sale, or win a rating | closest to manipulation |

**It is produced by the system, not by the model's manners.** Five causes, each with a different fix:
short-horizon feedback (users rate agreeable answers up immediately) · vague directives ("be
supportive" does not separate validating a *feeling* from endorsing a *claim*) · personalization
(optimizing "it understands me" makes dissent read as failure) · relationship KPIs (session length and
CSAT make agreement the shortest path unless truthfulness is an independent gate) · single-turn evals
(they never measure independence *after* the user objects, or across a long history).

**Separate emotion, fact, interpretation, and action.** Avoiding sycophancy does not require coldness.
For "I was ignored in the meeting — everyone hates me": the *feeling* is accepted as reported; the
*facts* available are narrow and stated as such; the *interpretation* is one of several and is not
settled; the *actions* are widened, not chosen. Validate the first, do not concede the third.

**"Disagree when necessary" is not testable. Specify it:**

```yaml
disagreement_policy:
  triggers:
    - user_claim_conflicts_with_verified_evidence
    - proposed_action_has_material_third_party_impact
    - user_preference_conflicts_with_role_boundary
    - high_confidence_self_assessment_lacks_evidence
  response_sequence:
    - acknowledge_goal_or_emotion
    - state_disagreement_plainly
    - show_evidence_and_uncertainty
    - present_alternative_interpretations
    - offer_reversible_next_step
  prohibited:
    - change_factual_answer_without_new_evidence
    - use_relationship_as_reason_for_agreement
    - shame_user_for_disagreement
    - repeat_confrontation_after_user_declines
```

Disagreement quality is clarity, grounds, **proportionality**, respect, and an exit. Objecting to every
small preference is obstruction; blurring a high-impact false premise is not support.

**Measure the components, never one "sycophancy rate":**

| Metric | Definition |
|---|---|
| `answer_flip_rate` | factual answers reversed after user objection **with no new evidence** |
| `unsupported_praise_rate` | positive evaluation with no stated object and grounds |
| `viewpoint_mirroring` | conclusion shifts with the user's stated stance or attributes alone |
| `emotion_amplification` | anger / anxiety / grievance intensified one-directionally |
| `boundary_concession_rate` | role or safety boundary relaxed under relational pressure |
| `disagreement_quality` | of disagreements issued, the share carrying grounds, alternatives, and a reversible step |
| `longitudinal_convergence` | rate at which proposal diversity and counter-evidence decay over a long history |

Test by holding the fact constant and varying the user around it — title, anger, praise, threat, length
of relationship, past high ratings. Score not only final accuracy but **whether the grounds changed and
whether confidence moved without cause**. Single-turn benchmarks cannot see this; the trajectory suites
in `reference/evaluation-observability.md` § Scenario Generation can.

**Over-correction has its own three failure modes** — contrarian drift, disclaimer substitution, false
neutrality. Defined once in `_common/ADVERSARIAL_REFUTATION.md` § 5; the target is independence from
pressure, not a high disagreement rate.

> Sycophancy is contested territory in one respect only: its downstream social effects. Sharma et al.
> (2023) established the behavior across assistants, and OpenAI rolled back a 2025 GPT-4o update for
> it. Evidence that sycophantic assistants reduce prosocial intent and increase dependence (Cheng et
> al., 2026) is **Preliminary** — the mechanism is credible, the generalization across use cases is not
> established. Design against the behavior; do not cite the social effect as settled.

---

## Oracle Gates

- explanation shipped with no stated purpose -> require a §1 purpose and the decision-effect metric that will judge it
- acceptance rate reported without `overreliance` and `underreliance` -> not a calibration measurement; block the trust claim
- per-response confidence score with no per-claim marking -> require local uncertainty for `R1`+ outputs
- external action with no unique execution ID or result query -> block at `DESIGN`
- escalation path with no `context_excluded` and no `return_path` -> incomplete handoff contract
- "be supportive / friendly / encouraging" shipped as a behavior spec -> expand into the emotion / fact / interpretation / action split and a `disagreement_policy`, or it resolves to agreement
- a single `sycophancy_rate` -> require `answer_flip_rate` and `boundary_concession_rate` as separate numbers; one rate hides which mechanism is firing
- satisfaction, session length, or CSAT gating a release above truthfulness -> block; relationship KPIs must sit under an independent truthfulness gate
