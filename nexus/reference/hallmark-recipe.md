# Hallmark Recipe — Brand Identity Package Quality-Max

> `/nexus hallmark "<scope>"` — Brand identity package quality-max — brand-core dialogue → identity tournament → persona-resonance + adversarial gauntlet → proof-carrying Brand Book + design tokens. The Quality-Max member that *creates* a product/org brand identity as a verified artifact: where `growth-acceptance` verifies brand tone at ship time (G14), `hallmark` builds the identity those checks verify against. Mostly no code (token definitions only).

Read this file before executing the `hallmark` Recipe.

---

## 1. Nature / When to Use / Boundaries

**Hallmark is a proof-carrying brand construction recipe, not a document generator.** Its identity comes from three things no sibling carries together:

1. **Brand Core dialogue** — a contract-level dialogue (spec-tier) excavates values, voice, personality, and explicit prohibitions before any visual work starts. An identity built on an unratified core is decoration, not brand.
2. **Persona-resonance + differentiation gauntlet** — the identity must survive (a) a persona panel that reacts to it as the real audience would, and (b) an adversarial refutation panel whose central attack is the **logo-swap test**: "does this identity still hold if a competitor's logo is swapped in?" An identity that survives the swap is interchangeable — refuted.
3. **Proof-carrying Brand Book** — the deliverable is a Brand Book + design tokens + application guide whose every load-bearing claim traces to a ratified dialogue decision or a gauntlet verdict, gated by the Doc Quality Gate.

### Use `hallmark` for

- Building a product/org brand identity from scratch (naming direction, values, voice, visual identity, tokens).
- Overhauling an existing identity where the *core* is in question, not just the surfaces.
- Producing the brand source-of-truth that downstream recipes consume: `rebrand` (propagation), `marquee` (acquisition LP), `growth-acceptance` (Brand Compiler input).

### Not this — route to

| Not this | Route to | Why |
|----------|----------|-----|
| Propagate an already-decided brand across all surfaces | `rebrand` | Hallmark *creates*; rebrand *propagates* with a completeness proof — a discover→build pair |
| Ship-time brand-tone verification on a launch | `growth-acceptance` | Layer C verifies B.tone against an existing identity; hallmark is its upstream |
| Engineer personal branding (GitHub/LinkedIn/blog) | `compete[brand]` | Person, not product/org |
| A document package with no verification gates | `package` | Hallmark's gauntlet + Doc Quality Gate are the point |
| One design direction or one token set, minimum chain | `vision` / `muse` direct | Single-agent work with clear ownership |
| The flagship landing page that *uses* the brand | `marquee` | Marquee consumes the Brand Book; hallmark produces it |

**Scale: 10-24 agents, 3-8× cost.** Mostly no code (token definitions only). Per-phase: P1 ≈ 3-4 · P2 ≈ 2 (dialogue-heavy, agent-light) · P3 ≈ 6-9 (3 directions × identity crafts) · P4 ≈ 5-8 (persona panel + refutation panel + Canon) · P5 ≈ 2-3.

**Model selection (Plan-and-Execute):** Phase 2 Brand Core dialogue and the Phase 4 refutation verdicts are judgment-heavy → plan-tier (opus / Fable 5). Phase 3 identity generators and Phase 4 persona panelists → Sonnet 5 default, per SKILL.md § Core Contract.

---

## 2. Termination Bound

The Phase 4 gauntlet is a **loop ≤ N cycles (default N=2)**: each cycle re-crafts the identity against surviving attacks and re-runs the panels. Exit reasons use the canonical vocabulary:

| Exit reason | Hallmark-specific meaning |
|-------------|---------------------------|
| `ACCEPT` | persona-resonance panel positive on every persona AND refutation panel surviving attacks = 0 (logo-swap attack killed) AND Canon accessibility checks pass |
| `diminishing-returns (Δ < ε)` | surviving-attack count did not decrease between cycles; report as plateau with every open attack listed |
| `cap-reached` | 2 cycles without full ACCEPT |
| `BLOCK` | a core-level contradiction surfaces (identity cannot satisfy the ratified Brand Core) — escalate to the user; may re-enter Phase 2 |

On any non-`ACCEPT` exit the recipe reports best-so-far + the residual gap — never silently stops. Phases 0-3 and 5 are non-looping (`N/A`).

## 3. Confirm / Safety Gate

- **Phase 0 Scope Gate: Confirm before launch** — classify the ask as new-identity / full-rebrand-core / partial-refresh, surface the cost envelope and the downstream consumers (`rebrand`, `marquee`, `growth-acceptance`) so the user knows what this artifact feeds.
- **Phase 2 Brand Core: contract-level dialogue; AUTORUN cannot skip** (per `reference/dialogue-protocol.md` — same tier as `spec` dialogue). Values, voice, and prohibitions are user decisions, never inferred silently.
- **Phase 5 sign-off:** the Brand Book is presented for explicit ratification before it is written as the locked source of truth (it will govern every downstream surface).
- Standard Ask First tiers apply unchanged (hallmark rarely trips them — no destructive actions, minimal code).

## 4. Resume

**Draft-resume** (`hallmark resume` — spec-style: the dialogue draft + identity drafts are the state). State persists incrementally to `docs/brand/<slug>.draft.md`: Phase 1 findings → Discovery section; Phase 2 ratified core + Assumption Ledger delta at each checkpoint; Phase 3 the three direction candidates + tournament verdict; Phase 4 per-cycle surviving-attack ledger; Phase 5 promotes the draft to the locked `docs/brand/<slug>.md` + token files. A current-phase marker lets `hallmark resume` re-enter at the last checkpoint, summarizing decisions-so-far in 3-5 lines — never silently restarting from Discovery.

---

## 5. Phase Contract (AUTORUN chain template)

```
Phase 0  SCOPE GATE ★Confirm-before-launch
         Nexus[classify: new / rebrand-core / partial-refresh + cost + downstream consumers]
   ▼
Phase 1  DISCOVER ‖
         Compete[positioning + LLM brand visibility] ‖ Field/Voice[user perception — how the
         brand is actually heard today] ‖ Lens[existing asset inventory: logos, palettes,
         voice fragments, token files]
         → Discovery Digest (position, perception gaps, reusable assets)
   ▼
Phase 2  BRAND CORE ★contract-level dialogue (AUTORUN cannot skip; plan-tier model)
         Magi+Prose drive per reference/dialogue-protocol.md: values (3-5, ranked) · voice
         (register, vocabulary, tone anchors) · personality · explicit prohibitions
         ("never says / never looks like") · audience personas ratified
         → Brand Core Contract (every element elicited/ratified, Assumption Ledger for gaps)
   ▼
Phase 3  IDENTITY TOURNAMENT ‖ 3 directions from angles surfaced in the dialogue
         each: Vision[direction] → Muse[tokenize: color/type/spacing] + Ink[icon policy]
         + Builder[image]?[key visual] — token-first so every direction is application-ready
         → judge panel scores vs the Brand Core Contract → winner + salvage list
   ▼
Phase 4  GAUNTLET loop ≤ 2 cycles (default 2)
         ‖ Cast+Echo[demand]+Echo persona-resonance panel (each ratified persona reacts: trust,
           recall, emotional read — misresonance = attack)
         ‖ refutation panel per _common/ADVERSARIAL_REFUTATION.md — central attack is the
           logo-swap test: "swap in a competitor's logo; does the identity still hold?"
           surviving = interchangeable = refuted; plus core-contradiction and
           prohibition-violation attacks
         ‖ Canon[accessibility: palette contrast (WCAG), legibility at scale]
         exit per §2 (ACCEPT | diminishing-returns | cap-reached | BLOCK→Phase 2)
   ▼
Phase 5  COMPILE + DELIVER
         Prose+Scribe compile Brand Book (core, voice guide with do/don't pairs, visual
         identity, application guide) + Muse emits design tokens
         → Doc Quality Gate per reference/doc-quality-protocol.md (W1-W12; single source
           of truth — the Book may not contradict the tokens)
         → ★user ratification → lock docs/brand/<slug>.md + tokens
         → Hallmark Charter emitted; handoff recommendations (rebrand / marquee /
           growth-acceptance Brand Compiler) recorded, not executed
```

## 6. Output Report — **Hallmark Charter** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **Brand Core Contract recap** — values, voice, prohibitions, personas; each element's provenance (elicited / ratified / parked — none silent)
- **Tournament verdict** — 3 directions, per-direction scores vs the core, winner rationale + salvage applied
- **Gauntlet ledger** — persona-resonance results per persona; refutations raised / killed / survived (logo-swap verdict called out explicitly); Canon accessibility results
- **Exit reason** (§2 vocabulary) + residual gap (empty only on ACCEPT)
- **Deliverable manifest** — Brand Book path, token files, application guide
- **Downstream handoffs** — recommended next recipes (`rebrand`, `marquee`, `growth-acceptance`) with what each consumes

## 7. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| Interchangeable-with-competitor identity | Logo-swap refutation is the gauntlet's central attack (Phase 4) |
| Visual identity built on an unratified core | Phase 2 contract-level dialogue blocks Phase 3 until the core is ratified |
| Identity the actual audience doesn't resonate with | Cast+Echo[demand]+Echo persona panel uses the personas ratified in Phase 2, not invented ones |
| Inaccessible brand palette shipped as law | Canon WCAG contrast + legibility checks are an ACCEPT precondition (Phase 4) |
| Brand book that contradicts its own tokens | Doc Quality Gate single-source-of-truth check (Phase 5, W7-W9) |
| First-idea anchoring on one aesthetic | Tournament: 3 directions from dialogue-derived angles + salvage (Phase 3) |
| Prohibitions eroding under iteration | Prohibition-violation is a standing attack class in every gauntlet cycle |
| Silent assumptions inside a locked brand | Assumption Ledger (dialogue protocol D9) + provenance recap in the Charter |
| Unbounded polish of a subjective artifact | loop ≤ 2 cycles + plateau exit with open attacks listed (§2) |
| Brand created then never applied consistently | Charter records explicit downstream handoffs; tokens are application-ready by construction (token-first Phase 3) |

## 8. Shared-Protocol References

| Protocol | What hallmark takes from it | Hallmark-specific specialization |
|----------|----------------------------|----------------------------------|
| `reference/dialogue-protocol.md` | Question craft, Assumption Ledger, checkpoint presentation, Provenance Gate | Brand Core elements (values / voice / prohibitions) as the elicitation targets; prohibitions must be explicit, never inferred |
| `_common/ADVERSARIAL_REFUTATION.md` | Skeptic panel, polarity, exclusions | Target claim = "this identity is distinct and true to the core"; logo-swap test as the canonical differentiation attack |
| `reference/doc-quality-protocol.md` | W1-W12 for the Brand Book | Single-source-of-truth check extended to Book↔tokens consistency |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation for the gauntlet loop | Evaluators = persona panel + refutation panel + Canon; identity generators excluded |
| `reference/autonomy-quality-protocol.md` | Intent contract (Q1-Q3), producer ≠ verifier (Q9), Acceptance Provenance (Q15) | Q15 applied to Brand Core elements, not code ACs |

## 9. Decision Tree vs Neighbors

```
Is the ask about a brand/identity (values, voice, look) rather than a feature/surface?
  NO  → the natural recipe for the task shape
  YES ↓
Does a ratified brand identity already exist, and the ask is applying it everywhere?
  YES → rebrand (propagation with completeness proof)
  NO ↓
Is it a person's professional brand (GitHub/LinkedIn/blog/conference)?
  YES → compete[brand]
  NO ↓
Is it one bounded design decision (a direction, a token set) with clear ownership?
  YES → vision / muse direct (minimum viable chain)
  NO ↓
Is the deliverable a conversion surface that consumes a brand (flagship LP)?
  YES → marquee (hallmark first if no Brand Book exists)
  NO  → hallmark — discover → core dialogue → tournament → gauntlet → Brand Book
```
