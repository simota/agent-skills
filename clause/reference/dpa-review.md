# DPA (Data Processing Agreement) Review Reference

Purpose: Structured review methodology for Data Processing Agreements under GDPR Article 28 (controller-processor relationship), covering sub-processor chain governance, international transfer mechanisms (SCC / BCR / adequacy decisions), Schrems II Transfer Impact Assessment, and audit rights. Surfaces clause gaps that expose controllers to joint liability without empirical user testing.

## Scope Boundary

- **clause `dpa`**: GDPR Art. 28-aligned DPA review — controller/processor obligations, sub-processor approval, SCC module selection, TIA, audit rights, breach notification SLA. Output is a clause-level findings report with statute citations.
- **clause `privacy` (sibling)**: data-subject-facing privacy policy review (collection purposes, retention, rights). DPA is the back-stage B2B contract; `privacy` is the front-stage B2C disclosure.
- **clause `tos` (sibling)**: service terms between provider and end user. DPA sits beneath ToS when the customer (controller) procures the service (processor).
- **clause `gap` (sibling)**: cross-document consistency. Use `gap` after `dpa` to verify that DPA terms do not contradict the privacy policy or main service agreement.
- **Cloak (elsewhere)**: implements consent flows, PII tagging, and data-flow code. Clause `dpa` checks the contract; Cloak checks the code that fulfills it. Hand discovered implementation gaps to Cloak.
- **Canon `gdpr` (elsewhere)**: codebase-level GDPR standard compliance audit. Clause `dpa` reviews paper contracts; Canon reviews source code against the GDPR control set. Cite findings to each other when the contract promises a control the code does not deliver.

## Workflow

```
SCOPE     →  identify roles (controller / processor / joint controller / sub-processor)
          →  identify transfer geography (EEA-only, EEA→adequate, EEA→third country)
          →  identify data categories (personal, special category Art. 9, criminal Art. 10)

SCAN      →  walk Art. 28(3) mandatory clause checklist (subject-matter, duration, nature,
              purpose, type of personal data, categories of data subjects, controller rights)
          →  walk SCC module selection (C2C / C2P / P2P / P2C, 2021/914 EU SCCs)
          →  walk sub-processor chain (named list, prior authorization, flow-down terms)

ASSESS    →  Schrems II TIA: third-country law analysis, supplementary measures
          →  audit rights scope: notice period, frequency cap, third-party auditor acceptance
          →  breach notification: hours-to-notify SLA vs GDPR Art. 33 72-hour controller duty
          →  liability cap and indemnity allocation between roles

REPORT    →  per-clause findings with risk level, Art. citation, proposed wording

SUGGEST   →  proposed redlines, missing-clause inserts, sub-processor list template
```

## Clause Checklist

> **Canonical privacy clauses** (P-01–P-14 generic privacy, G-01–G-08 GDPR data-subject-facing) live in `legal-checklists.md`. This table covers **DPA-specific Art. 28 controller-processor clauses only** — items that do not appear in the canonical privacy checklist. Walk both during SCAN: the canonical list for what the data subject sees, this list for what the controller-processor contract binds.

| Clause | GDPR basis | Common gap | Risk |
|--------|------------|------------|------|
| Subject-matter / duration / nature / purpose | Art. 28(3) chapeau | Vague "as needed" purpose; no end-of-contract trigger | High |
| Type of personal data and categories of data subjects | Art. 28(3) chapeau | Not enumerated; processor cannot scope safeguards | High |
| Process only on documented controller instructions | Art. 28(3)(a) | Processor self-grants secondary use rights | High |
| Confidentiality of authorized personnel | Art. 28(3)(b) | No personnel-binding clause | Medium |
| Security measures (Art. 32) | Art. 28(3)(c) | "Industry standard" only; no concrete control list | High |
| Sub-processor terms (prior authorization, flow-down) | Art. 28(2), 28(4) | Generic consent; no objection mechanism; no list | High |
| Data subject rights assistance | Art. 28(3)(e) | No SLA for forwarding access/erasure requests | Medium |
| Assistance with Art. 32-36 (security, breach, DPIA) | Art. 28(3)(f) | Cost-shift to controller for routine support | Medium |
| Deletion or return at end of services | Art. 28(3)(g) | Default retention; no deletion certificate | High |
| Audit rights and information access | Art. 28(3)(h) | "Once per year, 90-day notice" — too restrictive | Medium |
| Schrems II supplementary measures | EDPB 01/2020 | Encryption-in-transit only; no key custody analysis | High |
| Breach notification SLA to controller | Art. 33(2) | "Without undue delay" undefined (target ≤24-48h) | High |

(For the international-transfer safeguards clause itself, see `legal-checklists.md` G-08. This file's "Transfer Mechanism Selection" section below covers the DPA-specific module-selection extension.)

## Sub-processor Chain Management

Three governance models. Pick one and document:

| Model | Mechanism | When to use |
|-------|-----------|-------------|
| Specific prior consent | Each new sub-processor needs written approval | Highly regulated data (health, finance) |
| General authorization with objection | Notice in advance; controller can object within X days | SaaS at scale |
| Named list at execution | Annex lists current sub-processors; processor maintains updates | Standard B2B SaaS |

Required for all models: flow-down clause requiring sub-processor to accept terms equivalent to the DPA, and processor remains fully liable for sub-processor acts (Art. 28(4) final sentence).

## Transfer Mechanism Selection

| Destination | Primary mechanism | Notes |
|-------------|-------------------|-------|
| EEA / EFTA | None required | Free movement under GDPR |
| Adequacy-decision country (UK, JP, KR, CH, IL, AR, CA-commercial, NZ, US-DPF certified) | Adequacy decision | Verify DPF certification status if US destination |
| Third country (general) | EU SCCs (2021/914) modules 1-4 | Pick correct module by role pairing |
| Intra-group | BCRs (Binding Corporate Rules) | Approved BCRs only — verify on EDPB list |
| Specific situations | Art. 49 derogations | Last resort; not for systematic transfers |

Schrems II (CJEU C-311/18) requires Transfer Impact Assessment for any non-adequacy transfer: assess third-country surveillance law (e.g., FISA 702, EO 12333 for US), document supplementary measures (encryption with controller-held keys, pseudonymization, contractual protections, transparency reports).

## Anti-Patterns

- **Treating Art. 28(3) chapeau as boilerplate** — vague subject-matter, duration, or "all personal data needed for the service" fails the specificity requirement. Regulators read Art. 28(3) literally; generic language equals missing clause.
- **"Industry standard security measures" without an annex** — Art. 28(3)(c) requires reference to Art. 32 controls. Attach a concrete security annex (encryption, access control, logging, BCP) or the clause is unenforceable in audit.
- **Generic sub-processor consent without a list and objection right** — "Customer agrees processor may use sub-processors" is invalid. The controller must know the chain or be able to know on request, and have an objection mechanism.
- **Citing pre-2021 SCCs** — Decision 2010/87/EU (old SCCs) is repealed; Commission Decision 2021/914 (new modular SCCs) is the only valid set. Old SCC references signal a stale template.
- **Skipping the Schrems II TIA for US transfers** — relying solely on SCCs without supplementary measures is the exact pattern struck down. TIA + measures is mandatory; processors that say "SCCs are sufficient" are wrong post-July 2020.
- **Audit rights so restrictive they're unusable** — "annual, 180-day notice, on-site only, processor staff escort, no documents leave premises" defeats Art. 28(3)(h). Either grant SOC2/ISO27001 report acceptance as an alternative, or accept reasonable on-site terms (≥30 days notice, NDA, business hours).
- **Breach SLA = "without undue delay"** — quoting the GDPR text back is not an SLA. Specify hours (24-48h is market). The controller has 72h from awareness; the processor must give the controller buffer to investigate.
- **Silent on deletion or default to retention** — Art. 28(3)(g) requires a choice (delete vs return) at controller's discretion at end of services. Default-keep clauses are non-compliant.
- **No flow-down to sub-processors** — Art. 28(4) requires the same data-protection obligations to bind the sub-processor. Without flow-down, the processor breaches Art. 28 the moment it onboards a sub-processor.

## Handoff

- **To Cloak**: implementation work — sub-processor list page, DSAR forwarding workflow, breach detection pipeline, encryption-key custody design. Send sub-processor names, audit-evidence requirements, and breach SLA targets.
- **To Comply**: regulatory mapping — DPA ↔ SOC2 CC9.1 (vendor mgmt), ISO 27001 A.5.19-A.5.22 (supplier relationships), HIPAA BAA equivalence. Send DPA control list and request gap analysis vs target framework.
- **To Canon**: code-level GDPR audit. Send DPA-promised controls (encryption-at-rest, pseudonymization, deletion within X days) and request verification that the codebase implements them.
- **To Builder**: contract-driven implementation tasks (sub-processor objection form, automated deletion job at contract end, breach-notification webhook). Spec the SLAs and acceptance criteria.
- **To Prose**: plain-language version of customer-facing DPA summary or sub-processor change notice. Send key clauses that need translation from contract language to user comprehension.
