# Review Patterns

**Purpose:** Catalog of design patterns for legal document review.
**Read when:** Selecting a review approach or designing a report structure.

---

## Pattern 1: Single Document Review

**When to use:** Reviewing a single legal document in isolation.

```
SCOPE → SCAN → ASSESS → REPORT → SUGGEST
```

### Steps
1. **SCOPE**: Identify document type, jurisdiction, and target service.
2. **SCAN**: Walk the relevant checklist (`legal-checklists.md`) clause by clause.
3. **ASSESS**: Assign a risk level to each clause and identify missing ones.
4. **REPORT**: Produce a structured report.
5. **SUGGEST**: Propose concrete amendments and additional clauses.

---

## Pattern 2: Cross-Document Consistency Review

**When to use:** Verifying consistency across multiple documents such as Terms of Service and Privacy Policy.

```
SCOPE → SCAN (per document) → CROSS-CHECK → REPORT → SUGGEST
```

### Check points
- Personal-information handling described in ToS and Privacy Policy does not contradict.
- Scope of disclaimers aligns between ToS and Tokushoho notation.
- Governing-law and jurisdiction clauses are uniform across all documents.
- Term definitions are consistent across documents.
- Service name and business-operator name match.

### Consistency Matrix

```markdown
| 項目 | 利用規約 | プライバシーポリシー | 特商法表記 | 整合性 |
|------|---------|-------------------|-----------|--------|
| 事業者名 | ○ 記載あり | ○ 記載あり | ○ 記載あり | ✅ |
| データ保持期間 | 記載なし | 6ヶ月 | - | ⚠ 利用規約に未記載 |
| 第三者提供 | 「提供しない」 | 「広告目的で提供」 | - | ❌ 矛盾 |
```

---

## Pattern 3: Pre-Launch Review

**When to use:** Comprehensive legal-document check prior to launching a new service.

```
INVENTORY → SCOPE → SCAN (all documents) → CROSS-CHECK → GAP-ANALYSIS → REPORT
```

### Document inventory
1. Terms of Service — required
2. Privacy Policy — required
3. Tokushoho notation (特定商取引法に基づく表記) — required for paid services
4. Cookie Policy — recommended for web services
5. Community Guidelines — recommended when UGC is present
6. SLA — recommended for B2B SaaS
7. DPA (Data Processing Agreement) — required for GDPR compliance

---

## Pattern 4: Compliance Delta Review

**When to use:** Assessing readiness against a legal amendment or new regulation.

```
IDENTIFY (amendment) → MAP (impact scope) → GAP (delta vs. current docs) → SUGGEST (fixes)
```

### Steps
1. Organize the amendment's requirements.
2. Map the corresponding clauses in the current documents.
3. Identify gaps between requirements and current text.
4. Propose concrete amendments.

---

## Pattern 5: Industry-Specific Review

**When to use:** Industry-specific regulation applies.

### Additional check items by industry

| Industry | Additional statutes | Focus areas |
|----------|---------------------|-------------|
| Finance | 金融商品取引法, 貸金業法 | Risk disclosure, suitability principle |
| Healthcare | 医薬品医療機器等法, 医師法 | Handling of medical information, disclaimers |
| Education | 学校教育法 | Protection of minors, guardian consent |
| Real estate | 宅建業法 | Important-matters explanation |
| Food service | 食品衛生法, 景品表示法 | Allergy labeling, exaggerated advertising |
| Games | 景品表示法, 資金決済法 | Gacha-probability disclosure, virtual currency |

For prohibitions during review, see SKILL.md → Boundaries → Never.
