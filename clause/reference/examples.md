# Usage Examples

**Purpose:** Usage examples for the Clause agent.
**Read when:** You need a reference for output format or review granularity.

The example outputs below are Japanese because Clause produces Japanese review reports for Japan-jurisdiction documents. Adapt the language of the output to match the jurisdiction of the reviewed document.

---

## Example 1: SaaS Terms of Service review

### Input
```
Please review the Terms of Service for a SaaS project-management tool.
Target jurisdiction: Japan. B2B service.
```

### Output example

```markdown
## レビューレポート: プロジェクト管理ツール利用規約

**スコープ:** 日本法 / 利用規約 / B2B SaaS
**レビュー日:** 2026-04-12
**免責:** 本レポートは参考情報であり法的助言ではありません。重要な法的判断には弁護士にご相談ください。

### サマリー
- High: 2件 / Medium: 3件 / Low: 2件 / Info: 1件

### 発見事項

#### [H-01] 規約変更手続きの欠如
- **リスク:** High
- **該当条項:** 欠落
- **問題:** 規約変更時の通知手続き・猶予期間が定められていない。民法548条の4（定型約款の変更）の要件を満たさない可能性がある。
- **参照法令:** 民法 第548条の4
- **改善案:** 「変更の30日前までに通知し、異議がない場合は同意とみなす」等の変更手続条項を追加。

#### [H-02] 免責条項が広すぎる
- **リスク:** High
- **該当条項:** 第12条
- **問題:** 「一切の責任を負わない」という包括的免責は、消費者契約法8条により無効となる可能性がある。B2Bであっても下請法等の観点から注意が必要。
- **参照法令:** 消費者契約法 第8条
- **改善案:** 「故意または重過失による場合を除き」等の限定を付す。損害賠償の上限額を設定。

#### [M-01] データ取扱い条項の不足
- **リスク:** Medium
- **該当条項:** 第8条
- **問題:** サービス終了時のデータエクスポート・返還について明記されていない。
- **改善案:** データエクスポート期間（例: サービス終了後90日間）と形式を明記。

...
```

---

## Example 2: Privacy Policy GDPR compliance check

### Input
```
Please verify that our Privacy Policy complies with GDPR.
Global web service with users residing in the EU.
```

### Output example (excerpt)

```markdown
### GDPR 準拠チェック結果

| # | 要件 | 状態 | リスク | コメント |
|---|------|------|--------|---------|
| G-01 | 処理の法的根拠 | ❌ 欠落 | High | Art.6に基づく法的根拠の明示が必要 |
| G-02 | データ主体の権利 | ⚠ 不十分 | High | アクセス権のみ記載。消去権・ポータビリティ権が欠落 |
| G-03 | DPO情報 | ❌ 欠落 | Medium | DPO設置義務の有無を確認し、該当する場合は連絡先を記載 |
| G-04 | データポータビリティ | ❌ 欠落 | High | Art.20に基づくデータポータビリティ権の記載が必要 |
| G-05 | 忘れられる権利 | ❌ 欠落 | High | Art.17に基づく消去権の手続きを記載 |
| G-06 | 自動意思決定 | ✅ 充足 | - | プロファイリング非使用の旨が記載済み |
| G-07 | データ侵害通知 | ❌ 欠落 | High | 72時間以内の通知義務について記載が必要 |
| G-08 | 国際移転の保護措置 | ⚠ 不十分 | High | SCCまたは十分性認定の言及が必要 |

**充足率:** 2/8 (25%)
**判定:** GDPR 対応として大幅な改善が必要
```

---

## Example 3: Tokushoho notation check

### Input
```
Please verify the Specified Commercial Transactions Act (Tokushoho) notation for an e-commerce site.
```

### Output example (excerpt)

```markdown
### 特定商取引法表記チェック結果

| # | 項目 | 状態 | コメント |
|---|------|------|---------|
| S-01 | 事業者名 | ✅ | 株式会社○○ |
| S-02 | 代表者名 | ✅ | ○○太郎 |
| S-03 | 住所 | ⚠ | 番地まで記載されていない |
| S-04 | 電話番号 | ✅ | 03-XXXX-XXXX |
| S-05 | メールアドレス | ✅ | info@example.com |
| S-06 | 販売価格 | ⚠ | 税込表示の明記なし |
| S-07 | 送料 | ❌ | 記載なし |
| S-08 | 支払方法 | ✅ | クレジットカード、銀行振込 |
| S-09 | 引渡時期 | ❌ | 記載なし |
| S-10 | 返品ポリシー | ⚠ | 期間が不明確（「速やかに」） |

**充足率:** 5/12 (42%)
**High リスク欠落:** 2件 (送料、引渡時期)
```
