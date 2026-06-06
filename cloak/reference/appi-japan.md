# APPI (Japan) Compliance Reference

Purpose: Implementation guidance for Japan's Act on the Protection of Personal Information (個人情報保護法, APPI) — original 2003, major amendments 2017, 2022, and the 2024 amendment cycle. Covers the three-tier data taxonomy (個人情報 / 仮名加工情報 / 匿名加工情報), Article 24 cross-border transfer regime, Article 23 opt-out for third-party provision, PPC notification thresholds, and 要配慮個人情報 (special-care PI) handling.

## Scope Boundary

- **cloak `appi`**: Japan-specific implementation (PPC reporting, three-tier taxonomy, Article 24 transfer, Article 23 opt-out filing, 要配慮個人情報 explicit consent).
- **cloak `gdpr` (sibling)**: EU regime — overlaps on consent and DSAR shape, diverges on retention philosophy and lawful basis. APPI uses "purpose of utilization" (利用目的), not GDPR's six bases.
- **cloak `ccpa` (sibling)**: California — opt-out by default. APPI is a hybrid: opt-in for sensitive, opt-in for third-party transfer (with Art. 23 opt-out exception), purpose-bound use otherwise.
- **cloak `pseudonymize` (sibling)**: techniques. `appi` consumes pseudonymization output and applies the 仮名加工情報 / 匿名加工情報 distinction to determine downstream obligations.
- **cloak `dpia` (sibling)**: APPI does not mandate DPIA but PPC strongly recommends for large-scale or special-care processing.
- **canon (elsewhere)**: standards-level audit. `appi` produces operational compliance code.
- **crypt (elsewhere)**: encryption design backing the "appropriate safety management" duty (Art. 23 安全管理措置).
- **clause (elsewhere)**: 個人情報保護方針 (Privacy Policy in Japanese), 利用目的の特定 wording, Tokushoho disclosures for EC.
- **comply (elsewhere)**: ISMS / Pマーク (Privacy Mark) certification mapping; APPI is law, Pマーク is voluntary certification.

## Workflow

```
DISCOVER  →  inventory 個人情報 / 個人データ / 保有個人データ
          →  flag 要配慮個人情報 (sensitive); identify cross-border processors

CLASSIFY  →  three-tier taxonomy: 個人情報 vs 仮名加工情報 vs 匿名加工情報
          →  determine 利用目的 (purpose of utilization) for each field set

MAP       →  domestic third-party transfers (Art. 23 opt-out filing path)
          →  cross-border transfers (Art. 24 — equivalent country list / SCC-equivalent / consent)

ASSESS    →  consent surface for 要配慮個人情報, breach-notification thresholds (1k records or sensitive),
          →  PPC reporting timeline (速やか — promptly), 3-year retention limit on access logs

REMEDIATE →  consent UI for 要配慮; opt-out filing form for Art. 23;
          →  cross-border addendum templates; pseudonymization pipeline for 仮名加工情報 reuse;
          →  anonymization pipeline + deletion of intermediate keys for 匿名加工情報

VERIFY    →  PPC report channel tested, 利用目的変更 re-consent flow, retention auto-purge,
          →  third-party recipient registry maintained for 3 years (Art. 26)
```

## Three-Tier Data Taxonomy

| Tier | Japanese | Definition | Re-identification | Permitted Use | Disclosure Duty |
|------|----------|-----------|-------------------|---------------|-----------------|
| Personal Information | 個人情報 | Identifies a living individual (incl. by combination) | N/A | Within stated purpose | Full DSAR rights |
| Pseudonymized Information | 仮名加工情報 | Cannot identify individual without additional info | Possible with key | Internal analytics; no third-party transfer except processors | DSAR exempt internally |
| Anonymized Information | 匿名加工情報 | Cannot identify individual; cannot be restored | Impossible (key destroyed) | Free use incl. third-party | DSAR exempt |

**Critical distinction**: 仮名加工情報 retains the key (held separately, access-controlled); 匿名加工情報 destroys the key irreversibly. Cloak must verify operationally — many implementations claim 匿名 but retain reversible mappings, making them 仮名 in fact.

**仮名加工情報 standards** (PPC rules): remove direct identifiers, remove descriptions enabling identification, remove individual identification codes (My Number, biometric IDs).

**匿名加工情報 standards**: same as above plus mandatory technical evaluation that re-identification is infeasible; public disclosure of categories created (Art. 43).

## 要配慮個人情報 (Special-Care Personal Information)

| Category | Examples |
|----------|----------|
| Race | 人種 (excluding nationality and skin color alone) |
| Creed | 信条 — religious or political beliefs |
| Social status | 社会的身分 — birth-based class |
| Medical history | 病歴 |
| Criminal record | 犯罪の経歴 |
| Crime victim status | 犯罪被害事実 |
| Physical / mental disability | 心身の機能の障害 |
| Health checkup results | 健康診断等の結果 |
| Medical guidance / treatment | 医師等による指導・診療・調剤 |
| Arrest / search / seizure | 刑事手続が行われたこと |
| Juvenile protection record | 少年保護事件の手続が行われたこと |

Acquisition and third-party transfer require **explicit prior consent** — opt-out under Art. 23 is unavailable.

## Cross-Border Transfer (Article 24)

| Path | Requirement |
|------|-------------|
| Equivalent-protection country | EU and UK currently designated; transfer treated as domestic |
| SCC-equivalent contract | Bind recipient to APPI-aligned standards; document retention 3 years |
| Subject's prior consent | Disclose recipient country, that country's privacy regime summary, and recipient's safeguards (post-2022 amendment requirement) |

**2022 amendment teeth**: consent-based path now requires the *substance* of the foreign regime to be disclosed — generic "we may transfer abroad" no longer suffices. PPC publishes country fact-sheets businesses can reference.

## Article 23 — Opt-Out for Third-Party Transfer

Domestic third-party transfer can use opt-out if all of the following are filed with PPC and disclosed to subjects:

| Item | Requirement |
|------|-------------|
| Categories of PI transferred | Specific list |
| Method of acquisition | Source description |
| Categories of recipients | Including geography |
| Method of transfer | Bulk, API, etc. |
| Subject's opt-out method | Functional channel |
| Date of opt-out filing | PPC submission date |

**Excluded** from opt-out path: 要配慮個人情報, illegally acquired PI, data acquired via opt-out from another business (no chain-opt-out).

## PPC Notification (Article 26)

| Trigger | Threshold | Timeline |
|---------|-----------|----------|
| Breach of 要配慮個人情報 | Any record | Promptly (速やか — interpreted ~3-5 days speculative report; 30 days confirmed report) |
| Breach with financial damage risk | Any record | Same |
| Breach involving illegal purpose | Any record | Same |
| Breach >1,000 records | All other PI | Same |

Plus subject notification (or public announcement if individual notice infeasible). Cloak's `appi` recipe must wire both PPC API/form path AND subject-notification template.

## 2024 Amendment Highlights

| Change | Effect |
|--------|--------|
| Class action enablement | Consumer organizations can sue on behalf of victims |
| Strengthened PPC investigative powers | On-site inspection, document seizure |
| Statutory damages (under discussion) | Currently actual-damage only; reform proposes statutory minimums |
| Child PI special protection | Under-18 explicit protections expanded |
| Cookie / web tracking explicit rules | Closer to ePrivacy-style consent for tracking |
| Cross-border tightening | Annual recipient verification required |

Reform is staged — track PPC quarterly notices for in-force dates.

## Anti-Patterns

- **Calling pseudonymized data 匿名加工** — keeping the mapping table anywhere makes it 仮名加工情報 with all the duties (no third-party transfer, internal-use-only). Auditors check key-destruction logs.
- **Generic "may transfer abroad" notice** — post-2022, the foreign regime substance must be disclosed. Insufficient notice voids consent.
- **Treating health-checkup results as ordinary PI** — corporate wellness data is 要配慮個人情報. Explicit consent required even for HR processing.
- **Single 利用目的 declaration covering everything** — purpose must be specific enough to predict use. "For business purposes" fails Art. 17 specificity.
- **Skipping the Art. 23 PPC filing for opt-out third-party transfer** — without filing, the legal basis is consent, not opt-out. Most ad-tech vendors get this wrong.
- **No retention limit on access logs** — Art. 26 requires 3-year retention of disclosure/correction request records; longer creates liability.
- **Conflating APPI with PIPL or PIPA** — China's PIPL and Korea's PIPA share vocabulary but diverge on consent granularity, transfer regime, and breach thresholds. Don't reuse Chinese/Korean templates verbatim.
- **Assuming 匿名加工情報 lets you skip privacy notice** — Art. 43 requires public disclosure of categories of anonymized information created and method.
- **Manual PPC reporting** — the 速やか standard implies operational readiness. Build the channel before the breach.

## Handoff

- **To Crypt**: encryption + key management for the 仮名加工情報 mapping table; key destruction protocol for 匿名加工情報 transition.
- **To Canon**: APPI ↔ ISO/IEC 27701 control mapping; Pマーク (JIS Q 15001) gap matrix when seeking certification.
- **To Clause**: 個人情報保護方針 (Privacy Policy) review in Japanese; 利用目的 specificity check; cross-border disclosure substance per 2022 standard.
- **To Comply**: ISMS scope alignment, Pマーク evidence package, audit trail design for PPC inspection.
- **To Builder**: PPC reporting endpoint, consent UI for 要配慮 categories, Art. 23 opt-out channel, transfer addendum signing flow.
- **To Schema**: tier annotations (`appi_tier: 個人 | 仮名 | 匿名`), 要配慮 flags, 利用目的 column-level metadata.
- **To Gateway**: cross-border-aware routing — block prohibited destinations at API edge.
