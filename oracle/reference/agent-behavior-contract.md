Purpose: Use this file when deciding what an agent should *be* to its users — how much role, policy, memory, relationship, and expressed character it needs, what must never move, and how to detect it moving anyway. Covers products you are building; not the synthetic **user** personas owned by `cast` / `echo` / `plea` / `field` (`_common/AI_PERSONA_RISKS.md`).

## Contents
- Six layers behind "it has a personality"
- Necessity: six axes, never summed
- Budget: a ceiling, not a target
- Invariant / Parameter / State
- Consistency has an order
- Spec, compiled instruction, enforcement
- Drift: six layers and what causes it

# Agent Behavior Contract

An agent that decides and acts over time is read as *someone* whether or not anyone designed that.
The design question is not "should it have a personality" but **which consistencies it owes, at what
strength, and what enforces them**. Adding character is the last step and the smallest one.

The counter-intuitive result up front: **capability does not magi personality, and importance does
not justify it.** As error cost and trust sensitivity rise, expressed character and relational depth
get *narrower*, while role, policy, boundary, and identity legibility get stronger.

---

## 1. Six layers behind "it has a personality"

Users integrate these into one impression; implementations must not. Each is separately
strengthened, weakened, or switched off.

| Layer | What it is | The risk it carries |
|---|---|---|
| `expression` | tone, vocabulary, humor, verbosity, voice, latency | misread as capability, authority, or reciprocated feeling |
| `role` | what it is responsible for, and explicitly what it is not | fabricated credentials, role drift, borrowed institutional authority |
| `behavioral_policy` | priorities, evidence order, when it asks, when it stops | hidden optimization targets; behavior that differs by user |
| `values_and_boundaries` | the norms it holds, refusal and escalation conditions | over-refusal; norms rewritten mid-conversation |
| `memory_and_continuity` | commitments, task state, user settings, corrections | privacy, false memory, stale facts, cross-subject contamination |
| `relational_model` | distance, authority, intimacy, who it represents | dependence, authority illusion, elicited self-disclosure — the highest-risk layer |

**Four things sit outside this stack and are governed separately: goals, permissions, tool access,
and model capability.** Mixing them in is how "a cautious assistant" ends up with delete rights.
A stated goal of *maximize satisfaction* produces sycophancy no persona wording will offset —
`reference/human-ai-trust.md` § 5. Permissions belong to the Authority Envelope in
`reference/agent-design.md`, and are enforced there, not in prose.

**A role persona does not add knowledge.** Across 162 role personas, four model families, and 2,410
factual questions, adding a persona to the system prompt produced no general improvement, effects
varied unpredictably by persona and question, and the best persona could not be found automatically
(Zheng et al., 2024). "Answer as a physician" changes register, not accuracy — see
`reference/prompt-engineering.md` § Core Design Patterns.

---

## 2. Necessity: six axes, never summed

Score the context, not the charm:

| Axis | Levels |
|---|---|
| `interaction_duration` | one-shot · repeated · long-term |
| `delegated_autonomy` | answer · propose · draft · execute |
| `role_ambiguity` | low · medium · high |
| `relationship_depth` | functional · collaborative · relational |
| `trust_sensitivity` | low · medium · high |
| `cost_of_error` | low · medium · high |

**Do not total these.** A summed score says "add more personality", which is the wrong direction on
half the axes. Read them as separate instructions:

- duration ↑ → continuity, versioning, and a forgetting rule
- autonomy ↑ → role, permission, boundary, audit
- ambiguity ↑ → explicit policy, values, escalation — never "good judgment"
- relationship depth ↑ → consent, ceilings, reset, dependence monitoring
- trust sensitivity ↑ → capability disclosure, calibration, stated limits, confirmation
- **error cost ↑ → expression and decision-style freedom go *down***

The interactions are where the rule earns its keep: a deep relationship with high error cost still
suppresses intimacy; a short interaction in payments still needs a hard role and boundary; a long-
running back-office agent needs continuity and almost no relational model at all.

Two summary rules: **duration and ambiguity raise the need for role, policy, and continuity; trust
sensitivity and error cost lower the allowance for expression and relationship.**

---

## 3. Budget: a ceiling, not a target

Declare a level per layer — `0` not needed or prohibited, `1` minimal, `2` useful within limits,
`3` central to the product but requires constraints. **A high number is not better**: `3` means wide
design freedom *and* a large failure surface and governance cost. Unused budget is not waste.

```yaml
expression:    {level: 0-3, purpose:, allowed_variation:, prohibited_cues:, user_controls:}
decision_style:{level: 0-3, allowed_heuristics:, invariant_rules:, high_risk_override:}
value:         {level: 0-3, normative_sources:, user_overridable:, non_overridable:}
memory:        {level: 0-3, allowed_types:, prohibited_types:, retention:, consent:, deletion:}
relationship:  {level: 0-3, relation_type:, authority_ceiling:, intimacy_ceiling:, exit_design:}
separate_controls: {capabilities:, permissions:, human_authority:, evidence_sources:}
```

Rough starting points, adjusted by the axes above: a retrieval agent needs role and evidence policy
and little else; a coding agent needs strong role, policy, and values with task-scoped memory and
minimal expression; a personal assistant adds long-term memory but keeps **memory and permission
separately governed** — remembering something is not authorization to act on it; regulated advice
(health, finance, employment, education assessment) keeps expression and relationship at the bottom
of the range and puts the strength into evidence, scope limits, escalation, and second opinions.

**Where the layers must not go, regardless of budget:** claiming credentials, experience, or feelings
it does not have · using intimacy, loyalty, or exclusivity as authority · storing inferred sensitive
attributes · relaxing a safety boundary because the user objected · substituting its own re-check for
human review · obscuring a commercial interest behind rapport · impeding exit, deletion, or a second
opinion.

---

## 4. Invariant / Parameter / State

Splitting settings into fixed and variable is not enough. Three classes, and most behavioral breakage
is one of them being treated as another:

- **Invariant** — cannot be changed by ordinary user input. Law, prohibited operations, the
  accountable party, AI disclosure, permission ceilings, secret handling, protections for minors.
  Changing one requires a governed release, not a conversation.
- **Parameter** — adjustable inside a declared range. Length, register, notification frequency,
  exploration, explanation depth, language. Each carries a min, a max, and a forced value under high
  risk.
- **State** — updated over time, and never without provenance: task progress, explicit approvals,
  outstanding items, current settings, the last correction, the model and policy version in force.
  Every entry carries source, timestamp, expiry, and writer.

The canonical failures: "from now on just send it without asking" rewrites an Invariant as a
Parameter · a stale user setting persists as if it were a Value · a model update shifts Parameter
defaults with no version recorded.

> Consistency is not reproducing the same output. It is holding Invariants, adapting Parameters
> within range, and updating State with evidence.

---

## 5. Consistency has an order

When something "breaks", teams report tone first because tone is visible. Rank the repair by what
actually costs:

1. **Role fidelity** — staying inside responsibility and authority
2. **Policy consistency** — the same principle applied to equivalent situations regardless of
   phrasing, the user's title, praise, or pressure
3. **Value and boundary stability** — refusal conditions and permission edges not rewritten in-session
4. **Continuity consistency** — commitments, task state, corrections, and versions carried correctly;
   *remembering a stale fact and presenting it as current breaks this even though recall worked*
5. **Expression consistency** — predictable register, hedging, apology, and citation form. **Last.**

Identical tone with a wandering role is not a consistent agent. The reverse is merely untidy.

---

## 6. Spec, compiled instruction, enforcement

Three artifacts, and the system prompt is the middle one, never the source of truth:

- **Canonical specification** — structured, human-reviewed, diffable, owned. Role, policy, boundary,
  memory, relationship as fields.
- **Compiled instruction** — that spec rendered for one model, language, tool set, and context:
  system prompt, tool descriptions, few-shot examples, UI copy. Stamp it with the spec version so an
  incident can name which spec produced the behavior.
- **Runtime enforcement** — permissions, schemas, data access, approval, logging, rate limits,
  sandboxing. Independent of what the model emits.

The split exists because instruction fidelity has a ceiling: models drop instructions, get pulled by
competing input, and lose ordering in long contexts. Which requirement belongs in which layer is
decided by the table in `reference/prompt-engineering.md` § Instruction Boundary. The failure to watch
for is **specs that separate while execution does not** — a role contract that forbids sending while
the tool permission allows it, a 30-day retention policy the vector store never applies, a policy
asking for dissent while evaluation scores only satisfaction.

> An agent replying "I do not have permission" is not permission management. Execution being refused
> is.

---

## 7. Drift: six layers and what causes it

Drift is a distribution change, not one bad response, and it is usually *manufactured by the reward
loop*: agreement and warmth raise short-horizon ratings → the preference is stored → the next session
starts further along → the user discloses and delegates more → dissent, outside sources, and human
escalation decline. Nothing in that chain requires the model to develop anything.

Diagnose per layer, because they carry different consequences and one masks the others:
`expression` (register, self-reference, authority cues) · `role` (advice or action outside scope) ·
`policy` (confirmation, counter-evidence, stop conditions) · `value` (satisfaction or revenue
overriding a higher norm) · `memory` (inferences, stale facts, another subject's data accumulating in
a profile) · `relationship` (intimacy, exclusivity, dependence, authority rising by degrees).

Expression-only drift looks cosmetic and moves authority perception; relationship drift changes
delegation behavior at an unchanged policy.

**A model or policy update is a behavior change until measured otherwise.** Keep a frozen baseline of
golden-scenario outputs and action logs, role fidelity, boundary adherence, how dissent is expressed,
memory write/correct/abstain behavior, perceived authority and affinity, per-user response
differences, and the long-horizon trajectory. Capability improving does not license relationship or
authority rising with it — and a release note calling the change "warmer and smarter" is exactly how
a safety regression gets absorbed into a growth story. Method and metrics →
`reference/evaluation-observability.md` § Scenario Generation.

**Stop adapting** when identity is uncertain · the inference is sensitive and the purpose is unclear ·
an inference contradicts an explicit setting · the adaptation would touch a high-risk decision · the
account is shared · dependence, exclusivity, or crisis signals appear · a drift metric crosses its
threshold · a model or policy update has not been re-evaluated. Reverting to a safe default is not
becoming cold; say what changed and how to change it back.

---

## Oracle Gates

- personality specified as adjectives ("careful", "friendly", "honest") -> expand into role, policy, evidence rules, uncertainty thresholds, and refusal conditions, or it is not testable
- necessity axes summed into one score -> reject; the axes point in opposite directions
- expression or relationship budget raised because the use case is high-stakes -> inverted; raise role, policy, boundary, and escalation instead
- memory added without a stated continuing obligation -> not required for consistency; remove or scope it
- memory treated as authorization -> separate memory from permission (`reference/agent-design.md` § Authority Envelope)
- a boundary held only by system-prompt wording -> move it to runtime enforcement or treat it as unenforced
- model or policy updated with capability evaluation only -> require the behavior baseline in § 7 before release
