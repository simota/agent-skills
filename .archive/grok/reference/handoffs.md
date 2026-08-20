# Grok Handoff Templates

**Purpose:** Canonical handoff formats for input to Grok and output from Grok to downstream agents.
**Read when:** Packaging deliverables for Builder, Radar, Sentinel, Canon, Atlas, Judge, or Shift; receiving grammar / regex / DSL requests from upstream.

## Contents
- User → Grok (grammar or regex requirement)
- Grok → Builder (parser implementation spec)
- Grok → Radar (fuzz tests for parser)
- Grok → Sentinel (regex security review)
- Grok → Canon (grammar-to-standards mapping)
- Grok → Atlas (parser/AST module boundary)
- Grok → Judge (grammar decision review)
- Grok → Shift (codemod migration plan)
- Nexus ↔ Grok

---

## User → Grok

Received at ANALYZE phase. Grok normalizes informal requirements to grammar class + engine target + trust level before entering GRAMMAR phase.

```yaml
USER_TO_GROK_HANDOFF:
  Scenario: [regex | grammar | DSL | AST-transform | grammar-audit]
  Input:
    sample_text: [path or inline]
    existing_grammar: [path or inline, optional]
    existing_regex: [inline, optional]
    informal_spec: [prose description, optional]
  Context:
    runtime_target: [Node | Go | Rust | Python | Java | .NET | browser | OCaml | multi]
    input_trust_level: [trusted | untrusted | mixed]
    engine_preference: [RE2 | PCRE | ECMAScript | Oniguruma | any]
    generator_preference: [hand-written | tree-sitter | ANTLR4 | Chevrotain | peggy | nearley | Menhir | Lark | any]
    grammar_class_guess: [regular | LL(k) | LR(1) | PEG | Earley | unknown]
    error_message_quality: [best-possible | acceptable | minimal]
    incremental_parsing_required: [yes | no | unknown]
    roundtrip_fidelity_required: [yes | no | n/a]
  Constraints:
    - [hard performance budget, e.g., 1MB/s throughput]
    - [dependency constraints, e.g., no native code]
    - [license constraints]
  Deadline: [if applicable]
```

---

## Grok → Builder

Delivered at IMPLEMENT → DOCUMENT boundary. Builder picks up the implementation spec and writes the parser code.

```yaml
GROK_TO_BUILDER_HANDOFF:
  Artifact: Parser Implementation Spec
  Grammar:
    file: [path to .ebnf / .abnf / .peg / .g4 / tree-sitter grammar.js]
    class: [LL(k) | LR(1) | LALR | PEG | Earley | GLR]
    ambiguities_resolved: [count with brief notes]
    left_recursion: [none | direct | indirect — handling strategy]
  Engine:
    choice: [hand-written RD | tree-sitter | ANTLR4 | Chevrotain | peggy | Menhir | Lark]
    reason: [1-2 lines citing decision matrix from parser-generators.md]
  Tokenizer:
    tokens: [list of token kinds]
    modes: [list of lexer modes if any]
    context_sensitivity: [description if any, e.g., typedef lookup]
    indentation_rules: [description if applicable]
    trivia_handling: [skip | preserve-as-leading-trailing | preserve-as-separate]
  AST:
    node_types: [list with fields]
    position_tracking: [yes — Position has start/end line/column/offset]
    parent_pointers: [stored | computed-on-demand]
    tagged_union: [yes — kind field discriminator]
  ErrorRecovery:
    strategy: [panic | phrase-level | error-productions | incremental]
    diagnostic_style: [Elm-like | rustc-like | Clang-like | minimal]
    sample_diagnostics:
      - scenario: [common parse error]
        message: [example output]
  TestCorpus:
    positive: [path with >=3 inputs per rule]
    negative: [path with >=3 inputs per rule]
    worst_case: [path for regex/ReDoS patterns]
  Performance:
    budget: [e.g., 1MB/s throughput, 10µs parse per typical input]
  NextAgent: Radar (fuzz tests) or DONE
```

---

## Grok → Radar

Delivered when parser edge cases and fuzz corpus are ready. Radar writes fuzz tests and property-based tests against the parser.

```yaml
GROK_TO_RADAR_HANDOFF:
  Artifact: Parser Fuzz Test Corpus
  Parser:
    location: [path to parser under test]
    interface: [function signature or entry point]
  Grammar:
    file: [path]
    critical_rules: [list of rules most likely to break]
  TestInputs:
    minimal_valid:
      path: [path]
      description: [smallest valid input per rule]
    edge_cases:
      path: [path]
      description: [deeply nested, maximum-length tokens, Unicode edge cases]
    adversarial:
      path: [path]
      description: [ReDoS pumping strings, catastrophic backtracking inputs if backtracking engine]
    fuzz_seed_corpus:
      path: [path]
      description: [AFL/libFuzzer-compatible seed files]
  PropertyTests:
    invariants:
      - "parse(input).toSource() === input for valid inputs (roundtrip)"
      - "parse(invalid).errors.length > 0 for every invalid input"
      - "parse(input) terminates in <100ms for any input up to 1MB"
  CoverageTargets:
    grammar_rule_coverage: ">=95%"
    branch_coverage_of_parser: ">=85%"
  NextAgent: Sentinel (if untrusted input) or DONE
```

---

## Grok → Sentinel

Delivered when a regex touches untrusted input, or when a parser runs on network data. Sentinel verifies ReDoS resistance in the full context.

```yaml
GROK_TO_SENTINEL_HANDOFF:
  Artifact: Regex / Parser Security Review Request
  Target:
    pattern_or_parser: [inline regex | path to parser]
    runtime: [Node | Go | Rust | Python | Java | .NET | browser]
    engine: [RE2 | PCRE | ECMAScript | Oniguruma | Python re | Java regex]
  InputTrustLevel: untrusted
  Audit:
    redos_vectors_checked:
      - nested_quantifier: [none found | found at: ...]
      - overlapping_alternation: [none found | found at: ...]
      - quantified_quantifier: [none found | found at: ...]
    complexity_class: [O(n) | O(n*m) | O(n^2) | exponential]
    worst_case_pumping_string: [concrete input demonstrating upper bound]
    detection_tools_run:
      - [redos-detector version, result]
      - [safe-regex version, result]
      - [rxxr2, result]
  Mitigations:
    timeout_enforced: [yes / no — where]
    atomic_groups_used: [yes / no / n/a for engine]
    linear_time_engine_alternative: [e.g., re2 npm package, considered yes/no]
  ReviewRequested:
    - ReDoS resistance in production deployment context
    - Untrusted-input handling review
    - Regex engine feature audit (no unbounded backreferences, etc.)
  NextAgent: Builder (to apply fixes) or DONE
```

---

## Grok → Canon

Delivered when the grammar corresponds to a published standard (RFC, W3C, ISO). Canon maps compliance.

```yaml
GROK_TO_CANON_HANDOFF:
  Artifact: Grammar-to-Standards Mapping
  Grammar:
    file: [path]
    origin: [RFC / W3C / ISO / proprietary]
  Standards:
    - id: RFC 5322
      scope: [email address grammar]
      compliance: [full | subset | superset | incompatible]
      deviations: [list with rationale]
    - id: WHATWG URL
      scope: [URL parsing]
      compliance: [full | subset]
  ComplianceQuestions:
    - [question for Canon about interpretation or gap]
  NextAgent: Builder (for compliant implementation) or DONE
```

---

## Grok → Atlas

Delivered when the parser/AST layer constitutes a module boundary that needs architectural documentation (ADR).

```yaml
GROK_TO_ATLAS_HANDOFF:
  Artifact: Parser/AST Module Boundary
  ModuleName: [parser | lexer | ast | codemod]
  PublicInterface:
    entry_points: [list of exported functions/classes]
    ast_types: [list of exported AST node types]
    error_types: [list of exported error types]
  InternalDependencies:
    - [tokenizer depends on ...]
    - [parser depends on tokenizer + ast]
  ExternalDependencies:
    - [generator library if any]
    - [Unicode data if any]
  ADRTopic: [choice of engine / choice of grammar class / internal vs external DSL / roundtrip fidelity]
  Context: [2-3 paragraphs on the design forces]
  Decision: [chosen approach]
  Consequences:
    positive: [list]
    negative: [list]
    neutral: [list]
  NextAgent: Judge (review) or Builder (implement) or DONE
```

---

## Grok → Judge

Delivered when grammar design decisions warrant peer review before implementation commits.

```yaml
GROK_TO_JUDGE_HANDOFF:
  Artifact: Grammar Decision Review
  DecisionsForReview:
    - topic: [engine choice]
      alternatives_considered: [list]
      chosen: [final choice]
      rationale: [1-2 paragraphs]
    - topic: [ambiguity resolution]
      alternatives_considered: [refactor / ordered-choice / GLR]
      chosen: [final]
      rationale: [1-2 paragraphs]
    - topic: [error-recovery strategy]
      alternatives_considered: [panic / phrase-level / incremental]
      chosen: [final]
      rationale: [1-2 paragraphs]
  SupportingArtifacts:
    grammar_file: [path]
    audit_reports: [list of paths]
    test_corpus: [path]
  ReviewFocus:
    - [specific question for Judge]
    - [risk Grok is uncertain about]
  NextAgent: Builder (on approval) or revise
```

---

## Grok → Shift

Delivered when the AST transform plan spans many files and needs migration orchestration (incremental rollout, Strangler Fig, rollback plan).

```yaml
GROK_TO_SHIFT_HANDOFF:
  Artifact: Codemod / AST-Transform Migration Plan
  Scope:
    framework: [React | Vue | Angular | custom]
    from_version: [x.y]
    to_version: [x.y]
    file_count_estimate: [number]
    loc_estimate: [number]
  CodemodStrategy:
    tool: [jscodeshift | ts-morph | Babel plugin | custom]
    visitors: [list of key visitors]
    roundtrip_fidelity: [required | not-required]
    type_awareness: [required | not-required]
  MigrationPhases:
    - phase_1: [pilot — ~5 representative files]
    - phase_2: [expansion — ~50 files, verify test suite]
    - phase_3: [full run — all files]
    - phase_4: [cleanup — remove deprecated APIs]
  SafetyGates:
    - parse error handling (skip or fail)
    - test suite must pass after each phase
    - roundtrip fidelity check on random sample
    - manual review of first 10 changed files
  RollbackPlan:
    - git revert specific commits per phase
    - feature flag gate if runtime behavior changes
  RiskRegister:
    - [known edge cases where codemod is incomplete]
    - [tests that historically flake]
  NextAgent: Builder (to execute codemod) or Shift (to orchestrate)
```

---

## Nexus ↔ Grok

When invoked by Nexus in chain execution, input arrives as `_AGENT_CONTEXT` (see SKILL.md AUTORUN section). Output returns as `_STEP_COMPLETE`. Grok treats Nexus as hub and does not instruct other agent calls; it suggests next agents in the handoff.

```yaml
NEXUS_TO_GROK:
  Role: Grok
  Task: [specific task]
  Mode: AUTORUN
  Chain: [previous agents]
  Input: [handoff from previous agent]
  Constraints:
    - [runtime target]
    - [input trust level]
    - [engine preference]
    - [error-message quality target]
  Expected_Output: [grammar spec / regex audit / DSL design / AST transform plan]

GROK_TO_NEXUS:
  Agent: Grok
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [path or inline]
    artifact_type: [Grammar Spec | Regex Audit | DSL Design | AST Transform Plan]
    parameters:
      grammar_class: [value]
      engine_choice: [value]
      redos_complexity: [value]
      ambiguities_resolved: [count]
      test_corpus_size: {positive, negative, worst_case}
    files_changed: [list]
  Handoff:
    Format: GROK_TO_[NEXT]_HANDOFF
    Content: [see handoff sections above]
  Artifacts: [list]
  Risks: [list]
  Next: Builder | Radar | Sentinel | Canon | Atlas | Judge | Shift | DONE
  Reason: [why this next step]
```
