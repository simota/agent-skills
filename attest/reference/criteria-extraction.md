# Criteria Extraction and Specification Quality

Purpose: Read this when ingesting a specification, extracting `AC-*` criteria, classifying testability, raising `AMBIGUOUS_FLAG`, or scoring specification quality.

## Contents

- [Source format detection](#source-format-detection)
- [Extraction strategies by format](#extraction-strategies-by-format)
- [Testability classification](#testability-classification)
- [Dangerous expression catalog](#dangerous-expression-catalog)
- [Requirement smells](#requirement-smells)
- [Acceptance-criteria quality patterns](#acceptance-criteria-quality-patterns)
- [Specification quality metrics](#specification-quality-metrics)
- [AMBIGUOUS_FLAG protocol](#ambiguous_flag-protocol)
- [Criterion ID convention](#criterion-id-convention)
- [INGEST-time quality check flow](#ingest-time-quality-check-flow)
- [Output format](#output-format)

## Source Format Detection

### Auto-Detection Rules

| Indicator | Detected format | Confidence |
|-----------|-----------------|------------|
| `## L3 受入基準` or `## Acceptance Criteria` | `SCRIBE_L3` | `HIGH` |
| `## Functional Requirements` with numbered items | `PRD/SRS` | `HIGH` |
| `As a [role], I want [goal]` | `USER_STORY` | `HIGH` |
| `MUST`, `SHALL`, `SHOULD` keywords | `FORMAL_SPEC` | `MEDIUM` |
| Unstructured feature prose | `FREE_FORM` | `LOW` |

### Confidence Threshold

| Confidence | Range | Action |
|------------|-------|--------|
| `HIGH` | `>= 0.8` | Proceed with automatic extraction |
| `MEDIUM` | `0.5-0.8` | Extract, but add `AMBIGUOUS_FLAG` to uncertain items |
| `LOW` | `< 0.5` | Raise `SPEC_MISSING` and suggest `Scribe` / `Scribe[unified]` |

## Extraction Strategies by Format

### Scribe[unified] L3

```text
Source: ## L3 受入基準 / ## Acceptance Criteria
  -> Each bullet becomes one AC
  -> ID: AC-{feature}-{NNN}
  -> Priority: inherit from parent priority when available
  -> Testability: classify with the matrix below
```

### PRD / SRS

```text
Source: numbered functional requirements
  -> Split compound requirements into separate ACs
  -> MUST / SHALL -> CRITICAL
  -> SHOULD -> HIGH
  -> MAY -> MEDIUM or LOW depending on business impact
```

### User Stories

```text
Primary AC:
  derive from the "I want" canon

Additional ACs:
  derive from explicit acceptance bullets

Implicit ACs:
  infer only when the "so that" canon makes the benefit testable
```

### Free-Form Text

```text
1. Extract action verbs and affected entities
2. Convert them into testable assertions
3. Mark uncertain items as PARTIALLY_TESTABLE or AMBIGUOUS
4. Prefer clarification over over-inference
```

## Testability Classification

| Classification | Meaning | Action |
|----------------|---------|--------|
| `TESTABLE` | Clear input -> expected output or measurable threshold | Generate BDD directly |
| `PARTIALLY_TESTABLE` | Some aspects measurable, others vague | Generate measurable scenarios and flag the rest |
| `AMBIGUOUS` | Expected behavior cannot be determined | Emit `AMBIGUOUS_FLAG` and route for clarification |

### Testability Matrix

| Pattern | Classification | Example |
|---------|----------------|---------|
| “When X happens, Y is displayed” | `TESTABLE` | Login error message |
| “Complete within N seconds” | `TESTABLE` | API response under `200ms` |
| “Should be user-friendly” | `AMBIGUOUS` | Subjective UX criterion |
| “Handle errors gracefully” | `PARTIALLY_TESTABLE` | “Gracefully” needs definition |
| “Data must be encrypted at rest” | `TESTABLE` | Configuration or storage check |
| “Should feel responsive” | `AMBIGUOUS` | Subjective without a metric |

## Dangerous Expression Catalog

Every match below should trigger `AMBIGUOUS_FLAG`.

| Category | Expressions | Problem | Example fix |
|----------|-------------|---------|-------------|
| Subjective adjectives | fast, easy, user-friendly, intuitive | No measurement basis | “Respond within `200ms`” |
| Vague adverbs | quickly, efficiently, seamlessly | Not measurable | “Complete in 3 steps or fewer” |
| Superlatives | best, highest quality | No reference point | “Meet SLA `99.9%`” |
| Comparatives | better, faster, more reliable | Target unknown | “`50%` faster than current P95” |
| Loopholes | if possible, as appropriate, when feasible | Weak obligation | Convert to `must` or remove |
| Vague pronouns | it, they, the system | Referent unclear | Name the component |
| Undefined references | “see related document” | Missing source | Cite document and section explicitly |
| Negations | not slow, not complex | No positive target | Use a measurable positive criterion |
| Open-ended lists | etc., and so on, among others | Scope unbounded | Replace with a closed list |

## Requirement Smells

| Smell | Meaning | Severity |
|-------|---------|----------|
| Ambiguity | Multiple interpretations possible | High |
| Verifiability | Cannot be tested | High |
| Consistency | Contradicts another requirement | High |
| Completeness | Missing required information | Medium-High |
| Complexity | Too much logic in one requirement | Medium |
| Correctness | Factually wrong | High |
| Traceability | Missing parent link | Medium |
| Understandability | Hard to parse | Medium |
| Redundancy | Duplicate requirement | Low |
| Reusability | Over-specialized wording | Low |
| Relevancy | Out of scope | Low |
| Undefined | Quality issue not otherwise classified | Variable |

## Acceptance-Criteria Quality Patterns

### Good Traits

| Trait | Check |
|-------|-------|
| Independent | Can be verified alone |
| Negotiable | Describes `WHAT`, not `HOW` |
| Valuable | Business or user value is explicit |
| Estimable | Scope is bounded |
| Small | Fits a single delivery slice |
| Testable | Deterministic `PASS/FAIL` outcome |

### Quality Anti-Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Vague language | “Works fast” | Add a numeric threshold |
| Too many criteria | `20+` per story | Split the story |
| Too few criteria | Only one happy-path bullet | Add error and boundary behavior |
| Missing NFR | No perf/security/accessibility criteria | Add explicit NFR criteria |
| Missing context | No role or situation | Add role and state context |
| Implementation detail | “Use React” | Replace with user-visible behavior |

## Specification Quality Metrics

| Metric | Target |
|--------|--------|
| `Ambiguity Rate` | `< 10%` |
| `Testability Rate` | `> 80%` |
| `Completeness Rate` | `> 90%` |
| `Defect Injection Rate` | `< 10%` |

### Quality Score

```text
GOOD: Ambiguity < 10%, Testability > 80%, Completeness > 90%
FAIR: Ambiguity < 20%, Testability > 60%, Completeness > 70%
POOR: Below FAIR -> route to Scribe / Scribe[unified] for improvement
```

## AMBIGUOUS_FLAG Protocol

```yaml
AMBIGUOUS_FLAG:
  criterion_id: AC-LOGIN-005
  original_text: "The login should be fast"
  ambiguity_type: UNMEASURABLE | CONTRADICTORY | INCOMPLETE | SUBJECTIVE | OPEN_ENDED
  what_is_missing: "No latency threshold defined"
  suggested_clarification: "Login response time should be under 500ms at P95"
  impact: HIGH
  route_to: Scribe
```

## Criterion ID Convention

```text
AC-{FEATURE}-{NNN}

Examples:
  AC-LOGIN-001
  AC-PAYMENT-015
  AC-GLOBAL-001
```

### Priority Assignment

| Priority | Keywords | RFC 2119 mapping |
|----------|----------|------------------|
| `CRITICAL` | must, required, shall | `MUST`, `SHALL` |
| `HIGH` | should, expected | `SHOULD` |
| `MEDIUM` | may, desirable | `MAY` |
| `LOW` | nice to have, optional | No strict RFC term |

## INGEST-Time Quality Check Flow

```text
1. Dangerous-expression scan -> AMBIGUOUS_FLAG
2. Testability classification -> TESTABLE / PARTIALLY_TESTABLE / AMBIGUOUS
3. Completeness check -> normal / error / boundary coverage present?
4. Consistency check -> contradiction candidates for adversarial probing
5. NFR check -> performance / security / accessibility criteria present?
6. Quality score -> GOOD / FAIR / POOR
```

## Output Format

```yaml
EXTRACTED_CRITERIA:
  spec_source: "docs/login-spec.md"
  spec_format: SCRIBE_L3 | PRD | USER_STORY | FREE_FORM
  extraction_confidence: 0.95
  spec_quality: GOOD | FAIR | POOR
  total_criteria: 12
  by_priority:
    CRITICAL: 3
    HIGH: 5
    MEDIUM: 3
    LOW: 1
  by_testability:
    TESTABLE: 8
    PARTIALLY_TESTABLE: 3
    AMBIGUOUS: 1
  criteria:
    - id: AC-LOGIN-001
      text: "Valid credentials grant access to dashboard"
      priority: CRITICAL
      testability: TESTABLE
      source: "login-spec.md:L24"
      related_criteria: [AC-LOGIN-002, AC-LOGIN-003]
  ambiguity_flags:
    - criterion_id: AC-LOGIN-005
      type: UNMEASURABLE
      suggestion: "Define latency threshold"
```


## ISO/IEC/IEEE 29148 Quality Gate (SKILL.md excerpt)

Before extraction is complete, validate each criterion against these attributes:

| Attribute | Check |
|-----------|-------|
| Necessary | Traces to a real stakeholder need; prevents scope creep and gold-plating |
| Verifiable | Can be confirmed by inspection, analysis, demonstration, or test |
| Unambiguous | Single interpretation only; no subjective adjectives ("fast", "user-friendly") |
| Consistent | Does not contradict other criteria in the same spec |
| Singular | Addresses one requirement (no conjunctions splitting behavior) |
| Complete | Self-contained — verifiable without chasing cross-references |
| Feasible | Achievable within known technical and resource constraints |
| Traceable | Links to a source requirement and can link forward to implementation |
| Implementation-free | Describes what, not how |

Flag violations as `QUALITY_DEFECT:{attribute}` and report in Specification Quality Feedback.



## INTERACTION_TRIGGERS Question Templates (SKILL.md excerpt)

```yaml
questions:
  - question: "No specification found. How would you like to proceed?"
    header: "Spec Source"
    options:
      - label: "Delegate spec creation to Scribe/Scribe[unified]"
        description: "Create the specification first, then run verification"
      - label: "Reverse-extract spec from code (EXTRACT)"
        description: "Infer implicit specifications from existing implementation and report"
      - label: "Specify the spec file path manually"
        description: "Provide the specification file location manually"
    multiSelect: false
```

```yaml
questions:
  - question: "The specification contains 20+ acceptance criteria. Select the verification scope."
    header: "Scope"
    options:
      - label: "Verify all criteria (recommended)"
        description: "Exhaustively verify every acceptance criterion"
      - label: "CRITICAL/HIGH only"
        description: "Limit verification to high-priority criteria"
      - label: "Diff-related criteria only"
        description: "Auto-select criteria affected by recent changes"
    multiSelect: false
```



## Signal Keywords → Recipe (SKILL.md excerpt)

For natural-language input without a subcommand; a subcommand match wins. Mode auto-detect runs in parallel — explicit Recipe selection overrides it.

| Keywords | Recipe |
|----------|--------|
| `verify`, `compliance`, `spec check` | `verify` |
| `extract criteria`, `acceptance criteria` | `bdd` (with `EXTRACT` mode) |
| `audit`, `traceability`, `coverage gap` | `trace` |
| `adversarial`, `probe`, `edge cases` | `verify` (with `ADVERSARIAL` mode) |
| `bdd`, `scenarios`, `given when then` | `bdd` |
| `gherkin`, `feature file`, `step definitions`, `cucumber`, `specflow`, `behave` | `gherkin` |
| `property-based`, `invariant`, `hypothesis`, `fast-check`, `jqwik`, `proptest` | `property` |
| `oracle`, `golden master`, `metamorphic`, `differential testing`, `model-based test` | `oracle` |
| unclear spec verification request | `verify` |



## Required Criterion Fields (SKILL.md excerpt)

| Field | Rule |
|-------|------|
| `ID` | `AC-{FEATURE}-{NNN}` (append `_v{N}` when spec revisions change the criterion) |
| `Priority` | `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` |
| `Testability` | `TESTABLE` / `PARTIALLY_TESTABLE` / `AMBIGUOUS` |
| `Source` | Spec document plus section or line reference |
| `V&V Method` | `INSPECTION` / `ANALYSIS` / `DEMONSTRATION` / `TEST` (per IEEE 1012) |

Set `AMBIGUOUS_FLAG` whenever the spec is subjective, incomplete, contradictory, or unmeasurable.
