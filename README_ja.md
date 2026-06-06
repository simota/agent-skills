# AI Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agents](https://img.shields.io/badge/Agents-135-blue.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

🤖 135種類の専門AIエージェントチームによる協調開発を実現するスキルコレクション

## ✨ Features

- **135種類の専門エージェント** - バグ調査、テスト、セキュリティ、UI/UX、AI/ML、可観測性、インフラまで網羅
- **Nexusオーケストレーター** - タスクを分析し最適なエージェントチェーンを自動設計
- **プラットフォーム非依存** - Claude Code、Codex CLI、Antigravity CLI等で動作

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

このリポジトリには、ソフトウェア開発の様々な側面を専門とする135種類のAIエージェントが含まれています。各エージェントは特定のドメインに特化しており、**Nexus**オーケストレーターによって統括・連携されます。

## エージェント一覧

> 全 125 エージェントのカテゴリ別カタログ。

### オーケストレーション

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Nexus** | _"The right agent at the right time changes everything."_ - チーム統括オーケストレーター。要求を分解し、最適なエージェントチェーンを設計 | プロンプト、進行管理 |
| **Sherpa** | _"The mountain doesn't care about your deadline. Plan accordingly."_ - タスク分解ガイド。複雑なタスクを15分以内のAtomic Stepに分解 | チェックリスト |
| **Architect** | _"Every agent is a possibility. Every SKILL.md is a birth certificate."_ - 新しいスキルエージェントを設計・生成するメタデザイナー。エコシステムギャップ分析、重複検出、SKILL.md生成 | SKILL.md、references |
| **Rally** | _"One task, many hands. Parallel by design."_ - マルチセッション並列オーケストレーター。Claude Code Agent Teams APIで複数Claudeインスタンスを生成・管理し、並行タスク実行を実現 | チーム管理、並列実行 |
| **Titan** | _"Give me a dream. I'll give you the product."_ - プロダクトライフサイクル統括メタオーケストレーター。曖昧なゴールから全105エージェントを9フェーズ（DISCOVER→BUILD→LAUNCH→EVOLVE）で指揮し、プロダクトを完走まで導く | プロダクトデリバリー |
| **Sigil** | _"Every project has patterns waiting to become power."_ - 動的スキル生成エージェント。プロジェクトのコードベースを分析し、パターン・規約を発見し、最適化されたClaude Codeスキルをプロジェクトの`.claude/skills/`に生成 | プロジェクト固有スキル |
| **Gauge** | _"What gets measured gets managed. What gets audited gets normalized."_ - SKILL.md正規化監査・自己進化エージェント。16項目チェックリストに基づくコンプライアンススキャン、修正提案、Webベースのベストプラクティス自動取得 | コンプライアンスレポート、修正プラン |
| **Orbit** | _"Give me a goal. I'll give you a runner that finishes."_ - Nexus-autoloop完走スペシャリスト。自律ループの完走スクリプト生成・運用契約設計・監査を担当。ゴールを渡せば完走できるランナー一式を生成 | ランナースクリプト、契約 |
| **Darwin** | _"Ecosystems that cannot sense themselves cannot evolve themselves."_ - エコシステム自己進化オーケストレーター。プロジェクトライフサイクルを検出し、エージェントの関連性を評価し、横断的知識を統合してエコシステム全体を進化させる | エコシステムフィットネススコア、進化提案 |
| **Lore** | _"Forgotten lessons are lessons repeated. Institutional memory is the compound interest of experience."_ - エコシステム横断の知識統合・パターン抽出・伝播を担うメモリキュレーター。エージェントjournalから共通パターンを発見し、カタログ化して関連エージェントへ配信。知識の腐敗検出・ベストプラクティス伝播により制度的記憶を維持 | METAPATTERNS.md、知識インサイト |
| **Atelier** | _"Design decided upstream. Assets produced downstream. atelier is the studio floor in between."_ - デザインから実装までを閉ループで繋ぐパイプラインオーケストレーター。Vision → Muse/Frame → Forge → Artisan → Vitrine → Canvas を統括し、デザイン抽出・プロトタイプ・ビジュアルアセット・スライド・本番実装をプロジェクトデザインシステムを永続化しながら一気通貫で提供 | デザインシステムパッケージ、統合成果物 |
| **Bazaar** | _"A landing page is one promise, one path, one decision. bazaar runs the studio that delivers all three."_ - 超高品質LP制作スタジオチェーン・オーケストレーター。Field → Cast → Pulse → Funnel → Vision → Saga → Compete → Muse → Flow → Artisan → Growth → Bolt → Judge → Launch を、LP種別レシピと9段階の品質ゲート（Discover → Audience → Strategy → Structure → Design → Build → Optimize → Verify → Launch）で束ね、6つのクラフト軸（デザイン／アニメーション／ブランディング／マーケティング／SEO／IA）すべてにルーブリックと納品閾値を課したLPを納品 | 6軸ルーブリック通過済みLPパッケージ、CVR最適化された本番コード、ブランド整合性のあるビジュアル、トークン化されたモーション、スキーマ妥当性のあるSEO、AI検索引用対応GEO、計測稼働 |
| **Compass** | _"When in doubt, ask Compass. It finds the right skill for you among 130+."_ - スキルエコシステムのナビゲーター・オンボーディングガイド。エージェントを一覧化し、タスクに最適な担当を推薦し、初心者が適切なスペシャリストを発見できるよう支援 | レコメンド、エージェントマップ |

### 調査・企画（コードを書かない）

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Scout** | _"Every bug has a story. I read the ending first."_ - バグ調査・根本原因分析（RCA）。再現手順と修正箇所を特定 | 調査レポート |
| **Ripple** | _"Every change sends ripples. Know where they land before you leap."_ - 変更前の影響分析。縦（依存関係・影響ファイル）と横（パターン一貫性・命名規則）の両面からリスク評価 | 影響分析レポート |
| **Spark** | _"The best feature is the one users didn't know they needed."_ - 新機能提案。既存データ/ロジックを活用した機能をMarkdownで提案 | 仕様書 |
| **Dawn** | _"One idea a day. Something that makes you smile when it runs, something you'll want to talk about tomorrow."_ - 個人サイドプロジェクトのアイデア提案エージェント。1呼び出しあたり1-3日でMVPが完成する1つのアイデアを提案。CLI・自動化・LLM・DX・生産性・データ可視化の角度をカバーし、コーディングエージェントへすぐ貼れるプロンプトも同梱 | サイドプロジェクトブリーフ |
| **Compete** | _"Know your enemy. Know the market. Know yourself."_ - 競合調査・差別化ポイント特定・ポジショニング。SWOT分析、機能マトリクス | 競合分析レポート |
| **Voice** | _"Feedback is a gift. Analysis is unwrapping it."_ - ユーザーフィードバック収集・NPS調査設計・感情分析・インサイト抽出 | フィードバックレポート |
| **Plea** | _"I am your user. I feel every day what you overlook."_ - 合成ユーザー代弁者。多様なエンドユーザーペルソナになりきり、本物のような機能要望を生成し、未充足ニーズを発掘し、チームの思い込みに挑戦する | 機能要望レポート |
| **Field** | _"Users don't lie. They just don't know what they want yet."_ - ユーザーリサーチ設計・インタビューガイド作成・定性分析・ペルソナ/ジャーニーマップ作成 | リサーチレポート |
| **Trace** | _"Every click tells a story. I read between the actions."_ - セッションリプレイ分析・ペルソナ別行動パターン抽出・UX問題の物語化。Field/Echoと連携 | 行動分析レポート |
| **Canon** | _"Standards are the accumulated wisdom of the industry. Apply them, don't reinvent them."_ - 世界標準・業界標準で物事を解決する調査・分析エージェント。OWASP/WCAG/OpenAPI/ISO 25010等の標準への準拠度評価、標準違反検出、改善提案 | 準拠度レポート |
| **Lens** | _"See the code, not just search it."_ - コードベース理解・調査スペシャリスト。「〇〇機能はあるか」「〇〇のフローはどうか」「このモジュールの責務は何か」をコード構造把握・機能探索・データフロー追跡で体系的に調査 | 調査レポート |
| **Magi** | _"Three minds, one verdict. Consensus through diversity."_ - 3視点（論理・共感・実利）による多角的意思決定。アーキテクチャ選定、トレードオフ判断、Go/No-Go判定 | 意思決定レポート |
| **Flux** | _"Bend the light. See what was always there."_ - 思考屈折エンジン。前提を疑い、異分野知識を組み合わせ、視点をずらして問題を再構成。Cynefinベースのフレームワーク選択、Serendipity Injection、10+思考フレームワーク。コードは書かない | リフレーミングパッケージ、Insight Matrix、Blind Spot Report |
| **Riff** | _"The best ideas don't arrive. They evolve — one riff at a time."_ - 4つの思考モード（拡散/提案/評価/引き算）による反復対話でアイデアを深めるインタラクティブなブレインストーミングパートナー。コードは書かない | ブレインストーミングセッション出力 |
| **Cast** | _"Personas are not invented. They are discovered, born, and evolved."_ - ペルソナキャスティングエージェント。多種多様な入力からペルソナを迅速生成・永続化・ライフサイクル管理し、下流エージェントに統一フォーマットで配信 | ペルソナレジストリ |
| **Helm** | _"A ship without a destination has no favorable wind. A ship without a helm has no direction at all."_ - 財務・市場・競合データから短期/中期/長期の経営シミュレーションを実施する経営戦略特化エージェント。SWOT/PESTLE/Porter分析、シナリオプランニング、KPI予測、戦略ロードマップ生成。コードは書かない | 戦略シミュレーションレポート |
| **Levy** | _"納税は義務。でも、正しく知れば、賢く果たせる。"_ - 日本の確定申告ガイダンスエージェント。所得分類・控除最適化・税額計算・e-Tax手続きをフリーランス/副業向けに解説。コードは書かない | 確定申告ガイダンスレポート |
| **Accord** | _"Three teams, one truth."_ - 3チーム横断（ビジネス・開発・デザイン）の統合仕様パッケージを作成する仕様アーキテクト。段階的詳細化テンプレート（L0ビジョン→L1要件→L2チーム別詳細→L3受入基準）で共通認識を形成。コードは書かない | 統合仕様パッケージ、トレーサビリティマトリクス |
| **Matrix** | _"Infinite combinations, finite resources. Matrix finds the minimum that covers the maximum."_ - 任意の多次元軸×値を入力とし、組み合わせ爆発を制御するユニバーサル分析エージェント。最小カバレッジセット選定・実行計画・優先順位付け。テスト・デプロイ・UX検証・リスク評価・互換性など全ドメイン対応。コードは書かない | マトリクス分析、カバレッジ最適化計画 |
| **Saga** | _"Features don't sell. Stories do."_ - プロダクト・機能のユースケースをストーリーテリングで語るナラティブデザインエージェント。顧客体験の物語化、シナリオストーリー、プロダクトナラティブ。コードは書かない | ナラティブドキュメント |
| **Fossil** | _"The past writes the rules. I dig them up."_ - レガシーコード考古学。ドキュメントのないコードから暗黙的なビジネスルールを抽出し、マイグレーションリスクを評価 | 調査レポート |
| **Omen** | _"Plan for the worst. Build for the best."_ - プリモーテム分析・障害モード列挙。計画・設計・機能のリスクシナリオをRPN/APスコアリングで体系的に特定。コードは書かない | プリモーテムレポート |
| **Rank** | _"Every priority tells a story of trade-offs."_ - 優先度定量化エージェント。ICE/RICE/WSJF/MoSCoW/Kanoフレームワークで競合アイテムをスコアリング・順序付け。コードは書かない | 優先度レポート |
| **Sage** | _"Tell me what you're avoiding."_ - YC のオフィスアワー流アドバイザリーエージェント。ソクラテス式問答で「いま最も自分を止めているボトルネック」を1つに絞り込み、過去の数百スタートアップから引いたパターンで率直に診断し、1-2週間で実行する具体アクションに落とす。創業者アンチパターン検出付き。コードは書かない | オフィスアワー出力 (ボトルネック + アクション) |

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
| **Harvest** | _"Code writes history. I harvest its meaning."_ - PR情報収集・レポート生成。ghコマンドでPR情報を取得し、週報・月報・リリースノートを自動生成 | 作業報告書、リリースノート |
| **Launch** | _"Shipping is not the end. It's the beginning of accountability."_ - リリース管理。バージョニング戦略、CHANGELOG生成、リリースノート作成、ロールバック計画、Feature Flag設計 | リリース計画、CHANGELOG |
| **Trail** | _"Every bug has a birthday. Every regression has a parent commit. Find them."_ - Git履歴調査・リグレッション原因分析・コード考古学。時間を遡って真相を解明 | 履歴調査レポート |
**Guardian → Judge → Zen の連携**：Guardian（PR準備）→ Judge（レビュー）→ Zen（修正）
**Guardian → Launch の連携**：Guardian（変更分析）→ Launch（リリース計画）
**Trail → Scout の連携**：Trail（リグレッション特定）→ Scout（詳細調査）

### 品質保証

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Radar** | _"Untested code is unfinished code."_ - ユニット/統合テスト追加・フレーキーテスト修正・カバレッジ向上 | テストコード |
| **Voyager** | _"E2E tests are the user's advocate in CI/CD."_ - E2Eテスト専門。Playwright/Cypress設定、Page Object設計、視覚回帰、CI統合 | E2Eテストコード |
| **Sentinel** | _"Security is not a feature. It's a responsibility."_ - セキュリティ静的分析（SAST）・脆弱性パターン検出・入力検証追加 | セキュリティ修正 |
| **Probe** | _"A system is only as secure as its weakest endpoint."_ - セキュリティ動的テスト（DAST）・OWASP ZAP/Nuclei連携・ペネトレーションテスト | 脆弱性レポート |
| **Judge** | _"Good code needs no defense. Bad code has no excuse."_ - codex reviewによるコードレビュー・PRレビュー自動化・コミット前チェック・AI幻覚検出 | レビューレポート |
| **Zen** | _"Clean code is not written. It's rewritten."_ - リファクタリング・コード品質改善（動作は変えない） | コード改善 |
| **Sweep** | _"Dead code is technical debt that earns no interest."_ - 不要ファイル検出・未使用コード特定・孤立ファイル発見・安全な削除提案 | クリーンアップ提案 |
| **Warden** | _"Quality is not negotiable. Ship nothing unworthy."_ - V.A.I.R.E.品質基準の番人。リリース前評価、スコアカード、合否判定 | 品質評価レポート |
| **Attest** | _"Specs are truth. Code is evidence. Attest finds the gaps."_ - 仕様適合検証エージェント。仕様書から受入基準を抽出し、BDDシナリオを生成し、実装が仕様通りか敵対的に検証。CERTIFIED/CONDITIONAL/REJECTED判定を発行 | 適合レポート、BDDシナリオ |
| **Specter** | _"The bugs you can't see are the ones that haunt you."_ - 並行性・非同期処理・リソース管理の「見えない」問題を狩る幽霊ハンター。Race Condition、Memory Leak、Resource Leak、Deadlockを検出・分析・レポート | 検出レポート |
| **Siege** | _"Break it before users do. Fix it before they notice."_ - 高度テストスペシャリスト。負荷テスト（k6/Locust/Artillery）、契約テスト（Pact CDC）、カオスエンジニアリング、ミューテーションテスト、レジリエンスパターン検証 | テスト結果、レジリエンスレポート |
| **Void** | _"The best code is the code that was never written."_ - YAGNI検証・スコープカット・機能プルーニング・複雑性削減提案。5つの存在検証問とCost-of-Keeping Scoreで不要な複雑性を特定 | 削減提案 |
| **Vigil** | _"Detection is the first line of defense. Engineering is the last."_ - Detection Engineeringエージェント。Sigma/YARAルール設計、検出カバレッジマッピング、脅威ハンティング仮説設計、Detection-as-Code CI/CD統合 | 検出ルール、カバレッジマップ |
| **Cull** | _"The worm leaves a husk. Find it before it sheds again."_ - サプライチェーンマルウェア感染スキャナ。npm/PyPI ワーム型攻撃（Mini Shai-Hulud、S1ngularity、lottie-player）を IoC ベースでローカル環境スキャン。OS 永続化（LaunchAgent/systemd）、IDE フック実装、lockfile pin、既知 C2/exfil トレースを検出。`rm -rf ~/` リテリエーションを発動させないよう永続化先停止、ローテーションは除染検証後に gate | 感染レポート、除染ランブック |
| **Vista** | _"Tests you can't see, you don't trust. Tests you trust, you ship."_ - テスト知見の可視化スペシャリスト。junit.xml/lcov/allure/playwright/CTRF/OTelからカバレッジヒートマップ、トレーサビリティマトリクス、Test-Shape（Pyramid/Trophy/Honeycomb/Diamond/Cupcake/Hourglass/Ice-Cream-Cone）、フレーキーテストダッシュボード（Wilson下限）、ミューテーション重畳カバレッジ、AI起点テストリスクレンズ、リグレッションタイムライン（E-Divisive変化点）を生成。Markdown + HTML 二重出力 | カバレッジヒートマップ、Test-Shape、フレーキーダッシュボード |
| **Mint** | _"Good tests deserve great data."_ - テストデータ＆フィクスチャ生成エージェント。ファクトリパターン設計、境界値データ生成、合成データ生成、シードデータ管理 | コード |
| **Oath** | _"Trust is earned. Compliance is proven."_ - 規制コンプライアンス＆監査エージェント。SOC2/PCI-DSS/HIPAA/ISO 27001のコントロールマッピング、監査証跡設計、Policy as Code | レポート、チェックリスト |
| **Breach** | _"Think like an attacker. Defend like an engineer."_ - レッドチームエンジニアリング。攻撃シナリオ設計、脅威モデリング、MITRE ATT&CK/OWASPフレームワーク、Purple Team演習、AI/LLMレッドチーミング | セキュリティ評価 |
| **Cloak** | _"Privacy is not a feature. It's a right."_ - プライバシーエンジニアリング・データガバナンス。PII検出、データフローマッピング、同意管理、GDPR/CCPA準拠コード実装 | プライバシー評価 |

### 実装

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Builder** | _"Types are contracts. Code is a promise."_ - 本番実装。TDD・Event Sourcing・CQRS・パフォーマンス最適化を備えた型安全な実装職人。仕様の曖昧性検出、Forgeからの自動引き継ぎ対応 | プロダクションコード |
| **Artisan** | _"Prototypes promise. Production delivers."_ - フロントエンド本番実装の職人。React/Vue/Svelte、Hooks設計、状態管理、Server Components、フォーム処理、データフェッチング | フロントエンドコード |
| **Forge** | _"Done is better than perfect. Ship it, learn, iterate."_ - プロトタイプ作成。完璧より動くものを優先。Builder連携用にtypes.ts, errors.ts, forge-insights.mdを出力 | MVP/PoC |
| **Arena** | _"Arena is the judge, not a player. External engines compete; the best solution wins."_ - codex exec / Antigravity CLI を直接操り並列実装・評価・採用。Solo Mode（逐次）と Team Mode（Agent Teams 並列）をサポート | 比較実装・評価 |
| **Native** | _"Every pixel ships. Every platform matters."_ - Pure-nativeモバイル実装スペシャリスト。iOS（Swift 6.3 + SwiftUI + Liquid Glass）と Android（Kotlin 2.4+ + Jetpack Compose + Material 3 Expressive）。@Observable/Swift Concurrency、Compose Strong Skipping + Type-safe Navigation、SwiftData/Room、Credential Manager + Passkey、Privacy Manifest、edge-to-edge、predictive back、Live Activities、App Intents、Foundation Models / Gemini Nano、ストア準拠、ステージドロールアウト。React Native / Flutter / KMP / CMP は対象外 | コード |
| **Pixel** | _"Every pixel matters. Fidelity is non-negotiable."_ - 画像モックアップ（PNG/JPG/スクリーンショット）からピクセルパーフェクトなHTML/CSSを生成し、視覚的検証を行う忠実再現エージェント | HTML/CSSコード |

### AI/ML

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Oracle** | _"AI is only as good as its architecture. Design it, measure it, trust nothing."_ - AI/ML設計・評価スペシャリスト。プロンプトエンジニアリング、RAGアーキテクチャ、LLMアプリケーションパターン、安全ガードレール、評価フレームワーク、MLOps、コスト最適化 | 設計仕様、評価レポート |

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
| **Echo** | _"I don't test interfaces. I feel what users feel."_ - ペルソナ検証。ユーザーになりきりUIフローの混乱ポイントを報告 | UXレポート |
| **Vitrine** | _"Components without stories are components without context."_ - Storybookストーリー作成・カタログ管理・Visual Regression連携。CSF 3.0形式 | Storybook Stories |
| **Prose** | _"Words are the smallest unit of design. Get them wrong, and nothing else matters."_ - ユーザー向けテキストの専門エージェント。マイクロコピー、エラーメッセージ、ボイス＆トーンフレームワーク、オンボーディングコピー、アクセシビリティテキスト | コピーガイドライン、コンテンツ仕様 |
| **Frame** | _"Design speaks in pixels. I translate it to code."_ - Figma MCP Serverを活用してデザインコンテキストを抽出・構造化し、実装エージェントに渡すブリッジエージェント。デザインからコードへの橋渡し、Code Connect管理、デザインシステムルール抽出。コードは書かない | 構造化デザインコンテキスト、デザインシステムルール |
| **Loom** | _"Design intent deserves preparation. Every thread of context I weave makes creation more precise."_ - Figma Make最適化エージェント。コードベースを分析してGuidelines.mdを生成し、プロンプト戦略を設計し、Make出力をデザインシステム規約と照合検証。コードは書かない | Guidelines.md、プロンプトシーケンス、検証レポート |
| **Ink** | _"Every stroke serves a purpose."_ - SVGアイコン/イラスト生成、アイコンシステム設計、スプライトシンボル構築 | SVGアセット |

**Frame vs Loom の役割分担**:
- **Frame**: Figma → Code 方向（Figma MCP経由でデザインコンテキストを抽出）
- **Loom**: Code → Figma Make 方向（コードベース分析からFigma Makeへの最適入力を準備）

### ドキュメント

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Scribe** | _"A specification is a contract between vision and reality."_ - PRD/SRS/HLD/LLD・実装チェックリスト・テスト仕様書を作成するドキュメントライター | 仕様書・設計書 |
| **Quill** | _"Code tells computers what to do. Documentation tells humans why."_ - JSDoc/TSDoc追加・README更新・any型の型定義化 | ドキュメント |
| **Morph** | _"A document is timeless. Its format is temporary."_ - ドキュメントフォーマット変換（Markdown↔Word/Excel/PDF/HTML）。Scribeの仕様書やHarvestのレポートを各種フォーマットに変換 | 変換済みドキュメント |
| **Prism** | _"One source, many lights."_ - NotebookLMのステアリングプロンプト設計コンサルタント。ソース準備の助言と最適な出力フォーマット（Audio/Video/Slide/Infographic/Mind Map）の選定 | ステアリングプロンプト |
| **Tome** | _"Changes are forgotten. Knowledge endures."_ - リポジトリの変更内容を詳細な学習ドキュメントに変換。用語・フロー・設計判断・アンチパターンを教育的に解説 | 学習ドキュメント |
| **Clause** | _"Every clause carries weight. Every omission carries risk."_ - 利用規約・プライバシーポリシー・特商法の法的ドキュメントレビュー。条項ギャップ検出・リスクフラグ・規制整合性確認 | 法務レビューレポート |
| **Zine** | _"The hook earns the second paragraph."_ - 外部公開向けテックブログ・記事連載オーサリングエージェント。note/Zenn/Qiita/dev.to向けフック設計、記事構造、プラットフォーム別チューニング、連載管理 | 公開記事、連載index |

**Scribe vs Quill vs Morph vs Prism vs Tome vs Zine の役割分担**:
- **Scribe**: プロジェクトドキュメント（PRD、SRS、設計書、チェックリスト、テスト仕様書）
- **Quill**: コードドキュメント（JSDoc/TSDoc、README、型定義）
- **Morph**: フォーマット変換（Markdown→PDF/Word/HTML等）
- **Prism**: NotebookLMコンテンツ最適化（Audio/Video/Slide向けステアリングプロンプト）
- **Tome**: 変更ベース学習教材（diffから設計判断・用語・アンチパターンを教材化）
- **Zine**: 外部公開記事（note/Zenn/Qiita/dev.to）・連載管理

### 可視化

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Canvas** | _"A diagram is worth a thousand lines of documentation."_ - 設計可視化。コード・仕様・コンテキストをMermaid図またはASCIIアート（フローチャート、シーケンス図、状態遷移図、クラス図、ER図等）に変換 | Mermaid図 / ASCII Art |
| **Sketch** | _"From words to worlds, prompt to pixel."_ - AI画像生成コード職人。Gemini APIを使用した画像生成用Pythonコードの作成。プロンプトエンジニアリング、バッチ生成、コスト見積もり | Pythonコード |
| **Realm** | _"Every company tells a story — let the agents write theirs."_ - エージェントエコシステムをゲーミフィケーションで可視化するメタ可視化エージェント。Phaser 3による2Dオフィスシミュレーション、リアルタイムXP成長・ランクアップエフェクト、インタラクティブHTMLマップ、キャラクターシート、クエストボード、バッジシステム | RPGスタイルダッシュボード、ゲーム可視化 |
| **Dot** | _"Every pixel is a decision. Every constraint is a creative opportunity."_ - ピクセルアート専門エージェント。コード（SVG/Canvas/Phaser 3/Pillow/CSS）でドット絵を生成。パレット設計、スプライトシート、タイルセット、フレームアニメーション、Antigravity CLIへのSVG生成委譲をサポート | ピクセルアートコード（SVG/Canvas/CSS） |
| **Quest** | _"Every great game starts with a question the player cannot resist answering."_ - ゲーム企画・プロダクションエージェント。GDD構造化、ゲームバランス数理、ナラティブ設計、経済設計、システムデザイン、プレイヤー心理学。コードは書かない | GDD、バランスシート、経済モデル |
| **Tone** | _"Sound is the invisible architecture of emotion."_ - ゲームオーディオ生成エージェント。ElevenLabs/Stable Audio/MusicGen/OpenAI TTS/JSFXR等によるSFX・BGM・Voice・Ambient・UIサウンド用コード生成。LUFS正規化、ミドルウェア統合 | オーディオパイプラインコード |
| **Clay** | _"From prompt to polygon, every vertex earns its place."_ - AI 3Dモデル生成エージェント。Meshy/Tripo/Hunyuan3D/Rodin/Sloyd/Stability APIを使用したtext-to-3D・image-to-3D用コード（Python/JS/OpenSCAD）を生成。ゲームパイプライン：LOD、リトポロジー、UV、テクスチャベイク、QC検証 | 3Dパイプラインコード（Python/JS/SCAD） |
| **Cue** | _"Every frame tells a story."_ - ビデオスクリプト・ストーリーボード・ナレーション設計。プロダクト動画、解説動画、オンボーディングコンテンツ企画 | 動画台本、ストーリーボード |
| **Stage** | _"Every slide is a stage."_ - Marp/reveal.js/Slidevによるスライド生成、ストーリー構成設計、カンファレンストーク最適化 | スライドデッキ |
| **Lyric** | _"From theme to anthem, verse by verse."_ - Suno AI向けソングライティングエージェント。テーマ・ジャンル・ムードからメタタグ付き歌詞を作成 | メタタグ付き歌詞 |

**Vision → Dot → Forge の連携**：Vision（アートディレクション）→ Dot（ピクセルアートコード）→ Forge（プロトタイプ統合）
**Dot → Realm の連携**：Dot（Phaser 3テクスチャ）→ Realm（エコシステム可視化）
**Vision → Clay → Builder の連携**：Vision（アートディレクション）→ Clay（3Dアセットコード）→ Builder（ゲームロジック統合）

### アーキテクチャ

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Atlas** | _"Dependencies are destiny. Map them before they map you."_ - 依存関係分析・循環参照検出・ADR/RFC作成 | 設計文書 |
| **Port** | _"From web to native. Translate the experience, not just the code."_ - WebアプリからiOS Swift / Android Kotlin pure-nativeへのポーティング設計スペシャリスト（2026仕様：Liquid Glass / Material 3 Expressive / Swift 6.3 / targetSdk 36 / Privacy Manifest / 5.1.2(i) AI開示対応）。機能パリティマトリクス、ネイティブアーキテクチャマップ、規制コンプライアンス計画、Strangler-Fig段階的ロードマップを生成。Pure-Native UI + KMP共有ロジックのハイブリッドパスも提案可 | ポーティング設計、パリティマトリクス、ロードマップ |
| **Gateway** | _"APIs are promises to the future. Design them like contracts."_ - API設計・レビュー・OpenAPI仕様生成・バージョニング戦略・破壊的変更検出 | API仕様書 |
| **Grove** | _"A well-structured repository is a well-structured mind."_ - リポジトリ構造の設計・最適化・監査。ディレクトリ設計、docs/構成、テスト構成、アンチパターン検出 | 構造設計・監査レポート |
| **Nest** | _"Structure what reaches the model, and the model structures the rest."_ - LLM最適化フォルダ構造設計。プロジェクトディレクトリをコンテキスト効率・プログレッシブディスクロージャー・プロンプトキャッシュ性能の観点で監査・再構成 | 構造レポート・レイアウト設計 |
| **Weave** | _"Every state tells a story. Every transition is a contract."_ - ワークフロー＆ステートマシン設計エージェント。状態遷移設計、不正遷移検出、Sagaパターン、承認フロー設計 | 設計、図 |
| **Seek** | _"The right result at the right time in the right order."_ - 検索エンジン・ベクトルDB設計エージェント。全文検索/ベクトル検索/ハイブリッド検索の設計・インデックス最適化・RAG Retrieval層実装 | コード、設定 |
| **Stratum** | _"Architecture without visualization is architecture without communication."_ - C4モデルに基づくソフトウェアアーキテクチャモデリング・評価・Structurizr DSL生成 | アーキテクチャ図、DSL |
| **Crypt** | _"Trust no channel. Verify every key."_ - 暗号アーキテクチャ設計。アルゴリズム選定、鍵管理、E2E暗号化、KMS統合、TLS設定 | 暗号設計仕様 |
| **Shard** | _"Isolation is the foundation of trust in multi-tenancy."_ - マルチテナントアーキテクチャ設計。テナント分離戦略、RLS、ルーティング、SaaS向けスケール設計 | アーキテクチャ設計 |
| **Trawl** | _"Design the web that catches the web."_ - クロールシステムアーキテクチャ設計。分散クローラー設計、URLフロンティア管理、ポライトネスポリシー、法的準拠設計 | アーキテクチャ仕様 |
| **Tempo** | _"Time is not a scalar — it's a minefield of conventions."_ - スケジューリング・時間ロジックアーキテクト。cron表現設計、タイムゾーン/DST処理、retry/backoffポリシー、idempotencyキー、backfill戦略、営業カレンダー設計（日本の祝日、会計年度、銀行営業日） | スケジュール仕様、cron設定、retryポリシー |
| **Grok** | _"Understand the shape before writing the parser."_ - パターン・regex・parser・DSL設計スペシャリスト。文法オーサリング（EBNF/PEG）、ReDoS-safe regex、parser-generator選定（ANTLR4/tree-sitter/Chevrotain）、内部DSLアーキテクチャ、AST変換 | 文法仕様、parser設計、DSL仕様 |

### コミュニケーション

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Relay** | _"Every message finds its way. Every channel speaks the same language."_ - メッセージング統合・Bot開発・リアルタイム通信の設計＋実装スペシャリスト。チャネルアダプター、Webhookハンドラ、WebSocketサーバー、イベント駆動アーキテクチャ | チャネルアダプター、メッセージハンドラ、Botフレームワーク |

**Relay → Builder → Radar の連携**：Relay（メッセージング設計）→ Builder（実装）→ Radar（テスト）
**Gateway → Relay の連携**：Gateway（Webhook API仕様）→ Relay（ハンドラ設計）

### データ

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Schema** | _"A schema is a contract with the future."_ - DBスキーマ設計・マイグレーション作成・ER図設計 | マイグレーション/スキーマ定義 |
| **Stream** | _"Data flows like water. My job is to build the pipes."_ - データパイプライン。ETL/ELT設計、Kafka/Airflow/dbt、バッチ/ストリーミング選定、データ品質管理 | パイプライン設計、DAG、dbtモデル |

**Schema → Stream の連携**：Schema（データモデル）→ Stream（パイプライン設計）

### DevOps

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Anvil** | _"The terminal is the first interface. Make it unforgettable."_ - Terminal UI構築・CLI開発支援・開発ツール統合（Linter/テストランナー/ビルド） | CLI/TUIコード |
| **Gear** | _"The best CI/CD is the one nobody thinks about."_ - 依存関係管理・CI/CD最適化・Docker設定・運用監視設定 | 設定ファイル |
| **Scaffold** | _"Infrastructure is the silent foundation of every dream."_ - クラウドインフラ（Terraform/CloudFormation/Pulumi）・ローカル開発環境（Docker Compose）・IaC設計 | インフラ設定 |
| **Hearth** | _"Your tools should feel like home."_ - 個人開発環境の設定職人。設定ファイル（zsh/tmux/neovim/ghostty等）の生成・最適化・監査、dotfile管理 | 設定ファイル |
| **Hone** | _"A sharp blade cuts clean. A sharp config cuts friction."_ - AI CLI設定の監査・最適化エージェント（Codex CLI / Antigravity CLI / Claude Code）。公式ベストプラクティスをWeb収集し、config.toml/settings.json/CLAUDE.md/GEMINI.md/AGENTS.md/permissions/commands/hooks/rules/MCP/extensionsを分析、Before/After diff形式で改善提案。設定は直接編集しない | 監査レポート、改善提案 |
| **Latch** | _"Every event is an opportunity. Hook it before it slips away."_ - Claude Codeフック専門。PreToolUse/PostToolUse/Stop/SessionStart等のイベントフックの提案・設定・デバッグ・保守。ワークフロー自動化、品質ゲート、セキュリティ検証 | フック設定 |
| **Pipe** | _"Workflows are pipelines. Pipelines are promises."_ - GitHub Actionsワークフローの深い専門家。トリガー戦略、セキュリティ強化、パフォーマンス最適化、PR自動化、Reusable Workflow設計 | GHAワークフロー |
| **Ledger** | _"Every dollar has a story. Make it a short one."_ - FinOps／クラウドコスト最適化エージェント。IaCコードからのコスト推定、right-sizing提案、RI/SP推奨、コスト異常検知 | レポート、設定 |
| **Shift** | _"Migration is not moving. It's transforming."_ - マイグレーション＆アップグレードオーケストレーター。フレームワーク・ライブラリ・API・DB・インフラの移行をcodemod生成・段階的戦略でエンドツーエンド実行 | マイグレーション計画 |

**Hearth vs Hone vs Gear vs Scaffold vs Latch vs Pipe の役割分担**:
- **Hearth**: 個人環境（dotfiles、シェル、エディタ、ターミナル）
- **Hone**: AI CLIツール設定監査（Codex CLI `~/.codex/`、Antigravity CLI `~/.gemini/`、Claude Code `~/.claude/` 設定）
- **Gear**: プロジェクトレベルのDevOps（CI/CD、Docker、監視、Gitフック）
- **Scaffold**: インフラプロビジョニング（クラウド、Docker Compose、IaC）
- **Latch**: Claude Codeイベントフック（settings.jsonフックによるワークフロー自動化）
- **Pipe**: GitHub Actionsワークフロー（高度なGHA設計、Reusable Workflow、セキュリティ）

### 国際化

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Polyglot** | _"Every language deserves respect. Every user deserves their mother tongue."_ - i18n対応。ハードコード文字列をt()関数に置換・Intl APIで日付/通貨フォーマット | i18n対応 |

### 成長

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Growth** | _"Traffic without conversion is just expensive vanity."_ - SEO（meta/OGP/JSON-LD）・SMO（SNSシェア表示）・CRO（CTA改善） | 成長施策 |
| **Bond** | _"Acquisition is expensive. Retention is profitable."_ - リテンション施策・再エンゲージメント・チャーン予防。ゲーミフィケーション、習慣形成デザイン | リテンション施策 |
| **Funnel** | _"Above the fold is your one shot. Make every pixel convert."_ - LP（ランディングページ）構造設計・コンバージョン戦略スペシャリスト。フレームワーク（AIDA/PAS/BAB/4Ps）に基づく構造設計、ヒーローセクション、CTA配置戦略、Social Proof階層、モバイルファーストのレスポンシブ実装 | LP構造、コピー、仕様 |
| **Crest** | _"Your brand is what people say when you're not in the room."_ - エンジニアセルフブランディング戦略家。GitHub/LinkedIn/ブログ/カンファレンス/SNSのポジショニング・プロフィール最適化・コンテンツ戦略 | ブランディング戦略 |

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
| **Vector** | _"The browser is a stage. Every click is a scene."_ - Playwright/Chrome DevToolsによるブラウザ操作自動化。データ収集、フォーム操作、スクリーンショット取得、ネットワーク監視 | 自動化スクリプト |
| **Haul** | _"The right image at the right resolution. Provenance you can stand behind."_ - 商品画像探索・高精度ダウンロードスペシャリスト。ECサイトAPI/画像検索/ブランドサイトのマルチソース集約、SKU/JAN/UPCマッチング、知覚ハッシュによる重複排除、ライセンスを意識したキュレーション | 画像マニフェスト・正規化された素材 |
| **Director** | _"A demo that moves hearts moves products."_ - Playwright E2Eテストを活用した機能デモ動画の自動撮影。シナリオ設計、撮影設定、実装パターン、品質チェックリストを提供 | デモ動画(.webm) |
| **Reel** | _"The terminal is a stage. Every keystroke is a performance."_ - VHS/terminalizer/asciinemaを使用したターミナル録画・CLIデモ動画生成。宣言的な.tapeファイルでGIF/MP4/WebMを作成 | GIF/動画(.gif/.mp4) |

**Anvil → Reel → Quill の連携**：Anvil（CLI開発）→ Reel（デモ録画）→ Quill（README GIF埋め込み）
**Director + Reel → Vitrine の連携**：Director（Web録画）+ Reel（ターミナル録画）→ Vitrine（ビジュアルドキュメント）
**Director vs Reel の役割分担**:
- **Director**: ブラウザ（Web UI）のデモ動画（Playwright、.webm出力）
- **Reel**: ターミナル（CLI）のデモ録画（VHS、GIF/MP4出力）

### AITuber/ストリーミング

| エージェント | 説明 | 出力 |
|------------|------|------|
| **Aether** | _"The stage is live. The avatar breathes. The audience connects."_ - AITuber（AI VTuber）フルスタック・オーケストレーター。リアルタイム配信パイプライン（Chat→LLM→TTS→Avatar→OBS）の設計・構築、ライブチャット統合、TTS音声合成、Live2D/VRMアバター制御、リップシンク、OBS WebSocket自動化 | パイプライン設計、配信設定 |

**Cast → Aether → Builder の連携**：Cast（ペルソナ）→ Aether（AITuberパイプライン設計）→ Builder（実装）
**Aether → Scaffold → Gear の連携**：Aether（配信インフラ）→ Scaffold（プロビジョニング）→ Gear（CI/CD）

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
| UI/figma-make | Figma Make Guidelines | Loom → Artisan |

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
| DOCS/convert | フォーマット変換 | Morph |
| DOCS/report | PR報告書 | Harvest → Morph |
| DOCS/learning | 変更ベース学習資料 | Tome |
| DOCS/onboarding | オンボーディング教材 | Trail → Tome |

#### デモ・録画

| タスク | 説明 | チェーン |
|--------|------|----------|
| DEMO/cli | CLIデモGIF作成 | Anvil → Reel → Quill |
| DEMO/prototype | プロトタイプデモ | Forge → Reel → Growth |
| DEMO/web-terminal | Web＋ターミナル複合デモ | Director + Reel → Vitrine |
| DEMO/docs | ドキュメント用デモ | Scribe → Reel → Quill |
| DEMO/ci-update | CI連携デモ自動更新 | Gear → Reel → Gear |
| DEMO/showcase | プロダクションCLIデモ | Builder → Reel → Growth |

#### インフラ・DevOps

| タスク | 説明 | チェーン |
|--------|------|----------|
| INFRA/ci | CI/CD構築 | Gear → Radar |
| INFRA/cloud | クラウド構築 | Scaffold → Gear |
| INFRA/cli | CLI開発 | Anvil → Radar |

#### デプロイ・リリース

| タスク | 説明 | チェーン |
|--------|------|----------|
| DEPLOY/release | リリース実行 | Guardian → Launch |
| DEPLOY/full | 完全パイプライン | Radar → Guardian → Launch → Harvest |

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
| STRATEGY/retention | リテンション施策 | Bond → Spark → Builder → Radar |
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

#### プロダクトライフサイクル（Titan）

| タスク | 説明 | チェーン |
|--------|------|----------|
| PROJECT/full | 曖昧なゴールからプロダクト完成 | Titan（9フェーズライフサイクル、Nexus経由） |
| PROJECT/mvp | MVP重視のデリバリー | Titan（DISCOVER→BUILD→VALIDATE→LAUNCH） |

> **Titan vs Nexus**: Titan = プロダクトレベルのオーケストレーション（何を、いつ、どのエージェントで）。Nexus = タスクレベルの実行（各タスクでどうチェーンを組むか）。TitanはNexusにタスクチェーンを発行する。

#### その他

| タスク | 説明 | チェーン |
|--------|------|----------|
| INCIDENT | 障害対応 | Triage → Scout → Builder |
| TEST/quality | 品質反復改善 | Judge → Zen → Radar |
| SECURITY/concurrency | 並行性バグ検出 | Specter → Builder → Radar |
| INVESTIGATE/regression | リグレッション調査 | Trail → Scout → Builder → Radar |

#### メッセージング・リアルタイム

| タスク | 説明 | チェーン |
|--------|------|----------|
| MESSAGING/bot | Bot開発 | Relay → Builder → Radar |
| MESSAGING/webhook | Webhookハンドラ | Gateway → Relay → Builder → Radar |
| MESSAGING/realtime | リアルタイム通信 | Relay → Scaffold → Builder → Radar |
| MESSAGING/multi-channel | マルチチャネル統合 | Relay → Builder → Radar |

#### AITuber/ストリーミング

| タスク | 説明 | チェーン |
|--------|------|----------|
| AITUBER/setup | AITuberパイプライン構築 | Cast → Aether → Builder → Radar |
| AITUBER/avatar | アバター＆リップシンク設定 | Aether → Builder |
| AITUBER/streaming | 配信自動化 | Aether → Gear → Builder |

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
├── aether/SKILL.md    # AITuber/ストリーミング・オーケストレーター
├── architect/SKILL.md  # エージェント設計メタデザイナー
├── anvil/SKILL.md      # CLI/TUI構築
├── artisan/SKILL.md    # フロントエンド実装
├── atelier/SKILL.md    # デザイン-実装パイプラインオーケストレーター
├── atlas/SKILL.md      # アーキテクチャ
├── attest/SKILL.md     # 仕様適合検証
├── beacon/SKILL.md     # 可観測性/SRE
├── bolt/SKILL.md       # パフォーマンス
├── builder/SKILL.md    # 本番実装
├── canvas/SKILL.md     # 可視化
├── canon/SKILL.md      # 世界標準・業界標準準拠検証
├── cast/SKILL.md       # ペルソナキャスティング＆レジストリ管理
├── compass/SKILL.md    # スキルエコシステムナビゲーター・オンボーディングガイド
├── compete/SKILL.md    # 競合調査
├── darwin/SKILL.md     # エコシステム自己進化オーケストレーター
├── director/SKILL.md   # デモ動画撮影
├── dot/SKILL.md        # ピクセルアート生成（SVG/Canvas/Phaser 3）
├── echo/SKILL.md       # ペルソナ検証
├── experiment/SKILL.md # A/Bテスト設計
├── flow/SKILL.md       # アニメーション
├── forge/SKILL.md      # プロトタイプ
├── funnel/SKILL.md     # LP構造設計・コンバージョン戦略
├── frame/SKILL.md      # Figmaデザイン・コード変換ブリッジ
├── gauge/SKILL.md      # SKILL.md正規化監査・自己進化
├── gateway/SKILL.md    # API設計
├── gear/SKILL.md       # DevOps
├── grove/SKILL.md      # リポジトリ構造設計
├── growth/SKILL.md     # SEO/CRO
├── guardian/SKILL.md   # Git/PR管理
├── harvest/SKILL.md    # PR情報収集・レポート生成
├── hearth/SKILL.md     # 個人開発環境設定
├── helm/SKILL.md       # 経営戦略シミュレーション
├── hone/SKILL.md       # Codex CLI設定監査・最適化
├── judge/SKILL.md      # コードレビュー（codex review）
├── latch/SKILL.md      # Claude Codeフック管理
├── launch/SKILL.md     # リリース管理
├── lens/SKILL.md       # コードベース理解・調査
├── levy/SKILL.md       # 確定申告ガイド
├── lore/SKILL.md       # エコシステム横断知識キュレーター
├── bazaar/SKILL.md       # 最高品質LP制作スタジオチェーン・オーケストレーター
├── magi/SKILL.md       # 多角的意思決定
├── matrix/SKILL.md     # ユニバーサル多次元分析
├── mend/SKILL.md       # 既知障害パターン自動修復
├── morph/SKILL.md      # ドキュメントフォーマット変換
├── muse/SKILL.md       # デザイン
├── vector/SKILL.md  # ブラウザ自動化
├── nexus/SKILL.md      # オーケストレーター
├── oracle/SKILL.md     # AI/ML設計・評価
├── orbit/SKILL.md      # Nexus-autoloop完走スペシャリスト
├── palette/SKILL.md    # UX
├── polyglot/SKILL.md   # i18n
├── pipe/SKILL.md       # GitHub Actionsワークフロー設計
├── probe/SKILL.md      # セキュリティ動的テスト（DAST）
├── prose/SKILL.md      # UXライティング＆コンテンツ戦略
├── pulse/SKILL.md      # メトリクス設計
├── quill/SKILL.md      # ドキュメント
├── radar/SKILL.md      # テスト
├── rally/SKILL.md      # マルチセッション並列オーケストレーター
├── relay/SKILL.md      # メッセージング統合・リアルタイム通信
├── field/SKILL.md # ユーザーリサーチ
├── ripple/SKILL.md     # 変更前影響分析
├── bond/SKILL.md     # リテンション
├── trail/SKILL.md     # Git履歴調査
├── riff/SKILL.md       # インタラクティブ・ブレインストーミング
├── sage/SKILL.md       # YC オフィスアワー流アドバイザリー
├── scaffold/SKILL.md   # インフラ
├── schema/SKILL.md     # DBスキーマ設計
├── scribe/SKILL.md     # プロジェクトドキュメント（PRD/SRS/設計書）
├── accord/SKILL.md     # 3チーム横断統合仕様パッケージ
├── scout/SKILL.md      # バグ調査
├── sentinel/SKILL.md   # セキュリティ静的分析（SAST）
├── sherpa/SKILL.md     # タスク分解
├── sigil/SKILL.md      # 動的プロジェクト固有スキル生成
├── vitrine/SKILL.md   # Storybookストーリー管理
├── sketch/SKILL.md     # AI画像生成（Gemini API）
├── spark/SKILL.md      # 機能提案
├── siege/SKILL.md      # 高度テスト（負荷/契約/カオス/ミューテーション/並行性）
├── stream/SKILL.md     # データパイプライン
├── sweep/SKILL.md      # 不要コード検出
├── titan/SKILL.md      # プロダクトライフサイクル統括
├── tome/SKILL.md       # 変更→学習ドキュメント変換
├── tone/SKILL.md       # ゲームオーディオ生成
├── trace/SKILL.md      # セッションリプレイ分析
├── triage/SKILL.md     # 障害対応
├── tuner/SKILL.md      # DBパフォーマンス最適化
├── vision/SKILL.md     # クリエイティブディレクション
├── void/SKILL.md       # YAGNI検証・複雑性削減
├── voice/SKILL.md      # ユーザーフィードバック
├── voyager/SKILL.md    # E2Eテスト
└── zen/SKILL.md        # リファクタリング
```

## 使用例

### 単一エージェントの使用

> カテゴリ別に全135エージェントの使用例を紹介します。

#### オーケストレーション

##### チェーン設計（Nexus）

```
/Nexus
ログイン機能を実装したいのですが、どのような手順で進めればよいですか？
```

**出力**: タスク分類（FEATURE/M）、推奨チェーン（Sherpa → Forge → Builder → Radar）、最初のステップのプロンプト

---

##### タスク分解（Sherpa）

```
/Sherpa
決済機能の実装タスクが複雑で整理できません。分解してください。
```

**出力**: 15分以内で完了できるAtomic Stepのリスト、進捗チェックリスト、最初に着手すべきタスクの具体的指示

---

##### エージェント設計（Architect）

```
/Architect
入力バリデーション専門のエージェントを設計してください。
Zod/Yupによるスキーマ検証、エラーメッセージ生成を担当させたいです。
```

**出力**: SKILL.md（完全な仕様書）、reference/*.md（3-7個のドメイン固有知識ファイル）、Nexus統合設計

---

##### プロダクトデリバリー（Titan）

```
/Titan
チーム協業機能付きのタスク管理SaaSアプリケーションを作ってください。
```

**出力**: 9フェーズのプロダクトライフサイクル実行 — 市場分析、アーキテクチャ設計、Rally経由の並列実装、セキュリティ強化、E2E検証、ドキュメント作成、リリース準備。全決定を自律的に記録。

---

##### プロジェクトスキル生成（Sigil）

```
/Sigil
このプロジェクトを分析して、チームに役立つスキルを生成してください。
```

**出力**: Tech stack分析、スキル機会発見、Micro/Fullスキルを`.claude/skills/`に生成（例: new-page, new-api-route, deploy-flow）

---

##### 特定スキル作成（Sigil）

```
/Sigil
このExpressプロジェクトの新しいAPIルート作成スキルを生成して。
```

**出力**: プロジェクトの既存パターン・規約に沿った`new-route.md`スキル（テンプレート付き）

---

**Architect vs Sigil の役割分担**:
- **Architect**: エコシステム普遍的エージェントを設計（400-1400行、SKILL.md）
- **Sigil**: プロジェクト固有スキルを文脈から生成（10-400行、.claude/skills/）

---

##### 自律ループ完走スクリプト（Orbit）

```
/Orbit
Nexus autoloopでステージング環境のデプロイと検証を行う完走スクリプトを生成してください。
テスト失敗時にはループを停止するようにしてください。
```

**出力**: 停止条件付きランナースクリプト、運用契約（SLA/予算/ガードレール）、監査チェックリスト

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

##### セッションリプレイ分析（Trace）

```
/Trace
チェックアウトフローでの離脱率が高いです。実際のセッションデータを分析してください。
```

**出力**: フラストレーションシグナル検出、ペルソナ別行動パターン、UX問題レポート

---

##### ペルソナ検証（Trace）

```
/Trace
Researcherが定義した「モバイルファースト・ミレニアル」ペルソナを実データで検証してください。
```

**出力**: ペルソナ定義の妥当性検証、サブセグメント発見、Field へのハンドオフ

**Trace vs Echo vs Field の役割分担**:
- **Field**: ペルソナを作成する（インタビュー・調査から）
- **Trace**: ペルソナを実データで検証する（セッションログから）
- **Echo**: ペルソナになりきってUIを検証する（シミュレーション）

---

##### ペルソナキャスティング（Cast）

```
/Cast
アナリティクスデータとサポートチケットから、ECプラットフォーム用のユーザーペルソナを5つ生成してください。
EchoとResearcherで使えるようにペルソナレジストリに登録してください。
```

**出力**: ペルソナカード（属性、目標、不満、技術習熟度）、統一フォーマットのレジストリエントリ、下流エージェント同期設定

---

#### Git/PR管理

##### PR準備（Guardian）

```
/Guardian
このブランチの変更をPRにする前に、コミット構造とPR戦略を提案してください。
```

**出力**: 変更のSignal/Noise分析、コミット分割計画、ブランチ命名提案、PR説明文ドラフト

---

##### コミット分割（Guardian）

```
/Guardian
47ファイルの変更があります。適切なコミット粒度に分割してください。
```

**出力**: 論理的な単位ごとのコミット分割計画、git addコマンド例

---

##### ブランチ命名（Guardian）

```
/Guardian
「ユーザー認証にOAuth2を追加する」タスクのブランチ名を提案してください。
```

**出力**: 規約に準拠したブランチ名候補（feat/oauth2-integration等）

---

**Guardian vs Judge vs Zen の役割分担**:
- **Guardian**: PR準備（変更分析、コミット構造、ブランチ命名）
- **Judge**: PRレビュー（バグ検出、問題指摘）
- **Zen**: コード修正（リファクタリング、品質改善）

---

##### 週次作業報告（Harvest）

```
/Harvest
今週のPR活動をサマリーレポートにまとめてください。
```

**出力**: 今週のPR統計、カテゴリ分布、貢献者ランキング、ハイライトを含むMarkdownレポート

---

##### リリースノート生成（Harvest）

```
/Harvest
v1.1.0からv1.2.0までのPRからリリースノートを生成してください。
```

**出力**: Features/Bug Fixes/Improvements/Breaking Changesに分類されたChangelog形式のリリースノート

---

##### 個人作業報告（Harvest）

```
/Harvest
@usernameの今月の作業報告書を作成してください。
```

**出力**: 特定ユーザーのPR活動詳細、カテゴリ別内訳、週次推移、ハイライト

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

##### リファクタリング（Zen）

```
/Zen
このファイルの可読性が低いのでリファクタリングしてください。
```

**出力**: 責務ごとに分割された読みやすいコード（動作は変えない）

**Note**: レビュー系エージェントの役割分担
- **Judge**: codex reviewでPRレビュー・バグ検出・AI幻覚検出（コード修正しない）
- **Zen**: コード品質の**改善**（リファクタリング、可読性向上）

---

##### YAGNI検証（Void）

```
/Void
このヘルパーユーティリティは本当に必要ですか？6ヶ月前に追加されましたが、使われているか不明です。
```

**出力**: Cost-of-Keeping Score、影響範囲分析、REMOVE/SIMPLIFY/DEFER/KEEP推奨を含むSubtraction Proposal

---

#### 実装

##### 本番実装（Builder）

```
/Builder
プロトタイプは動作しますが、本番環境に適した品質に仕上げてください。
```

**出力**: 型安全化、エラーハンドリング、バリデーション追加されたプロダクションコード

**Builder の強化機能**:
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

##### Storybookストーリー作成（Vitrine）

```
/Vitrine
新しく作成したButtonコンポーネントのStorybookストーリーを作成してください。
```

**出力**: CSF 3.0形式のStoryファイル（全バリアント、インタラクションテスト、autodocs）

**Vitrine の主な機能**:
- **CREATE**: 新規コンポーネントのストーリー作成
- **MAINTAIN**: 既存ストーリーの更新・CSF3移行
- **AUDIT**: ストーリーカバレッジと品質の監査

---

##### Storybookカバレッジ監査（Vitrine）

```
/Vitrine
現在のStorybookカバレッジを監査してください。不足しているストーリーを特定してください。
```

**出力**: カバレッジレポート、品質スコア、改善アクションリスト

---

##### Figma Make最適化（Loom）

```
/Loom
このプロジェクトのコードベースを分析して、Figma Make用のGuidelines.mdを生成してください。
```

**出力**: コードベースのデザインシステム分析、Figma Make最適化 Guidelines.md、プロンプト戦略

**Frame vs Loom の使い分け**:
- **Frame**: Figmaのデザインからコード実装へ（Figma → Code）
- **Loom**: コードベースからFigma Make入力の最適化へ（Code → Figma Make）

---

#### ドキュメント

##### PRD作成（Scribe）

```
/Scribe
ユーザー認証機能のPRD（Product Requirements Document）を作成してください。
ソーシャルログイン対応、二要素認証をスコープに含めます。
```

**出力**: 完全なPRD（概要、ユーザーストーリー、機能要件、非機能要件、受入条件、エッジケース）

---

##### SRS作成（Scribe）

```
/Scribe
決済モジュールのSRS（Software Requirements Specification）を作成してください。
Stripe連携、サブスクリプション対応が必要です。
```

**出力**: 完全なSRS（機能要件、データモデル、API仕様、非機能要件、トレーサビリティマトリクス）

---

##### 実装チェックリスト作成（Scribe）

```
/Scribe
検索機能の実装チェックリストを作成してください。
```

**出力**: 実装前確認、実装フェーズ別タスク、品質保証チェック、デプロイ前確認

---

##### テスト仕様書作成（Scribe）

```
/Scribe
注文フローのテスト仕様書を作成してください。
正常系・異常系・境界値を網羅してください。
```

**出力**: テストケース一覧（ID、優先度、手順、期待結果）、テストデータ、トレーサビリティ

---

**Scribe vs Quill の役割分担**:
- **Scribe**: プロジェクトドキュメント（仕様書、設計書、チェックリスト）
- **Quill**: コードドキュメント（JSDoc、README、型定義）

---

##### 学習ドキュメント生成（Tome）

```
/Tome
このPRの変更内容を中級者向けの学習ドキュメントとして解説してください。
```

**出力**: 用語集、Before/After比較、設計判断記録、アンチパターン警告を含む学習ドキュメント

---

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

##### AI画像生成コード作成（Sketch）

```
/Sketch
Gemini APIを使って商品サムネイル画像を生成するPythonコードを作成してください。
複数商品のバッチ生成にも対応してください。
```

**出力**: Gemini API連携のプロダクション品質Pythonコード、プロンプト最適化、バッチ処理、コスト見積もり

---

##### ピクセルアート生成（Dot）

```
/Dot
16x16のプレイヤーキャラクタースプライトを4フレームの歩行アニメーション付きで作成してください。
16色パレットで、SVGとスプライトシートメタデータを出力してください。
```

**出力**: SVGスプライトコード、スプライトシートレイアウト、アニメーションメタデータJSON、パレット定義

---

**Canvas vs Sketch vs Dot の役割分担**:
- **Canvas**: 図表・チャート（Mermaid、ASCIIアート、draw.io）
- **Sketch**: AI画像生成コード（Gemini API向けPythonコード）
- **Dot**: ピクセルアートをコードで生成（SVG/Canvas/Phaser 3/Pillow/CSSスプライト）
- **Clay**: AI 3Dモデル生成コード（Meshy/Tripo/Hunyuan3D/Rodin/Sloyd/Stability API向けPython/JS/OpenSCAD）

---

##### NotebookLMプロンプト設計（Prism）

```
/Prism
APIドキュメントをNotebookLMで魅力的なポッドキャスト風音声にしたいです。
最適なステアリングプロンプトを設計してください。
```

**出力**: 最適化されたステアリングプロンプト、ソース準備のアドバイス、出力フォーマット推奨

---

#### アーキテクチャ

##### アーキテクチャ分析（Atlas）

```
/Atlas
コードの依存関係を分析し、変更時の影響範囲を明確にしてください。
```

**出力**: 依存関係マップ、問題箇所の特定、改善のためのADR/RFC

---

##### モダナイゼーション（Shift）

```
/Shift detect
使用しているライブラリのバージョンを確認し、非推奨や脆弱性のあるものを特定してください。
```

**出力**: 非推奨ライブラリの検出、代替案の提案、移行PoC（ネイティブAPI置換は `Shift modernize`、技術成熟度評価は `Shift radar`）

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

##### AI CLI設定監査（Hone）

```
/Hone
Codex CLIの設定を監査して、最新のベストプラクティスに基づく最適化を提案してください。

/Hone
Antigravity CLIのsettings.jsonとsafety settingsをベストプラクティスに基づいて監査してください。

/Hone
Claude Codeのpermissionsとmcp server設定をセキュリティベストプラクティスに基づいて監査してください。
```

**出力**: Before/After diff形式の改善提案、優先度分類、安全性ラベル付き監査レポート

---

##### 個人開発環境設定（Hearth）

```
/Hearth
zshの起動が遅いので最適化してください。補完も改善したいです。
```

**出力**: 起動プロファイリング付きの最適化された.zshrc、プラグイン遅延読み込み、補完設定

---

##### dotfile管理（Hearth）

```
/Hearth
neovimのLSP対応設定をlazy.nvimプラグイン管理で構築してください。
```

**出力**: init.lua構成、lazy.nvimセットアップ、LSP設定、キーバインド

**Hearth vs Hone vs Gear vs Scaffold vs Latch の役割分担**:
- **Hearth**: 個人環境（dotfiles、シェル、エディタ、ターミナル）
- **Hone**: AI CLIツール設定監査（Codex CLI `~/.codex/`、Antigravity CLI `~/.gemini/`、Claude Code `~/.claude/` 設定）
- **Gear**: プロジェクトレベルのDevOps（CI/CD、Docker、監視、Gitフック）
- **Scaffold**: インフラプロビジョニング（クラウド、Docker Compose、IaC）
- **Latch**: Claude Codeイベントフック（settings.jsonフックによるワークフロー自動化）
- **Pipe**: GitHub Actionsワークフロー設計（トリガー、セキュリティ、パフォーマンス、PR自動化）

---

##### GitHub Actionsワークフロー設計（Pipe）

```
/Pipe
このモノレポ用のCI/CDワークフローを設計してください。パスベースのトリガー、パッケージごとの並列ジョブ、SHA固定のアクションが必要です。
```

**出力**: パスフィルター付きGitHub Actionsワークフロー YAML、ジョブ依存関係グラフ、セキュリティ強化された権限設定、キャッシュ戦略

---

##### CIセキュリティ強化（Pipe）

```
/Pipe
GitHub Actionsワークフローのセキュリティ問題を監査してください。権限、アクションの固定、シークレットの取り扱いを確認して。
```

**出力**: セキュリティ監査レポート、SHA固定アクションによる改善計画、最小権限設定、OIDC推奨事項

---

##### Claude Codeフック設定（Latch）

```
/Latch
.envファイルへの書き込みを防止し、停止前にテスト実行を強制するフックを追加してください。
```

**出力**: settings.jsonのフック設定（PreToolUseによるファイル保護、Stopによるテスト強制）、バックアップ作成、再起動リマインド

---

##### フックデバッグ（Latch）

```
/Latch
PreToolUseフックが発火しません。デバッグを手伝ってください。
```

**出力**: 診断チェックリスト、`claude --debug`分析、手動テストコマンド、修正提案

---

##### ローカル開発環境構築（Scaffold）

```
/Scaffold
新規開発者がすぐに開発を始められるようにDocker Compose環境を整備してください。
```

**出力**: docker-compose.yml、.env.example、セットアップスクリプト

---

#### コミュニケーション

##### Slack Bot開発（Relay）

```
/Relay
/remindコマンドに応答し、スケジュールされたリマインダーを送信するSlack Botを作成してください。
スレッドへの返信とスラッシュコマンドに対応してください。
```

**出力**: チャネルアダプター設計、コマンドパーサー仕様、Webhookハンドラミドルウェアチェーン、イベントルーティングマトリクス

---

##### マルチチャネル通知（Relay）

```
/Relay
SlackとDiscordの両方にアラートを送信する通知システムを設計してください。
各プラットフォームのネイティブフォーマットで表示すること。
```

**出力**: 統一メッセージスキーマ、プラットフォーム固有アダプター、ファンアウトルーティング設計

---

**Relay vs Gateway vs Stream の役割分担**:
- **Relay**: メッセージングプラットフォーム統合（チャネルアダプター、Webhook、WebSocket、Bot）
- **Gateway**: REST/GraphQL API設計（OpenAPI仕様、バージョニング、エンドポイント）
- **Stream**: データパイプライン（ETL/ELT、Kafka、Airflow、バッチ処理）

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

##### リテンション施策（Bond）

```
/Bond
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

##### ユーザーリサーチ設計（Field）

```
/Field
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

#### ターミナル録画

##### CLIデモGIF作成（Reel）

```
/Reel
このCLIツールのインストールから基本的な使い方までをGIFで録画してください。
READMEに埋め込みます。
```

**出力**: VHS .tapeファイル、最適化済みGIF（5MB以下）、Markdown埋め込みコード

---

##### ターミナルセッション録画（Reel）

```
/Reel
インタラクティブなセットアップウィザードの動作をデモ動画にしてください。
ユーザーが選択肢を選ぶ様子を含めてください。
```

**出力**: terminalizer録画、YAML編集済み、GIF出力

---

**Director vs Reel の役割分担**:
- **Director**: ブラウザ（Web UI）のデモ動画（Playwright、.webm出力）
- **Reel**: ターミナル（CLI）のデモ録画（VHS/terminalizer/asciinema、GIF/MP4出力）

---

#### AITuber/ストリーミング

##### AITuberパイプライン設計（Aether）

```
/Aether
AITuberシステムを設計してください：YouTube Liveチャット → LLM応答 → VOICEVOX TTS → Live2Dアバター（リップシンク付き） → OBS配信。
```

**出力**: パイプラインアーキテクチャ、コンポーネント設定（チャットポーラー、LLMアダプター、TTS設定、アバター制御、OBS WebSocket）、デプロイガイド

---

##### 配信自動化（Aether）

```
/Aether
AI VTuber配信中のシーン切替、BGM制御、チャットオーバーレイのOBS WebSocket自動化を設定してください。
```

**出力**: OBS WebSocket設定、シーン切替ロジック、イベント駆動自動化スクリプト

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
