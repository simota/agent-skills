# Architecture Modernization Anti-Patterns

> レガシー刷新の失敗パターン、Strangler Fig の落とし穴、マイグレーション戦略の罠、段階的移行のベストプラクティス

## 1. アーキテクチャモダナイゼーション 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **AM-01** | **Big Bang Rewrite（全面書き直し）** | レガシーを一括で新システムに置換 | リスク集中、人的・時間的リソース枯渇、ビジネス停止 | Strangler Fig パターンで段階的移行 |
| **AM-02** | **Incomplete Migration（不完全移行）** | モダナイゼーションが途中で停滞 | レガシー+新システムのハイブリッドが常態化、複雑性倍増 | マイルストーン設定、デコミッション計画の事前策定 |
| **AM-03** | **Zombie Code（ゾンビコード）** | 移行済みレガシーコードが削除されず残存 | モノリスの肥大化、混乱、保守コスト増 | トラフィック切替完了後の積極的削除、削除のDoD設定 |
| **AM-04** | **Database Entanglement（DB絡み合い）** | DB マイグレーションの複雑性を過小評価 | 外部キー制約、ACID トランザクション跨ぎの問題 | CDC（Change Data Capture）、最終整合性モデル、Saga |
| **AM-05** | **Frontend Neglect（フロントエンド無視）** | バックエンドのみ移行しフロントエンドを放置 | UI が複数データソースに対応できず統合失敗 | マイクロフロントエンド、BFF パターン、UI 並行移行 |
| **AM-06** | **Skill Gap Blindness（スキルギャップ軽視）** | レガシー技術の理解者不足を無視 | 抽出失敗、ビジネスルールの喪失、手戻り | ハイブリッドチーム編成（レガシー+モダン技術者） |
| **AM-07** | **Feature Parity Trap（機能等価の罠）** | レガシーの全機能を新システムに100%再現しようとする | 不要機能の移行、コスト・時間の浪費 | 機能の取捨選択、80/20ルール、利用データに基づく判断 |

---

## 2. Strangler Fig パターンのベストプラクティス

```
Strangler Fig の 5 段階実装:

  Step 1: システム境界の特定
    → レガシーシステムの機能マップ作成
    → 「thin slice」— 独立して置換可能な最小単位を特定
    → ドメインイベントの洗い出し

  Step 2: Facade（間接層）の設置
    → レガシーと新システムの間にルーティング層を配置
    → Feature Flag で旧/新の切り替えを動的制御
    → 全通信が Facade を経由するよう設計

  Step 3: 低リスクスライスから開始
    → 非ミッションクリティカルな読み取り専用コンポーネント
    → 成功指標: ゼロダウンタイム、ルーティング検証
    → ビジネス価値より「パターン証明」を優先

  Step 4: 段階的移行の実行
    → Anti-Corruption Layer で新旧データモデルを翻訳
    → CDC（Debezium 等）でリアルタイムデータ同期
    → 移行中のレガシースライスに新機能を追加しない

  Step 5: 段階的デコミッション
    → 新サービスがプロダクション安定後にレガシー削除
    → フォールバックパスを初期段階で維持
    → 削除は「積極的に実行」— ゾンビコード防止

  2025 年トレンド:
    → Strangler Fig + Event Streaming（Apache Kafka）の組合せ
    → CDC による レガシー DB → モダンデータストア のリアルタイム同期
    → 金融・製造業で「刷新しなければ存続できない」戦略的必須化
```

---

## 3. マイグレーション失敗の共通原因

```
移行プロジェクトの典型的失敗パターン:

  1. 相互依存の過小評価:
     → レガシーシステムの「複雑で深く埋め込まれた相互依存」
     → 1つの機能抽出が10の依存関係に波及
     → 対策: 移行前の徹底的な依存関係マッピング

  2. データ同期の軽視:
     → 新旧システム間のデータ整合性維持は「複雑でエラーを起こしやすい」
     → 対策: CDC ツール、最終整合性の設計、検証メカニズム

  3. 知識移転の不足:
     → 既存システムの機能を「徹底的に理解」してから移行開始
     → 暗黙知（undocumented business rules）の喪失リスク
     → 対策: レガシーコードの考古学的調査、ドメインエキスパートへのヒアリング

  4. ステークホルダーの無関心:
     → コミュニケーション不足が「変化への抵抗」を生む
     → 対策: 定期的な進捗共有、早期の成功事例で信頼構築

  5. 分散トランザクションの複雑性:
     → レガシー・モダン跨ぎの ACID トランザクション不可
     → 2 Phase Commit はマイクロサービス環境で破綻
     → 対策: Saga パターン、最終整合性モデル
```

---

## 4. 段階的移行の判断フレームワーク

```
モダナイゼーション戦略の選択:

  戦略              | 適用条件                    | リスク  | コスト
  -----------------|-----------------------------|--------|------
  Strangler Fig    | 段階的移行可能、稼働継続必須   | 低      | 中
  Leave & Layer    | レガシー変更不可、イベント駆動  | 中      | 中
  Big Bang         | 小規模システム、短期停止許容   | 高      | 低-高
  Lift & Shift     | インフラのみ刷新              | 低      | 低
  Re-platform      | クラウドネイティブ化           | 中      | 中-高

  判断基準:
    → ビジネスクリティカル度（高→Strangler Fig）
    → システム規模（小→Big Bangも許容）
    → チームスキル（レガシー理解者の有無）
    → 時間的制約（短→Lift & Shift で応急）
    → 予算（限定→段階的アプローチ）

  ❌ アンチパターン: 戦略選択なしに「とりあえずマイクロサービス化」
  ✅ 推奨: 現状分析→戦略選択→PoC→段階的実行
```

---

## 5. Atlas との連携

```
Atlas での活用:
  1. SURVEY フェーズで AM-01〜07 のスクリーニング
  2. architecture-patterns.md と連携した移行先パターン選定
  3. PLAN フェーズで Strangler Fig 実装計画策定
  4. VERIFY フェーズで移行進捗とリスク検証

品質ゲート:
  - 全面書き直し提案 → Strangler Fig 検討必須（AM-01 防止）
  - 移行停滞 → マイルストーン+デコミッション計画（AM-02 防止）
  - レガシーコード残存 → 積極的削除計画（AM-03 防止）
  - DB 移行計画なし → CDC+整合性設計必須（AM-04 防止）
  - バックエンドのみ移行 → フロントエンド並行計画（AM-05 防止）
  - スキルギャップ未確認 → チーム編成評価必須（AM-06 防止）
  - 全機能100%移行 → 利用データに基づく取捨選択（AM-07 防止）
```

**Source:** [Thoughtworks: Embracing the Strangler Fig Pattern](https://www.thoughtworks.com/en-us/insights/articles/embracing-strangler-fig-pattern-legacy-modernization-part-one) · [Salfati Group: CIO Guide to Strangler Fig Pattern](https://salfati.group/topics/strangler-fig-pattern) · [vFunction: Strangler Architecture Pattern for Modernization](https://vfunction.com/blog/strangler-architecture-pattern-for-modernization/) · [Martin Fowler: Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html)
