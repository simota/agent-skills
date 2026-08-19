# Recipe: `rebrand` — All-Surface Brand Propagation with Proven Completeness

**Purpose:** All-surface brand propagation with a proven-complete guarantee — migrate's RESIDUE-GATE discipline × brand-consistency rubric; old-brand decommission gated on the completeness proof. Take a **settled** brand identity (a Hallmark Charter, an existing Brand Book, or an explicit old→new mapping) and propagate it **exhaustively** across every brand touchpoint — UI, LP, docs, emails, error messages, OGP, README — where a partial rebrand is a defect, not a milestone. The Quality-Max framing: a half-applied rebrand is *worse* than no rebrand (stale logo next to new logo reads as brand damage), so the no-omission property is the deliverable.

**Read when:** Executing the `rebrand` Recipe.

---

## Invocation & preconditions

```
/nexus rebrand <brand-source>        # brand-source: Hallmark Charter, Brand Book path, or old→new mapping
/nexus rebrand                       # no source → precondition fails, route to hallmark first
```

**Precondition — a settled brand.** `rebrand` propagates; it does not decide. The entry gate requires a settled identity: name/logo direction, voice/tone rules, and token values (color/type/spacing where they change). A rebrand request **without** a settled Brand Book routes to `hallmark` first (hallmark *creates* the identity, rebrand *propagates* it — a discover→build pair). Nexus asks one question and redirects; it never invents brand values mid-sweep.

**Non-negotiable principles (inherited from `reference/migrate-recipe.md` — cited, not re-derived):**
1. **Freeze the denominator first.** INVENTORY enumerates the total brand-touchpoint surface before any edit.
2. **Prove residue, do not trust the counter.** Completeness is established by an independent re-scan that finds zero old-brand traces, looped until dry — not by the forward counter reaching M.
3. **Delete only after the proof.** DECOMMISSION of old assets/tokens is gated on ATTEST passing.

Scale: **8-20 agents, 3-6× cost.** **Confirm tier: Ask First** on big-bang strategy / 10+ files (intentional parity with migrate — a rebrand inherently touches 10+ files, so the Ask First fires **once at launch**, not per batch, and again before the destructive DECOMMISSION cut).

---

## The parity oracle — old→new brand mapping

Per `_common/DIFFERENTIAL_PARITY.md`, the sweep needs a declared oracle: here it is the **old→new brand mapping table**, frozen at INVENTORY:

| Dimension | Old signature (residue) | New target | Check type |
|-----------|------------------------|-----------|-----------|
| Visual tokens | old hex values, old font stacks, old logo files | new token values | text/grep + asset hash |
| Naming | old product/company name, old domain, old handles | new names | text/grep |
| Voice/tone | old tagline, old boilerplate copy, banned phrases | new voice rules | text + Prose judgment |
| Assets | old logo/OG images/favicons/email headers | new assets | file inventory + visual scan |
| Metadata | old OGP/JSON-LD/manifest/meta descriptions | new metadata | text/grep |

The **old signatures are the residue signatures** for the RESIDUE-GATE. Voice/tone residue is the one dimension grep alone cannot close — Prose re-reads user-facing copy for old-voice phrasing (the structural-residue analog of migrate's `case=arch`).

---

## Chain template

```
INVENTORY  (Lens[enumerate ALL brand touchpoints: UI / LP / docs / emails / error messages / OGP / README
            + configs, CI badges, store listings, transactional templates] ‖ Ripple[blast radius]
            → freeze baseline denominator { total_touchpoints, surface axes[], residue signatures }
            axes[] derived mechanically from repo-structure + asset + template scan, NOT free recall)
→ STRATEGY (Magi[strangler-fig default / big-bang] + Sherpa[per-surface batches])
   ★Ask First: big-bang / 10+ files (fires once at launch)
→ ┌─ OUTER LOOP (completeness) — repeat until RESIDUE-GATE passes ────────────────┐
  │  per batch: Muse[token swap — tokens first, never ad-hoc restyling]           │
  │           → Artisan/Prose[apply: components + copy/voice]                     │
  │           → Echo+Palette[brand-consistency rubric + a11y ≥ baseline]          │
  │           → Radar[no-regression — rebrand changes presentation, never contracts]│
  │  RESIDUE-GATE ★ (grep old tokens/names/metadata + Prose old-voice scan        │
  │                  + visual scan for old assets — 2× consecutive zero)          │
  └───────────────────────────────────────────────────────────────────────────────┘
→ ATTEST   (consistency score all surfaces = 3 + completeness proof:
            counter complete AND residue 2× zero AND all surface axes touched)
→ DECOMMISSION (old assets / old tokens / old redirects removal — GATED on ATTEST;
            Sweep[detect] → Ripple+Lens[residual refs == 0 on latest tree] → cut → Radar green)
→ Guardian (phased per-surface commits + Consistency Attestation; decommission as a SEPARATE revertible PR)
```

**Parallelism:** independent surface batches (e.g. app UI vs docs vs email templates) run concurrently under `_common/PARALLEL.md` ownership — one owner per surface, no shared mutable state; `isolation: worktree` when batches would touch overlapping trees.

**Strategy notes:** strangler-fig (default) ships surface-by-surface — acceptable **only when surfaces are audience-disjoint** (internal docs may lag the public site; two states visible to the *same* audience is the brand-damage failure this recipe exists to prevent, so audience-shared surfaces batch together). Big-bang (all surfaces, one cutover) requires the Ask First confirm.

## Phase contract

- **INVENTORY (parallel)** — Lens enumerates every brand touchpoint; the axis list (repo dirs, asset dirs, template stores, metadata files, external-facing configs) is derived mechanically from a repo-structure + asset + template scan, never free recall. Ripple maps blast radius. Output: the **frozen denominator** + the old→new mapping table (the parity oracle). Missing mapping entries are a BLOCK, not a guess.
- **STRATEGY** — Magi arbitrates strangler-fig vs big-bang (audience-disjointness rule above); Sherpa splits the surface into per-surface batches. The launch Ask First fires here.
- **OUTER LOOP (per batch)** — Muse swaps tokens first (token-level change propagates for free wherever the system is tokenized; ad-hoc styles found here are tokenized as they are touched). Artisan applies component/asset changes; Prose applies voice/copy changes. Echo + Palette score the batch against the **brand-consistency rubric** (all mapping dimensions applied, a11y ≥ baseline — a new palette that fails contrast fails the gate). Radar confirms no behavioral regression. Batch FAIL → rollback that batch, re-plan; do not advance.
- **RESIDUE-GATE** — the completeness proof, per migrate §3a (cited): (1) forward counter `rebranded == total_touchpoints`; (2) independent residue re-scan from the latest tree — grep old tokens/names/metadata, Prose re-read for old voice, visual scan for old assets — **two consecutive zero scans** before "dry"; (3) axis coverage — every surface axis touched at least once (catches the forgotten email-template tier or store listing). Any miss → schedule as a new batch, re-enter the loop. Exit vocabulary: **ACCEPT** (gate passes) · **cap-reached** (batch budget exhausted → report rebranded-so-far + the residue list; never silently stop) · **BLOCK** (mapping gap / contract conflict → escalate).
- **ATTEST** — the consistency claim: every surface scores 3 on the brand rubric AND the completeness proof holds. Evidence-bound per `reference/autonomy-quality-protocol.md` (Q9-Q11): unscanned surfaces are labeled `UNVERIFIED`, never assumed.
- **DECOMMISSION** — old logos, old token definitions, old OG images, dead redirects. Gated on ATTEST + a fresh residual-reference re-check (== 0) + announce-and-confirm before the destructive cut. Ships as a separate revertible PR.

---

## The eight contract elements

| # | Element | Contract |
|---|---------|----------|
| 1 | Termination bound | Outer completeness loop closed by the RESIDUE-GATE (counter complete + independent re-scan 2× zero + axis coverage); per-batch inner loop with rollback-on-fail. Exits: **ACCEPT** · **cap-reached** (report best-so-far + residue list) · **BLOCK**. |
| 2 | Confirm / safety gate | **Ask First** on big-bang strategy / 10+ files — fires once at launch (intentional parity with migrate), and again (announce-and-confirm) before the destructive DECOMMISSION cut. |
| 3 | Resume | **checkpoint-resume** (`rebrand resume` — frozen denominator, old→new mapping, and per-batch gate outputs persisted at batch boundaries; resumes from the last completed batch with the denominator intact). |
| 4 | Output report | Named **Consistency Attestation** — surface × rubric matrix (every touchpoint × every mapping dimension, all = 3) + zero-residue proof (final 2× zero scan output, counter, axis-coverage table + derivation source) + decommission result. |
| 5 | Failure Modes Prevented | Consolidated section below. |
| 6 | Boundaries / vs neighbors | Section below + Decision Tree. |
| 7 | Scale | **8-20 agents, 3-6× cost** (cost scales with touchpoint count; the per-surface batch split is the governor). |
| 8 | Shared-protocol refs | `_common/DIFFERENTIAL_PARITY.md` (old→new mapping = parity oracle; oracle-adequacy discipline for the axis list); `reference/migrate-recipe.md` (RESIDUE-GATE + gated DECOMMISSION — cited, not re-derived); `_common/PARALLEL.md` (batch ownership); `reference/autonomy-quality-protocol.md` (intent contract, producer ≠ verifier — Echo/Palette never author what they score, evidence-bound ATTEST). Verdict/refutation protocols: `N/A` (no verdict — the brand decision was made upstream). |

## Failure Modes Prevented

1. **Partial rebrand = brand damage** — the identity failure mode: stale logo / old voice surviving on an overlooked surface next to the new brand. The RESIDUE-GATE independent re-scan (2× zero), not the forward counter, proves no survivor.
2. **Silent surface omission** — a whole touchpoint category (email templates, error pages, store listing, OGP) never inventoried. Frozen denominator + mechanically-derived axis coverage; a missed axis re-enters the loop as a new batch.
3. **Voice residue invisible to grep** — old tone surviving in copy with no searchable string. Prose old-voice re-read is a first-class residue scan, parallel to migrate's structural-residue rule.
4. **Two brands visible to one audience** — strangler-fig batches are audience-disjoint by rule; audience-shared surfaces cut over together, or the run is big-bang (confirmed).
5. **Decommission before proof** — old assets deleted while still referenced. DECOMMISSION is gated on ATTEST + fresh residual-reference re-check + confirm; ships as a separate revertible PR.
6. **Presentation change breaking contracts** — Radar no-regression per batch; rebrand changes presentation, never behavior. A rename that alters public APIs/URLs escalates to `migrate` scope (BLOCK).
7. **Rebrand eroding the design system** — Muse token-first rule: token swap propagates systematically; ad-hoc styles are tokenized as touched, so the sweep strengthens tokenization.
8. **Prettier-but-less-accessible** — Echo/Palette gate requires a11y ≥ baseline per batch; a new palette failing contrast fails the batch.
9. **Deciding brand values mid-sweep** — the settled-brand precondition; missing mapping entries BLOCK to the user (or route to `hallmark`), never guessed.

## Boundaries

- **vs `migrate`** — migrate owns *technical* change-completeness (arch/framework/middleware/mock→prod); `rebrand` is the brand-surface specialization — same double-loop + RESIDUE-GATE + gated DECOMMISSION skeleton, but the oracle is the old→new brand mapping, residue includes voice (judgment, not grep), and the rubric is brand consistency. A rebrand whose rename changes public APIs, URLs, or package names hands that portion to `migrate`.
- **vs `hallmark`** — hallmark *creates* the brand identity (core dialogue → identity tournament → gauntlet → Brand Book); `rebrand` *propagates* a settled one. Discover→build pair: no settled Brand Book → hallmark first.
- **vs `restyle`** — restyle improves one surface's design under a direction, with **no completeness guarantee**; rebrand applies a *decided* identity everywhere, with the guarantee as the deliverable. "Make this screen match the new brand" (one surface) → restyle; "the new brand, everywhere, provably" → rebrand.
- **vs `muse` direct** — a single token change (one color, one font) → muse direct; the completeness loop is overhead below ~3 surfaces.
- **vs `growth-acceptance`** — downstream: growth-acceptance verifies brand tone + market fit *post-ship* (B.tone, G14); rebrand's Consistency Attestation is an input to it.
- **vs `marquee`** — marquee builds one flagship LP to ceiling quality; a rebrand touching the LP applies the mapping there, but "rebuild the LP at wish level under the new brand" routes to marquee after the sweep.

### Decision Tree

```
Brand change request?
├─ brand identity not yet settled (no Brand Book / no old→new mapping) → hallmark first, then rebrand
├─ one token / one asset swap → muse direct
├─ one surface brought in line with the (new) brand → restyle
├─ rename changes public APIs / URLs / package names → migrate (that portion), rebrand (presentation)
├─ settled brand, propagate across all touchpoints, omission = defect → rebrand ✓
└─ post-ship brand/market verification → growth-acceptance
```

## Add-ons

+Growth for OGP/JSON-LD/SEO metadata surfaces and redirect strategy · +Canon[legal] when the rename has legal/ToS surface (company name in policies) · +Vector/vitrine for Before/After visual-evidence capture in the Consistency Attestation · +Frame when a Figma library is a brand touchpoint (design-file side of the sweep) · +Launch for the public cutover announcement + rollback plan on big-bang runs.
