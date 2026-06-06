# REST API Design Anti-Patterns

> URL設計、HTTPメソッド、レスポンス設計、エラーハンドリング、ページネーションの失敗パターン
>
> **2026-05 更新**: RFC 9457 Problem Details (2023-07, obsoletes RFC 7807) と OpenAPI 3.2 (2025-09-23) を前提とする。RFC 6648 で `X-` ヘッダーは2012年に正式 deprecated — Standard Webhooks も `webhook-id` / `webhook-timestamp` / `webhook-signature` のように `X-` を捨てた。新規 API ヘッダーで `X-` プレフィックスを使うのは AD-08 アンチパターン相当。

## 1. REST API設計 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **AD-01** | **Verb-in-URL（URLに動詞）** | `/getUsers`, `/createOrder`のようにURLにアクション動詞を含める | URLがCRUD操作ごとに増殖、REST原則から逸脱 | リソース名詞のみ使用: `GET /users`, `POST /orders`、HTTPメソッドでアクションを表現 |
| **AD-02** | **POST for Everything（全てPOST）** | 検索・削除・更新も含め全操作にPOSTを使用 | キャッシュ不可、冪等性保証なし、ミドルウェア活用不能 | GET=取得、POST=作成、PUT=全更新、PATCH=部分更新、DELETE=削除を適切に使い分け |
| **AD-03** | **Inconsistent Naming（命名不統一）** | camelCase/snake_case/kebab-caseがAPIごとに混在 | 開発者の混乱、ドキュメント負担増、API採用率低下 | API Linter（Spectral/Vacuum）で命名規則を強制、スタイルガイドを事前策定 |
| **AD-04** | **Kitchen Sink Response（全部入りレスポンス）** | 全フィールドを常に返却、不要データでペイロード肥大 | レスポンス遅延、帯域浪費、クライアント側の不要なパース | Sparse fieldsets: `?fields=id,name,email`、必要最小限のデフォルト、関連リソースは別エンドポイント |
| **AD-05** | **Implementation Exposure（実装露出）** | DBテーブル名やカラム名がURLに露出 | `/api/database/tables/book_inventory/records`のような内部構造漏洩 | 抽象的なリソース名: `GET /api/books?available=true`、内部実装を隠蔽 |
| **AD-06** | **Excessive Nesting（過剰ネスト）** | `/companies/456/departments/2/employees/123/projects` | URL長大、関連リソースの探索困難 | 最大2階層: `/employees/123/projects` or `/projects?employeeId=123` |
| **AD-07** | **No Pagination（ページネーション欠如）** | 全レコードを一括返却、後からページネーション追加で全クライアント破壊 | 10,000件返却でタイムアウト、メモリ溢れ | 初期設計でページネーション組込: cursor-based推奨（大規模時）、offsetは小規模のみ |

---

## 2. エラーハンドリングのアンチパターン

```
エラー設計の失敗:

  ❌ Vague Error Messages（曖昧なエラーメッセージ）:
    → { "error": "An error occurred" } のみ返却
    → 開発者がデバッグ不能、サポート問い合わせ急増
    → 対策: RFC 7807 Problem Details形式、field/rule/acceptable valuesを含める

  ❌ 200 OK with Error Body（200で全エラー返却）:
    → HTTPステータスは常に200、ボディ内にerror情報
    → HTTPキャッシュ・ミドルウェア・監視ツールが正常と誤認
    → 対策: 適切なHTTPステータスコード使用（400/401/403/404/409/422/429/500）

  ❌ Status Code Misuse（ステータスコード誤用）:
    → バリデーションエラーに500、認証エラーに400を返却
    → クライアント側のエラーハンドリングロジック崩壊
    → 対策: 400=入力不正、401=未認証、403=権限不足、404=未発見、409=競合、422=処理不能、429=レート制限

  ❌ Inconsistent Error Format（エラーフォーマット不統一）:
    → エンドポイントごとにエラーJSONの構造が異なる
    → クライアントSDKでの統一的エラーハンドリング不能
    → 対策: 全エンドポイントで統一エラースキーマ、OpenAPIで定義

  ❌ No Error Catalog（エラーカタログ未整備）:
    → エラーコードの一覧・説明が未文書化
    → 同じエラーに異なるコード、重複エラー定義
    → 対策: エラーコード一覧（help_url付き）を公開、機械可読なエラーカタログ
```

---

## 3. レスポンス設計の罠

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **RD-01** | **Nullable vs Optional Confusion（null/optional混同）** | null値と未設定を区別せず、3状態ロジックが発生 | nullの意味が「未設定」「明示的null」「エラー」か不明 | optionalフィールドは省略、明示的null不要、OpenAPIでnullable/required明確化 |
| **RD-02** | **No HATEOAS（ハイパーメディア欠如）** | クライアントがURL構造をハードコード | API変更時に全クライアント修正、ワークフロー発見不能 | レスポンスにlinks/actionsを含め、動的ナビゲーション可能に |
| **RD-03** | **Hyrum's Law Ignorance（Hyrumの法則無視）** | 配列順序等の非文書化挙動にクライアントが依存 | ソート順変更で予期せぬクライアント破壊 | 全observable behaviorを文書化、契約外の挙動は保証しないことを明記 |
| **RD-04** | **No Idempotency Keys（冪等性キー未提供）** | POSTリクエストのリトライで重複作成 | ネットワークエラー後の再送で注文が2重に | Idempotency-Keyヘッダーの提供（Stripe方式） |

---

## 4. API設計哲学の罠

```
設計アプローチの失敗:

  ❌ Inside-Out Design（内部起点設計）:
    → DB構造やバックエンド実装からAPIを逆算
    → 消費者視点でない不自然なリソースモデル
    → 対策: Outside-In設計: 開発者ユーザーストーリーから開始、サンドボックス提供

  ❌ Over-Engineering（過剰設計）:
    → 未来の要件を全て先取りした複雑なAPI
    → 使いにくい、ドキュメント膨大、メンテナンス困難
    → 対策: 現在の要件にフォーカス、進化的設計、必要時に拡張

  ❌ Chatty API（おしゃべりAPI）:
    → 1画面表示に10+回のAPI呼出が必要
    → レイテンシ増大、モバイルでの体験悪化
    → 対策: 適切な粒度のリソース設計、BFF(Backend For Frontend)パターン検討

  ❌ God Endpoint（神エンドポイント）:
    → 1つのエンドポイントが全機能を処理
    → 複雑なパラメータ、テスト困難、スケール不能
    → 対策: 単一責任原則: 1エンドポイント=1リソース操作
```

---

## 5. Gateway との連携

```
Gateway での活用:
  1. SURVEY フェーズで AD-01〜07 のURL/メソッド設計スクリーニング
  2. PLAN フェーズでエラーハンドリング設計の品質チェック
  3. VERIFY フェーズでレスポンス設計の一貫性確認
  4. PRESENT フェーズで改善提案を含むAPI設計レポート

品質ゲート:
  - URL動詞検出 → リソース名詞化提案（AD-01 防止）
  - POST-only API検出 → HTTPメソッド適正化（AD-02 防止）
  - 命名規則不統一 → Linterルール追加提案（AD-03 防止）
  - ページネーション未実装 → cursor-based設計提案（AD-07 防止）
  - エラーレスポンス形式不統一 → RFC 7807統一フォーマット提案（Error 防止）
  - 200 OKエラーパターン → 適切なステータスコード使用提案（Error 防止）
  - 冪等性未対応POST → Idempotency-Key提案（RD-04 防止）
```

**Source:** [Zuplo: Common Pitfalls in RESTful API Design](https://zuplo.com/blog/2025/03/12/common-pitfalls-in-restful-api-design) · [Specmatic: API Design Anti-patterns](https://specmatic.io/appearance/how-to-identify-avoid-api-design-anti-patterns/) · [Milan Jovanovic: 5 Most Common REST API Design Mistakes](https://www.milanjovanovic.tech/blog/the-5-most-common-rest-api-design-mistakes-and-how-to-avoid-them) · [DEV.to: 7 API Design Mistakes](https://dev.to/maxxmini/7-api-design-mistakes-that-make-your-users-hate-you-and-how-to-fix-them-3722) · [Speakeasy: Errors Best Practices in REST API Design](https://www.speakeasy.com/api-design/errors)
