# Design System as Machine-Readable Context

How to expose a design system so an agent **consumes it as a constraint** rather than re-inferring it from screenshots. Read when packaging a system for downstream agents (`forge`, `artisan`, `pixel`, `native`, `vitrine`), when a generated UI keeps inventing components or raw values, or when deciding what to hand an agent versus what to withhold.

**Composes with:** `_common/design-system-registry.md` (the persistence contract), `_common/ASSET_PROVENANCE.md` (rights on assets referenced by the system), `frame/reference/token-mapping.md` (Figma-side extraction).

---

## 1. The governing rule: contract, not picture

An agent given a **picture** of a component reconstructs the parts it cannot see by guessing plausible defaults. It will produce something that renders correctly and is wrong in every dimension the image did not encode: focus order, disabled semantics, content limits, announcement text, which token the color came from.

An agent given a **contract** is constrained where it matters and free where it should be.

This is why component screenshots are an input to *review*, never to *generation*.

---

## 2. Token context — seven fields per token

A token exposed as `name: value` is a lookup table, not a system. Emit at minimum:

| Field | Why the agent needs it |
|-------|------------------------|
| `name` + semantic role | so it selects by intent, not by appearance |
| `value` / type / alias / theme | resolution across themes |
| `allowed components` / `prohibited use` | prevents correct-looking misuse (using a border token as text color) |
| `accessibility constraint` | contrast pairing, minimum target, motion bound |
| `owner` / `version` / `deprecated` / `replacement` | prevents adoption of a token on its way out |
| code name / design-tool name / doc URL | keeps the three surfaces reconcilable |
| change impact / migration note | tells the agent what a change costs before it makes one |

### The raw-value ban

**Generation may select semantic tokens. Generation may not emit raw values.** When no token fits, the required output is a *gap report* — "no semantic token covers this state; proposing `<name>` with rationale" — never a hex code inlined at the call site.

This single rule converts the most common design-system regression (silent drift via literals) from an invisible one into a reviewable proposal. Detection of existing violations → `reference/token-anti-patterns.md`.

---

## 3. Component contract — eleven fields

| Field | Content |
|-------|---------|
| `purpose` | what it is for **and when not to use it** |
| `anatomy` | required and optional parts |
| `properties` | props, types, defaults, constraints |
| `states` | default / hover / focus / active / disabled / loading / error / empty |
| `behavior` | keyboard pattern, focus management, announcement, motion + reduced-motion fallback |
| `content rules` | length limits, locale expansion, prohibited phrasing, fallback |
| `tokens` | which tokens it consumes; which literals are forbidden |
| `responsive` | breakpoint behavior and reflow rules |
| `analytics` | what it emits, if anything |
| `tests` | unit, accessibility, visual regression |
| `owner` + `status` | plus known limitations and migration notes |

`states` and `behavior` are the two fields that a screenshot cannot carry and that generation therefore fabricates. If the contract is abridged, keep those two.

---

## 4. Package layout

A system handed to agents is a directory, not a document:

```
/system      principles.md, accessibility.md, content-guidelines.md, decision-priority.md
/tokens      tokens.json, token-metadata.json, migration.json
/components  component-schema.json, states.md, examples/, anti-patterns/
/patterns    pattern-contracts.md, ai-interaction-patterns.md
/tests       lint-rules.md, accessibility-tests.md, visual-baselines/
/governance  owners.md, version-policy.md, proposal-template.md, decision-history.md
```

`decision-priority.md` earns its place: it states what wins when principles collide (accessibility floor vs. brand expression vs. platform convention). Without it, an agent facing a conflict picks silently. Author it from `_common/UX_PRINCIPLE_CONFLICTS.md` — the conflict matrix supplies the pairs and the failure each one-sided win produces, and the resolution sheet supplies the fields an allocation must record. Two constraints carry over: the accessibility floor is a **Gate**, not a conflict entry, and every allocation names the alternative it rejected.

`anti-patterns/` entries describe **failure conditions**, not verdicts — "this breaks when the label wraps to two lines," not "this is bad."

---

## 5. Do not ship the whole system into context

Retrieve the minimum slice the task needs. Tag every unit on seven axes so a slice can be selected:

`domain` · `task` · `risk` · `platform` · `locale` · `status` (current / deprecated / experimental) · `authority` (required / recommended / example)

Two consequences worth stating explicitly:

- **`authority` must be visible.** An example carried at the same weight as a requirement gets imitated as if it were one.
- **Decide what leaves the building.** The package mixes publishable guidance with internal, confidential, or client-identifying material. Split before any external model call — see `_common/SECURITY.md`.

---

## 6. Keeping documentation true

Order matters; inverting steps 2 and 3 is how generated documentation drifts from the system.

1. Read structured data from the source of truth (tokens, component schema) — never from prose.
2. **Extract the diff deterministically.**
3. Let the agent draft prose *for that diff*.
4. Owner confirms breaking changes, migration, and deprecations.
5. Publish with tests run and a version attached.
6. Feed observed usage back into the next revision.

Consistency detection splits the same way: token matching, type checks, lint, and visual regression are **deterministic**; summarizing, finding similar prior issues, proposing fixes, and explaining blast radius are **generative**. Never let a model assert conformance that a checker could have proven — a model's "this matches the system" is `E0` evidence (`_common/EVIDENCE_LADDER.md`).
