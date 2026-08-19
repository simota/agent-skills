# Ambiguity Lexicon

**Purpose:** The detection surface — seven lexical classes, their vocabulary in English and Japanese, why each is ambiguous, and the disposition each defaults to.
**Read when:** You are in `SCAN` and need the catalog, or you are unsure whether a term counts as a detection.

## Contents
- Detection rule
- The seven classes
- Open semantic detection
- Non-English source prompts
- Non-detections

---

## Detection Rule

A term is a detection when **two defensible readings of it would produce different deliverables**. The lexicon below is a starting set, not an allowlist — a domain word absent from every table still counts if it fails that test, and a listed word does not count if the surrounding text already fixes its reading.

Record the competing readings, not just the word. `"concise" → (a) under 200 words (b) no redundancy at any length` is a detection; `"concise — vague"` is not usable downstream.

---

## The Seven Classes

### 1. Quality

| Vocabulary | Why ambiguous | Default |
|------------|---------------|---------|
| good, high-quality, best, optimal, professional, top-tier, polished, refined, compelling, effective | Names a verdict without naming the standard that produces it | `CRITERIA` |

Quality words are the highest-value detections: they are what the author will judge the output by, and they are the ones most often answered with another quality word.

### 2. Quantity

| Vocabulary | Why ambiguous | Default |
|------------|---------------|---------|
| concise, brief, short, detailed, thorough, comprehensive, in depth, sufficient, moderate | A length instruction with no scale; "detailed" spans one paragraph to twenty pages | `QUANTIFY`, else `BEHAVIORALIZE` |

### 3. Explanation Level

| Vocabulary | Why ambiguous | Default |
|------------|---------------|---------|
| clear, easy to understand, simple, for beginners, for experts, broken down, carefully | Depends entirely on an unstated reader model | `AUDIENCE` + `BEHAVIORALIZE` |

### 4. Style

| Vocabulary | Why ambiguous | Default |
|------------|---------------|---------|
| natural, casual, formal, friendly, soft, intelligent, human-like, not AI-sounding | Register words with no shared referent; "not AI-sounding" names a negative no one can check | `BEHAVIORALIZE` |

"Human-like" and "not AI-sounding" translate to concrete surface rules (sentence-length variation, no section-summary closers, no tricolon padding) or they translate to nothing.

### 5. Design

| Vocabulary | Why ambiguous | Default |
|------------|---------------|---------|
| modern, simple, minimal, stylish, premium, Apple-like, current, intuitive | Aesthetic labels whose referents shift by year, market, and taste | `BEHAVIORALIZE` (visual rules) |

Named-brand comparisons ("Apple-like") are additionally unsafe as instructions to imitate; translate to the underlying properties (restraint in color count, generous spacing, one primary action per screen), never to the brand.

### 6. Technical

| Vocabulary | Why ambiguous | Default |
|------------|---------------|---------|
| clean code, efficient, fast, robust, secure, maintainable, extensible, best practice, production-quality | Each names a whole discipline; without a threshold or a checklist the executor picks its own | `CRITERIA`, `QUANTIFY` where a metric exists |

"Fast" and "secure" often belong to an enforcing layer rather than the prompt — a budget checked in CI, a scanner in the pipeline. Check before translating.

### 7. Judgment

| Vocabulary | Why ambiguous | Default |
|------------|---------------|---------|
| as appropriate, if needed, where possible, as much as you can, important ones, representative, recommended, latest | Delegates a decision without giving the criterion the decision needs | `CONDITION`, `DATE` for recency words |

This class is where the largest silent variance lives: "as appropriate" reads as "always" to one executor and "rarely" to another, and both are defensible.

---

## Open Semantic Detection

After the seven classes, sweep for these — they carry no signature vocabulary:

- **Missing actor.** Who performs, who verifies, who decides. Especially common in subject-dropping languages, where the actor is routinely absent from the sentence.
- **Missing object.** "Improve it" — improve which property?
- **Unstated comparison.** "Better", "faster", "more consistent" — than what baseline?
- **Undeclared scope.** Whether an instruction covers one file, one feature, or the whole system.
- **Implied precedence.** Two instructions that will collide only in some inputs, with no stated winner.
- **Unbounded enumeration.** "List the options" — all of them, or a selection made on an unstated criterion?

---

## Non-English Source Prompts

A prompt written in a language that drops arguments or nominalizes freely hides ambiguity in **grammar** as much as in adjectives. The lexical sweep above will miss all of it. Japanese is the common case here; the same patterns appear in Korean and, partially, in Chinese.

| Pattern | Ambiguity it hides | Detection cue |
|---------|--------------------|---------------|
| Dropped subject | Who acts, who verifies, who decides is undecided | A bare verb phrase ("verify", `kakunin suru`) with no agent anywhere in the sentence or its neighbors |
| Open-ended enumeration suffix (`nado`, "and so on") | The set has no closure rule — one more item, or twenty | An enumerated list ending in the suffix instead of a stated boundary |
| Property-nominalizing suffix (`-teki`, "-wise", "-oriented") | A whole discipline compressed into one adjective | `efficiency-wise`, `coverage-wise` used as if it were a bound |
| Permission vs preference modals (`-te mo yoi` "may", `-ga nozomashii` "is desirable") | Requirement level is unmarked — optional, preferred, or mandatory | A modal that could be read as any of MUST / SHOULD / MAY |
| Compound delegation | Neither the set nor the trigger is fixed | The enumeration suffix and a discretion word in one canon ("add examples and so on as appropriate") |

Translate the **missing argument**, not just the vague word. A dropped-subject "verify" becomes *who* verifies and *what check* they run — not an intensified "verify thoroughly", which changes nothing and reads as progress.

The rewritten prompt stays in the source's language (`SKILL.md` § Output Requirements); only the ledger and the derived rules follow the configured output language.

---

## Non-Detections

Do not flag these; flagging them inflates the ledger and buries real findings.

- Terms the surrounding text already fixes ("concise — one paragraph").
- Domain terms of art with a single accepted meaning in context (`p95`, `idempotent`, `RLS`).
- Deliberate open-endedness the source marked as such ("pick whichever framing you prefer").
- Aesthetic or voice choices in a task whose purpose is exploration — those are `KEEP` candidates, not defects (`ambiguity-budget.md`).
- Politeness and framing language that carries no instruction ("thanks in advance").
