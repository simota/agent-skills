# Regex Safety & ReDoS Prevention

**Purpose:** Protocol for authoring regular expressions that are correct, safe on untrusted input, and portable across engines.
**Read when:** Writing, reviewing, or auditing any regex — especially one that touches user input, log lines, request headers, or file contents of unknown origin.

## Contents
- ReDoS root causes
- Catastrophic backtracking demonstrations
- Regex engine taxonomy
- Detection tools
- Safe patterns and features
- Unicode considerations
- Testing strategies
- Anti-patterns
- Engine-specific notes

---

## ReDoS: Regular Expression Denial of Service

ReDoS is a denial-of-service attack where a carefully crafted input forces a backtracking regex engine into exponential or super-linear runtime. A single request can pin a CPU for minutes.

> **2026 prevalence.** A widely-cited measurement estimates that **~`12%` of JavaScript-based web servers expose at least one ReDoS-vulnerable regex** through their request-handling path. Assume the codebase is vulnerable until proven otherwise — make ReDoS auditing a default CI gate, not an opt-in.

### The Three Root Causes

Every ReDoS-vulnerable regex maps to one of these structural forms:

#### 1. Nested quantifier

```
(a+)+$
```

For input `aaaaa...aaaaaX` the engine tries every partition of the `a`s across the outer and inner quantifier. Runtime: O(2^n) worst case.

#### 2. Overlapping alternation

```
(a|a)*$
```

Two alternatives match the same input. Every character has two parse paths; with `*` that compounds. Runtime: exponential.

Subtler variants: `(a|ab)*`, `(\w|\d)*` (digit is also word), `(x+|x)*`.

#### 3. Quantifier on a quantified group

```
(a*)*$
(.*)*
(\s+)+
```

Empty matches on the inner quantifier combined with the outer quantifier explode the state space. Runtime: exponential.

### The detection heuristic

Walk the regex AST. If any quantified subexpression (`X+`, `X*`, `X{n,}`) matches the empty string OR overlaps with its sibling under a parent quantifier, you have a ReDoS candidate. Automate this with `safe-regex` or `redos-detector`.

---

## Catastrophic Backtracking Demonstration

Node.js (V8, ECMAScript engine):

```js
const pattern = /^(a+)+$/;
const input = 'a'.repeat(30) + 'X';
console.time('match');
pattern.test(input);
console.timeEnd('match'); // ~30 seconds
```

Each added `a` roughly doubles the runtime. 35 `a`s pins a core for ~15 minutes.

RE2 equivalent (Go):

```go
re := regexp.MustCompile(`^(a+)+$`)
re.MatchString(strings.Repeat("a", 30) + "X") // returns in microseconds
```

RE2 is a linear-time (DFA-based) engine — it refuses or rewrites patterns that would require backtracking semantics.

---

## Regex Engine Taxonomy

### Linear-time engines (ReDoS-immune)

| Engine | Language / target | Notes |
|--------|-------------------|-------|
| RE2 | Go stdlib `regexp`, C++, Python (via `re2`) | No backreferences, no lookaround, no recursion |
| Rust `regex` | Rust | RE2-style; optional Unicode, guaranteed O(n) |
| Hyperscan | Intel, C | Stream-scanning multi-pattern matcher; very fast |
| RE2J | Java | Pure Java port of RE2 |

Trade-off: linear-time engines drop features that require NFA backtracking — no backreferences (`\1`), no lookaround in classical RE2 (Rust `regex` allows lookaround at the cost of some linear guarantees on certain constructions), no recursion. If you need those, you cannot be linear-time.

### Backtracking engines (ReDoS-vulnerable)

| Engine | Language / target | Mitigations |
|--------|-------------------|-------------|
| PCRE / PCRE2 | C, PHP, many others | Atomic groups `(?>...)`, possessive quantifiers `a++`, backtrack limit |
| ECMAScript | JS/TS | ES2018 named captures, lookbehind; ES2024 `/v` flag adds atomic groups and set notation |
| Oniguruma / Onigmo | Ruby, mruby | Named captures, multi-byte; ReDoS-prone |
| Java `java.util.regex` | JVM | Atomic groups, possessive quantifiers, backtrack limit via `setMatchLimit` in third-party wrappers |
| .NET `System.Text.RegularExpressions` | .NET | `MatchTimeout`, atomic groups, balancing groups |
| Python `re` | Python | No atomic groups until 3.11; use `regex` package for richer features |
| Perl | Perl | Full PCRE-like semantics |

**Rule of thumb:** if the input can come from a network adversary, prefer a linear-time engine. If you must use a backtracking engine on untrusted input, enforce a hard timeout and audit every pattern.

---

## Detection Tools (2026-05 snapshot)

| Tool | Language | Notes |
|------|----------|-------|
| `safe-regex` (npm) | JS | Simple star-height heuristic; fast but many false negatives — keep only for legacy CI |
| `redos-detector` | JS/TS, Node, Deno, browser | Path-counting analysis with per-pattern **score**; score `1` = no backtracking possible. ESLint plugin (`eslint-plugin-redos-detector`) integrates with existing lint pipelines. Source: [github.com/tjenkinson/redos-detector](https://github.com/tjenkinson/redos-detector) |
| `recheck` | JS / Rust | Hybrid static + fuzzing; reasonable precision; broadest engine coverage; used in many `npm audit`-adjacent toolchains as of 2026 |
| `regexploit` | Python | Finds ReDoS with concrete attack inputs; ideal for CI as a fail-with-PoC step |
| `rxxr2` | OCaml / C | Academic-grade analyser; finds pumping strings; useful for high-stakes audits |
| `Rengar` | Research | Hybrid detector with principled vulnerability modeling and disturbance-free attack-string generation; outperforms `safe-regex` on precision. Source: [ieeexplore.ieee.org/document/10179328](https://ieeexplore.ieee.org/document/10179328/) |
| Semgrep `detect-redos` | JS (and more) | Metavariable-analysis rule in Semgrep ruleset; integrates with existing Semgrep pipelines. Source: [semgrep.dev/r?q=javascript.lang.security.audit.detect-redos](https://semgrep.dev/r?q=javascript.lang.security.audit.detect-redos) |
| ESLint `security/detect-unsafe-regex` | JS | Light backstop; pair with `redos-detector` for coverage |

Usage pattern in CI (2026 default):

```yaml
- run: npx redos-detector check "$(git diff --name-only | xargs)"
- run: npx recheck check ./src                # second-opinion engine
- run: regexploit ./src --score-threshold 100 # PoC on the worst remaining offenders
```

Gate the build on detection; reviewer must justify any exceptions and attach the `redos-detector` score for the regex left in place.

### How `redos-detector` Scores Work (because the score is the contract)

`redos-detector` walks the input string against every path the pattern could take, finds all sibling paths that could also match the same prefix, and reports the **maximum number of backtracks** a worst-case input could force. The mapping:

| Score | Meaning | Action |
|-------|---------|--------|
| `1` | Every input matches in exactly one way; no backtracking possible | Safe to ship |
| `2-5` | Bounded backtracking; super-linear under contrived input but not exponential | Document the input length cap; safe behind a timeout |
| `6-100` | Exponential paths exist within reach | Rewrite, atomic-group, or move to a linear-time engine |
| `> 100` | Worst-case exponential, weaponisable from short inputs | **Block** — treat as a CVE-class finding |

### Linear-Time Revival

After ~5 years of measurable JS ReDoS incidents, there is renewed momentum behind linear-time engines that trade backreferences and lookaround for an `O(n)` worst-case guarantee. Two practical paths in 2026:

- **RE2 / Rust `regex`** for new untrusted-input handlers — accept the feature-set tradeoff up front.
- **Memoized backtracking** (academic, e.g. arXiv `2401.12639`) preserves lookaround and atomic grouping while bounding worst-case time; not yet mainstream but worth tracking before standardising on RE2 for everything.

---

## Safe Patterns and Features

### Anchor everything you can

Unanchored patterns like `/foo/` search the entire input; on a 10MB log line that is unnecessary work. Anchor with `^`, `$`, `\b`, or explicit position semantics.

### Specific character classes over `.`

```
# BAD
<a href="(.*)">

# BETTER (still fragile for HTML — see anti-patterns)
<a href="([^"]*)">
```

Any `.*` or `.+` on untrusted input is a ReDoS liability unless the engine is linear-time.

### Atomic groups and possessive quantifiers (backtracking engines only)

Atomic groups `(?>...)` prevent the engine from backtracking into the group once matched. Possessive quantifiers `a*+`, `a++`, `a?+` are shorthand for single-alternative atomic groups.

```
# Non-atomic (backtracking possible)
^(a+)b

# Atomic (no backtracking into the a+ group)
^(?>a+)b
^a++b        # PCRE / Java
```

**Support matrix:**

| Engine | Atomic group `(?>...)` | Possessive `a++` |
|--------|------------------------|------------------|
| PCRE / Perl | Yes | Yes |
| Java | Yes | Yes |
| .NET | Yes (with `(?>...)` or `(?i-i:...)`) | No direct syntax |
| Ruby (Onigmo) | Yes | Yes |
| ECMAScript pre-2024 | No | No |
| ECMAScript `/v` flag (ES2024) | No (still not supported directly) | No |
| Python `re` | No (Python 3.11+ adds possessive in `re`) | 3.11+ |
| Python `regex` (3rd party) | Yes | Yes |
| RE2 / Rust `regex` | N/A (already linear) | N/A |

### Avoid ambiguous alternation ordering

```
# BAD — first alternative subsumes second, second never matches
(if|ifelse)

# GOOD — longer alternative first, or use anchored match
(ifelse|if)
```

### Prefer fixed-width lookaround

Lookbehind is variable-width in some engines (Java, .NET, ES2018+) and fixed-width in others (Python pre-3.7, PCRE pre-10.34). Keep to fixed-width for portability.

---

## Unicode Considerations

### Code units vs code points vs grapheme clusters

- **Code unit**: UTF-16 unit (JS native strings). `"𝑥".length === 2` — surrogate pair.
- **Code point**: Unicode scalar value. `[..."𝑥"].length === 1`.
- **Grapheme cluster**: what a user perceives as one character. `"👨‍👩‍👧".length === 8` in UTF-16; it is one grapheme.

Regex engines have different defaults:

| Engine | Default unit | Flag for code-point mode |
|--------|--------------|--------------------------|
| ECMAScript | Code unit | `/u` (Unicode mode), `/v` (Unicode sets, ES2024) |
| Python 3 `re` | Code point | Default; `re.ASCII` opts out |
| Rust `regex` | Unicode-aware | On by default |
| RE2 | Byte or rune | `(?-u)` to switch |
| PCRE | Byte or code point | `(*UTF)` or `/u` depending on binding |
| Java | Code unit; `(?U)` enables Unicode property escapes | `Pattern.UNICODE_CHARACTER_CLASS` |

### Unicode property escapes

```
\p{L}        # any letter
\p{N}        # any number
\p{Script=Hiragana}
\p{White_Space}
\p{Emoji}
```

Supported in ECMAScript with `/u`, in modern PCRE, Python `regex`, Rust `regex`, Java. Prefer over ASCII ranges like `[a-zA-Z]` when input is multilingual.

### Grapheme clusters

- PCRE: `\X` matches one extended grapheme cluster.
- ECMAScript: no native `\X`; use `Intl.Segmenter` with `granularity: 'grapheme'`.
- Rust: `unicode-segmentation` crate.

**Rule:** if you need to count "visible characters" for truncation or cursor movement, use grapheme segmentation APIs, not regex.

### Unicode 16.0 (released September 2024)

Unicode 16.0 adds 5,185 new characters (total: 154,998), including 7 new scripts (Garay, Gurung Khema, Kirat Rai, Ol Onal, Sunuwar, Todhri, Tulu Tigalari), 7 new emoji, and 686 legacy computing symbols. Source: [unicode.org/versions/Unicode16.0.0](https://www.unicode.org/versions/Unicode16.0.0/)

**Impact on regex:**
- `\p{Script=...}` values for the new scripts are available in engines that bundle Unicode 16 data (PCRE2 10.45+, Rust `regex` 1.11+, ICU 76+).
- `\p{Emoji}` now covers the 7 new emoji; update regex-based emoji filters after an engine upgrade.
- If your engine bundles an older Unicode version (common in older Node.js / V8 builds), property escapes for new scripts may silently miss matches. Check your engine's bundled Unicode version before relying on `\p{Script=Garay}`.

### Normalization

NFC, NFD, NFKC, NFKD. A search for `"café"` might miss `"café"` unless both are normalized to the same form. Normalize at ingest.

---

## Testing Strategies

### Positive and negative corpus

Every non-trivial regex ships with:
- ≥3 positive inputs (expected matches)
- ≥3 negative inputs (expected non-matches including boundary cases)
- ≥1 worst-case input (longest expected runtime given engine)

### Property-based fuzzing

`fast-check` (JS), `hypothesis` (Python), `proptest` (Rust) can generate strings from a grammar and check invariants:

```js
import fc from 'fast-check';

fc.assert(fc.property(fc.string(), (input) => {
  const start = Date.now();
  pattern.test(input);
  return Date.now() - start < 100; // 100ms budget
}));
```

### Worst-case benchmarks

Explicit benchmarks for known ReDoS patterns:

```js
// tests/pattern.bench.ts
const worstCase = 'a'.repeat(30) + 'X';
bench('pattern on worst case', () => pattern.test(worstCase));
// Assert completion under 10ms for RE2, N/A for backtracking engines without timeout
```

### Timeout enforcement

When a backtracking engine is unavoidable and input is untrusted:

- .NET: `new Regex(pattern, options, TimeSpan.FromMilliseconds(100))`
- Java: use a worker thread with interrupt; stdlib has no native timeout
- Node.js: run in a Worker thread with timeout, or use RE2 bindings (`re2` npm package)
- Python: run in a subprocess; `re` has no timeout

---

## Anti-patterns

### 1. Parsing HTML / XML with regex

```
# WRONG
/<([a-z]+)(.*?)>(.*?)<\/\1>/
```

HTML is not a regular language. Use a parser: `jsdom`, `cheerio`, `parse5`, `html5ever`. Regex-based HTML parsing fails on nested tags, CDATA, comments, processing instructions, HTML entities, and malformed-but-browser-accepted markup.

### 2. Parsing JSON with regex

JSON is a context-free grammar. Use `JSON.parse`. Regex cannot balance `{}` and `[]`.

### 3. Parsing email addresses with RFC 5322 regex

The full RFC 5322 regex is ~6000 characters. Almost no product needs full RFC 5322 compliance. Use the WHATWG HTML email validation regex instead:

```
# WHATWG / HTML5 form validation (the pragmatic choice)
/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/
```

Or, for maximum practicality, validate with `/@/` and send a confirmation email — the mail system is the real validator.

### 4. Parsing URLs with regex

Use `URL` (WHATWG), `url.parse` (Node deprecated), or a URL parser library. URL grammar is complex (RFC 3986 + WHATWG living standard) and full of engine-specific escape rules.

### 5. Stripping whitespace with `/\s+/g`

If input is untrusted and contains many whitespace runs, `/\s+/g` with a replacement can still be slow on backtracking engines. Prefer `String.prototype.split(/\s+/)` or explicit iteration.

### 6. Using regex to parse programming languages

Use a real parser. See `parser-generators.md`.

---

## Engine-Specific Notes

### ECMAScript

- `/u` flag enables Unicode mode (code-point semantics, property escapes).
- `/v` flag (ES2024) adds set notation `[[a-z]--[aeiou]]`, string properties. Browser support: V8 12+ / Chrome 112+, WebKit/Safari 17+.
- **ES2025 new regex features** (ECMA-262 16th edition, finalized June 2025): Source: [tc39.es/ecma262/2025](https://tc39.es/ecma262/2025/multipage/)
  - `RegExp.escape(str)` — safely escapes a raw string for use inside a regex literal; eliminates regex-injection bugs from `new RegExp(userInput)`.
  - **Inline flag modifiers** `(?i:...)` — apply a flag (e.g. case-insensitivity) to only part of the pattern; active flag after `?`, deactivated flag after `-`.
- No atomic groups in ECMAScript (pre-ES2025); rewrite or use `regex` npm package with RE2 semantics.
- Named captures: `(?<name>...)`.
- Lookbehind: `(?<=...)` / `(?<!...)` — ES2018.

### PCRE

- Backtrack control verbs: `(*ACCEPT)`, `(*FAIL)`, `(*COMMIT)`, `(*PRUNE)`, `(*SKIP)`.
- Subroutine calls: `(?1)`, `(?&name)` — recursive subpattern invocation.
- `\A`, `\Z`, `\z` absolute anchors distinct from `^` `$`.

### RE2

- No backreferences: `\1` is a syntax error.
- No lookaround: `(?=...)` is a syntax error.
- No recursion.
- Unicode-aware by default; `(?-u)` for byte mode.
- Trade these feature losses for guaranteed linear time — fair trade on untrusted input.

### Rust `regex`

- Similar feature set to RE2.
- Pre-compile patterns with `Regex::new` once; never in a hot loop.
- `regex-automata` crate for low-level DFA access.

### .NET

- `RegexOptions.NonBacktracking` (since .NET 7) gives RE2-style semantics.
- `MatchTimeout` enforces a hard timeout — use it on untrusted input.
- Balancing groups: `(?<open>\()|(?<-open>\))` — a non-regular feature unique to .NET.

### Java

- Compile with `Pattern.compile(regex, Pattern.UNICODE_CHARACTER_CLASS)` for Unicode semantics.
- No stdlib timeout; wrap with `Thread.interrupt()` pattern or use `RE2J`.

### Python

- `re` module is backtracking; no atomic groups until 3.11.
- `regex` package (`pip install regex`) is a superset with atomic groups, recursion, Unicode property escapes, `\X` grapheme, `\p{…}` — drop-in better replacement.

---

## Checklist: Ship-Ready Regex

- [ ] Engine target declared (RE2 / PCRE / ECMAScript / …)
- [ ] Input trust level declared (trusted / untrusted)
- [ ] ReDoS analysis complete (no nested quantifier / overlapping alternation / quantified-quantifier)
- [ ] Complexity class documented (O(n) / O(n·m) / O(n²) / exponential)
- [ ] Worst-case pumping string documented
- [ ] Unicode posture declared (`/u` flag, property escapes, grapheme handling)
- [ ] ≥3 positive, ≥3 negative, ≥1 worst-case test input
- [ ] Timeout enforced if backtracking engine + untrusted input
- [ ] Anti-pattern check (not parsing HTML/XML/JSON/language/URL)
