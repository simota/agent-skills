# AST Design & Transformation

**Purpose:** Patterns for designing AST nodes, choosing a transform framework, and executing code modifications safely.
**Read when:** Designing AST node types, writing a codemod, migrating a framework (React class → hooks, Vue 2 → 3, Angular versions), or auditing existing AST-based tooling.

## Contents
- AST design fundamentals
- Immutable vs mutable trees
- Visitor pattern implementations
- AST diff / patch tools
- Codemod patterns
- Source-map preservation
- Roundtrip-safe transforms
- Anti-patterns

---

## AST Design Fundamentals

### Tagged union nodes

Each node has a discriminator field identifying its kind. Downstream code switches on the discriminator for exhaustive handling.

```typescript
type Node =
  | { kind: 'NumberLiteral'; value: number; pos: Position }
  | { kind: 'Identifier'; name: string; pos: Position }
  | { kind: 'BinaryExpr'; op: '+' | '-' | '*' | '/'; left: Node; right: Node; pos: Position }
  | { kind: 'CallExpr'; callee: Node; args: Node[]; pos: Position };
```

TypeScript's discriminated-union type-narrowing makes exhaustive switches compile-checked. In Rust, use `enum`. In Java, sealed classes (Java 17+) or the visitor pattern.

### Position tracking

Every node carries the source position range it originated from:

```typescript
interface Position {
  start: { line: number; column: number; offset: number };
  end: { line: number; column: number; offset: number };
}
```

Needed for:
- Error messages with source-span pointers.
- Source maps (preserving original position through transformations).
- IDE go-to-definition, diagnostics, refactoring.

### Parent pointers

Useful for upward queries (find enclosing function, enclosing class). Two options:

- **Computed on demand**: walk the tree each time; simpler but O(n).
- **Stored in node**: mutation requires keeping pointer consistent; tools like Babel set parent lazily during traversal.

### Trivia (comments, whitespace)

For roundtrip-safe transforms, attach comments and whitespace to nodes:

```typescript
interface Node {
  leadingTrivia: string;
  trailingTrivia: string;
  // ...
}
```

TypeScript compiler uses this; `recast` rebuilds it on top of Babel's AST.

### Immutable-friendly design

Use structural sharing: a transform returns a new node referencing unchanged children:

```typescript
const newExpr: BinaryExpr = { ...oldExpr, right: newRight };
// left is shared; only right is new
```

---

## Immutable vs Mutable Trees

### Mutable (Babel default)

```javascript
path.node.name = 'newName';  // mutates in place
```

**Pros:** straightforward, efficient for large-scale mutation.
**Cons:** history is lost; concurrent traversal is unsafe; undo requires checkpointing.

### Immutable with path-based updates

Immer / Ramda lenses produce a new tree per mutation, with structural sharing:

```typescript
import { produce } from 'immer';
const newTree = produce(tree, (draft) => {
  draft.body[0].name = 'newName';
});
```

**Pros:** time-travel debugging, undo-redo, safe concurrent reads.
**Cons:** every write allocates; larger memory footprint.

### Choice heuristic

- One-shot codemod over a codebase: mutable is fine.
- Long-lived editor buffer: immutable with structural sharing.
- IDE refactoring with undo: immutable.
- Build-time transform (Babel, SWC): mutable for performance.

---

## Visitor Pattern Implementations

### ESLint rules

Enter/exit callbacks per node type; traversal order is depth-first.

```javascript
module.exports = {
  create(context) {
    return {
      Identifier(node) {
        if (node.name === 'bad') {
          context.report({ node, message: 'Avoid name "bad"' });
        }
      },
      'CallExpression:exit'(node) { /* ... */ }
    };
  }
};
```

### Babel plugin

Visitor object with entry per node type; `path` provides mutation and traversal methods.

```javascript
module.exports = function ({ types: t }) {
  return {
    visitor: {
      Identifier(path) {
        if (path.node.name === 'old') {
          path.node.name = 'new';
        }
      },
      CallExpression(path) {
        if (t.isIdentifier(path.node.callee, { name: 'oldFn' })) {
          path.node.callee = t.identifier('newFn');
        }
      }
    }
  };
};
```

### jscodeshift

Collection-based query API; chainable like jQuery for ASTs.

```javascript
module.exports = function (file, api) {
  const j = api.jscodeshift;
  return j(file.source)
    .find(j.Identifier, { name: 'old' })
    .replaceWith(() => j.identifier('new'))
    .toSource();
};
```

Good for large codemods; used by React team for class-to-function component migrations.

### ts-morph (TypeScript)

Project / SourceFile / Node API with direct manipulation and built-in type-aware refactorings.

```typescript
import { Project } from 'ts-morph';

const project = new Project();
project.addSourceFilesAtPaths('src/**/*.ts');
for (const sourceFile of project.getSourceFiles()) {
  sourceFile.getClasses().forEach(cls => {
    if (cls.getName() === 'Old') cls.rename('New');
  });
}
project.saveSync();
```

ts-morph carries full TypeScript semantic info — rename propagates across files.

### tree-sitter query

Scheme-like pattern matching against the parse tree:

```scheme
(call_expression
  function: (identifier) @fn
  arguments: (arguments (string) @arg))
```

Queries return captures. Useful for linters, structural search, refactoring tools in editors.

### JetBrains MPS

Projectional editor: the "source" IS the AST; there is no text form. Transforms are structural edits. Used for industrial DSLs (mbeddr C, for example).

---

## AST Diff / Patch Tools

### Tree-edit distance (Zhang-Shasha)

Classical algorithm for comparing ordered labeled trees; returns minimum insert/delete/rename edit sequence.

### GumTree

Modern tool-backed tree differ: `https://github.com/GumTreeDiff/gumtree`. Produces semantically meaningful diffs (move detection, not just insert-delete).

Use cases:
- Intelligent code review (show moved functions as moves, not delete+insert).
- Conflict resolution in merges.
- Refactoring recognition in empirical software engineering research.

### Patch application

Once diff is computed, applying it to a working tree: insert / delete / update / move operations at tree positions. Persistent data structures (Immer-style) are natural here.

---

## Codemod Patterns

### Rename

```javascript
// jscodeshift
root.find(j.Identifier, { name: 'oldName' })
  .replaceWith(j.identifier('newName'));
```

Caveats: `oldName` might be a method name, variable, type parameter. Use type information (ts-morph) to rename only the specific binding.

### Extract

Replace inline expression with a variable:

```javascript
// Before
foo(complicated(expression, here));

// After
const result = complicated(expression, here);
foo(result);
```

Requires scope analysis: where is `result` visible? Does it shadow existing bindings?

### Inline

Opposite of extract. Replace variable references with their definition. Requires:
- Definition is used only once (or is pure and idempotent).
- No side effects in the definition.

### Framework migration

**React class → hooks** (facebook/jscodeshift-codemods):

```jsx
// Before
class Counter extends React.Component {
  state = { count: 0 };
  render() { return <button onClick={() => this.setState({ count: this.state.count + 1 })}>{this.state.count}</button>; }
}

// After
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

Full migration requires handling lifecycle methods, refs, context, HOCs. jscodeshift codemods ship with the framework.

**Vue 2 → 3:** Options API → Composition API. Deprecated filters, removed `.sync` modifier, new slot syntax. `@vue/compiler-sfc` provides AST access.

**Angular:** `ng update` uses schematics (TypeScript AST transforms via TypeScript Compiler API).

### Import reorganization

Sort imports, consolidate duplicates, remove unused. Tools: `organize-imports-cli`, `eslint-plugin-import`, Prettier plugins.

### Codemod safety gates

For every codemod:
1. Run on a test fixture with known before/after.
2. Run on a representative production file.
3. Diff the output against manual rewrite.
4. Run the test suite.
5. Only then apply at scale.

---

## Source-Map Preservation

A source map associates generated output positions with original input positions. Required for:
- Stack traces that point to original source (pre-transform).
- Debuggers that step through original code.
- Editor diagnostics on generated files.

Babel, SWC, esbuild, TypeScript all emit source maps. When chaining transforms, chain the maps too: each tool consumes the upstream source map and produces a composed one (via `source-map` npm package or equivalent).

---

## Roundtrip-Safe Transforms

"Roundtrip-safe" means: parse → transform → print produces output identical to input when no semantic change was made. Required for:
- Code that developers author (comments, formatting, trailing commas must survive).
- Git-friendly diffs (only intended changes appear).

Tools with roundtrip support:
- **recast** (JS): layer over Babel AST that preserves original formatting for untouched nodes.
- **jscodeshift** (JS): uses recast under the hood; `jscodeshift --parser=babel` with careful visitor.
- **ts-morph** (TS): preserves formatting via TypeScript's printer with existing-formatting hints.
- **tree-sitter**: concrete syntax tree includes every token including trivia; you can reprint exactly.
- **libcst** (Python): concrete syntax tree for Python, roundtrip-safe.
- **SwiftSyntax** (Swift): Apple's official roundtrip-safe Swift AST.

Tools that are NOT roundtrip-safe by default:
- Babel's built-in printer: reformats untouched nodes.
- TypeScript's printer: reformats; ts-morph adds hints but cannot always preserve.
- PHP-Parser's standard printer.

**Rule:** if the target is developer-authored code, verify roundtrip fidelity on a test fixture before running at scale.

---

## Anti-patterns

### 1. Regex-based code modification

```javascript
// BAD: this will break on
//   - comments containing "foo"
//   - strings containing "foo"
//   - foo.bar vs foo_bar
//   - multi-line declarations
//   - unicode identifiers
//   - etc.
content.replace(/function foo\(/g, 'function newFoo(');
```

Always use an AST. The 10x time investment pays back on the first edge case the regex missed.

Acceptable regex use cases:
- Non-code text: Markdown, plain text, simple config.
- Tokenization preprocessing (not parsing).
- Transforms bounded to a single token kind in an already-tokenized stream.

### 2. Printer discards comments

A codemod that normalizes formatting (printer strips comments, reformats layout) on code that humans maintain. Review will be impossible; the PR looks like a full rewrite.

### 3. Hand-rolled AST traversal missing nodes

Writing a recursive visitor by hand and forgetting JSX fragments, optional chaining, decorators. Use a framework's visitor (Babel, ts-morph, ESLint) that traverses every official node type.

### 4. Codemod without type information

Rename `oldName` to `newName` as a text replace across a codebase with multiple `oldName` bindings in different scopes. At least two will be wrong. Use a type-aware tool (ts-morph, Roslyn, IntelliJ refactoring API).

### 5. Transform before parse errors are fixed

Running a codemod on a file that failed to parse (the AST is a stub). Silent data loss. Always gate codemod application on successful parse.

### 6. Concurrent mutation during traversal

Babel allows this but the semantics are subtle. Removing a node during its own visit can cause sibling skips. Prefer collecting mutations and applying in a second pass.

### 7. Ignoring source-map chain

Running three transforms without composing source maps leaves stack traces pointing at intermediate output. Compose maps or use a toolchain (esbuild, SWC) that handles it.

### 8. Per-file parse in a large codemod

Parsing each file separately misses cross-file type info. Use ts-morph's Project, or configure jscodeshift with `--parser=tsx` and batch type resolution. For 10k-file codebases, Project-level tools are hours faster.

---

## Checklist: Ship-Ready AST Transform

- [ ] AST framework chosen (Babel / ESLint / jscodeshift / ts-morph / tree-sitter / SWC / libcst)
- [ ] Node types identified and exhaustive visitor covers them
- [ ] Position tracking verified (source maps composable)
- [ ] Roundtrip fidelity decision made (preserve trivia / normalize)
- [ ] Type-awareness decision made (AST-only / semantic analysis)
- [ ] Test fixture (≥3 before/after pairs)
- [ ] Parse-error gate (skip or fail on unparseable files)
- [ ] Scale test (run on 50+ representative files before 10000)
- [ ] Source-map chain verified if part of a pipeline
- [ ] Anti-pattern check (no regex-based modification, no comment stripping, no hand-rolled visitor)
- [ ] Handoff to Shift for migration orchestration if codemod spans many files
