# Nexus Newsroom Recipe Reference

> **"An article is only as true as its weakest uncited claim."**
>
> Grounded article production and audit, run like an editorial newsroom: the writer drafts, the fact-check desk verifies. Every factual claim traces to a cited, trust-tiered source; speculation, inference, and opinion are explicitly labeled or removed; wrong views are hunted by adversarial cross-checking — before the article ships, not after a reader catches it.

## Contents

- [Overview](#overview)
- [Invocation and Modes](#invocation-and-modes)
- [When to Use Newsroom](#when-to-use-newsroom)
- [Claim Taxonomy (the core contract)](#claim-taxonomy-the-core-contract)
- [Ledger Membership](#ledger-membership)
- [Phase Contracts](#phase-contracts)
- [Gates](#gates)
- [AUTORUN Chain Template](#autorun-chain-template)
- [Failure Modes Prevented](#failure-modes-prevented)
- [Cost and Scale](#cost-and-scale)
- [Boundaries — vs Neighbors](#boundaries--vs-neighbors)

---

## Overview

Newsroom is a **claim-grounding maximization recipe** for articles (blog posts, tech articles, announcements, explainers). Where `podium` maximizes content *polish* across formats (prose + visuals + slides), newsroom maximizes content **truth provenance** for a single written artifact — the editorial fact-check-desk discipline: it builds a cited **Evidence Ledger** before (or against) the text, decomposes the article into atomic claims, verifies each claim's source *actually supports it* (citation-support, not citation-existence), attacks load-bearing claims with an adversarial skeptic panel, and ships with a named **Provenance Report** in which no claim is silently unaccounted for.

**Two modes, one verification core:**

- **`compose`** (default when no existing article is supplied) — evidence-first authoring. The Evidence Sweep runs **before** writing; the writer is ledger-bound: it may assert as fact only what a ledger entry backs, and everything else must be phrased as labeled opinion/hypothesis or dropped. Verification then audits the writer's own output (producer ≠ verifier).
- **`audit`** — an existing article is the input. Phase 2 is skipped; the sweep is *claim-driven* (research what the article asserts), and the remediation loop corrects, re-cites, downgrades, or marks the text.

**Key design decisions:**
- **Evidence Ledger is the single source of truth for facts** — schema, trust tiers (T1–T4), and per-claim `verification` status are inherited from `reference/research-grounding.md` (§3), with one adaptation: newsroom has no captured artifact, so the authority rule becomes **primary-source-authoritative** — a claim's ground is its highest-tier source, cross-corroborated; T4 (community/unverified) is never a sufficient ground alone.
- **Citation-support over citation-existence** — the auditor re-opens each cited source (WebFetch) and confirms it says what the article says it says. A real URL that doesn't support the sentence is a `miscited` defect, not a pass.
- **Producer ≠ verifier** (`reference/autonomy-quality-protocol.md` Q9) — the Phase 3 claim auditor and Phase 4 skeptics are never the Phase 2 writer.
- **Wrong views are a first-class target** — Phase 4 doesn't only check "is there a source"; it hunts *incorrect-despite-cited* content: outdated best practices, deprecated APIs presented as current, misread statistics, causal claims a correlational source can't carry, and staleness relative to the publication date.
- **Transparency over cosmetic completeness** (shared with podium's hard rule) — a claim that cannot be grounded and cannot be sourced by the user ships explicitly marked `[UNVERIFIED]` or is removed *with a log entry*; it is never silently kept or silently deleted.

---

## Invocation and Modes

```
/nexus newsroom "<article goal>"              # compose mode: evidence-first article creation
/nexus newsroom audit <path-or-url>           # audit mode: verify an existing article
/nexus newsroom "<goal>" --risk external      # risk_tier override (routine | external-facing | release-critical)
```

Mode detection when unstated: an existing article path/URL/pasted text → `audit`; a topic/goal only → `compose`.

---

## When to Use Newsroom

### Use Newsroom for

- Tech articles / blog posts where factual credibility carries the piece (benchmarks, comparisons, "state of X" surveys, security write-ups)
- Announcements or explainers that make verifiable claims (statistics, version numbers, API behavior, quotes, pricing)
- Fact-checking an existing draft before external publication
- Any article where the user asks for "no speculation", "every claim sourced", or "check this is actually correct"

### Do NOT use Newsroom for

- Article authoring with no grounding requirement → `tome` direct
- Doc + slide unified package with polish maximization → `podium` (its Phase 4 claim-grounding branch covers grounding *within* that pipeline)
- Spec-vs-implementation conformance → `attest` direct
- Standards compliance (WCAG/OWASP/style) → `canon` direct
- Opinion pieces / personal essays where the value *is* the subjective take — newsroom would strip the point (still usable in `audit` mode to label facts vs opinion, if asked)
- Reproducing an external product's surface → `clone` (its Evidence Ledger serves parity, not prose)

---

## Claim Taxonomy (the core contract)

Every assertion in the article is classified into exactly one class. The classes carry different obligations:

| Class | Definition | Obligation |
|-------|-----------|------------|
| `fact` | Verifiable statement about the world (statistic, date, version, API behavior, quote, event, price, benchmark number) | MUST map to a ledger entry with trust tier T1–T3 whose source **supports the exact statement**; load-bearing facts need ≥2 independent sources (§Phase 4) |
| `inference` | Conclusion the article draws from cited facts | The supporting facts must each be grounded AND the inference step must survive the skeptic panel (a correlational source cannot carry a causal claim) |
| `opinion` | Author's judgment or preference | Explicitly attributed ("in my view", "we recommend") — never phrased as fact |
| `speculation` / `prediction` | Forward-looking or unknowable statement | Explicitly hedged and labeled; load-bearing speculation is challenged (should it be in the article at all?) |

**Claim-tolerance contract** (fixed in Phase 0): which statement kinds require a source at this risk tier. At `external-facing` and above, *every* `fact` does. At `routine`, widely-known background facts ("HTTP has status codes") may pass as `common-knowledge` — but any number, name, date, quote, or comparative/causal statement is never common-knowledge.

Per-claim audit verdicts (Phase 3/4 output vocabulary):

`grounded` | `miscited` (source exists but doesn't support the sentence) | `unsupported` (no source) | `contradicted` (a higher/equal-tier source says otherwise) | `stale` (was true; no longer true at publication date) | `mislabeled` (opinion/speculation phrased as fact)

---

## Ledger Membership

Newsroom is a member of the **external-reviewer-to-zero** family: its completion oracle is an evaluator's finding set driven to zero, not a rubric score. The shared machinery is `_common/FINDING_LEDGER.md`; the Evidence Ledger + `claim_audit.json` **are** that file's ledger, with claims as the findings. Newsroom's five declaration slots:

| Slot | newsroom |
|------|----------|
| **(a) Evaluator** | the Phase 3 claim auditor + Phase 4 skeptic panel — separately spawned, never the writer. Maker ≠ checker is bought by spawn separation and adversarial refutation rather than by a second engine (`FINDING_LEDGER.md` §2) |
| **(b) Frozen scope unit** | `newsroom_charter.yaml`, fixed at Phase 0: article ref + **claim-tolerance contract** (which statement kinds need a source at this `risk_tier` — this *is* the severity floor) + the load-bearing thesis list |
| **(c) Identity mechanism** | **assigned** — `claim_id` fixed at first decomposition and carried through rewrites. Remediation legitimately rewrites the sentence a claim lives in, so a derived fingerprint would lose the claim on the first fix (`FINDING_LEDGER.md` §4) |
| **(d) Validity gate** | **Thesis-Integrity** (§ Gates) — the load-bearing thesis still stands and is still stated after remediation |
| **(e) Invariant + profiles** | the article still makes its point. No profiles: `risk_tier` is a floor preset, `compose`/`audit` are input modes |

**C4 holds** (`FINDING_LEDGER.md` §1): the claim set is the article's own assertions — finite, and each has a right answer — so newsroom needs **no split oracle**, which is why `loop ≤ 2 cycles` suffices where `quell` needs 6. The **craft** axis of prose (structure, altitude, register, redundancy) fails C4 and is *not* in scope here; it lives in `reference/doc-quality-protocol.md` W7-W11 as a single-pass gate.

**Verdict → disposition.** A verdict is what the evaluation found; a disposition is why the claim is closed. Both appear in `claim_audit.json`.

| Verdict / outcome | Disposition |
|---|---|
| `miscited` · `unsupported` · `contradicted` · `stale` · `mislabeled` | `OPEN` |
| re-audited `grounded` after a remedy | `FIXED-VERIFIED` |
| the auditor tried to confirm the defect against the source and failed | `FALSE-POSITIVE-RATIFIED` |
| downgraded to labeled opinion (logged, re-audited as `opinion`) | `DOWNGRADED` |
| removed with a log entry | `DELETED (logged)` |
| shipped `[UNVERIFIED]` at `cap-reached` | `DEFERRED` |
| `common-knowledge` pass at `risk_tier: routine` | `BELOW-FLOOR` |
| a claim that returns to `OPEN` twice after being `FIXED-VERIFIED` | `FROZEN` + `BLOCK` (`FINDING_LEDGER.md` §7) |

`DOWNGRADED` and `DELETED (logged)` are newsroom's **self-dismissal analogue** (`FINDING_LEDGER.md` §6): weakening a claim into vacuity and deleting the inconvenient paragraph both close a finding by moving the standard rather than meeting it. That is why both are logged, both are re-audited, and a hollowed-out thesis is a `BLOCK` rather than a ship.

---

## Phase Contracts

### Phase 0: FRAMING (Nexus internal, 0-1 agents)

Detect mode (`compose` | `audit`), scope, audience, and `risk_tier`. Fix the **claim-tolerance contract** (§ taxonomy) and the article's load-bearing thesis (the 3-7 claims the piece stands on — these get the ≥2-source + skeptic-panel treatment).

**Output:** `newsroom_charter.yaml` (mode, topic/article ref, risk_tier, claim-tolerance contract, load-bearing thesis list, loop budget).

**Gate:** `risk_tier == release-critical` → **Confirm before launch** (conditional confirm — intentional parity with podium, not summit's unconditional gate).

### Phase 1: EVIDENCE SWEEP (parallel, 2-4 agents)

Build the **Evidence Ledger** per `reference/research-grounding.md` §3 (schema: `claim` / `source_url` + `retrieved` / `trust_tier` T1–T4 / `describes_version` / `category` / `verification`). Adaptation: authority is **primary-source-authoritative** (highest-tier source wins ties; no capture oracle exists here).

```yaml
parallel:
  - branch: external_grounding
    agents: [field]            # WebSearch/WebFetch sweep of T1 (official docs, papers, changelogs) → T3
    mission: exhaust T1 sources for every in-scope topic; cite + tier + date every entry
  - branch: internal_sources        # conditional: article derived from a codebase / releases
    agents: [lens | launch]
    mission: code citations, PR/release facts — internal claims get repo-path/SHA provenance, same ledger schema
  - branch: competitive_claims      # conditional: article compares products/tools
    agents: [compete]
    mission: comparison facts from each vendor's own T1 sources, never from a rival's marketing
```

In `audit` mode the sweep is **claim-driven**: a pre-pass extracts the existing article's claims (Phase 3 machinery run early, extraction only) and the sweep researches exactly those.

**Gate (Research Completeness, inherited):** T1 exhausted for in-scope topics; every ledger entry cited + dated; uncited entries rejected. Critical gaps (a load-bearing thesis has no findable source) → pause and present to the user before writing.

### Phase 2: COMPOSE (compose mode only, 1-2 agents)

`tome` writes the article **ledger-bound**: every `fact` sentence carries an inline ledger reference (`[E12]`); anything not in the ledger is written as labeled opinion/hypothesis or not written. `prose?` for headings/hook. `reference/doc-quality-protocol.md` W1-W6 apply (reader contract + UNKNOWN-over-fabrication).

In `audit` mode this phase is skipped; the existing article is ingested verbatim.

### Phase 3: CLAIM AUDIT (producer ≠ verifier, 1-2 agents)

A **separately spawned auditor** (never the writer):
1. Decomposes the article into atomic claims and classifies each per the taxonomy.
2. For every `fact`: locates its ledger entry, **re-opens the cited source** (WebFetch) and confirms citation-support — the source must state what the sentence states, at the claimed strength.
3. Flags `mislabeled` phrasing (speculation dressed as fact) and inference steps that outrun their sources.

**Output:** `claim_audit.json` — one row per claim: `{ claim_id, claim, class, ledger_ref, verdict, disposition, evidence_note, first_seen_cycle }`. **No claim may be absent from the table** — unaccounted claims fail the gate (Acceptance-Provenance discipline, Q15).

`claim_id` is **assigned at this first decomposition and never re-derived** (§ Ledger Membership slot (c)). Remediation rewrites sentences, so a claim re-extracted from the fixed text would otherwise arrive as a new row with no history — and a claim that has already been refuted once would be indistinguishable from a fresh one.

### Phase 4: ADVERSARIAL VERIFY (parallel, 2-4 agents)

Skeptic panel per `_common/ADVERSARIAL_REFUTATION.md` on the **load-bearing thesis claims** + any Phase 3 `grounded` claim the auditor marked shaky:

- Each skeptic independently tries to **refute** the claim via fresh search: contradicting T1-T3 sources, newer versions/deprecations, misread statistics (base rates, survivorship, denominator games), causal overreach.
- **Corroboration rule:** load-bearing facts require ≥2 independent sources (independent = not citing each other / not the same origin).
- **Staleness check:** every date-sensitive claim is tested against "still true at publication date?" — a 2023 benchmark presented as current is `stale`.
- Verdicts merge into `claim_audit.json` (a refuted claim's verdict is overwritten to `contradicted`/`stale` with the refuting citation attached).

### Phase 5: REMEDIATE — loop ≤ N cycles (default N=2)

Fix per verdict, generator-evaluator separated per `reference/evaluator-loop-protocol.md` (writer fixes, auditor re-verifies the diff — never self-graded):

| Verdict | Remedy |
|---------|--------|
| `miscited` | Re-cite to the source that actually supports it, or rewrite the sentence to what the source does support |
| `unsupported` | Find a T1–T3 source; else downgrade to labeled opinion, or delete (logged) |
| `contradicted` | Correct the claim to what the evidence says (never argue with the source) |
| `stale` | Update to current facts + date-stamp ("as of <date>") |
| `mislabeled` | Re-phrase with explicit attribution/hedging |

The writer **states the `claim_id` it acted on** for every remedy, so the re-audit re-attaches the claim's verdict history instead of re-discovering it (Phase 3). A claim returning to `OPEN` twice after a `FIXED-VERIFIED` is `FROZEN` + `BLOCK`, never a third attempt.

Re-run Phase 3 on changed text only, then the **Thesis-Integrity gate** (§ Gates). **Exit reasons:** `ACCEPT` (zero unresolved `fact` verdicts **and** the thesis gate green) | `cap-reached` (deliver best-so-far with residual claims explicitly marked `[UNVERIFIED]` + the residual gap listed) | `BLOCK` (a load-bearing thesis is refuted and the article's premise fails → escalate to the user; do not ship a corrected-into-meaninglessness piece).

### Phase 6: DELIVER

`NEXUS_COMPLETE` with `## Nexus Execution Report` plus the named **Provenance Report**:

```markdown
### Provenance Report
- Mode: compose | audit          Risk tier: <tier>
- Evidence Ledger: N entries (T1: n / T2: n / T3: n / T4-leads: n)
- Claims: N total — fact n / inference n / opinion n / speculation n
- Verdicts: grounded n · miscited→fixed n · unsupported→(sourced n / downgraded n / deleted n) · contradicted→corrected n · stale→updated n
- Load-bearing thesis: each claim + its ≥2 independent sources + skeptic verdict
- Dispositions: every claim carries exactly one (§ Ledger Membership); `DOWNGRADED` / `DELETED (logged)` / `FROZEN` listed individually with the ratifying auditor
- Thesis-Integrity gate: result per cycle
- Residuals: [UNVERIFIED] claims shipped (0 required for external-facing) + deletions log
- Loop: N/2 cycles, exit reason
```

---

## Gates

| Gate | Phase | Rule |
|------|-------|------|
| **Confirm-before-launch** | 0 | `risk_tier == release-critical` (conditional — intentional parity with podium) |
| **Research Completeness** | 1 | T1 exhausted in scope; all entries cited + dated; critical thesis gap → pause to user |
| **Zero-Ungrounded** | 3→6 | `external-facing`+: zero unresolved `fact` claims; every claim present in the audit table (none silent) |
| **Citation-Support** | 3 | Cited source re-opened and confirmed to state the claim — URL existence is not support |
| **Corroboration** | 4 | Load-bearing facts: ≥2 independent T1–T3 sources |
| **Never-silent** | 5-6 | Unresolvable → `[UNVERIFIED]` marker or logged deletion; silent keep and silent delete both forbidden |
| **Thesis-Integrity** (validity gate) | 5, **every cycle** | After each remediation cycle: every load-bearing thesis claim is **still present in the text and still supported**. A cycle that hollowed one out — downgraded it to opinion, deleted it, or hedged it into vacuity — **injects a blocking finding into the audit table** for the next cycle rather than warning (`_common/FINDING_LEDGER.md` §10). This is the per-cycle form of the `BLOCK` exit: the exit catches a thesis the *evidence* refuted, this gate catches a thesis the *remediation* dissolved |

**Resume:** checkpoint-resume — recipes with ≥ 4 phases persist phase outputs at each boundary (ledger, `claim_audit.json`, remediation diffs), so an interrupted run resumes from the last checkpoint (`newsroom resume`).

---

## AUTORUN Chain Template

```yaml
recipe: newsroom
mode: AUTORUN_FULL
required_confirmation: only risk_tier == release-critical
phase_chain:
  - { phase: 0_framing,   owner: nexus_internal, gate: release_critical_confirm }
  - { phase: 1_evidence,  parallel: [field, lens|launch?, compete?], gate: research_completeness }
  - { phase: 2_compose,   agents: [tome, prose?], if: mode == compose }   # ledger-bound writing
  - { phase: 3_claim_audit, agents: [auditor(spawned, != writer)], output: claim_audit.json }
  - { phase: 4_adversarial, parallel: [skeptic ×2-3 per _common/ADVERSARIAL_REFUTATION.md, staleness_check] }
  - { phase: 5_remediate, loop: "≤ 2 cycles", gate: thesis_integrity, exit: [ACCEPT, cap-reached, BLOCK] }
  - { phase: 6_deliver,   output: NEXUS_COMPLETE + Provenance Report }
```

---

## Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Plausible-but-invented "facts"** (fluent prose, no source) | Ledger-bound composition — a fact not in the Evidence Ledger cannot be written as fact |
| **Citation laundering** (URL attached, source says something else) | Phase 3 citation-support re-open: the auditor fetches and reads every cited source |
| **Self-graded verification** (writer approves its own claims) | Producer ≠ verifier (Q9): auditor and skeptics are separate spawns from the writer |
| **Wrong-despite-cited views** (deprecated API taught as current, misread statistic) | Phase 4 skeptic panel refutes with fresh search; staleness check against publication date |
| **Single-source fragility** (thesis rests on one blog post) | Corroboration rule: load-bearing facts need ≥2 independent T1–T3 sources; T4 never sufficient alone |
| **Causal overreach** (correlational source, causal sentence) | `inference` class audited separately — the step, not just the inputs, must survive refutation |
| **Speculation dressed as fact** | `mislabeled` verdict + mandatory hedged re-phrasing |
| **Silent claim loss** (an inconvenient claim quietly deleted, or quietly kept) | Never-silent gate: `[UNVERIFIED]` markers + deletions log; every claim appears in the audit table |
| **Fixing into meaninglessness** (corrections hollow out a refuted premise) | `BLOCK` exit: a refuted load-bearing thesis escalates to the user instead of shipping a gutted article |

---

## Cost and Scale

**Scale:** 6-16 agents × ≤2 remediation cycles; 20-60 min; **2-5× a `feature` chain** (compose mode upper range; audit of a short article sits at the bottom). Roughly half of podium (16-53 agents) — newsroom has no visual/layout/slide tracks.

| Scenario | Agents | Cost |
|----------|--------|------|
| `audit` of one article, no loop | 6-9 | 2-3× |
| `compose`, one loop | 9-13 | 3-4× |
| `compose`, 2 loops + wide sweep | 12-16 | 4-5× |

---

## Boundaries — vs Neighbors

- **vs `podium`** — podium is the *package polish* recipe (doc + slides + visuals, five teams); its claim-grounding is one verification branch. Newsroom inverts the weighting: grounding IS the deliverable's core guarantee, polish is incidental. An article that also needs a slide deck and hero imagery → podium (optionally with newsroom-grade rigor requested); an article whose selling point is "every claim checked" → newsroom.
- **vs `tome` direct** — Tome authors without Newsroom's Evidence Ledger, independent auditor, or refutation loop. Article with no grounding requirement → Tome direct.
- **vs `attest`** — attest verifies implementation against a *normative spec* (AC conformance). Newsroom verifies prose against *the world* (external sources).
- **vs `canon`** — canon checks compliance with named standards (WCAG/OWASP/style guides); newsroom checks factual truth provenance.
- **vs `clone`/`fuse`/`graft` research sweep** — same Evidence Ledger machinery (`reference/research-grounding.md`), different oracle: reproduction recipes stay capture-authoritative; newsroom is primary-source-authoritative because there is no artifact to capture.
- **vs `wish`/`marquee`** — ceiling-quality one-shot wrappers; newsroom is a repeatable grounding pipeline with a standard bar (zero ungrounded facts), not a scarcity-gated ceiling.

### Decision tree

```
Is the deliverable prose that makes factual claims?
  └─ NO  → not newsroom (code → judge/acceptance; spec conformance → attest)
  └─ YES ↓
Does it need slides/visuals/multi-format packaging as the main ask?
  └─ YES → podium (grounding runs as its Phase 4 branch)
  └─ NO ↓
Is "every claim sourced / no speculation / verify correctness" part of the ask
  (or the artifact is external-facing with verifiable claims)?
  └─ NO  → tome direct
  └─ YES → newsroom  (existing draft → newsroom audit; new article → newsroom compose)
```

**Shared protocols cited (not re-derived):** `_common/FINDING_LEDGER.md` (the ledger machinery this recipe is a member of — scope freeze, identity across cycles, disposition vocabulary + integrity, oscillation, ZERO predicate, validity-gate requirement; newsroom declares its five slots in § Ledger Membership) · `reference/research-grounding.md` (Evidence Ledger schema, trust tiers, Research Completeness gate) · `_common/ADVERSARIAL_REFUTATION.md` (skeptic panel discipline) · `reference/evaluator-loop-protocol.md` (generator-evaluator separation, single termination oracle) · `reference/autonomy-quality-protocol.md` (Q9 producer≠verifier, Q10-Q11 evidence-bound claims, Q15 Acceptance Provenance) · `reference/doc-quality-protocol.md` (W4-W6 grounding / UNKNOWN-over-fabrication, W12 Doc Quality Gate — newsroom's Phase 3-4 gates subsume W12 and add citation-support + corroboration).
