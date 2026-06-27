# Research Grounding — Evidence Research Sweep for clone / fuse / graft

> A shared **first-research** sub-phase for the reproduction-and-synthesis family (`clone`, `fuse`, `graft`). Before (and alongside) capturing a target's observable surface, run a thorough **web evidence sweep** that mines first-party docs, design specs, changelogs, API references, and authoritative write-ups, distills them into a verified, cited **Evidence Ledger**, and uses it to **raise reproduction fidelity** — without ever letting a web claim displace the captured artifact as the parity oracle.

Read this when executing `clone` Phase 0.5, `fuse` Phase 1 (per source), or `graft` Phase 1 (donor + host-domain). The recipes invoke this sweep; this file owns its contract, the Evidence Ledger schema, the trust-tier model, and the governing principle.

---

## 1. Why research first (what it buys fidelity)

Surface capture alone reproduces *what you happened to reach*. A target's own documentation, design system, changelog, and the wider web describe *what exists and why* — turning fidelity from "best effort on the screens we stumbled onto" into "grounded against a declared, cross-checked map." The sweep raises every downstream fidelity oracle:

| Fidelity lever | What the web adds | Feeds (clone / fuse / graft) |
|----------------|-------------------|------------------------------|
| **Completeness** | Docs/help-center/changelog enumerate features, flows, and reachable states you would otherwise miss (admin views, error states, rare edge cases, recently-shipped surfaces) | Capture Completeness Gate **denominator** (clone §3a) — the checklist of what *must* be captured, not a guess |
| **Exact values** | Published design tokens, brand guidelines, public Figma, API references give **exact** colors/type/spacing/field-types — not pixel-estimated or response-inferred | Visual parity precision + fidelity-tolerance contract (clone §3a) + data/contract shape (clone Parity Map) |
| **Semantics / intent** | Docs explain *why* a behavior exists and its rules → separates **significant from incidental** and seeds behavioral fixtures | Fidelity-tolerance contract + behavioral parity (clone §3c); concept **essence** distillation (graft §2) |
| **Version & drift** | Changelogs / release notes pin the exact version and reveal recently-changed or A/B-rotated surfaces | Provenance stamp + drift gate (clone §3b) |
| **Concept rationale** | Design rationale, engineering blog posts, reverse-engineering write-ups explain *how a mechanism works and why it's load-bearing* | graft Concept Catalog essence (graft §2); fuse conflict-resolution rationale (fuse §3a) |

---

## 2. Governing principle — research-first, capture-authoritative

The sweep runs **first** because it is cheap, broad, and tells capture *what to look for*. But it never outranks the captured artifact:

1. **The captured artifact (clone/fuse) or observed mechanism (graft) remains the oracle.** A web claim is a **lead to confirm by capture**, never a substitute for it. "The docs say the button is `#1A73E8`" sets an expectation; the parity baseline still records the *captured* pixel and diffs against it. Reproducing from a doc you never confirmed against the live surface is the memory-based-rebuild failure in disguise (clone §1 principle 1) — web docs are **secondary evidence**, capture is primary.
2. **Every claim is provenance-stamped, trust-tiered, and verification-tracked** (§3). Marketing copy overstates; docs lag the shipped product; community posts guess. Untracked web "facts" silently corrupt the baseline.
3. **Adversarial verification, capture wins ties.** Each load-bearing claim is cross-checked against the captured artifact and against other sources (deep-research discipline). **A claim contradicted by capture is a signal, not a correction**: it flags either a stale/aspirational doc (discard the claim, keep the capture) or genuine drift (the doc describes a version newer/older than captured → re-stamp / re-capture per clone §3b). The clone is never re-tuned toward a doc the live surface contradicts.
4. **Feeds gates, replaces none.** The Evidence Ledger supplies inputs to the *existing* integrity gates (completeness denominator, tolerance contract, provenance version, concept essence) — it does not introduce a parallel oracle or relax any gate.

---

## 3. The sweep (contract)

**Spawn:** the `deep-research` skill (the Claude Code-shipped harness: fan-out web search → fetch → adversarially verify → cited synthesis) is the primary tool **when the hub is Claude Code**. On a hub where it is unavailable (Codex CLI / agy, or `deep-research` not installed), fall back to **repo-native specialists**: `Vector` (browser crawl / fetch / network observe) + `Compete` (positioning / competitive context) + `Seek?`/`Trawl?` for retrieval scale, all driving `WebSearch`/`WebFetch`. Either path produces the same Evidence Ledger contract below; record which path ran in the report (§6). Use `+Compete` regardless for the competitive/positioning context (fuse Thesis, graft Innovation Thesis); `WebSearch`/`WebFetch` for targeted lookups. Run as a parallel branch that **completes before the Capture Completeness Gate** so its inventory can serve as that gate's denominator.

**Source targets (in trust-tier order):**

| Tier | Source | Use | Caveat |
|------|--------|-----|--------|
| **T1 — first-party authoritative** | Official docs, help center, API reference, **public design system / tokens / Figma**, changelog / release notes, status page | Feature inventory, exact values, version, documented behavior | May lag the shipped product → still verify vs capture |
| **T2 — first-party intent** | Marketing/landing pages, product tour, pricing/feature matrix, announcement blog | Feature breadth, intended positioning, naming | Describes *intent*; **overstates / shows unreleased** → low weight on exact behavior |
| **T3 — third-party authoritative** | Reputable technical write-ups, reverse-engineering posts, conference talks, well-maintained wikis | Hidden mechanisms, internals, history | Author may be wrong/outdated → corroborate |
| **T4 — community / unverified** | Forums, social posts, reviews, Q&A threads | Edge-case leads, rare states, user-observed quirks | Treat as **leads only**; never a baseline source |

**Output: the Evidence Ledger** (cited; one entry per claim):

| Field | Meaning |
|-------|---------|
| `claim` | The fidelity-relevant fact (a feature exists / an exact token value / a documented rule / a version) |
| `source_url` + `retrieved` | Citation + retrieval date (every entry is traceable; uncited claim is rejected) |
| `trust_tier` | T1–T4 (§3 table) |
| `describes_version` | The product version/build the source describes (or "undated") → cross-checked against the capture provenance stamp (clone §3b) |
| `category` | `feature-inventory` \| `exact-value` \| `behavior-semantics` \| `version-drift` \| `concept-rationale` (graft) |
| `verification` | `confirmed-by-capture` \| `contradicted-by-capture` (→ §2.3 drift/stale handling) \| `unconfirmed-lead` \| `unreachable` |

**Ledger sections (the deliverables that feed the gates):**
- **Declared inventory** — features / flows / reachable states named by T1/T2 sources → the **completeness-gate denominator**. Anything declared but never captured is an explicit coverage gap (clone §3a), not a silent omission.
- **Exact-value catalog** — published tokens, brand colors, fonts, spacing, API field types/contracts → raises visual + data parity precision; each value still confirmed against the captured artifact before it enters the baseline.
- **Behavior & semantics notes** — documented rules / edge cases / *why* → significant-vs-incidental for the tolerance contract + behavioral-fixture seeds.
- **Version & drift signals** — changelog/release data → sharpens the provenance stamp; recently-changed or A/B surfaces flagged for extra capture care.
- **Concept rationale** *(graft only)* — design/engineering rationale for *why a mechanism works and is load-bearing* → the raw material for distilling a concept to its essence (graft §2).

**Gate (Research Completeness):** before capture is trusted, the sweep must have (a) exhausted T1 first-party sources for the in-scope surface, (b) cited every load-bearing claim, and (c) marked each claim's `verification` status. A capture run that proceeds with an empty or uncited ledger forfeits the fidelity gains and is flagged in the report — the sweep is *mandatory first-research*, not optional enrichment. Scope the sweep to the reproduction scope (clone whole/area; fuse per-source adopted slice; graft the donor concept + host domain) — exhaustiveness is judged within scope, not the target's entire web footprint.

---

## 4. Per-recipe wiring

- **clone** — runs as **Phase 0.5 RESEARCH SWEEP** between FRAMING and CAPTURE. The Declared inventory becomes the Phase 2 Capture Completeness Gate denominator; the Exact-value catalog feeds the fidelity-tolerance contract (§3a) and Phase 4 pixel/data precision; Version & drift signals sharpen the provenance stamp (§3b). Capture stays artifact-authoritative.
- **fuse** — the sweep is **per source** (inherited via "fuse reuses clone per source," fuse §2), scoped to each source's *adopted slice*; plus one **fusion-level** competitive/positioning sweep that informs the Fusion Thesis and the Conflict Ledger rationale (fuse §3a). Each source's ledger is stamped to that source.
- **graft** — the **donor** sweep is weighted toward `concept-rationale` (docs/engineering write-ups explaining *why a mechanism works* are the best raw material for essence distillation, graft §2) and explicitly **resists surface reproduction** (a doc screenshot is a concept lead, not a parity target — graft rejects surface copying). A lighter **host-domain / competitive** sweep sharpens the Innovation Thesis (graft §3e). Concept-fidelity, not surface-fidelity, is the reproduction fidelity raised here.

---

## 5. Failure modes prevented

| Failure | Mitigation |
|---------|-----------|
| **Thin baseline from stumbled-onto capture** (captured only what was easy to reach) | Declared inventory (§3) supplies the completeness-gate denominator — capture is checked against a researched list, not guesswork |
| **Pixel-estimated values when exact ones are published** | Exact-value catalog pulls T1 tokens/specs; confirmed against capture before entering the baseline |
| **Doc-as-truth corruption** (rebuilt from a doc, never confirmed; doc was aspirational/stale) | §2 capture-authoritative rule + per-claim `verification` status; contradicted claims flag stale/drift, capture wins |
| **Marketing overstatement** (built a feature the landing page advertised but the product doesn't ship) | Trust tiers — T2 is low-weight on exact behavior; every claim verified against capture |
| **Stale version baked in** (doc described an old/unreleased version) | `describes_version` cross-checked vs the capture provenance stamp (clone §3b); mismatch → drift handling |
| **Uncited "facts"** (an unverifiable claim silently shapes the build) | Every ledger entry requires `source_url` + `retrieved`; uncited claim rejected |
| **Surface-leak in graft** (a donor doc screenshot pulls surface copying into a concept transplant) | graft donor sweep treats screenshots as concept leads only; surface resemblance remains a smell (graft §3b/§3d) |

## 6. Output contribution

Each recipe's final report gains a **Research Grounding** subsection: research path used (`deep-research` | repo-native Vector+Compete), ledger size + per-tier source count, the declared-vs-captured coverage delta (what research surfaced that capture confirmed / still-missing / contradicted), exact-values adopted into the baseline, and version/drift signals found. For `graft`, also the concept-rationale sources that grounded each Concept Catalog entry.
