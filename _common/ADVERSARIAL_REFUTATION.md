# Adversarial Refutation Protocol

> **Tier:** `orchestration` — activates from the hub, a recipe, or on engine detection. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

Cross-skill discipline for **stress-testing a high-stakes claim with a panel of independent skeptics before committing to it**. A claim survives only if it withstands a genuine attempt to refute it. The shared kernel behind `nexus[killer]` (differentiator verdict), `nexus[trim]` (removal verdict, inverse polarity), and `nexus[graft]` (Innovation Gate). Decision/review skills — `judge`, `magi`, `probe`, `omen` — import the same discipline.

**Read when:** a recipe gates a verdict on "refute ×2-3", "adversarial refutation", "must survive a skeptic panel", or an Innovation/Defensibility gate.

**Prerequisites:** `nexus/reference/verdict-gate.md` (the gate this protocol feeds) when used to decide build/no-build; `_common/MULTI_ENGINE_RECIPE.md` for cross-engine prior-diversity.

---

## 1. The panel

- **2-3 independent skeptics**, each attacking from a **distinct angle**, not three copies of the same objection. Independence is the whole point: a single reviewer rationalizes; a diverse panel surfaces failure modes redundancy can't.
- **Distribute across engines for prior-diversity** where available (e.g. claude + codex; +agy when AVAILABLE). Model-monoculture defeats the panel — the same priors produce the same blind spots. Tag each skeptic's engine in the evidence record.
- **Each skeptic is prompted to actively REFUTE** (or, in defend-polarity recipes, to actively keep — §3), from its assigned angle. A skeptic asked to "evaluate" will hedge; one asked to "kill this claim" finds the real weakness.

Typical angles (pick per domain): market/substitution ("already served by X"), demand ("users won't switch for this"), delivery ("infeasible at our scale/timeline"), dependency, security, maintenance cost.

---

## 2. The evidence-vs-novelty discipline (the load-bearing nuance)

The panel must **kill weak claims, not bold ones.** The distinction that does this work:

- **Refuted-on-evidence** — a *concrete* fact defeats the claim: a real competitor already serves it, measured demand is absent, a specific delivery blocker exists. This is a real refutation.
- **Unproven-because-new** — there is no data *because no one has built it yet*. "We have no proof it works" is the **signature of a genuine novel bet**, not grounds for rejection.

**Default-to-refuted-when-uncertain applies only to *evidence claims*** — it must **not** kill a claim merely for being ambitious or unvalidated. A claim that survives evidence-based refutation but remains unproven-because-new routes to **GO-with-flag + kill-criterion** (test it for real), never to NO-GO.

> The gate exists to stop *plausible-but-wrong* from shipping, not to enforce conservatism. Penalizing a feature for lacking proof that can only exist post-launch is the exact failure this protocol guards against.

---

## 3. Polarity (refute vs defend)

The same machinery runs in two directions; the recipe picks one:

| Polarity | Recipe | Skeptics argue | Default-when-uncertain | Survives if |
|----------|--------|----------------|------------------------|-------------|
| **Refute** | killer, graft (Innovation Gate) | "this is *not* decisive / not novel" | refuted (for evidence claims only) | majority do **not** refute-on-evidence |
| **Defend** | trim | "this feature *must stay*" | keep | majority do **not** establish must-stay-on-evidence |

**Trim's inverse rules:** skeptics argue load-bearing ("a critical cohort silently depends on this"), mandate ("compliance/contractual obligation"), entanglement ("a downstream feature breaks without it"). Majority "must-stay-on-evidence" → downgrade that target to KEEP/DEFER. **Distinguish genuinely-dead-weight from low-usage-but-load-bearing** the same way refute-polarity distinguishes evidence from novelty.

---

## 4. Verdict aggregation

- **Majority on evidence decides.** Refute-polarity: majority refuted-on-evidence → **NO-GO or Modify**; majority merely-unproven → **GO-with-flag**. Defend-polarity: majority must-stay-on-evidence → **KEEP**; otherwise the removal candidate proceeds.
- **Carry forward the survivors' failures.** Record which refutations the claim survived and which it failed, and whether any open risk is "refuted-on-evidence" vs "unproven-because-new". On a Modify loop, **carry refuted claims forward as exclusions** so the reframe does not re-derive an already-refuted option.
- **Surface, don't bury.** The verdict card states the surviving/failed refutations so the decision is auditable (feeds `nexus/reference/verdict-gate.md`).

---

## 5. Hard exclusions (never refute/remove on a panel vote alone)

- **Safety-critical code** (auth / encryption / input validation) is **excluded from removal without an explicit security review** — a skeptic panel does not authorize cutting it.
- **Confidence `< 60%`** → do not propose the destructive/irreversible action; route to "defer + gather evidence".
- **`PUBLIC_API` / `DATA` blast radius** → Ask First regardless of panel verdict.
- **A verdict flips on new evidence, never on pressure.** Objection from the author, the user, or a
  louder panel member is not a refutation — only a fact that was not in the record is. Evidence
  updates the verdict no matter who supplies it, **including the party being refuted**; unaccompanied
  objection does not. Name the triggering evidence in the verdict card, or do not flip. Instrument
  this as `answer_flip_rate` — the share of reversals carrying no new evidence — separately from the
  reversal rate overall, since a healthy panel reverses often and a sycophantic one reverses cheaply.
  [Source: Sharma et al. 2023, sycophancy under user disagreement; OpenAI 2025 GPT-4o rollback]

**Three ways over-correcting fails.** The goal is independence from pressure, not refusal to move:

- **Contrarian drift** — objecting by default, hedging every claim, second-guessing the author inside
  their own domain. Disagreement has become the posture rather than the finding.
- **Disclaimer substitution** — "the final call is yours" appended to output that already narrowed the
  options. Returning responsibility in words while removing it in substance.
- **False neutrality** — presenting two sides where the evidence is not two-sided. Declining to flip
  must not flatten a real evidence gap into a balanced-looking summary.

---

## 6. What this protocol owns vs the recipe

This protocol owns: panel composition, engine-diversity, the evidence-vs-novelty discipline, polarity, aggregation, exclusions. Each recipe keeps **only** its specialization:
- `killer` → moat-class/trajectory gate (current vs buildable-emergent) that runs *alongside* refutation; GO-with-flag semantics.
- `trim` → the essential×killer 2×2 that *selects* removal candidates before they reach the defend-panel; cohort-segmented usage thresholds.
- `graft` → the Innovation Gate's "emergence" criterion + felt-novelty (Echo) + defensibility (Compete) layered on top of refutation; "this is just a bolt-on/gimmick" as the canonical attack.
