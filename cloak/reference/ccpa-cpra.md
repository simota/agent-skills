# CCPA / CPRA Compliance Reference

Purpose: Implementation guidance for the California Consumer Privacy Act (CCPA, 2018) as amended by the California Privacy Rights Act (CPRA, 2020, fully effective Jan 2023) and the 2026 ADMT/risk-assessment regulations. Covers consumer rights automation, opt-out signal handling (GPC), Sensitive Personal Information (SPI) limitation, and the service-provider/contractor/third-party distinction that determines contractual obligations and disclosure thresholds.

## Scope Boundary

- **cloak `ccpa`**: California-specific implementation (consumer rights endpoints, GPC honoring, "Do Not Sell or Share" link, SPI limit-use mechanism, service-provider contracts).
- **cloak `gdpr` (sibling)**: EU regime — opt-in/lawful-basis model. CCPA is opt-out by default; do not conflate.
- **cloak `pii` (sibling)**: detection. CCPA `ccpa` consumes a PII inventory but enforces rights/disclosure on top of it.
- **cloak `consent` (sibling)**: consent-capture UI patterns. CCPA opt-out flows live here when scoped to CA users.
- **cloak `dpia` (sibling)**: CCPA risk assessments (selling/sharing PI, SPI, ADMT, biometric) are formally documented in `dpia`; `ccpa` only flags when one is required.
- **canon `gdpr` / standard compliance (elsewhere)**: standard checklists across regulations. `ccpa` produces actionable code, not audit narrative.
- **crypt (elsewhere)**: encryption primitives backing CCPA's "reasonable security" duty. Cloak references; Crypt designs.
- **clause (elsewhere)**: legal review of Privacy Policy clauses, MSA addenda, DPA language. Cloak emits the technical surface; Clause approves the prose.

## Workflow

```
DISCOVER  →  identify CA-resident data subjects, SPI fields, sale/share flows,
          →  third-party tags, ADMT touchpoints

CLASSIFY  →  bucket processors as service provider | contractor | third party
          →  flag SPI categories triggering limit-use right

MAP       →  trace PI → service providers (contract-bound) vs third parties (sale/share)
          →  GPC ingress → consumer-rights state store → downstream propagation

ASSESS    →  rights coverage (know/delete/correct/opt-out/limit), GPC honoring,
          →  visible confirmation, 2026 risk-assessment triggers, ADMT readiness

REMEDIATE →  /ccpa/opt-out, /ccpa/access, /ccpa/delete, /ccpa/correct, /ccpa/limit-spi
          →  GPC header parser + visible "Opt-Out Request Honored" UI
          →  contract templates (1798.140(ag) service provider, (j) contractor)

VERIFY    →  45-day SLA timers, authorized-agent flow, minor opt-in (<16),
          →  do-not-sell link present site-wide, financial incentive disclosure
```

## Consumer Rights (CCPA + CPRA)

| Right | Statute | Trigger | SLA | Notes |
|-------|---------|---------|-----|-------|
| Know (categories + specific pieces) | §1798.100, §1798.110 | Verifiable consumer request | 45 days (+45 ext.) | 12-month lookback waived by CPRA — now full history |
| Delete | §1798.105 | Verifiable consumer request | 45 days | 9 enumerated exceptions (security, legal, free speech, etc.) |
| Correct | §1798.106 | CPRA addition | 45 days | Must propagate to service providers |
| Opt-out of Sale or Sharing | §1798.120, §1798.135 | Single click; GPC signal | Effective immediately; 15 days to propagate | "Sharing" = cross-context behavioral advertising |
| Limit Use of Sensitive PI | §1798.121 | SPI processed beyond §7027 narrow purposes | Effective immediately | Required link if SPI used for inferences |
| Non-discrimination | §1798.125 | Any rights exercise | — | Financial incentives allowed if disclosed and reasonably related to value |
| Opt-out of ADMT | 2026 Regs §7220 | Significant decisions, profiling | Pre-use notice + opt-out + appeal | Effective Jan 1 2026 |
| Data portability | §1798.100(d) | Subset of right-to-know | 45 days | Machine-readable, structured |

## Sensitive Personal Information (SPI)

| Category | Examples | Limit-Use Trigger |
|----------|----------|-------------------|
| Government IDs | SSN, driver's license, passport, state ID | Always |
| Account credentials | Username + password, security Q&A | Always |
| Financial | Account number + access code, debit/credit + CVV | Always |
| Precise geolocation | <1,850 ft (~564 m) radius | Always |
| Racial / ethnic origin | Self-reported or inferred | Always |
| Religious / philosophical beliefs | — | Always |
| Union membership | — | Always |
| Communications content | Mail, email, text content (non-addressee) | Always |
| Genetic / biometric / health | DNA, fingerprint, face geometry, medical | Always |
| Sex life / sexual orientation | — | Always |

**Narrow-purpose exemptions** (§7027(m)): perform requested service, prevent fraud/security incidents, ensure physical safety, short-term transient use, perform internal services, comply with law, verify/maintain quality. Anything else triggers the Limit-Use link.

## Service Provider vs Contractor vs Third Party

| Entity | Definition | Key contract terms | Disclosure obligation |
|--------|-----------|--------------------|-----------------------|
| Service Provider §1798.140(ag) | Processes PI on business's behalf for business purpose | No sale/share, no combining across clients, certify compliance, allow audits | Disclosed but not "sale" |
| Contractor §1798.140(j) | Same role, distinct definition for non-processor recipients | Same as service provider | Disclosed but not "sale" |
| Third Party §1798.140(ai) | Anyone receiving PI not as service provider/contractor | Sale/share — opt-out applies | Disclosed as sale/share |

**Failure to bind = automatic third-party classification.** Sephora ($1.2M, 2022) was the first major settlement: pixel/cookie sharing without opt-out treated as sale.

## GPC (Global Privacy Control)

| Aspect | Requirement |
|--------|-------------|
| Detection | Read `Sec-GPC: 1` HTTP request header on every page load |
| Honor scope | Treat as opt-out of sale/sharing AND opt-out of cross-context behavioral advertising |
| Propagation | Apply to known-user identity if logged in; persist across sessions |
| Visible confirmation (2026 CA Regs) | Display "Opt-Out Request Honored" or equivalent when GPC processed |
| Conflict with cookie banner | GPC overrides ambiguous banner state; never re-prompt |
| Browser support (2027) | AB 566 — all CA-distributed browsers must include GPC by Jan 1 2027 |

Twelve states require GPC honoring by Jan 1 2026 (CA, CO, CT, DE, NJ, NH, OR, MN, MT, TX implicit, others). Cloak's `ccpa` recipe assumes CA semantics by default; widen scope when other states apply.

## 2026 Regulations — ADMT, Risk Assessment, Cybersecurity Audit

| Obligation | Trigger | Deliverable |
|------------|---------|-------------|
| ADMT pre-use notice | Significant decision use | Plain-language description, logic, opt-out link |
| ADMT opt-out | Same | Functional channel — appeal to human review |
| ADMT access | Same | Decision-specific output, key reasons, role of input data |
| Risk Assessment | Selling/sharing PI, SPI processing, ADMT, biometric processing, training AI on PI | Documented benefits/risks; submit abbreviated version to CPPA |
| Cybersecurity Audit | Threshold business + high-risk processing | Annual independent audit; certified to CPPA |
| DROP — DELETE Request and Opt-out Platform | Data brokers | Single-channel deletion via centralized platform |

## Enforcement Snapshot

| Penalty | Amount |
|---------|--------|
| Per unintentional violation | $2,663 |
| Per intentional or minor-related violation | $7,988 |
| Statutory damages (data breach, private right) | $107–$799 per consumer per incident |

Notable actions: Sephora $1.2M (2022, sale without opt-out), DoorDash $375K (2024, sale to ad cooperative), Tractor Supply $1.35M (2024, GPC failure), Honda $632K (2024, dark patterns + opt-out friction).

## Anti-Patterns

- **Treating "Do Not Sell" as a sale-only flag** — CPRA added "or Share" for cross-context behavioral ads; pixel/tag-based ad personalization is sharing even if no money changes hands.
- **One-link policy footers** — both "Do Not Sell or Share" and "Limit the Use of My Sensitive PI" must be present (or one combined link with both rights). Hiding either is a violation.
- **Asking the user to log in to opt out** — opt-out must be available without authentication; only verification of *identity-tied* requests (delete/access/correct) requires login.
- **Honoring GPC silently** — 2026 CA regs require visible confirmation. Set `data-gpc="honored"` and surface a banner.
- **Skipping service-provider contracts** — without the §1798.140(ag) contractual flow-down, the vendor is a third party and every transfer is a sale.
- **Treating CCPA as GDPR-lite** — opt-out vs opt-in inverts the default. Pre-checking marketing in CA is fine; pre-sharing with ad networks is not.
- **45-day SLA without queue** — manual response to high-volume DSARs misses windows. Build verifiable-request intake → identity-proof → workflow with timer.
- **SPI inference without limit-use link** — using ZIP+name to infer ethnicity for ad targeting triggers SPI even if the source field wasn't SPI. Inference creates SPI.
- **Ignoring authorized agents** — CCPA allows power-of-attorney delegation; refusing agent-submitted requests is an automatic violation.

## Handoff

- **To Crypt**: encryption design for SPI at rest/in transit (CCPA "reasonable security" defense). Required for credentials, financial, geolocation, biometric.
- **To Canon**: CCPA standard checklist cross-validation against ISO/IEC 27701 PIMS controls; gap matrix.
- **To Clause**: Privacy Policy clause review — disclose categories, purposes, retention, sale/share, SPI, rights. Tokushoho-style equivalents for CA-targeted commerce.
- **To Comply**: SOC 2 / ISO 27001 mapping for CCPA risk-assessment + cybersecurity-audit controls; evidence package.
- **To Builder**: Implement opt-out endpoint, GPC parser, SPI limit-use toggle, ADMT pre-use notice, deletion-propagation queue.
- **To Schema**: tag SPI fields with `spi_category` annotation; persist `gpc_honored_at`, `opt_out_status`, `limit_spi_status` per consumer.
- **To Gateway**: header-level GPC detection middleware; consent-state propagation to downstream services.
