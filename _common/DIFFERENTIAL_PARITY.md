# Differential Parity Protocol

Cross-skill discipline for **proving behavioral / observable equivalence by diffing two implementations against a shared oracle**, rather than asserting equivalence by faith. The shared kernel behind `nexus[transmute]` (cross-language rewrite), `nexus[clone]` (faithful product reproduction), `nexus[fuse]` (multi-source synthesis, selective parity), and `nexus[graft]` (concept-fidelity, the fidelity-inverse). Verification skills that compute the diff — `radar`, `attest`, `voyager`, `mint`, `pixel`, `frame` — also import this protocol.

**Read when:** authoring or executing any recipe that claims "verified by differential parity" / "parity-verified" / "differential oracle"; or designing the comparator/harness that computes it.

**Prerequisites:** `_common/TRACEABILITY.md` (AC IDs the spec-conformance oracle consumes).

---

## 1. The two non-negotiable principles

1. **Parity over faith.** Equivalence is *proven* by running both sides against the same oracle and diffing the result, never asserted because the rewrite "looks right". A recipe that ships on assertion has not done differential parity.
2. **Idiomatic re-expression, not transliteration.** Faithfulness is in the **observable result**, not the internal code. Re-expressing behavior in the target stack's idioms is correct; copying internal structure is a separate, lower bar (`judge` distinguishes faithful-result from cargo-cult-internals).

The strength of any parity claim is bounded by the strength of its oracle. **A green diff on a thin or non-deterministic oracle is false confidence, not proof.** The two gates in §3 exist to make the oracle trustworthy *before* a green diff is allowed to mean anything.

---

## 2. Oracle origin (the axis that distinguishes the recipes)

Differential parity is one discipline with one mechanism; recipes differ only in **where the oracle comes from** and **how many oracles there are**:

| Recipe | Oracle origin | Oracle count |
|--------|---------------|--------------|
| `transmute` | **Extracted from your own source** (Mint golden I/O fixtures generated from the source impl) | one |
| `clone` | **Captured by observing an external product** (screenshots / network / flow recordings — black-box) | one (a stamped baseline) |
| `fuse` | **Captured per source**, then assigned per element | **two/selective** — adopted→parity-vs-*that-source*; merged/net-new→spec-AC |
| `graft` | Donor **concept** distilled from observation; host behavior from own source | **triple** — concept-fidelity ∧ host-integrity ∧ Innovation Gate (parity is the *inverse* bar: high donor-surface resemblance is a *smell*) |
| `migrate` | Own pre-change behavior as the baseline | one (forward) |

Everything below is shared regardless of origin.

---

## 3. The two oracle-integrity gates (clear both before any diff is trusted)

### Gate A — Oracle / Baseline Adequacy (coverage)

The oracle must exercise the **full reachable surface in scope**, not just the happy path. A target can diverge wildly on an untested branch / unreached state and still pass a happy-path-only oracle.

- **Extracted oracle** (transmute/migrate): the golden corpus must hit the source's **branches, every `throw`/`error`/`panic` path, and each boundary/equivalence class**. Run the source under coverage while generating fixtures; if coverage falls short, **expand the corpus before trusting it**. Record the achieved source-coverage % in the report.
- **Captured oracle** (clone/fuse): the capture corpus must hold a reference artifact for **every screen, every reachable state (empty / loading / error / populated / auth'd-vs-anon), and every flow** in scope. The **denominator of "in scope"** is the declared inventory (research + navigation-graph crawl), not guesswork.
- **No silent omission.** A surface that was declared/discovered but not captured/covered cannot be parity-verified — either **expand the oracle** or **explicitly defer it (named)** in the report. Silently dropping it reads as "covered" when it wasn't.

**Reject** an oracle that is happy-path-only / landing-page-only. Fix it at the oracle-build phase; do not proceed to trust it.

### Gate B — Non-determinism canonicalization (the integrity backbone)

Differential comparison assumes determinism per input, but real systems emit **incidental non-determinism**: hash/map iteration order, timestamps, float ULP differences, locale, RNG, concurrency interleaving (code); anti-aliasing, font-hinting, dynamic/timestamped content, randomized feeds, A/B layouts, animation mid-frames (UI).

For **each output/dimension**, declare which aspects are **semantically significant vs incidental**, then **canonicalize the incidental on *both* sides before comparing**:
- sort order-incidental collections · pin seeds · round floats to a declared tolerance · freeze clock / locale · pin the account
- (UI) mask dynamic regions · normalize fonts/AA · disable or mid-freeze animations (verify motion separately) · compare at a declared SSIM / pixel-delta threshold

> **The failure pair this prevents (verbatim across recipes):** without canonicalization the differential either **spuriously fails** on incidental divergence or **masks real divergence** under noise. Both make the green/red signal meaningless.

**Compare the mechanism, not a frozen sample of its output.** A clone of a randomized feed is faithful when its *feed mechanism* reproduces the original's behavior — not when one frame matches byte-for-byte.

---

## 4. Comparator & harness discipline

- **Explicit, reproducible comparator per dimension — never eyeballed.** Each dimension (visual / behavioral / feature / data-API / asset, or branch/value for code) has a named comparator with a stated pass condition and threshold. "Looks about right" is not a comparator.
- **Spec-conformance is the oracle where parity is meaningless.** A merged/net-new/invented element has *no single baseline*; demanding byte-parity spuriously fails every synthesis. Hold it to **L3 acceptance criteria via `attest`** instead (`_common/TRACEABILITY.md`). Never downgrade a genuine `adopt`/parity element to spec-AC to dodge a hard diff, and never fail a `merge`/`net-new` element with a parity diff it cannot satisfy — the element's resolution dictates its oracle.
- **Emit a re-runnable parity harness.** The comparators ship as a re-runnable suite (diff suite + fixtures + coverage/feature matrix) so a later change — or a later oracle re-capture — re-verifies without re-deriving the oracle. For incremental runs, each increment's harness accretes into a growing regression suite.

---

## 5. Provenance & drift (when the oracle is a snapshot of a moving target)

For **captured** oracles (clone/fuse) the target keeps shipping while you build, so the baseline is a snapshot, not a constant.

- **Provenance stamp** — every artifact + the baseline as a whole carry: target version/build (or capture date if unversioned), capture environment/OS, browser/app version, locale, viewport/window size, pinned account/seed. A baseline without a stamp is rejected at Gate A.
- **Drift re-check** — before SHIP and at the start of any resumed run, **spot-recapture a sample and diff it against the stamped baseline**. If the target drifted beyond tolerance, **re-capture and re-establish the baseline — never silently re-tune toward a target that moved** (that yields a copy matching neither the baseline nor the current target). Re-stamp per increment.

Extracted oracles (transmute/migrate) are frozen with the source revision and need no drift re-check, but should still record the source revision they were generated from.

---

## 6. Report contract (parity section of `NEXUS_COMPLETE`)

Every parity recipe surfaces, at minimum: oracle origin + count · **adequacy** (coverage % or captured-vs-enumerated, with deferred/blocked gaps named) · **canonicalization contract** (which aspects masked/frozen vs compared raw) · per-dimension diff results vs threshold (must be empty/green for SHIP) · for captured oracles, **provenance stamp + drift status** (no-drift / re-captured / deferred) · idiom/synthesis-review verdict. Recipe-specific report names: transmute **Parity Report**, clone **Fidelity Report**, fuse **Fusion Report**, graft **Graft Report**.

---

## 7. Recipe-specific specialization (owned by each recipe's reference)

This protocol owns the shared kernel above. Each recipe keeps **only** its specialization in its own reference:
- `transmute` → the four-axis Transmutation Map (type / error / concurrency / memory) + idiom review.
- `clone` → the 5-dimension Parity Map + Stack Decision Record + mandatory provenance/drift.
- `fuse` → the **Selective-Oracle Gate** (per-element oracle from the Fusion Map) + **Coherence Gate** (one-product proof) + multi-source IP posture.
- `graft` → the **triple oracle** (concept-fidelity ∧ host-integrity regression net ∧ Innovation Gate); here high parity-vs-donor-*surface* is a failure smell, not a goal.
- `migrate` → the RESIDUE-GATE completeness proof wraps parity per batch.
