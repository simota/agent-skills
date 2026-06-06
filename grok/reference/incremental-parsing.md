# Incremental Parser Design Reference

Purpose: Design a parser architecture that reparses *edits*, not whole files — the foundation of responsive IDE/LSP tooling. Incremental parsing is about preserving unchanged subtrees across keystrokes, tracking dirty regions, and amortizing cost so the editor stays at 60 fps on million-line files.

## Scope Boundary

- **Grok `incremental`**: algorithmic/architectural design for re-parse-on-edit. What stays valid, what is recomputed, how state persists.
- **Grok `parser`**: one-shot parse design (grammar class, generator). Incremental is a separate axis — many `parser` choices preclude incremental (e.g. pure Earley with no reuse).
- **Grok `error`**: local error recovery that does not invalidate the whole tree — strict prerequisite for incremental. Cross-reference its error-node strategy.
- **Grok `lexer`**: incremental lexing (re-tokenize only the edited region + lookahead window) is a subordinate concern here.
- **Builder**: implements the LSP server, the editor integration, and the persistence layer based on the `incremental` spec. Does not redesign the reuse algorithm.

If the question is "how do I keep the syntax tree current while the user types?" → `incremental`. If it is "how do I wire this into VS Code?" → Builder, using the `incremental` output.

## When Incremental Is Justified

- Editor / IDE / LSP server for a language with files > 10k lines.
- Live syntax highlighting, bracket matching, semantic tokens.
- Linters / formatters / structural search that run on every keystroke.
- Notebook kernels where edits are small but frequent.

Skip incremental when: batch compile only, CLI one-shot tools, data-format parsers on whole documents. A fast non-incremental parser on a 100 KB file beats a slow incremental one.

## Core Algorithms

| Algorithm | Model | Reference implementation |
|-----------|-------|--------------------------|
| tree-sitter incremental GLR | GLR with node-reuse on unchanged byte ranges | tree-sitter `0.25.x` (Neovim / Zed / Helix / GitHub / Cursor) |
| Red-green trees | Immutable "green" nodes with position-free structure + "red" wrappers carrying parent + offset | Roslyn (C# / F# / VB) |
| Rowan (syntax tree with offsets) | Untyped green tree + typed API layer; interned text | rust-analyzer, Kotlin compiler (partial) |
| Salsa / memoization | Query-based incremental computation; reparse is one query among many | rust-analyzer, Rowan-backed languages |
| Langium AST + CST with incremental scoping | LSP-first framework, caches AST per document revision | Langium (DSL on Node/LSP) |
| Lezer (incremental LR-with-GLR-fallback) | CodeMirror 6's parser generator, stream-based parse | Lezer (CodeMirror, Dialect) |

Default for new work: **tree-sitter** for editor integration, **Rowan + salsa** for compiler-grade IDE, **Lezer** for CodeMirror-hosted editors.

### tree-sitter Snapshot (2026-05)

- Current stable line is **`0.25.x`** (v0.25.8); ABI 15 (v0.25.0) adds language name, version, and supertype metadata to parsers. `web-tree-sitter` was rewritten in TypeScript with CommonJS + ESM dual output and sourcemaps. Source: [github.com/tree-sitter/tree-sitter/releases](https://github.com/tree-sitter/tree-sitter/releases)
- `tree-sitter-language-pack` ships pre-built parsers for **~`305` languages**; prefer it over per-language `cargo install` / `npm install` of individual parsers for any new editor or LSP project.
- Empirical workloads (editor / LSP keystroke loops) report incremental reparse cutting wall-clock parse time by **~`70%`** vs full reparse on large files. Treat that as the design budget — if your incremental path does not beat full reparse by `2x`+ on a `10k`-line file, the reuse predicate is broken.
- Tree-sitter is the default backend for AI coding tools (Cursor, Zed, Helix, recent Neovim distributions) — its query language (`.scm`) doubles as a structural-search engine, not just a syntax-highlight DSL.
- Atom is no longer maintained (archived 2022); do not reference it as a tree-sitter integration target.

## Edit-Aware State Model

An incremental parser needs these pieces:

1. **Persistent tree**: the last-good parse tree, structurally shared across revisions. Nodes are immutable; edits produce a new root sharing most subtrees.
2. **Stable node identity**: either positional (rope + byte offset) or intern-based (content hash). Required for "this node survived the edit" reasoning.
3. **Edit description**: `{ start_byte, old_end_byte, new_end_byte, new_text }`. LSP-compatible.
4. **Dirty region**: bytes in the new source whose tree is stale. Expands to the minimal enclosing reparseable production.
5. **Reuse predicate**: given an old subtree and its new position, can its parse result stand? True when the byte range is unchanged AND the lookahead context is unchanged.

## Dirty-Subtree Tracking

The reparse algorithm:

1. Shift the byte offsets of all subtrees after the edit.
2. Walk from the root toward the edit location; at each node, decide: reuse wholesale, descend, or reparse.
3. The reparse region starts at the deepest ancestor whose lookahead window overlaps the edit.
4. Emit a new tree that reuses every subtree outside the reparse region.
5. Diff old vs new for downstream consumers (highlight ranges, diagnostics, semantic tokens).

Amortized cost target: **O(log n + k)** where `n` is file size and `k` is edit size. Tree-sitter and Rowan achieve this in practice; pure Earley/GLR without reuse is O(n) per keystroke — unacceptable above ~50 KB.

## LSP / IDE Integration Concerns

- **textDocument/didChange** delivers LSP `ContentChangeEvent[]`. Translate to the edit tuple above. Batch consecutive events within a debounce window (e.g. 16 ms).
- **Revision numbers**: every edit bumps a revision; cached queries key off it. Stale results must be detectable.
- **Cancellation**: a new edit arriving mid-parse must cancel the in-flight parse. Salsa's cancellation tokens, tree-sitter's `parse` with a deadline callback.
- **Semantic tokens**: emit deltas (`semanticTokens/full/delta`) from the tree diff, not a full retokenize.
- **Error recovery locality**: a syntax error in function F must not invalidate function G. This is where `error` recipe's error-node strategy is load-bearing.

## Persistence and Serialization

Optional but valuable:

- **Cross-session cache**: serialize the green tree per file hash; skip reparse on cold start if the source is unchanged. rust-analyzer uses this via salsa DB persistence.
- **Binary format discipline**: version the serialization; invalidate on grammar changes. A single bad deserialize should fall back to full parse, never crash.
- **Memory budget**: interned strings and shared subtrees keep memory reasonable; set a ceiling and evict cold files.

## Amortized Cost Analysis

Document per-operation complexity in the spec:

- **Token-level edit in a leaf**: O(log n) — walk down + reparse one production.
- **Typing at EOF**: O(k) where k is the size of the open production stack.
- **Paste N bytes**: O(N + log n) for the reparse region; still linear in paste size, not in file size.
- **Delete balanced block**: O(log n) — the enclosing production is the reparse region.
- **Delete unbalanced opening brace**: O(n) worst-case — the whole tail reparses. Unavoidable; mitigate with error recovery.

Call out the worst cases explicitly; Builder needs them for capacity planning.

## Anti-Patterns

- Claiming incremental while reparsing from scratch under the hood (common in "incremental" parser-combinator libraries).
- Mutable trees with parent pointers — defeats structural sharing, makes cancellation unsafe.
- Coupling the AST to the parser's internal state, so reuse requires re-running actions. Keep the tree a pure data structure.
- Reparse triggered on every keystroke without debouncing — wastes CPU and fights the GC.
- Unrecoverable errors that poison the tree for the rest of the session — design `error` first.
- Ignoring the lexer: incremental parse on a non-incremental lexer reparses the whole token stream. Pair with incremental tokenization (tree-sitter bundles this; most others need explicit design).

## Handoff to Builder

Deliver:
- Algorithm choice (tree-sitter / Rowan+salsa / Lezer / red-green / bespoke) with reason.
- Tree-node data model: green-node schema, stable-ID scheme, trivia handling.
- Edit-application algorithm in pseudocode.
- Reuse predicate with examples of reused vs reparsed edits.
- LSP event mapping: which LSP messages drive which cache invalidations.
- Cancellation protocol.
- Persistence format (if any): versioning, fallback path.
- Amortized cost table per edit shape.
- Test corpus: ≥ 10 edit sequences covering reuse, error-recovery locality, paste, undo/redo, format-on-save.

Builder receives this spec and implements the LSP server, editor integration, and persistence without re-deciding the incremental algorithm.
