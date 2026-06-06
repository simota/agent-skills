# Grok Interaction Questions

Canonical question schemas Grok asks at INTERACTION_TRIGGERS (engine choice, generator choice, internal vs external DSL, ambiguity resolution, roundtrip fidelity).

```yaml
questions:
  - question: "Which regex engine should this pattern target?"
    header: "Engine"
    options:
      - label: "RE2 / Rust regex / Hyperscan (Recommended)"
        description: "Linear-time, ReDoS-immune. Required when input is untrusted"
      - label: "PCRE / Perl-compat"
        description: "Full feature set incl. backreferences, lookaround; ReDoS-prone"
      - label: "ECMAScript (/u or /v flag)"
        description: "Browser/Node default. ES2024 /v adds set notation; ES2025 adds RegExp.escape() and inline flag modifiers (?i:...)"
      - label: "Oniguruma (Ruby)"
        description: "Ruby / mruby environments; supports named captures, multi-byte"
      - label: "Other (please specify)"
        description: "Java, .NET, Python re, etc."
    multiSelect: false
  - question: "Which parser generator should implement this grammar?"
    header: "Generator"
    options:
      - label: "Hand-written recursive descent (Recommended for small LL(k))"
        description: "Best error messages; control over performance and diagnostics"
      - label: "tree-sitter"
        description: "Incremental parsing, error recovery; ideal for editor/IDE tooling"
      - label: "ANTLR4"
        description: "LL(*) with strong tooling; multi-language targets"
      - label: "Chevrotain (JS/TS)"
        description: "Fluent-API, no codegen, excellent error recovery"
      - label: "PEG.js / peggy / nearley"
        description: "PEG or Earley; good for rapid JS/TS prototyping"
      - label: "Other (please specify)"
        description: "Menhir, Lark, Marpa, Yacc/Bison, etc."
    multiSelect: false
  - question: "Is this DSL internal (host-language embedded) or external (standalone syntax)?"
    header: "DSL Kind"
    options:
      - label: "Internal (Recommended when users are developers)"
        description: "Fluent API, tagged template, or builder pattern in host language"
      - label: "External"
        description: "Standalone grammar with its own parser, for non-programmer authors"
      - label: "Hybrid (YAML/JSON with schema + embedded expressions)"
        description: "Data-driven config with validated extension points"
    multiSelect: false
  - question: "Grammar has ambiguity / conflicts. How to resolve?"
    header: "Ambiguity"
    options:
      - label: "Refactor to unambiguous form (Recommended)"
        description: "Rewrite rules; document precedence/associativity explicitly"
      - label: "Use ordered choice (PEG)"
        description: "Accept PEG semantics; callers must know the order matters"
      - label: "Accept GLR / Earley ambiguity"
        description: "Return all parses; downstream must disambiguate semantically"
    multiSelect: false
  - question: "Should AST transforms preserve source formatting (comments, whitespace)?"
    header: "Roundtrip"
    options:
      - label: "Preserve (Recommended for codemods)"
        description: "Use recast, jscodeshift, or ts-morph with full-fidelity nodes"
      - label: "Normalize"
        description: "Emit via printer; simpler but loses developer-authored formatting"
    multiSelect: false
```
