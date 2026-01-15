# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.0.0] - 2025-01-15

### Added

#### New Agents
- **Artisan** - フロントエンド本番実装の職人（React/Vue/Svelte、Hooks、状態管理）
- **Showcase** - Storybookストーリー作成・カタログ管理・Visual Regression連携
- **Vision** - クリエイティブディレクション・Design System構築
- **Probe** - セキュリティ動的テスト（DAST）・ペネトレーションテスト
- **Tuner** - DBパフォーマンス最適化・EXPLAIN ANALYZE分析
- **Researcher** - ユーザーリサーチ設計・インタビューガイド作成
- **Voyager** - E2Eテスト専門（Playwright/Cypress）
- **Judge** - codex reviewによるコードレビュー・PRレビュー自動化
- **Rabbit** - coderabbit reviewによるコードレビュー・自動修正
- **Anvil** - Terminal UI構築・CLI開発支援

#### Features
- **AUTORUN_FULL mode** - ガードレール付き完全自動実行モード
- 40種類の専門エージェント体制
- 全エージェントの使用例を完備
- タスクタイプ別チェーンテンプレート（11カテゴリ、41テンプレート）

### Enhanced
- **Vision** - 2025-2026デザイントレンド、AI設計ツール統合（Figma AI、v0、Claude）
- **Artisan** - Vue 3 Composition API、Svelte 5 Runes、スタイリング戦略ガイド
- **Showcase** - Storybook 8対応、MDX 3ドキュメント、Figma連携
- **Mason** - TDD、Event Sourcing、CQRS、Forgeからの自動引き継ぎ

### Changed
- AUTORUN_FULLをデフォルトモードに設定
- プラットフォーム非依存に対応（Claude Code、Codex CLI、Gemini CLI等）
- エージェント境界定義の明確化（Bolt vs Tuner、Schema vs Tuner等）

### Removed
- **Roadmap** - PM向け機能のため削除
- **Insight** - Spark/Scoutに統合
- **Lens** - Canvas/Showcaseに統合
- **Fixture** - Mason/Radarに統合

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
| Orchestration | 2 | Nexus, Sherpa |
| Research & Planning | 5 | Scout, Spark, Compete, Voice, Researcher |
| Quality Assurance | 7 | Radar, Voyager, Sentinel, Probe, Judge, Rabbit, Zen |
| Implementation | 3 | Mason, Artisan, Forge |
| Performance | 2 | Bolt, Tuner |
| UI/UX | 6 | Vision, Palette, Muse, Flow, Echo, Showcase |
| Documentation | 1 | Quill |
| Visualization | 1 | Canvas |
| Architecture | 3 | Atlas, Horizon, Gateway |
| Data | 1 | Schema |
| DevOps | 3 | Anvil, Gear, Scaffold |
| i18n | 1 | Polyglot |
| Growth | 2 | Growth, Retain |
| Analytics | 2 | Pulse, Experiment |
| Operations | 1 | Triage |
| **Total** | **40** | |
