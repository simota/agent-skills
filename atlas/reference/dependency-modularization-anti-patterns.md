# Dependency & Modularization Anti-Patterns

> 依存関係管理の失敗パターン、モジュール分割の罠、分散モノリス、カップリングの落とし穴

## 1. 依存関係・モジュール化 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DM-01** | **Distributed Monolith（分散モノリス）** | マイクロサービス化したが密結合のまま | 協調デプロイ必須、障害の連鎖、両方のデメリット | DDD による Bounded Context 設計、非同期通信パターン |
| **DM-02** | **Over-Decomposition（過剰分割）** | 細かすぎるサービス分割で複雑性爆発 | サービス間通信過多、デバッグ困難、運用負荷増大 | ビジネス能力単位でのサービス設計、粗い粒度から開始 |
| **DM-03** | **Spaghetti Dependencies（スパゲッティ依存）** | サービス/モジュール間の依存が絡み合う | 循環依存、不明確なオーナーシップ、重複機能 | 依存グラフ可視化、API Gateway、明確な責務分離 |
| **DM-04** | **Shared Database Coupling（共有DB結合）** | 複数サービス/モジュールが同一DBを直接参照 | スキーマ変更が全サービスに波及、独立デプロイ不能 | サービスごとのデータストア、API 経由のデータアクセス |
| **DM-05** | **Chatty Communication（おしゃべり通信）** | サービス間の同期呼び出しが過多 | レイテンシ蓄積、20ms遅延で応答時間5.5倍劣化 | リクエストバッチ化、非同期メッセージ、ローカルキャッシュ |
| **DM-06** | **Leaky Abstraction（漏れた抽象化）** | モジュールの内部実装が外部に漏出 | internal/ からの直接 import、公開 API 以外への依存 | Public API（index.ts）による厳格なモジュール境界 |
| **DM-07** | **Data Inconsistency（データ不整合）** | 分散データの同期失敗 | データ重複・競合、ACID 保証の欠如 | イベント駆動伝播、Saga パターン、CQRS、整合性検証 |

---

## 2. 分散モノリスの検出と修復

```
分散モノリスの 3 つの検出軸（Gremlin）:

  1. 密結合テスト:
     → 障害注入でサービス停止をシミュレート
     → 結果: 依存サービスがハング/無限ローディング
     → 対策: タイムアウト短縮、非同期 API 化、DDD 適用

  2. 水平スケーラビリティテスト:
     → CPU 負荷注入でオートスケール検証
     → 結果: 全依存関係込みでのインスタンス起動が必要
     → 対策: アプリとDBの分離、独立スケーリングポリシー

  3. 過剰通信テスト:
     → サービス間に20ms遅延を注入
     → 結果: 128ms → 718ms（5.5倍劣化）
     → 対策: リクエストバッチ化、非同期化、キャッシュ

  ❌ 分散モノリスの本質:
    → モノリスの硬直性 + マイクロサービスの運用複雑性
    → 両方のデメリットを持ち、どちらのメリットも失う

  ✅ カオスエンジニアリングで実証:
    → 設計上の意図と実際の動作の乖離を検出
    → 「テストしていなければ、動くことを祈っているだけ」
```

---

## 3. Modular Monolith の再評価（2024-2025 トレンド）

```
マイクロサービスからの揺り戻し:

  背景（2024-2025）:
    → 多くの組織がマイクロサービスの運用負荷に苦戦
    → Modular Monolith が「賢い中間解」として再浮上
    → 運用のシンプルさとモジュール性の両立

  Modular Monolith の原則:
    → モジュール依存は DI コンテナで明示的管理
    → 循環依存は静的解析でアーキテクチャ違反として検出
    → 各モジュールは Public API のみを公開

  モジュール通信ルール:
    ✅ 許可: import { UserService } from '@/modules/users'
    ❌ 禁止: import { UserRepo } from '@/modules/users/internal'

  選択基準:
    → チーム規模 < 50人: Modular Monolith が有利
    → 独立デプロイ不要: Modular Monolith が有利
    → ドメイン境界が不明確: Modular Monolith で探索→後で分離
    → 異なる技術スタック必要: マイクロサービスが有利

  AI 活用（2025 トレンド）:
    → LLM ベースツールと静的コードグラフ解析で
      サービス境界の自動候補を提示
    → アーキテクトがドメイン知識で精査・調整
```

---

## 4. 結合度測定と可観測性

```
カップリング検出の実践的アプローチ:

  行動的結合（Behavioral Coupling）:
    → サービス A が B の可用性に依存してタスクを完了
    → 検出: 障害注入テスト
    → 対策: サーキットブレーカー、フォールバック

  時間的結合（Temporal Coupling）:
    → 高速・低レイテンシの同期通信が必須
    → 検出: レイテンシ注入テスト
    → 対策: 非同期メッセージング、イベント駆動

  実装結合（Implementation Coupling）:
    → 1サービスの変更が他の複数サービスの変更を要求
    → 検出: 変更影響分析、コミット相関分析
    → 対策: API バージョニング、後方互換性、契約テスト

  可観測性の必須要素:
    → 集中ログ管理（全サービス横断）
    → 分散トレーシング（リクエストフロー追跡）
    → パフォーマンスメトリクス収集
    → サービスごとのヘルスチェックエンドポイント
```

---

## 5. Atlas との連携

```
Atlas での活用:
  1. SURVEY フェーズで DM-01〜07 のスクリーニング
  2. dependency-analysis-patterns.md と連携した依存グラフ分析
  3. architecture-patterns.md と連携したモジュール境界設計
  4. VERIFY フェーズでカップリング指標の定量検証

品質ゲート:
  - 協調デプロイ必須 → 分散モノリス疑い検証（DM-01 防止）
  - サービス間通信過多 → 粒度の再評価（DM-02 防止）
  - 循環依存検出 → 依存グラフ可視化+修正必須（DM-03 防止）
  - 共有DB参照 → サービスごとのデータストア設計（DM-04 防止）
  - レイテンシ蓄積 → 非同期化+キャッシュ設計（DM-05 防止）
  - internal 直接参照 → Public API 強制（DM-06 防止）
  - データ不整合 → イベント駆動+整合性検証（DM-07 防止）
```

**Source:** [vFunction: How to Avoid Microservices Anti-Patterns](https://vfunction.com/blog/how-to-avoid-microservices-anti-patterns/) · [Gremlin: Is Your Microservice a Distributed Monolith?](https://www.gremlin.com/blog/is-your-microservice-a-distributed-monolith) · [Modular Monoliths: Why the Industry Got Distributed Systems Wrong](https://bugfree.medium.com/modular-monoliths-why-the-industry-got-distributed-systems-wrong-4aaceeacc807) · [MDPI: Modular Monolith Architecture in Cloud Environments](https://www.mdpi.com/1999-5903/17/11/496)
