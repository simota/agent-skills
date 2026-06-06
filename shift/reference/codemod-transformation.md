# Codemod Transformation Reference

Purpose: Author and apply AST-based code transformations across a codebase. Covers tool selection (jscodeshift / ts-morph / ast-grep / comby / Recast), dry-run workflow, idempotency discipline, and commit-batch rollout.

## Scope Boundary

- **horizon `codemod`**: AST-transformation authoring and rollout (this document).
- **horizon `replace` (elsewhere)**: Library-level swap decisions; codemod is often the execution tool.
- **horizon `strangler` (elsewhere)**: System-level incremental migration. Codemod is one tactic used inside a Strangler.
- **shift (elsewhere)**: Migration orchestration. `shift` may commission a codemod; `codemod` here designs and runs it.
- **Builder (elsewhere)**: Executes the codemod PRs at commit granularity.
- **Judge (elsewhere)**: Reviews codemod output before merge.

## Tool Selection

| Tool | Strength | Use when |
|------|---------|----------|
| **jscodeshift** | Mature JS/TS ecosystem, recast under hood | Large JS/TS rewrites, framework migrations |
| **ts-morph** | TypeScript-aware, type-preserving | TypeScript refactors needing type info (rename, move members) |
| **ast-grep** | Polyglot (Tree-sitter), pattern-based | Simple multi-language pattern → pattern rewrites |
| **comby** | Syntax-light regex-like | Lightweight multi-language textual patches where full AST is overkill |
| **Recast** (low-level) | Formatting-preserving AST output | Custom tools or embedded in scripts |
| **OpenRewrite** | JVM ecosystem (Java / Kotlin / Gradle) | Enterprise Java refactors |
| **Ruff-fix / Black** | Python | Python auto-formatting / Python codemods via LibCST |
| **LibCST** | Python concrete syntax tree | Python codemods preserving comments |
| **gofmt + rewrite** | Go | Go code-level rewrites |
| **Rustfmt + rustfix** | Rust | Rust compiler-suggested edits |

## Workflow

```
DESIGN     →  define before/after pattern
           →  write positive and negative test cases

AUTHOR     →  implement codemod in chosen tool
           →  cover edge cases (comments preserved, imports updated)

DRY-RUN    →  run against 10-20 sample files
           →  diff-review manually
           →  fix misses and over-matches

VALIDATE   →  idempotency: running twice = same output
           →  correctness: existing tests still pass on sampled files
           →  coverage: sampled missed cases < 5%

BATCH      →  split by directory / package / commit size
           →  typical batch: 50-200 files or ≤ 500 LOC per commit

ROLLOUT    →  commit batch by batch
           →  one commit per logical transform (per rule)
           →  include before/after example in commit message

REVIEW     →  Judge reviews batch-0 carefully
           →  subsequent batches fast-track if batch-0 passes

CLEANUP    →  remove codemod script or archive under scripts/codemods/
           →  document in CHANGELOG
```

## Example — jscodeshift (React PropTypes → TypeScript)

```js
// codemod-proptypes-to-ts.js
module.exports = function(fileInfo, api) {
  const j = api.jscodeshift;
  const root = j(fileInfo.source);

  // find: Component.propTypes = { ... };
  root.find(j.ExpressionStatement, {
    expression: {
      type: 'AssignmentExpression',
      left: { type: 'MemberExpression', property: { name: 'propTypes' } }
    }
  }).forEach(path => {
    const componentName = path.value.expression.left.object.name;
    const props = path.value.expression.right.properties;

    // generate TypeScript interface
    const iface = j.tsInterfaceDeclaration(
      j.identifier(`${componentName}Props`),
      j.tsInterfaceBody(
        props.map(p => j.tsPropertySignature(
          j.identifier(p.key.name),
          j.tsTypeAnnotation(mapPropType(p.value))
        ))
      )
    );

    // insert before component, remove propTypes assignment
    path.insertBefore(iface);
    j(path).remove();
  });

  return root.toSource({ quote: 'single' });
};

function mapPropType(node) {
  // PropTypes.string → string, PropTypes.number → number, ...
  // (edge cases omitted for brevity)
}
```

Run:
```
npx jscodeshift -t codemod-proptypes-to-ts.js --dry --print 'src/components/**/*.js'
# review output
npx jscodeshift -t codemod-proptypes-to-ts.js 'src/components/Button.js'
# batch
npx jscodeshift -t codemod-proptypes-to-ts.js 'src/components/**/*.js'
```

## Idempotency Check

Every codemod **must** produce the same output on a second run:

```
1. Run codemod → output A
2. Run codemod again → output B
3. A === B  →  idempotent (safe)
   A !== B  →  bug; fix before rollout
```

Common non-idempotent bugs:
- Generating a new import every run (always appending).
- Not detecting already-transformed code.
- Regex-based "find and replace" that re-matches its own output.

## Safety Checks

| Check | Fix if missing |
|-------|----------------|
| Comments preserved | Use Recast / jscodeshift / LibCST (CST-level, not AST) |
| Imports updated | Add/remove imports as a dedicated pass |
| Trailing commas preserved | Configure tool's printer |
| Quotes (single vs double) preserved | Match project style |
| Indentation preserved | Use formatting-preserving tool |
| Non-target code untouched | Tight pattern matching, test with negative cases |
| Types valid after transform | Run `tsc --noEmit` on sample |
| Tests still pass | Run unit tests on sample |
| Lint passes | Run ESLint on sample |

## Batch Rollout

| Batch size | Use when |
|-----------|----------|
| 1 file | High-risk areas, first batch of a new codemod |
| 10-50 files | Medium-risk, review batch-0 carefully |
| 50-200 files | Standard refactor |
| Whole directory | Low-risk transforms that have passed smaller batches |
| Whole repo | Only after ≥3 successful batches |

PR / commit granularity:
- **Preferred**: one PR per batch, linked to a parent issue.
- **Commit message template**: `refactor(scope): codemod <description> (batch N/M, X files)`.
- **Each PR**: auto-generated, human-reviewed batch-0, fast-track subsequent.

## Rollout Ordering Heuristics

1. **Start with test files** — if they break, easy to see.
2. **Then type-only modules** — low blast radius.
3. **Then leaf modules** — no downstream consumers.
4. **Then shared utilities** — careful review.
5. **Finally critical paths** — auth, payment, core flows.

## When NOT to Use Codemod

- **< 10 occurrences**: manual edit is faster.
- **Semantic ambiguity**: if the tool cannot distinguish cases without human judgment, don't force it.
- **One-off rename where IDE Rename-Symbol works**: use the IDE.
- **Complex refactors requiring architectural judgment**: hand off to Atlas / Builder.

## Output Template

```markdown
## Codemod: [Name]

### Goal
[Before / after pattern summary in 1-2 lines]

### Tool
- **Chosen**: [jscodeshift / ts-morph / ast-grep / comby / ...]
- **Rationale**: [why this tool]

### Patterns
- **Target pattern (AST)**: [description or code sample]
- **Replacement pattern**: [description or code sample]
- **Edge cases**: [list]
- **Negative cases** (must NOT match): [list]

### Dry-Run Results
- **Sample size**: N files
- **Matches**: M
- **Over-matches (wrong)**: X → fixed by [rule tweak]
- **Under-matches (missed)**: Y → fixed by [rule tweak]

### Idempotency
- [x] Running twice produces identical output.

### Safety
- [x] Comments preserved
- [x] Imports updated
- [x] Formatting preserved
- [x] `tsc --noEmit` green on sample
- [x] Unit tests green on sample
- [x] Lint green on sample

### Rollout Plan
- Batch 0: [path pattern, N files, reviewer]
- Batch 1: [...]
- ...

### Rollback
- Revert the specific PR(s).
- Since codemod is reversible (code-only), rollback is `git revert`.

### Handoff
- Builder: execute batches.
- Judge: review batch-0 in detail.
- Zen: re-evaluate readability of transformed code.
- shift: if this is part of a larger migration.
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Regex-only "codemod" on complex syntax | Use AST tool |
| No dry-run before full run | Always dry-run + diff-review on sample |
| Skipping idempotency check | Always test double-run |
| Big-bang across 1000 files in one PR | Batch 50-200 |
| No negative test cases | Author negative cases explicitly |
| Losing comments | Use formatting-preserving library (Recast / LibCST) |
| Running without lint/tests | Always run both on sample first |

## Deliverable Contract

When `codemod` completes, emit:

- **Tool selection** with rationale.
- **Before/after pattern** with negative cases.
- **Dry-run results** (matches, over/under).
- **Idempotency verified**.
- **Safety-check list** (comments, imports, formatting, tests, lint).
- **Batched rollout plan** (size + order).
- **Rollback plan** (revert PRs).
- **Handoffs**: Builder, Judge, Zen, shift.

## References

- Facebook jscodeshift
- ts-morph (TypeScript Compiler API wrapper)
- ast-grep (Tree-sitter based, polyglot)
- comby.dev
- Benjamin Coe — "Writing codemods with jscodeshift"
- Stripe Engineering — large-scale codemod rollouts
- Airbnb — React codemods for class → hooks
- OpenRewrite (JVM)
- LibCST (Python Concrete Syntax Tree, Meta)
