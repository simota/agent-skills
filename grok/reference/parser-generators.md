# Parser Generator Selection

**Purpose:** Decision framework for picking a parser generator (or hand-written recursive descent) for a new grammar.
**Read when:** Designing a parser for a DSL, config file, query language, or programming language; reviewing an existing parser; selecting tooling for a new project.

## Contents
- Decision matrix
- Grammar classification
- Per-tool profiles
- Choice flowchart
- When to avoid parser generators
- Error-recovery strategies
- Tokenizer design notes

---

## Decision Matrix

| Tool | Grammar class | Target runtimes | Error messages | Incremental | Ambiguity | Learning curve |
|------|---------------|-----------------|----------------|-------------|-----------|----------------|
| Hand-written RD | LL(k) | any | ★★★★★ | N/A | Resolved in code | Low (if LL(k)) |
| tree-sitter | LR(1)+recovery | C core, bindings everywhere | ★★★★ (error nodes) | Yes | No | Medium |
| ANTLR4 | LL(*) | JVM, JS, Python, Go, C#, C++, Dart, PHP, Swift | ★★★★ | No | Predicated | Medium-high |
| Chevrotain | LL(k) | JS/TS | ★★★★★ (built-in recovery) | Partial | No | Low |
| PEG.js / peggy | PEG | JS/TS | ★★★ | No | Ordered choice | Low |
| nearley | Earley | JS | ★★★ | No | Yes (all parses) | Medium |
| Menhir | LR(1) | OCaml | ★★★★★ | No | Resolved in grammar | Medium |
| Lark | Earley / LALR / CYK | Python | ★★★★ | No | Yes (Earley) | Low-medium |
| Marpa | Earley | C, Perl | ★★★ | No | Yes (all CFG) | High |
| Yacc / Bison | LALR(1) | C (Bison: C++, Java, D) | ★★ | No | Resolved via precedence | Medium |
| ts-parsec / parsimmon | PEG / combinator | TS / JS | ★★★ | No | Ordered | Low |
| Parsec (Haskell) | PEG-like combinator | Haskell | ★★★★ | No | Ordered | Medium |
| pest (Rust) | PEG | Rust | ★★★ | No | Ordered | Low |
| Coco/R | LL(k) | C#, Java, C++ | ★★★ | No | No | Medium |

**Scoring note:** Error-message quality is subjective; ★★★★★ reserved for tools that produce Elm/Rust-tier diagnostics with source spans and actionable suggestions out of the box.

### 2026 State of the Tooling

- **tree-sitter** is on the **`0.26.x`** line (v0.26.9 current as of 2026-05-19). ABI 15 (introduced in v0.25.0) adds language name, version, and supertype metadata to parsers. `web-tree-sitter` was rewritten in TypeScript with CommonJS + ESM dual output and sourcemaps. `tree-sitter-language-pack` ships pre-compiled parsers for ~`305` languages, removing per-binding compilation toil. Default to it for any editor / LSP target. Source: [github.com/tree-sitter/tree-sitter/releases](https://github.com/tree-sitter/tree-sitter/releases)
- **ANTLR4** remains the de facto choice for cross-runtime grammar reuse (4.13+ relocates the Go runtime to [github.com/antlr4-go/antlr](https://github.com/antlr4-go/antlr)); Python target continues to receive parity improvements. Source: [github.com/antlr/antlr4/releases](https://github.com/antlr/antlr4/releases)
- **Chevrotain** is the canonical JS / TS choice when you need a hand-tunable LL(k) parser without leaving Node — its error-recovery primitives still set the bar in the JS ecosystem.
- **Lezer** (CodeMirror 6's parser generator) is the right answer when the editor itself is CodeMirror; pair with tree-sitter only when CodeMirror is not a constraint.
- **Rust ecosystem**: `lalrpop` 0.23.x (LR(1), v0.23.1 2026-03-11) and `pest` (PEG, v2.8.6 2026-02-05) are both actively maintained as of 2026-05. Source: [crates.io/keywords/grammar](https://crates.io/keywords/grammar)
- **Marpa** and **nearley** stay useful for ambiguous grammars (linguistic, partial / streaming, exploratory) — Lark + Earley covers the same ground in Python.

---

## Grammar Classification

Pick an engine that matches (or exceeds) the class of your grammar. Going above wastes capability; going below produces an unparseable grammar.

### Regular (Chomsky Type 3)

Can be recognized by a finite automaton. Use a regex, not a parser generator.

Examples: URL path fragments, simple tokens, log line prefixes.

### Context-free (Type 2)

Productions of the form `A → β` where `A` is a non-terminal and `β` is any string of terminals and non-terminals. Most programming languages are CFG.

Sub-classes by parser class:

- **LL(1)**: predictable with one token lookahead. Hand-written RD and most generators handle this easily. Json is LL(1) modulo number parsing.
- **LL(k)**: k-token lookahead. ANTLR4's LL(*) goes arbitrarily far. Chevrotain, hand-written RD.
- **LR(0) / SLR / LALR(1) / LR(1)**: bottom-up. Yacc/Bison are LALR(1); Menhir is LR(1). Most stricter than LL, can handle left recursion naturally.
- **GLR**: generalized LR; handles ambiguous CFGs. Bison has GLR mode; tree-sitter uses a variant.
- **PEG**: parsing expression grammars — looks like CFG but with ordered choice `/`, making every PEG unambiguous. Not all CFGs are PEG-expressible; not all PEGs are CFGs.
- **Earley**: recognizes any CFG including ambiguous and left-recursive. Slower (O(n³) worst case, O(n²) unambiguous, O(n) for LR-like grammars). Used by nearley, Lark, Marpa.

### Context-sensitive / unrestricted

Real programming languages often have context-sensitive features (e.g., C's `typedef` name resolution, Python's indentation). Handle with:
- Lexer hacks (feed type info back to lexer).
- Two-pass parsing (parse skeleton, resolve names, re-parse if needed).
- Post-parse semantic analysis.

### Left recursion

- **LL parsers** (RD, ANTLR4 in older versions, Chevrotain): left recursion causes infinite loop; must rewrite as right-recursive plus iteration. ANTLR4 4.x handles direct left recursion via rewriting.
- **LR parsers** (Yacc, Menhir, tree-sitter): left recursion is natural and preferred (avoids right-recursive stack depth).
- **PEG**: most PEG engines disallow left recursion; some (pegjs, peggy) support it experimentally via the packrat seed-parsing technique.

---

## Per-Tool Profiles

### Hand-written recursive descent

**When to pick:**
- Grammar is LL(k) with small k.
- You need the best error messages possible (Clang, rustc, Elm-tier).
- You want full control over performance, memory layout, incremental parsing.
- Production compilers and production query engines.

**Examples:** Clang, rustc, Go's go/parser, TypeScript's compiler, V8's parser, the Swift parser.

**Trade-offs:** most effort upfront; cannot mechanically verify LL(k) property (you rely on discipline). Pays off for long-lived projects; overkill for one-off config parsers.

**Pattern:**

```typescript
class Parser {
  peek(): Token;
  consume(kind: TokenKind): Token;
  parseExpression(): Expr {
    const left = this.parsePrimary();
    while (this.peek().isBinaryOp()) {
      const op = this.consume(TokenKind.Op);
      const right = this.parsePrimary();
      return new BinaryExpr(left, op, right);
    }
    return left;
  }
}
```

### tree-sitter

**When to pick:**
- Editor / IDE tooling (syntax highlighting, folding, selection expansion, structural search).
- Need incremental re-parse (user edits a file; only damaged region re-parses).
- Need robust error recovery (edited buffers are syntactically invalid most of the time).
- You want a query language for AST pattern matching.

**Examples:** Neovim, Helix, Zed, Atom (historical), GitHub's code search, Sourcegraph.

**Trade-offs:** C runtime; bindings exist for everything. Grammar DSL has a learning curve — productions, precedence, conflicts are stated explicitly. Generated parser is fast and memory-efficient.

**Grammar snippet:**

```javascript
module.exports = grammar({
  name: 'mylang',
  rules: {
    source_file: $ => repeat($._statement),
    _statement: $ => choice($.assignment, $.expression_statement),
    assignment: $ => seq($.identifier, '=', $._expression, ';'),
    _expression: $ => choice($.number, $.identifier, $.binary_expression),
    binary_expression: $ => prec.left(1, seq($._expression, choice('+', '-'), $._expression)),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,
    number: $ => /\d+/,
  }
});
```

### ANTLR4

**When to pick:**
- You need targets beyond JS (JVM, Python, Go, C#, C++).
- Visual grammar tooling (ANTLR IDE plugins) is valuable.
- LL(*) expressiveness handles your grammar without contortions.
- Generated tree walker (visitor / listener) is enough for your semantic analysis.

**Examples:** Twitter Storm, Groovy, Apex (Salesforce), many query languages.

**Trade-offs:** generated parser is larger and slower than hand-written. Error messages are OK but not Elm-tier without custom work. Predicate grammars exist but make the grammar harder to maintain.

### Chevrotain

**When to pick:**
- Project is JS/TS.
- You want a parser generator without a code-gen step.
- Built-in error recovery matters.
- Near-hand-written performance on the V8 engine.

**Trade-offs:** fluent API is JS-specific; grammar lives in code, not a separate .g4 file. No multi-language targets.

**Pattern:**

```typescript
import { CstParser } from 'chevrotain';

class ExprParser extends CstParser {
  expression = this.RULE('expression', () => {
    this.SUBRULE(this.term);
    this.MANY(() => {
      this.CONSUME(Plus);
      this.SUBRULE2(this.term);
    });
  });
  term = this.RULE('term', () => this.CONSUME(NumberLiteral));
}
```

### PEG.js / peggy / nearley

**When to pick:**
- Rapid prototyping.
- Grammar is naturally expressible in PEG (ordered choice, no ambiguity tolerance needed).
- Target is JS/TS.
- nearley specifically: when you need Earley (ambiguous CFG).

**Trade-offs:** PEG ordered-choice hazards are real — a longer alternative must come before a shorter prefix, or matches will silently shadow. Error messages are generic by default.

### Parsec-style (ts-parsec, parsimmon, pest)

**When to pick:**
- You like functional composition.
- Grammar is small to medium.
- Type-safety of combinators (TypeScript / Haskell / Rust) is valued.

**Pattern (ts-parsec):**

```typescript
import { apply, seq, tok, rep_sc } from 'typescript-parsec';

const NUMBER = apply(tok(TokenKind.Number), (t) => parseInt(t.text));
const PLUS = tok(TokenKind.Plus);
const EXPR = apply(seq(NUMBER, rep_sc(seq(PLUS, NUMBER))), ([head, tail]) =>
  tail.reduce((acc, [, n]) => acc + n, head));
```

### Menhir (OCaml)

**When to pick:**
- OCaml project.
- You need LR(1) with excellent conflict diagnostics (Menhir's `--explain` is a model).
- ML-family language design.

**Examples:** OCaml compiler itself, Coq, F*.

### Lark (Python)

**When to pick:**
- Python ecosystem.
- Grammar requires Earley (ambiguous or left-recursive in PEG-unfriendly way).
- Teaching / prototyping.

### Marpa

**When to pick:**
- You truly need to parse any CFG (natural language analysis, academic projects).
- Performance is less important than expressiveness.

### Yacc / Bison

**When to pick:**
- Legacy C codebase already uses it.
- Interop with existing Yacc grammars.

**Avoid for new projects**: error messages are poor, LALR conflicts are opaque, and Menhir / tree-sitter / hand-written RD are strictly better for most use cases.

---

## Choice Flowchart

```
Start: what are you parsing?
├─ Untrusted network input? ──Yes──▶ Prefer linear-time regex + hardened parser
│                                    Prefer hand-written RD or tree-sitter
│
├─ Editor / IDE tooling? ─────Yes──▶ tree-sitter (incremental + recovery built-in)
│
├─ Need multi-language target? ──Yes──▶ ANTLR4
│
├─ Best error messages matter most? ──Yes──▶ Hand-written RD
│
├─ Grammar is ambiguous (natural language, etc.)? ──Yes──▶ Earley: nearley / Lark / Marpa
│
├─ Rapid prototype in JS/TS? ──Yes──▶ peggy or Chevrotain
│
├─ Rust project? ──Yes──▶ pest (PEG) or lalrpop (LR(1)) or hand-written
│
├─ OCaml project? ──Yes──▶ Menhir
│
├─ Python project, mid-complexity? ──Yes──▶ Lark
│
└─ Small, LL(1), full control? ─────▶ Hand-written RD
```

---

## When to Avoid Parser Generators

Hand-written is strictly better when:

1. **Grammar is simple and LL(1).** Writing a few recursive functions is less code than learning a generator.
2. **You need maximum error-message quality.** No generator matches a hand-crafted parser's ability to emit "expected expression after `return`, found `}`" with a fix-it suggestion.
3. **You need custom AST node pooling, arena allocation, or specific memory layout.**
4. **Grammar is context-sensitive enough that you need lexer-parser feedback loops.**
5. **Incremental parsing with custom granularity.** (tree-sitter is an alternative here.)
6. **Binary formats.** Use a dedicated binary parser library (e.g., `nom` in Rust) or hand-written byte reader; regex/parser generators are for text.

---

## Error-Recovery Strategies

### Panic mode

On error, skip tokens until a synchronizing terminal (`;`, `}`, newline). Simple, loses context. Acceptable for compile-once workflows.

### Phrase-level recovery

Insert, delete, or replace a single token to continue parsing. Chevrotain implements this automatically; tree-sitter uses error nodes.

### Error productions

Add explicit grammar rules that match common mistakes:

```
statement
  : expression ';'
  | expression                     { emit("missing semicolon") }
  | expression ';;'                { emit("extra semicolon") }
```

Quality depends on how well you enumerate mistakes. Effective for high-traffic syntax (e.g., JavaScript's `class` syntax historically).

### Incremental re-parse

tree-sitter's approach: diff the edit range; re-parse only the damaged subtree; preserve the rest. Required for editor responsiveness on large files.

### Diagnostic quality benchmarks

| Style | Example |
|-------|---------|
| Elm | "I found an error in this expression: ... I was expecting to see a record field. Did you mean `name` or `age`?" |
| rustc | `error: expected expression, found '}'\n --> src/main.rs:3:5\n  | let x = ;\n  |         ^ expected expression` |
| Clang | Multi-line caret, fix-it hints, template backtrace trimming |

---

## Tokenizer Design Notes

### Lexer modes

Different contexts produce different tokens. Examples:
- String interpolation: `` `hello ${name}` `` — lexer switches into expression mode inside `${...}`.
- HTML: attribute mode vs content mode.
- Shell: command mode vs parameter expansion mode.

Tools with native mode support: ANTLR4 (`mode NAME;`), Chevrotain (`Lexer.SKIPPED`), tree-sitter (external scanners). Hand-written lexers handle modes with a stack.

### Context-sensitive tokens

C's `typedef` trick: the lexer needs a symbol table to know whether `foo` is a type or an identifier. Solutions:
- Pass symbol table to lexer (tight coupling).
- Always lex as identifier; disambiguate in parser (cleaner).
- Use a GLR / Earley parser to keep ambiguity alive.

### Indentation-based (Python, Haskell, YAML)

Emit synthetic `INDENT` and `DEDENT` tokens. The lexer maintains an indentation stack; each newline followed by leading whitespace compares against the top.

Tools:
- Python's own `tokenize` module.
- ANTLR4 has a community `DenterHelper`.
- tree-sitter: external C scanner.

### Whitespace and comments

- Skip: most languages.
- Preserve as trivia: needed for roundtrip-safe transforms (see `ast-transforms.md`).
- Significant: Haskell layout, Python indentation, Ruby's newline-as-terminator.

---

## Checklist: Ship-Ready Parser Design

- [ ] Grammar class classified (regular / LL / LR / PEG / Earley / unrestricted)
- [ ] Engine chosen with decision-matrix justification
- [ ] Ambiguities resolved (grammar refactor, precedence declaration, or accepted as Earley multi-parse)
- [ ] Left recursion handled (LR engine or rewritten for LL)
- [ ] Lexer modes / context-sensitivity documented
- [ ] Error-recovery strategy documented
- [ ] Sample diagnostic for three most common errors
- [ ] Incremental parsing decision (yes / no)
- [ ] Roundtrip fidelity decision (preserve trivia / normalize)
- [ ] Test corpus ≥3 positive / ≥3 negative per production
- [ ] Performance budget stated (tokens/sec or µs/call)
