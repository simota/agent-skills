# Over-Engineering Anti-Patterns

Purpose: Use this file when a target feels more elaborate than the problem it solves.

Contents:
- Ten common over-engineering patterns
- YAGNI / KISS / DRY tension and Rule of Three
- Root causes, detection signals, and prevention rules

## 10 Common Anti-Patterns

| ID | Anti-pattern | Symptom | Void question |
|----|--------------|---------|---------------|
| `OE-01` | Premature abstraction | Interface or abstract class used in one place | Is this abstraction used in 2+ real places? |
| `OE-02` | Future-proofing by speculation | Extension points that never get used | Is there a concrete near-term plan? |
| `OE-03` | Pattern worship | Factory / Strategy / Observer where an `if` would do | Is the pattern smaller than the problem? |
| `OE-04` | Homegrown framework | Custom infrastructure where a mature library exists | Why is the standard option insufficient? |
| `OE-05` | Over-configurability | Endless options and flags | Does this option actually change in practice? |
| `OE-06` | Premature optimization | Complexity added before measuring a bottleneck | Do we have performance evidence? |
| `OE-07` | Type-system maze | Deeply nested generics or conditional types | Are types improving comprehension? |
| `OE-08` | Microservice overuse | Tiny services with huge operational cost | Would a modular monolith be enough? |
| `OE-09` | DRY obsession | Coincidental similarity becomes forced coupling | Do these things change for the same reason? |
| `OE-10` | Excessive defensive programming | Internal paths full of redundant checks | Is this actually a system boundary? |
| `OE-11` | AI-generated over-elaboration | Helper, util, and adapter layers that no caller asks for | Does any concrete caller exist *today* for this generality? |
| `OE-12` | Comprehension debt | Shipped code no human on the team can fully explain | Can the original requester walk the call graph without rereading? |

## YAGNI / KISS / DRY Tension

Rules:
- Prefer `YAGNI` over speculative generality.
- Prefer `KISS` when DRY adds indirection without durable payoff.
- Use `DRY` only when duplication changes for the same reason.

### Rule of Three

```text
1st time: write the straightforward implementation
2nd time: tolerate duplication while watching the pattern
3rd time: extract or abstract if the change reason is truly shared
```

## Root Causes

1. Fear of future rework
2. Status from architectural sophistication
3. Cargo-culted best practices
4. Lack of usage or performance evidence
5. Confusing flexibility with value

## Detection Signals

| Signal | Threshold | Meaning |
|--------|-----------|---------|
| Single-use abstraction | `1` implementation | `OE-01` likely |
| Unchanged config options | `>50%` never changed | `OE-05` likely |
| Design discussion vs implementation time | `>50%` of total effort is design debate | over-design likely |
| Generics depth | `3+` nested levels | `OE-07` likely |
| Helper functions with `0` callers in the same diff | `≥1` such helper | `OE-11` likely (AI-generated speculative utility) |
| Duplicated code blocks in AI-touched files | `> 2x` baseline duplication for the repo | Comprehension Debt — review for `OE-12` |
| PRs where reviewer cannot answer "what happens if you delete this branch?" | `≥1` block per PR | `OE-12` likely — fail fast before merge |

### Empirical Backdrop (2026 evidence)

- ~`41%` of new code shipped in 2026 is AI-generated; five independent studies (Feb 2026) report AI tooling generates code `5-7x` faster than humans can build a mental model of it. Default to a YAGNI audit on every AI-authored PR.
- GitClear's longitudinal study found duplicated code blocks rose `~8x` between 2022 and 2024, with AI assistants doubling duplication while halving refactor commits — `OE-09` (DRY obsession) and `OE-11` (speculative helpers) both spike under AI authorship.
- An Anthropic internal study reports developers primarily using AI for generation scored `50%` on comprehension assessments versus `67%` for those who wrote more code manually — a `17-point` gap that held across seniority. Comprehension debt (`OE-12`) is real and load-bearing.
- Pull requests per developer rose `+20%` with AI assistance, but **incidents per PR rose `+23.5%`** — so the marginal "saved" feature is statistically a net negative once incidents are priced in.
- Unmanaged AI-generated code is reported to drive maintenance costs to `~4x` traditional levels by year two. Treat the cost-of-keeping curve as steeper than it was in pre-2024 baselines.

## Prevention Rules

- Ask for evidence before adding flexibility.
- Prefer concrete code until the third real repetition.
- Keep configuration only when the default is not enough for a meaningful share of use cases.
- Reject optimization work without measured bottlenecks.
- Review "future use" comments as subtraction candidates.

## Void Use

Use this reference to:
- flag `OE-01` to `OE-10` during `QUESTION`
- map overhead into the `Cognitive Load` dimension during `WEIGH`
- prefer `Pattern Simplification` or `Abstraction Collapse` during `SUBTRACT`

Quality gates:
- single-use abstraction -> warn on `OE-01`
- `"TODO: future use"` -> flag `OE-02`
- `3+` generic nesting levels -> consider simplification
- `50%+` unchanged config options -> consider hardcoding defaults
- AI-authored helper / adapter / interface with no caller in the same diff -> flag `OE-11`, propose deletion
- AI-authored PR where the human author cannot summarise the control flow in `< 3` sentences -> flag `OE-12`, request rewrite or shrink before merge

Sources: [Martin Fowler: YAGNI](https://martinfowler.com/bliki/Yagni.html) · [Sandi Metz: The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction) · [Joel Spolsky: Things You Should Never Do](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/) · [arXiv 2603.28592 — Debt Behind the AI Boom (2026)](https://arxiv.org/abs/2603.28592) · [GitClear AI Coding Trends 2024-2026](https://www.gitclear.com/coding_on_copilot) · [LeadDev — How AI-generated code accelerates technical debt (2026)](https://leaddev.com/technical-direction/how-ai-generated-code-accelerates-technical-debt) · [StepTo — Comprehension Debt (2026)](https://stepto.net/blog/comprehension-debt-ai-code-understanding-2026)
