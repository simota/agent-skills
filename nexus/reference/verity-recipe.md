# `verity` — Codebase × documentation coherence audit → a triaged register of contradictions, stale record, and unexplained artifacts

**Purpose:** Full phase contract for the `verity` Recipe — take a **repository's record** (documentation, comments, config, CI, specs) and its **reality** (the code as it runs today), audit them against each other in **both directions**, and produce a **triaged discrepancy register** covering exactly three finding classes: **CONTRADICTION** (two artifacts assert incompatible things), **STALE** (an artifact was true once and no longer is), and **UNEXPLAINED** (something exists and the repo records no reason why). **Writes no product code and fixes nothing** — the deliverable is the register at `docs/audit/verity-<slug>/`, every entry located, quoted, corroborated, severity-tiered, and routed to the recipe that would close it. The **coherence** member of the Comprehend family: `cartograph` maps how a system is built **across space**, `chronicle` maps how it evolved **across time**, `verity` maps where its account of itself **fails to hold**.

**Read when:** Executing the `verity` Recipe. Authored to `reference/recipe-contract.md` (all 8 elements).

---

## What `verity` is for

A repository accumulates two kinds of decay that no test catches. First, the **record drifts from reality**: a README documents a flag that was removed, two docs state different retry limits, a config comment describes the opposite of what the code does, an onboarding guide names a script that no longer exists. Second, the **reason evaporates**: a timeout is `4300ms` and nobody knows why, a module has no callers and no commit message explaining it, a workaround says "temporary" and predates everyone on the team. A new contributor trusts the record and is misled; an operator trusts a runbook and makes it worse; a maintainer is afraid to touch a constant because its justification is gone. The user's ask is not "fix it" — it is **"show me, in detail, everywhere this is true."**

`verity` exists because **auditing a repo's self-account has a method distinct from the single-agent tools that touch parts of it**. `lens` answers one "does X exist / how does Y work" question; `trail` chases one regression; `sweep` finds unused files; `pdm` reconciles planned scope against shipped code; `attest` proves an implementation conforms to *one given spec*; none of them **enumerate the record's checkable claims, verify each against the code, invert the sweep to find code the record never explains, and triage the result into an actionable register**. That is a controlled multi-agent protocol: freeze the artifact inventory → extract the claims → verify them forward → trace provenance backward → corroborate adversarially → triage and cluster → register → prove coverage.

**`verity` is `newsroom` pointed inward.** `newsroom` grounds an article's claims against the world and ships a Provenance Report; `verity` grounds a repository's claims against the repository and ships a **Verity Register**. The discipline is the same — claim extraction, producer ≠ verifier, refute-polarity confirmation, nothing dropped silently — and it is cited (`reference/research-grounding.md`, `_common/ADVERSARIAL_REFUTATION.md`) rather than re-derived. The inversion is that `verity`'s third class is an **absence**: a finding *about the record's silence*, which needs the opposite discipline (see the Provenance Search Record).

**Report-only by contract.** `verity` reads the repo and writes only under `docs/audit/`. It never edits a doc, never fixes a constant, never deletes an orphan — because a discrepancy's correct resolution is frequently *the opposite* of the obvious one (see the authority rule below), and choosing wrong silently is worse than the drift. Every finding carries a **route** to the recipe that would close it; that hand-off is where remediation lives.

### Default Mode: `AUTORUN` (with a SCOPE gate)

`verity` ships nothing executable and changes no behavior, so it runs autonomously by default. But "audit the codebase and the docs" has an unbounded denominator, and fanning claim-verification out over the wrong artifact set is the expensive mistake — so the **SCOPE gate is contract-level**: the resolved artifact set, finding charter, authority table, severity floor, and depth are confirmed before the EXTRACT/CORRELATE fan-out. This is a **scope/blast-radius gate, not a knowledge-juncture dialogue** — `verity` is a comprehension recipe, not a dialogue recipe. The one *optional* human touchpoint beyond it is the Mode-conditional **owner-ratification** checkpoint in CORROBORATE (`GUIDED`/`INTERACTIVE` only): a participant who knows *why* the constant is `4300` or *which side* of a contradiction was intended resolves in one line what no amount of searching can. Escalate to **confirm-before-launch** at `depth=deep`, `repos ≥ 2`, or an inventory over **400 in-scope artifacts**. There is **no destructive-action gate** (read-only over the repo; writes only under `docs/audit/`) — same posture as `cartograph`/`chronicle`/`delve`.

---

## The three finding classes

The charter is **frozen at SCOPE** and is exactly these three classes with their subclasses. A candidate that fits none of them is `OUT-OF-CHARTER` — this is what keeps a coherence audit from becoming a general opinion dump (a style preference, a design critique, a missing feature are all real findings and all belong to `anneal`/`judge`/`spark`, not here).

| Class | Subclass | The finding is | Minimum evidence |
|-------|----------|----------------|------------------|
| **CONTRADICTION** | `doc↔code` | a document asserts behavior the code does not have | both sides quoted verbatim + located |
| | `doc↔doc` | two documents assert incompatible things about the same subject | both excerpts + the shared subject named |
| | `comment↔code` | an in-code comment describes something the adjacent code does not do | excerpt + the code it annotates |
| | `contract↔impl` | a declared interface (OpenAPI/schema/types/env template/CLI help) diverges from the implementation | the declaration + the implementing site |
| | `code↔code` | two implementations of the same rule have diverged (forked helper, duplicated constant, two configs of one thing) | both sites + the rule they both claim to encode |
| **STALE** | `dangling-reference` | a path, symbol, URL, command, or doc anchor the record names no longer resolves | the reference + the resolution failure |
| | `version-drift` | the record pins/describes a version, API, or tool the project has moved off | the record's claim + the current version's evidence |
| | `dead-scaffolding` | a flag permanently on, a deprecation past its stated removal, a `TODO`/`FIXME` whose premise is gone | the marker + evidence its premise no longer holds |
| | `process-rot` | a documented procedure (setup, release, runbook step) that cannot succeed as written | the step + why it fails today |
| | `freshness-gap` | a time-sensitive document with no `as-of`/owner/review-trigger, or one past its own trigger (doc-quality W3) | the document + the missing/lapsed metadata |
| **UNEXPLAINED** | `unexplained-value` | a magic constant, threshold, or limit with no recorded justification | the value + the **Provenance Search Record** |
| | `unexplained-decision` | a structural/technology/convention choice with no ADR, doc, or commit rationale | the choice + the search record |
| | `unexplained-workaround` | a hack/guard/special-case with no linked issue or stated cause | the site + the search record |
| | `orphan` | code/config/asset with no caller, no reference, no doc, and no recoverable reason to exist | the reachability evidence + the search record |
| | `authority-less-rule` | a lint rule, convention, or prohibition nobody can source | the rule + the search record |

**A CONTRADICTION does not name a culprit.** Which side is wrong is a *separate adjudication* (see § Authority) and is frequently **undecidable from the artifacts alone**. Filing "the doc is out of date" for what is actually a code regression against an intentional spec is this recipe's most damaging failure mode, because it converts a bug into a documentation chore.

**An UNEXPLAINED finding is a claim about the record's silence, so it must prove the silence.** Every entry in this class carries a **Provenance Search Record**: the sources searched and their misses — in-code comments · the doc set · ADR/spec directory · `git log`/`git blame` on the introducing commit · the PR/merge body · linked issues · `CHANGELOG` — each marked `searched: miss` or `not-available: <reason>`. An UNEXPLAINED entry without a complete search record is **inadmissible**, because "I did not look" is indistinguishable from "nobody knows" in the output, and only one of them is a finding.

---

## Scope resolution

- **`verity`** — the whole repo at the current HEAD. The default form.
- **`verity <path>`** — scope the audit to a subtree/component (its docs, code, config, and the references pointing into it).
- **`verity classes=<set>`** — narrow the charter (e.g. `classes=stale` for a pre-release doc pass, `classes=unexplained` for a knowledge-transfer audit before a maintainer leaves). Default: all three.
- **`verity depth=scout|standard|deep`** — `scout` = the load-bearing record only (README/entry docs/public contracts) + a sampled reverse sweep; `standard` (default) = the full doc set forward + top-K surfaces reverse; `deep` = both sweeps exhaustive over the inventory, all subclasses (**confirm-before-launch**).
- **`verity since=<tag|date|sha>`** — restrict the inventory to artifacts touched since a release/date: "what drift did this cycle introduce", the pre-release form.
- **`verity floor=S1|S2|S3|S4`** — the severity floor for the README's reported set (default `S3`). Below-floor findings still enter `register.yaml`, never dropped.
- **`verity repos=a,b,c`** — multi-repo: inventory and sweep each in parallel (hub-spoke), then a **cross-repo pass** for the contradictions only a shared view can see (a contract one repo publishes and another consumes). Defaults to **confirm-before-launch**.
- **`verity resume`** — re-enter from the last checkpoint (see **Resume**).

**File layout:** `docs/audit/verity-<slug>/` — `README.md` (summary-first overview) · `findings/contradiction.md` · `findings/stale.md` · `findings/unexplained.md` · `register.yaml` (the machine-readable ledger, the artifact a follow-on recipe consumes) · `rejected.md` (the refuted-candidate annex). A narrowed `classes=` set ships only its class files.

---

## Authority — which side is the source of truth

Adjudicating a contradiction requires knowing *what governs what*, and that is project-specific. The **authority table** is resolved at SCOPE, stated in the scope sheet, and applied in CORROBORATE. The default ordering:

| Subject | Authority order (highest first) | Rationale |
|---------|--------------------------------|-----------|
| **Observable behavior** | running code → its tests → the spec/AC → reference docs → comments | what the system *does* is not a matter of opinion |
| **Intent / requirement** | spec, AC, ADR → PR discussion → commit message → code | what the system *should* do is not readable off the code |
| **External contract** | the published artifact consumers use (OpenAPI, schema, SDK types, CLI help) → impl → prose docs | consumers bind to the declaration |
| **Operational procedure** | a procedure verified to succeed today → the runbook → tribal prose | a step that cannot run is not authoritative |

**The rule that matters:** when code contradicts an **intentional** spec/AC, authority sits with the spec and the finding routes to `bug`/`security` — *not* to a documentation edit. When the spec is merely descriptive prose about how it happens to work, authority sits with the code and the doc is stale. When the artifacts cannot settle which was intended, the finding is `authority: UNDECIDED`, routes to an **owner question**, and is **never auto-resolved toward the code**. `UNDECIDED` is a first-class outcome, not a failure to finish.

---

## Phase contract

`SCOPE → INVENTORY → EXTRACT → CORRELATE-FORWARD → CORRELATE-REVERSE → CORROBORATE → TRIAGE → REGISTER → GATE`

Judgment/comprehension throughout — **Claude-owned** (Lens/Grove/Trail/Attest/Sweep/Atlas/Gear/Magi/Rank/Omen/Canvas/Scribe/Judge); there is no code-gen phase, so no Codex routing for *production*. The exception is GATE: the grounding check **may** route to a second engine for prior-diversity on a high-stakes audit — verification is not code generation. **CORRELATE-FORWARD and CORRELATE-REVERSE are the distinctive core**: the two sweeps are *deliberately asymmetric and both mandatory*, because forward-only finds no orphans and reverse-only finds no contradictions, and either alone reads as a complete audit while missing an entire class.

### Phase 1 — SCOPE (resolve the audit contract)
Establish *what record*, *against what reality*, *under which charter*, *judged by which authority*, *at which revision* — an unbounded "check everything" is the recipe's first failure mode. Engines: `Lens`[anchor what the system currently is], `+Grove`?[repo/doc structure when the layout is unfamiliar]. Produce a **scope sheet**:
- the repo/path set (+ each repo's role for multi-repo) **+ the pinned HEAD SHA + read timestamp** — the baseline the register is grounded against, so every entry is re-verifiable and the audit's own staleness is detectable;
- the **artifact classes in scope** (docs · in-code comments-of-record · config/env templates · CI/workflows · schemas/API contracts · specs/ADRs · scripts/runbooks) and any exclusions with a one-line reason (`vendor/`, generated files, third-party docs);
- the **finding charter** (which of the three classes and which subclasses — frozen here, § The three finding classes);
- the **authority table** (§ Authority — defaults, plus any project-specific override such as "the OpenAPI file is generated from code, so code outranks it");
- the **severity floor** (default `S3`) and the **depth** (`scout`/`standard`/`deep`);
- the **caps** that will bound EXTRACT and CORRELATE (claims per artifact, surfaces per module) — declared here so the not-inspected long tail is explicit from the start, never implied-complete at the end;
- **SCOPE gate (contract-level; AUTORUN cannot skip):** present the scope sheet (4-8 lines: target + pinned HEAD, artifact classes, charter, authority overrides, floor, depth, caps). The user confirms/corrects before the fan-out. `depth=deep`, `repos ≥ 2`, or `> 400` inventory items → confirm-before-launch.
- **Draft init:** on confirmation, write `docs/audit/verity-<slug>/README.draft.md` (status `draft`, scope sheet filled). See **Resume**.

### Phase 2 — INVENTORY (freeze the denominator)
Enumerate every in-scope artifact at the pinned HEAD and classify it — this set **is** the denominator coverage is later measured against, and freezing it is what lets the register state "N of M artifacts verdicted" instead of an unfalsifiable "thorough". `Grove`[doc/dir topology, where the record actually lives], `Lens`[code surface map — modules, public entry points, contracts], `+Sweep`?[reachability pass seeding the `orphan` subclass], `+Gear`?[dependency/tooling/CI inventory when those classes are in scope]. Per artifact: path · type · **authority tier** (from the SCOPE table) · last-touched commit + date · a load-bearing score (referenced-by count × audience reach). **Output: the frozen Artifact Inventory** — plus the **sweep assignment**: which artifacts feed CORRELATE-FORWARD (record side) and which code surfaces feed CORRELATE-REVERSE (reality side). The inventory is **never widened by a later phase**; a discovery that would widen it is recorded as an inventory gap for the next run.

### Phase 3 — EXTRACT (turn the record into checkable claims)
The cost governor. Do **not** diff artifacts pairwise (O(n²) and unactionable); instead pull, from each record-side artifact, its **checkable claims** — single assertions about the system that can be confirmed or refuted against code. `Lens`[read each artifact, split it into atomic claims], `+Quill`?[comment/docstring extraction at scale when comments-of-record are in scope]. Per claim: `claim_id` · source locator (file + anchor/line) · verbatim text · **claim type** (behavioral · structural · procedural · contractual · version/factual) · the **code anchor(s)** it would be verified against · a load-bearing flag. Caps: **≤ top-N claims per artifact (N=12 at `standard`)**, ranked by load-bearing-ness — a claim a reader would act on outranks a passing mention. Claims are **assigned IDs here and carried through**, per `_common/FINDING_LEDGER.md` §4's assigned-identity mechanism: remediation rewrites the sentence a claim lives in, so a derived key would lose it. **Output: the Claim Set** + the per-artifact extraction cap actually applied.

### Phase 4 — CORRELATE-FORWARD (claim → reality; parallel, per claim batch)
Verify each claim against the system as it is. Batched and fanned out hub-spoke, no shared mutable state (`_common/PARALLEL.md`). Engines per claim type: `Lens`[behavioral/structural — does the code do this], `Attest`[contractual — spec/AC conformance, its native capability], `Gear`/`Gear[gha]`[procedural/version — does this command, CI step, or pinned version still hold], `Schema`/`Gateway`?[schema and API-contract claims], `Trail`[**the staleness stamp** — for a refuted claim, when did it stop being true, and in which commit]. Per claim, exactly one verdict:
- `HOLDS` — confirmed against the code (recorded; this is the coverage numerator, not a finding).
- `CONTRADICTED` — the code does something incompatible → CONTRADICTION candidate (both sides quoted).
- `STALE` — the claim was true and is no longer, with Trail's when-and-where → STALE candidate. **The distinction from `CONTRADICTED` is temporal evidence, not tone**: without a commit showing the transition it is `CONTRADICTED`, not `STALE`.
- `UNVERIFIABLE` — the claim is not checkable against this repo (an external fact, an aspiration, an opinion) → recorded, not a finding.
**Output: the verdicted Claim Set** + the CONTRADICTION/STALE candidate pool.

### Phase 5 — CORRELATE-REVERSE (reality → record; parallel, per surface batch)
The inverted sweep, and the only source of the UNEXPLAINED class. For each significant code surface from the INVENTORY (public entry points, configs, constants of consequence, flags, workarounds, orphan candidates — **≤ top-K per module, K=10 at `standard`**, ranked by consequence × opacity), establish what the record says about it. `Trail`[the introducing commit, its message, blame lineage, the PR body — the primary provenance engine], `Lens`[is it referenced by any doc, is it reachable in code], `+Sweep`?[reachability confirmation for `orphan`], `+Atlas`?[whether a structural choice has an ADR at all]. Per surface, exactly one verdict:
- `EXPLAINED` — documented **and** its rationale recoverable (recorded; the reverse-sweep coverage numerator).
- `DOCUMENTED-NO-RATIONALE` — the *what* is written, the *why* is not → UNEXPLAINED candidate at reduced severity.
- `UNEXPLAINED` — no recoverable rationale anywhere → UNEXPLAINED candidate. **Requires the complete Provenance Search Record** (§ The three finding classes) — an entry without it is inadmissible and is dropped at CORROBORATE.
- `ORPHANED` — unreferenced, unreachable, and unexplained → UNEXPLAINED candidate, `orphan` subclass.
**Discipline:** an absence is only a finding once the search is exhausted at the declared depth. Where a source cannot be searched (no issue tracker access, squashed history, an imported `Initial commit`), record `not-available: <reason>` — a **history-integrity gap**, never silently counted as a miss. **Output: the verdicted Surface Set** + the UNEXPLAINED candidate pool + the integrity-gap list.

### Phase 6 — CORROBORATE (adversarial confirmation + authority adjudication)
The noise filter, and the reason this register is worth reading. **Producer ≠ verifier**: the agent that raised a candidate never confirms it. `Judge`[re-derive each candidate from the artifacts alone — refute polarity per `_common/ADVERSARIAL_REFUTATION.md`, default-to-refuted on evidence claims], `Magi`[**authority adjudication** on each surviving CONTRADICTION per the SCOPE authority table, and dispute resolution]. Per candidate:
- **Confirmation:** both sides must resolve to real text at the pinned HEAD and the incompatibility must be re-derivable. A candidate that cannot be re-derived is `REJECTED-REFUTED` → the `rejected.md` annex **with its refutation evidence** (never silently dropped — a reader must be able to see what was considered and why it did not qualify).
- **Authority adjudication:** each CONTRADICTION gets `authority: code | spec | contract | procedure | UNDECIDED` (§ Authority). `UNDECIDED` is an outcome, never a placeholder for "assume the code".
- **`ACCEPTED-BY-DESIGN`:** a candidate that is intentional and correct is closed — **but only against a written statement of that intent**. If the intent exists nowhere in the repo, the candidate is not closed; it is **re-filed as `unexplained-decision`**, because "everyone knows it is deliberate" is precisely this recipe's third class.
- **Dedupe + cluster seeding:** fingerprint candidates (`class ⊕ subject ⊕ normalized statement`, **excluding line numbers and other locators that move when a fix lands** — `_common/FINDING_LEDGER.md` §4) and mark duplicates against a surviving id.
- **Owner-ratification (Mode-conditional checkpoint; not contract-level):** under `GUIDED`/`INTERACTIVE`, present the `UNDECIDED` authority questions and the top UNEXPLAINED entries (≤ 5-7 lines) to whoever was there. A ratified item is promoted (`UNDECIDED` → adjudicated, or `UNEXPLAINED` → `EXPLAINED (owner-attested)` with the rationale captured for the register). The cheapest high-value upgrade the recipe has; skipped under headless `AUTORUN`, **never fabricated**.
**Output: the confirmed finding set** + the rejected annex + per-finding authority.

### Phase 7 — TRIAGE (severity, root-cause clusters, routes)
Turn a confirmed set into an actionable one — an untriaged 300-item list is a dump, not a deliverable.
- **Severity** = *misdirection impact* (what breaks if a reader trusts this: production/security/data → contributor time → local friction) × *exposure* (external users/consumers → operators → contributors → internal-only). Tiers `S1` blocking-misdirection · `S2` misleading · `S3` friction · `S4` cosmetic. `Rank`[score the set], `+Omen`?[failure-mode read on the S1/S2 shortlist — what actually goes wrong downstream].
- **Root-cause clustering (the analysis that makes the list short):** group findings by the change that produced them. Most large registers are a handful of causes — *an abandoned migration*, *a renamed concept never propagated*, *a doc set written once and never re-read*, *a departed owner*. `Trail`[correlate the introducing commits across findings]. A cluster carries its own route, and one cluster route often supersedes twenty per-finding routes: **14 findings tracing to a half-finished migration route to `migrate` to finish it**, not to 14 doc edits.
- **Route** per finding and per cluster:

| Finding | Route |
|---------|-------|
| CONTRADICTION, `authority: code` | doc correction → `quill`/`scribe` direct |
| CONTRADICTION, `authority: spec` (code diverged from intent) | `bug` — or `security` when the divergence is a control |
| CONTRADICTION, `authority: contract` | `gateway`/`schema` direct, or `migrate` if consumers bound to the wrong side |
| CONTRADICTION, `code↔code` (forked rule) | `anneal` (design), or `refactor` when the consolidation is known |
| CONTRADICTION, `UNDECIDED` | **owner question** → `spec` (settle the intent) or `magi` (adjudicate) |
| STALE `dangling-reference` / `freshness-gap` | doc correction → `quill`/`scribe` direct |
| STALE `version-drift` | `gear` (deps/tooling) or `shift` (a real upgrade) |
| STALE `dead-scaffolding` | `trim` (feature removal verdict) or `sweep` direct |
| STALE `process-rot` | `bug` if the procedure is a shipped path; otherwise doc correction |
| UNEXPLAINED `unexplained-decision` | `chronicle` (mine the history first) → `atlas` (write the ADR) |
| UNEXPLAINED `unexplained-value` | `assay` (prove the value experimentally) or owner question |
| UNEXPLAINED `orphan` | `trim`/`sweep` (removal verdict — `verity` never deletes) |
| UNEXPLAINED `unexplained-workaround` / `authority-less-rule` | owner question → `atlas` (record it) or `trim` (retire it) |
| **Cluster: abandoned migration** | `migrate` — finish the change; the per-finding routes are superseded |
| **Cluster: whole doc set never re-read** | `package`/`scribe` re-authoring, scoped to that set |

- **Output: the triaged register content** — every confirmed finding with severity, cluster, route; the cluster list ranked by finding-count × severity.

### Phase 8 — REGISTER (author the deliverable)
`Scribe` authors the document set; `+Canvas`?[a coherence heatmap — artifact × finding class — and a root-cause cluster map; default on at `depth ≥ standard`]. Follows `reference/doc-quality-protocol.md` (reader contract W1-W3, grounding W4-W6, coherence W7-W9, summary-first W10-W11, **and W11b's per-file length envelope — stated per file, never for the set**).
- `README.md` — summary-first: the audit contract (target, pinned HEAD, charter, caps) · **the coverage line** (claims verdicted / inventory artifacts covered / surfaces traced, each against its frozen denominator) · the top clusters · the `S1`/`S2` findings in full · counts per class · the diagrams · how to read `register.yaml`. Per-class depth lives in the class files, linked, **not duplicated** (W7-W9 across the set).
- `findings/<class>.md` — one file per in-charter class, every entry at or above the floor, ordered by severity: `id · subclass · locus · counterpart · verbatim evidence (both sides) · authority · severity · cluster · route`, plus the **Provenance Search Record** for every UNEXPLAINED entry.
- `register.yaml` — the complete machine-readable ledger **including below-floor entries**, one record per finding: `id · class · subclass · locus · counterpart · evidence_refs · authority · confidence · severity · cluster · route · first_seen_head · disposition`. This is the artifact a follow-on recipe consumes; the prose files are the human view of the same data.
- `rejected.md` — the refuted candidates with their refutation evidence, and the `OUT-OF-CHARTER` items with the class that owns them.
- **Freshness metadata (W3):** `as-of` = the pinned HEAD + timestamp · owner · **review trigger** — the register is itself a document that rots, and it says so.

### Phase 9 — GATE (coverage + grounding — the recipe's quality bar)
The register is only as good as its grounding and its denominator. **Producer ≠ verifier** (the checker is not Scribe, nor the agent that raised the finding): `Attest`/`Judge` run —
- **Grounding check:** sample across classes; every entry's locators must resolve to real text at the pinned HEAD and every quoted excerpt must be verbatim (doc-quality W6). A fabricated citation, a quote that is not in the file, or a "contradiction" whose two sides do not actually conflict **fails the gate**.
- **Search-record check (the UNEXPLAINED gate):** every UNEXPLAINED entry has a **complete** Provenance Search Record with per-source `searched: miss` or `not-available: <reason>`. An incomplete record fails — the entry is either completed or withdrawn.
- **Authority check:** no CONTRADICTION is silently resolved toward the code; every `authority: code` verdict shows why the record was not authoritative for that subject, and `UNDECIDED` entries carry their owner question.
- **Coverage check:** every INVENTORY artifact is verdicted, sampled-with-its-cap-stated, or excluded-with-a-reason — never silently skipped. The applied caps (claims per artifact, surfaces per module) and the resulting **not-inspected long tail** are stated explicitly, so the register is never implied-complete. History-integrity gaps from Phase 5 appear in the README.
- **False-positive check:** re-derive a sample of confirmed findings independently; a sample failure rate above the declared tolerance (default: any confirmed finding that fails re-derivation) sends the whole class back through CORROBORATE.
- **Doc Quality Gate (W12):** the register passes `reference/doc-quality-protocol.md` — reader-path (can a maintainer act on an entry without the auditor present?), coherence across the file set, readability.
- **Cross-engine grounding (option — prior-diversity):** on a high-stakes audit (due-diligence, hand-over, `repos ≥ 2`), route the sampled-claim check to a second engine so the verifier's priors differ from the producer's (`_common/ADVERSARIAL_REFUTATION.md`).
- **Coverage / grounding loop:** on failure, loop back to CORRELATE-FORWARD (unverified claim), CORRELATE-REVERSE (incomplete search record), CORROBORATE (unsound finding or mis-adjudicated authority), or INVENTORY (an artifact class was never assigned to a sweep). **Termination bound:** `loop ≤ 3 cycles (default N=3)` (recipe-contract §2); exit on `ACCEPT`/`target-met` (fully grounded, coverage-complete, no failed re-derivation) · `diminishing-returns (Δ < ε)` · `cap-reached` · `BLOCK` (a class cannot be verified — e.g. the reality side is unrunnable, or history the repo does not retain is required). On any non-`ACCEPT` exit, **ship the register with the unverified entries labeled `UNVERIFIED` and the residual gap named** — never silently ship an ungrounded register, never loop past marginal value.
- **Finalize:** promote the draft → `docs/audit/verity-<slug>/` with the pinned-HEAD provenance attestation stamped in `README.md`.

---

## Termination bound

The one bounded loop is Phase 9's coverage/grounding loop — cap, exit vocabulary, and loop-back targets are defined there (recipe-contract §2). Every other phase is single-pass: EXTRACT and both CORRELATE phases fan out per batch, CORROBORATE runs a bounded confirmation per candidate, but none of them loop.

**Not a `_common/FINDING_LEDGER.md` member — by design.** `verity` emits a finding set, but it has **no fix cycle**: nothing closes inside the run, so it fails C6 (the fix must close inside the loop) exactly as compliance findings do — closure belongs to the routed recipes and to humans, on their own timeline. What it needs is the **tracker shape** that §1a prescribes: a durable, owned, re-checkable register. It therefore **borrows** two primitives and cites the rest — assigned identity (§4, because remediation rewrites the text a claim lives in) and the "nothing is silently dropped" discipline (§5, realized here as the rejected annex + below-floor records) — and adds no loop machinery. Re-running `verity` at a later HEAD and diffing `register.yaml` is the intended re-check; it is a new run, not a cycle.

## Confirm / safety gate

Default Mode `AUTORUN`, with two touchpoints: the contract-level **SCOPE gate** (Phase 1 — the scope sheet is confirmed before the EXTRACT/CORRELATE fan-out; `depth=deep`, `repos ≥ 2`, or `> 400` inventory items escalates it to **confirm-before-launch**) and the Mode-conditional **owner-ratification** checkpoint (Phase 6 — `UNDECIDED` authority questions and top UNEXPLAINED entries; skipped under headless `AUTORUN`, never auto-confirmed). **No destructive-action gate and no Ask First trigger by construction:** `verity` is read-only over the repo and writes only under `docs/audit/` — the same posture as `cartograph`/`chronicle`/`delve`. A run that finds itself wanting to *fix* something has left its contract; the fix routes out (§ TRIAGE).

## Resume

**Checkpoint-resume** (recipe-contract §4): recipes with ≥ 4 phases persist phase outputs at each boundary so an interrupted run resumes from the last checkpoint. Each phase's output — as defined in § Phase contract — is written to the draft (`docs/audit/verity-<slug>/README.draft.md` plus the growing `register.draft.yaml`) with a current-phase marker; the frozen Inventory, Claim Set, and per-candidate verdicts are the resumable state. `verity resume` reads the draft, summarizes progress in 3-5 lines, and continues from the last successful boundary — never silently restarts from SCOPE. On GATE-`ACCEPT` the drafts are promoted (Phase 9 Finalize).

## Output — Verity Register

`NEXUS_COMPLETE` with the base `## Nexus Execution Report` plus the named **Verity Register**. Each element's content and shape is defined in the phase named after it — the document set itself is authored to the Phase 8 outline, which is canonical and not restated here:

- **Audit contract** (Phase 1: target · pinned HEAD + timestamp · artifact classes · finding charter · authority table · severity floor · depth · caps).
- **Coverage statement** (Phases 2/4/5/9): claims verdicted / inventory artifacts covered / surfaces traced, each against its frozen denominator, **with the applied caps and the not-inspected long tail stated** — the line that makes the register falsifiable rather than merely long.
- **Finding set** (Phases 4-7), per class, every entry located · quoted on both sides · authority-adjudicated · severity-tiered · clustered · routed; UNEXPLAINED entries carry their Provenance Search Record.
- **Root-cause clusters** (Phase 7), ranked, each with the cluster-level route that supersedes its members'.
- **Rejected annex** (Phase 6): refuted candidates with refutation evidence; `OUT-OF-CHARTER` items with their owning recipe.
- **Register document set** at `docs/audit/verity-<slug>/` (`README.md` · `findings/*.md` · `register.yaml` · `rejected.md`), authored to the Phase 8 outline.
- **Provenance attestation** (Phase 9): sampled-claim resolution at the pinned HEAD, the search-record / authority / coverage / false-positive verdicts, cross-engine verifier if used, loop trajectory + exit reason.
- **Residual Ledger** — per `reference/autonomy-quality-protocol.md` Q17-Q19 (typed, never a free-text follow-up list). `verity`'s **Done** is deliverable-relative: the audit is done when every inventory artifact is verdicted-or-capped-with-the-cap-stated and every register entry is corroborated. **Unfixed findings are not residuals — they are the deliverable**, and each carries its route. Genuine residuals are of exactly three kinds, each routed: an artifact class that could not be verified (`BLOCK`, with the blocker), a history-integrity gap that made provenance unrecoverable (routed to an owner question), and the capped long tail (routed to a deeper re-run).

## Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **The noise dump** (300 undifferentiated findings nobody acts on) | TRIAGE severity × exposure tiers + a declared floor + **root-cause clustering** — a cluster route supersedes its members' |
| **False positives** (a plausible "inconsistency" that is not one) | CORROBORATE: producer ≠ verifier, refute polarity, candidate must be re-derivable from the artifacts; GATE re-derives a sample |
| **The "code is always right" fallacy** (filing a code regression as a stale doc) | § Authority table + per-finding `authority` adjudication; `UNDECIDED` is a first-class outcome; GATE fails any silent resolution toward the code |
| **"I did not look" reported as "nobody knows"** | the **Provenance Search Record** is mandatory for every UNEXPLAINED entry; GATE withdraws incomplete ones |
| **Unbounded scope / implied completeness** | frozen INVENTORY denominator + caps declared at SCOPE + the coverage statement naming the not-inspected long tail |
| **One-directional audit** (forward only misses orphans; reverse only misses contradictions) | both CORRELATE sweeps are mandatory and asymmetric; the coverage statement reports each denominator separately |
| **Silently dropped candidates** (rejected findings vanish, so the audit cannot be audited) | `rejected.md` annex with refutation evidence; below-floor entries kept in `register.yaml` |
| **Charter creep** (design critiques, style preferences, and feature wishes filed as inconsistencies) | the three-class charter is frozen at SCOPE; anything else is `OUT-OF-CHARTER` with the recipe that owns it |
| **"Everyone knows it is deliberate"** (an intentional oddity closed on tribal knowledge) | `ACCEPTED-BY-DESIGN` requires a *written* statement of intent; without one the candidate is re-filed as `unexplained-decision` |
| **Fabricated evidence** (a quote that is not in the file, a contradiction whose sides do not conflict) | GATE grounding check — verbatim resolution at the pinned HEAD, producer ≠ verifier, optional cross-engine |
| **Rot mistaken for divergence** (a doc that was never true reported as "outdated") | CORRELATE-FORWARD separates `STALE` from `CONTRADICTED` on **temporal evidence** — no transition commit, no staleness claim |
| **Scope creep into fixing** (an audit that starts editing docs mid-run) | report-only contract: writes confined to `docs/audit/`; every finding carries a route instead of an edit |
| **Stale-on-delivery** (the register itself ages silently) | grounding at a **pinned HEAD** + W3 freshness metadata (`as-of` · owner · review trigger); re-run and diff `register.yaml` is the re-check |
| **Duplicate findings across artifacts and re-runs** | fingerprint dedupe excluding volatile locators (`_common/FINDING_LEDGER.md` §4) + assigned `claim_id` carried through |
| **Invisible search failures** (an unsearchable source counted as a miss) | Phase 5 records `not-available: <reason>` as a **history-integrity gap**, surfaced in the README |

## Boundaries / vs neighbors

- **vs `cartograph`** — the family sibling on the **space** axis: cartograph documents *how the system is built* (a structural snapshot); `verity` documents *where the account of it fails to hold*. `cartograph → verity` when mapping surfaces contradictions worth enumerating; `verity → cartograph` when the register shows there is no structural map to be inconsistent with. Full detail: see Decision tree.
- **vs `chronicle`** — the family sibling on the **time** axis: chronicle reconstructs *how the repo got here* and reports UNKNOWN rationales as gaps in its narrative; `verity` makes *the unexplained itself the deliverable*, enumerated, searched-to-exhaustion, and routed. `verity → chronicle` is the standard escalation for a cluster of `unexplained-decision` findings: chronicle mines the history that verity's per-finding search could not.
- **vs `anneal`** — **audit vs fix**, the same pair shape as `assay`→`anneal`. anneal discovers *design weaknesses* and **brushes them up** with real code changes; `verity` discovers *record-vs-reality discrepancies* and **never edits**. Bare "spec-code drift" is overloaded: a **register of every divergence** → `verity`; **align the code and clean it up** → `anneal`. `verity → anneal` is the audit→fix pair.
- **vs `pdm` (agent)** — pdm answers *what is built vs what was planned* (delivery status against a roadmap/PRD). `verity` has no privileged plan: it audits every artifact against every other, in both directions, and adds the staleness and unexplained classes pdm does not carry. "Is feature X shipped?" → `pdm` direct; "where does our record disagree with our code?" → `verity`.
- **vs `attest` (agent)** — attest proves an implementation conforms to **one given spec's ACs** (a spec is the privileged authority, conformance is the question). `verity` has no privileged artifact — deciding which side governs is its own adjudication step — and it audits the reverse direction too. A spec to verify against → `attest` direct.
- **vs `canon` (agent)** — canon audits against **external named standards** (OWASP/WCAG/OpenAPI/ISO 25010). `verity` audits **internal self-consistency**; it has no external rulebook.
- **vs `lattice`** — lattice proves **design-system** conformance against a frozen token denominator (visual). `verity` audits the **textual/semantic** record. Design tokens drifting → `lattice`; docs describing tokens that no longer exist → `verity`.
- **vs `newsroom`** — the same discipline, opposite direction: newsroom grounds an article's claims against **the world** and ships an article; `verity` grounds the repo's claims against **the repo** and ships a register. An article to fact-check → `newsroom`.
- **vs `sweep` / `trail` / `lens` (agents)** — each answers one question (unused files · one archaeology question · one comprehension question) and each is a `verity` **engine**. One question → the agent direct; the repo-wide register → `verity`.
- **vs `judge` / code review** — judge reviews a **diff** for bugs and quality. `verity` audits the **standing record** repo-wide and files nothing about code quality.
- **vs `gauge`** — gauge audits `SKILL.md` **format** normalization in this ecosystem specifically; `verity` audits content coherence in any repo.

**Decision tree:**
```
Want a report of where the repo's record and its reality disagree (no fixes)?
  NO  → how the system is built now (structure)?        → cartograph
        how it got here (history, decisions)?           → chronicle
        find design weaknesses AND fix them?            → anneal
        prove impl conforms to a given spec?            → attest
        what is built vs planned (delivery status)?      → pdm
        conformance to an external standard?            → canon
        unused files / dead code to delete?             → sweep direct
  YES → one question ("does X exist", "why this commit")? → lens / trail direct
        a design-system token denominator?               → lattice
        an article's claims vs the world?                → newsroom
        the WHOLE record → contradictions + stale + unexplained, triaged?
              → verity
                    verity                    → whole repo, all three classes
                    verity <path>             → one component's record
                    verity classes=stale      → pre-release doc pass
                    verity classes=unexplained → knowledge-transfer / owner-departure audit
                    verity since=<tag>        → drift introduced this cycle
                    verity depth=deep         → exhaustive (confirm-before-launch)
                    verity repos=a,b,c        → cross-repo contracts (confirm-before-launch)
                    then fix                  → verity → anneal / bug / quill / migrate (per route)
                    unexplained cluster       → verity → chronicle → atlas
```

## Scale

**7-24 agents × the GATE loop (≤ 3 cycles).** *Range derivation:* floor = SCOPE 1 (Lens) + INVENTORY 1 + EXTRACT 1 + CORRELATE-FORWARD 1 + CORRELATE-REVERSE 1 + CORROBORATE 1 + REGISTER 1 + GATE 1 = **8**, less one where `depth=scout` merges SCOPE into INVENTORY = **7**. Ceiling = SCOPE 2 (Lens + Grove) + INVENTORY 3 (Grove + Lens + Sweep/Gear) + EXTRACT 2 (Lens + Quill) + CORRELATE-FORWARD 5 (Lens + Attest + Gear/Gear[gha] + Schema/Gateway + Trail) + CORRELATE-REVERSE 4 (Trail + Lens + Sweep + Atlas) + CORROBORATE 2 (Judge + Magi) + TRIAGE 2 (Rank + Omen) + REGISTER 2 (Scribe + Canvas) + GATE 2 (Attest + a second-engine verifier) = **24**. The low end is `verity <path> depth=scout classes=stale`; the high end is a multi-repo `depth=deep` run with all three classes and cross-engine grounding.

**Cost scales with claim count × surface count — not with repo size.** SCOPE and INVENTORY are cheap enumeration; EXTRACT is capped (≤ N claims per artifact); both CORRELATE phases are capped (claim batches; ≤ K surfaces per module) and run in parallel; CORROBORATE is bounded by the candidate count, which the caps already bound. A 200k-line repo and a 20k-line repo cost similarly at the same claim/surface budget. The cost governors are **`depth`**, **`classes`** (dropping `unexplained` removes CORRELATE-REVERSE entirely — the single biggest lever), the **severity floor**, and the EXTRACT/CORRELATE caps. Read-heavy, write-light; lighter than the execution recipes (no build/verify-code phases), heavier than `cartograph` at equal scope because two sweeps run instead of one.

## Shared protocols & Add-ons

- **Shared:** claim extraction, per-claim verification, and the nothing-unverified-ships discipline → `reference/research-grounding.md` (pointed inward — the repo is the source corpus). Adversarial confirmation, refute polarity, default-to-refuted → `_common/ADVERSARIAL_REFUTATION.md` (CORROBORATE; also the prior-diversity basis for GATE's optional cross-engine check). Register document authoring, freshness metadata, per-file length envelope → `reference/doc-quality-protocol.md` (W1-W3, W4-W6, W7-W9, W10-W11b, W12). Evidence-bound claims, producer ≠ verifier, typed residuals and the completion sweep → `reference/autonomy-quality-protocol.md` (Q9-Q11, Q15-Q19). Per-batch parallel isolation → `_common/PARALLEL.md` (hub-spoke, no shared mutable state across claim/surface batches). Assigned identity + nothing-silently-dropped → `_common/FINDING_LEDGER.md` §§4-5 **as borrowed primitives only** (`verity` is a declared non-member — see § Termination bound). Owner-ratification checkpoint presentation → `reference/dialogue-protocol.md` (the Mode-conditional checkpoint only — `verity` is a comprehension recipe, not a dialogue recipe).
- **Add-ons:** +`Gateway`/`Schema` (contract↔impl claims when an OpenAPI spec, GraphQL schema, or DB schema is in the artifact set), +`Gear[gha]`/`Gear` (CI-workflow and dependency/tooling claims), +`Sentinel` (when a contradiction touches a security control — its divergence routes to `security`, not to a doc edit), +`Sweep` (reachability for the `orphan` subclass), +`Atlas` (whether a structural choice has an ADR at all, and shaping an `unexplained-decision` into the ADR that would close it), +`Omen` (downstream failure read on the S1/S2 shortlist), +`Canvas` (coherence heatmap + cluster map), +`Polyglot` (when the record exists in more than one language and the translations have drifted from each other — a `doc↔doc` contradiction the monolingual sweep cannot see), +`Sherpa` (decompose a multi-repo or `depth=deep` run into independent per-repo/per-class sub-runs).

## Chain template

`SCOPE (Lens +Grove?) → ✓SCOPE-gate + draft-init → INVENTORY (Grove + Lens +Sweep? +Gear?) → EXTRACT ∥per-artifact-batch (Lens +Quill?) → CORRELATE-FORWARD ∥per-claim-batch (Lens + Attest +Gear/Gear[gha]? +Schema/Gateway? + Trail[staleness stamp]) → CORRELATE-REVERSE ∥per-surface-batch (Trail + Lens +Sweep? +Atlas?) → CORROBORATE (Judge[refute-polarity] + Magi[authority], ✓owner-ratification) → TRIAGE (Rank +Omen? + Trail[cluster correlation]) → REGISTER (Scribe +Canvas?) → ⟲GATE (Attest/Judge, +2nd engine?) → promote docs/audit/verity-<slug>/ + pinned-HEAD attestation` [NO CODE]

Each phase's inputs, caps, engine bindings, discipline rules, and outputs are canonical in § Phase contract; `∥` marks the parallel fan-outs (per artifact / claim / surface batch, hub-spoke per `_common/PARALLEL.md`). The `✓` markers are the **SCOPE gate** (Phase 1 — contract-level, AUTORUN cannot skip) and the **owner-ratification** checkpoint (Phase 6 — Mode-conditional); `⟲` is the **coverage/grounding loop** (Phase 9 — `loop ≤ 3 cycles (default N=3)`, exit vocabulary and loop-back targets defined there). Resumable via `verity resume` from the draft's current-phase marker. Hands off per finding and cluster route (§ TRIAGE) — `anneal` / `bug` / `security` / `quill` / `migrate` / `trim` / `chronicle` → `atlas` / `spec` / `assay`.
