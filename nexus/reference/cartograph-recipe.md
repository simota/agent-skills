# `cartograph` — Multi-repo reverse-engineering → bird's-eye diagrams + design document

**Purpose:** Full phase contract for the `cartograph` Recipe — take a **target feature or system that spans multiple repositories**, reverse-engineer it **from the code itself** (white-box, own/accessible source — not black-box observation), stitch the per-repo reads into **one cross-repo model**, and produce a **bird's-eye overview** (aggregated architecture diagrams) **+ a design document** that explains how it actually works. **Writes no product code** — the deliverable is documentation (diagrams + design doc), grounded in code evidence. The comprehension-and-documentation member of the ecosystem: where `delve` excavates *one shipped feature in one codebase* for *evolution directions* through dialogue, `cartograph` **maps how an existing feature/system is architected across many repositories and documents it**.

**Read when:** Executing the `cartograph` Recipe. Authored to `reference/recipe-contract.md` (all 8 elements).

---

## What `cartograph` is for

A user has a feature or system whose implementation is **scattered across multiple repositories** — a web frontend repo, a BFF, two backend services, a shared library, an infra repo — and no single up-to-date document explains how the pieces fit. They (a new team member, an architect, an auditor) want a **bird's-eye view** (俯瞰図): aggregated architecture diagrams that show the components, the boundaries, and where the feature crosses repo lines, **plus a design document** that reconstructs the design from the code. The deliverable is a named **Cartography Map** — cross-repo architecture diagrams + a design document + a per-repo breakdown, every element **grounded in a code citation**.

`cartograph` exists because **reverse-engineering a cross-repo feature into a coherent overview has a method distinct from the single-agent comprehension tools**. `lens` comprehends *one* codebase; `atlas` analyzes *one* repo's architecture; `canvas` draws a diagram from *one* input; none of them **read N repos independently, correlate the feature across the seams between them (API calls, events, shared contracts), and synthesize a single grounded bird's-eye model + design doc**. That is exactly a controlled multi-agent protocol: scope the repo set + feature boundary → map each repo independently → correlate across the seams → synthesize the bird's-eye model → draw the diagrams → author the design doc → verify every claim is grounded.

**Grounded-by-construction (doc-grade discipline):** every component, edge, and design-decision in the output traces to a **code citation** (`repo/path:line` or a named artifact). Reconstructed *intent* ("this queue exists to decouple X from Y") is marked as **inferred** and separated from *observed structure*; where the code does not reveal the answer, the recipe writes **UNKNOWN**, never a plausible fabrication (doc-quality-protocol W4-W6). A diagram edge with no code evidence is a defect, not a helpful guess.

### Default Mode: `AUTORUN` (with a SCOPE gate)

`cartograph` writes no product code and ships nothing executable, so it runs autonomously by default — but a cross-repo read starts with an ambiguous boundary (*which* repos, *which* feature, *how deep*), so the **SCOPE gate is contract-level**: the resolved repo set + feature boundary + diagram set is confirmed before the expensive per-repo mapping fan-out. Unlike `delve`/`spec` this is a **scope/blast-radius gate, not a knowledge-juncture dialogue** — `cartograph` is a comprehension recipe, not a dialogue recipe. Escalate to `GUIDED` when the repo set is large (≥ 5) or the feature boundary is fuzzy. There is **no destructive-action gate** (read-only over source; writes only the doc/diagram files under `docs/`).

---

## Scope resolution

- **`cartograph <feature>`** — reverse-engineer a named feature/system. Nexus resolves the repo set from the workspace (sibling repos, a manifest, a monorepo's packages, or the user-supplied list). The default form.
- **`cartograph <feature> repos=a,b,c`** — the repo set is supplied explicitly (paths or clone URLs); skips repo discovery.
- **`cartograph` with no feature → whole-system map** (the broad form): map the entire cross-repo system rather than one feature. Defaults to **confirm-before-launch** (a whole-system sweep is higher-stakes) and caps the SYNTHESIZE/DIAGRAM output to the **top-N subsystems by centrality** (default 8), the long-tail recorded as "not expanded", never silently dropped.
- **`cartograph resume`** — re-enter from the last checkpoint (see **Resume**).

**Single-repo degradation:** if only one repo is in scope, CORRELATE degrades from *cross-repo seams* to *cross-module seams* within that repo and the recipe still delivers a valid overview — but a single large repo is usually better served by `lens`/`atlas` direct (see Boundaries). `cartograph`'s headline value is the **cross-repo** correlation.

---

## Phase contract

`SCOPE → MAP → CORRELATE → SYNTHESIZE → DIAGRAM → DOCUMENT → VERIFY`

Judgment/comprehension throughout — **Claude-owned** (Lens/Atlas/Magi/Canvas/Scribe/Judge); there is no code-gen phase, so no Codex routing.

### Phase 1 — SCOPE (resolve the repo set + feature boundary)
Establish *what to map* before mapping it — an unbounded "map everything" is the recipe's first failure mode. `Grove`?/`Lens`[detect the repos in the workspace and each repo's role] + `Lens`[locate the target feature's entry points in each repo — where does this feature touch this repo?]. Produce a **scope sheet**: the repo set (with each repo's one-line role), the feature boundary (in / out), the intended diagram set (system-context / component / sequence-per-flow / data-flow / cross-repo-dependency), and the doc outline.
- **SCOPE gate (contract-level; AUTORUN cannot skip):** present the scope sheet (3-6 lines). The user confirms/corrects the repo set + feature boundary + diagram set before the mapping fan-out. Mapping the wrong repos or an over-broad boundary is the expensive mistake this gate prevents. No-feature (whole-system) and ≥ 5 repos → confirm-before-launch (may escalate to `GUIDED`).
- **Draft init:** on confirmation, write `docs/architecture/<slug>.draft.md` (status `draft`, scope sheet filled). See **Resume**.

### Phase 2 — MAP (read each repo independently — parallel, hub-spoke)
Map each repo **independently** — independence is what keeps the reads unbiased and parallelizable (hub-spoke, no shared mutable state per `_common/PARALLEL.md`). Per repo, in parallel:
- `Lens`[structure, responsibilities, the feature's data flow *within this repo*, entry points, and the **public surface** this repo exposes to the others — HTTP routes, RPC/gRPC methods, published events, exported library API, DB tables owned]
- +`Atlas`?[internal architecture / layering / key modules] when the repo is large or architecturally central
- +`Trail`?[history / why — recent churn on the feature, when the seam was introduced] when design rationale matters
- **Output per repo: a repo card** — role · internal shape of the feature · **exposed interfaces** (the outbound/inbound contract surface) · owned data · citations. The exposed-interfaces list is the raw material CORRELATE stitches on.

### Phase 3 — CORRELATE (stitch the seams — the cross-repo core)
The distinctive phase: connect the independent repo cards into **one** model by resolving the **seams** where the feature crosses a repo boundary. Match each repo's *outbound* call/event/dependency to another repo's *inbound* surface:
- `Atlas`[cross-repo dependency & integration graph — who calls whom, who depends on whose library, who consumes whose events] + `Gateway`?[API/contract boundaries — match client calls to server routes, flag version/contract mismatch] + `Stream`?[data/event flow across services — queues, topics, pipelines] + `Schema`?[shared/duplicated data model across repos — the same entity in two stores].
- Resolve **seam type** per edge: sync call (HTTP/RPC) · async event/queue · shared library · shared datastore · build/deploy dependency. Each edge carries the citation on **both** ends (caller site + callee definition).
- **Unresolved-seam handling:** an outbound call with no matching inbound surface found (or vice-versa) is recorded as an **open seam** (`external dependency` / `unmapped repo` / `dead call`), never silently dropped — it is a finding, not noise.
- **Output: a unified cross-repo model** — nodes (components across all repos), edges (typed, cited seams), and the open-seam list.

### Phase 4 — SYNTHESIZE (the bird's-eye model)
`Magi`[synthesize the correlated model into the bird's-eye architecture — layers, bounded contexts, the feature's end-to-end control/data path across repos] + `Atlas`[name the architectural style + the load-bearing design decisions inferred from the structure]. Reconstruct **intent** here, under discipline: an inferred design decision ("the BFF exists to aggregate the two backends for the mobile client") is labeled **inferred** and tied to the structural evidence that suggests it; where intent is not recoverable from code, write **UNKNOWN** (doc-quality W4-W6). Separate **observed structure** (high confidence, cited) from **inferred rationale** (marked, evidence-linked).
- **Completeness self-check:** does the synthesized model account for every repo card and resolve/record every seam? Gaps feed the VERIFY loop.
- **Output: the bird's-eye model** — the overview architecture + the end-to-end feature path + the design-decision ledger (observed vs inferred).

### Phase 5 — DIAGRAM (the visual bird's-eye view)
`Canvas` renders the aggregated visuals from the model (Mermaid by default; draw.io/ASCII per `canvas` conventions) — **multiple diagram types**, each serving a different altitude:
- **System-context / component diagram** — the 俯瞰図: all repos/services as nodes, the typed seams as edges (the headline artifact).
- **Sequence diagram(s)** — the feature's key end-to-end flow(s) across repos (request → BFF → services → data).
- **Data-flow / ER diagram** — where the feature's data lives and moves, across the repos' stores (when a data surface exists).
- **Cross-repo dependency diagram** — library/build/deploy dependencies between repos.
- Every diagram node/edge is **traceable to a model element** (which is itself cited); no node exists that CORRELATE did not establish.

### Phase 6 — DOCUMENT (the design document)
`Scribe`[author the design document — HLD altitude] embedding the DIAGRAM artifacts. Follows `reference/doc-quality-protocol.md` (reader contract W1-W3, grounding W4-W6, coherence W7-W9, summary-first readability W10-W11). Standard outline:
- **Overview** — what the feature/system does + the bird's-eye diagram, summary-first.
- **Repo breakdown** — per repo: role · the feature's slice in it · exposed interfaces · owned data (from the repo cards).
- **Cross-repo interactions** — the typed seams + the sequence diagram(s); how the feature flows end-to-end.
- **Data & contracts** — the data-flow/ER + shared-contract analysis (+ any version/contract mismatch flagged in CORRELATE).
- **Design decisions** — observed structure vs inferred rationale (from SYNTHESIZE), each labeled and cited.
- **Open questions & gaps** — open seams, UNKNOWN intents, not-expanded subsystems — recorded honestly.
- **Glossary** — the domain terms, unified across repos (repos often name the same concept differently — CORRELATE's reconciliation lands here).

### Phase 7 — VERIFY (grounding gate — the recipe's quality bar)
The output is only as good as its grounding. **Producer ≠ verifier** (the checker is not Scribe/Canvas):
- **Grounding check:** `Judge`/`Attest`[sample the diagram edges and design-doc claims → each must resolve to a real code citation]. A fabricated component, a seam with no code on one end, or an inferred rationale presented as fact **fails the gate**. This is `cartograph`'s core discipline (the analog of clone's differential-parity): claims are **evidence-bound**, and anything unverified is labeled, never asserted.
- **Doc Quality Gate (W12):** the design doc passes the reader-contract / coherence / grounding checks of `reference/doc-quality-protocol.md`.
- **Coverage check:** every in-scope repo appears in the model and doc; every seam is typed-or-open; no in-scope repo silently missing.
- **Coverage / grounding loop:** if the gate finds fabricated/unsupported elements, missing components, or unresolved coverage, loop back to CORRELATE (missing seam) or SYNTHESIZE (missing/ungrounded model element). **Termination bound:** `loop ≤ 3 cycles (default 3)` (recipe-contract §2); exit on `ACCEPT`/`target-met` (fully grounded + coverage-complete) · `diminishing-returns (Δ < ε)` (a cycle resolves little new) · `cap-reached` · `BLOCK` (a seam is unresolvable without access to a repo not in scope). On any non-`ACCEPT` exit, **finalize the map with the open seams / UNKNOWNs explicit + the residual gap** — never silently ship an ungrounded diagram, never loop past marginal value.
- **Finalize:** promote `docs/architecture/<slug>.draft.md` → `docs/architecture/<slug>.md` with diagrams embedded/linked.

---

## Termination bound

The Phase 7 coverage/grounding loop: `loop ≤ 3 cycles (default 3)` (recipe-contract §2). Exit vocabulary: `ACCEPT`/`target-met` | `diminishing-returns (Δ < ε)` | `cap-reached` | `BLOCK`. Non-`ACCEPT` exit → finalize with open seams + UNKNOWNs + residual gap explicit. SCOPE/MAP/CORRELATE/SYNTHESIZE/DIAGRAM/DOCUMENT are single-pass (MAP fans out in parallel but does not loop).

## Confirm / safety gate

- **Default Mode `AUTORUN`** with the **SCOPE gate** (contract-level; AUTORUN cannot skip) — confirm the repo set + feature boundary + diagram set before the mapping fan-out.
- **Confirm-before-launch** when run with no feature (whole-system map) or the repo set is ≥ 5.
- **No destructive-action gate** — `cartograph` is read-only over source and writes only documentation under `docs/architecture/` (same posture as `delve`/`charter`: no code, nothing shipped). Escalate to `GUIDED` for a fuzzy boundary / large repo set.

## Resume

**Checkpoint-resume** (recipe-contract §4): `cartograph` has ≥ 4 phases, so it persists phase outputs at each boundary to `docs/architecture/<slug>.draft.md` (SCOPE → scope sheet; MAP → repo cards; CORRELATE → cross-repo model + open seams; SYNTHESIZE → bird's-eye model + design-decision ledger; DIAGRAM → diagram sources; DOCUMENT → draft doc; VERIFY → grounding results + loop trajectory) with a current-phase marker. `cartograph resume` reads the draft, summarizes progress in 3-5 lines, and continues from the last successful boundary — never silently restarts from SCOPE. On VERIFY-ACCEPT the draft is promoted and the `.draft.md` archived/removed.

## Output — Cartography Map

`NEXUS_COMPLETE` with the base `## Nexus Execution Report` plus the named **Cartography Map**:
- **Scope sheet** — repo set (+ roles) · feature boundary · diagram set (SCOPE).
- **Bird's-eye diagrams** — system-context/component · sequence(s) · data-flow/ER · cross-repo dependency (DIAGRAM), each traceable to the model.
- **Design document** — overview · repo breakdown · cross-repo interactions · data & contracts · design decisions (observed vs inferred) · open questions · glossary (DOCUMENT), at `docs/architecture/<slug>.md`.
- **Design-decision ledger** — observed structure vs inferred rationale, each labeled + cited (SYNTHESIZE).
- **Open seams & gaps** — unresolved seams, UNKNOWN intents, not-expanded subsystems — recorded, never dropped.
- **Grounding attestation** — VERIFY result: sampled claims/edges → citation-resolved; loop trajectory + exit reason.
- **Follow-ups** — recommended next recipe per gap (`delve` to evolve one mapped feature · `anneal` to brush up a design weakness the map surfaced · `migrate` if the map reveals a wholesale change · `charter` to turn the map into a delivery plan · `spec` to specify a change to a mapped seam).

## Failure Modes Prevented

| Failure | Mitigation |
|---------|------------|
| **Fabricated architecture** (drawing components/edges that aren't in the code) | VERIFY grounding gate — every node/edge resolves to a citation; producer ≠ verifier |
| **Plausible-but-wrong intent** (asserting *why* a design exists when the code doesn't say) | SYNTHESIZE separates observed structure from **inferred** rationale; UNKNOWN over fabrication (doc-quality W4-W6) |
| **Mapping the wrong / too many repos** (unbounded "map everything") | SCOPE gate confirms the repo set + feature boundary before the fan-out; no-feature caps to top-N by centrality |
| **Missed seams** (a cross-repo call/event silently absent from the map) | CORRELATE matches outbound↔inbound surfaces + records **open seams**; VERIFY coverage check |
| **Repo-blindness** (per-repo reads never stitched into one view) | CORRELATE is a mandatory dedicated phase — the recipe's headline value, not an afterthought |
| **Single-agent shallowness** (one lens read of a huge cross-repo system) | MAP fans Lens across repos in parallel + Atlas correlation + Canvas + Scribe — machinery a single agent lacks |
| **Terminology drift across repos** (same concept, different names → confusing doc) | CORRELATE reconciles; DOCUMENT glossary unifies the terms |
| **Stale-on-delivery** (diagrams that don't match current code) | grounding is to the code *as read*; citations let a reader re-verify; open seams/UNKNOWNs are explicit |
| **Boil-the-ocean whole-system** (expand every subsystem) | no-feature form caps to top-N by centrality; long-tail recorded, not dropped |
| **Ungrounded diagram shipped** (loop burns out but map ships as if complete) | non-ACCEPT exit finalizes with open seams + residual gap explicit, never silently |
| **Work lost on interruption** | checkpoint-resume + `cartograph resume` from the current-phase marker |

## Boundaries / vs neighbors

- **vs `delve`** — both are no-code and grounded in real code, but `delve` excavates **one shipped feature in one codebase** through **dialogue** to produce **evolution directions** (forward-looking: what it could become, INTERACTIVE). `cartograph` maps **a feature/system across multiple repos** **autonomously** to produce **architecture diagrams + a design doc** (backward-looking: how it works today). `cartograph → delve` when, after understanding a mapped feature, the user wants to evolve it. Axis: **comprehend-and-document-across-repos** vs **excavate-one-feature-for-evolution**.
- **vs `charter`** — `charter` analyzes **one repo** and produces a forward **team + work plan** (`docs/CHARTER.md`) to *deliver* something. `cartograph` analyzes **multiple repos** and produces a backward **architecture overview + design doc** to *understand* what exists. charter answers "who does what work next"; cartograph answers "how is the existing system built". `cartograph → charter` when the map becomes the input to a delivery plan.
- **vs `pdm` (agent)** — `pdm` reconciles **planned scope** (specs/issues/roadmap) **against implemented code** → a feature-inventory / gap report (plan-vs-code, read-only, single-agent). `cartograph` does **pure code reverse-engineering** → architecture diagrams + design doc; it compares nothing against a plan. pdm answers "what's built vs planned"; cartograph answers "how is it architected". A `cartograph` run may *use* pdm's inventory as a scoping input.
- **vs `clone`** — `clone` reverse-engineers an **external** product's **observable surface** (black-box) to **rebuild it** in code, verified by differential parity. `cartograph` reverse-engineers **your own / accessible source** (white-box) to **document it**, verified by grounding — it writes **no code** and rebuilds nothing. Axis: **black-box-external-to-rebuild** vs **white-box-own-source-to-document**.
- **vs `migrate`** — `migrate` *changes* an own-system wholesale with a completeness guarantee (writes code). `cartograph` only *documents* the system as-is (no change). `cartograph → migrate` when the map reveals a change worth making across the seams.
- **vs `package`** — `package` generates a **document package** from a **preset registry** (forward authoring from inputs/intent across 12 domains). `cartograph` reverse-engineers **existing code** into a **specific architecture artifact** (diagrams + design doc). package is domain-preset doc generation; cartograph is code-grounded architecture documentation.
- **vs `lens` / `atlas` / `canvas` (agents)** — each is single-agent and single-repo/single-input: `lens` comprehends one codebase, `atlas` analyzes one repo's architecture + ADRs, `canvas` draws one diagram from one input. `cartograph` orchestrates `Lens`×N (per repo) + `Atlas` (cross-repo correlation) + `Canvas` (the diagram set) + `Scribe` (the design doc) + a grounding gate — the multi-repo correlation, synthesis, and verification machinery none of them have alone. Each is one engine inside `cartograph`. A single-repo overview → `lens`/`atlas`/`canvas` direct (minimum viable chain).

**Decision tree:**
```
Want to understand an EXISTING system from its code (no code changes)?
  NO  → rebuild an external product?          → clone
        change an own-system wholesale?         → migrate
        evolve ONE shipped feature (dialogue)?  → delve
        plan the work / design a team?          → charter
        generate docs from a domain preset?     → package
  YES → is it ONE repo / a single diagram?     → lens / atlas / canvas direct (minimum viable chain)
        does it span MULTIPLE repos and need a bird's-eye overview + design doc?
              → cartograph
                    cartograph <feature>        → scoped cross-repo map
                    cartograph <feature> repos=… → explicit repo set
                    cartograph (no feature)     → whole-system map (confirm-before-launch, top-N)
                    a mapped feature to evolve   → cartograph → delve
                    a change the map revealed    → cartograph → migrate / spec
                    turn the map into a plan     → cartograph → charter
```

## Scale

5-16 agents × the coverage loop (≤ 3 cycles). The low end is a scoped `cartograph <feature>` over 2 repos (SCOPE → Lens×2 → one Atlas correlation → Magi → Canvas → Scribe → one grounding check ≈ 6-8 agents). The high end is a whole-system map fanning Lens across many repos with Atlas/Gateway/Stream/Schema correlation, the full diagram set, and a grounding loop. **Cost scales with repo count** (the MAP fan-out) and diagram-set size, not lines of code — SCOPE is the cost governor (a tight feature boundary keeps each per-repo read shallow). Read-heavy, write-light; lighter than the execution recipes (no build/verify-code phases).

## Shared protocols & Add-ons

- **Shared:** doc authoring & grounding → `reference/doc-quality-protocol.md` (W1-W12: reader contract, UNKNOWN-over-fabrication, coherence, summary-first, Doc Quality Gate). Evidence-bound claims / producer≠verifier → `reference/autonomy-quality-protocol.md` (Q9-Q11: independent verification, evidence-bound claims, Acceptance Provenance). Per-repo parallel isolation → `_common/PARALLEL.md` (hub-spoke, no shared mutable state across repo reads). Diagram conventions (Mermaid/draw.io/ASCII) → `canvas` skill. Contested inference (is this really the design intent?) → `_common/ADVERSARIAL_REFUTATION.md` (light skeptic pass on high-stakes inferred rationale).
- **Add-ons:** +`Trail` (history/why a seam was introduced, in MAP), +`Gateway` (API-contract seam matching + version/breaking-change flag, in CORRELATE), +`Stream` (event/data-pipeline flow across services, in CORRELATE), +`Schema` (shared/duplicated data model across repos, in CORRELATE), +`Grove` (repo/directory structure detection, in SCOPE), +`PDM` (feature-inventory as a scoping input), +`Ripple` (blast-radius annotation when the map is a precursor to change), +`Attest` (grounding/citation-conformance in VERIFY), +`Sherpa` (decompose a large whole-system map into per-subsystem passes).

## Chain template

`SCOPE (Grove?/Lens[detect repos + roles] + Lens[locate feature entry points per repo] → scope sheet: repo set + boundary + diagram set + outline) → ✓SCOPE-gate (contract-level; confirm-before-launch when no-feature/≥5 repos) + draft-init → MAP ∥per-repo (Lens[structure + in-repo data flow + exposed interface surface + owned data] +Atlas?[internal arch] +Trail?[history] per _common/PARALLEL.md → repo cards) → CORRELATE (Atlas[cross-repo dep/integration graph] +Gateway?[API-contract seams] +Stream?[event/data flow] +Schema?[shared data model]; match outbound↔inbound, type each seam, record open seams → unified cross-repo model) → SYNTHESIZE (Magi[bird's-eye model + end-to-end path] + Atlas[style + design decisions]; observed-structure vs inferred-rationale, UNKNOWN over fabrication) → DIAGRAM (Canvas[system-context/component ‖ sequence(s) ‖ data-flow/ER ‖ cross-repo dependency], every node/edge model-traceable) → DOCUMENT (Scribe[design doc per doc-quality-protocol, diagrams embedded: overview/repo-breakdown/interactions/data/decisions/open-questions/glossary]) → VERIFY (Judge/Attest[grounding: claims/edges → citations, producer≠verifier] + Doc Quality Gate W12 + coverage check; ⟲ loop ≤3 cycles (default 3) back to CORRELATE/SYNTHESIZE on ungrounded/missing, exit ACCEPT | diminishing-returns (Δ<ε) | cap-reached | BLOCK → finalize with open seams + residual gap) → promote docs/architecture/<slug>.md` [NO CODE]

The SCOPE gate and the grounding/coverage bound are contract-level; resumable via `cartograph resume` from the draft's current-phase marker. Hands off to `delve` / `anneal` / `migrate` / `charter` / `spec` per surfaced gap.
