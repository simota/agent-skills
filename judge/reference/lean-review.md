# Lean Review — Detecting Waste During Code Review

> Read this when running the `lean` recipe, or when the lean dimension fires inside the default `pr` flow. Lean is the third quality axis alongside **secure** (security/absence detection) and **correct** (bug/logic). It answers: *"Is this code doing more than it needs to?"*

Judge **detects and reports** waste. It does **not** delete or simplify — that is Zen (dead code / simplification implementation) and Void (YAGNI verdict / scope-cut decision). Lean review surfaces the finding with evidence, scores it, and routes it.

---

## The Lean Dimension vs Style

Lean is **not** style. A lean finding must tie to a **measurable cost** — extra code paths to maintain, an abstraction with one caller, a confirmed duplicate, an unreferenced export. If the rationale reduces to *"this feels over-engineered"* or *"I'd write it differently,"* it fails `style_bias_check` and is **rejected** (it never ships). This is the dominant FP source for lean review; hold the line.

| Ships as a lean finding | Rejected (style bias) |
|--------------------------|------------------------|
| "Strategy interface has exactly 1 implementation, no second planned in this PR" | "This could be more elegant" |
| "`formatDate` here duplicates `utils/date.ts:formatDate` (identical body)" | "I prefer composition over inheritance" |
| "`legacyMode` flag is never read after line 40 — dead since commit abc123" | "Too many small functions" |
| "Param `options.retryV2` is passed but never consumed" | "Naming is verbose" |

---

## The 6 Waste Patterns

Each pattern lists: **signal** (what to look for), **evidence required** (the verifiable fact that lets it ship), **severity**, **route**.

### L1 · Over-engineering / Gas-factory abstraction
- **Signal:** Abstraction layers (factories, managers, generic base classes, dependency-injection scaffolding) whose complexity exceeds the concrete need. Indirection with one concrete path.
- **Evidence required:** Caller count = 1 (or N where the abstraction buys nothing at N), and no second use introduced in this PR/spec.
- **Severity:** MEDIUM (LOW if isolated, HIGH if it spreads a pattern across files).
- **Route:** Void (is the abstraction justified? CoK verdict) → Zen (collapse if confirmed).

### L2 · YAGNI violation (speculative future-proofing)
- **Signal:** Code, config, flags, or parameters built for a requirement that does not exist yet. "We'll need this later." Unused hooks/extension points.
- **Evidence required:** The feature/branch is not exercised by any current caller, test, or the stated PR intent.
- **Severity:** MEDIUM.
- **Route:** Void (5 Existence Questions + CoK) — Void owns the YAGNI verdict.

### L3 · Dead code
- **Signal:** Unreachable branches, unreferenced exports/functions, retired feature flags, commented-out blocks, unused imports.
- **Evidence required:** No reference in the codebase (grep-confirmed at GROUND), or provably unreachable control flow. Not "looks unused."
- **Severity:** LOW–MEDIUM (MEDIUM if it carries security surface or confuses readers).
- **Route:** Zen (`dead_code_removal`) — mechanical, behavior-preserving.

### L4 · Speculative generality
- **Signal:** Generic type params, configurable options, or pluggable seams with a single fixed value/implementation. `<T>` that is always `string`. An options bag where every caller passes the same thing.
- **Evidence required:** All call sites use identical concrete values; the generality is never varied.
- **Severity:** LOW–MEDIUM.
- **Route:** Void (justified?) → Zen (specialize).

### L5 · Redundant / duplicated logic
- **Signal:** Copy-pasted blocks, a re-implementation of an existing utility, parallel code paths that do the same thing, redundant transformations (map→filter→map collapsible).
- **Evidence required:** Cite the existing equivalent (`file:line`) or the duplicated sibling. Bodies are semantically equal.
- **Severity:** MEDIUM (HIGH if the duplicate is a correctness liability — two copies drift).
- **Route:** Zen (`logic_simplification` / consolidate to the canonical impl).

### L6 · Unnecessary dependency
- **Signal:** A new package added for what the stdlib or an existing in-repo util already does (left-pad-class deps, a date lib for one `toISOString`).
- **Evidence required:** Name the stdlib/existing equivalent that covers the use; confirm the dep is used only for that.
- **Severity:** MEDIUM (carrying cost: supply-chain surface, bundle size).
- **Route:** Void (frequency × carrying cost × risk) → Shift/Builder for removal.

---

## Lean ≠ Removing Defenses (hard boundary with absence-detection)

Lean review and Judge's **absence detection** pull in opposite directions; do not let lean delete real defenses.

- **Never flag as waste:** input validation, parameterized queries, output encoding, URL allowlists, or any check at a **system boundary** (user input, external API, untrusted data). These are *required*, not waste — even if they "look defensive."
- **Eligible for lean:** redundant guards on **internal, type-guaranteed** paths only (matches Zen's `defensive_cleanup` boundary) — e.g. a null-check on a value the type system already proves non-null, the same validation re-run two layers deep.
- When unsure whether a guard is boundary or internal → **keep it** and do not file a lean finding. Secure beats lean.

---

## Scoring & Routing Summary

| Cost-of-Keeping (CoK proxy) | Action |
|------------------------------|--------|
| Low — mechanical, behavior-preserving (dead code, unused import, duplicate) | Route **Zen** directly with a Fix Prompt |
| Medium — needs a "is this justified?" judgment (abstraction, generality, YAGNI) | Route **Void** for verdict, then Zen/Builder |
| High — removal has blast radius (public API, shared module, data) | Route **Void**; **Ask First** before any excision (mirrors SKILL Ask-First) |

Lean findings obey the universal FILTER discipline: VERIFIED/CONFIRMED + concrete evidence + severity ≥ MEDIUM to ship in the main list (LOW lean findings go to a condensed "leanness notes" sub-list, not the headline). Track lean FP-rate against the **maintainability < 5%** category ceiling.

---

## `lean` Recipe VERIFY Gate

In addition to Judge's universal FILTER discipline, the `lean` recipe ships only if:
1. **Every finding cites a verifiable fact** — caller count, grep-confirmed non-reference, named duplicate `file:line`, or unused param. No speculative "might not need this later" without present-tense evidence.
2. **`style_bias_check` passed** on every finding — no "looks over-engineered" rationales.
3. **No boundary defense flagged** — absence-detection invariant held (see hard boundary above).
4. **Behavior-preservation is deferred, not asserted** — Judge reports the waste; it does **not** claim the removal is safe. The safety proof belongs to Zen (equivalence) / Void (blast radius) at fix time.
5. **High-CoK removals routed to Void**, not proposed for direct deletion.

When run as a dimension inside the default `pr` flow (not the standalone `lean` recipe), keep it light: surface only HIGH/MEDIUM L1–L6 with airtight evidence; push LOW lean noise to the leanness-notes sub-list so it never erodes SNR.
