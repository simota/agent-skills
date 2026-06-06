# Legal Document Checklists

**Purpose:** Clause-coverage checklists for legal document review.
**Read when:** Verifying clause coverage during the SCAN phase.

---

## Terms of Service (利用規約) Checklist

### Required Clauses

| # | Clause | Risk (if missing) | Statute (Japan) |
|---|--------|-------------------|-----------------|
| T-01 | Service definition and scope | Medium | - |
| T-02 | Eligibility and age restrictions | High | 民法 第5条 (minor's legal acts) |
| T-03 | Account registration and management responsibility | Medium | - |
| T-04 | Fees and payment terms | High | 特商法 第11条 |
| T-05 | Prohibited conduct | Medium | - |
| T-06 | Intellectual property ownership | High | 著作権法 |
| T-07 | User-generated content (UGC) handling | High | 著作権法・プロバイダ責任制限法 |
| T-08 | Disclaimers and limitation of liability | High | 消費者契約法 第8条・第10条 |
| T-09 | Service change, suspension, and termination | Medium | - |
| T-10 | Procedure for amending the terms | High | 民法 第548条の4 (amendment of standard-form contracts) |
| T-11 | Contract termination and withdrawal | Medium | 消費者契約法 |
| T-12 | Governing law | Low | 法の適用に関する通則法 |
| T-13 | Dispute resolution (jurisdiction / ADR) | Low | 民事訴訟法 |
| T-14 | Anti-social-forces exclusion clause | Medium | 各都道府県暴力団排除条例 |
| T-15 | Severability clause | Low | - |

### Recommended Clauses

| # | Clause | When applicable |
|---|--------|-----------------|
| T-16 | Third-party service integrations | APIs / external integrations exist |
| T-17 | Beta / experimental-feature disclaimer | New-feature rollouts |
| T-18 | Data export / portability | SaaS / subscription |
| T-19 | SLA (service-level agreement) | B2B SaaS |
| T-20 | Force Majeure | Recommended for all services |

---

## Privacy Policy Checklist

### Japan (Act on Protection of Personal Information / 個人情報保護法)

| # | Clause | Risk (if missing) | Statute |
|---|--------|-------------------|---------|
| P-01 | Name and contact of the handling business operator | High | 個情法 第32条 |
| P-02 | Specification and notice of purpose of use | High | 個情法 第17条・第21条 |
| P-03 | Categories of personal information collected | High | 個情法 第21条 |
| P-04 | Third-party provision: whether and under what conditions | High | 個情法 第27条 |
| P-05 | Joint use: scope and purpose | Medium | 個情法 第27条第5項第3号 |
| P-06 | Provision to contractors / processors | Medium | 個情法 第25条 |
| P-07 | Handling disclosure and similar requests from data subjects | High | 個情法 第33条 |
| P-08 | Outline of safety management measures | Medium | 個情法 第23条 |
| P-09 | Use of cookies / external transmission | High | 電気通信事業法 第27条の12 |
| P-10 | Retention period of personal information | Medium | - |
| P-11 | International data transfers | High | 個情法 第28条 |
| P-12 | Handling of sensitive personal information (要配慮個人情報) | High | 個情法 第20条第2項 |
| P-13 | Children's personal information | Medium | - |
| P-14 | Notice procedure for policy changes | Medium | - |

### Additional GDPR Requirements

| # | Clause | Risk (if missing) | Reference |
|---|--------|-------------------|-----------|
| G-01 | Lawful basis for processing (Art. 6) | High | GDPR Art. 6 |
| G-02 | List of data-subject rights | High | GDPR Art. 12–22 |
| G-03 | DPO (Data Protection Officer) information | Medium | GDPR Art. 37–39 |
| G-04 | Right to data portability | High | GDPR Art. 20 |
| G-05 | Right to erasure ("right to be forgotten") | High | GDPR Art. 17 |
| G-06 | Automated decision-making and profiling | Medium | GDPR Art. 22 |
| G-07 | Data-breach notification (within 72 hours) | High | GDPR Art. 33 |
| G-08 | Safeguards for international transfers (SCC, etc.) | High | GDPR Art. 46 |

### Additional CCPA / CPRA Requirements

| # | Clause | Risk (if missing) |
|---|--------|-------------------|
| C-01 | Opt-out right for "sale of personal information" | High |
| C-02 | "Do Not Sell My Personal Information" link | High |
| C-03 | Disclosure of information categories from the last 12 months | Medium |
| C-04 | Non-discrimination against consumers | Medium |
| C-05 | Distinction between "sharing" and "selling" of information | Medium |

---

## Tokushoho Notation Checklist (特定商取引法に基づく表記)

| # | Item | Required / Recommended | Reference |
|---|------|------------------------|-----------|
| S-01 | Business operator's name (company or individual) | Required | 特商法 第11条第1号 |
| S-02 | Name of representative or responsible person | Required | 特商法 第11条 |
| S-03 | Address | Required | 特商法 第11条第2号 |
| S-04 | Telephone number | Required | 特商法 第11条第3号 |
| S-05 | Email address | Recommended | - |
| S-06 | Selling price (tax-inclusive display) | Required | 特商法 第11条第4号 |
| S-07 | Shipping fees and handling charges | Required | 特商法 第11条第4号 |
| S-08 | Payment methods and timing | Required | 特商法 第11条第5号 |
| S-09 | Product / service delivery timing | Required | 特商法 第11条第6号 |
| S-10 | Return and cancellation policy | Required | 特商法 第15条の3 |
| S-11 | Application withdrawal and termination conditions | Required | 特商法 第11条 |
| S-12 | Operating environment (digital content) | Conditionally required | 特商法 第11条 |

---

## Review Result Template

Use this Japanese template when producing the review output:

```markdown
## 条項網羅性チェック結果

**文書:** [文書名]
**チェックリスト:** [使用チェックリスト名]
**日付:** YYYY-MM-DD

| # | 条項 | 状態 | リスク | コメント |
|---|------|------|--------|---------|
| T-01 | サービスの定義 | ✅ 充足 | - | - |
| T-02 | 利用資格 | ⚠ 不十分 | Medium | 年齢制限の明記なし |
| T-03 | アカウント管理 | ❌ 欠落 | High | 条項の追加が必要 |

**充足率:** X/Y (Z%)
**High リスク欠落:** N件
```

---

## Dangerous Clause Patterns

Flag any of the following patterns as High risk:

| Pattern (source phrase) | Problem | Recommended fix |
|-------------------------|---------|-----------------|
| 「一切の責任を負わない」 | Likely invalid under 消費者契約法 第8条 | Limit liability to a reasonable scope |
| 「当社の判断で自由に変更」 | May conflict with 民法 第548条の4 | Specify amendment procedure and notice period |
| 「すべての権利を譲渡」(UGC) | Copyright concern and user pushback | Switch to a license-grant model |
| Third-party provision without consent | Violates 個情法 第27条 | Obtain consent or document an exempting ground |
| No cookie notice | Violates 電気通信事業法 第27条の12 | Add a banner aligned with the external-transmission rule |
| No governing-law / jurisdiction clause | Uncertainty in disputes | Add an explicit governing-law / jurisdiction clause |
