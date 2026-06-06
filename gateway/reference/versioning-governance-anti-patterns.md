# API Versioning & Governance Anti-Patterns

> バージョニング戦略、破壊的変更管理、OpenAPIスペック管理、APIガバナンスの失敗パターン
>
> **2026-05 baseline**: OpenAPI 3.2.0（2025-09-23 公開）が現在のターゲット。3.0/3.1 と完全後方互換のため既存仕様は無変更で valid。Stripe は 2024-09-30.`acacia` から **月次マイナー＋年2回 named major**（現行 `2026-04-22.dahlia`）の CalVer 運用に移行 — 月次は必ず additive。新規 SaaS で date-pinned versioning を採用する際は Stripe の運用ポリシーを参照する。**RFC 9745 Deprecation**（2025-03）が Standards Track として確定、構造化フィールド `Date` 型 (`Deprecation: @1727136000`) が canonical。

## 1. バージョニング 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **VG-01** | **No Versioning Strategy（バージョニング戦略なし）** | APIにバージョンの概念がなく、変更が直接反映 | 破壊的変更でクライアントが突然動作停止 | 初期設計時にバージョニング方式選定（URL path推奨）、セマンティックバージョニング |
| **VG-02** | **Over-Versioning（過剰バージョニング）** | 軽微な変更でもメジャーバージョンを発行 | v1→v2→v3→v7が数ヶ月で乱立、保守コスト爆発 | 破壊的変更のみバージョン発行、追加的変更は既存バージョン内で吸収 |
| **VG-03** | **No Deprecation Plan（非推奨化計画なし）** | 旧バージョンを告知なく突然削除 or 永久に放置 | クライアント破壊 or 古いバージョンが無期限に稼働 | 6ヶ月告知→12ヶ月移行支援→18-24ヶ月で削除、Deprecation/Sunsetヘッダー |
| **VG-04** | **Inconsistent Versioning Across Services（サービス間バージョン不統一）** | マイクロサービスごとに異なるバージョニング方式 | `/v1/users` + `?api_version=2` + `Accept: v3` が混在 | 組織横断で統一バージョニングポリシー策定 |
| **VG-05** | **Silent Breaking Changes（無通知破壊的変更）** | 消費者への通知なく互換性を壊す変更をデプロイ | クライアントアプリが突然エラー、信頼喪失 | 変更ログ公開、breaking change検出ツール（oasdiff）、消費者への通知フロー |
| **VG-06** | **Spec Drift（仕様と実装の乖離）** | OpenAPI仕様と実際のAPI動作が不一致 | 70%のAPI障害がスペックドリフトに起因、ドキュメント不信 | 契約テスト（Schemathesis/Dredd）、CI/CDでスペック検証、ランタイムモニタリング |
| **VG-07** | **No Breaking Change Detection（破壊的変更検出なし）** | PRマージ前に互換性チェックがない | 破壊的変更が本番到達後に発覚 | oasdiff（300+ルール）をCI/CDに統合、PR時に自動チェック |

---

## 2. 破壊的変更 vs 非破壊的変更

```
非破壊的変更（バージョン不要）:
  ✅ 新エンドポイントの追加
  ✅ レスポンスへのオプショナルフィールド追加
  ✅ リクエストへのオプショナルパラメータ追加
  ✅ 新HTTPメソッドのサポート
  ✅ 既存フィールドの説明文更新
  ✅ レート制限の緩和

破壊的変更（バージョン発行 or 段階的移行）:
  ❌ 既存エンドポイントの削除/名前変更
  ❌ 必須パラメータの追加
  ❌ レスポンスフィールドの削除/型変更
  ❌ HTTPステータスコードの変更
  ❌ 認証方式の変更
  ❌ URLパスの変更
  ❌ ページネーション方式の変更
  ❌ エラーレスポンス形式の変更

Stripe方式（ハイブリッドアプローチ）:
  → 大半の変更はEvolution（追加的変更）で吸収
  → 重要なアーキテクチャ変更のみフルバージョンリリース
  → 安定性を最大化しつつ、大規模改善への明確な移行パスを提供
```

---

## 3. APIガバナンスのアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **GV-01** | **Code-First Spec（実装先行仕様）** | 実装後にOpenAPI仕様を自動生成 | 仕様が受動的成果物、設計意図が失われる | Design-First: 仕様を先に定義→モック→実装→契約テスト |
| **GV-02** | **No Linting Rules（Lintルールなし）** | OpenAPI仕様の品質チェックが手動のみ | 命名不統一、セキュリティ定義漏れ、非標準エラーモデル | Spectral/Vacuumカスタムルールセットでpr時自動チェック |
| **GV-03** | **Schema Duplication（スキーマ重複）** | 同一モデルを複数仕様にコピペ | 更新漏れで仕様間の微妙な差異、セキュリティリスク | `$ref`で共有モデル、components/schemasに一元定義 |
| **GV-04** | **No Contract Testing（契約テストなし）** | 仕様と実装の整合性を検証するテストがない | デプロイ後にクライアント破壊が発覚 | Schemathesis/Dreddで自動検証、CI/CDパイプラインに統合 |

---

## 4. スペック管理のベストプラクティス

```
OpenAPI仕様管理:

  バージョン管理:
    - OpenAPI仕様をGitでバージョン管理（コードと同じリポジトリ or 専用リポジトリ）
    - PRベースのレビューフロー
    - 変更ログ自動生成（oasdiff/changelog）

  CI/CDパイプライン:
    1. Lint: Spectral/Vacuum → 命名規則・セキュリティ定義チェック
    2. Diff: oasdiff → 破壊的変更検出（PR blocking）
    3. Test: Schemathesis/Dredd → 実装との整合性検証
    4. Publish: Redocly/SwaggerUI → ドキュメント自動公開

  ドリフト検出:
    - ランタイムトラフィックとOpenAPI仕様の比較
    - 未文書化エンドポイント・パラメータの自動検出
    - Shadow API（ドキュメント化されていないAPI）の発見

  ガバナンスフレームワーク:
    - 仕様承認フローの義務化（デプロイ前）
    - APIライフサイクル管理（設計→開発→公開→非推奨→削除）
    - 組織横断のAPIスタイルガイド
    - 定期的なAPI監査（セキュリティ・一貫性・使用率）
```

---

## 5. バージョニング方式比較

| 方式 | 例 | 長所 | 短所 | 推奨度 |
|------|-----|------|------|--------|
| URL Path | `/v1/users` | 明確、キャッシュ可能、デバッグ容易 | URL変更、リソース重複 | ★★★★★ |
| Query Param | `/users?v=1` | 既存URL維持 | キャッシュキーに影響、見落としやすい | ★★★☆☆ |
| Header | `Accept: application/vnd.api+json;v=1` | URL汚染なし、コンテンツネゴシエーション | テスト困難、ブラウザで直接確認不可 | ★★★★☆ |
| Date-based | `2025-03-01` | 変更時期が明確 | セマンティック情報なし | ★★☆☆☆ |

---

## 6. Gateway との連携

```
Gateway での活用:
  1. SURVEY フェーズで VG-01〜07 のバージョニング/ガバナンススクリーニング
  2. PLAN フェーズで破壊的変更の影響分析
  3. VERIFY フェーズでoasdiff/Spectral/契約テスト実行
  4. PRESENT フェーズでバージョニング戦略・移行計画の提示

品質ゲート:
  - バージョニング未設定 → URL Pathバージョニング追加提案（VG-01 防止）
  - 軽微変更でメジャーバージョン → 追加的変更パターン提案（VG-02 防止）
  - Deprecation計画なし → Sunset Header + 移行タイムライン設計（VG-03 防止）
  - OpenAPI仕様不在/陳腐化 → Design-First移行 + CI/CD統合（VG-06 防止）
  - PR時の互換性チェックなし → oasdiff GitHub Action追加（VG-07 防止）
  - スキーマ重複 → $ref統合提案（GV-03 防止）
  - 契約テストなし → Schemathesis/Dredd導入提案（GV-04 防止）
```

**Source:** [Zuplo: API Backwards Compatibility Best Practices](https://zuplo.com/learning-center/api-versioning-backward-compatibility-best-practices) · [Speakeasy: Versioning Best Practices](https://www.speakeasy.com/api-design/versioning) · [DEV.to: When Swagger Lies — Fixing API Drift](https://dev.to/copyleftdev/title-when-swagger-lies-fixing-api-drift-before-it-breaks-you-ijo) · [oasdiff: OpenAPI Diff & Breaking Change Detection](https://www.oasdiff.com/) · [Treblle: API Governance Best Practices 2026](https://treblle.com/blog/api-governance-best-practices) · [Nordic APIs: Understanding Root Causes of API Drift](https://nordicapis.com/understanding-the-root-causes-of-api-drift/)
