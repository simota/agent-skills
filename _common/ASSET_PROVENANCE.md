# Asset Provenance & Rights Protocol

Cross-skill discipline for **knowing where a produced asset came from, what may legally be done with it, and who decided to ship it**. Applies to any generated artifact that leaves the workspace: images, illustrations, icons, logos, copy, video, audio, and generated code bundled as a deliverable.

**Read when:** an asset is generated rather than authored; a reference or stock source feeds a deliverable; an asset moves from exploration toward publication; someone asks "can we actually use this?"; an asset needs to be reproduced or re-derived months later.

**Audience:** `forge`, `pixel`, `muse`, `ink`, `funnel`, `funnel[premium]`, `atelier`, `frame`, `vision`, `sketch`, `cue`, `director`, `stage`, `nexus`.

**Prerequisites:** none.
**Composes with:** `_common/EVIDENCE_LADDER.md` (a rights claim is evidence and has a level), `_common/CANDIDATE_SELECTION.md` (rights is a **Gate**, never a lens), `_common/TRACEABILITY.md` (ID conventions), `_common/SECURITY.md` (what may be sent to an external service).

**Not legal advice.** This file governs *process*: what to record, when to check, and what to stop. Jurisdiction-specific questions (statutory exceptions, license interpretation, contract terms) route to `clause`; standards-conformance audits route to `canon`. When a question is genuinely legal, the correct output is an escalation, not an opinion.

---

## 1. Provenance has four layers — do not collapse them

| Layer | Answers | Typical carrier |
|-------|---------|-----------------|
| **Technical** | which tool, model, version, and edit path produced this | embedded metadata, signing (e.g. C2PA Content Credentials) |
| **Source** | what inputs and references fed it | generation log, reference sheet |
| **Rights** | what may be done with it, by whom, where, for how long | license record, consent, contract |
| **Decision** | why this one was adopted, and by whom | selection record (`CANDIDATE_SELECTION.md` §5) |

**No single metadata standard satisfies all four.** A file carrying signed technical provenance still tells you nothing about whether you are licensed to publish it.

**What provenance does not prove.** Content Credentials and comparable schemes make tampering detectable and origin auditable. They do **not** establish that the content is true, that it infringes nothing, or that it is good. Metadata is also routinely stripped in transit and is not displayed by every surface. Treat provenance as *evidence you can inspect*, never as clearance.

---

## 2. Asset states — "it looks finished" is not a state

| State | Meaning | May be published? |
|-------|---------|-------------------|
| `input` | source material brought in | — |
| `generated` | model output, **unevaluated** | **No** |
| `candidate` | retained for comparison | No |
| `edited` | human modification applied | No |
| `verified` | passed the QA checks that apply to its type | No |
| `approved` | an accountable owner approved it for a **named** use | No |
| `released` | published for that use | Yes, as approved |
| `retired` | withdrawn from use | No |

Two rules carry most of the value:

1. **`generated` is unevaluated by definition.** Presentation fidelity is not verification — model output arrives looking complete, and that appearance is uncorrelated with whether it is checkable. A polished render is `generated`, not `verified`.
2. **Re-apply the rights gate on every state change that widens exposure.** An image cleared for an internal moodboard is not thereby cleared for a landing page, and a landing page asset is not thereby cleared for paid media. Approval is scoped to a use, and it expires when the use changes.

---

## 3. Check rights at the decision points, not at the end

Seven points. A single pre-launch review is too late to be actionable, because by then the asset is embedded.

| Point | Confirm |
|-------|---------|
| **Brief / contract** | what the client engagement permits, disclosure obligations, deliverable ownership |
| **Input** | source, acquisition date, rights holder, whether it may be submitted to an external service, permitted modification / commercial / redistribution scope |
| **Service / model** | terms version in effect, retention, whether inputs train the model, output-use conditions — these differ **per model** inside one product |
| **Generation** | prompt and references recorded; no confidential or personal data submitted |
| **Output** | similarity to specific known works; presence of third-party marks, likenesses, or protected elements |
| **Human edit** | what a person actually changed, and who |
| **Use / publication** | medium, territory, term, audience, disclosure placement |

### License is a bundle, not a flag

Recording `commercial OK` is not a rights record. Resolve each dimension separately, and leave unresolved ones **visibly blank** rather than absent:

`reproduction` · `adaptation` · `distribution` · `public transmission` · `sublicense` · `commercial use` · `attribution` · `territory & term` · `model / likeness release` · `AI-specific restrictions`

A blank field is a finding. Publishing over a blank rights field is the failure mode, not the paperwork.

---

## 4. Generation log — three kinds of reproducibility

Record at the moment an asset is promoted to `candidate` — not for every throwaway generation.

```yaml
generation_id: <stable id>
date: <iso>
operator: <who>
tool: { name: <>, model: <>, version: <> }
inputs: [<asset ids>]
context_ref: <which brief / token set / system version was in force>
instruction: <prompt or parameters>
seed: <if available>
outputs: [<asset ids>]
known_limitations: [<what this asset does not do>]
data_classification: <public | internal | confidential | personal | restricted>
terms_snapshot: <service terms version at generation time>
review_status: <state from §2>
```

Three distinct properties, often confused:

| Reproducibility | Means | Realistic? |
|-----------------|-------|-----------|
| **Operational** | re-running the same settings yields the same output | often not — models change under you |
| **Functional** | an equivalent asset meeting the same requirements can be re-made | usually achievable, and usually sufficient |
| **Decision** | a third party can reconstruct *why this asset was adopted* | **the one that matters most in practice** |

Optimize for Decision reproducibility first. Chasing bit-identical regeneration against a moving model is wasted effort; being unable to explain an adoption six months later is not recoverable at all.

---

## 5. Reference discipline

For every reference, record three columns — the third is the one that gets skipped and the one that causes the incident:

| Extract | Verify | **Do not borrow** |
|---------|--------|-------------------|
| the mechanism (why it works) | that the mechanism transfers to this context | the specific expression: characters, marks, distinctive motifs, copy, a named creator's recognizable style |

Rules that follow:

- Never carry a **single** reference through to generation at full fidelity — pair it with a counter-reference (`CANDIDATE_SELECTION.md` §1).
- Reproducing a living creator's style on request, or steering an output toward an existing brand's identity, is a **stop**, not a trade-off.
- When output resembles a known work: record what it reads as *on its own*, place it beside the reference, separate genre convention from distinctive expression, review the generation path, then decide modify / replace / escalate. Have someone who has not seen the reference look at the output first.

---

## 6. What to attach to a shipped asset

Minimum record per released asset:

- stable **asset ID**, distinct from its filename (filenames get renamed; lineage must not break)
- **state** (§2) and the **approved use** it is scoped to
- **derivation**: which assets it came from
- **rights record** (§3), with unresolved fields visibly blank
- **generation log** reference (§4)
- **decision record** reference (`CANDIDATE_SELECTION.md` §5)

Filenames are for humans; IDs are for lineage. Keep a readable convention (`{project}_{type}_{channel}_{locale}_{variant}_{version}_{state}`) but never make lineage depend on it, and never encode personal or confidential names into it.

---

## 7. Scope — when this is overhead

Skip the record for: throwaway internal exploration that will never leave the workspace; assets whose sources are entirely first-party and already tracked; placeholder content explicitly marked as such.

Apply it in full whenever any of these hold: the asset will be **published**; a **third-party or model-generated** source feeds it; it depicts a **person, place, mark, or product**; it goes into a **design system or reusable library**; or the deliverable is for a **client**.

---

## 8. Failure modes

| Mode | Symptom | Mechanism | Response |
|------|---------|-----------|----------|
| `unclear provenance` | nobody can say which parts are generated, from what, edited by whom | four layers collapsed into one label | assign stable ID + state + record at `candidate`, not at release |
| `rights ambiguity` | the record says "commercial OK" and nothing else | vendor summary trusted in place of the bundle | resolve §3 dimensions; blank fields block release |
| `state promotion without re-check` | an exploration asset appears in paid media | approval treated as a property of the asset rather than of a use | re-apply the gate at each widening state change |
| `reference copying` | output is recognizably a specific work | single reference carried at full fidelity | §5 three columns; counter-reference; independent similarity look |
| `provenance as clearance` | "it has Content Credentials, so it is fine" | auditability mistaken for permission | §1 — provenance is evidence, not clearance |
| `confidential input` | client or personal data sits in prompts and logs | no data classification before tool choice | classify before selecting the tool; minimize input; see `_common/SECURITY.md` |
| `synthetic misrepresentation` | a generated person, result, or endorsement reads as real | high presentation fidelity implies a truth claim | label concept assets; do not use synthetic depictions for testimonial, credential, or performance claims |
| `non-reproducible adoption` | the shipped asset cannot be re-derived or explained | only the output was kept | §4 — prioritize Decision reproducibility |
