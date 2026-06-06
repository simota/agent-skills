# EULA (End User License Agreement) Review Reference

Purpose: Structured review methodology for End User License Agreements covering license type selection (proprietary perpetual / subscription / SaaS / OSS dual-license), license-grant scope, IP ownership and feedback assignment, restriction clauses (reverse engineering, benchmarking, AI-training), warranty/disclaimer/indemnity allocation, and jurisdiction-specific enforceability differences (US / EU / Japan).

## Scope Boundary

- **clause `eula`**: software license agreement review — grant scope, restrictions, IP, warranty, indemnity, termination, audit. Output is a clause-level findings report focused on licensor/licensee balance and enforceability.
- **clause `tos` (sibling)**: terms of service for an online service. EULA governs software you install or license; ToS governs a service you use. SaaS often blurs the line — when a downloaded SDK or on-prem component exists, an EULA is required alongside the ToS.
- **clause `dpa` (sibling)**: data processing addendum. EULA covers software rights; DPA covers personal data processed via the software. Many enterprise SaaS bundles need both.
- **clause `privacy` (sibling)**: data-subject privacy disclosure. EULA touches privacy only at telemetry / usage-data clauses.
- **clause `gap` (sibling)**: cross-document consistency. Use `gap` to verify EULA's IP-ownership clause does not contradict the ToS's user-content license.
- **Cloak (elsewhere)**: privacy implementation. EULA telemetry clauses describe what is collected; Cloak implements collection and consent. Hand telemetry-scope decisions to Cloak.
- **Canon `gdpr` / `wcag` (elsewhere)**: standards audit. EULA review checks the contract; Canon checks the codebase. License compliance scanning of OSS dependencies belongs to Canon `oss-license` if available, not Clause.

## Workflow

```
SCOPE     →  identify license type (perpetual / subscription / SaaS / OSS / hybrid)
          →  identify deployment (on-prem install / cloud-hosted / embedded SDK / API)
          →  identify licensee class (consumer / SMB / enterprise / government)
          →  identify governing law (state of US / EU member state / Japan)

SCAN      →  walk grant clause (scope, exclusivity, territory, term, sublicense, transfer)
          →  walk restriction clause (reverse engineering, benchmark, AI training, competitive use)
          →  walk IP clause (background IP retention, foreground IP, feedback assignment)
          →  walk warranty / disclaimer / limitation of liability / indemnity stack
          →  walk OSS notices and dependency obligations

ASSESS    →  enforceability per jurisdiction (clickwrap acceptance, unconscionability,
              consumer-protection overrides, EU UCTD test, Japan Consumer Contract Act test)
          →  liability cap proportionality (cap vs fees paid; carve-outs for IP infringement,
              confidentiality breach, gross negligence)
          →  termination triggers and post-termination data/license survival

REPORT    →  per-clause findings with risk level, statute/case citation, proposed wording

SUGGEST   →  proposed redlines, missing-clause inserts, jurisdiction-specific overrides
```

## License Type Matrix

| Type | Grant pattern | Revenue model | Termination effect | Common pitfalls |
|------|--------------|---------------|--------------------|-----------------| 
| Perpetual | One-time fee, perpetual license, time-bound maintenance | Upfront | License survives; updates stop | No version-lock clause; "perpetual" is undefined |
| Subscription (on-prem) | Time-limited license, auto-renew | Recurring | License terminates; software must stop running | License-key kill-switch unstated |
| SaaS | Right to access service, no software delivery | Recurring | Access ends; data export window | No exit-data clause; lock-in by default |
| Embedded SDK | License to integrate into licensee product, royalty or per-seat | Mixed | Sublicense to end users — depth must be defined | Sublicense scope unclear |
| OSS (permissive) | MIT / Apache 2.0 / BSD — broad grant, attribution required | Free | None | Patent grant absence (BSD/MIT); attribution gaps |
| OSS (copyleft) | GPL / AGPL / LGPL / MPL — derivative-work disclosure | Free | Auto-termination on breach | AGPL network-use trigger ignored in SaaS |
| Dual license | Commercial + OSS — pick one | Mixed | Per chosen license | Internal use of OSS edition triggers commercial license without notice |

## Clause Checklist

> **Canonical ToS-overlap clauses** (T-12 governing law, T-13 dispute resolution, T-15 severability, T-08 limitation of liability, T-06 IP ownership) live in `legal-checklists.md`. This table covers **EULA-specific software-license clauses only** — license-grant, restrictions, IP allocation, OSS, AI-training, license-compliance audit. For the generic governing-law/liability rows below, treat the canonical T-08/T-12/T-13 rows as primary and use these EULA rows only for the licensing-flavored gap context.

| Clause | Purpose | Common gap | Risk |
|--------|---------|------------|------|
| Grant scope (use, copy, modify, distribute, sublicense) | Define exactly what licensee can do | Missing "internal business use" qualifier | High |
| Term and territory | Time and geographic limits | Worldwide perpetual sublicensable — overly broad | Medium |
| Restrictions (reverse engineer, benchmark, AI training) | Protect IP and competitive position | Missing AI-training prohibition (2024+ standard) | High |
| Background IP retention | Each party keeps pre-existing IP | Silent — leads to ownership ambiguity | Medium |
| Foreground IP / deliverables | Who owns work product | Default to licensor; consumers expect to own outputs | High |
| Feedback assignment | License or assignment of licensee feedback | Overbroad — assigning all feedback may chill input | Low |
| Open-source notice | List OSS components and licenses | Stale list; no flow-down of OSS terms | Medium |
| Warranty / disclaimer | Limited warranty + as-is for everything else | Pure as-is in EU consumer context — unenforceable | High |
| Limitation of liability | Cap and exclusion of damages | Cap below fees; carve-outs missing | High |
| Indemnity (IP infringement) | Licensor defends against IP claims | No defense; no carve-back for combinations | High |
| Termination triggers | Breach / insolvency / convenience | No cure period; no survival clause | Medium |
| Audit rights (license compliance) | Verify deployment matches license | Surprise audits; no notice / scope | Medium |
| Export controls / sanctions | Oath with EAR / OFAC / EU dual-use | Missing entirely | Medium |
| Telemetry / usage data | What the software collects | Privacy policy reference missing | Medium |

(For governing law and venue, use `legal-checklists.md` T-12 / T-13 as canonical; this file's "Jurisdiction-Specific Differences" section below covers the EULA-specific enforceability extensions.)

## Jurisdiction-Specific Differences

| Topic | United States | European Union | Japan |
|-------|---------------|----------------|-------|
| Clickwrap enforceability | Generally enforceable if reasonable notice + affirmative action (Specht v. Netscape line) | Enforceable; consumer must have clear opportunity to review (UCTD 93/13) | Generally enforceable (Civil Code Art. 548-2 standard terms) |
| Unconscionability / unfair-terms test | UCC § 2-302 (procedural + substantive) | UCTD 93/13 — clauses creating significant imbalance struck | Consumer Contract Act Art. 8-10 — unilaterally disadvantageous clauses void |
| Reverse engineering ban | Generally enforceable (DMCA § 1201, Bowers v. Baystate) | Limited — Software Directive 2009/24 Art. 6 permits decompilation for interoperability (cannot waive) | Copyright Act Art. 30-4 / Art. 47-3 permit RE for security research and interoperability |
| Implied warranties | UCC § 2-314 / 2-315 — disclaimable with conspicuous "AS IS" | Largely non-disclaimable for consumers (CRD 2011/83, Sale of Goods Directive 2019/771) | Civil Code Art. 562 (non-conformity) — non-disclaimable in B2C under Consumer Contract Act |
| Liability cap floor | Generally upheld if not unconscionable | Cannot exclude liability for death, personal injury, gross negligence, intent (UCTD) | Cannot disclaim damages from intent/gross negligence (Consumer Contract Act Art. 8) |
| Choice of law (B2C) | Often respected with reasonable relationship | Rome I Art. 6 — consumer's habitual residence law applies despite choice | App Law Art. 11 — consumer's habitual residence mandatory rules apply |
| AI training restriction | Contract-based; no statutory override | Aligns with TDM opt-out (DSM Directive Art. 4) | Copyright Act Art. 30-4 limits — consider opt-out signals |

## Anti-Patterns

- **One EULA for all jurisdictions** — US-template "AS IS, NO WARRANTIES" survives in California but is partially void in Germany and Japan. Either localize or include jurisdiction-specific overrides.
- **Liability cap below fees paid** — caps at "$100" or "fees in last month" while taking $1M ARR is the textbook unconscionability case. Cap at 12 months' fees with carve-outs is the market standard.
- **No IP indemnity carve-back for combinations / modifications** — forces licensor to defend claims arising from licensee's mods. Add carve-back for combinations with non-licensor products and licensee modifications.
- **Reverse-engineering ban without interoperability carve-out in EU** — Software Directive 2009/24 Art. 6 grants a non-waivable right to decompile for interoperability. Absolute bans are void in EU, exposing the entire restriction clause.
- **AI-training silence on user content / outputs** — 2024+ users assume their inputs train your model and your outputs train competitors'. State clearly whether (a) licensee inputs train licensor models, (b) licensor outputs may be used to train licensee models, (c) outputs are licensee-owned or licensor-owned.
- **OSS attribution buried or stale** — copyleft auto-terminates on breach; missing attribution for a single MIT component can trigger termination of the entire grant. Ship a current NOTICES file and verify it on every release.
- **AGPL component in SaaS without disclosure** — using AGPL code to power your service triggers the network-use copyleft. Either license commercially, replace, or open-source the corresponding source.
- **"Perpetual" with no version qualifier** — does perpetual mean v1.0 forever, or every future version? Without a version-lock or maintenance-tied clause, licensors face indefinite update obligations and licensees face surprise sunsets.
- **Audit rights with no notice or scope cap** — surprise audits + access to all financial records reads as oppressive and gets struck. Use 30-day notice, business-hours, scope-limited to license usage, NDA-bound auditor.

## Handoff

- **To Cloak**: telemetry and usage-data implementation. Send EULA telemetry clause and request data-flow mapping, opt-out implementation, and privacy-policy alignment.
- **To Oath**: framework mapping — EULA ↔ SOC2 (license-mgmt control), ISO 27001 A.5.32 (IP), export-control program (EAR/OFAC). Send clause list and request control gap analysis.
- **To Canon**: OSS-license codebase audit. Send dependency manifest and EULA's OSS notice annex; request mismatch detection (e.g., AGPL dep claimed as MIT).
- **To Builder**: license-key system, telemetry kill-switch, audit-log endpoints, OSS notices generator. Spec the SLAs and acceptance criteria from EULA terms.
- **To Prose**: plain-language summary of restrictions for in-product display ("what you can/cannot do with this software"). Send the restriction clause and target reading level.
- **To Scribe**: EULA delta documentation for version-to-version change logs and customer-facing change summaries.
