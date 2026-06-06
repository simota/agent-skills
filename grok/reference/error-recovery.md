# Parser Error Recovery and Diagnostics Design Reference

Purpose: Design the parser's error-recovery strategy and the shape of its diagnostic messages. This is a language-theoretic artifact — which tokens are synchronizing, which productions catch common mistakes, what a good error message for *this* grammar looks like. It is not the code that implements it.

## Scope Boundary

- **Grok `error`**: recovery strategy + diagnostic template design (what to show, when to resync, how to point at source).
- **Grok `parser`**: grammar-class + generator choice (recovery strategy is a factor but not the focus).
- **Grok `lexer`**: token-level error states (invalid byte, unterminated string) — cross-reference, not duplicate.
- **Builder**: implements the recovery + diagnostic code the `error` spec describes. Does not redesign the strategy.

If the question is "what should happen when the parser sees an unexpected token?" → `error`. If it is "how do I wire rustc-style spans into my parser code?" → Builder, using the `error` output as input.

## Recovery Strategies

| Strategy | Model | Strength | Weakness | Canonical reference |
|----------|-------|----------|----------|---------------------|
| Panic-mode | Skip tokens until a synchronizing terminal (`;`, `}`, EOL) | Trivial to implement; works everywhere | Loses context; cascades errors | Dragon Book §4.1.4 |
| Phrase-level | Insert / delete / replace one token to continue | Good single-error UX | Can mask real error; needs cost model | Chevrotain, tree-sitter |
| Error productions | Explicit grammar rules that match common mistakes | Best-quality diagnostics for known mistakes | Must be authored per mistake | ANTLR4, lalrpop `!` |
| Error nodes (damaged-region) | Wrap malformed subtree as an error node; keep the rest of the CST valid | Enables continuous parsing / IDE | Requires CST design + incremental model | tree-sitter, Roslyn |
| Parse-all (GLR / Earley) | Return all parses; caller disambiguates | No recovery needed — ambiguity is the output | Downstream must resolve; cost | nearley, Marpa, tree-sitter GLR |

Most production parsers combine strategies: panic-mode as fallback, error productions for the top N known mistakes, phrase-level for expected-token recovery, error nodes for IDE continuity.

## Choosing a Strategy

- **Compiler (batch)**: panic-mode + error productions for the 5-10 most common mistakes. Target: one message per real error, no cascade.
- **IDE / LSP**: error nodes + incremental reparse (coordinate with `incremental` recipe). Target: the rest of the file keeps highlighting and diagnostics.
- **Interpreter / REPL**: phrase-level recovery + "expected X" template. Target: clear single-line message.
- **Data-format parser (JSON, config)**: panic-mode to the next structural delimiter. Target: report line/col + expected token set.

## Diagnostic Message Anatomy

A modern diagnostic (Rust/Clang style) has six layers:

1. **Severity**: error / warning / note / help.
2. **Code**: stable identifier (`E0308`, `grammar/UNEXPECTED_TOKEN`). Enables docs and suppression.
3. **Primary span**: byte range → line/col pair (1-based for users, 0-based for tools).
4. **Primary label**: short description at the span ("expected `)`, found `,`").
5. **Secondary spans**: related locations ("unclosed `(` here" at the opening paren).
6. **Help / suggestion**: optional applicable fix ("try inserting `)` before `,`").

Elm-style adds a conversational framing ("I am partway through parsing an expression..."), a concrete example, and a "did you mean" based on edit distance.

## Source-Span Tracking

Every token and AST node carries a span. Span design choices:

- **Byte offsets**: compact (u32 per end), requires a `SourceMap` to resolve to line/col. Used by rustc, roslyn, swc.
- **Line + column**: human-friendly, harder to diff with byte edits. Used by some JS parsers.
- **File ID + byte range**: multi-file / multi-input parsers (macros, includes). rustc's `Span` is `(FileId, lo, hi, SyntaxContext)`.

Multi-span diagnostics require the span to survive AST transformations — coordinate with `ast` recipe's trivia policy. If the AST drops trivia, the span must still point at the original source.

## Expected-Token Reporting

Naive "expected X, got Y" is insufficient. Upgrades:

- **Expected set**: compute FIRST of the next production and show all valid tokens ("expected one of `,`, `)`, `=>`").
- **Context anchor**: name the rule in progress ("while parsing a function parameter list").
- **Did-you-mean**: edit distance on keywords / identifiers (Elm, rustc).
- **Structured fix**: machine-applicable suggestion an IDE can offer as a quick fix (rustc `Applicability::MachineApplicable`).

## Error Productions Catalog

For each grammar, design the top 5-10 error productions. Example for a C-like language:

- Missing `;` after statement → insert, single error.
- `=` used instead of `==` in condition → error production + hint.
- Unclosed string literal to end-of-line → lexer-level, specialized message.
- Unmatched `}` → error node, do not cascade.
- `if cond {` without parens (when grammar requires them) → suggest parens.

Error productions are the cheapest way to get rustc-tier diagnostics for known mistakes.

## Anti-Patterns

- Cascading errors (one real mistake → 20 reported errors). Symptom: panic-mode without a synchronizing token. Fix: widen the sync set or add error productions.
- Token-level messages without rule context ("unexpected `,`"). Fix: include the in-progress rule name.
- Byte offsets shown to users. Fix: resolve to line/col at the presentation layer.
- Silent recovery (parser continues, no diagnostic emitted). Every recovery must emit at least one diagnostic.
- Hard-coding messages in the parser code instead of a message catalog — blocks i18n and makes code review of wording impossible. Use a catalog keyed by diagnostic code.

## Generator-Specific Notes

- **chumsky**: `recover_with` combinators (`nested_delimiters`, `skip_until`) compose per-rule; the design lives in the grammar.
- **lalrpop**: `!` marker in productions inserts error tokens; recovery is LR-automaton-driven.
- **ANTLR4**: default `DefaultErrorStrategy` (single-token insertion/deletion) plus `BailErrorStrategy` for fail-fast.
- **tree-sitter**: error nodes are automatic from the GLR-style algorithm; the designer picks which rules tolerate error children.
- **Hand-written RD**: most design freedom; highest authoring cost. Prefer when diagnostic quality is the product (rustc, Elm, Clang).

## Handoff to Builder

Deliver:
- Strategy selection (panic / phrase / error-prod / error-node / GLR) with reason per rule class.
- Synchronizing-token set per recovery region.
- Error-production list with grammar fragments and target message.
- Message catalog: code → severity → template → variables → suggested fix.
- Span-tracking decision: byte vs line/col, single-file vs multi-file, trivia preservation.
- Sample rendered diagnostics for the three most likely parse errors in the target language.
- Test corpus: ≥ 5 malformed inputs per error production, asserting the expected diagnostic code and span.

Builder implements the parser's error paths against this spec; it does not re-decide recovery strategy or message wording.
