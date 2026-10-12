# AI Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Global Agents](https://img.shields.io/badge/Global_Agents-90-blue.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

🤖 90のグローバルスキルと3つのproject-local拡張による協調開発を実現するスキルコレクション

## ✨ Features

- **90のグローバルエージェント + 3つのproject-local拡張** - バグ調査、テスト、セキュリティ、UI/UX、AI/ML、可観測性、インフラまで網羅
- **Nexusオーケストレーター** - タスクを分析し最適なエージェントチェーンを自動設計
- **プラットフォーム非依存** - Claude Code、Codex CLI、Antigravity CLI等で動作

## 🚀 Quick Start

### インストール

**推奨 — 1つの作業ツリーを全 CLI で共有**

```bash
git clone https://github.com/simota/agent-skills.git ~/repos/agent-skills
cd ~/repos/agent-skills
make link
```

`make link` は各スキルディレクトリを `~/.claude/skills`・`~/.agents/skills`・`~/.gemini/antigravity-cli/skills` へ
個別に symlink します。全 CLI が同一の作業ツリーを読むため、`git pull` 1回で全 CLI が最新になります。
それらのディレクトリに既にあるスキルは維持されます — 同名エントリは報告のうえ skip され、上書きされる
ことはありません。配置先の親ディレクトリが無ければ、下記の保護付きCodex移行を除いてskipするため、CLIが1つだけの環境でも利用できます。ディレクトリの有無は配置の手掛かりであり、実際のCLI利用可否を保証しません。

| コマンド | 効果 |
|---------|------|
| `make link` | 3つの CLI ディレクトリへ一括リンク — 個別は `link-claude` / `link-codex` / `link-agy` |
| `make status` | CLI ごとのリンク数（`リンク済み / リンク対象`）と総エントリ数を表示 |
| `make unlink` | `make link` が作成したリンクのみ削除。他のスキルや独自の別名リンクはそのまま残る |

**シンプル — CLI ディレクトリへ直接クローン**

```bash
# Claude Code の場合
git clone https://github.com/simota/agent-skills.git ~/.claude/skills

# その他のプラットフォーム
git clone https://github.com/simota/agent-skills.git /path/to/your/skills
```

対象ディレクトリがまだ存在せず、1つの CLI でしか使わない場合はこちらが最短です。

### 使用方法

```
/Nexus ログイン機能を実装したい
/Scout このバグの原因を調査して
/Radar テストカバレッジを向上させて
/Vision ダッシュボードをモダンにリデザインしたい
```

### 実行環境の互換性と旧Codexインストール

最新モデル・CLI仕様・公式根拠は [`_common/CLI_COMPATIBILITY.md`](_common/CLI_COMPATIBILITY.md) に集約しています。スキル本体はモデル非依存です。実環境の利用権限・機能・スキル読込は別途確認してください。Gemini CLIとCursorは追加の読取環境であり、インストーラーの対象追加ではありません。

Codexのスキル配置先は `~/.agents/skills`、設定は引き続き `~/.codex` です。旧配置は自動削除しません。**このリポジトリが作った旧リンクだけ**を外す場合は `make unlink-codex CODEX_DIR="$HOME/.codex/skills"` の結果を確認し、`make link-codex` を実行してください。他のファイルやリンクは保持します。`.agents` がなく `.codex` が存在する場合、新しい親ディレクトリをソースリポジトリ外に限って作成します。それ以外は意図した外部配置先を明示的に準備してください。

## 📚 概要

このリポジトリには、ソフトウェア開発の様々な側面を専門とする90のグローバルエージェントと、3つのproject-local拡張が含まれています。各エージェントは特定のドメインに特化しており、**Nexus**オーケストレーターによって統括・連携されます。

### スキル数の数え方

- **90のグローバルスキル**は、`<skill-name>/SKILL.md`配下の再利用可能なアクティブロスターです。
- **3つのproject-local拡張**（`orbit`、`lore`、`darwin`）はこのリポジトリ専用の運用スキルで、グローバル数やグローバルプロファイルには含めません。
- `.claude/skills/`がproject-localの正本、`.agents/skills/`がクロスツール用のミラーであり、別スキルとして重複カウントしません。
- `.archive/`はロールバック用の非アクティブパッケージで、アクティブロスター数から除外します。

したがって、現在のアクティブ構成は **90 global + 3 project-local = 93の個別スキル**です。

## エージェント一覧

> 90のグローバルエージェントと、明記した3つのproject-local拡張のカテゴリ別カタログ。

### オーケストレーション

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Nexus** | _"The right agent at the right time changes everything."_ - チーム統括と規模適応型プロダクトデリバリー。最小限のエージェントチェーンを設計・実行 | プロンプト、進行管理 |
| **Sherpa** | _"The mountain doesn't care about your deadline. Plan accordingly."_ - タスク分解ガイド。複雑なタスクを15分以内のAtomic Stepに分解 | チェックリスト |
| **Architect** | _"Every agent is a possibility. Every SKILL.md is a birth certificate."_ - 新しいスキルエージェントを設計・生成するメタデザイナー。エコシステムギャップ分析、重複検出、SKILL.md生成 | SKILL.md、references |
| **Rally** | _"One task, many hands. Parallel by design."_ - マルチセッション並列オーケストレーター。Claude Code Agent Teams APIで複数Claudeインスタンスを生成・管理し、並行タスク実行を実現 | チーム管理、並列実行 |
| **Sigil** | _"Every project has patterns waiting to become power."_ - プロジェクト運用レイヤー設計・生成。スキル、レシピ、ワークフロー、ルーティングマップを作成 | プロジェクト固有スキル |
| **Gauge** | _"What gets measured gets managed. What gets audited gets normalized."_ - SKILL.md正規化監査・自己進化エージェント。21項目チェックリストに基づくコンプライアンススキャン、修正提案、Webベースのベストプラクティス自動取得 | コンプライアンスレポート、修正プラン |
| **Orbit** *(project-local)* | _"Give me a goal. I'll give you a runner that finishes."_ - このリポジトリのNexus-autoloop完走スクリプト生成・運用契約設計・監査を担当 | ランナースクリプト、契約 |
| **Darwin** *(project-local)* | _"Ecosystems that cannot sense themselves cannot evolve themselves."_ - `.agents/ECOSYSTEM.md`へ永続化する、このリポジトリ専用のエコシステム進化オーケストレーター | エコシステムフィットネススコア、進化提案 |
| **Lore** *(project-local)* | _"Forgotten lessons are lessons repeated. Institutional memory is the compound interest of experience."_ - `.agents/*.md`を`METAPATTERNS.md`へ統合する、このリポジトリ専用の知識キュレーター | METAPATTERNS.md、知識インサイト |
| **Atelier** | _"Design decided upstream. Assets produced downstream. atelier is the studio floor in between."_ - デザインから実装までを閉ループで繋ぐパイプラインオーケストレーター。Vision → Muse/Frame → Forge → Artisan → Vitrine → Canvas を統括し、デザイン抽出・プロトタイプ・ビジュアルアセット・スライド・本番実装をプロジェクトデザインシステムを永続化しながら一気通貫で提供 | デザインシステムパッケージ、統合成果物 |
| **Compass** | _"When in doubt, ask Compass. It finds the right skill for the task."_ - 90のグローバルスキルと利用可能なproject-local拡張から、タスクに最適な担当を推薦 | レコメンド、エージェントマップ |
| **Prune** | _"A garden grows by what you cut, not what you plant."_ - スキルエコシステム整理監査エージェント。エージェント編成の重複・冗長・不活性を監査し、統合候補とサンセット計画を根拠・アーカイブ手順付きで提案（提案のみ・実行はしない） | 整理監査レポート、統合/サンセット提案 |

### 調査・企画（コードを書かない）

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Scout** | _"Every bug has a story. I read the ending first."_ - バグ調査・根本原因分析（RCA）。再現手順と修正箇所を特定 | 調査レポート |
| **Ripple** | _"Every change sends ripples. Know where they land before you leap."_ - 変更前の影響分析。縦（依存関係・影響ファイル）と横（パターン一貫性・命名規則）の両面からリスク評価 | 影響分析レポート |
| **Spark** | _"The best feature is the one users didn't know they needed."_ - 新機能提案。既存データ/ロジックを活用した機能をMarkdownで提案 | 仕様書 |
| **Compete** | _"Know your enemy. Know the market. Know yourself."_ - 競合調査・差別化・ポジショニングに加え、GitHub、LinkedIn、ポートフォリオ、技術発信、登壇を横断するエンジニア個人ブランドを設計 | 競合分析・ポジショニング・ブランド戦略 |
| **Voice** | _"Feedback is a gift. Analysis is unwrapping it."_ - ユーザーフィードバック収集・NPS調査設計・感情分析・インサイト抽出 | フィードバックレポート |
| **Field** | _"Good research asks the right questions. Great research changes what you thought was the question."_ - ユーザーリサーチ設計・インタビューガイド作成・定性分析・ペルソナ/ジャーニーマップ作成 | リサーチレポート |
| **Trace** | _"Every click tells a story. I read between the actions."_ - セッションリプレイ分析・ペルソナ別行動パターン抽出・UX問題の物語化。Field/Echoと連携 | 行動分析レポート |
| **Canon** | _"Standards are the accumulated wisdom of the industry. Apply them, don't reinvent them."_ - OWASP/WCAG/OpenAPI/ISO 25010、SOC2/PCI-DSS/HIPAA/ISO 27001の準拠評価に加え、利用規約、プライバシーポリシー、DPA/EULA、Cookie同意、広告表現をレビュー | 準拠度・法務文書レビューレポート |
| **Lens** | _"See the code, not just search it."_ - コードベース理解・調査スペシャリスト。「〇〇機能はあるか」「〇〇のフローはどうか」「このモジュールの責務は何か」をコード構造把握・機能探索・データフロー追跡で体系的に調査 | 調査レポート |
| **Magi** | _"Three minds, one verdict. Consensus through diversity."_ - 3視点の意思決定に、創業者向けoffice hours、ボトルネック診断、ピッチ批評、著名人の文書化された思考に基づく助言レンズ、経営シナリオシミュレーション（`simulate` Recipe）を統合 | 意思決定・助言レポート |
| **Flux** | _"Bend the light. See what was always there."_ - 思考屈折エンジン。前提を疑い、異分野知識を組み合わせ、視点をずらして問題を再構成。Cynefinベースのフレームワーク選択、Serendipity Injection、10+思考フレームワーク、拡散/提案/評価/引き算の多ターン発想（`ideate` Recipe）。コードは書かない | リフレーミングパッケージ、Insight Matrix、Blind Spot Report |
| **Cast** | _"Personas are not invented. They are discovered, born, and evolved."_ - ペルソナキャスティングエージェント。多種多様な入力からペルソナを迅速生成・永続化・ライフサイクル管理し、下流エージェントに統一フォーマットで配信 | ペルソナレジストリ |
| **Matrix** | _"Infinite combinations, finite resources. Matrix finds the minimum that covers the maximum."_ - 任意の多次元軸×値を入力とし、組み合わせ爆発を制御するユニバーサル分析エージェント。最小カバレッジセット選定・実行計画・優先順位付け。テスト・デプロイ・UX検証・リスク評価・互換性など全ドメイン対応。コードは書かない | マトリクス分析、カバレッジ最適化計画 |
| **Saga** | _"Facts are remembered 5-10% of the time. Stories raise that to 65-70%. The customer is the hero. The product is the guide."_ - プロダクト・機能のユースケースをストーリーテリングで語るナラティブデザインエージェント。顧客体験の物語化、シナリオストーリー、プロダクトナラティブ。コードは書かない | ナラティブドキュメント |
| **Omen** | _"Plan for the worst. Build for the best."_ - プリモーテム分析・障害モード列挙。計画・設計・機能のリスクシナリオをRPN/APスコアリングで体系的に特定。コードは書かない | プリモーテムレポート |
| **Rank** | _"Every priority tells a story of trade-offs."_ - 優先度定量化エージェント。ICE/RICE/WSJF/MoSCoW/Kanoフレームワークで競合アイテムをスコアリング・順序付け。コードは書かない | 優先度レポート |
| **PDM** | _"Show where the project stands — planned, built, and the gap between."_ - PdMスタイルのリードオンリー・デリバリー状況ナビゲーター。計画スコープ（仕様/Issue/ロードマップ/PRD）と実装済みコードを突き合わせ、機能インベントリ、未実装機能リスト、ロードマップロールアップ、WBSビューを生成。「何ができていて、何が残っていて、今どこか」に回答 | 機能インベントリ、未実装リスト、WBS |

**Scout → Ripple → Builder の連携**：Scout（バグ調査）→ Ripple（修正の影響分析）→ Builder（実装）
**Ripple → Guardian の連携**：Ripple（影響分析）→ Guardian（PR戦略）
**Field → Trace → Echo の連携**：Field（ペルソナ定義）→ Trace（実データ検証）→ Echo（シミュレーション確認）
**Sentinel → Canon → Builder の連携**：Sentinel（脆弱性検出）→ Canon（OWASP準拠評価）→ Builder（修正実装）
**Gateway → Canon → Gateway の連携**：Gateway（API設計）→ Canon（OpenAPI/RFC準拠確認）→ Gateway（修正）
**Echo → Canon → Palette の連携**：Echo（UX問題）→ Canon（WCAG準拠評価）→ Palette（アクセシビリティ修正）
**Field → Cast → Echo の連携**：Field（調査データ）→ Cast（ペルソナ統合）→ Echo（UI検証）
**Trace → Cast の連携**：Trace（行動データ）→ Cast（ペルソナ進化）

### Git/PR管理

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Guardian** | _"Every commit tells a story. Make it worth reading."_ - Git/PRの番人。変更のSignal/Noise分析、コミット粒度最適化、ブランチ命名、PR戦略提案 | 分析レポート、PR準備 |
| **Launch** | _"Shipping is not the end. It's the beginning of accountability."_ - リリース管理に、GitHub PRのread-only収集、週次/月次/client report、DORA/SPACE指標、retrospective、PDF出力を統合 | リリース計画、CHANGELOG、デリバリーレポート |
| **Trail** | _"Every bug has a birthday. Every regression has a parent commit. Find them."_ - Git履歴調査・リグレッション原因分析・コード考古学。時間を遡って真相を解明 | 履歴調査レポート |

**Guardian → Judge → Zen の連携**：Guardian（PR準備）→ Judge（レビュー）→ Zen（修正）
**Guardian → Launch の連携**：Guardian（変更分析）→ Launch（リリース計画）
**Trail → Scout の連携**：Trail（リグレッション特定）→ Scout（詳細調査）

### 品質保証

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Radar** | _"Untested code is unfinished code."_ - ユニット/統合テスト追加・フレーキーテスト修正・カバレッジ向上・テストデータ/フィクスチャ生成（`fixtures` Recipe） | テストコード |
| **Voyager** | _"E2E tests are the user's advocate in CI/CD."_ - Web・モバイル・iOS E2E専門。Playwright/Cypress/Appium/Detox/Maestro、XCUITest、App Storeスナップショットに対応 | E2Eテストコード |
| **Sentinel** | _"Security is not a feature. It's a responsibility."_ - セキュリティ静的分析（SAST）・脆弱性パターン検出・入力検証追加 | セキュリティ修正 |
| **Probe** | _"A system is only as secure as its weakest endpoint."_ - セキュリティ動的テスト（DAST）・OWASP ZAP/Nuclei連携・ペネトレーションテスト | 脆弱性レポート |
| **Judge** | _"Good code needs no defense. Bad code has no excuse."_ - codex reviewによるコードレビュー・PRレビュー自動化・コミット前チェック・AI幻覚検出 | レビューレポート |
| **Zen** | _"Clean code is not written. It's rewritten."_ - リファクタリング・コード品質改善（動作は変えない） | コード改善 |
| **Sweep** | _"Dead code is technical debt that earns no interest."_ - 不要ファイル検出・未使用コード特定・孤立ファイル発見・安全な削除提案 | クリーンアップ提案 |
| **Attest** | _"Specs are truth. Code is evidence. Attest finds the gaps."_ - 仕様適合検証エージェント。仕様書から受入基準を抽出し、BDDシナリオを生成し、実装が仕様通りか敵対的に検証。CERTIFIED/CONDITIONAL/REJECTED判定を発行 | 適合レポート、BDDシナリオ |
| **Siege** | _"Break it before users do. Fix it before they notice."_ - 高度テストスペシャリスト。負荷テスト（k6/Locust/Artillery）、契約テスト（Pact CDC）、カオスエンジニアリング、ミューテーションテスト、レジリエンスパターン検証 | テスト結果、レジリエンスレポート |
| **Void** | _"The best code is the code that was never written."_ - YAGNI検証・スコープカット・機能プルーニング・複雑性削減提案。5つの存在検証問とCost-of-Keeping Scoreで不要な複雑性を特定 | 削減提案 |
| **Vigil** | _"An undetected attack is an undefended system. Vigil ensures nothing passes unseen."_ - Detection Engineeringエージェント。Sigma/YARAルール設計、検出カバレッジマッピング、脅威ハンティング仮説設計、Detection-as-Code CI/CD統合 | 検出ルール、カバレッジマップ |
| **Breach** | _"Think like an attacker. Defend like an engineer."_ - レッドチームエンジニアリング。攻撃シナリオ設計、脅威モデリング、MITRE ATT&CK/OWASPフレームワーク、Purple Team演習、AI/LLMレッドチーミング | セキュリティ評価 |
| **Cloak** | _"Privacy is not a feature. It's a right."_ - プライバシーエンジニアリング・データガバナンス。PII検出、データフローマッピング、同意管理、GDPR/CCPA準拠コード実装 | プライバシー評価 |
| **Chain** | _"Treat every third-party skill like an npm install. Audit before invoking."_ - スキル/プラグイン/MCPの受け入れ監査と、npm/PyPIマルウェアのlive調査を担当。sha256、Unicode/窃取パターン、campaign IoC、永続化優先の駆除、認証情報ローテーションを扱う | サプライチェーン監査、感染レポート、復旧runbook |

### 実装

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Builder** | _"Types are contracts. Code is a promise."_ - 型安全な本番実装に、Gemini画像生成・編集コード、prompt設計、batch生成、style transfer、後処理、provenance、content-policy gateに加え、CLI/TUI構築（`cli`）と regex/parser/DSL設計（`grammar`）を統合 | プロダクションコード、画像生成コード |
| **Artisan** | _"Prototypes promise. Production delivers."_ - フロントエンド本番実装の職人。React/Vue/Svelte、Hooks設計、状態管理、Server Components、フォーム処理、データフェッチング | フロントエンドコード |
| **Forge** | _"Done is better than perfect. Ship it, learn, iterate."_ - プロトタイプ作成。完璧より動くものを優先。Builder連携用にtypes.ts, errors.ts, forge-insights.mdを出力 | MVP/PoC |
| **Native** | _"Every pixel ships. Every platform matters."_ - Pure-nativeモバイル実装スペシャリスト。iOS（Swift 6.3 + SwiftUI + Liquid Glass）と Android（Kotlin 2.4+ + Jetpack Compose + Material 3 Expressive）。@Observable/Swift Concurrency、Compose Strong Skipping + Type-safe Navigation、SwiftData/Room、Credential Manager + Passkey、Privacy Manifest、edge-to-edge、predictive back、Live Activities、App Intents、Foundation Models / Gemini Nano、ストア準拠、ステージドロールアウト。React Native / Flutter / KMP / CMP は対象外 | コード |
| **Pixel** | _"Every pixel matters. Fidelity is non-negotiable."_ - 画像モックアップ（PNG/JPG/スクリーンショット）からピクセルパーフェクトなHTML/CSSを生成し、視覚的検証を行う忠実再現エージェント | HTML/CSSコード |

### AI/ML

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Oracle** | _"AI is only as good as its architecture. Design it, measure it, trust nothing."_ - AI/ML設計・評価スペシャリスト。プロンプトエンジニアリング、RAGアーキテクチャ、LLMアプリケーションパターン、安全ガードレール、評価フレームワーク、MLOps、コスト最適化 | 設計仕様、評価レポート |
| **Chisel** | _"A vague word is a decision you left to chance. Carve it into something that can be checked."_ - プロンプトを実行仕様へ変換するスペシャリスト。品質・分量・文体・デザイン・判断の曖昧語を検出し、役割/肩書きを能力と評価軸へ分解し、矛盾する指示を整理し、意図的に開いたままにした箇所を記録する | 曖昧表現の台帳、仕様化済みプロンプト |

**Oracle → Builder → Radar の連携**：Oracle（AI/ML設計）→ Builder（実装）→ Radar（テスト）
**Oracle → Stream → Builder の連携**：Oracle（RAG設計）→ Stream（データパイプライン）→ Builder（実装）
**Oracle → Sentinel → Oracle の連携**：Oracle（安全性設計）→ Sentinel（セキュリティレビュー）→ Oracle（改善）

### パフォーマンス

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Bolt** | _"Speed is a feature. Slowness is a bug you haven't fixed yet."_ - アプリケーションパフォーマンス改善。フロント（再レンダリング削減）とバック（N+1修正）両面 | 最適化コード |
| **Tuner** | _"A fast query is a happy user. A slow query is a lost customer."_ - DBパフォーマンス最適化。EXPLAIN ANALYZE分析・インデックス推奨・スロークエリ改善 | クエリ最適化 |

### 可観測性/SRE

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Beacon** | _"You can't fix what you can't see. You can't see what you don't measure."_ - 可観測性・信頼性エンジニアリングスペシャリスト。SLO/SLI設計、分散トレーシング、アラート戦略、ダッシュボード設計、キャパシティプランニング、トイル自動化 | SLO定義、可観測性仕様 |

**Beacon → Gear → Builder の連携**：Beacon（可観測性設計）→ Gear（監視実装）→ Builder（計装）
**Triage → Beacon → Gear の連携**：Triage（インシデント事後分析）→ Beacon（監視改善）→ Gear（実装）

### UI/UX

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Vision** | _"Design is not how it looks. Design is how it feels."_ - クリエイティブディレクション。デザイン方向性決定・Design System構築・Muse/Palette/Flow/Forgeのオーケストレーション | デザイン戦略 |
| **Palette** | _"Usability is invisible when done right, painful when done wrong."_ - ユーザビリティ改善・認知負荷軽減・a11y対応 | UX改善 |
| **Muse** | _"Tokens are the DNA of design. Mutate them with care."_ - デザイントークン適用・余白/角丸/シャドウ統一・ダークモード対応 | 視覚的改善 |
| **Flow** | _"Motion creates emotion. Animation breathes life."_ - UIアニメーション・ホバー効果・ローディング状態・モーダル遷移 | アニメーション |
| **Echo** | _"I don't test interfaces. I feel what users feel."_ - ペルソナ検証と合成需要。UI混乱、機能要望、JTBD、未充足ニーズを分析 | UXレポート |
| **Vitrine** | _"Components without stories are components without context."_ - Storybookストーリー作成・カタログ管理・Visual Regression連携。CSF 3.0形式 | Storybook Stories |
| **Prose** | _"Words are the smallest unit of design. Get them wrong, and nothing else matters."_ - ユーザー向けテキストの専門エージェント。マイクロコピー、エラーメッセージ、ボイス＆トーンフレームワーク、オンボーディングコピー、アクセシビリティテキスト | コピーガイドライン、コンテンツ仕様 |
| **Frame** | _"Design speaks in pixels. I translate it to code."_ - Figma MCP Serverを活用してデザインコンテキストを抽出・構造化し、実装エージェントに渡すブリッジエージェント。デザインからコードへの橋渡し、Code Connect管理、デザインシステムルール抽出。コードは書かない | 構造化デザインコンテキスト、デザインシステムルール |
| **Ink** | _"Every stroke serves a purpose."_ - SVGアイコン/イラスト生成、アイコンシステム設計、スプライトシンボル構築 | SVGアセット |

### ドキュメント

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Scribe** | _"A specification is a contract between vision and reality."_ - PRD/SRS/HLD/LLDと部門横断L0-L4仕様（`unified` Recipe）、実装チェックリスト、テスト仕様書を作成し、ドキュメントフォーマット変換（`convert` Recipe）も担う仕様エージェント | 仕様書・設計書 |
| **Quill** | _"Code tells computers what to do. Documentation tells humans why."_ - JSDoc/TSDoc追加・README更新・any型の型定義化 | ドキュメント |
| **Tome** | _"Changes are forgotten. Knowledge endures."_ - 変更を学習ドキュメントへ、検証済み知識をnote/Zenn/Qiita/dev.to向け技術記事へ変換。連載管理とcross-platform再利用にも対応 | 学習ドキュメント、技術記事 |

**Scribe vs Quill vs Tome の役割分担**:
- **Scribe**: プロジェクトドキュメント（PRD、SRS、設計書、チェックリスト、テスト仕様書）とフォーマット変換（Markdown→PDF/Word/HTML、`convert` Recipe）
- **Quill**: コードドキュメント（JSDoc/TSDoc、README、型定義）
- **Tome**: 変更ベース学習教材とnote/Zenn/Qiita/dev.to向け外部公開記事・連載管理

### 可視化

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Canvas** | _"A diagram is worth a thousand lines of documentation."_ - 設計可視化。コード・仕様・コンテキストをMermaid図またはASCIIアート（フローチャート、シーケンス図、状態遷移図、クラス図、ER図等）に変換 | Mermaid図 / ASCII Art |
| **Cue** | _"Every frame tells a story."_ - 動画台本・絵コンテ・ナレーションに、Playwrightデモ収録、複数aspect、字幕、品質gate、voiceover、transcript、thumbnail制作を統合 | 動画企画、デモ、公開用assets |
| **Stage** | _"Every slide is a stage."_ - Marp/reveal.js/Slidevによるスライド生成、ストーリー構成設計、カンファレンストーク最適化 | スライドデッキ |
### アーキテクチャ

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Atlas** | _"Dependencies are destiny. Map them before they map you."_ - 依存関係分析・循環参照検出・ADR/RFC作成 | 設計文書 |
| **Port** | _"From web to native. Translate the experience, not just the code."_ - WebアプリからiOS Swift / Android Kotlin pure-nativeへのポーティング設計スペシャリスト（2026仕様：Liquid Glass / Material 3 Expressive / Swift 6.3 / targetSdk 36 / Privacy Manifest / 5.1.2(i) AI開示対応）。機能パリティマトリクス、ネイティブアーキテクチャマップ、規制コンプライアンス計画、Strangler-Fig段階的ロードマップを生成。Pure-Native UI + KMP共有ロジックのハイブリッドパスも提案可 | ポーティング設計、パリティマトリクス、ロードマップ |
| **Gateway** | _"APIs are promises to the future. Design them like contracts."_ - API設計・レビュー・OpenAPI仕様生成・バージョニング戦略・破壊的変更検出・メッセージング統合（`messaging` Recipe） | API仕様書 |
| **Grove** | _"A well-structured repository is a well-structured mind."_ - 人間とLLM向けリポジトリ構造の設計・監査。コンテキスト効率、プロンプトキャッシュ、シャーディングを含む | 構造設計・監査レポート |
| **Weave** | _"Every state tells a story. Every transition is a contract."_ - ワークフロー＆ステートマシン設計エージェント。状態遷移設計、不正遷移検出、Sagaパターン、承認フロー設計、cron/タイムゾーン/営業日スケジューリング（`schedule` Recipe） | 設計、図 |
| **Seek** | _"The right result at the right time in the right order."_ - 検索エンジン・ベクトルDB設計エージェント。全文検索/ベクトル検索/ハイブリッド検索の設計・インデックス最適化・RAG Retrieval層実装 | コード、設定 |
| **Crypt** | _"Trust no channel. Verify every key."_ - 暗号アーキテクチャ設計。アルゴリズム選定、鍵管理、E2E暗号化、KMS統合、TLS設定 | 暗号設計仕様 |

**Gateway → Builder → Radar の連携**：Gateway（メッセージング設計）→ Builder（実装）→ Radar（テスト）

### データ

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Schema** | _"A schema is a contract with the future."_ - DBスキーマ、マイグレーション、ER図、マルチテナント分離/RLS/ルーティング設計 | マイグレーション/スキーマ定義 |
| **Stream** | _"Data flows like water. My job is to build the pipes."_ - データパイプライン。ETL/ELT設計、Kafka/Airflow/dbt、バッチ/ストリーミング選定、データ品質管理 | パイプライン設計、DAG、dbtモデル |

**Schema → Stream の連携**：Schema（データモデル）→ Stream（パイプライン設計）

### DevOps

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Gear** | _"The best CI/CD is the one nobody thinks about."_ - 依存関係、CI/CD、Docker最適化、高度なGitHub Actions設計 | 設定ファイル |
| **Scaffold** | _"Infrastructure is the silent foundation of every dream."_ - クラウドインフラ（Terraform/CloudFormation/Pulumi）・ローカル開発環境（Docker Compose）・IaC設計 | インフラ設定 |
| **Hone** | _"A sharp blade cuts clean. A sharp config cuts friction."_ - Codex/Antigravity/Claude Code設定の監査と、Claude Code lifecycle hookの設計・設定・デバッグを担当。対象をhooks節と必要scriptに限定し検証。個人環境（dotfiles/シェル/エディタ）とmacOS自動化（`env`/`automate` Recipe）も担当 | 監査レポート、改善提案、hook設定 |
| **Ledger** | _"Every dollar has a story. Make it a short one."_ - FinOps／クラウドコスト最適化エージェント。IaCコードからのコスト推定、right-sizing提案、RI/SP推奨、コスト異常検知 | レポート、設定 |
| **Shift** | _"Migration is not moving. It's transforming."_ - マイグレーション＆アップグレードオーケストレーター。フレームワーク・ライブラリ・API・DB・インフラの移行をcodemod生成・段階的戦略でエンドツーエンド実行 | マイグレーション計画 |

**Builder vs Hone vs Gear vs Scaffold の役割分担**:
- **Builder**: CLI/TUI構築（`cli` Recipe）— ツール本体の実装
- **Hone**: 個人環境（dotfiles、シェル、エディタ、ターミナル、macOS自動化）とAI CLI設定監査・Claude Codeイベントフックの設計/設定/デバッグ
- **Gear**: プロジェクトレベルのDevOps（CI/CD、Docker、監視、Gitフック）。高度なGitHub Actionsは `gha` モード
- **Scaffold**: インフラプロビジョニング（クラウド、Docker Compose、IaC）

### 国際化

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Polyglot** | _"Every language deserves respect. Every user deserves their mother tongue."_ - i18n対応。ハードコード文字列をt()関数に置換・Intl APIで日付/通貨フォーマット | i18n対応 |

### 成長

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Growth** | _"Traffic without conversion is just expensive vanity."_ - SEO（meta/OGP/JSON-LD）・SMO（SNSシェア表示）・CRO（CTA改善）・リテンション/再エンゲージメント設計（`retention` Recipe） | 成長施策 |
| **Funnel** | _"Above the fold is your one shot. Make every pixel convert."_ - LP（ランディングページ）のコンバージョン戦略とプレミアム制作パイプライン。フレームワーク（AIDA/PAS/BAB/4Ps）に基づく構造設計、ヒーローセクション、CTA配置戦略、Social Proof階層、モバイルファーストのレスポンシブ実装 | LP構造、コピー、仕様 |

### 分析

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Pulse** | _"What gets measured gets managed. What gets measured wrong gets destroyed."_ - KPI定義・トラッキングイベント設計・ダッシュボード仕様作成 | メトリクス設計 |
| **Experiment** | _"Every hypothesis deserves a fair trial. Every decision deserves data."_ - A/Bテスト設計・仮説ドキュメント作成・サンプルサイズ計算・フィーチャーフラグ実装 | 実験レポート |

### 運用

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Triage** | _"In chaos, clarity is the first act of healing."_ - 障害対応・影響範囲特定・復旧手順策定・ポストモーテム作成 | 運用レポート |
| **Mend** | _"Known failures deserve known fixes. Speed of recovery defines reliability."_ - 既知障害パターンの自動修復エージェント。Triageの診断結果やBeaconのアラートを受け、安全ティア分類に基づくrunbook実行・段階的検証・ロールバックまで一貫して担当 | 修復結果、検証レポート |

**Triage → Mend → Beacon の連携**：Triage（診断）→ Mend（自動修復）→ Beacon（復旧監視）

### ブラウザ自動化

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Vector** | _"The browser is a stage. Every click is a scene."_ - Playwright/Chrome DevToolsによるブラウザ操作自動化。データ収集、フォーム操作、スクリーンショット取得、ネットワーク監視、クロールシステム設計（`crawl` Recipe） | 自動化スクリプト |

**Cue と Vitrine の役割分担**:
- **Cue**: ブラウザ（Web UI）のデモ動画（Playwright、.webm出力）
- **Vitrine**: コンポーネントカタログと Storybook ストーリー、ビジュアルリグレッション連携

## ワークフロー

### 基本的な使い方

1. `/AgentName` でエージェントを呼び出し
2. エージェントがタスクを実行
3. 必要に応じて他エージェントへの引き継ぎを提案

### Nexusによるオーケストレーション

複雑なタスクには**Nexus**を使用します。Nexusは以下のモードで動作します：

| モード | トリガー | 動作 | 対話 |
|--------|----------|------|------|
| **Full Auto**（デフォルト） | マーカーなし、または `## NEXUS_AUTORUN_FULL` | ガードレール付きで全タスクを実行 | Ask First / エラー時のみ |
| **Auto** | `## NEXUS_AUTORUN` | 単純タスクのみ実行、複雑なタスクは Guided に切替 | エラー時のみ |
| **Guided** | `## NEXUS_GUIDED` | 判断ポイントで確認 | 選択肢形式で対話 |
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

#### 調査・理解

| タスク | 説明 | チェーン |
|--------|------|----------|
| INVESTIGATE/feature | 機能の有無・実装状況調査 | Lens |
| INVESTIGATE/flow | データフロー・処理フロー追跡 | Lens → Canvas |
| INVESTIGATE/onboarding | コードベース全体理解 | Lens → Scribe |
| INVESTIGATE/pre-impl | 調査→実装 | Lens → Builder → Radar |

> **Lens vs Scout**: Lens = コードベース理解・機能探索（「〇〇はあるか」「フローはどうか」）、Scout = バグ調査・根本原因分析（「なぜ壊れたか」）

#### バグ修正

| タスク | 説明 | チェーン |
|--------|------|----------|
| BUG/simple | 単純なバグ修正 | Scout → Builder → Radar |
| BUG/complex | 複雑なバグ（RCA必要） | Scout → Sherpa → Builder → Radar → Sentinel |
| BUG/frontend | フロントエンドのバグ | Scout → Artisan → Radar |

#### 機能開発

| タスク | 説明 | チェーン |
|--------|------|----------|
| FEATURE/S | 小規模機能 | Builder → Radar |
| FEATURE/M | 中規模機能 | Sherpa → Forge → Builder → Radar |
| FEATURE/L | 大規模機能 | Spark → Sherpa → Forge → Builder → Radar → Quill |
| FEATURE/frontend | フロントエンド機能 | Sherpa → Forge → Artisan → Radar |
| FEATURE/fullstack | フルスタック機能 | Sherpa → Forge → Artisan → Builder → Radar |
| FEATURE/api | API開発 | Gateway → Builder → Radar |

#### UI/UX

| タスク | 説明 | チェーン |
|--------|------|----------|
| UI/new | 新規UI実装 | Vision → Forge → Vitrine → Muse → Artisan → Radar |
| UI/redesign | UIリデザイン | Vision → Muse → Palette → Flow → Artisan → Radar |
| UI/component | コンポーネント作成 | Forge → Vitrine → Muse → Artisan → Radar |
| UI/animation | アニメーション追加 | Flow → Artisan → Radar |
| UX/research | UXリサーチ | Field → Echo → Palette |
| UX/improve | UX改善 | Echo → Palette → Artisan → Radar |
| UX/session-analysis | セッション分析 | Trace → Echo → Palette |
| UX/persona-validation | ペルソナ検証 | Field → Trace → Echo |

#### リファクタリング

| タスク | 説明 | チェーン |
|--------|------|----------|
| REFACTOR/small | 小規模リファクタ | Zen → Radar |
| REFACTOR/arch | アーキテクチャ改善 | Atlas → Sherpa → Zen → Radar |
| REFACTOR/legacy | レガシー刷新 | Shift (detect) → Sherpa → Zen → Radar |

#### パフォーマンス

| タスク | 説明 | チェーン |
|--------|------|----------|
| PERF/frontend | フロントエンド最適化 | Bolt → Artisan → Radar |
| PERF/backend | バックエンド最適化 | Bolt → Builder → Radar |
| PERF/db | データベース最適化 | Tuner → Schema → Builder → Radar |

#### AI/ML

| タスク | 説明 | チェーン |
|--------|------|----------|
| AI/rag | RAGパイプライン設計 | Oracle → Stream → Builder → Radar |
| AI/llm-app | LLMアプリケーション設計 | Oracle → Builder → Radar |
| AI/safety | AI安全性レビュー | Oracle → Sentinel → Oracle |
| AI/prompt-ops | プロンプトエンジニアリング＆評価 | Oracle → Radar |
| AI/prompt-spec | 曖昧なプロンプトを実行仕様へ変換 | Chisel |

#### 可観測性/SRE

| タスク | 説明 | チェーン |
|--------|------|----------|
| SRE/slo | SLO定義＆監視 | Beacon → Gear → Builder |
| SRE/observability | 完全可観測性セットアップ | Beacon → Gear → Builder → Radar |

#### セキュリティ

| タスク | 説明 | チェーン |
|--------|------|----------|
| SECURITY/audit | 静的解析 | Sentinel → Builder → Radar |
| SECURITY/pentest | 動的テスト | Probe → Builder → Radar → Probe |
| SECURITY/full | 完全監査 | Sentinel → Probe → Builder → Radar → Sentinel |

#### テスト

| タスク | 説明 | チェーン |
|--------|------|----------|
| TEST/unit | ユニットテスト追加 | Radar |
| TEST/e2e | E2Eテスト追加 | Voyager |
| TEST/coverage | カバレッジ向上 | Radar → Voyager |
| TEST/load | 負荷テスト | Siege → Bolt |
| TEST/chaos | カオスエンジニアリング | Siege → Triage → Builder |
| TEST/contract | 契約テスト | Gateway → Siege → Radar |
| TEST/mutation | ミューテーションテスト | Siege → Radar |

#### レビュー

| タスク | 説明 | チェーン |
|--------|------|----------|
| REVIEW/pr | PRレビュー | Judge → Zen/Builder/Sentinel |
| REVIEW/security | セキュリティレビュー | Judge → Sentinel |

#### Git/PR

| タスク | 説明 | チェーン |
|--------|------|----------|
| GIT/pr-prep | PR準備 | Guardian → Judge |
| GIT/commit-split | コミット分割 | Guardian |
| GIT/pr-full | 実装→PR→レビュー | Builder → Guardian → Judge → Zen |
| GIT/release | リリースノート生成 | Guardian |

#### 意思決定

| タスク | 説明 | チェーン |
|--------|------|----------|
| DECISION/arch | アーキテクチャ選定 | Magi → Builder/Zen |
| DECISION/strategy | 戦略的判断 | Magi → Spark |
| DECISION/office-hours | 創業者向けオフィスアワー相談 | Magi → Builder/Echo[demand]/Sherpa |
| DECISION/retro | 直近の意思決定・結果の振り返り | Magi |

#### 分析

| タスク | 説明 | チェーン |
|--------|------|----------|
| ANALYSIS/impact | 変更影響分析 | Ripple → Builder → Radar |
| ANALYSIS/standards | 標準準拠確認 | Canon → Builder → Radar |
| ANALYSIS/cleanup | コードクリーンアップ | Sweep → Zen → Radar |

#### 引き算・文化

| タスク | 説明 | チェーン |
|--------|------|----------|
| SUBTRACT/feature-gate | 機能提案の引き算ゲート | Spark → Void → Magi |
| SUBTRACT/scope-check | スコープ検証 | Sherpa → Void → Sherpa |
| SUBTRACT/arch-simplify | アーキテクチャ過剰設計検出 | Atlas → Void → Zen |

#### ドキュメント

| タスク | 説明 | チェーン |
|--------|------|----------|
| DOCS/prd | PRD作成 | Scribe |
| DOCS/srs | SRS作成 | Scribe |
| DOCS/design | 設計書作成 | Scribe |
| DOCS/spec-to-build | 仕様から実装 | Spark → Scribe → Sherpa → Builder |
| DOCS/code | コードドキュメント | Quill |
| DOCS/component | コンポーネント文書化 | Vitrine → Quill |
| DOCS/architecture | アーキテクチャ図 | Canvas |
| DOCS/convert | フォーマット変換 | Scribe |
| DOCS/report | PR報告書 | Launch → Scribe |
| DOCS/learning | 変更ベース学習資料 | Tome |
| DOCS/onboarding | オンボーディング教材 | Trail → Tome |

#### デモ・録画

| タスク | 説明 | チェーン |
|--------|------|----------|
| DEMO/prototype | プロトタイプのデモ | Forge → Cue → Growth |

#### インフラ・DevOps

| タスク | 説明 | チェーン |
|--------|------|----------|
| INFRA/ci | CI/CD構築 | Gear → Radar |
| INFRA/cloud | クラウド構築 | Scaffold → Gear |
| INFRA/cli | CLI開発 | Builder → Radar |

#### デプロイ・リリース

| タスク | 説明 | チェーン |
|--------|------|----------|
| DEPLOY/release | リリース実行 | Guardian → Launch |
| DEPLOY/full | 完全パイプライン | Radar → Guardian → Launch |

#### モダナイゼーション

| タスク | 説明 | チェーン |
|--------|------|----------|
| MODERNIZE/stack | 技術スタック刷新 | Lens → Shift (detect+modernize) → Sherpa → Builder → Radar |
| MODERNIZE/i18n | 国際化対応 | Polyglot → Artisan → Radar |
| MODERNIZE/structure | リポジトリ構造改善 | Grove → Sherpa → Zen → Radar |

#### 戦略・グロース

| タスク | 説明 | チェーン |
|--------|------|----------|
| STRATEGY/seo | SEO改善 | Growth → Artisan → Radar |
| STRATEGY/compete | 競合分析→実装 | Compete → Spark → Builder → Radar |
| STRATEGY/feedback | フィードバック反映 | Voice → Spark → Builder → Radar |
| STRATEGY/metrics | メトリクス基盤 | Pulse → Builder → Radar |
| STRATEGY/retention | リテンション施策 | Growth → Spark → Builder → Radar |
| STRATEGY/ab-test | A/Bテスト設計 | Experiment → Builder → Radar |
| STRATEGY/data | データパイプライン | Stream → Schema → Builder → Radar |

#### 並列実行（Rally統合）

大規模タスクで並列実行が有効な場合、NexusはRallyにエスカレーションします。

| タスク | 説明 | 並列チェーン |
|--------|------|-------------|
| FEATURE/L (並列) | 大規模フルスタック | Sherpa → Rally(Artisan + Builder + Radar) |
| FEATURE/fullstack (並列) | フロントエンド＋バックエンド | Rally(Artisan, Builder, Radar) |
| FEATURE/multi (並列) | 複数独立機能 | Sherpa → Rally(Builder×N, Radar) |
| BUG/multiple (並列) | 複数独立バグ修正 | Rally(Builder×N) → Radar |
| REFACTOR/arch (並列) | 複数モジュールリファクタ | Atlas → Sherpa → Rally(Zen×N) → Radar |
| SECURITY/full (並列) | 静的＋動的並行スキャン | Rally(Sentinel, Probe) → Builder → Radar |
| TEST/coverage (並列) | Unit＋E2E並行テスト | Rally(Radar, Voyager) |
| MODERNIZE/stack (並列) | マルチエリア刷新 | Shift (detect+modernize) → Sherpa → Rally(Builder×N) → Radar |
| DOCS/full (並列) | コード文書＋図＋ストーリー | Rally(Quill, Canvas, Vitrine) |

> **Rallyエスカレーション基準**: 2つ以上の独立した実装ステップ、4ファイル以上で2ドメイン以上にまたがる場合、またはSherpaが`parallel_group`を検出した場合にRallyが起動されます。

> **Nexus並列 vs Rally**: Nexus内蔵の`_PARALLEL_BRANCHES`は軽量な並列（各ブランチ50行未満）向け。本格的な実装作業にはRallyのマルチセッション並列が使用されます。

#### プロダクトライフサイクル（Nexus[deliver]）

| タスク | 説明 | チェーン |
|--------|------|----------|
| PROJECT/full | 曖昧なゴールからプロダクト完成 | `Nexus deliver`（スコープ適応型ライフサイクル） |
| PROJECT/mvp | MVP重視のデリバリー | `Nexus deliver`（最小限の専門チェーン） |

> **Nexus のビルドモード**: `feature` は単一機能、`deliver` は規模に応じた製品/MVP、`apex` は高投資の discovery-to-ship を担当します。

#### その他

| タスク | 説明 | チェーン |
|--------|------|----------|
| INCIDENT | 障害対応 | Triage → Scout → Builder |
| TEST/quality | 品質反復改善 | Judge → Zen → Radar |
| INVESTIGATE/regression | リグレッション調査 | Trail → Scout → Builder → Radar |

#### メッセージング・リアルタイム

| タスク | 説明 | チェーン |
|--------|------|----------|
| MESSAGING/bot | Bot開発 | Gateway → Builder → Radar |
| MESSAGING/webhook | Webhookハンドラ | Gateway → Builder → Radar |
| MESSAGING/realtime | リアルタイム通信 | Gateway → Scaffold → Builder → Radar |
| MESSAGING/multi-channel | マルチチャネル統合 | Gateway → Builder → Radar |

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
agent-skills/
├── <skill>/                # グローバルスキルごとに1ディレクトリ（エージェント一覧を参照）
│   ├── SKILL.md            # エントリポイント：frontmatter、境界、レシピ
│   └── reference/          # 必要時に読み込む参照資料（任意）
├── .claude/skills/         # project-localスキル：darwin、lore、orbit（正本）
├── .agents/skills/         # .claude/skills/ の同期ミラー
├── _common/                # 共通プロトコル（BOUNDARIES.md、HANDOFF.md など）
│   └── scripts/            # `make validate` / `make test` の検査スクリプト
├── _templates/             # SKILL_TEMPLATE.md、PROJECT.md、キット
└── Makefile                # link / unlink / status / validate / test / check / hooks
```

## 使用例

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

**実行チェーン**: Spark（仕様策定）→ Sherpa（タスク分解）→ Forge（プロトタイプ）→ Builder（本番実装）→ Radar（テスト）→ Quill（ドキュメント）

---

#### バグ修正（複雑なケース）

```
/Nexus
本番環境でのみ発生する決済エラーを調査・修正してください。
ローカルでは再現しません。

## NEXUS_AUTORUN
```

**実行チェーン**: Scout（調査）→ Sherpa（タスク分解）→ Builder（修正）→ Radar（回帰テスト）→ Sentinel（セキュリティ確認）

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

**実行チェーン**: Spark（仕様）→ Forge（UI プロトタイプ）→ Muse（デザイン調整）→ Builder（実装）→ Radar（テスト）

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
- Chain: **Spark** → **Sherpa** → **Builder** → **Radar**
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
- Chain: **Spark** → **Sherpa** → **Builder** → **Radar**
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
*(Builder を呼び出しますか？)*

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

1. リポジトリ直下に `<skill-name>/SKILL.md` を作成（小文字 kebab-case）
2. frontmatter に `name` と `description` を定義
3. 境界（Always do / Ask first / Never do）を明記
4. AUTORUN SupportとNexus Hub Modeのセクションを追加

### エージェントの修正

[_templates/SKILL_TEMPLATE.md](_templates/SKILL_TEMPLATE.md) に従って各 `SKILL.md` を直接編集します。frontmatter の例：

```markdown
---
name: skill-name
description: One-line English description of the skill and its primary use case.
---

[エージェントの詳細な指示]
```

## ライセンス

MIT
