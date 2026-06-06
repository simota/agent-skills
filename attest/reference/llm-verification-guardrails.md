# LLM-Assisted Specification Verification

Purpose: Read this when using LLM assistance during `INGEST`, `EXTRACT`, `GENERATE`, or `VERIFY`, and when you need guardrails against hallucinated evidence or verdict inflation.

## Contents

- [Capability tiers](#capability-tiers)
- [Phase strategies](#phase-strategies)
- [Evidence chain pattern](#evidence-chain-pattern)
- [Guardrail rules](#guardrail-rules)
- [Communication roles](#communication-roles)
- [Anti-patterns](#anti-patterns)

## Capability Tiers

### Tier 1: Reliable

| Task | Why it is acceptable |
|------|----------------------|
| Ambiguity detection | Catalogs and pattern scans constrain the reasoning space |
| BDD scenario generation | Structural templates limit drift |
| Explanation generation | Converts structured findings into prose |
| Testability evaluation | Classification rules are explicit |
| Dangerous-expression scan | Uses anchored pattern catalogs |

### Tier 2: Assisted

| Task | Main risk | Required mitigation |
|------|-----------|---------------------|
| Code-spec compliance judgment | Hallucinated `file:line` evidence | Verify all references against actual files |
| Implicit assumption inference | Over-inference from silence | Mark confidence and keep it below `HIGH` without support |
| Contradiction detection | False contradiction from misunderstood context | Require at least two supporting evidence points |
| Spec-gap identification | Invented requirements | Ground each suggestion in quoted spec context or explicit domain convention |

### Tier 3: Forbidden

| Task | Why forbidden |
|------|---------------|
| AI-only `CERTIFIED` verdict | Final verdicts must be deterministic and evidence-based |
| `FAIL` based only on LLM inference | Absence requires real search evidence |
| Formal-verification substitute | LLM output is probabilistic, not mathematically sound |
| Verdict override without evidence | Every override requires explicit evidence |

## Phase Strategies

| Phase | Recommended strategy | Constraint |
|-------|----------------------|-----------|
| `INGEST` | Zero-shot with format examples | Use examples only to classify format |
| `EXTRACT` | Few-shot with criterion extraction examples | Keep output grounded in source text |
| `GENERATE` | Template-constrained generation | Do not let the model invent scenario structure |
| `VERIFY` | Evidence-first reasoning chain | Verdict depends on verified evidence, not fluent prose |
| `ATTEST` | Rule-based verdict, LLM for explanation only | Decision thresholds stay mechanical |

## Evidence Chain Pattern

Use the sequence below during `VERIFY`:

```text
1. Quote what the criterion requires.
2. Search for implementation artifacts using explicit terms.
3. Read each candidate artifact and assess match quality.
4. Assign verdict from evidence completeness.
5. Assign confidence from evidence directness.
```

## Guardrail Rules

1. Evidence first: never state `PASS`, `PARTIAL`, or `FAIL` without `file:line` or `spec:section` evidence.
2. Confidence gating: if confidence `< 0.5`, route to `NOT_TESTED` with a runtime plan.
3. Reference verification: cross-check every LLM-produced file path and line number against actual file reads.
4. Dual verification for `CRITICAL`: run two independent reasoning passes; disagreement triggers review.
5. Probe self-check: remove adversarial probes whose claimed gap is already covered by the spec.
6. No verdict inflation: ambiguous evidence defaults to `PARTIAL` or `NOT_TESTED`, never optimistic `PASS`.

## Communication Roles

### Explanation Assistant

Use the LLM to:

- translate structured findings into stakeholder-readable language
- explain why a criterion failed or stayed partial
- produce concrete impact statements without changing the evidence set

### Refinement Assistant

Use the LLM to:

- rewrite `AMBIGUOUS_FLAG` items into measurable criteria
- propose testable replacements that preserve business intent
- produce before/after wording for `Scribe` handoff

## Anti-Patterns

| Anti-pattern | Failure mode | Prevention |
|-------------|--------------|------------|
| Confident hallucination | Non-existent `file:line` reference | Always re-open referenced files |
| Over-inference | Complex behavior inferred from thin evidence | Require multiple evidence points |
| Spec projection | Best-practice ideas presented as requirements | Quote the source requirement or mark as suggestion |
| False absence | Feature declared missing under the wrong search terms | Use multiple search strategies before `ABSENCE_CHECK` |
| Verdict inflation | Weak evidence upgraded to `PASS` | Keep deterministic thresholds and confidence gating |
