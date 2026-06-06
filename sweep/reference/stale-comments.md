# Stale Comments Cleanup

Reference for Sweep's `comments` recipe. Detect stale TODOs/FIXMEs, commented-out code blocks, divergent JSDoc, version-stale annotations, and dead doc references.

> Comments do not affect runtime; safe to remove at confidence ≥ 70. But they encode intent and history — verify with `git blame` before bulk removal.

---

## 1. Categories of Stale Comments

| Category | Indicator | Confidence to remove |
|---|---|---|
| Aged TODO/FIXME | `// TODO(2023):` or git blame >180 days | 70-85 |
| Commented-out code | `/* ... */` block of N≥3 lines that was once code | 80-90 |
| Divergent JSDoc | `@param x: number` but actual signature is `string` | 60-75 (auto-fix safer) |
| Version-stale | `// added in v1.2` and current version is 5.x | 75-85 |
| Author/date noise | `// John 2018-04-15` | 90+ (no value) |
| Dead reference | `// see docs/old-feature.md` (file deleted) | 85+ |
| Obvious paraphrase | `i++; // increment i` | 85+ |
| Outdated workaround | `// workaround for IE11 bug` (IE11 dropped) | 80-90 |

---

## 2. Detection Strategies

### Aged TODO/FIXME
```bash
# Find TODO/FIXME with git blame age
git ls-files | xargs grep -nE '(TODO|FIXME|HACK|XXX)' 2>/dev/null | while read -r line; do
  file=$(echo "$line" | cut -d: -f1)
  lineno=$(echo "$line" | cut -d: -f2)
  age=$(git log -1 --format=%ci -L "$lineno,$lineno:$file" 2>/dev/null | head -1)
  echo "$age | $line"
done | sort
```

Or use `tslint`/`biome`/`ruff` plugins:
- `eslint-plugin-todo-plz` — fail on undated/stale TODOs
- `pylint W0511` — warning on TODO comments

### Commented-out code blocks
Heuristic: ≥ 3 consecutive lines starting with `//` or inside `/* */` that contain code-like syntax (matched braces, identifiers, semicolons).

```bash
# Rough detector for commented JS/TS blocks
grep -rB0 -A20 -nE '^[[:space:]]*//[[:space:]]*\b(if|for|while|function|const|let|var|class|return)\b' --include='*.ts' --include='*.js' src/
```

Tools:
- `eslint-plugin-eslint-comments`
- `dead-code-detection` (custom AST analyzers)

### Divergent JSDoc
Compare `@param` / `@returns` annotations to actual function signatures.
- TypeScript: `tsc --noEmit` catches type mismatches when types are inferred from JSDoc
- ESLint: `jsdoc/check-param-names`, `jsdoc/check-types`

### Version-stale annotations
```bash
# Find "added in vX.Y", "since vX.Y", "deprecated in vX.Y"
grep -rEn '(added in|since|deprecated in)[[:space:]]+v?[0-9]+\.[0-9]+' --include='*.ts' --include='*.js' src/
```

Compare to current package.json version. If current is N major versions ahead, the annotation is stale.

### Dead doc references
```bash
# Find comment links to docs/ files
grep -rEn 'docs/[a-z0-9_-]+\.md' --include='*.ts' --include='*.js' src/ | while read -r line; do
  ref=$(echo "$line" | grep -oE 'docs/[a-z0-9_-]+\.md')
  [ -f "$ref" ] || echo "DEAD: $line"
done
```

---

## 3. What to KEEP (high false-positive risk)

| Pattern | Reason to keep |
|---|---|
| `// SAFETY:` comments in unsafe Rust / unsafe JS | Documents invariants required for soundness |
| Comments inside complex regex | Regex is opaque; comment is the primary documentation |
| License headers | Required for compliance |
| `// eslint-disable-next-line` | Active suppression |
| Type assertions explained: `// `as Foo` because Bar` | Documents type-system limitation |
| External API quirk: `// API returns 0 instead of null when X` | Encodes vendor behavior |
| Race condition / concurrency: `// must be called before lock release` | Documents subtle invariant |
| Number with no obvious meaning + comment: `2592000 // 30 days in seconds` | Constant explanation |

---

## 4. Confidence Scoring Rules

| Signal | Confidence delta |
|---|---|
| Tool flagged | +20 |
| `git blame` age > 180 days | +15 |
| `git blame` age > 365 days | +25 |
| Commented-out code (≥ 3 lines) | +30 |
| Author tag with old date | +20 |
| References deleted file | +25 |
| Divergent JSDoc + auto-fix available | +20 |
| Inside complex algorithm or regex | -40 |
| Contains `SAFETY` / `WARN` / `INVARIANT` keywords | -50 |
| License header | -100 (never remove) |

Threshold for auto-removal proposal: ≥ 70.

---

## 5. Verification

Comments are runtime-irrelevant, but:
- Some build tools strip comments → bundle hash may change → trigger CI cache miss (mostly OK)
- Type-providing JSDoc (in JS-only projects without TS) IS load-bearing — verify via `tsc --noEmit --checkJs`
- Sourcemaps may shift; integration tests using exact line numbers will break

---

## 6. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Removing JSDoc that provides types in JS-only project | Run `tsc --checkJs` baseline first |
| Removing `// eslint-disable` comments | Tag suppressions as protected |
| Removing license headers | Maintain explicit allow-list |
| Bulk remove `// TODO` from tracked work items | Cross-reference against issue tracker |
| Removing safety/invariant comments | Keyword filter: SAFETY, INVARIANT, WARN, XXX-safety |
| Removing comment-out code that's intentional reference | Check git history for "see for reference" pattern |
| Date comments removed but they document audit trail | Compliance projects keep author+date |

---

## 7. Decision Walkthrough Template

```
Scope: ____ files
Comment categories scanned:
  □ Aged TODO/FIXME (>180d)
  □ Commented-out code blocks
  □ Divergent JSDoc
  □ Version-stale annotations
  □ Dead doc references
  □ Obvious paraphrase

Findings:
  Total comment candidates: ____
  Auto-removable (conf ≥ 80):  ____
  Review-required (conf 70-79): ____
  Protected (license/safety):  ____

Verification:
  □ tsc --checkJs baseline pass (if JS+JSDoc)
  □ ESLint pass post-removal
  □ License headers preserved
  □ TODO items cross-checked vs issue tracker

Handoff:
  □ Builder for execution
  □ Quill for JSDoc auto-fix (divergent annotations)
```

---

## 8. References
- `eslint-plugin-jsdoc` (validate / autofix JSDoc)
- `eslint-plugin-todo-plz` (require dated TODOs)
- `pylint W0511`, `ruff TD002` (Python TODO checking)
- TypeScript `--checkJs` (validate JSDoc types)
- ESLint comments plugin (manage `eslint-disable` directives)
