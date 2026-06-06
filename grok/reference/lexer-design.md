# Lexer / Tokenizer Design Reference

Purpose: Design a standalone tokenization stage. The lexer consumes a byte/character stream and emits a token stream for the parser. Many small DSLs correctly skip a separate lexer — this reference is for when the separation earns its keep.

## Scope Boundary

- **Grok `lexer`**: whether to extract tokenization as a distinct stage, and how to structure it (modes, context-sensitivity, trivia, lookahead).
- **Grok `parser`**: grammar class + parser generator for the full syntactic layer (LL/LR/PEG/GLR, ANTLR vs tree-sitter vs hand-written RD, etc.).
- **Grok `error`**: recovery strategy; lexer-level recovery (invalid-byte token, unterminated string) is scoped here but diagnostic templating is `error`.

If the question is "do I need a separate tokenizer at all?" → `lexer`. If it is "which parser generator for this grammar?" → `parser`. Scannerless designs (PEG with literal strings, chumsky on `char`) skip this recipe by construction.

## When a Separate Lexer Earns Its Keep

Choose a separate lexer when at least one applies:

- **Performance**: hot-path parsing on large inputs (log lines, source files ≥ MB). DFA-compiled lexers (re2c, logos, flex) outperform scannerless grammars by 5-20x.
- **IDE reuse**: the token stream is consumed independently by syntax highlighting, semantic tokens (LSP), and bracket matching. Tree-sitter's `highlights.scm` operates at the token layer.
- **Context-sensitive tokens**: `>>` in C++ (shift vs two closes in templates), here-docs in shell, regex literals in JavaScript (division vs regex), JSX text mode.
- **Indentation-sensitive syntax**: Python, Haskell, YAML, F# — the lexer emits synthetic `INDENT` / `DEDENT` / `NEWLINE` tokens from layout.
- **Trivia discipline**: comments and whitespace must be attached to tokens (CST for roundtrip-safe transforms), not silently dropped.

Skip a separate lexer when: the grammar is small (< 20 productions), the input is trusted and small, or a parser combinator library handles characters directly and that is fast enough.

## Hand-Written vs Generator

| Approach | Pick when | Skip when |
|----------|-----------|-----------|
| Hand-written (switch on char / peekable iterator) | Best diagnostics, tricky context-sensitivity, small token set (< 30) | Token set large and regular — generator wins |
| `logos` (Rust, derive macro → DFA) | Rust, need speed + ergonomics, regex-describable tokens | Heavy context-sensitivity needs callbacks anyway |
| `re2c` (C/C++/Go/Rust codegen) | Maximum throughput, greenfield C-family project | No re2c expertise on team |
| `flex` / `lex` | Legacy C toolchain, Bison integration | Modern project — prefer re2c or logos |
| ANTLR4 lexer | Already using ANTLR parser, multi-target codegen | Standalone lexer needs — ANTLR is heavier |
| tree-sitter built-in scanner + external scanner (C) | Editor tooling, context-sensitive tokens (heredocs, indent) | Non-editor use — prefer logos/re2c |
| `chumsky` token phase | Rust parser-combinator project wanting explicit tokenization | Fully scannerless is fine for the grammar |

Default for new projects: **hand-written for < 30 tokens + tricky rules, `logos`/re2c for regular token sets with throughput pressure, tree-sitter external scanner when the target is an editor**.

## Context-Sensitivity Patterns

- **Lexer modes / states** (flex `%x`, ANTLR `mode`, tree-sitter external scanner state): switch the active token set based on context. Canonical uses: string interpolation `"hello ${name}"`, template literals, comment nesting, heredoc body.
- **Keyword-as-identifier fallback**: context-sensitive keywords (Kotlin `field`, SQL `on`) — lex as identifier, let the parser promote.
- **Regex-vs-division in JavaScript**: the lexer cannot decide alone; uses the previous token class as a hint (e.g. after `)` → division, after `=` → regex).
- **Off-side rule (indentation)**: maintain an indentation stack; emit synthetic `INDENT` when column increases, `DEDENT` (possibly multiple) when it decreases. Python reference: `tokenize` module. Haskell uses a richer algorithm (layout rule + explicit braces).

## Lookahead Budget

Declare the maximum lookahead per token decision up front:
- **LL(1) lexer**: single-char peek (most hand-written scanners).
- **LL(k)**: `k` chars — e.g. `..` vs `..=` vs `...` needs 2-3.
- **Unbounded backtracking** (PEG-style): avoid in hot paths; acceptable only when the token set forces it (e.g. numeric literal prefixes `0x`, `0b`, `0o`).

Document the budget alongside the token table — it drives engine choice.

## Trivia and Whitespace Strategy

Three defensible policies. Pick one and stick with it:

1. **Skip silently** (yacc/bison default): trivia is consumed by the lexer, parser never sees it. Lossy — cannot roundtrip.
2. **Attach to next token** (Roslyn, rust-analyzer, Prettier): each token carries leading + trailing trivia. CST-friendly, enables roundtrip transforms.
3. **Emit as tokens** (tree-sitter, Prettier's handling of meaningful whitespace): trivia is a first-class token kind the parser may ignore or consume.

Policy choice propagates into the AST/CST design — coordinate with `ast` recipe and the transform's roundtrip requirements.

## Anti-Patterns

- Hand-rolling a tokenizer for a grammar the parser combinator can already handle character-by-character — wasted complexity.
- Using flex in 2026 for new C projects — prefer re2c or logos.
- Dropping comments silently when downstream needs codemods (breaks roundtrip).
- Implementing indentation by trying to "fix up" tokens in the parser — always do it in the lexer with a dedicated indentation stack.
- Letting context-sensitive keywords bleed into the grammar as ordered-choice hacks — push the disambiguation down to lexer modes or up to post-parse resolution, not scattered between them.

## Handoff to Builder

Deliver:
- Token table: name, pattern (regex or literal), examples, precedence / longest-match tiebreak.
- Lexer mode diagram if context-sensitive.
- Indentation rule in pseudocode if off-side applies.
- Lookahead budget per token class.
- Trivia policy decision (skip / attach / emit).
- Chosen tool (hand-written / logos / re2c / tree-sitter external scanner) and reason.
- Error-token design (unterminated string, invalid byte) — links to `error` recipe output.
- Test corpus: ≥ 3 positive and ≥ 3 negative examples per non-trivial token, plus worst-case inputs for throughput-sensitive targets.

Builder receives this spec and implements the scanner + unit tests without re-deciding the tokenization architecture.
