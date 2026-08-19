# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Changed — consolidate global roster to 100 skills (2026-08-19)

- Absorbed 11 narrowly scoped skills into broader owners while preserving their recipes and reference material: `cull` → `chain`, `director` → `cue`, `harvest` → `launch`, `zine` → `tome`, `sage` + `summon` → `magi`, `sketch` → `builder`, `crest` → `compete`, `clause` → `canon`, `latch` → `hone`, and `hearth` → `anvil`.
- Archived the 11 source packages under `.archive/` with owner mappings, a retain-through date of 2026-11-17, and explicit restoration steps.
- Updated routing, skill packs, profiles, catalogs, public documentation, and the generated Recipes directory for the 100-global + 3-project-local roster.
- Clarified the active-roster counting convention and corrected stale 111/123/124-skill labels in the public catalog and contributor documentation.

### Changed — Builder reference grounding (2026-08-19)

- Replaced 15 general language, architecture, domain, frontend, implementation, and AI-coding primers with `builder/reference/implementation-policy.md`, a repository-first decision and toolchain-grounding policy.
- Rewired Builder recipes and Kotlin/Rust/Swift specialist references to preserve role-specific checklists while requiring local toolchain evidence for version-sensitive claims.
- Removed frozen chapter links and dependency defaults that could override repository conventions or drift from current primary documentation.

### Changed — skill consolidation and profile repair (2026-08-19)

- Absorbed `accord` into `scribe` as the cross-team `unified` L0-L4 recipe while preserving BDD, traceability, stakeholder, RACI, and staged-elaboration references.
- Absorbed `oath` into `canon` as regulatory compliance recipes while preserving SOC 2, PCI-DSS, HIPAA, ISO 27001, GDPR/EU AI Act, audit-readiness, vendor-risk, and Policy as Code references.
- Archived both merged-in skill packages under `.archive/` with 90-day reactivation instructions; roster 124 → 122.
- Repaired all filtered profiles after the 2026-06-06 rename set, removed the retired `mentor` entry, and added `chisel`, `loom`, and `pdm` to their declared packs.

### Added — `chisel` skill: prompt → executable specification (2026-08-18)

Closes a gap no existing skill held: taking a **supplied prompt** as the object and converting its vague wording into rules that can be executed and scored. Roster 123 → 124.

- **New skill `chisel`** (SKILL.md + 5 references): seven-class ambiguity detection (quality / quantity / explanation level / style / design / technical / judgment) plus open semantic detection for missing actors, objects, comparisons, and scope; ten dispositions (`QUANTIFY` / `BEHAVIORALIZE` / `CRITERIA` / `DECOMPOSE` / `AUDIENCE` / `CONDITION` / `DATE` / `PARAMETERIZE` / `KEEP` / `DELETE`); the Numeric Licensing Cascade against fabricated precision; role decomposition into six slots so no bare title or credential claim survives; an **ambiguity budget** so terms left open are deliberate and recorded; and an eight-item Exit Checklist that blocks delivery. Recipes: `spec` (default) / `scan` / `role` / `audit`.
- **Boundary vs `oracle`**: Oracle owns the prompt *system* — few-shot policy, structured output, versioning, eval gates, cost, and the Instruction Boundary / five-layer triage doctrine. Chisel owns the *wording of a supplied prompt* and consumes that doctrine by reference rather than restating it. Measured functional overlap ≈ 24%, under the 30% confirmation threshold.
- **Consistency with existing repo positions**: role decomposition implements nexus's "never personality adoption" for user-supplied prompts; the ambiguity budget imports `AS-09 Over-Specified Process` and the Process Constraint Tiers so that eliminating every vague term is explicitly *not* the goal; the delete test reuses `_common/MECHANISM_SELECTION.md` § Admission.

**Routing:** new `PROMPT_SPEC` task type (`Chisel`) in `nexus/reference/routing-matrix.md` (95 task types); anchors added under *Specialist Skill Anchors* in `nexus/reference/signal-keywords.md`; a four-way disambiguation entry (Chisel / Oracle / Scribe / Attest) added to `nexus/reference/agent-disambiguation.md`; `_common/BOUNDARIES.md`, `compass/reference/catalog.md`, and `architect/reference/agent-categories.md` updated; added to the `ai-eval` Skill Pack. Registered as a task type rather than a Nexus Recipe — it is a single-agent route with no chain template, like `PRIORITIZE` (Rank) or brainstorming (Riff).

### Added — Apple platform coverage: `dock` skill + perf/design-trend references (2026-07-25)

> **Superseded 2026-07-29 (`a9510248`).** `dock` was absorbed into `native` as the `macos`/`macdist` recipes and no longer exists as a standalone skill; `wield`, referenced below, was absorbed into `hearth` as `automate`. The `MACOS_NATIVE` routing chain no longer starts at `Dock`. The entry is kept verbatim as a record of what shipped on 2026-07-25 — see `_common/HARNESS_DEBT.md` § *A Record is not a derived asset*. Roster as of 2026-08-17: **123 skills**.

Closes three verified gaps in Apple-platform knowledge. Agent count 132 → 133.

- **New skill `dock`** (macOS native application development, 277-line SKILL.md + 15 references, ~3.9k lines total): SwiftUI for macOS + AppKit interop, scene/window architecture, menu bar Commands, document-based apps, NavigationSplitView layout, drag & drop / pasteboard / Services, App Sandbox + entitlements, distribution (App Store vs Developer ID, notarization, Sparkle), XPC / SMAppService helpers, Mac HIG + Liquid Glass on macOS Tahoe 26, and the Catalyst-vs-native decision. Boundary: `dock` **builds** Mac apps; `wield` **automates existing** Mac apps via AppleScript/JXA — zero functional overlap.
- **`native/reference/apple-perf.md`** (324 lines): Apple-platform performance measurement — Instruments template decision table, SwiftUI render perf, launch time, hitches, memory, concurrency cost, MetricKit/`os_signpost` field telemetry, CI perf budgets. Resolves the dangling pointer in `bolt/reference/swift-cheatsheet.md` §11, which claimed to defer SwiftUI perf to a Native reference that did not exist.
- **`vision/reference/apple-design-trends.md`** (266 lines): Apple design *direction* (as distinct from HIG's normative rules in `native/reference/ios-hig.md`) — the Liquid Glass era and its tasteful-vs-wrong uses, 6 direction archetypes, Apple Design Award pattern analysis (2025/2026 winners, multi-source verified), macOS-specific direction, cross-platform coherence, and a durability test.

**Routing:** new `MACOS_NATIVE` task type (`Dock → Radar → Vitrine → Launch`) in `nexus/reference/routing-matrix.md` (99 task types); macOS anchors added to `nexus/reference/signal-keywords.md` (§ renamed *Mobile Native Anchors* → *Native App Anchors (mobile + macOS desktop)*); `mobile` Skill Pack extended to native-app scope with `dock` + `wield` (pack name kept for `mobile-dev` profile compatibility).

### Changed — Anthropic Agent Skills official-spec alignment (2026-06-06)

- **Directory convention**: `references/` (plural) → `reference/` (singular) across all 121 skill folders. Matches Anthropic official example layout. 5,048 path references updated across 375 .md files.
- **Frontmatter `description`**: All 124 SKILL.md `description` fields rewritten to start with a gerund (`-ing` form) per official best-practices for model-invoked discovery. Third-person voice and exclusion rules preserved.

### Changed — 9 skill renames for world-view consistency

Non-metaphor / weak-metaphor names replaced with single-word metaphors that fit the established abstract-1-word convention:

| Old → New | Rationale |
|---|---|
| `researcher` → `field` | role name → fieldwork metaphor |
| `navigator` → `vector` | direct descriptor → directional intent |
| `showcase` → `vitrine` | verb compound → display case |
| `retain` → `bond` | English verb → relationship metaphor |
| `comply` → `oath` | English verb → commitment |
| `mentor` → `agora` | role name → learning marketplace |
| `husk` → `cull` | weak fit → selective eradication |
| `lure` → `bazaar` | manipulative → marketplace orchestration |
| `spider` → `trawl` | industry literal → sweep metaphor |

Git history preserved via `git mv`; all cross-references (PascalCase / paths / backticks / chain-DSL delimiters) updated. Tier 2 high-collision names (`schema` / `stream` / `growth` / `palette` / `pixel`) intentionally left as-is to avoid technical-term collisions.

### Changed — Nexus Recipe refinements

- `venture` Recipe row removed; alias only (≡ `package domain=startup`)
- `bug` / `feature` / `refactor` / `optimize` chains surface conditional steps inline (`Sherpa?`, `Muse?`, `Radar?`, `Bolt (code) / Tuner (DB)` branch)
- Hidden ~78 `classify`-only task types now explicitly documented in SKILL.md
- Chain reference Source-of-Truth hierarchy declared in Routing Quick Start
- 4 orphaned `.mmd` flow diagrams linked from corresponding recipe files

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
| Decision & Strategy | 3 | Magi, Helm, Accord |
| Git/PR Management | 4 | Guardian, Harvest, Launch, Trail |
| Quality Assurance | 10 | Radar, Voyager, Sentinel, Probe, Judge, Zen, Sweep, Siege, Void, Attest |
| Implementation | 3 | Builder, Artisan, Forge |
| AI/ML | 1 | Oracle |
| Performance | 2 | Bolt, Tuner |
| Observability/SRE | 2 | Beacon, Mend |
| UI/UX | 8 | Vision, Palette, Muse, Flow, Echo, Vitrine, Prose, Frame |
| Documentation | 3 | Scribe, Quill, Morph |
| Visualization | 2 | Canvas, Sketch |
| Architecture | 4 | Atlas, Horizon, Gateway, Grove |
| Communication | 1 | Relay |
| Data | 2 | Schema, Stream |
| DevOps | 6 | Anvil, Gear, Scaffold, Hearth, Latch, Pipe |
| i18n | 1 | Polyglot |
| Growth | 2 | Growth, Bond |
| Analytics | 3 | Pulse, Experiment, Matrix |
| Operations | 1 | Triage |
| Browser Automation | 2 | Vector, Director |
| **Total** | **78** | |
