# GraphQL & OpenAPI Specification Anti-Patterns

> GraphQLスキーマ設計、OpenAPI仕様構造、API仕様品質の失敗パターン
>
> **2026-05 baseline**: GraphQL **September 2025 spec edition**（[spec.graphql.org/September2025](https://spec.graphql.org/September2025/), October 2021 以来 4 年ぶりのフル仕様改訂）が現在の参照。Schema Coordinates、@oneOf input objects、executable-document descriptions、Unicode 完全対応を追加。Apollo Federation **2.10**（2025-02）が現行最小推奨バージョン（明示的 `@link` バージョニング必須、`@connect`/`@source` Connectors の前提）。OpenAPI 側は **3.2.0**（2025-09-23）が現行ターゲット、JSON Schema Draft 2020-12 dialect 維持。

## 1. GraphQLスキーマ設計 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **GQ-01** | **N+1 Query Problem（N+1クエリ問題）** | リスト内の各アイテムで子リゾルバが個別DB呼出 | クエリ実行時間がアイテム数に比例、DB負荷急増 | DataLoader（バッチ+キャッシュ）でフィールド境界のN+1を解消 |
| **GQ-02** | **No Depth Limiting（深度制限なし）** | 循環参照でネスト無制限のクエリが可能 | 悪意あるクエリでサーバークラッシュ、DoS脆弱性 | `graphql-depth-limit`でネスト深度制限、クエリコスト分析 |
| **GQ-03** | **Nullable by Default（デフォルトnullable）** | 全フィールドがデフォルトでnullを返却可能 | フロントエンドがnullチェックだらけ、意図しないnullでUI崩壊 | 必須フィールドに`!`マーカー: `name: String!`、nullは明示的な設計判断のみ |
| **GQ-04** | **No Pagination Default（ページネーションデフォルトなし）** | リストクエリにlimit未設定で全件返却可能 | 数百万件取得でクライアント/サーバーともにクラッシュ | スキーマ設計時にデフォルトlimit設定、Connection/Edgesパターン推奨 |
| **GQ-05** | **Lengthy Mutation Arguments（冗長なMutation引数）** | Mutationに個別引数を大量列挙 | 引数追加でシグネチャ破壊、可読性低下 | Input Object Type: `input CreateUserInput { name: String!, email: String! }` |
| **GQ-06** | **Insufficient Mutation Response（不十分なMutation応答）** | Mutationが最小限のデータのみ返却 | 更新後に追加クエリが必要、不要なネットワークラウンドトリップ | Mutation応答で変更されたデータを完全に返却、クライアントのローカルステート即時更新 |
| **GQ-07** | **No Schema Documentation（スキーマ文書化なし）** | 型・フィールドにdescription未記述 | GraphiQL/Playgroundの自動ドキュメントが空、開発者が意味を推測 | 全型・フィールドにdescription string追加、自動ドキュメント生成活用 |

---

## 2. GraphQLパフォーマンスの罠

```
パフォーマンスの失敗:

  ❌ Over-Fetching at Resolver Level（リゾルバレベルの過剰取得）:
    → リゾルバがクライアント要求以上のデータをDBから取得
    → 対策: フィールドレベルのデータ取得最適化、requested fieldsの確認

  ❌ No Caching Strategy（キャッシュ戦略なし）:
    → リゾルバが毎回DBアクセス、頻繁にアクセスされるデータも未キャッシュ
    → 対策: インメモリキャッシュ/分散キャッシュ、DataLoaderのキャッシュ活用

  ❌ Query Complexity Ignorance（クエリ複雑度無視）:
    → 複雑なネストクエリのコスト計算なし
    → 対策: クエリコスト分析、複雑度制限、タイムアウト設定

  ❌ No Persisted Queries（永続クエリ未使用）:
    → 毎回フルクエリ文字列を送信
    → 対策: 永続クエリ/APQ（Automatic Persisted Queries）でハッシュのみ送信

  ❌ Schema Stitching Without Planning（無計画なスキーマスティッチング）:
    → マイクロサービスのスキーマを無計画に結合
    → 互換性問題、名前衝突、パフォーマンス劣化
    → 対策: Federation（Apollo Federation等）による計画的な統合
```

---

## 3. OpenAPI仕様のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **OA-01** | **Post-Hoc Spec Generation（事後仕様生成）** | 実装完了後にコードからOpenAPI仕様を自動生成 | 仕様が不完全、examples欠如、設計意図消失 | Design-First: 仕様→モック→レビュー→実装→契約テスト |
| **OA-02** | **Internal Naming Leak（内部命名漏洩）** | 内部の略語・ビジネスロジック名がそのまま仕様に | 外部開発者が `GET /api/txn_proc/{boid}` を理解不能 | 公開向けのクリーンな命名、internal/external APIの分離 |
| **OA-03** | **No Security Scheme Context（セキュリティ定義の文脈なし）** | OAuth/APIキーを宣言するが、スコープや粒度が不明 | 監査では合格するが実運用で権限制御が機能しない | エンドポイント別のスコープ定義、セキュリティ要件の文脈的記述 |
| **OA-04** | **Missing Examples（サンプル欠如）** | リクエスト/レスポンスのexampleが未定義 | モックサーバーが空応答、開発者がAPI動作を推測 | 全エンドポイントにrequest/response例、エッジケースの例も含める |
| **OA-05** | **Loose Validation（バリデーション緩い）** | required/readOnly/writeOnly/pattern未使用 | あらゆる入力が通過、実行時エラーで初めて発覚 | min/max/pattern/enum/required等のバリデーション属性を厳格に定義 |
| **OA-06** | **Monolithic Spec File（モノリス仕様ファイル）** | 数千行の単一OpenAPIファイル | レビュー困難、merge衝突多発、チーム間のコラボ阻害 | components/paths/schemasを分割ファイルに、`$ref`で結合 |

---

## 4. REST vs GraphQL vs gRPC 選定の罠

```
選定ミスのパターン:

  ❌ GraphQL for Simple CRUD（単純CRUDにGraphQL）:
    → シンプルなリソースCRUDにGraphQLの複雑さを導入
    → スキーマ管理・キャッシュ戦略のオーバーヘッド
    → 対策: 単純CRUD → REST、複雑なデータ取得パターン → GraphQL

  ❌ REST for Real-Time（リアルタイムにREST）:
    → ポーリングで擬似リアルタイムを実現
    → 帯域浪費、レイテンシ、サーバー負荷
    → 対策: リアルタイム → WebSocket/SSE、双方向ストリーミング → gRPC

  ❌ gRPC for Public APIs（公開APIにgRPC）:
    → ブラウザから直接利用不能、ツールチェーン要求
    → 対策: 内部マイクロサービス間 → gRPC、公開API → REST or GraphQL

  ❌ Mixing Without Gateway（ゲートウェイなしの混在）:
    → REST + GraphQL + gRPCが統一的なエントリポイントなく混在
    → 対策: API Gatewayで統一エントリポイント、プロトコル変換
```

---

## 5. Custom Scalar & Enum設計

```
型設計の失敗:

  ❌ String for Everything（全てString型）:
    → 日付、メール、URL、金額を全てString型で定義
    → バリデーションがリゾルバ依存、スキーマレベルで型安全性なし
    → 対策: カスタムスカラー定義（Date, Email, URL, Money）

  ❌ Boolean for Multi-State（多状態にBoolean）:
    → 将来3つ以上の状態になる可能性があるのにBooleanで定義
    → 対策: Enum使用: `enum OrderStatus { PENDING, PROCESSING, SHIPPED, DELIVERED }`

  ❌ No Format Specification（フォーマット未指定）:
    → OpenAPIで`type: string`のみ、`format`未指定
    → 対策: `format: date-time`, `format: email`, `format: uri`で明確化
```

---

## 6. Gateway との連携

```
Gateway での活用:
  1. SURVEY フェーズで GQ-01〜07 / OA-01〜06 のスキーマ/仕様スクリーニング
  2. PLAN フェーズでGraphQL/REST/gRPC選定の妥当性チェック
  3. VERIFY フェーズでOpenAPI仕様の品質監査
  4. PRESENT フェーズでスキーマ改善提案

品質ゲート:
  - GraphQLにDataLoader未使用 → N+1解消提案（GQ-01 防止）
  - 深度制限未設定 → graphql-depth-limit導入（GQ-02 防止）
  - OpenAPI examples未定義 → サンプル追加提案（OA-04 防止）
  - 仕様が実装後生成 → Design-First移行提案（OA-01 防止）
  - バリデーション属性未使用 → required/pattern/enum追加（OA-05 防止）
  - 単一巨大仕様ファイル → 分割+$ref構造化提案（OA-06 防止）
  - 全フィールドString型 → カスタムスカラー/format追加（型設計 防止）
```

---

## 7. Apollo Federation: v1 vs v2 vs v2.10+

| Feature | Federation v1 | Federation v2 | Federation v2.10+ (2025-02) |
|---------|--------------|--------------|---------------------------|
| Composition | `@apollo/gateway` only | `@apollo/composition` (standalone) | Rewritten composition engine — descriptive errors, composition hints for query planning |
| `@key` directive | Single subgraph owns entity | Multiple subgraphs can extend entity with `@key(resolvable: false)` | Same; required to be stable identifiers |
| `@extends` | Required for entity extension | Not needed — implicit extension | Not needed |
| `@shareable` | Not available | Fields shared across subgraphs must be marked `@shareable` | Same |
| `@override` | Not available | One subgraph can override another's field ownership | Same |
| `@inaccessible` | Not available | Mark fields hidden from supergraph consumers | Same |
| Link import | Not available | `@link` directive for importing external definitions | **MANDATORY** — every subgraph must declare `@link(url: "https://specs.apollo.dev/federation/v2.x")` |
| Connectors | Not available | Not available | **`@connect` / `@source`** — wrap REST endpoints / AI tools as subgraph fields (prerequisite: Federation 2.10) |

### When to Use Federation vs REST

| Criteria | Use GraphQL Federation | Use REST |
|----------|----------------------|---------|
| Data shape | Complex, nested, cross-service entities | Simple, flat resource per endpoint |
| Client variety | Many clients with different field needs | One or few clients with fixed shapes |
| Team structure | Multiple teams owning schema fragments | Single team or simple CRUD service |
| Caching | Willing to invest in query-level caching | HTTP response caching sufficient |
| Real-time | Subscriptions needed across subgraphs | Polling or WebSocket simpler |
| Operations maturity | Can invest in schema governance tooling | Standard HTTP monitoring sufficient |

### Subgraph Design Rules

1. **Single responsibility**: Each subgraph owns one domain (users, orders, catalog) — no cross-domain mutations.
2. **Entity key stability**: `@key` fields must be stable identifiers (avoid mutable fields like `email`).
3. **No circular dependencies**: Subgraph A should not require data from Subgraph B to resolve what Subgraph B also needs from A.
4. **Define entities at their source of truth**: Only the owning subgraph should define the full entity; others use `@key(resolvable: false)` references.
5. **Avoid schema sprawl**: Federation does not eliminate the need for schema review — all subgraph changes go through composition validation.

---

**Source:** [LogRocket: Anti-patterns in GraphQL Schema Design](https://blog.logrocket.com/anti-patterns-graphql-schema-design/) · [Composite Code: Top 10 GraphQL Anti-patterns](https://compositecode.blog/2023/08/02/top-10-graphql-anti-patterns-ime-the-horror/) · [Medium: GraphQL at Scale — 9 Anti-Patterns](https://medium.com/@connect.hashblock/graphql-at-scale-9-anti-patterns-faster-fixes-5146a1db9db8) · [Medium: Stop Shipping Fragile APIs — Advanced OpenAPI Best Practices](https://medium.com/@yasaswinitatikonda1/stop-shipping-fragile-apis-the-advanced-openapi-best-practices-every-engineer-should-know-de1fd311cf91) · [APIMatic: 14 Best Practices for OpenAPI](https://www.apimatic.io/blog/2022/11/14-best-practices-to-write-openapi-for-better-api-consumption) · [DEV.to: 10 OpenAPI Best Practices](https://dev.to/hsmall/10-openapi-best-practices-that-elevate-your-api-game-2hpj)
