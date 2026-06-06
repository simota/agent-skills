# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

#### New Agents
- **Attest** - 仕様適合検証エージェント。仕様書から受入基準を抽出し、BDDシナリオを生成し、実装が仕様通りか敵対的に検証。CERTIFIED/CONDITIONAL/REJECTED判定を発行。5つのリファレンス（criteria-extraction, verification-methods, bdd-generation, compliance-report, adversarial-probing）を含む
- **Levy** - 日本の確定申告（所得税）をガイドするドメイン知識エージェント。所得分類・控除最適化・税額計算・e-Tax手順をフリーランス/副業サラリーマン向けに解説
- **Helm** - 財務・市場・競合データから短期/中期/長期の経営シミュレーションを実施する経営戦略特化エージェント（SWOT/PESTLE/Porter分析、シナリオプランニング）
- **Pipe** - GHAワークフロー専門エージェント（トリガー戦略、セキュリティ強化、PR自動化、Reusable Workflow設計）
- **Aether** - AITuber（AI VTuber）システムの企画から実装・運用までを一貫支援するフルスタック・オーケストレーター
- **Oracle** - AI/ML設計・評価専門エージェント（プロンプトエンジニアリング、RAG設計、LLMアプリパターン）
- **Beacon** - 可観測性・信頼性エンジニアリング専門エージェント（SLO/SLI設計、分散トレーシング）
- **Siege** - 負荷テスト・カオスエンジニアリング・レジリエンス検証専門エージェント
- **Prose** - ユーザー向けテキスト専門エージェント（マイクロコピー、エラーメッセージ、ボイス＆トーン設計）
- **Latch** - Claude Codeフック管理エージェント（PreToolUse/PostToolUse等のイベントシステム）
- **Relay** - メッセージング統合・Bot開発・リアルタイム通信の設計＋実装エージェント
- **Void** - 引き算設計エージェント。YAGNI検証、スコープカット、複雑性削減提案
- **Totem** - プロジェクトDNAプロファイラー。8次元の文化分析、逸脱検出、オンボーディングガイド
- **Matrix** - ユニバーサル組み合わせ分析エージェント。多次元軸の組み合わせ爆発を制御し、最小カバレッジセット選定・優先順位付けを担当
- **Compass** - 戦略実行モニタリング・前提条件監視・OKRカスケード。Helmのロードマップを受け取りKPI乖離を追跡
- **Refract** - 3軸（視野・視座・視点）リフレーミングエージェント。問題やアイデアを回転させ新たな洞察を生成
- **Darwin** - エコシステム自己進化オーケストレーター。プロジェクトライフサイクル検出、エージェント関連性評価、横断的知識統合

### Enhanced
- **Nexus** - 19種類のルーティングコマンドと42種類のチェーンテンプレートを追加。エージェント重複ペアの曖昧性解消ガイドも追加
- **Orbit** - Gemini TTSによるイテレーション通知（Pattern D）、スクリプト生成機能、ブランチ分離戦略、ループランナー防御パターン・リカバリ拡張、Executor Engine CLI参照、全スクリプトテンプレート拡張、macOS互換性修正
- **Guardian** - Squash最適化エンジン追加（スコアリング、グルーピング、メッセージ合成）
- **Sigil** - `.agents/skills/` サポート追加でポータブルなスキル配置が可能に
- **Bard** - エンジン・エゴアーキテクチャに刷新（Codex/Gemini/Claude各エンジンが固有の声で語る）
- **Cast** - SPEAKモード追加、Google Cloud TTSを第三のエンジンとして統合
- **Titan** - build-firstアプローチ強制。スコープ適応型チェーン、統合プロトコル・自律検証・実行ブートストラップを追加
- **Scaffold** - Terraformオペレーション、コンプライアンス、FinOps参照ドキュメントを追加
- **Hearth** - SKILL.mdと参照ドキュメントを拡充
- **Zen** - 防御的過剰検出パターンを追加
- **Grove/Sweep** - メンテナンスモード、インラインしきい値、クロススキルハンドオフパイプラインを追加
- **Void** - コード以外の全ドメイン（機能・プロセス・ドキュメント・設計・仕様・依存・設定）への引き算フレームワーク汎化
- **Voyager, Vector, Sketch** - 各SKILL.mdを包括的に改善（グレードA相当）
- **Levy** - Interaction Triggers追加（6トリガー+YAMLテンプレート）、Principles番号付きリスト化、Quick Decision判定テーブル2種追加（申告要否・事業所得vs雑所得）

### Changed
- 全エージェントのSKILL.mdを原則中心設計で最適化（コンテキスト削減、28〜91%圧縮）
- 38 SKILL.mdファイルのテンプレート一貫性を強制
- エコシステムへのPipe/Relay/Aether/Oracle/Beacon/Siege/Prose統合（Nexus, Architect, Gearのルーティング更新）
- Titanをbuild-firstエンジンとしてリビルド、参照整理

## [1.0.0] - 2025-01-15

### Added

#### New Agents
- **Artisan** - フロントエンド本番実装の職人（React/Vue/Svelte、Hooks、状態管理）
- **Vitrine** - Storybookストーリー作成・カタログ管理・Visual Regression連携
- **Vision** - クリエイティブディレクション・Design System構築
- **Probe** - セキュリティ動的テスト（DAST）・ペネトレーションテスト
- **Tuner** - DBパフォーマンス最適化・EXPLAIN ANALYZE分析
- **Field** - ユーザーリサーチ設計・インタビューガイド作成
- **Voyager** - E2Eテスト専門（Playwright/Cypress）
- **Judge** - codex reviewによるコードレビュー・PRレビュー自動化・AI幻覚検出
- **Anvil** - Terminal UI構築・CLI開発支援

#### Features
- **AUTORUN_FULL mode** - ガードレール付き完全自動実行モード
- 40種類の専門エージェント体制
- 全エージェントの使用例を完備
- タスクタイプ別チェーンテンプレート（11カテゴリ、41テンプレート）

### Enhanced
- **Vision** - 2025-2026デザイントレンド、AI設計ツール統合（Figma AI、v0、Claude）
- **Artisan** - Vue 3 Composition API、Svelte 5 Runes、スタイリング戦略ガイド
- **Vitrine** - Storybook 8対応、MDX 3ドキュメント、Figma連携
- **Builder** - TDD、Event Sourcing、CQRS、Forgeからの自動引き継ぎ

### Changed
- AUTORUN_FULLをデフォルトモードに設定
- プラットフォーム非依存に対応（Claude Code、Codex CLI、Gemini CLI等）
- エージェント境界定義の明確化（Bolt vs Tuner、Schema vs Tuner等）

### Removed
- **Roadmap** - PM向け機能のため削除
- **Insight** - Spark/Scoutに統合
- **Lens** - Canvas/Showcaseに統合
- **Fixture** - Builder/Radarに統合

## [0.9.0] - 2025-01-08

### Added
- Initial release with 35 agents
- Nexus orchestrator with AUTORUN/GUIDED modes
- Basic agent collaboration framework
- Hub & Spoke architecture

---

## Agent Categories

| Category | Count | Agents |
|----------|-------|--------|
| Orchestration | 8 | Nexus, Sherpa, Architect, Rally, Titan, Sigil, Orbit, Darwin |
| Research & Planning | 10 | Scout, Ripple, Spark, Compete, Voice, Field, Trace, Canon, Lens, Cast |
| Decision & Strategy | 4 | Magi, Helm, Levy, Accord |
| Git/PR Management | 4 | Guardian, Harvest, Launch, Trail |
| Quality Assurance | 12 | Radar, Voyager, Sentinel, Probe, Judge, Zen, Sweep, Warden, Specter, Siege, Void, Attest |
| Implementation | 4 | Builder, Artisan, Forge, Arena |
| AI/ML | 1 | Oracle |
| Performance | 2 | Bolt, Tuner |
| Observability/SRE | 2 | Beacon, Mend |
| UI/UX | 8 | Vision, Palette, Muse, Flow, Echo, Vitrine, Prose, Frame |
| Documentation | 4 | Scribe, Quill, Morph, Prism |
| Visualization | 2 | Canvas, Sketch |
| Architecture | 4 | Atlas, Horizon, Gateway, Grove |
| Communication | 1 | Relay |
| Data | 2 | Schema, Stream |
| DevOps | 6 | Anvil, Gear, Scaffold, Hearth, Latch, Pipe |
| i18n | 1 | Polyglot |
| Growth | 2 | Growth, Bond |
| Analytics | 3 | Pulse, Experiment, Matrix |
| Operations | 1 | Triage |
| Browser Automation | 3 | Vector, Director, Reel |
| AITuber/Streaming | 1 | Aether |
| **Total** | **85** | |
