# PDM Framework Reference

**Purpose:** Phase-by-phase workflow, status taxonomy, and the navigator Q&A loop.
**Read when:** You need LOCATE→INVENTORY→RECONCILE→ROLLUP→REPORT detail, the status states, or the `ask` loop.

## Contents
- Status Taxonomy
- LOCATE Phase
- INVENTORY Phase
- RECONCILE Phase
- ROLLUP Phase
- REPORT Phase
- Navigator Q&A Loop (`ask`)
- Worked Example

---

## Status Taxonomy

Every feature reconciled by PDM resolves to exactly one status, plus a confidence level.

| Status | Definition | Evidence required |
|--------|------------|-------------------|
| `Done` | Planned AND fully implemented | Spec/issue ref + code `file:line` covering the scope |
| `In-Progress` | Planned, partially implemented | Spec/issue ref + partial code + stated missing pieces |
| `Not-Started` | Planned, no implementation found | Spec/issue ref + search coverage proving absence |
| `Undocumented` | Implemented but not in any plan source | Code `file:line` + confirmation no spec/issue covers it |

Confidence:
- **High** — both sides directly verified (artifact text + code read).
- **Medium** — one side strong, the other inferred (e.g. spec clear, code presence inferred from a single entry point).
- **Low** — intent-only or static-only; e.g. roadmap line with no spec detail, or code presence without confirmed behavior. Always downgrade and say why.

---

## LOCATE Phase

Find both sides before reconciling. Confirm with the user if a planning side is entirely absent (Ask First boundary).

```yaml
SCOPE_SOURCES:
  plan_side:
    specs: ["docs/**/*.md", "PRD", "SRS", "spec/"]      # via Scribe/Scribe[unified] if available
    issues: ["gh issue list", "labels", "milestones", "projects"]
    roadmap: ["ROADMAP.md", "roadmap/", "milestone descriptions"]
    changelog: ["CHANGELOG.md", "releases"]
    decisions: ["ADR/", "docs/adr/"]
  code_side:
    entry_points: ["routes", "CLI commands", "feature flags", "modules"]
    tests: ["test/spec describe-blocks as feature signals"]
    flags: ["feature-flag config as in-progress signal"]
```

Detail and commands → `reference/source-triangulation.md`.

---

## INVENTORY Phase

Build the implemented-feature catalog. Prefer a Lens handoff (`LENS_TO_PDM_HANDOFF`) when deep comprehension is needed; otherwise do a lightweight feature survey.

```yaml
FEATURE_INVENTORY:
  - feature: "User login"
    area: "Auth"
    evidence:
      - "src/routes/auth.ts:15 (POST /api/auth/login)"
      - "src/services/authService.ts:28"
    signals: ["route present", "tests present", "no feature flag"]
    inferred_status: Done   # provisional; finalized in RECONCILE
```

Rule: each feature gets at least one code `file:line`. A feature with no code evidence is a candidate `Not-Started` or `Undocumented` — resolved against the plan side in RECONCILE.

---

## RECONCILE Phase

The core judgment. Match plan items to inventory items and assign status + confidence. This is the high-stakes step — think step-by-step (Opus 5 P5).

Method and matching heuristics → `reference/reconciliation.md`.

Outputs a status matrix row per feature and a drift list.

---

## ROLLUP Phase

Assemble higher-level views from reconciled data. **Organize only — do not score or decompose.**

- **Roadmap**: group features by milestone/release; present order as-found in artifacts. Priority scoring is deferred to Rank (offer `PDM_TO_RANK_HANDOFF`).
- **WBS**: build a scope tree (Project → Epic → Feature) from existing epics/specs/issues. This is a static *view*; live execution decomposition into atomic steps is deferred to Sherpa (offer `PDM_TO_SHERPA_HANDOFF`).
- **Dashboard**: overall delivery %, per-area breakdown, status counts. Compute the % by the stated rule and attach aggregate confidence — never an eyeballed number → `reference/reconciliation.md` §Rollup Math & Aggregate Confidence.

---

## REPORT Phase

Emit the deliverable using `reference/output-formats.md`. Keep documented intent and implemented reality visibly distinct, include confidence, and always include "What I couldn't reconcile."

---

## Navigator Q&A Loop (`ask`)

PdM-style conversational entry point. Per turn: `CLASSIFY → ANSWER → OFFER`.

```
per turn:
  1. CLASSIFY — map the question to a recipe lens:
       "is X shipped / built"        → features + reconcile (status of X)
       "what's left / not done"      → gaps
       "what's next / roadmap"       → roadmap
       "how is work structured"      → wbs
       "where are we overall"        → status
  2. REUSE   — reuse already-located sources and inventory from earlier turns
  3. ANSWER  — lowest sufficient tier: one-line status + evidence first
  4. GROUND  — artifact ref + code file:line (or coverage); state confidence; keep intent vs reality distinct
  5. OFFER   — one most-likely next question, mapped to a recipe or a handoff
  6. ROUTE   — out-of-scope → name the agent and stop:
       "how does X work?"            → Lens
       "which should we do first?"   → Rank
       "when did X change?"          → Trail
       "is X spec-compliant?"        → Attest
```

Session memory: cache located scope sources and the feature inventory once per session; re-verify a cached `file:line` if the repo may have changed. Never reuse a status without its evidence still holding.

---

## Worked Example

A full `status` pass on a small repo, end to end. Use as the reference shape for reconciliation.

**Question:** "Where are we on the Payments module?"

**LOCATE** — plan side: `ROADMAP.md` ("v2: Payments"), `gh issue list --state all` → #142 Refunds (open), #150 Payouts (closed), #151 Webhooks (closed). Code side: `src/payments/` exists.

**INVENTORY** — survey `src/payments/`:
- `payouts.ts:30` payout schedule + tests → built
- `payouts.ts:75` retry handler is a `// TODO` stub
- `webhooks.ts:12` webhook receiver + tests → built
- no `refund*` file anywhere

**RECONCILE** — pair plan ↔ code, apply Issue-State Cross-Signal:

| Feature | Plan | Code | Status | Conf. | Note |
|---------|------|------|--------|-------|------|
| Payouts | #150 closed | `payouts.ts:30` + tests | `Done` | High | closed + code agree |
| Payout retry | #150 closed | `payouts.ts:75` stub | `In-Progress` | High | **drift: closed-but-partial** — issue closed, retry unbuilt |
| Webhooks | #151 closed | `webhooks.ts:12` + tests | `Done` | High | |
| Refunds | #142 open, ROADMAP v2 | none (searched `src/payments/**`, routes, tests) | `Not-Started` | Medium | could exist under other terms |

**REPORT** — deliver Status Matrix (`output-formats.md`); surface the payout-retry drift as the headline finding; offer: prioritize Refunds → Rank, decompose Refunds → Sherpa.

The valuable output here is not the 60% number — it is the **drift row** (a closed issue whose work is half-done) that no single-source view would catch.
