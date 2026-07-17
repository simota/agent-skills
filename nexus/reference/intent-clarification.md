# Intent Clarification (absorbed from Cipher)

**Purpose:** Interpretation method for ambiguous user requests.
**Read when:** The request is vague and routing depends on resolving intent first.
**See also:** After resolving intent, see `routing-explanation.md` for how to present the chosen chain (and alternatives) back to the user.

Methodology for decoding ambiguous user intent before agent routing. Previously a standalone agent (Cipher), now integrated as a Nexus capability.

---

## The Three Laws

1. **No Interpretation Without Context**: git log → .agents/PROJECT.md → conversation history. Context reveals intent. Words are noise.
2. **Ambiguity is Sin, Over-Questioning Also Sin**: Context clear → Proceed. 2+ valid paths → Ask. Safe default → Proceed. Don't block flow.
3. **Never Hide Assumptions**: Always state "I interpreted this as..." "I'm assuming that..." Hidden assumptions are time bombs.

---

## Process: GATHER → READ → DECIDE → OUTPUT

| Phase | Actions |
|-------|---------|
| **GATHER** | git log · .agents/PROJECT.md · conversation history · resolve pronouns ("it", "that", "this") |
| **READ** | Interpret tone, scope, urgency (see patterns below) |
| **DECIDE** | Single interpretation → Proceed · Multiple valid → Ask · Safe default → Proceed |
| **OUTPUT** | Structured clarification with assumptions documented |

---

## Tone & Scope Interpretation Patterns

| Signal | Interpretation | Action |
|--------|---------------|--------|
| "Fix this" / "Please fix it" | Bug fix, specific target | Check git diff/status for context |
| "Improve" / "Enhance it" | Enhancement, broad scope | Narrow scope via recent activity |
| "Something is wrong" | Vague bug report | Investigate before interpreting |
| "Make it better" | Quality improvement | Check recent Judge feedback |
| Frustrated tone | User wants action, not questions | Use safest default, proceed — **but never in place of a GATE-mandated question** (see Precedence rule below) |
| Technical terms used | User knows domain | Match precision level |
| Vague keywords | Scope ambiguity | Check .agents/PROJECT.md context |

**Precedence rule (tone vs GATE):** frustrated tone changes *how much* is asked, never *whether* something is asked. When GATE fires (`context_confidence < 0.60` OR 2+ valid interpretations — see `routing-matrix.md` § Classify Flow), a frustrated tone **COMPRESSES the ask to exactly ONE focused clarifying question** (tightest possible framing, safest-default options pre-filled) — it never authorizes proceeding with **zero** questions on a sub-floor classification. "Use safest default, proceed" applies only when GATE has *not* fired (confidence ≥ floor, single valid interpretation); it is not a tone-based override of the confidence floor itself.

### Scope Detection

| Keyword | Likely Scope | Example |
|---------|-------------|---------|
| "the button" / "this component" | Minimal (1 file) | Specific element fix |
| "the auth flow" / "login" | Moderate (feature) | Feature-level change |
| "the whole app" / "overall" | Extensive (system) | System-wide concern |
| "everything" / "all of it" | Over-scope → narrow down | Ask one clarifying question |

---

## CIPHER_GATE Integration

The following rules apply as an internal Nexus capability (previously the Cipher integration protocol):

- Trigger: context_confidence < 0.60, multiple valid interpretations, or missing critical context
- Auto-clarification: Nexus attempts to resolve using gathered context
- Single question: If still ambiguous, ask ONE focused question with options
- Confidence boost: +0.20 on successful clarification

When the blocker is **missing context** (not just ambiguous wording), run the Context Sufficiency
Gate (`_common/CONTEXT_SUFFICIENCY.md`): inventory which context dimensions the outcome needs
(GOAL / SCOPE / ACCEPTANCE / INPUTS / CONSTRAINTS / ENVIRONMENT / INTERFACES / AUDIENCE / PRIOR_ART /
RISK), retrieve the inferable ones first (Law 1 — git → PROJECT.md → conversation), and batch only the
irreducibly-missing blocking dimensions into a single option-driven question. This makes the one
allowed question *comprehensive and targeted* ("give me X, Y, Z") rather than a vague re-ask. The
"one question max" rule (Law 2) means one AskUserQuestion turn — it may batch up to 4 dimensions.

---

## Overloaded-Anchor REDIRECT (recipe ambiguity)

Some English anchors map cleanly to one recipe; these do **not** — the same word fits 2+ recipes, so a bare keyword match would mis-route. When the input's main anchor is one of these AND context (Law 1) does not already disambiguate, run the classify **REDIRECT** as a single option-driven question (Law 2) before selecting a Recipe. Pick the option from the family axis in SKILL.md `### Recipe Families`.

**Option-count discipline:** a single REDIRECT question presents **at most 4 options**. When a row's candidate set is larger (e.g. the `audit`/`review`/`check` row), first eliminate candidates that context (Law 1) already rules out; if more than 4 still remain, ask a two-tier question — one broad-category pick first (e.g. "code quality / security / compliance / other"), then at most one narrow follow-up within the chosen category. This mirrors the Context Sufficiency Gate's ≤4-dimension batching bound; never present a 6-7-branch single question.

| Overloaded anchor | Candidate recipes | The one question (options) |
|-------------------|-------------------|----------------------------|
| `improve` / `polish` / `enhance` / `refine` / `make it better` / `evolve` / `deepen a feature` | `delve` · `kaizen` · `optimize` · `refactor` · `restyle` · `converge` | "Execute an improvement, or first *discover* what to even do? — **`delve`** (deep-dive a shipped feature → insights + evolution directions, **no code**) when the direction is unsettled; else perf only (`optimize`) / internal cleanup, no behavior change (`refactor`) / multi-axis polish vs a target (`kaizen`) / UI-visual-interaction design of an existing surface (`restyle`) / iterate to a quality rubric (`converge`)" |
| `improve the design` / `design improvement` | `anneal` · `restyle` | "Improve *what* design? — code/architecture design (`anneal`: discover undiagnosed design weaknesses → behavior-preserving brush-up) / UI visual/look-and-feel design of an existing surface (`restyle`)" |
| `audit` / `review` / `check` | legacy quality review · `security` (Sentinel) · `SUPPLY_CHAIN_AUDIT` (Chain) · `DESIGN_AUDIT` (Pixel) · `COMPLIANCE` (Oath) · red-team (Breach) · `AI_FEATURE` (Oracle+Sentinel) | "Audit for *what*? — code quality / security vulns / skill-MCP supply chain / design-a11y / regulatory compliance / adversarial AI/LLM red-team (prompt injection, jailbreak, misuse scenarios) / AI feature safety (prompt+output review)" |
| `differential parity` | `transmute` · `clone` · `migrate` · `fuse` | "Parity against what? — your own source rewritten in another language (`transmute`) / an external product you're copying (`clone`) / your own system you're changing completely (`migrate`) / ≥2 sources synthesized (`fuse`)" |
| `build` / `implement` (broad) | `feature` · `apex` | "Single guided build (`feature`) or autonomous discovery→ship (`apex`)?" — default `feature` unless 'whole thing / end-to-end' |
| `migrate` (broad) | `migrate` · `transmute` · `PORTING` · `refactor` · `MODERNIZE` (Shift) | "Same-system change-completeness across arch/framework/middleware (`migrate`) / cross-language rewrite (`transmute`) / web→native (`PORTING`) / one known internal restructure, no behavior change (`refactor`) / same-language library swap or deprecated-API replacement (`MODERNIZE` — Shift)?" |
| `combine` / `merge` / `mix in` | `fuse` · `graft` | "Synthesize ≥2 products' surfaces into one (`fuse`) or transplant another product's *concept* onto your own (`graft`)?" |
| `define what we build` / `nail down` | `spec` · `essential` · `charter` | "Refine one feature into a locked spec via dialogue (`spec`) / decide which ONE feature (`essential`) / whole-repo team plan (`charter`)?" |

After redirecting, state the interpretation per Law 3 ("I routed this to `<recipe>` because …").

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Better |
|-------------|---------------|--------|
| Asking what user already said | Wastes trust | Re-read conversation |
| Multiple questions in sequence | Blocks flow | One question max |
| "What do you mean?" (open-ended) | Too vague | Offer specific options |
| Interpreting without any context | Guessing | Always gather first |
| Assuming domain expertise | May confuse user | Match user's language level |

---

## Learning Loop

Record interpretation patterns in `.agents/nexus.md`:

```yaml
vocabulary_corrections:
  - phrase: "[User's phrase]"
    means: "[Actual meaning in this project]"
    context: "[When this applies]"
```
