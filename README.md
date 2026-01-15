# AI Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agents](https://img.shields.io/badge/Agents-40-blue.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

🤖 専門AIエージェントチームによる協調開発を実現するスキルコレクション

## ✨ Features

- **40種類の専門エージェント** - バグ調査、テスト、セキュリティ、UI/UX、インフラまで網羅
- **Nexusオーケストレーター** - タスクを分析し最適なエージェントチェーンを自動設計
- **プラットフォーム非依存** - Claude Code、Codex CLI、Gemini CLI等で動作

## 🚀 Quick Start

### インストール

```bash
# Claude Code の場合
git clone https://github.com/simota/agent-skills.git ~/.claude/skills

# その他のプラットフォーム
git clone https://github.com/simota/agent-skills.git /path/to/your/skills
```

### 使用方法

```
/Nexus ログイン機能を実装したい
/Scout このバグの原因を調査して
/Radar テストカバレッジを向上させて
/Vision ダッシュボードをモダンにリデザインしたい
```

## 📚 概要

このリポジトリには、ソフトウェア開発の様々な側面を専門とする40種類のAIエージェントが含まれています。各エージェントは特定のドメインに特化しており、**Nexus**オーケストレーターによって統括・連携されます。

## エージェント一覧

### オーケストレーション

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Nexus** | チーム統括オーケストレーター。要求を分解し、最適なエージェントチェーンを設計 | プロンプト、進行管理 |
| **Sherpa** | タスク分解ガイド。複雑なタスクを15分以内のAtomic Stepに分解 | チェックリスト |

### 調査・企画（コードを書かない）

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Scout** | バグ調査・根本原因分析（RCA）。再現手順と修正箇所を特定 | 調査レポート |
| **Spark** | 新機能提案。既存データ/ロジックを活用した機能をMarkdownで提案 | 仕様書 |
| **Compete** | 競合調査・差別化ポイント特定・ポジショニング。SWOT分析、機能マトリクス | 競合分析レポート |
| **Voice** | ユーザーフィードバック収集・NPS調査設計・感情分析・インサイト抽出 | フィードバックレポート |
| **Researcher** | ユーザーリサーチ設計・インタビューガイド作成・定性分析・ペルソナ/ジャーニーマップ作成 | リサーチレポート |

### 品質保証

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Radar** | ユニット/統合テスト追加・フレーキーテスト修正・カバレッジ向上 | テストコード |
| **Voyager** | E2Eテスト専門。Playwright/Cypress設定、Page Object設計、視覚回帰、CI統合 | E2Eテストコード |
| **Sentinel** | セキュリティ静的分析（SAST）・脆弱性パターン検出・入力検証追加 | セキュリティ修正 |
| **Probe** | セキュリティ動的テスト（DAST）・OWASP ZAP/Nuclei連携・ペネトレーションテスト | 脆弱性レポート |
| **Judge** | codex reviewによるコードレビュー・PRレビュー自動化・コミット前チェック | レビューレポート |
| **Rabbit** | coderabbit reviewによるコードレビュー・ファイルレビュー・セキュリティフォーカス・自動修正・AI幻覚検出 | レビューレポート |
| **Zen** | リファクタリング・コード品質改善（動作は変えない） | コード改善 |

### 実装

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Mason** | 本番実装。TDD・Event Sourcing・CQRS・パフォーマンス最適化を備えた型安全な実装職人。仕様の曖昧性検出、Forgeからの自動引き継ぎ対応 | プロダクションコード |
| **Artisan** | フロントエンド本番実装の職人。React/Vue/Svelte、Hooks設計、状態管理、Server Components、フォーム処理、データフェッチング | フロントエンドコード |
| **Forge** | プロトタイプ作成。完璧より動くものを優先。Mason連携用にtypes.ts, errors.ts, forge-insights.mdを出力 | MVP/PoC |

### パフォーマンス

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Bolt** | アプリケーションパフォーマンス改善。フロント（再レンダリング削減）とバック（N+1修正）両面 | 最適化コード |
| **Tuner** | DBパフォーマンス最適化。EXPLAIN ANALYZE分析・インデックス推奨・スロークエリ改善 | クエリ最適化 |

### UI/UX

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Vision** | クリエイティブディレクション。デザイン方向性決定・Design System構築・Muse/Palette/Flow/Forgeのオーケストレーション | デザイン戦略 |
| **Palette** | ユーザビリティ改善・認知負荷軽減・a11y対応 | UX改善 |
| **Muse** | デザイントークン適用・余白/角丸/シャドウ統一・ダークモード対応 | 視覚的改善 |
| **Flow** | UIアニメーション・ホバー効果・ローディング状態・モーダル遷移 | アニメーション |
| **Echo** | ペルソナ検証。ユーザーになりきりUIフローの混乱ポイントを報告 | UXレポート |
| **Showcase** | Storybookストーリー作成・カタログ管理・Visual Regression連携。CSF 3.0形式 | Storybook Stories |

### ドキュメント

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Quill** | JSDoc/TSDoc追加・README更新・any型の型定義化 | ドキュメント |

### 可視化

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Canvas** | 設計可視化。コード・仕様・コンテキストをMermaid図またはASCIIアート（フローチャート、シーケンス図、状態遷移図、クラス図、ER図等）に変換 | Mermaid図 / ASCII Art |

### アーキテクチャ

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Atlas** | 依存関係分析・循環参照検出・ADR/RFC作成 | 設計文書 |
| **Horizon** | モダナイゼーション。非推奨ライブラリ検出・ネイティブAPI置換・PoC作成 | 移行計画 |
| **Gateway** | API設計・レビュー・OpenAPI仕様生成・バージョニング戦略・破壊的変更検出 | API仕様書 |

### データ

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Schema** | DBスキーマ設計・マイグレーション作成・ER図設計 | マイグレーション/スキーマ定義 |

### DevOps

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Anvil** | Terminal UI構築・CLI開発支援・開発ツール統合（Linter/テストランナー/ビルド） | CLI/TUIコード |
| **Gear** | 依存関係管理・CI/CD最適化・Docker設定・運用監視設定 | 設定ファイル |
| **Scaffold** | クラウドインフラ（Terraform/CloudFormation/Pulumi）・ローカル開発環境（Docker Compose）・IaC設計 | インフラ設定 |

### 国際化

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Polyglot** | i18n対応。ハードコード文字列をt()関数に置換・Intl APIで日付/通貨フォーマット | i18n対応 |

### 成長

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Growth** | SEO（meta/OGP/JSON-LD）・SMO（SNSシェア表示）・CRO（CTA改善） | 成長施策 |
| **Retain** | リテンション施策・再エンゲージメント・チャーン予防。ゲーミフィケーション、習慣形成デザイン | リテンション施策 |

### 分析

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Pulse** | KPI定義・トラッキングイベント設計・ダッシュボード仕様作成 | メトリクス設計 |
| **Experiment** | A/Bテスト設計・仮説ドキュメント作成・サンプルサイズ計算・フィーチャーフラグ実装 | 実験レポート |

### 運用

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Triage** | 障害対応・影響範囲特定・復旧手順策定・ポストモーテム作成 | 運用レポート |

## ワークフロー

### 基本的な使い方

1. `/AgentName` でエージェントを呼び出し
2. エージェントがタスクを実行
3. 必要に応じて他エージェントへの引き継ぎを提案

### Nexusによるオーケストレーション

複雑なタスクには**Nexus**を使用します。Nexusは以下のモードで動作します：

| モード | トリガー | 動作 | 対話 |
|--------|----------|------|------|
| **Full Auto** | `## NEXUS_AUTORUN` + 単純タスク | 完全自動実行 | エラー時のみ |
| **Guided** | `## NEXUS_GUIDED` またはデフォルト | 判断ポイントで確認 | 選択肢形式で対話 |
| **Interactive** | `## NEXUS_INTERACTIVE` | 各ステップで確認 | 常に対話 |
| **Continue** | `## NEXUS_HANDOFF` | 結果の引き継ぎ | 必要に応じて対話 |

### 対話型実行（Guided/Interactive）

各エージェントは重要な判断ポイントでユーザーに確認を求めます（プラットフォームの対話機能を使用）：

- **開始時確認**: チェーン設計後、実行前に方針を確認
- **判断ポイント確認**: セキュリティリスク、破壊的変更、複数アプローチなど
- **質問は選択肢形式**: 2〜4つの選択肢から選択（「その他」も選択可能）

```yaml
# 選択肢形式の質問例
questions:
  - question: "セキュリティ脆弱性の可能性があります。どう対応しますか？"
    header: "セキュリティ"
    options:
      - label: "Sentinelで監査（推奨）"
        description: "セキュリティ専門エージェントに確認を依頼"
      - label: "リスクを承知で続行"
        description: "自己責任で調査を継続"
      - label: "調査を中断"
        description: "安全のため調査を停止"
```

### 複雑度による自動モード選択

| 指標 | SIMPLE | COMPLEX |
|------|--------|---------|
| 推定ステップ数 | 1-2 | 3+ |
| 影響ファイル数 | 1-3 | 4+ |
| セキュリティ関連 | No | Yes |
| 破壊的変更 | No | Yes |

- **SIMPLE + NEXUS_AUTORUN**: 完全自動実行
- **COMPLEX**: Guided モードに自動切り替え（対話必須）

詳細は `_common/INTERACTION.md` を参照してください。

### タスクタイプ別チェーンテンプレート

#### バグ修正

| タスク | 説明 | チェーン |
|--------|------|----------|
| BUG/simple | 単純なバグ修正 | Scout → Mason → Radar |
| BUG/complex | 複雑なバグ（RCA必要） | Scout → Sherpa → Mason → Radar → Sentinel |
| BUG/frontend | フロントエンドのバグ | Scout → Artisan → Radar |

#### 機能開発

| タスク | 説明 | チェーン |
|--------|------|----------|
| FEATURE/S | 小規模機能 | Mason → Radar |
| FEATURE/M | 中規模機能 | Sherpa → Forge → Mason → Radar |
| FEATURE/L | 大規模機能 | Spark → Sherpa → Forge → Mason → Radar → Quill |
| FEATURE/frontend | フロントエンド機能 | Sherpa → Forge → Artisan → Radar |
| FEATURE/fullstack | フルスタック機能 | Sherpa → Forge → Artisan → Mason → Radar |
| FEATURE/api | API開発 | Gateway → Mason → Radar |

#### UI/UX

| タスク | 説明 | チェーン |
|--------|------|----------|
| UI/new | 新規UI実装 | Vision → Forge → Showcase → Muse → Artisan → Radar |
| UI/redesign | UIリデザイン | Vision → Muse → Palette → Flow → Artisan → Radar |
| UI/component | コンポーネント作成 | Forge → Showcase → Muse → Artisan → Radar |
| UI/animation | アニメーション追加 | Flow → Artisan → Radar |
| UX/research | UXリサーチ | Researcher → Echo → Palette |
| UX/improve | UX改善 | Echo → Palette → Artisan → Radar |

#### リファクタリング

| タスク | 説明 | チェーン |
|--------|------|----------|
| REFACTOR/small | 小規模リファクタ | Zen → Radar |
| REFACTOR/arch | アーキテクチャ改善 | Atlas → Sherpa → Zen → Radar |
| REFACTOR/legacy | レガシー刷新 | Horizon → Sherpa → Zen → Radar |

#### パフォーマンス

| タスク | 説明 | チェーン |
|--------|------|----------|
| PERF/frontend | フロントエンド最適化 | Bolt → Artisan → Radar |
| PERF/backend | バックエンド最適化 | Bolt → Mason → Radar |
| PERF/db | データベース最適化 | Tuner → Schema → Mason → Radar |

#### セキュリティ

| タスク | 説明 | チェーン |
|--------|------|----------|
| SECURITY/audit | 静的解析 | Sentinel → Mason → Radar |
| SECURITY/pentest | 動的テスト | Probe → Mason → Radar → Probe |
| SECURITY/full | 完全監査 | Sentinel → Probe → Mason → Radar → Sentinel |

#### テスト

| タスク | 説明 | チェーン |
|--------|------|----------|
| TEST/unit | ユニットテスト追加 | Radar |
| TEST/e2e | E2Eテスト追加 | Voyager |
| TEST/coverage | カバレッジ向上 | Radar → Voyager |

#### レビュー

| タスク | 説明 | チェーン |
|--------|------|----------|
| REVIEW/pr | PRレビュー | Judge → Zen/Mason/Sentinel |
| REVIEW/security | セキュリティレビュー | Judge → Sentinel |
| REVIEW/coderabbit | CodeRabbitレビュー | Rabbit → Zen/Mason |

#### ドキュメント

| タスク | 説明 | チェーン |
|--------|------|----------|
| DOCS/code | コードドキュメント | Quill |
| DOCS/component | コンポーネント文書化 | Showcase → Quill |
| DOCS/architecture | アーキテクチャ図 | Canvas |

#### インフラ・DevOps

| タスク | 説明 | チェーン |
|--------|------|----------|
| INFRA/ci | CI/CD構築 | Gear → Radar |
| INFRA/cloud | クラウド構築 | Scaffold → Gear |
| INFRA/cli | CLI開発 | Anvil → Radar |

#### その他

| タスク | 説明 | チェーン |
|--------|------|----------|
| i18n | 国際化対応 | Polyglot → Radar |
| GROWTH/seo | SEO改善 | Growth → Artisan → Radar |
| ANALYTICS | 分析基盤構築 | Pulse → Mason → Radar |
| A/B | A/Bテスト設計 | Experiment → Mason → Radar |
| INCIDENT | 障害対応 | Triage → Scout → Mason |

## 共有ナレッジ

エージェント間の知識共有には `.agents/` ディレクトリを使用します：

| ファイル | 目的 | 更新タイミング |
|---------|------|---------------|
| `PROJECT.md` | 共有知識 + アクティビティログ | **全エージェントが作業完了後に必須** |
| `{agent}.md` | エージェント固有の学習 | ドメイン固有の発見時 |

### PROJECT.md の構成

- **Architecture Decisions** - アーキテクチャ選択の記録
- **Domain Glossary** - 用語の統一
- **API & External Services** - 外部サービスの制約
- **Known Gotchas** - 既知の落とし穴
- **Security Considerations** - セキュリティ制約
- **Performance Budgets** - パフォーマンス予算
- **Activity Log** - エージェントの作業履歴

## エージェントの原則

各エージェントは以下の原則に従います：

### 共通ルール

- **変更は50行以内** - 小さく安全な変更を心がける
- **既存パターンの尊重** - プロジェクトの規約に従う
- **テスト実行** - 変更前後でテストを実行
- **ジャーナルは重要な学習のみ** - ルーチンワークは記録しない

### 境界の種類

| マーカー | 意味 |
|---------|------|
| ✅ Always do | 常に実行すべきこと |
| ⚠️ Ask first | 確認が必要なこと |
| 🚫 Never do | 絶対にしないこと |

## ディレクトリ構成

```
skills/
├── _common/
│   └── INTERACTION.md  # 対話ルール共通定義
├── _templates/
│   └── PROJECT.md      # プロジェクト知識テンプレート
├── Anvil/SKILL.md      # CLI/TUI構築
├── Artisan/SKILL.md    # フロントエンド実装
├── Atlas/SKILL.md      # アーキテクチャ
├── Bolt/SKILL.md       # パフォーマンス
├── Canvas/SKILL.md     # 可視化
├── Compete/SKILL.md    # 競合調査
├── Echo/SKILL.md       # ペルソナ検証
├── Experiment/SKILL.md # A/Bテスト設計
├── Flow/SKILL.md       # アニメーション
├── Forge/SKILL.md      # プロトタイプ
├── Gateway/SKILL.md    # API設計
├── Gear/SKILL.md       # DevOps
├── Growth/SKILL.md     # SEO/CRO
├── Horizon/SKILL.md    # モダナイゼーション
├── Judge/SKILL.md      # コードレビュー（codex review）
├── Rabbit/SKILL.md     # コードレビュー（coderabbit review）
├── Mason/SKILL.md      # 本番実装
├── Muse/SKILL.md       # デザイン
├── Nexus/SKILL.md      # オーケストレーター
├── Palette/SKILL.md    # UX
├── Polyglot/SKILL.md   # i18n
├── Probe/SKILL.md      # セキュリティ動的テスト（DAST）
├── Pulse/SKILL.md      # メトリクス設計
├── Quill/SKILL.md      # ドキュメント
├── Radar/SKILL.md      # テスト
├── Researcher/SKILL.md # ユーザーリサーチ
├── Retain/SKILL.md     # リテンション
├── Scaffold/SKILL.md   # インフラ
├── Schema/SKILL.md     # DBスキーマ設計
├── Scout/SKILL.md      # バグ調査
├── Showcase/SKILL.md   # Storybookストーリー管理
├── Sentinel/SKILL.md   # セキュリティ静的分析（SAST）
├── Sherpa/SKILL.md     # タスク分解
├── Spark/SKILL.md      # 機能提案
├── Triage/SKILL.md     # 障害対応
├── Tuner/SKILL.md      # DBパフォーマンス最適化
├── Vision/SKILL.md     # クリエイティブディレクション
├── Voice/SKILL.md      # ユーザーフィードバック
├── Voyager/SKILL.md    # E2Eテスト
└── Zen/SKILL.md        # リファクタリング
```

## 使用例

### 単一エージェントの使用

> カテゴリ別に全40エージェントの使用例を紹介します。

#### オーケストレーション

##### チェーン設計（Nexus）

```
/Nexus
ログイン機能を実装したいのですが、どのような手順で進めればよいですか？
```

**出力**: タスク分類（FEATURE/M）、推奨チェーン（Sherpa → Forge → Mason → Radar）、最初のステップのプロンプト

---

##### タスク分解（Sherpa）

```
/Sherpa
決済機能の実装タスクが複雑で整理できません。分解してください。
```

**出力**: 15分以内で完了できるAtomic Stepのリスト、進捗チェックリスト、最初に着手すべきタスクの具体的指示

---

#### 調査・企画

##### バグ調査（Scout）

```
/Scout
ユーザーからログインできないという報告がありました。原因を調査してください。
```

**出力**: 再現手順、根本原因、修正対象ファイル、推奨修正アプローチを含む調査レポート

---

##### 機能提案（Spark）

```
/Spark
このアプリケーションの利便性を向上させる機能を提案してください。
```

**出力**: 既存データ/ロジックを活用した機能提案の仕様書（Markdown）

---

#### 品質保証

##### テスト追加（Radar）

```
/Radar
この部分のテストカバレッジを確認し、不足しているテストを追加してください。
```

**出力**: 不足しているエッジケーステスト、境界値テスト、エラーケーステストの追加

---

##### E2Eテスト作成（Voyager）

```
/Voyager
ログインから購入完了までのフローのE2Eテストを作成してください。
```

**出力**: Playwright/CypressでのE2Eテストコード（Page Object Model設計、認証状態管理、CI統合設定含む）

---

##### セキュリティ監査（Sentinel）

```
/Sentinel
このAPIのセキュリティを監査してください。
```

**出力**: 脆弱性の検出（SQLインジェクション、XSS等）と修正コード

---

##### PRレビュー（Judge）

```
/Judge
このPRをレビューしてください。バグやセキュリティ問題がないか確認をお願いします。
```

**出力**: codex reviewによる自動レビュー、重大度別の問題リスト、修正担当エージェントの提案

---

##### コミット前チェック（Judge）

```
/Judge
コミット前に変更内容をレビューしてください。
```

**出力**: 未コミット変更のレビュー、バグ・セキュリティ問題の検出、コミット可否の判定

---

##### ファイルレビュー（Rabbit）

```
/Rabbit
src/auth/login.ts をレビューしてください。AIで生成したコードなので品質が心配です。
```

**出力**: coderabbit reviewによる深い依存関係分析、AI幻覚検出、自動修正提案

---

##### セキュリティフォーカスレビュー（Rabbit）

```
/Rabbit
認証周りのセキュリティを重点的にチェックしてください。
```

**出力**: `--focus security` によるセキュリティ重視レビュー、脆弱性検出

**Note**: Judge と Rabbit の役割分担
- **Judge**: codex reviewによるPRレビュー、ブランチ間diff
- **Rabbit**: coderabbit reviewによる深い分析、自動修正、セキュリティフォーカス

---

##### リファクタリング（Zen）

```
/Zen
このファイルの可読性が低いのでリファクタリングしてください。
```

**出力**: 責務ごとに分割された読みやすいコード（動作は変えない）

**Note**: レビュー系エージェントの役割分担
- **Judge**: codex reviewでPRレビュー・バグ検出（コード修正しない）
- **Rabbit**: coderabbit reviewで深い分析・自動修正・AI幻覚検出
- **Zen**: コード品質の**改善**（リファクタリング、可読性向上）

---

#### 実装

##### 本番実装（Mason）

```
/Mason
プロトタイプは動作しますが、本番環境に適した品質に仕上げてください。
```

**出力**: 型安全化、エラーハンドリング、バリデーション追加されたプロダクションコード

**Mason の強化機能**:
- **Clarify Phase**: 仕様の曖昧性を検出し、質問または複数案を提示
- **Design Phase**: TDD（テストファーストで設計）
- **Build Phase**: Event Sourcing / CQRS / Saga パターン対応
- **Validate Phase**: N+1検出、キャッシュ戦略、パフォーマンス最適化
- **Forge連携**: types.ts → Value Object、errors.ts → DomainError、forge-insights.md → ビジネスルール

---

##### プロトタイプ作成（Forge）

```
/Forge
以下の画面のプロトタイプを作成してください。動作確認できる状態で構いません。
```

**出力**: モックデータで動作する素早く作ったUIコンポーネント

---

##### フロントエンド実装（Artisan）

```
/Artisan
Forgeで作成したユーザープロフィールのプロトタイプを本番品質に仕上げてください。
TypeScript strict、適切なエラーハンドリング、アクセシビリティを確保してください。
```

**出力**: 型安全で本番品質のReact/Vue/Svelteコンポーネント、カスタムHooks、状態管理の統合

**Artisan の主な対応領域**:
- **Hooks設計**: カスタムHooksの作成、useEffect/useMemoの適切な使用
- **状態管理**: Zustand/Jotai/Redux Toolkitの選択と実装
- **Server Components**: React 19/Next.js App Routerでのサーバー/クライアント分離
- **フォーム処理**: React Hook Form + Zodによるバリデーション
- **データフェッチング**: TanStack Query/SWRによるキャッシュ戦略

---

#### パフォーマンス

##### パフォーマンス改善（Bolt）

```
/Bolt
このページの表示速度が遅いので改善してください。
```

**出力**: ボトルネックの特定と最適化（メモ化、遅延読み込み、クエリ改善など）

**Bolt の対応範囲**:
- **フロントエンド**: 再レンダリング削減、React.memo/useMemo、lazy loading、バンドルサイズ
- **バックエンド**: N+1検出、DataLoader導入、コネクションプール、非同期処理

---

##### DBパフォーマンス最適化（Tuner）

```
/Tuner
商品一覧ページのクエリが遅いです。EXPLAIN ANALYZEで分析して最適化してください。
```

**出力**: 実行計画分析、インデックス推奨、クエリリライト

**Bolt vs Tuner の役割分担**:
- **Bolt**: アプリケーション層（クエリの発行方法、キャッシュ）
- **Tuner**: データベース層（クエリの実行方法、インデックス）

---

#### UI/UX

##### クリエイティブディレクション（Vision）

```
/Vision
ダッシュボード画面をモダンにリデザインしたいです。
現在の見た目が古くなってきたので、2024年のトレンドを取り入れてください。
```

**出力**: 3つのデザイン方向性提案、選択された方向性のStyle Guide、Muse/Palette/Flow/Forgeへの委譲計画

---

##### デザインレビュー（Vision）

```
/Vision
現在のUIデザインをレビューして、改善点を特定してください。
```

**出力**: ヒューリスティック評価結果、改善優先度リスト、各改善の担当エージェント指定

---

##### UX改善（Palette）

```
/Palette
このフォームの使い勝手が悪いというフィードバックがありました。改善してください。
```

**出力**: フィードバック改善、認知負荷軽減、エラー表示の改善

---

##### デザイン統一（Muse）

```
/Muse
デザインの一貫性がないので統一してください。
```

**出力**: デザイントークンへの統一、余白・角丸・シャドウの調整

---

##### UIアニメーション（Flow）

```
/Flow
この画面にアニメーションを追加して、インタラクションを改善してください。
```

**出力**: 適切なトランジション、ホバー効果、ローディングアニメーションの追加

---

##### ペルソナ検証（Echo）

```
/Echo
高齢者ペルソナの視点でこのUIの使いやすさを検証してください。
```

**出力**: 指定ペルソナ視点での混乱ポイント、改善提案のUXレポート

---

##### Storybookストーリー作成（Showcase）

```
/Showcase
新しく作成したButtonコンポーネントのStorybookストーリーを作成してください。
```

**出力**: CSF 3.0形式のStoryファイル（全バリアント、インタラクションテスト、autodocs）

**Showcase の主な機能**:
- **CREATE**: 新規コンポーネントのストーリー作成
- **MAINTAIN**: 既存ストーリーの更新・CSF3移行
- **AUDIT**: ストーリーカバレッジと品質の監査

---

##### Storybookカバレッジ監査（Showcase）

```
/Showcase
現在のStorybookカバレッジを監査してください。不足しているストーリーを特定してください。
```

**出力**: カバレッジレポート、品質スコア、改善アクションリスト

---

#### ドキュメント

##### ドキュメント追加（Quill）

```
/Quill
この関数にドキュメントを追加してください。処理内容がわかりにくいという指摘がありました。
```

**出力**: JSDoc/TSDoc、使用例、パラメータ説明の追加

---

#### 可視化

##### 設計図の作成（Canvas）

```
/Canvas
この認証フローを図にして可視化してください。
```

**出力**: Mermaid形式のシーケンス図、フローチャート、状態遷移図など

---

##### コードから図を逆生成（Canvas）

```
/Canvas
src/services/payment/ の処理フローを可視化して
```

**出力**: コードを分析して生成されたフローチャートまたはシーケンス図

---

##### 会話コンテキストの整理（Canvas）

```
/Canvas
これまでの会話内容をマインドマップにまとめてください。
```

**出力**: 会話内容を整理したマインドマップ

---

##### ASCIIアートで図を作成（Canvas）

```
/Canvas
このAPIの処理フローをASCIIアートで作成してください。
```

**出力**: ターミナルやコメント内でも表示可能なASCII形式のフローチャート

---

#### アーキテクチャ

##### アーキテクチャ分析（Atlas）

```
/Atlas
コードの依存関係を分析し、変更時の影響範囲を明確にしてください。
```

**出力**: 依存関係マップ、問題箇所の特定、改善のためのADR/RFC

---

##### モダナイゼーション（Horizon）

```
/Horizon
使用しているライブラリのバージョンを確認し、非推奨や脆弱性のあるものを特定してください。
```

**出力**: 非推奨ライブラリの検出、代替案の提案、移行PoC

---

##### API設計（Gateway）

```
/Gateway
ユーザー管理APIのエンドポイントを設計してください。REST APIのベストプラクティスに従ってください。
```

**出力**: OpenAPI仕様書、エンドポイント設計、バージョニング戦略

---

##### API破壊的変更検出（Gateway）

```
/Gateway
このPRの変更がAPIの後方互換性を壊さないか確認してください。
```

**出力**: 破壊的変更のリスト、影響を受けるクライアント、移行ガイド

---

#### データ

##### DBスキーマ設計（Schema）

```
/Schema
注文管理システムのDBスキーマを設計してください。注文、注文明細、顧客、商品の関係を考慮してください。
```

**出力**: ER図（Mermaid形式）、DDL、マイグレーションファイル、インデックス設計

**Schema vs Tuner の役割分担**:
- **Schema**: 論理設計（テーブル構造、リレーション、正規化）
- **Tuner**: 物理最適化（インデックス調整、クエリ改善）

---

##### マイグレーション作成（Schema）

```
/Schema
usersテーブルにプロフィール画像URLを追加するマイグレーションを作成してください。
```

**出力**: Up/Down両方のマイグレーション、ロールバック手順

---

#### DevOps

##### CLI/TUI構築（Anvil）

```
/Anvil
コマンドラインツールを作成してください。ヘルプ表示やプログレスバーなども含めてください。
```

**出力**: 引数パース、ヘルプ生成、プログレスバー、カラー出力などを備えたCLI

---

##### CI/CD改善（Gear）

```
/Gear
CIの実行時間を短縮してください。現状では時間がかかりすぎています。
```

**出力**: キャッシュ最適化、並列化、不要ステップ削除などの改善

---

##### インフラ構築（Scaffold）

```
/Scaffold
AWS上にステージング環境を構築するためのTerraform設定を作成してください。
```

**出力**: Terraform/CloudFormation/Pulumiの設定ファイル、環境変数テンプレート

---

##### ローカル開発環境構築（Scaffold）

```
/Scaffold
新規開発者がすぐに開発を始められるようにDocker Compose環境を整備してください。
```

**出力**: docker-compose.yml、.env.example、セットアップスクリプト

---

#### 国際化

##### 国際化対応（Polyglot）

```
/Polyglot
海外展開に向けて、アプリケーションの国際化対応を行ってください。
```

**出力**: ハードコード文字列のi18n化、日付/通貨フォーマットの国際化対応

---

#### 成長

##### SEO改善（Growth）

```
/Growth
SNSでシェアした際のプレビュー表示を改善してください。
```

**出力**: OGPタグ、メタ情報、構造化データの追加

---

##### リテンション施策（Retain）

```
/Retain
ユーザーの継続利用率が低下しています。リテンション改善施策を提案してください。
```

**出力**: リテンション分析フレームワーク、再エンゲージメントトリガー設計、ゲーミフィケーション提案

---

#### 分析

##### メトリクス設計（Pulse）

```
/Pulse
このサービスのKPIを定義し、トラッキングイベントを設計してください。
```

**出力**: KPI定義、イベント設計、ダッシュボード仕様

---

##### A/Bテスト設計（Experiment）

```
/Experiment
CTAボタンの色変更による効果を検証するA/Bテストを設計してください。
```

**出力**: 仮説ドキュメント、サンプルサイズ計算、フィーチャーフラグ実装ガイド

---

#### 運用

##### 障害対応（Triage）

```
/Triage
本番環境でAPIレスポンスが遅延しています。初動対応をお願いします。
```

**出力**: 影響範囲特定、復旧手順、エスカレーション判断

---

##### ポストモーテム作成（Triage）

```
/Triage
先日の障害についてポストモーテムを作成してください。
```

**出力**: 障害タイムライン、根本原因、再発防止策

---

#### 調査・企画（追加）

##### 競合調査（Compete）

```
/Compete
競合サービスAとBを分析し、差別化ポイントを特定してください。
```

**出力**: 競合機能マトリクス、SWOT分析、ポジショニングマップ

---

##### ユーザーリサーチ設計（Researcher）

```
/Researcher
新機能の検証のためにユーザーインタビューを設計してください。
```

**出力**: インタビューガイド、質問リスト、ペルソナ/ジャーニーマップ

---

##### フィードバック分析（Voice）

```
/Voice
最近のアプリストアレビューを分析してインサイトを抽出してください。
```

**出力**: 感情分析、フィードバック分類、改善優先度リスト

---

#### セキュリティ（追加）

##### 動的セキュリティテスト（Probe）

```
/Probe
認証APIに対してペネトレーションテストを実施してください。
```

**出力**: OWASP ZAP/Nucleiによるスキャン結果、脆弱性レポート、修正優先度

**Sentinel vs Probe の役割分担**:
- **Sentinel**: 静的解析（SAST）- コードを読んで脆弱性を検出
- **Probe**: 動的テスト（DAST）- 実行中のアプリを攻撃して脆弱性を検出

---

### 複数エージェント連携（Nexus）

#### 新機能開発（自動実行）

```
/Nexus
ユーザープロフィール編集機能を追加したい
- 名前、メール、アバター画像を編集できる
- バリデーションあり
- 保存成功時にトースト表示

## NEXUS_AUTORUN
```

**実行チェーン**: Spark（仕様策定）→ Sherpa（タスク分解）→ Forge（プロトタイプ）→ Mason（本番実装）→ Radar（テスト）→ Quill（ドキュメント）

---

#### バグ修正（複雑なケース）

```
/Nexus
本番環境でのみ発生する決済エラーを調査・修正してください。
ローカルでは再現しません。

## NEXUS_AUTORUN
```

**実行チェーン**: Scout（調査）→ Sherpa（タスク分解）→ Mason（修正）→ Radar（回帰テスト）→ Sentinel（セキュリティ確認）

---

#### 大規模リファクタリング

```
/Nexus
認証モジュールがスパゲッティコードになっています。
Clean Architectureに沿ってリファクタリングしたいです。
```

**実行チェーン**: Atlas（アーキテクチャ設計）→ Sherpa（段階的計画）→ Zen（リファクタリング）→ Radar（テスト）

---

#### UI機能の追加

```
/Nexus
商品詳細ページにレビュー投稿機能を追加してください。
星評価とコメントを入力できるようにしたいです。
```

**実行チェーン**: Spark（仕様）→ Forge（UI プロトタイプ）→ Muse（デザイン調整）→ Mason（実装）→ Radar（テスト）

---

### ステップバイステップ実行（手動制御）

#### 段階的な機能開発

```
/Nexus
検索機能を追加したいです。
```

#### AUTORUNモード（自動実行・推奨）

```
## NEXUS_AUTORUN_FULL
検索機能を追加したいです。
```

Nexusが自動でチェーンを実行：

```
## Nexus Execution: 検索機能の追加
- Chain: **Spark** → **Sherpa** → **Mason** → **Radar**
- Mode: AUTORUN_FULL

### Executing Step 1/4: Spark
_AGENT_CONTEXT:
  Role: Spark
  Task: 検索機能の仕様書を作成

[Sparkとして仕様書を作成...]

_STEP_COMPLETE:
  Agent: Spark
  Status: SUCCESS
  Next: Sherpa

### Executing Step 2/4: Sherpa
[自動で次のステップへ...]
```

**コピペ不要** - 最終成果物まで自動実行されます。

#### GUIDEDモード（手動引き継ぎ）

手動で各エージェントを呼び出す場合：

```
## NEXUS_GUIDED
検索機能を追加したいです。
```

Nexusがチェーンを設計し、次のステップを提示：

```
## Nexus Plan: 検索機能の追加
- Chain: **Spark** → **Sherpa** → **Mason** → **Radar**
- Current step: 1/4

### Next Step: Spark
Invoke **Spark** with the following context:
[コンテキスト情報]
```

---

### タスク分解の活用（Sherpa）

#### 大きなタスクを小さく分割

```
/Sherpa
ECサイトのチェックアウトフローを実装したいです。
```

**出力**:

```
## 🏔️ Sherpa's Guide
**Current Objective:** チェックアウトフロー実装
**Progress:** 0/8 steps completed

### 👉 NOW: カート内容の型定義を作成
CartItem, CartSummary インターフェースを定義してください。
*(Mason を呼び出しますか？)*

### 📋 Upcoming Path:
- [ ] カートAPI エンドポイント作成
- [ ] 配送先入力フォーム
- [ ] 支払い方法選択UI
- [ ] 注文確認画面
- [ ] 注文完了処理
- [ ] エラーハンドリング
- [ ] テスト追加

**Status:** 🟢 On Track
```

## カスタマイズ

### 新しいエージェントの追加

1. `skills/[AgentName]/SKILL.md` を作成
2. frontmatter に `name` と `description` を定義
3. 境界（Always do / Ask first / Never do）を明記
4. AUTORUN SupportとNexus Hub Modeのセクションを追加

### エージェントの修正

各 `SKILL.md` を直接編集します。フォーマット：

```markdown
---
name: AgentName
description: 日本語での説明
---

[エージェントの詳細な指示]
```

## ライセンス

MIT
