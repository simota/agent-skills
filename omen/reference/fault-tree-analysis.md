# Fault Tree Analysis Reference

Purpose: Top-down deductive analysis (IEC 61025) that starts from a single undesired top event and decomposes failure logic through AND/OR/XOR/voting gates down to basic events. Produces Minimal Cut Sets (MCS) and, when input probabilities are available, a quantified top-event probability. Use FTA when one catastrophic outcome needs deep causal dissection — not when breadth across many failure modes is the goal.

## Scope Boundary

- **omen `faulttree`**: single undesired top event, deductive AND/OR decomposition, cut-set computation, optional probability roll-up, hand-off to `bowtie` or Triage playbooks.
- **omen `mode` / `premortem` (elsewhere)**: broad FMEA-style enumeration across many components. Use when the question is "what can go wrong?" rather than "why does *this* fail?".
- **siege concurrency (elsewhere)**: concurrency / async / resource-leak root-cause detection. FTA can *reference* a siege concurrency finding as a basic event, but the dynamic debugging stays there.
- **sentinel / breach (elsewhere)**: attacker-driven attack trees. FTA gates are safety-oriented; attack trees invert objectives and belong to Sentinel or Breach.
- **magi (elsewhere)**: trade-offs between competing mitigation paths derived from the tree.

## When FTA Beats FMEA

| Situation | Prefer |
|-----------|--------|
| One catastrophic outcome with many possible combined causes | FTA |
| Broad coverage across many components / modes | FMEA (`mode`) |
| Quantified probability roll-up required | FTA |
| Severity × Occurrence × Detection prioritization | FMEA (`rpn` / `ap`) |
| Regulatory artifact (aviation, nuclear, medical) | FTA |
| Early design hazard scan | FMEA first, then FTA on top hits |

FTA is single-event deep dive; FMEA is broad mode coverage. Use both for safety-critical releases.

## Workflow

```
1. TOP EVENT     pick one undesired, measurable, bounded outcome
                 e.g. "Checkout order placed but not persisted"
                 reject: "system is slow" (not bounded), "bad UX" (not measurable)

2. BOUNDARY      define system boundary, mission phase, time window
                 list assumed-working components (out of tree scope)

3. DECOMPOSE     ask: "what combinations of lower events cause this?"
                 AND  — all inputs must occur
                 OR   — any input suffices
                 XOR  — exactly one input (rare; use sparingly)
                 k/N  — voting / majority-fail (redundancy analysis)

4. TERMINATE     expand until each leaf is either:
                   - a basic event with known (or estimable) probability
                   - an undeveloped event (deferred, marked with diamond)
                   - an external/house event (on/off, binary condition)

5. CUT SETS      compute Minimal Cut Sets via MOCUS (top-down expansion):
                   - replace OR gate → union of child sets
                   - replace AND gate → Cartesian product of child sets
                   - reduce via absorption (X ⊆ Y drops Y)
                 rank MCS by order (size); order-1 cuts are single points of failure.

6. QUANTIFY      if basic-event probabilities known:
                   - independent OR: 1 − Π(1 − pᵢ)
                   - independent AND: Π pᵢ
                   - rare-event approximation: P(top) ≈ Σ P(MCSⱼ)
                   flag the assumption of independence explicitly.

7. HANDOFF       feed cut sets to `bowtie` (left side = threats) or to Triage
                 for playbook construction; escalate order-1 cuts to Magi.
```

## Gate Semantics Cheat Sheet

| Symbol | Gate | Meaning | Typical use |
|--------|------|---------|-------------|
| ∩ | AND | all inputs true → output true | redundant systems both fail |
| ∪ | OR | any input true → output true | single-point failure candidates |
| ⊕ | XOR | exactly one input | mutually exclusive failure paths |
| k/N | Voting | at least k of N | N-modular redundancy |
| ▷ | Priority AND | AND with ordering | sequence-dependent failure |
| ◇ | Inhibit | AND conditioned on a house event | failure only in mission phase X |

### Event symbol shorthand

- **Basic event (circle)**: atomic, quantifiable, no further decomposition.
- **Undeveloped event (diamond)**: could be decomposed but deferred.
- **House event (house)**: binary condition (on during cruise, off during taxi).
- **Conditional event (oval)**: qualifier attached to an inhibit gate.
- **Transfer (triangle)**: subtree continued elsewhere (keep trees readable).

## Worked Mini Example

Top event: *Payment captured but order row missing*.

```
TOP  Payment captured but order row missing
  └─ AND
       ├─ Payment gateway confirms capture   (basic, p=0.9990)
       └─ OR
            ├─ DB write fails silently        (basic, p=1e-4)
            ├─ AND
            │    ├─ Write succeeds             (house: normal path)
            │    └─ Post-commit hook loses row (basic, p=5e-5)
            └─ Idempotency key collision       (basic, p=2e-6)
```

Minimal Cut Sets (order-1 highlighted):
1. `{Payment confirm, DB write fails silently}` — AND, p ≈ 9.99e-5
2. `{Payment confirm, Write succeeds, Post-commit hook loses row}` — p ≈ 5e-5
3. `{Payment confirm, Idempotency collision}` — p ≈ 2e-6

Top-event probability (rare-event approx): ≈ 1.52e-4 per transaction.
Order-1 interpretation: no single basic event alone causes TOP — redundancy is effective against single failures here.

## Anti-Patterns

- Picking a vague top event ("app is unreliable") — tree becomes unbounded and useless.
- Mixing causes and symptoms in the same branch — keep the tree causal, top-down.
- Treating correlated basic events as independent when multiplying probabilities — flag common-cause failures (CCF) explicitly, often with a beta-factor model.
- Expanding a subtree below your evidence base — stop at undeveloped (diamond) rather than inventing numbers.
- Using FTA where the real question is "which of many things might fail?" — that is FMEA territory.
- Redrawing the tree after every review cycle without versioning — keep cut-set deltas between revisions.

## Handoff

- **To `bowtie`**: top event + Minimal Cut Sets become the left-side threats; barriers get attached per cut set.
- **To Triage**: order-1 cuts and top-3 highest-probability cuts seed runbook triggers.
- **To Magi**: when two barrier strategies have comparable risk reduction, hand the cut-set delta to Magi for trade-off arbitration.
- **To Beacon**: basic events with detectability gaps become observability targets (metrics, traces, alerts).
- **To Radar**: each minimal cut set is a test scenario candidate — especially order-1 and order-2 cuts.
